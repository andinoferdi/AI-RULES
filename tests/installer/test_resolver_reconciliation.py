import unittest

from ai_rules.capabilities.adapters import StaticCapabilityAdapter, managed_state
from ai_rules.catalog import load_catalog
from ai_rules.domain.models import ActualState
from ai_rules.domain.statuses import InstalledOwnership, ReconciliationAction, Scope
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver


class ResolverReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.profiles = load_profiles(self.catalog)

    def resolve_one(self, state=None, targets=None, capability="andino-workflow"):
        resolver = build_resolver(self.catalog, self.profiles, StaticCapabilityAdapter(state=state, targets=targets))
        plan = resolver.resolve(
            ResolveRequest(hosts=("codex",), scope=Scope.GLOBAL, capabilities=(capability,))
        )
        self.assertEqual(1, len(plan.targets))
        return plan.targets[0]

    def test_absent_target_installs(self):
        target = self.resolve_one()
        self.assertEqual(ReconciliationAction.INSTALL, target.action)

    def test_identical_managed_healthy_is_noop(self):
        version = "release-manifest:andino-workflow@9172810d1223cf441cf8637d63729aedad1e4ba5#1"
        target = self.resolve_one(
            state={("andino-workflow", "codex", "global"): managed_state(version)},
            targets={"andino-workflow": version},
        )
        self.assertEqual(ReconciliationAction.NO_OP, target.action)

    def test_older_managed_target_updates(self):
        target = self.resolve_one(
            state={("andino-workflow", "codex", "global"): managed_state("release-manifest:andino-workflow@old#0")},
            targets={"andino-workflow": "release-manifest:andino-workflow@new#1"},
        )
        self.assertEqual(ReconciliationAction.UPDATE, target.action)

    def test_managed_drift_repairs_without_update(self):
        version = "release-manifest:andino-workflow@9172810d1223cf441cf8637d63729aedad1e4ba5#1"
        target = self.resolve_one(
            state={("andino-workflow", "codex", "global"): managed_state(version, artifact_drift=True)},
            targets={"andino-workflow": version},
        )
        self.assertEqual(ReconciliationAction.REPAIR, target.action)

    def test_config_drift_reconfigures(self):
        version = "release-manifest:andino-workflow@9172810d1223cf441cf8637d63729aedad1e4ba5"
        target = self.resolve_one(
            state={("andino-workflow", "codex", "global"): managed_state(version, config_drift=True)},
            targets={"andino-workflow": version},
        )
        self.assertEqual(ReconciliationAction.RECONFIGURE, target.action)

    def test_unmanaged_existing_blocks_mutation(self):
        state = ActualState(exists=True, ownership=InstalledOwnership.EXTERNAL_EXISTING, healthy=True)
        target = self.resolve_one(state={("andino-workflow", "codex", "global"): state})
        self.assertEqual(ReconciliationAction.BLOCK, target.action)

    def test_newer_managed_target_is_not_silently_downgraded(self):
        target = self.resolve_one(
            state={("andino-workflow", "codex", "global"): managed_state("future:andino-workflow@edge")},
            targets={"andino-workflow": "release-manifest:andino-workflow@stable"},
        )
        self.assertEqual(ReconciliationAction.BLOCK, target.action)

    def test_opaque_commit_hashes_do_not_determine_update_direction(self):
        """Fails if changing hexadecimal SHA text alone causes an update or downgrade decision."""
        target = self.resolve_one(
            state={("andino-workflow", "codex", "global"): managed_state("release-manifest:andino-workflow@ffff")},
            targets={"andino-workflow": "release-manifest:andino-workflow@0000"},
        )
        self.assertEqual(ReconciliationAction.BLOCK, target.action)

    def test_multi_host_plan_is_supported(self):
        resolver = build_resolver(self.catalog, self.profiles, StaticCapabilityAdapter())
        plan = resolver.resolve(ResolveRequest(hosts=("codex", "opencode"), profile_id="minimal"))
        self.assertEqual(2, len(plan.targets))


if __name__ == "__main__":
    unittest.main()
