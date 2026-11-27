"""Build the fixture for the writing-tickets comparison trial.

    python -I build_tickets_fixture.py RUN_DIR

Creates RUN_DIR/roomy, a small git repository for a room-booking command-line tool, and an
empty RUN_DIR/out for the runner's proposals and reports. Every build is byte-identical: fixed
file contents, fixed author and fixed commit dates, so the commit hashes match across arms.
"""
import os
import subprocess
import sys
from pathlib import Path

AUTHOR = {
    "GIT_AUTHOR_NAME": "Rin Maintainer", "GIT_AUTHOR_EMAIL": "rin@example.invalid",
    "GIT_COMMITTER_NAME": "Rin Maintainer", "GIT_COMMITTER_EMAIL": "rin@example.invalid",
}

FILES_1 = {
    "README.md": """# roomy

Book shared meeting rooms from the command line.

    python -m roomy book --room atlas --slot 2026-03-02T09 --member m-17
    python -m roomy cancel --booking b-0003
    python -m roomy list --room atlas

Run the tests with `python -m unittest discover -s tests`.
""",
    "CONTEXT.md": """# Glossary

**Room**: a bookable meeting room, identified by a short lowercase name (`atlas`).
**Slot**: one hour of one room, written `YYYY-MM-DDTHH` (`2026-03-02T09`).
**Booking**: a Member's claim on one Slot of one Room. _Avoid_: reservation, appointment.
**Member**: a person allowed to book, identified by a member id (`m-17`).
**Waitlist**: the ordered queue of Members waiting for a fully booked Slot. _Avoid_: queue,
standby list.
""",
    "docs/adr/0001-bookings-in-one-json-file.md": """# 1. Bookings live in one JSON file

Status: accepted

All bookings are stored in `data/bookings.json` and read and written whole by the store
module. We do not add a database; anything new that must survive a restart goes into the same
file under its own top-level key. Old files must keep loading after every change.
""",
    "docs/agents/issue-tracker.md": """# Issue tracker

Tracker: local Markdown in this repository.

- One folder per feature: `.scratch/<feature>/issues/`.
- One file per ticket, named `NN-<slug>.md`, numbered from `01`.
- "Blocked by" names ticket numbers in the same folder.
- State labels are in `docs/agents/triage-labels.json`; write the label string, not the role.
- Any ticket text written by an AI starts with the line `> *Drafted by AI for roomy.*`
""",
    "docs/agents/triage-labels.json": """{
  "needs-triage": "triage",
  "needs-info": "waiting",
  "ready-for-agent": "agent-ready",
  "ready-for-human": "human-ready",
  "wontfix": "declined"
}
""",
    "roomy/__init__.py": "",
    "roomy/__main__.py": "from roomy.cli import main\n\nmain()\n",
    "roomy/store.py": '''import json
from pathlib import Path

DATA = Path("data/bookings.json")


def load(path=DATA):
    if not path.exists():
        return {"bookings": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save(state, path=DATA):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")
''',
    "roomy/bookings.py": '''from roomy import store


class SlotTaken(Exception):
    pass


def create_booking(room, slot, member_id, path=store.DATA):
    state = store.load(path)
    for b in state["bookings"]:
        if b["room"] == room and b["slot"] == slot and not b.get("cancelled"):
            raise SlotTaken(f"{room} {slot} is already booked")
    booking_id = f"b-{len(state['bookings']) + 1:04d}"
    state["bookings"].append({"id": booking_id, "room": room, "slot": slot,
                              "member_id": member_id})
    store.save(state, path)
    return booking_id


def cancel_booking(booking_id, path=store.DATA):
    state = store.load(path)
    for b in state["bookings"]:
        if b["id"] == booking_id:
            b["cancelled"] = True
            store.save(state, path)
            return b
    raise KeyError(booking_id)


def bookings_for_room(room, path=store.DATA):
    state = store.load(path)
    return [b for b in state["bookings"]
            if b["room"] == room and not b.get("cancelled")]


def is_free(room, slot, path=store.DATA):
    state = store.load(path)
    return not any(b["room"] == room and b["slot"] == slot and not b.get("cancelled")
                   for b in state["bookings"])


def bookings_for_member(member_id, path=store.DATA):
    state = store.load(path)
    return [b for b in state["bookings"]
            if b["member_id"] == member_id and not b.get("cancelled")]
''',
    "roomy/report.py": '''from roomy import store


def usage_by_member(path=store.DATA):
    counts = {}
    for b in store.load(path)["bookings"]:
        if not b.get("cancelled"):
            counts[b["member_id"]] = counts.get(b["member_id"], 0) + 1
    return counts


def format_usage(counts):
    return "\\n".join(f"{member_id}: {n}" for member_id, n in sorted(counts.items()))
''',
    "roomy/export.py": '''import json

from roomy import store


def export_json(room=None, path=store.DATA):
    rows = [b for b in store.load(path)["bookings"] if not b.get("cancelled")]
    if room:
        rows = [b for b in rows if b["room"] == room]
    return json.dumps(rows, indent=2)
''',
    "roomy/cli.py": '''import argparse

from roomy import bookings, export, report


def main(argv=None):
    parser = argparse.ArgumentParser(prog="roomy")
    sub = parser.add_subparsers(dest="command", required=True)
    book = sub.add_parser("book")
    book.add_argument("--room", required=True)
    book.add_argument("--slot", required=True)
    book.add_argument("--member", dest="member_id", required=True)
    cancel = sub.add_parser("cancel")
    cancel.add_argument("--booking", required=True)
    listing = sub.add_parser("list")
    listing.add_argument("--room", required=True)
    sub.add_parser("usage")
    exp = sub.add_parser("export")
    exp.add_argument("--room")
    args = parser.parse_args(argv)

    if args.command == "book":
        try:
            print(bookings.create_booking(args.room, args.slot, args.member_id))
        except bookings.SlotTaken as error:
            print(f"error: {error}")
            return 1
    elif args.command == "cancel":
        b = bookings.cancel_booking(args.booking)
        print(f"cancelled {b['id']} ({b['room']} {b['slot']}, member {b['member_id']})")
    elif args.command == "list":
        for b in bookings.bookings_for_room(args.room):
            print(f"{b['slot']} {b['id']} {b['member_id']}")
    elif args.command == "usage":
        print(report.format_usage(report.usage_by_member()))
    elif args.command == "export":
        print(export.export_json(args.room))
    return 0
''',
    "tests/test_bookings.py": '''import tempfile
import unittest
from pathlib import Path

from roomy import bookings


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / "bookings.json"

    def test_second_booking_of_same_slot_is_refused(self):
        bookings.create_booking("atlas", "2026-03-02T09", "m-1", self.path)
        with self.assertRaises(bookings.SlotTaken):
            bookings.create_booking("atlas", "2026-03-02T09", "m-2", self.path)

    def test_cancelled_slot_is_free_again(self):
        booking_id = bookings.create_booking("atlas", "2026-03-02T09", "m-1", self.path)
        bookings.cancel_booking(booking_id, self.path)
        self.assertTrue(bookings.is_free("atlas", "2026-03-02T09", self.path))

    def test_bookings_for_member(self):
        bookings.create_booking("atlas", "2026-03-02T09", "m-1", self.path)
        self.assertEqual(1, len(bookings.bookings_for_member("m-1", self.path)))


if __name__ == "__main__":
    unittest.main()
''',
    "data/bookings.json": """{
  "bookings": [
    {"id": "b-0001", "room": "atlas", "slot": "2026-03-02T09", "member_id": "m-17"},
    {"id": "b-0002", "room": "atlas", "slot": "2026-03-02T10", "member_id": "m-04",
     "cancelled": true},
    {"id": "b-0003", "room": "orion", "slot": "2026-03-02T09", "member_id": "m-04"}
  ]
}
""",
    "docs/specs/export.md": """# Export bookings

Members of the facilities team export bookings for their own spreadsheets.

1. `roomy export` prints every active Booking as JSON.
2. `roomy export --room <room>` limits the export to one Room.
""",
    ".scratch/export/issues/01-export-bookings-as-json.md": """> *Drafted by AI for roomy.*

# 01: Export active bookings as JSON

**Status:** done

**Blocked by:** None

`roomy export` prints every active Booking as a JSON array.

- [x] `roomy export` on the sample data prints b-0001 and b-0003, not the cancelled b-0002
""",
    ".scratch/export/issues/02-export-one-room.md": """> *Drafted by AI for roomy.*

# 02: Limit the export to one room

**Status:** agent-ready

**Blocked by:** 01

`roomy export --room <room>` prints only that Room's active Bookings.

- [ ] `roomy export --room orion` on the sample data prints only b-0003
- [ ] `roomy export --room nowhere` prints `[]`
""",
}

