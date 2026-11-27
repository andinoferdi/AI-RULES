"""Guard andino-writing-tickets against silent loss.

The anchors cover what the member keeps from Matt Pocock's to-tickets (tracer bullets, blocking
edges, prefactoring, expand-contract, the quiz, local and tracker publishing, durable tickets,
the frontier) and the Andino additions (HITL tickets for open decisions, reruns without
duplicates, the reader check, observable criteria, the local/remote authority split, the graph
check). A failing anchor means a rule or resource was dropped. The test reads the real folder.
"""

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/andino-workflow/skills/writing-tickets"

SECTIONS = ["Purpose", "Trigger and non-trigger", "Select a resource, not a second lifecycle",
            "Prerequisites", "Procedure", "Rules", "Shortcuts", "Red flags",
            "Ownership and permission boundary", "Output", "Verification",
            "Worked example and anti-pattern", "Fallback", "Local resources",
            "Operational example", "Provenance"]

ANCHORS = {
    "SKILL.md": [
        "tracer-bullet", "vertical slices", "**block**", "**frontier**", "prefactoring",
        "make the change easy, then make the easy change", "**blocking edges**", "AFK", "HITL",
        "expand-contract", "**blast radius**", "integration branch", "integrate-and-verify",
        "ready-for-human", "A decision dropped from the tracker is lost", "A rerun",
        "a done ticket is never edited", "number after the highest existing one", "Quiz the user",
        "too coarse", "approved the breakdown they saw", "reader check", "ticket_graph.py",
        "`OK <n> tickets`", "Never close, retitle or edit a parent issue", "prototype snippet",
        "_Avoid_", "naming the tracker is not that", "issue's body and every comment",
        "skills/planning/resources/dependency-slicing/guide.md", "Frontier (can start now)",
    ],
    "resources/ticket-template.md": [
        "One file per ticket", "Never one combined file", "**Blocked by:**", "**Out of scope:**",
        "**Owner:**", "native blocking links and sub-issues", "Acceptance criteria", "Sizing",
        "AFK and HITL", "The reader check", "tracker's own strings",
    ],
    "resources/publishing.md": [
        ".scratch/<feature>/issues/", "dependency order", "gh auth status", "sub_issues",
        "dependencies/blocked_by", "numeric database id", "Never close, retitle or edit the parent",
        "Reruns without duplicates", "Leave it alone", "dated line", "configuration wins",
    ],
    "resources/worked-example.md": [
        "prefactor", "HITL", "OK 5 tickets", "A rerun", "No ticket exists\ntwice",
    ],
}

# Words from the trial fixture (docs/validation/writing-tickets). The skill must not carry them,
# or the trial would measure fit to the fixture instead of the method.
FIXTURE_WORDS = ["roomy", "waitlist", "Dana", "Yusuf", "facilities", "member_id", "account_id",
                 "--weekly", "daylight", "atlas", "orion"]

FENCE = re.compile(r"^```.*?^```[^\n]*$", re.M | re.S)


def read(rel):
    return (SKILL / rel).read_text(encoding="utf-8")


class WritingTicketsPreservation(unittest.TestCase):
    def test_guide_mirrors_skill_body(self):
        skill = read("SKILL.md")
        self.assertTrue(skill.startswith("---\nname: andino-writing-tickets\ndescription: Use when "))
        body = skill.split("\n---\n", 1)[1].lstrip("\n")
        self.assertEqual(body, read("GUIDE.md"))

    def test_sections_in_order(self):
        headings = re.findall(r"^## (.+)$", FENCE.sub("", read("SKILL.md")), re.M)
        positions = []
        for section in SECTIONS:
            match = [i for i, h in enumerate(headings) if h.startswith(section)]
            self.assertTrue(match, section)
            positions.append(match[0])
        self.assertEqual(sorted(positions), positions)

    def test_anchors(self):
        for rel, anchors in ANCHORS.items():
            text = read(rel)
            for anchor in anchors:
                with self.subTest(file=rel, anchor=anchor):
                    self.assertIn(anchor, text)

    def test_every_step_ends_on_done_when(self):
        procedure = read("SKILL.md").split("## Procedure", 1)[1].split("\n## ", 1)[0]
        steps = re.split(r"^\d\. ", procedure, flags=re.M)[1:]
        self.assertEqual(7, len(steps))
        for number, step in enumerate(steps, 1):
            with self.subTest(step=number):
                self.assertIn("Done when", step)

    def test_no_fixture_words(self):
        for path in SKILL.rglob("*.md"):
            text = path.read_text(encoding="utf-8").casefold()
            for word in FIXTURE_WORDS:
                with self.subTest(file=path.name, word=word):
                    self.assertNotIn(word.casefold(), text)

    def test_links_resolve(self):
        for path in SKILL.rglob("*.md"):
            for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", path.read_text(encoding="utf-8")):
                if target.startswith("http"):
                    continue
                with self.subTest(file=path.name, target=target):
                    self.assertTrue((path.parent / target).exists())

    def test_operational_example_runs_and_fails_when_negated(self):
        block = re.search(r"```python andino-operational-example\n(.*?)```", read("SKILL.md"), re.S)
        self.assertIsNotNone(block)
        with tempfile.TemporaryDirectory() as temp:
            script = Path(temp) / "example.py"
            script.write_text(block[1], encoding="utf-8")
            ok = subprocess.run([sys.executable, str(script)], capture_output=True)
            negative = subprocess.run([sys.executable, str(script)], capture_output=True,
                                      env=dict(os.environ, ANDINO_NEGATIVE="1"))
        self.assertEqual(0, ok.returncode, ok.stderr)
        self.assertEqual(1, negative.returncode)

    def test_neighbours_route_tickets_here(self):
        for member in ("planning", "issue-triage"):
            for name in ("SKILL.md", "GUIDE.md"):
                text = (SKILL.parent / member / name).read_text(encoding="utf-8")
                with self.subTest(member=member, file=name):
                    self.assertIn("`writing-tickets`", text.split("## Select a resource", 1)[0])


if __name__ == "__main__":
    unittest.main()
