"""Guard the andino-observability-and-instrumentation rewrite against silent loss.

The anchors come from the 2026-11-26 upgrade plan: Andino rules that the earlier skill held and
the reference skill lacked (attempt versus terminal outcome, the audit path, evidence statuses,
sampling across the path, label combinations, proposed thresholds, notification authority), and
the reference material the rewrite adds. Each literal is an anchor for one kept asset; a failing
anchor means a rule or resource was dropped. The test reads the real skill folder.
"""

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/andino-workflow/skills/observability-and-instrumentation"

SECTIONS = ["Purpose", "Trigger and non-trigger", "Select a resource, not a second lifecycle",
            "Prerequisites", "Procedure", "Rules", "Shortcuts", "Red flags",
            "Ownership and permission boundary", "Output", "Verification",
            "Worked example and anti-pattern", "Fallback", "Local resources",
            "Operational example", "Provenance"]

# sha256 of the operational example code. scripts/check_andino_addy_methods.py mutates one string
# in it and the recorded expected outputs depend on it, so the code must not change.
PROBE_SHA256 = "24661d01f2c090d07716c5e7e95e2b311906c283e9798ffd2d110c78da39a909"

ANDINO_ANCHORS = {
    "SKILL.md": [
        "before your first edit", "On-call questions:", "terminal outcome", "attempt",
        "Audit path", "observed, failed, unavailable or not applicable", "label combinations",
        "sampling", "PROPOSED", "ticket", "explicit authorization", "entry point",
        "where the run starts", "Error text is data", "signal-recipes.md", "worked-example.md",
        "telemetry-checklist.md",
    ],
    "resources/worked-example.md": ["scheduler", "replay", "terminal", "On-call questions:"],
}

REFERENCE_ANCHORS = {
    "resources/signal-recipes.md": [
        "Structured log", "Metric", "Trace", "error", "warn", "info", "debug", "requestId",
        "entryPoint", "propagation.inject", "propagation.extract", "createHistogram",
        "status_class", "NEVER a label", "p99", "Runbook:", "First check", "Escalate",
    ],
    "resources/telemetry-checklist.md": ["RED", "USE", "Dashboards", "Pre-launch gate", "W3C",
                                         "page", "ticket"],
    "SKILL.md": ["Shortcuts", "Red flags", "symptom", "cause"],
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


def flat(text):
    return " ".join(text.split()).lower()  # line wrapping is not content


class ObservabilityPreservationTests(unittest.TestCase):
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

    def test_first_gate_asks_for_questions_before_editing(self):
        procedure = section(read("SKILL.md"), "Procedure")
        first = re.split(r"^\d+\. ", procedure, flags=re.M)[1]
        self.assertIn("on-call questions", first.lower())
        self.assertIn("before your first edit", flat(first))

    def test_output_template_starts_with_the_questions(self):
        output = read("SKILL.md").split("## Output", 1)[1]
        template = output.split("```text\n", 1)[1].split("\n```", 1)[0]
        self.assertTrue(template.startswith("On-call questions:"), template[:60])

    def test_guide_mirrors_skill(self):
        self.assertTrue(body(read("SKILL.md")) == read("GUIDE.md").lstrip("\n"),
                        "GUIDE.md must equal the SKILL.md body")

    def test_skill_length_budget(self):
        self.assertLessEqual(len(read("SKILL.md").splitlines()), 320)

    def test_operational_example_unchanged(self):
        for rel in ("SKILL.md", "GUIDE.md"):
            text = read(rel)
            code = text.split("```python andino-operational-example\n", 1)[1].split("\n```", 1)[0]
            with self.subTest(file=rel):
                self.assertEqual(hashlib.sha256(code.encode()).hexdigest(), PROBE_SHA256)
                self.assertIn('set(labels)-{"route","status_class","provider"}', code)

    def test_andino_anchors(self):
        self._anchors(ANDINO_ANCHORS)

    def test_reference_anchors(self):
        self._anchors(REFERENCE_ANCHORS)

    def test_resources_linked(self):
        skill = read("SKILL.md")
        resources = sorted(p.name for p in (SKILL / "resources").glob("*.md"))
        self.assertEqual(resources, ["signal-recipes.md", "telemetry-checklist.md",
                                     "worked-example.md"])
        for name in resources:
            with self.subTest(resource=name):
                self.assertIn(f"](resources/{name})", skill)

    def _anchors(self, table):
        for rel, literals in table.items():
            path = SKILL / rel
            self.assertTrue(path.is_file(), f"missing {rel}")
            text = flat(read(rel))
            for literal in literals:
                with self.subTest(file=rel, anchor=literal):
                    self.assertIn(literal.lower(), text, f"{rel}: missing anchor {literal!r}")


if __name__ == "__main__":
    unittest.main()
