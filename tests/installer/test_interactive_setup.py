import unittest

from ai_rules.interactive import InteractiveSelection, collect_selection, confirm_execution


class InteractiveSetupTests(unittest.TestCase):
    def test_custom_selection_collects_multiple_hosts_and_capabilities(self):
        """Fails if custom interactive setup cannot carry multi-host and multi-capability intent to the resolver."""
        selection = collect_selection(
            choose=lambda _message, _choices: "custom",
            checkbox=lambda _message, _choices: ["codex", "opencode"] if "host" in _message.lower() else ["andino-workflow", "context7"],
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
        )
        self.assertIsNone(selection)

    def test_declined_confirmation_returns_false(self):
        """Fails if declining the displayed plan is treated as permission to mutate."""
        self.assertFalse(confirm_execution(lambda _message: False))


if __name__ == "__main__":
    unittest.main()
