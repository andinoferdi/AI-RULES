import sys
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_skills import package_files, eval_cases


class PackageValidationTest(unittest.TestCase):
    SKRIPSI_SKILL = "---\nname: skripsi-skill\ndescription: Research workflow guidance\n---\n"

    def test_valid_package(self):
        files = {
            "README.md": "# Example\n",
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
        self.assertEqual(package_files({"README.md": "# Research\n", "SKILL.md": self.SKRIPSI_SKILL}, "skripsi-skill"), [])

    def test_skripsi_markdown_asset_allowed(self):
        files = {
            "README.md": "# Research\n",
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
            "README.md": "# Research\n",
            "SKILL.md": self.SKRIPSI_SKILL + "[core](references/core.md)\n[template](assets/template.md)\n",
            "references/core.md": "[template](../assets/template.md)\n",
            "assets/template.md": "[core](../references/core.md)\n",
        }
        self.assertEqual(package_files(files, "skripsi-skill"), [])

    def test_distribution_readme_required(self):
        errors = package_files({"SKILL.md": self.SKRIPSI_SKILL}, "skripsi-skill")
        self.assertTrue(any("missing README.md" in error for error in errors))

    def test_portable_name_constraints(self):
        for name in ("Upper", "two--hyphens", "-leading", "trailing-", "has_space", "a" * 65):
            with self.subTest(name=name):
                files = {"README.md": "# Example", "SKILL.md": f"---\nname: {name}\ndescription: Useful workflow\n---\n"}
                self.assertTrue(any("invalid portable name" in error for error in package_files(files, name)))

    def test_description_length_boundary(self):
        for length, valid in ((1, True), (1024, True), (1025, False)):
            files = {"README.md": "# Example", "SKILL.md": f"---\nname: example\ndescription: {'x' * length}\n---\n"}
            self.assertEqual(not package_files(files, "example"), valid)

    def test_yaml_non_string_metadata_rejected(self):
        for value in ("null", "~", "true", "false", "123", "# comment only"):
            files = {"README.md": "# Example", "SKILL.md": f"---\nname: example\ndescription: {value}\n---\n"}
            with self.subTest(value=value):
                self.assertTrue(package_files(files, "example"))

    def test_link_cannot_escape_package(self):
        files = {"README.md": "[outside](../private.md)", "SKILL.md": self.SKRIPSI_SKILL}
        self.assertTrue(any("escapes package" in error for error in package_files(files, "skripsi-skill")))

    def test_nonportable_runtime_paths_rejected(self):
        for path in ("references/../private.md", "references/.cache/private.md", "references\\a.md"):
            files = {"README.md": "# Research", "SKILL.md": self.SKRIPSI_SKILL, path: "# Bad path"}
            self.assertTrue(any("unexpected runtime file" in error for error in package_files(files, "skripsi-skill")))

    def test_runtime_symlink_and_gitlink_rejected(self):
        files = {"README.md": "# Research", "SKILL.md": self.SKRIPSI_SKILL}
        for mode in ("120000", "160000"):
            self.assertTrue(any("non-regular runtime file" in error for error in package_files(files, "skripsi-skill", {"SKILL.md": mode})))


class EvalSchemaTest(unittest.TestCase):
    def test_malformed_id_and_kind_report_errors_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evals").mkdir()
            (root / "evals/example.json").write_text('[{"id": [], "kind": {}, "prompt": "p", "expected": "e", "forbidden": "f"}]', encoding="utf-8")
            with patch("validate_skills.ROOT", root):
                errors = eval_cases("example")
            self.assertTrue(any("missing id" in error for error in errors))
            self.assertTrue(any("missing kind" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
