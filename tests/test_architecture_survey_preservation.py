"""Guard the andino-architecture-survey rewrite against silent loss and old defects.

The ledger rows (P1-P27), the reference additions (A1-A7) and the defect fixes (X1-X10) come from
the 2026-11-26 upgrade plan. Each literal below is an anchor for one kept asset; a failing anchor
means a rule or resource was dropped. The test reads the real skill folder.
"""

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/andino-workflow/skills/architecture-survey"

SECTIONS = ["Purpose", "Trigger and non-trigger", "Select a resource, not a second lifecycle",
            "Prerequisites", "Procedure", "Rules", "Shortcuts", "Red flags",
            "Ownership and permission boundary", "Output", "Verification",
            "Worked example and anti-pattern", "Fallback", "Local resources",
            "Operational example", "Provenance"]

ANCHORS = {
    "SKILL.md": [
        "rename", "product code", "hot spot", "deletion test", "one adapter", "two adapters",
        "how they are called", "test surface", "replace, don't layer", "temp", "summary card",
        "one sentence", "6 words", "Strong", "Worth exploring", "Speculative",
        "local-substitutable", "reopen", "GLOSSARY.md", "lazily", "api-and-interface-design",
        "module-depth", "execution plan", "Which of these would you like to explore?",
        "docs/adr", "untested", "hard to test", "widen", "do not propose interfaces yet",
        "redraw", "only when the user approves",
    ],
    "resources/architectural-vocabulary.md": [
        "module", "interface", "implementation", "depth", "deep", "shallow", "seam", "adapter",
        "leverage", "locality", "component", "service", "boundary", "cleaner code", "invariants",
        "error modes", "internal seam", "in-process", "true external",
    ],
    "resources/diagram-patterns.md": ["320"],
    "resources/html-report-scaffold.md": ["offline", "legend", "Top recommendation", "xdg-open",
                                          "headless"],
    "resources/subagent-exploration-brief.md": ['"dependency_category"', "exists",
                                                "deletion test", "only when the user approves"],
    "resources/grilling-and-adr-protocols.md": ["adapters", "tests survive", "callers",
                                                "GLOSSARY.md", "lazily", "ephemeral", "enduring",
                                                "## Consequences"],
    "resources/worked-example.md": ["OrderIntake"],
}

FENCE = re.compile(r"^```.*?^```[^\n]*$", re.M | re.S)


def read(rel):
    return (SKILL / rel).read_text(encoding="utf-8")


def prose(text):
    return FENCE.sub("", text)


def body(text):
    """SKILL.md text after the closing frontmatter line."""
    parts = text.split("\n---\n", 1)
    return parts[1].lstrip("\n") if text.startswith("---\n") and len(parts) == 2 else text


def section(text, name):
    match = re.search(rf"^## {re.escape(name)}[^\n]*$(.*?)(?=^## |\Z)", prose(text), re.M | re.S)
    return match.group(1) if match else ""


class ArchitectureSurveyPreservationTests(unittest.TestCase):
    def test_sections_in_sibling_order(self):
        found = re.findall(r"^## (.+?)\s*$", prose(body(read("SKILL.md"))), re.M)
        position = 0
        for name in SECTIONS:
            matches = [i for i, heading in enumerate(found) if heading.startswith(name)]
            self.assertTrue(matches, f"missing section: {name}")
            self.assertGreaterEqual(matches[0], position, f"out of order: {name}")
            position = matches[0]

    def test_procedure_steps_have_done_when(self):
        procedure = section(read("SKILL.md"), "Procedure")
        steps = re.split(r"^\d+\. ", procedure, flags=re.M)[1:]
        self.assertGreaterEqual(len(steps), 5)
        for number, step in enumerate(steps, 1):
            self.assertIn("Done when", step, f"step {number} has no completion check")

    def test_guide_mirrors_skill(self):
        self.assertTrue(body(read("SKILL.md")) == read("GUIDE.md").lstrip("\n"),
                        "GUIDE.md must equal the SKILL.md body")

    def test_skill_length_budget(self):
        self.assertLessEqual(len(read("SKILL.md").splitlines()), 424)

    def test_ledger_anchors(self):
        for rel, literals in ANCHORS.items():
            text = " ".join(read(rel).split()).lower()  # line wrapping is not content
            for literal in literals:
                with self.subTest(file=rel, anchor=literal):
                    self.assertTrue(literal.lower() in text, f"{rel}: missing anchor {literal!r}")

    def test_five_diagram_patterns(self):
        patterns = re.findall(r"^## Pattern \d", read("resources/diagram-patterns.md"), re.M)
        self.assertGreaterEqual(len(patterns), 5)

    def test_defects_stay_fixed(self):
        files = sorted(p for p in SKILL.rglob("*.md"))
        for path in files:
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(SKILL).as_posix()
            with self.subTest(file=rel):
                self.assertFalse("rtk " in text, f"{rel}: host-specific 'rtk' command")
                self.assertFalse("deep-module-design" in text, f"{rel}: retired method ID")
                for line in prose(text).splitlines():
                    # Identifiers quoted in backticks keep their names; only prose counts.
                    if "wrapper" not in re.sub(r"`[^`]*`", "", line).lower():
                        continue
                    table_rule = line.lstrip().startswith("|") and re.search(
                        r"substitut|never use", line, re.I)
                    self.assertTrue(table_rule, f"'wrapper' in prose: {line.strip()}")
        depth_rows = [line for line in read("resources/architectural-vocabulary.md").splitlines()
                      if re.match(r"\s*(\||\*\*|- \*\*)\s*`?\*?\*?depth", line, re.I)]
        self.assertTrue(depth_rows, "vocabulary has no depth definition")
        for row in depth_rows:
            self.assertFalse("ratio" in row.lower(), f"depth defined as a ratio: {row.strip()}")
        self.assertFalse("Lines" in read("resources/diagram-patterns.md"),
                         "mass diagram labels depth in lines of code")
        example = read("resources/worked-example.md")
        self.assertFalse("Dependency: in-process" in example,
                         "worked example classifies a database and email cluster as in-process")
        after = example.split("### The design after grilling", 1)
        self.assertEqual(2, len(after), "worked example lacks the after-grilling section")
        self.assertNotRegex(after[1], r"\b\w*Service\b")

    def test_operational_example_runs(self):
        match = re.search(r"^```python andino-operational-example\n(.*?)^```", read("SKILL.md"),
                          re.M | re.S)
        self.assertIsNotNone(match, "no operational example")
        code = match.group(1)
        self.assertNotIn("contract_lines", code)
        env = dict(os.environ)
        env.pop("ANDINO_NEGATIVE", None)
        ok = subprocess.run([sys.executable, "-I", "-c", code], env=env, capture_output=True)
        self.assertEqual(0, ok.returncode, ok.stderr.decode())
        env["ANDINO_NEGATIVE"] = "1"
        bad = subprocess.run([sys.executable, "-I", "-c", code], env=env, capture_output=True)
        self.assertNotEqual(0, bad.returncode)


if __name__ == "__main__":
    unittest.main()
