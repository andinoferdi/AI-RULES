import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_skills import package_files


class PackageValidationTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
