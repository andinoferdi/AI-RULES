"""Every first-party skill is registered in the same places, or CI names the gap.

A skill is a folder in skills/<id>/. Adding or removing one also touches the
catalog, the profiles, the package validator and evals. This test turns a
half-finished change into one clear failure instead of scattered red checks.
See AGENTS.md, "Adding or removing a skill".
"""

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CATALOG = ROOT / "src/ai_rules/catalog/data/capabilities.json"
PROFILES = ROOT / "src/ai_rules/profiles/data/profiles.json"
MANIFEST = ROOT / "src/ai_rules/release/data/release_manifest.json"
FAMILIES = {"threejs-skills"}  # validated by scripts/validate_threejs_family.py, not RUNTIME_SKILLS


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_skills():
    spec = importlib.util.spec_from_file_location("validate_skills", ROOT / "scripts/validate_skills.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(module.RUNTIME_SKILLS)


class SkillRegistryConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.catalog = {item["id"]: item for item in load(CATALOG)["capabilities"]
                        if item["ownership"] == "FIRST_PARTY"}
        self.folders = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}

    def test_catalog_and_skills_folder_list_the_same_skills(self):
        self.assertEqual(set(self.catalog) - self.folders, set(), "add skills/<id>/SKILL.md")
        self.assertEqual(self.folders - set(self.catalog), set(),
                         "register these skills/ folders in capabilities.json")

    def test_catalog_sources_read_main_subpaths(self):
        for skill, item in self.catalog.items():
            self.assertEqual("main", item["source"]["branch"], skill)
            self.assertEqual(f"skills/{skill}", item["source"]["subpath"], skill)

    def test_release_manifest_has_no_skill_pins(self):
        self.assertNotIn("first_party", load(MANIFEST),
                         "skills are read from skills/ on main; remove first_party pins")

    def test_package_validator_covers_every_skill_folder(self):
        self.assertEqual(runtime_skills() | FAMILIES, self.folders,
                         "update RUNTIME_SKILLS in scripts/validate_skills.py")

    def test_every_skill_has_eval_cases(self):
        for skill in runtime_skills():
            self.assertTrue((ROOT / "evals" / f"{skill}.json").is_file(), f"add evals/{skill}.json")

    def test_profiles_use_known_skills_and_everything_lists_all(self):
        known = {item["id"] for item in load(CATALOG)["capabilities"]}
        profiles = {item["id"]: item["capabilities"] for item in load(PROFILES)["profiles"]}
        for profile, skills in profiles.items():
            self.assertEqual(set(skills) - known, set(), f"profiles.json {profile}")
        self.assertEqual(set(self.catalog) - set(profiles["everything"]), set(),
                         "add these skills to the everything profile in profiles.json")


if __name__ == "__main__":
    unittest.main()
