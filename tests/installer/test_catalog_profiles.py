import unittest

from ai_rules.catalog import load_catalog
from ai_rules.domain.errors import ValidationError
from ai_rules.profiles import load_profiles


class CatalogProfileTests(unittest.TestCase):
    def test_catalog_loads_mvp_capabilities_and_hosts(self):
        catalog = load_catalog()
        self.assertEqual({"codex", "claude-code", "opencode", "antigravity"}, set(catalog.hosts))
        for capability_id in ["andino-workflow", "ai-codebase-rescue", "skripsi-skill", "superpowers", "context7"]:
            self.assertIn(capability_id, catalog.capabilities)

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
