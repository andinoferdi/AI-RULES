import unittest

from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver

HOSTS = ("codex", "claude-code", "opencode", "antigravity-cli", "antigravity-ide")


class NaturalWritingIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.profiles = load_profiles(self.catalog)
        self.resolver = build_resolver(self.catalog, self.profiles, StaticCapabilityAdapter())

    def ids(self, **kwargs):
        plan = self.resolver.resolve(ResolveRequest(hosts=("codex",), **kwargs))
        return {target.capability_id for target in plan.targets}

    def test_standalone_without_dependencies(self):
        entry = self.catalog.require_capability("natural-writing")
        self.assertEqual("natural-writing", entry.source["branch"])
        self.assertEqual((), tuple(entry.requires))
        self.assertEqual({"natural-writing"}, self.ids(capabilities=("natural-writing",)))

    def test_profile_membership(self):
        self.assertIn("natural-writing", self.ids(profile_id="everything"))
        self.assertIn("natural-writing", self.ids(profile_id="research-skripsi"))
        for profile in ("minimal", "engineering"):
            self.assertNotIn("natural-writing", self.ids(profile_id=profile))

    def test_selectable_in_custom_setup(self):
        from ai_rules.interactive import build_capability_choices
        choices = build_capability_choices(self.catalog.capabilities)
        self.assertTrue(any(c.value == "natural-writing" and c.title == "Natural Writing" for c in choices))

    def test_delivered_for_all_hosts(self):
        entry = self.catalog.require_capability("natural-writing")
        hosts = {host for delivery in entry.delivery for host in delivery.hosts}
        self.assertEqual(set(HOSTS), hosts)
        for host in HOSTS:
            plan = self.resolver.resolve(ResolveRequest(hosts=(host,), capabilities=("natural-writing",)))
            self.assertEqual({"natural-writing"}, {t.capability_id for t in plan.targets})


if __name__ == "__main__":
    unittest.main()
