import sys
import subprocess
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_skills import package_files, eval_cases, focus_reference_drift, directory_files


class FocusReferenceTest(unittest.TestCase):
    def setUp(self):
        self.source = {
            'put-in-your-projects/chat-rules.md': '# Chat Rules\n\nA. PRIORITAS\n\nComplete rules.\n',
            'README.md': '# Template\n\n## A. PRIORITAS\n\n````text\nA. PRIORITAS\n\nComplete rules.\n````\n\n## B. Other\nOther rules.\n',
            'put-in-your-projects/human-language-indonesia.md': '# Indonesia\nAll examples.\n',
            'put-in-your-projects/human-language-english.md': '# English\nAll examples.\n',
        }
        self.files = {
            'references/priority-a.md': 'A. PRIORITAS\n\nComplete rules.\n',
            'references/human-language-indonesia.md': '# Indonesia\nAll examples.\n',
            'references/human-language-english.md': '# English\nAll examples.\n',
        }

    def test_complete_copies_match_without_other_readme_sections(self):
        self.assertEqual([], focus_reference_drift(self.files, self.source))

    def test_missing_copy_is_rejected(self):
        del self.files['references/human-language-english.md']
        self.assertTrue(focus_reference_drift(self.files, self.source))

    def test_changed_example_is_rejected(self):
        self.files['references/human-language-indonesia.md'] += 'Invented example.\n'
        self.assertTrue(focus_reference_drift(self.files, self.source))

    def test_truncated_priority_is_rejected(self):
        self.files['references/priority-a.md'] = 'A. PRIORITAS\n'
        self.assertTrue(focus_reference_drift(self.files, self.source))

    def test_conflicting_readme_priority_is_rejected(self):
        self.source['README.md'] = self.source['README.md'].replace('Complete rules.', 'Different rules.')
        self.assertTrue(focus_reference_drift(self.files, self.source))

    def test_missing_source_section_is_rejected(self):
        self.source['README.md'] = '# No A section\n'
        self.assertTrue(focus_reference_drift(self.files, self.source))

    def test_unterminated_source_fence_is_rejected(self):
        self.source['README.md'] = '## A. PRIORITAS\n\n````text\nA. PRIORITAS\n\nComplete rules.\n'
        self.assertTrue(focus_reference_drift(self.files, self.source))

    def test_line_endings_are_portable_but_wording_is_not_normalized(self):
        self.files = {name: body.replace('\n', '\r\n') for name, body in self.files.items()}
        self.assertEqual([], focus_reference_drift(self.files, self.source))
        self.files['references/priority-a.md'] = self.files['references/priority-a.md'].replace('Complete', 'Partial')
        self.assertTrue(focus_reference_drift(self.files, self.source))

    def test_local_package_includes_untracked_references(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / '.git').mkdir()
            (root / '.git/private').write_text('ignored')
            for name, body in self.files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body, encoding='utf-8')
            files, modes = directory_files(root)
            self.assertEqual(self.files, files)
            self.assertEqual({'100644'}, set(modes.values()))


class PackageValidationTest(unittest.TestCase):
    def test_cli_validates_uncommitted_search_and_workflow_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arguments = []
            for name in ('search-first', 'andino-workflow'):
                package = root / name
                package.mkdir()
                (package / 'SKILL.md').write_text(
                    f'---\nname: {name}\ndescription: Useful research method\n---\n', encoding='utf-8')
                (package / 'README.md').write_text('# Package\n', encoding='utf-8')
                arguments += [f'--{name.replace("-workflow", "")}-dir', str(package)]
            result = subprocess.run([sys.executable, 'scripts/validate_skills.py', *arguments],
                                    cwd=Path(__file__).resolve().parents[1],
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(0, result.returncode, result.stderr)

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
