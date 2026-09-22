import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.domain.models import ActualState, InstallationPlan, Operation, PlanTarget
from ai_rules.domain.statuses import ReconciliationAction, ReconciliationAssessment, Scope, TargetStatus
from ai_rules.execution import Executor
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver
from ai_rules.state import create_snapshot, read_json, write_profile
from ai_rules.verification import doctor_from_plan


class ExecutionStateCliTests(unittest.TestCase):
    def test_executor_installs_first_party_bundle_into_disposable_host_root(self):
        """Fails if the executor records an operation without installing its skill artifact."""
        operation = Operation(
            kind="capability_operation",
            capability_id="andino-workflow",
            host_id="codex",
            scope=Scope.GLOBAL,
            action=ReconciliationAction.INSTALL,
            source="first-party",
            target="codex:global:andino-workflow",
            reason="test",
        )
        plan = InstallationPlan(
            schema_version=1,
            profile_id="minimal",
            targets=(
                PlanTarget(
                    capability_id="andino-workflow",
                    host_id="codex",
                    scope=Scope.GLOBAL,
                    action=ReconciliationAction.INSTALL,
                    assessment=ReconciliationAssessment.VERSION_UNKNOWN,
                    status=TargetStatus.PLANNED,
                    strategy_id="first-party-file",
                    reason="test",
                    operations=(operation,),
                    actual=ActualState(),
                ),
            ),
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = root / "bundle"
            bundle.mkdir()
            (bundle / "SKILL.md").write_text("# Andino Workflow\n", encoding="utf-8")
            result = Executor(
                root / "state",
                first_party_bundles={"andino-workflow": bundle},
                host_skill_roots={"codex": root / "codex-skills"},
            ).execute(plan, dry_run=False, yes=True)

            self.assertTrue((root / "codex-skills" / "andino-workflow" / "SKILL.md").exists())
            self.assertEqual("APPLIED", result.results[0].status)

    def test_dry_run_does_not_write_state(self):
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        plan = build_resolver(catalog, profiles, StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("codex",), profile_id="minimal")
        )
        with tempfile.TemporaryDirectory() as temp:
            state_dir = Path(temp) / "state"
            result = Executor(state_dir).execute(plan, dry_run=True)
            self.assertFalse(state_dir.exists())
            self.assertTrue(result.dry_run)

    def test_executor_requires_confirmation_for_mutation(self):
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        plan = build_resolver(catalog, profiles, StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("codex",), profile_id="minimal")
        )
        with tempfile.TemporaryDirectory() as temp:
            result = Executor(Path(temp)).execute(plan, dry_run=False, yes=False)
            self.assertEqual("BLOCKED", result.results[0].status)

    def test_executor_continues_independent_target_after_failed_operation(self):
        """Fails if one invalid bundle aborts later independent target operations."""
        def target(capability_id: str) -> PlanTarget:
            operation = Operation(
                kind="capability_operation", capability_id=capability_id, host_id="codex", scope=Scope.GLOBAL,
                action=ReconciliationAction.INSTALL, source="first-party", target=capability_id, reason="test",
            )
            return PlanTarget(
                capability_id=capability_id, host_id="codex", scope=Scope.GLOBAL, action=ReconciliationAction.INSTALL,
                assessment=ReconciliationAssessment.VERSION_UNKNOWN, status=TargetStatus.PLANNED,
                strategy_id="first-party-file", reason="test", operations=(operation,), actual=ActualState(),
            )

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            valid = root / "valid"
            valid.mkdir()
            (valid / "SKILL.md").write_text("# Valid\n", encoding="utf-8")
            invalid = root / "invalid"
            invalid.mkdir()
            plan = InstallationPlan(schema_version=1, profile_id=None, targets=(target("broken"), target("valid")))
            result = Executor(
                root / "state", first_party_bundles={"broken": invalid, "valid": valid},
                host_skill_roots={"codex": root / "skills"},
            ).execute(plan, dry_run=False, yes=True)
            self.assertEqual(["FAILED", "APPLIED"], [item.status for item in result.results])
            self.assertTrue((root / "skills" / "valid" / "SKILL.md").exists())

    def test_profile_and_snapshot_are_secret_free(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            profile = root / "profile.json"
            snapshot = root / "snapshot.json"
            write_profile(profile, "minimal", ("codex",), ("andino-workflow",), "global")
            create_snapshot(profile, None, snapshot)
            data = read_json(snapshot)
            self.assertEqual("desired", data["mode"])
            self.assertNotIn("secret", json.dumps(data).lower())

    def test_doctor_reports_blocked_unmanaged_state(self):
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        plan = build_resolver(catalog, profiles, StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("codex",), profile_id="recommended")
        )
        report = doctor_from_plan(plan)
        statuses = {target.capability_id: target.status.value for target in report.targets}
        self.assertEqual("MANUAL_ACTION_REQUIRED", statuses["superpowers"])

    def test_cli_setup_dry_run_smoke(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            completed = subprocess.run(
                [
                    sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                    "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                    "--dry-run", "--non-interactive",
                ],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertIn("INSTALL", completed.stdout)

    def test_cli_setup_yes_installs_first_party_skill_in_disposable_project(self):
        """Fails if CLI setup does not wire its approved plan to a real skill installation."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "ai_rules",
                    "setup",
                    "--profile",
                    "minimal",
                    "--host",
                    "codex",
                    "--scope",
                    "project",
                    "--project-root",
                    str(root / "project"),
                    "--state-dir",
                    str(root / "state"),
                    "--yes",
                    "--non-interactive",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertTrue((root / "project" / ".agents" / "skills" / "andino-workflow" / "SKILL.md").exists())

            repeated = subprocess.run(
                completed.args,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(0, repeated.returncode, repeated.stderr)
            self.assertIn("VERIFIED NO_OP", repeated.stdout)

    def test_cli_setup_without_yes_does_not_write_profile_or_managed_state(self):
        """Fails if the CLI persists desired or managed state before the required confirmation."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "ai_rules",
                    "setup",
                    "--profile",
                    "minimal",
                    "--host",
                    "codex",
                    "--scope",
                    "project",
                    "--project-root",
                    str(root / "project"),
                    "--state-dir",
                    str(root / "state"),
                    "--non-interactive",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertFalse((root / "state" / "profile.json").exists())
            self.assertFalse((root / "state" / "managed-installations.json").exists())

    def test_cli_blocks_opencode_install_when_discovery_alias_already_has_skill(self):
        """Fails if OpenCode receives a duplicate skill through its .claude discovery alias."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            duplicate = root / "project" / ".claude" / "skills" / "andino-workflow"
            duplicate.mkdir(parents=True)
            (duplicate / "SKILL.md").write_text("# Existing skill\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "opencode",
                    "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                    "--dry-run", "--non-interactive",
                ],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(1, completed.returncode, completed.stderr)
            self.assertIn("BLOCK", completed.stdout)

    def test_cli_setup_updates_older_managed_first_party_installation(self):
        """Fails if a managed installation below the release target is reclassified as install or no-op."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            command = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                "--yes", "--non-interactive",
            ]
            first = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, first.returncode, first.stderr)
            state_path = root / "state" / "managed-installations.json"
            state = read_json(state_path)
            state["installations"]["andino-workflow:codex:project"]["version"] = "release-manifest:andino-workflow@0000000#0"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            updated = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, updated.returncode, updated.stderr)
            self.assertIn("APPLIED UPDATE", updated.stdout)

    def test_cli_setup_repairs_missing_managed_skill_artifact_without_upgrade(self):
        """Fails if a managed artifact with a missing SKILL.md is not repaired in place."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            command = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                "--yes", "--non-interactive",
            ]
            first = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, first.returncode, first.stderr)
            skill_file = root / "project" / ".agents" / "skills" / "andino-workflow" / "SKILL.md"
            skill_file.unlink()

            repaired = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, repaired.returncode, repaired.stderr)
            self.assertIn("APPLIED REPAIR", repaired.stdout)
            self.assertTrue(skill_file.exists())

    def test_cli_doctor_reports_missing_managed_skill_artifact_as_failed(self):
        """Fails if doctor reports a repair plan instead of the observed broken artifact."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            setup = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                "--yes", "--non-interactive",
            ]
            first = subprocess.run(setup, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, first.returncode, first.stderr)
            (root / "project" / ".agents" / "skills" / "andino-workflow" / "SKILL.md").unlink()

            doctor = subprocess.run(
                [sys.executable, "-m", "ai_rules", "doctor", *setup[4:-2]],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(1, doctor.returncode, doctor.stderr)
            self.assertIn("FAILED", doctor.stdout)

    def test_cli_doctor_repair_restores_missing_managed_skill_artifact(self):
        """Fails if doctor --repair acknowledges drift without applying the repair operation."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            setup = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                "--yes", "--non-interactive",
            ]
            first = subprocess.run(setup, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, first.returncode, first.stderr)
            skill_file = root / "project" / ".agents" / "skills" / "andino-workflow" / "SKILL.md"
            skill_file.unlink()

            repaired = subprocess.run(
                [sys.executable, "-m", "ai_rules", "doctor", *setup[4:-2], "--repair", "--yes"],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(0, repaired.returncode, repaired.stderr)
            self.assertIn("APPLIED REPAIR", repaired.stdout)
            self.assertIn("VERIFIED", repaired.stdout)
            self.assertTrue(skill_file.exists())

    def test_cli_doctor_repair_preview_mentions_no_upgrade(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            completed = subprocess.run(
                [
                    sys.executable, "-m", "ai_rules", "doctor", "--profile", "minimal", "--host", "codex",
                    "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                    "--repair", "--dry-run",
                ],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertIn("does not upgrade versions", completed.stdout)


if __name__ == "__main__":
    unittest.main()
