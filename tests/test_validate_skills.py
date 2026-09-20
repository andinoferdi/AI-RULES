import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_skills import package_files


class PackageValidationTest(unittest.TestCase):
    SKRIPSI_SKILL = "---\nname: skripsi-skill\ndescription: Research workflow guidance\n---\n"

    def test_valid_package(self):
        files = {
            "SKILL.md": "---\nname: example\ndescription: Useful example\n---\n[ref](references/a.md)\n",
            "references/a.md": "# Reference\n",
        }
        self.assertEqual(package_files(files, "example"), [])

    def test_broken_link_fails(self):
        files = {"SKILL.md": "---\nname: example\ndescription: Useful example\n---\n[ref](references/missing.md)\n"}
        self.assertTrue(any("broken link" in error for error in package_files(files, "example")))

    def test_invalid_frontmatter_fails(self):
        files = {"SKILL.md": "---\nname example\ndescription: Useful example\n---\n"}
        self.assertTrue(any("frontmatter" in error for error in package_files(files, "example")))

    def test_wrong_identity_fails(self):
        files = {"SKILL.md": "---\nname: another\ndescription: Useful example\n---\n"}
        self.assertTrue(any("wrong or missing name" in error for error in package_files(files, "example")))

    def test_unsupported_yaml_fails(self):
        files = {"SKILL.md": "---\nname: example\ndescription: [unclosed\n---\n"}
        self.assertTrue(any("unsupported frontmatter" in error for error in package_files(files, "example")))

    def test_development_file_in_runtime_fails(self):
        files = {
            "SKILL.md": "---\nname: example\ndescription: Useful example\n---\n",
            "evals/cases.json": "[]",
        }
        self.assertTrue(any("unexpected runtime file" in error for error in package_files(files, "example")))

    def test_skripsi_identity_valid(self):
        self.assertEqual(package_files({"SKILL.md": self.SKRIPSI_SKILL}, "skripsi-skill"), [])

    def test_skripsi_markdown_asset_allowed(self):
        files = {
            "SKILL.md": self.SKRIPSI_SKILL,
            "assets/research-state-template.md": "# Research state\n",
        }
        self.assertEqual(package_files(files, "skripsi-skill"), [])

    def test_andino_markdown_asset_rejected(self):
        files = {
            "SKILL.md": "---\nname: andino-workflow\ndescription: Task workflow\n---\n",
            "assets/template.md": "# Template\n",
        }
        self.assertTrue(any("unexpected runtime file" in error for error in package_files(files, "andino-workflow")))

    def test_rescue_markdown_asset_rejected(self):
        files = {
            "SKILL.md": "---\nname: ai-codebase-rescue\ndescription: Codebase rescue\n---\n",
            "assets/template.md": "# Template\n",
        }
        self.assertTrue(any("unexpected runtime file" in error for error in package_files(files, "ai-codebase-rescue")))

    def test_skripsi_script_rejected(self):
        files = {"SKILL.md": self.SKRIPSI_SKILL, "scripts/tool.py": "print('hello')\n"}
        self.assertTrue(any("unexpected runtime file" in error for error in package_files(files, "skripsi-skill")))

    def test_wrong_skripsi_identity_rejected(self):
        files = {"SKILL.md": "---\nname: another-skill\ndescription: Research workflow\n---\n"}
        self.assertTrue(any("wrong or missing name" in error for error in package_files(files, "skripsi-skill")))

    def test_broken_link_to_skripsi_asset_rejected(self):
        files = {"SKILL.md": self.SKRIPSI_SKILL + "[template](assets/missing.md)\n"}
        self.assertTrue(any("broken link" in error for error in package_files(files, "skripsi-skill")))

    def test_broken_link_from_skripsi_asset_rejected(self):
        files = {
            "SKILL.md": self.SKRIPSI_SKILL,
            "assets/template.md": "[core](../references/missing.md)\n",
        }
        self.assertTrue(any("broken link" in error for error in package_files(files, "skripsi-skill")))

    def test_skripsi_reference_and_asset_links_valid(self):
        files = {
            "SKILL.md": self.SKRIPSI_SKILL + "[core](references/core.md)\n[template](assets/template.md)\n",
            "references/core.md": "[template](../assets/template.md)\n",
            "assets/template.md": "[core](../references/core.md)\n",
        }
        self.assertEqual(package_files(files, "skripsi-skill"), [])


if __name__ == "__main__":
    unittest.main()
