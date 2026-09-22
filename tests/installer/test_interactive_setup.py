import unittest

from ai_rules.catalog import load_catalog
from ai_rules.interactive import (
    InteractiveSelection,
    build_capability_choices,
    build_host_choices,
    build_profile_choices,
    collect_selection,
    confirm_execution,
    render_setup_summary,
)
from ai_rules.profiles import load_profiles


class InteractiveSetupTests(unittest.TestCase):
    def test_display_choices_keep_stable_ids_and_explain_selection(self):
        """Fails if a presentation change makes Questionary return labels instead of IDs."""
        catalog = load_catalog()
        profiles = load_profiles(catalog)

        host = build_host_choices(catalog.hosts)[0]
        engineering = next(choice for choice in build_profile_choices(profiles.profiles, catalog.capabilities) if choice.value == "engineering")
        rescue = next(choice for choice in build_capability_choices(catalog.capabilities) if choice.value == "ai-codebase-rescue")

        self.assertEqual("codex", host.value)
        self.assertEqual("Codex", host.title)
        self.assertIn("Skills: ~/.agents/skills", host.description)
        self.assertEqual("engineering", engineering.value)
        self.assertEqual("Engineering", engineering.title)
        self.assertIn("Includes: Andino Workflow, AI Codebase Rescue", engineering.description)
        self.assertEqual("ai-codebase-rescue", rescue.value)

    def test_setup_summary_uses_human_names_and_types(self):
        """Fails if the pre-confirmation summary exposes internal IDs instead of readable setup details."""
        catalog = load_catalog()
        profiles = load_profiles(catalog)

        summary = render_setup_summary(
            host_ids=("codex",),
            profile_id="engineering",
            capabilities=profiles.require("engineering").capabilities,
            scope="global",
            catalog=catalog,
        )

        self.assertIn("AI-RULES Setup", summary)
        self.assertIn("Codex", summary)
        self.assertIn("Engineering", summary)
        self.assertIn("Andino Workflow - first-party skill", summary)
        self.assertIn("AI Codebase Rescue - first-party skill", summary)
        self.assertNotIn("andino-workflow", summary)

    def test_custom_selection_collects_multiple_hosts_and_capabilities(self):
        """Fails if custom interactive setup cannot carry multi-host and multi-capability intent to the resolver."""
        selection = collect_selection(
            choose=lambda _message, _choices: "custom",
            checkbox=lambda message, _choices: ["codex", "opencode"] if "agent" in message.lower() else ["andino-workflow", "context7"],
            host_choices=("codex", "opencode"),
            profile_choices=("minimal", "custom"),
            capability_choices=("andino-workflow", "context7"),
        )
        self.assertEqual(
            InteractiveSelection(hosts=("codex", "opencode"), profile_id=None, capabilities=("andino-workflow", "context7")),
            selection,
        )

    def test_cancelled_selection_returns_none(self):
        """Fails if cancelling interactive setup creates a partial selection that could later mutate state."""
        selection = collect_selection(
            choose=lambda _message, _choices: None,
            checkbox=lambda _message, _choices: [],
            host_choices=("codex",),
            profile_choices=("minimal", "custom"),
            capability_choices=("andino-workflow",),
        )
        self.assertIsNone(selection)

    def test_declined_confirmation_returns_false(self):
        """Fails if declining the displayed plan is treated as permission to mutate."""
        self.assertFalse(confirm_execution(lambda _message: False))


if __name__ == "__main__":
    unittest.main()
