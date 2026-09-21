import unittest
from pathlib import Path
from unittest.mock import patch

from ai_rules.catalog import load_catalog
from ai_rules.domain.errors import ValidationError
from ai_rules.domain.statuses import DetectionStatus, Scope
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.profiles import load_profiles


class CatalogProfileTests(unittest.TestCase):
    def test_catalog_loads_mvp_capabilities_and_hosts(self):
        catalog = load_catalog()
        self.assertEqual(
            {"codex", "claude-code", "opencode", "antigravity-cli", "antigravity-ide"},
            set(catalog.hosts),
        )
        for capability_id in ["andino-workflow", "ai-codebase-rescue", "skripsi-skill", "superpowers", "context7"]:
            self.assertIn(capability_id, catalog.capabilities)

    def test_skill_roots_distinguish_codex_and_antigravity_surfaces(self):
        """Fails if global installation selects a stale Codex root or an ambiguous Antigravity surface."""
        catalog = load_catalog()
        adapters = build_host_adapters(catalog.hosts, home=Path("/home/andino"))

        self.assertEqual(Path("/home/andino/.agents/skills"), adapters["codex"].skill_target(Scope.GLOBAL))
        self.assertEqual(Path("/workspace/.agents/skills"), adapters["codex"].skill_target(Scope.PROJECT, Path("/workspace")))
        self.assertEqual(
            Path("/home/andino/.gemini/antigravity-cli/skills"),
            adapters["antigravity-cli"].skill_target(Scope.GLOBAL),
        )
        self.assertEqual(
            Path("/home/andino/.gemini/config/skills"),
            adapters["antigravity-ide"].skill_target(Scope.GLOBAL),
        )
        self.assertEqual(
            Path("/workspace/.agents/skills"),
            adapters["antigravity-cli"].skill_target(Scope.PROJECT, Path("/workspace")),
        )
        self.assertEqual(Path("/home/andino/.claude/skills"), adapters["claude-code"].skill_target(Scope.GLOBAL))
        self.assertEqual(Path("/workspace/.claude/skills"), adapters["claude-code"].skill_target(Scope.PROJECT, Path("/workspace")))
        self.assertEqual(Path("/home/andino/.config/opencode/skills"), adapters["opencode"].skill_target(Scope.GLOBAL))
        self.assertEqual(Path("/workspace/.agents/skills"), adapters["opencode"].skill_target(Scope.PROJECT, Path("/workspace")))
        self.assertEqual(
            (Path("/workspace/.agents/skills"), Path("/workspace/.claude/skills")),
            adapters["opencode"].skill_discovery_roots(Scope.PROJECT, Path("/workspace")),
        )

    def test_antigravity_cli_detection_uses_agy_binary(self):
        """Fails if a present official Antigravity CLI is checked under its obsolete executable name."""
        catalog = load_catalog()
        adapter = build_host_adapters(catalog.hosts)["antigravity-cli"]
        with patch("ai_rules.hosts.adapters.shutil.which", return_value="/bin/agy") as which:
            detection = adapter.detect()
        which.assert_called_once_with("agy")
        self.assertEqual(DetectionStatus.PRESENT, detection.status)

    def test_claude_and_opencode_detection_use_their_cli_binaries(self):
        """Fails if a detected host is checked under a different executable than its adapter contract."""
        catalog = load_catalog()
        adapters = build_host_adapters(catalog.hosts)
        with patch("ai_rules.hosts.adapters.shutil.which", side_effect=["/bin/claude", "/bin/opencode"]) as which:
            claude = adapters["claude-code"].detect()
            opencode = adapters["opencode"].detect()
        self.assertEqual(DetectionStatus.PRESENT, claude.status)
        self.assertEqual(DetectionStatus.PRESENT, opencode.status)
        self.assertEqual(["claude", "opencode"], [call.args[0] for call in which.call_args_list])

    def test_profiles_validate_and_everything_is_not_default(self):
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        self.assertEqual("minimal", profiles.default.id)
        self.assertFalse(profiles.require("everything").default)

    def test_invalid_capability_id_fails(self):
        data = {
            "schema_version": 1,
            "id": "bad id with spaces",
            "display_name": "Bad",
            "ownership": "FIRST_PARTY",
            "kind": "skill",
            "importance": "REQUIRED",
            "source": {},
            "delivery": [],
            "verification": [],
            "update_policy": {"model": "release_manifest"},
        }
        from ai_rules.domain.models import Capability

        with self.assertRaises(ValidationError):
            Capability.from_dict(data)

    def test_secret_value_is_rejected_in_profile_like_data(self):
        from ai_rules.domain.models import reject_secret_keys

        with self.assertRaises(ValidationError):
            reject_secret_keys({"api_key": "plain-secret"}, "fixture")


if __name__ == "__main__":
    unittest.main()
