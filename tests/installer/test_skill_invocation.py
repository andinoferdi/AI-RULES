import json
import tempfile
import unittest
from pathlib import Path

from ai_rules.catalog import load_catalog
from ai_rules.domain.models import ActualState, InstallationPlan, PlanTarget
from ai_rules.domain.statuses import InstalledOwnership, ReconciliationAction, ReconciliationAssessment, Scope, TargetStatus
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.hosts.invocation import (
    all_invocation_paths,
    family_members,
    family_retired,
    install_invocation,
    invocation_paths,
    invocation_ready,
    reconcile_invocations,
)


class SkillInvocationTests(unittest.TestCase):
    def test_global_host_registrations_and_native_hosts(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            adapters = build_host_adapters(load_catalog().hosts, home)
            for host in adapters.values():
                skill = host.skill_target(Scope.GLOBAL) / "skripsi-skill/SKILL.md"
                skill.parent.mkdir(parents=True, exist_ok=True)
                skill.write_text("---\nname: skripsi-skill\ndescription: Thesis\n---\nBody\n")
                install_invocation(host, Scope.GLOBAL, "skripsi-skill")
                paths = invocation_paths(host, Scope.GLOBAL, "skripsi-skill")
                self.assertTrue(all(invocation_ready(path) for path in paths))
                if host.id == "antigravity-ide":
                    self.assertEqual(2, len(paths))
                    self.assertIn(home / ".gemini/antigravity/global_workflows/skripsi-skill.md", paths)
                elif host.id != "opencode":
                    self.assertEqual((), paths)

    def test_opencode_family_invocation_installation_and_legacy_pruning(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            adapter = build_host_adapters(load_catalog().hosts, home)["opencode"]
            skills_dir = adapter.skill_target(Scope.GLOBAL)
            commands_dir = home / ".config/opencode/commands"
            commands_dir.mkdir(parents=True, exist_ok=True)

            # Pre-existing legacy manual command and retired member command
            legacy_file = commands_dir / "manual-old-debugging.md"
            legacy_file.write_text("old manual command")
            retired_file = commands_dir / "andino-delivery.md"
            retired_file.write_text("---\ndescription: old delivery\n---\nbody")

            # Setup andino-workflow and members
            wf_dir = skills_dir / "andino-workflow"
            wf_dir.mkdir(parents=True, exist_ok=True)
            (wf_dir / "SKILL.md").write_text("---\nname: andino-workflow\ndescription: Workflow Coordinator\n---\nBody\n")
            refs = wf_dir / "references"
            refs.mkdir(parents=True, exist_ok=True)
            portfolio = {
                "schema_version": 1,
                "installer_protocol": 1,
                "members": ["brainstorming", "tdd"],
                "retired": ["delivery"],
            }
            (refs / "portfolio.json").write_text(json.dumps(portfolio), encoding="utf-8")

            bs_dir = skills_dir / "andino-brainstorming"
            bs_dir.mkdir(parents=True, exist_ok=True)
            (bs_dir / "SKILL.md").write_text("---\nname: andino-brainstorming\ndescription: Brainstorming Ideas\n---\nBody\n")

            tdd_dir = skills_dir / "andino-tdd"
            tdd_dir.mkdir(parents=True, exist_ok=True)
            (tdd_dir / "SKILL.md").write_text("---\nname: andino-tdd\ndescription: Test Driven Development\n---\nBody\n")

            self.assertEqual(["andino-brainstorming", "andino-tdd"], family_members(adapter, Scope.GLOBAL, "andino-workflow"))
            self.assertEqual(["andino-delivery"], family_retired(adapter, Scope.GLOBAL, "andino-workflow"))

            # Install invocation
            install_invocation(adapter, Scope.GLOBAL, "andino-workflow")

            # Verify created member commands
            cmd_wf = commands_dir / "andino-workflow.md"
            cmd_bs = commands_dir / "andino-brainstorming.md"
            cmd_tdd = commands_dir / "andino-tdd.md"
            self.assertTrue(cmd_wf.is_file())
            self.assertTrue(cmd_bs.is_file())
            self.assertTrue(cmd_tdd.is_file())
            self.assertTrue(invocation_ready(cmd_wf))
            self.assertTrue(invocation_ready(cmd_bs))
            self.assertTrue(invocation_ready(cmd_tdd))

            # Verify extracted descriptions
            self.assertIn('description: "Brainstorming Ideas"', cmd_bs.read_text(encoding="utf-8"))
            self.assertIn('description: "Test Driven Development"', cmd_tdd.read_text(encoding="utf-8"))

            # Verify legacy manual file and retired file were pruned
            self.assertFalse(legacy_file.exists())
            self.assertFalse(retired_file.exists())

    def test_reconcile_invocations_detects_missing_member_invocation(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            catalog = load_catalog()
            adapters = build_host_adapters(catalog.hosts, home)
            adapter = adapters["opencode"]
            skills_dir = adapter.skill_target(Scope.GLOBAL)
            commands_dir = home / ".config/opencode/commands"
            commands_dir.mkdir(parents=True, exist_ok=True)

            wf_dir = skills_dir / "andino-workflow"
            wf_dir.mkdir(parents=True, exist_ok=True)
            (wf_dir / "SKILL.md").write_text("---\nname: andino-workflow\ndescription: Workflow Coordinator\n---\nBody\n")
            refs = wf_dir / "references"
            refs.mkdir(parents=True, exist_ok=True)
            portfolio = {
                "schema_version": 1,
                "installer_protocol": 1,
                "members": ["brainstorming"],
                "retired": [],
            }
            (refs / "portfolio.json").write_text(json.dumps(portfolio), encoding="utf-8")

            bs_dir = skills_dir / "andino-brainstorming"
            bs_dir.mkdir(parents=True, exist_ok=True)
            (bs_dir / "SKILL.md").write_text("---\nname: andino-brainstorming\ndescription: Brainstorming Ideas\n---\nBody\n")

            # Initially only andino-workflow.md exists; andino-brainstorming.md is missing
            install_invocation(adapter, Scope.GLOBAL, "andino-workflow")
            (commands_dir / "andino-brainstorming.md").unlink()

            target = PlanTarget(
                capability_id="andino-workflow",
                host_id="opencode",
                scope=Scope.GLOBAL,
                action=ReconciliationAction.NO_OP,
                actual=ActualState(exists=True, ownership=InstalledOwnership.MANAGED_BY_AI_RULES, healthy=True, content_matches=True),
                status=TargetStatus.VERIFIED,
                assessment=ReconciliationAssessment.CURRENT,
                strategy_id="first-party-skill-directory",
                reason="all clean",
                operations=(),
            )
            plan = InstallationPlan(schema_version=1, profile_id="test", targets=(target,))

            reconciled = reconcile_invocations(plan, catalog, adapters)
            rec_target = reconciled.targets[0]
            self.assertEqual(ReconciliationAction.RECONFIGURE, rec_target.action)
            self.assertEqual(TargetStatus.PLANNED, rec_target.status)
            self.assertIn("register missing", rec_target.reason)


if __name__ == "__main__":
    unittest.main()
