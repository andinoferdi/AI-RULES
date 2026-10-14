import unittest

from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver


class CouncilIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.profiles = load_profiles(self.catalog)
        self.resolver = build_resolver(self.catalog, self.profiles, StaticCapabilityAdapter())

    def test_council_is_standalone_with_focus_dependency(self):
        entry = self.catalog.require_capability("council")
        self.assertEqual("council", entry.source["branch"])
        self.assertEqual(("focus",), tuple(entry.requires))
        plan = self.resolver.resolve(ResolveRequest(hosts=("codex",), capabilities=("council",)))
        self.assertEqual({"council", "focus"}, {target.capability_id for target in plan.targets})
        self.assertNotIn("andino-workflow", {target.capability_id for target in plan.targets})

    def test_everything_installs_council_and_minimal_does_not(self):
        everything = self.resolver.resolve(ResolveRequest(hosts=("codex",), profile_id="everything"))
        minimal = self.resolver.resolve(ResolveRequest(hosts=("codex",), profile_id="minimal"))
        self.assertIn("council", {target.capability_id for target in everything.targets})
        self.assertNotIn("council", {target.capability_id for target in minimal.targets})

    def test_council_is_selectable_in_custom_setup(self):
        from ai_rules.interactive import build_capability_choices
        choices = build_capability_choices(self.catalog.capabilities)
        self.assertTrue(any(choice.value == "council" and choice.title == "Council" for choice in choices))


if __name__ == "__main__":
    unittest.main()
