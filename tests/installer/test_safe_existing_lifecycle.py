import tempfile
import unittest
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.domain.models import ActualState
from ai_rules.domain.statuses import InstalledOwnership, ReconciliationAction, Scope
from ai_rules.execution import copy_tree_atomic, tree_identity
from ai_rules.interactive import prompt_existing_migration
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver


class SafeExistingLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.profiles = load_profiles(self.catalog)

    def test_matching_unmanaged_first_party_can_be_explicitly_adopted(self):
        """Fails if a content-verified local skill is still blocked after adopt approval."""
        state = {
            ("andino-workflow", "codex", Scope.GLOBAL.value): ActualState(
                exists=True,
                ownership=InstalledOwnership.UNKNOWN_ORIGIN,
                healthy=True,
                content_matches=True,
            )
        }
        plan = build_resolver(self.catalog, self.profiles, StaticCapabilityAdapter(state=state)).resolve(
            ResolveRequest(hosts=("codex",), profile_id="minimal", allow_adopt=True)
        )

        target = plan.targets[0]
        self.assertEqual(ReconciliationAction.ADOPT, target.action)
        self.assertEqual("adopt_existing", target.operations[0].kind)

    def test_different_unmanaged_first_party_requires_explicit_replace(self):
        """Fails if a differing local skill is ever replaced without a specific decision."""
        state = {
            ("andino-workflow", "codex", Scope.GLOBAL.value): ActualState(
                exists=True,
                ownership=InstalledOwnership.UNKNOWN_ORIGIN,
                healthy=True,
                content_matches=False,
            )
        }
        resolver = build_resolver(self.catalog, self.profiles, StaticCapabilityAdapter(state=state))

        blocked = resolver.resolve(ResolveRequest(hosts=("codex",), profile_id="minimal"))
        replace = resolver.resolve(
            ResolveRequest(hosts=("codex",), profile_id="minimal", allow_replace=True)
        )

        self.assertEqual(ReconciliationAction.BLOCK, blocked.targets[0].action)
        self.assertEqual(ReconciliationAction.REPLACE, replace.targets[0].action)

    def test_tree_identity_includes_every_file_content(self):
        """Fails if adoption checks only for SKILL.md instead of the whole bundle tree."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            expected = root / "expected"
            existing = root / "existing"
            for path in (expected, existing):
                path.mkdir()
                (path / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
                (path / "support.txt").write_text("same\n", encoding="utf-8")

            self.assertEqual(tree_identity(expected), tree_identity(existing))
            (existing / "support.txt").write_text("modified\n", encoding="utf-8")
            self.assertNotEqual(tree_identity(expected), tree_identity(existing))

    def test_replace_creates_unique_backup_and_rolls_back_post_replace_failure(self):
        """Fails if a failed replacement loses the prior skill or reuses a backup directory."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            target = root / "skills" / "andino-workflow"
            source.mkdir()
            target.mkdir(parents=True)
            (source / "SKILL.md").write_text("# New\n", encoding="utf-8")
            (target / "SKILL.md").write_text("# Old\n", encoding="utf-8")

            calls = 0

            def fail_installed_verification(_path: Path) -> bool:
                nonlocal calls
                calls += 1
                return calls < 3

            with self.assertRaises(RuntimeError):
                copy_tree_atomic(source, target, root / "backups", verify=fail_installed_verification)

            self.assertEqual("# Old\n", (target / "SKILL.md").read_text(encoding="utf-8"))
            backups = list((root / "backups").glob("*/andino-workflow/SKILL.md"))
            self.assertEqual(1, len(backups))
            self.assertEqual("# Old\n", backups[0].read_text(encoding="utf-8"))

    def test_cli_adopt_and_replace_flags_require_explicit_migration_decisions(self):
        """Fails if CLI migration flags either rewrite an exact match or fail to back up a replacement."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "project"
            state = root / "state"
            target = project / ".agents" / "skills" / "andino-workflow"
            base = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(project), "--state-dir", str(state),
                "--yes", "--non-interactive",
            ]
            installed = subprocess.run(base, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, installed.returncode, installed.stderr)
            original_identity = tree_identity(target)
            (state / "managed-installations.json").unlink()

            adopted = subprocess.run([*base, "--adopt-existing"], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, adopted.returncode, adopted.stderr)
            self.assertIn("APPLIED ADOPT", adopted.stdout)
            self.assertEqual(original_identity, tree_identity(target))

            (target / "local-change.txt").write_text("preserve me\n", encoding="utf-8")
            (state / "managed-installations.json").unlink()
            replaced = subprocess.run([*base, "--replace-existing"], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, replaced.returncode, replaced.stderr)
            self.assertIn("APPLIED REPLACE", replaced.stdout)
            self.assertFalse((target / "local-change.txt").exists())
            backups = list((state / "backups").glob("*/andino-workflow/local-change.txt"))
            self.assertEqual(1, len(backups))

    def test_managed_content_drift_is_repaired(self):
        """Fails if a managed skill with a modified support file is falsely reported current."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "project"
            state = root / "state"
            command = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(project), "--state-dir", str(state),
                "--yes", "--non-interactive",
            ]
            first = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, first.returncode, first.stderr)
            modified = project / ".agents" / "skills" / "andino-workflow" / "local-change.txt"
            modified.write_text("drift\n", encoding="utf-8")

            repaired = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, repaired.returncode, repaired.stderr)
            self.assertIn("APPLIED REPAIR", repaired.stdout)
            self.assertFalse(modified.exists())

    def test_interactive_migration_keeps_differing_installations_by_default(self):
        """Fails if the interactive replacement choice defaults to overwriting local files."""
        state = {
            ("andino-workflow", "codex", Scope.GLOBAL.value): ActualState(
                exists=True, ownership=InstalledOwnership.UNKNOWN_ORIGIN, content_matches=False
            )
        }
        plan = build_resolver(self.catalog, self.profiles, StaticCapabilityAdapter(state=state)).resolve(
            ResolveRequest(hosts=("codex",), profile_id="minimal")
        )

        class Answer:
            def __init__(self, value):
                self.value = value

            def ask(self):
                return self.value

        with patch("questionary.select", return_value=Answer("keep")) as select:
            self.assertEqual((False, False), prompt_existing_migration(plan))
        self.assertTrue(select.called)

    def test_verified_existing_context7_can_be_explicitly_adopted(self):
        """Fails if a URL-verified external integration remains blocked after adoption approval."""
        state = {
            ("context7", "codex", Scope.GLOBAL.value): ActualState(
                exists=True, ownership=InstalledOwnership.EXTERNAL_EXISTING, content_matches=True
            )
        }
        plan = build_resolver(self.catalog, self.profiles, StaticCapabilityAdapter(state=state)).resolve(
            ResolveRequest(hosts=("codex",), capabilities=("context7",), allow_adopt=True)
        )

        self.assertEqual(ReconciliationAction.ADOPT, plan.targets[0].action)


if __name__ == "__main__":
    unittest.main()
