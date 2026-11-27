"""Behaviour of the andino-writing-tickets graph check (scripts/ticket_graph.py).

The helper reads one local ticket folder and reports what would make the set unsafe to work:
blockers that do not exist, cycles, blockers numbered after their dependents, duplicate
titles, tickets without acceptance criteria and repository paths in ticket bodies.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/andino-workflow/skills/writing-tickets/scripts/ticket_graph.py"


def ticket(number, title, blocked_by="None (can start immediately)", body="Behaviour.",
           criteria=("- [ ] `roomy list --room atlas` prints one line",)):
    return "\n".join([
        "> *Drafted by AI.*", "", f"# {number}: {title}", "",
        "**Status:** agent-ready", "", f"**Blocked by:** {blocked_by}", "", body, "",
        *criteria, "",
    ])


class TicketGraphTests(unittest.TestCase):
    def run_on(self, files):
        folder = Path(tempfile.mkdtemp())
        for name, text in files.items():
            (folder / name).write_text(text, encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), str(folder)],
                                capture_output=True, text=True, encoding="utf-8")
        return result.returncode, result.stdout.strip().splitlines()

    def test_valid_chain_passes(self):
        code, lines = self.run_on({
            "01-consolidate-slot-check.md": ticket("01", "Consolidate the slot check"),
            "02-join-waitlist.md": ticket("02", "Join a waitlist", "01"),
            "03-hand-on-cancelled-booking.md": ticket("03", "Hand on a cancelled booking", "#01, #02"),
        })
        self.assertEqual((0, ["OK 3 tickets"]), (code, lines))

    def test_unknown_blocker(self):
        code, lines = self.run_on({
            "01-a.md": ticket("01", "First"),
            "02-b.md": ticket("02", "Second", "01, 07"),
        })
        self.assertEqual((1, ["02: unknown blocker 07"]), (code, lines))

    def test_cycle(self):
        code, lines = self.run_on({
            "01-a.md": ticket("01", "First", "02"),
            "02-b.md": ticket("02", "Second", "01"),
        })
        self.assertEqual(1, code)
        self.assertIn("01: cycle", lines)
        self.assertIn("02: cycle", lines)

    def test_blocker_numbered_after_dependent(self):
        code, lines = self.run_on({
            "01-a.md": ticket("01", "First", "02"),
            "02-b.md": ticket("02", "Second"),
        })
        self.assertEqual((1, ["01: blocked by later ticket 02"]), (code, lines))

    def test_duplicate_title(self):
        code, lines = self.run_on({
            "01-a.md": ticket("01", "Export bookings as CSV"),
            "02-b.md": ticket("02", "Export bookings as CSV.", "01"),
        })
        self.assertEqual((1, ["02: duplicate title of 01"]), (code, lines))

    def test_missing_acceptance_criteria(self):
        code, lines = self.run_on({"01-a.md": ticket("01", "First", criteria=())})
        self.assertEqual((1, ["01: no acceptance criteria"]), (code, lines))

    def test_missing_blocked_by_line(self):
        text = ticket("01", "First").replace("**Blocked by:** None (can start immediately)", "")
        code, lines = self.run_on({"01-a.md": text})
        self.assertEqual((1, ["01: no Blocked by line"]), (code, lines))

    def test_path_in_body_but_not_in_code_fence(self):
        body = "Change `roomy/bookings.py` near line 12.\n\n```python\nfrom roomy import store\n# roomy/store.py\n```"
        code, lines = self.run_on({"01-a.md": ticket("01", "First", body=body)})
        self.assertEqual((1, ["01: file path in body roomy/bookings.py",
                              "01: line number in body line 12"]), (code, lines))

    def test_empty_folder_and_bad_argument(self):
        code, lines = self.run_on({})
        self.assertEqual((1, ["no NN-*.md tickets found"]), (code, lines))
        missing = subprocess.run([sys.executable, str(SCRIPT), str(ROOT / "no-such-folder")],
                                 capture_output=True, text=True)
        self.assertEqual(2, missing.returncode)


if __name__ == "__main__":
    unittest.main()
