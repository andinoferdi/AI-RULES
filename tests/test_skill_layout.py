"""Every first-party skill uses the same shell, described in docs/specs/changing-skills.md.

The test reads the real skills/ folder: the top-level entries, where license and
provenance files live, and the README heading order. Method content inside
SKILL.md and the internal skills/<method>/ folders is out of scope here.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

ALLOWED_TOP_LEVEL = {"SKILL.md", "README.md", "references", "scripts", "assets", "skills"}
README_SECTIONS = ["What It Does", "When to Use", "Quick Start", "How It Works",
                   "Works With Other Skills", "Files", "License"]
OPTIONAL_SECTIONS = {"How It Works"}
LEGAL_NAME = re.compile(r"(license|provenance)", re.I)


def skill_dirs():
    return sorted(path.parent for path in SKILLS.glob("*/SKILL.md"))


def without_code(text):
    """Drop fenced code so headings and rules inside examples are ignored."""
    return re.sub(r"^```.*?^```[^\n]*$", "", text, flags=re.M | re.S)


def headings(text, level):
    marks = "#" * level
    return re.findall(rf"^{marks} (.+?)\s*$", without_code(text), re.M)


def section(text, name):
    body = without_code(text)
    match = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return match.group(1) if match else ""


class SkillLayoutTests(unittest.TestCase):
    def test_every_skill_found(self):
        self.assertGreaterEqual(len(skill_dirs()), 1)

    def test_top_level_entries_are_from_the_shared_vocabulary(self):
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                extra = {entry.name for entry in skill.iterdir()} - ALLOWED_TOP_LEVEL
                self.assertEqual(set(), extra, "see docs/specs/changing-skills.md, Skill layout")
                for folder in ("scripts", "assets", "skills"):
                    path = skill / folder
                    if path.exists():
                        self.assertTrue(any(path.iterdir()), f"empty {folder}/")

    def test_legal_files_live_in_references_legal(self):
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                self.assertTrue((skill / "references/legal/license.md").is_file())
                stray = [str(path.relative_to(skill)) for path in skill.rglob("*")
                         if path.is_file() and LEGAL_NAME.search(path.name)
                         and path.relative_to(skill).parts[0] != "skills"
                         and path.parent != skill / "references/legal"]
                self.assertEqual([], stray)

    def test_readme_sections_follow_the_template(self):
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                text = (skill / "README.md").read_text(encoding="utf-8")
                self.assertEqual(1, len(headings(text, 1)), "exactly one level-1 title")
                self.assertTrue(text.startswith("# "), "README starts with its title")
                found = headings(text, 2)
                expected = [name for name in README_SECTIONS
                            if name not in OPTIONAL_SECTIONS or name in found]
                self.assertEqual(expected, found)
                self.assertEqual(["Installation", "Usage"], headings(section(text, "Quick Start"), 3))
                self.assertIn("| Use for | Do not use for |", section(text, "When to Use"))
                self.assertIn("references/legal/license.md", section(text, "License"))
                self.assertIn("references/legal/license.md", section(text, "Files"))
                self.assertNotRegex(without_code(text), r"(?m)^---\s*$")

    def test_readme_install_commands_use_main(self):
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                text = (skill / "README.md").read_text(encoding="utf-8")
                self.assertIn(f"ai-rules setup --", text)
                self.assertIn(f"sparse-checkout set skills/{skill.name}", text)
                branches = set(re.findall(r"--branch (\S+)", text))
                self.assertLessEqual(branches, {"main"}, "skills live on main (ADR 0002)")


if __name__ == "__main__":
    unittest.main()