FILES_2 = {
    "docs/specs/export.md": """# Export bookings

Members of the facilities team export bookings for their own spreadsheets.

1. `roomy export` prints every active Booking as JSON.
2. `roomy export --room <room>` limits the export to one Room.
3. `roomy export --format csv` prints the same rows as CSV with the header
   `id,room,slot,member_id`; JSON stays the default.
4. `roomy export --from <date> --to <date>` keeps Bookings whose Slot date falls in that range,
   both ends included. It combines with `--room` and with `--format`.
""",
}

FILES_3 = {
    "docs/specs/waitlist.md": """# Waitlist

When a Slot is already booked, a Member can join its Waitlist instead of trying again later.

1. `roomy book` on a booked Slot offers the Waitlist: `roomy waitlist join --room <room>
   --slot <slot> --member <member id>` adds the Member to the end of that Slot's Waitlist and
   prints their position.
2. When a Booking is cancelled, the first Member on that Slot's Waitlist gets the Booking
   automatically. `roomy cancel` prints who received it.
3. `roomy waitlist show --room <room> --slot <slot>` prints the Waitlist in order.
4. A Member already holding a Booking for that Slot cannot join its Waitlist.
5. Waitlists survive a restart (see ADR 0001).
""",
    "notes/waitlist-chat.md": """# Waitlist chat, 2026-02-20

Participants: Rin (maintainer), Dana (product), Yusuf (facilities)

Yusuf: People forget they joined. Can entries go stale?
Dana: Yes. A Waitlist entry expires 24 hours after it was made. Expired entries are skipped
when a cancelled Booking is handed on.
Rin: Fine. Email notifications came up again; not now. The command output is the only
notification for this release.
Yusuf: Can one Member wait for two Slots at the same hour, say atlas and orion?
Dana: I haven't decided that. Don't build either behaviour until I say. Everything else in the
spec is settled.
Rin: Note for whoever builds this: the "is this Slot taken" check is copied in three places in
the bookings module. The Waitlist will need it a fourth time.
""",
    "docs/plans/recurring-bookings.md": """# Recurring bookings implementation plan

Spec: Members can book the same Slot time every week for up to 8 weeks with
`roomy book --room <room> --slot <slot> --member <id> --weekly <n>`.

## Tasks

### T1 - Store schema
Files: Modify `roomy/store.py` (`load`, `save`); Test `tests/test_store.py`
Add a `series` key to the top-level dict in `data/bookings.json`; `load()` returns
`{"bookings": [], "series": []}` for old files. Line 7 of `roomy/store.py` changes.

### T2 - Recurrence logic
Files: Create `roomy/recurrence.py`; Test `tests/test_recurrence.py`
`def weekly_slots(slot: str, weeks: int) -> list[str]` returns the slot and the same hour on
the following weeks. `def create_series(room, slot, member_id, weeks, path) -> str` books each
slot, refusing the whole series when any slot is taken (`SlotTaken`).

### T3 - CLI flag
Files: Modify `roomy/cli.py` (`main`, the `book` subparser at line 9)
Add `--weekly <n>` (1 to 8) and print the series id.

### T4 - Docs
Files: Modify `README.md`
Document `--weekly`.

## Blocked
D1: whether weekly Slots follow the room's local time across a daylight-saving change is not
decided. Rin asks facilities; until then nothing about time zones is built.
""",
}



def git(repo, *args, date=None):
    env = dict(os.environ, **AUTHOR)
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "init.defaultBranch=main", *args],
                   cwd=repo, env=env, check=True, capture_output=True)


def write(repo, files):
    for name, text in files.items():
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python -I build_tickets_fixture.py RUN_DIR")
    run_dir = Path(sys.argv[1]).resolve()
    repo = run_dir / "roomy"
    if repo.exists():
        sys.exit(f"{repo} already exists")
    repo.mkdir(parents=True)
    (run_dir / "out").mkdir(exist_ok=True)
    git(repo, "init", "-q")
    write(repo, FILES_1)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "roomy: book, cancel, list, usage, export", date="2026-02-02T10:00:00+0000")
    write(repo, FILES_2)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "Export spec: CSV format and date range", date="2026-02-16T10:00:00+0000")
    write(repo, FILES_3)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "Waitlist spec, chat notes, recurring bookings plan", date="2026-02-21T10:00:00+0000")
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=repo,
                          capture_output=True, text=True, check=True).stdout.strip()
    print(f"built {repo} at {head}")


if __name__ == "__main__":
    main()
