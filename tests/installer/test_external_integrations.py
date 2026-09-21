from __future__ import annotations

import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from ai_rules.capabilities.adapters import StaticCapabilityAdapter, managed_state
from ai_rules.catalog import load_catalog
from ai_rules.cli import _actual_state, _managed_installation_records, _record_managed_installations
from ai_rules.domain.models import ActualState, InstallationPlan, Operation, PlanTarget
from ai_rules.domain.statuses import InstalledOwnership, ReconciliationAction, ReconciliationAssessment, Scope, TargetStatus
from ai_rules.execution import Executor, OperationResult, ExecutionResult
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver


class ExternalIntegrationTests(unittest.TestCase):
    def test_antigravity_superpowers_plan_uses_official_reinstallable_command(self):
        """Fails if the automated Superpowers path stops using Antigravity's upstream command."""
        catalog = load_catalog()
        plan = build_resolver(catalog, load_profiles(catalog), StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("antigravity-cli",), capabilities=("superpowers",))
        )

        target = plan.targets[0]
        self.assertEqual(ReconciliationAction.INSTALL, target.action)
        self.assertEqual(
            ("agy", "plugin", "install", "https://github.com/obra/superpowers"),
            target.operations[0].argv,
        )

    def test_context7_remote_registration_uses_each_host_native_cli(self):
        """Fails if Context7 loses an executable, secret-free MCP registration route for a supported CLI host."""
        catalog = load_catalog()
        plan = build_resolver(catalog, load_profiles(catalog), StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("codex", "claude-code", "opencode", "antigravity-cli"), capabilities=("context7",))
        )

        commands = {target.host_id: target.operations[0].argv for target in plan.targets}
        self.assertEqual(("codex", "mcp", "add", "context7", "--url", "https://mcp.context7.com/mcp"), commands["codex"])
        self.assertEqual(
            ("claude", "mcp", "add", "--scope", "user", "--transport", "http", "context7", "https://mcp.context7.com/mcp"),
            commands["claude-code"],
        )
        self.assertEqual(("opencode", "mcp", "add", "context7", "--url", "https://mcp.context7.com/mcp"), commands["opencode"])
        self.assertEqual(("agy", "mcp", "add", "context7", "https://mcp.context7.com/mcp"), commands["antigravity-cli"])

    def test_executor_runs_an_approved_external_command(self):
        """Fails if an approved external operation is reported applied without actually running its command."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / "command-ran.txt"
            operation = Operation(
                kind="run_command",
                capability_id="fixture-external",
                host_id="fixture-host",
                scope=Scope.GLOBAL,
                action=ReconciliationAction.INSTALL,
                source="fixture",
                target="fixture",
                reason="exercise real command execution",
                argv=(sys.executable, "-c", f"from pathlib import Path; Path(r'{marker}').write_text('ran')"),
                network=False,
            )
            target = PlanTarget(
                capability_id="fixture-external",
                host_id="fixture-host",
                scope=Scope.GLOBAL,
                action=ReconciliationAction.INSTALL,
                assessment=ReconciliationAssessment.VERSION_UNKNOWN,
                status=TargetStatus.PLANNED,
                strategy_id="fixture",
                reason="fixture",
                operations=(operation,),
                actual=ActualState(),
            )
            result = Executor(root / "state").execute(
                InstallationPlan(schema_version=1, profile_id=None, targets=(target,)), dry_run=False, yes=True
            )

            self.assertTrue(marker.is_file())
            self.assertEqual("APPLIED", result.results[0].status)

    def test_managed_superpowers_update_reuses_the_official_upstream_command(self):
        """Fails if an outdated managed Superpowers install is marked UPDATE but loses its executable update operation."""
        catalog = load_catalog()
        adapter = StaticCapabilityAdapter(
            state={
                ("superpowers", "antigravity-cli", "global"): managed_state("marketplace:old"),
            }
        )
        plan = build_resolver(catalog, load_profiles(catalog), adapter).resolve(
            ResolveRequest(hosts=("antigravity-cli",), capabilities=("superpowers",))
        )

        target = plan.targets[0]
        self.assertEqual(ReconciliationAction.UPDATE, target.action)
        self.assertEqual(
            ("agy", "plugin", "install", "https://github.com/obra/superpowers"),
            target.operations[0].argv,
        )

    def test_applied_external_operation_is_persisted_without_secrets(self):
        """Fails if a successful external install cannot be reconciled later without persisting credentials."""
        catalog = load_catalog()
        plan = build_resolver(catalog, load_profiles(catalog), StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("antigravity-cli",), capabilities=("superpowers",))
        )
        with tempfile.TemporaryDirectory() as temp:
            state_dir = Path(temp) / "state"
            args = Namespace(state_dir=state_dir, project_root=None)
            result = ExecutionResult(
                dry_run=False,
                results=(OperationResult("superpowers", "antigravity-cli", "INSTALL", "APPLIED", "installed"),),
            )

            _record_managed_installations(plan, result, args)

            record = _managed_installation_records(state_dir)["superpowers:antigravity-cli:global"]
            self.assertEqual("marketplace:stable", record["version"])
            self.assertEqual("external-operation", record["kind"])
            self.assertNotIn("secret", str(record).lower())

    def test_managed_external_record_becomes_noop_only_after_host_discovery(self):
        """Fails if a persisted external install is either duplicated or trusted without host discovery."""
        catalog = load_catalog()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = Namespace(state_dir=root / "state", project_root=None, hosts=["antigravity-cli"], scope="global")
            (args.state_dir).mkdir()
            (args.state_dir / "managed-installations.json").write_text(
                '{"schema_version":1,"installations":{"superpowers:antigravity-cli:global":'
                '{"capability":"superpowers","host":"antigravity-cli","scope":"global",'
                '"version":"marketplace:stable","kind":"external-operation"}}}',
                encoding="utf-8",
            )

            state = _actual_state(catalog, args, external_probe=lambda *_: True)

            actual = state[("superpowers", "antigravity-cli", "global")]
            self.assertEqual(InstalledOwnership.MANAGED_BY_AI_RULES, actual.ownership)
            self.assertTrue(actual.healthy)

    def test_context7_registration_without_runtime_health_is_not_healthy(self):
        """Fails if a Context7 mcp-list presence is mistaken for authenticated runtime health."""
        catalog = load_catalog()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = Namespace(state_dir=root / "state", project_root=None, hosts=["codex"], scope="global")
            args.state_dir.mkdir()
            (args.state_dir / "managed-installations.json").write_text(
                '{"schema_version":1,"installations":{"context7:codex:global":'
                '{"capability":"context7","host":"codex","scope":"global",'
                '"version":"upstream-managed:remote-service","kind":"external-operation"}}}',
                encoding="utf-8",
            )

            actual = _actual_state(catalog, args, external_probe=lambda *_: True)[("context7", "codex", "global")]

            self.assertFalse(actual.healthy)


if __name__ == "__main__":
    unittest.main()
