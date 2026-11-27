"""Build the disposable repository used for documentation-and-adrs skill trials.

Usage: python -I build_docs_fixture.py <run-dir>

Creates, inside <run-dir>:
  repo/   a small hall-booking service with a fixed git history:
          Task 1  meeting notes to turn into an architecture decision record
          Task 2  a last commit that changed cancellations, with stale API docs
          Task 3  module docs in docs/modules/, some stale, one with unordered history
          Task 4  hall/slots.py with comments to clean up
  out/    empty output folder

Standard library and git only. Commit dates and authors are fixed, so the
commit SHAs are the same on every build.
"""
import os
import subprocess
import sys
from pathlib import Path

GIT = ["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
       "-c", "init.defaultBranch=main", "-c", "merge.ff=false"]

# ---------------------------------------------------------------- shared text

README = """# Hall bookings

Bookings, prices and reminders for the community sports hall. Python standard
library only (ADR-0002).

Run the tests from the repository root:

    python -m unittest discover -s tests -t .

Module notes live in `docs/modules/`, the members API in `docs/api.md`, and
architecture decisions in `architecture/decisions/`.
"""

ADR_TEMPLATE = """# NNNN. Short title of the decision

* Status: proposed | accepted | superseded by [NNNN](NNNN-title.md)
* Deciders: names
* Date: YYYY-MM-DD

## Context and Problem Statement

What forces the decision, with the evidence.

## Considered Options

* Option one
* Option two

## Decision Outcome

Chosen option: "Option one", because ...

### Consequences

* Good, because ...
* Bad, because ...

## Pros and Cons of the Options

### Option one

* Good, because ...
* Bad, because ...
"""

ADR_INDEX_ROWS = [
    ("0001", "0001-record-architecture-decisions.md", "Record architecture decisions", "accepted"),
    ("0002", "0002-standard-library-only.md", "Python standard library only", "accepted"),
    ("0003", "0003-sqlite-storage.md", "SQLite for storage", "accepted"),
    ("0004", "0004-in-process-reminder-timers.md", "Schedule reminders with in-process timers", "accepted"),
    ("0005", "0005-venue-local-naive-times.md", "Venue-local naive times", "accepted"),
    ("0006", "0006-integer-cents.md", "Integer cents for money", "accepted"),
    ("0007", "0007-email-outbox.md", "E-mail through an outbox table", "accepted"),
]


def adr_index(count, reserved=False):
    lines = [
        "# Architecture decisions",
        "",
        "One file per decision, `NNNN-short-title.md`, copied from `template.md`.",
        "To add one: copy `template.md`, use the next number and add a row here.",
        "",
        "| No. | Decision | Status |",
        "| --- | --- | --- |",
    ]
    for number, name, title, status in ADR_INDEX_ROWS[:count]:
        lines.append(f"| [{number}]({name}) | {title} | {status} |")
    if reserved:
        lines.append("| 0008 | Rate limits for the public API | number reserved for draft PR #91 |")
    return "\n".join(lines) + "\n"


def adr(number, title, deciders, date, context, options, outcome, consequences):
    option_lines = "\n".join(f"* {o}" for o in options)
    consequence_lines = "\n".join(f"* {c}" for c in consequences)
    return f"""# {number}. {title}

* Status: accepted
* Deciders: {deciders}
* Date: {date}

## Context and Problem Statement

{context}

## Considered Options

{option_lines}

## Decision Outcome

{outcome}

### Consequences

{consequence_lines}
"""


ADR_0001 = adr(
    "0001", "Record architecture decisions", "Rina Hartono", "2025-01-10",
    "We want to remember why the service is built the way it is.",
    ["Architecture decision records in `architecture/decisions/`", "A wiki page"],
    'Chosen option: "Architecture decision records", because they live next to the code and are reviewed with it.',
    ["Good, because the reasons travel with the code.",
     "Bad, because someone has to write them."],
)
ADR_0002 = adr(
    "0002", "Python standard library only", "Rina Hartono", "2025-01-10",
    "The service runs on the hall's own Windows server with no package mirror and no one to patch dependencies.",
    ["Standard library only", "Third-party packages from PyPI"],
    'Chosen option: "Standard library only", because nobody is available to track and patch dependencies.',
    ["Good, because there is nothing to install or patch.",
     "Bad, because we write small things ourselves, and there is no time zone database."],
)
ADR_0003 = adr(
    "0003", "SQLite for storage", "Rina Hartono", "2025-01-10",
    "One service process, under a thousand bookings a week, one server.",
    ["SQLite", "PostgreSQL"],
    'Chosen option: "SQLite", because it ships with Python (ADR-0002) and needs no server.',
    ["Good, because backups are a file copy.",
     "Bad, because only one process should write at a time."],
)
ADR_0004 = adr(
    "0004", "Schedule reminders with in-process timers", "Rina Hartono", "2025-03-02",
    "Members asked for an e-mail before their booking. We run one service process and no job runner.",
    ["A `threading.Timer` per booking in the service process",
     "A cron job that scans bookings every few minutes"],
    'Chosen option: "A `threading.Timer` per booking", because it needs no extra process and the hall has under 200 bookings a week.',
    ["Good, because there is nothing else to deploy.",
     "Bad, because timers live in memory: a restart or crash loses every reminder still waiting. "
     "Acceptable while restarts are rare and planned at night."],
)
ADR_0005 = adr(
    "0005", "Venue-local naive times", "Rina Hartono, Tomás Ibáñez", "2025-06-10",
    "The hall is in Amsterdam. Members, the caretaker and the paper timetable all use local time.",
    ["Naive datetimes in venue local time", "Aware UTC datetimes converted at the edges"],
    'Chosen option: "Naive datetimes in venue local time", because everyone reads local time and '
    "ADR-0002 leaves us without a time zone database.",
    ["Good, because stored times read the same as the timetable.",
     "Bad, because `datetime.now()` is compared with booking times directly, so the service host "
     "must run in the Europe/Amsterdam time zone. On a host set to UTC the service would accept "
     "starts that are already up to 2 hours in the past in summer (1 hour in winter).",
     "Neutral, because the hour that does not exist when clocks go forward (02:00 to 03:00) is "
     "before opening time (08:00), so no slot falls in it."],
)
ADR_0006 = adr(
    "0006", "Integer cents for money", "Rina Hartono", "2025-07-15",
    "Prices and refunds were stored as floats in a prototype and drifted by a cent.",
    ["Integer cents", "`decimal.Decimal`"],
    'Chosen option: "Integer cents", because sums stay exact and SQLite stores them natively.',
    ["Good, because amounts are exact.",
     "Bad, because divisions must state their rounding."],
)
ADR_0007 = adr(
    "0007", "E-mail through an outbox table", "Rina Hartono", "2025-07-15",
    "Sending e-mail inside a request made requests slow when the mail server was slow.",
    ["Queue messages in an outbox table drained by a sender", "Send inside the request"],
    'Chosen option: "Queue messages in an outbox table", because requests no longer wait for the mail server.',
    ["Good, because requests stay fast.",
     "Bad, because an e-mail is sent later, not at once."],
)

CHANGELOG_1 = """# Changelog

All notable changes to this project are documented here. The format follows
Keep a Changelog.

## [Unreleased]

## [1.0.0] - 2025-01-10
### Added
- Court bookings with weekend pricing.
"""

CHANGELOG_2 = CHANGELOG_1.replace("## [1.0.0]", """## [1.2.0] - 2025-07-01
### Added
- Studio room at 80.00 per hour.
### Fixes
- Bokings that crossed midnight were accepted.

## [1.0.0]""")

CHANGELOG_3 = CHANGELOG_2.replace("## [1.2.0]", """## [1.3.0] - 2025-08-20
### Changed
- Access tokens expire after 30 minutes (was 60).

## [1.2.0]""")

CHANGELOG_4 = CHANGELOG_3.replace("## [1.3.0]", """## [1.4.0] - 2026-10-02
### Changed
- Weekend surcharge is now 20% (was 15%).
- Reminder e-mails go out 2 hours before the booking (was 24 hours).

## [1.3.0]""")

# ---------------------------------------------------------------- code

PRICING_1 = '''"""Room prices. Money is integer cents (ADR-0006)."""

HOURLY_RATE_CENTS = {
    "court": 12000,
}
WEEKEND_SURCHARGE_PERCENT = 15


def price_cents(room, hours, weekday):
    """Price of `hours` whole hours in `room`; weekday is 0 (Monday) to 6 (Sunday)."""
    base = HOURLY_RATE_CENTS[room] * hours
    if weekday >= 5:
        base += base * WEEKEND_SURCHARGE_PERCENT // 100
    return base
'''
PRICING_2 = PRICING_1.replace('    "court": 12000,\n', '    "court": 12000,\n    "studio": 8000,\n')
PRICING_3 = PRICING_2.replace("WEEKEND_SURCHARGE_PERCENT = 15", "WEEKEND_SURCHARGE_PERCENT = 20")

PRICING_DOC_1 = """# Pricing

`hall/pricing.py` computes the price of a booking.

- Court: 120.00 per hour.
- Weekend bookings (Saturday and Sunday) cost 15% more. The surcharge is
  rounded down to the cent.
- All amounts are integer cents (ADR-0006).

## Change log

- 2025-01-10: First version.
"""
PRICING_DOC_2 = PRICING_DOC_1.replace(
    "- Court: 120.00 per hour.\n", "- Court: 120.00 per hour.\n- Studio: 80.00 per hour.\n"
) + "- 2025-07-01: Added the studio rate.\n"

BOOKINGS_1 = '''"""Create bookings."""
from hall.pricing import HOURLY_RATE_CENTS, price_cents

MIN_HOURS = 1
MAX_HOURS = 4


class BookingError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def create_booking(room, start, hours, member_email):
    if room not in HOURLY_RATE_CENTS:
        raise BookingError("unknown_room")
    if not MIN_HOURS <= hours <= MAX_HOURS:
        raise BookingError("invalid_hours")
    p = price_cents(room, hours, start.weekday())
    return {"room": room, "start": start, "hours": hours,
            "member_email": member_email, "paid_cents": p, "status": "confirmed"}
'''
BOOKINGS_2 = BOOKINGS_1.replace(
    '''    p = price_cents(room, hours, start.weekday())
    return {"room": room, "start": start, "hours": hours,
            "member_email": member_email, "paid_cents": p, "status": "confirmed"}
''',
    '''    amount_cents = price_cents(room, hours, start.weekday())
    booking = {
        "room": room,
        "start": start,
        "hours": hours,
        "member_email": member_email,
        "paid_cents": amount_cents,
        "status": "confirmed",
    }
    return booking
''')

BOOKINGS_DOC = """# Bookings

`hall/bookings.py` creates bookings.

- A booking lasts 1 to 4 whole hours. Other lengths fail with `invalid_hours`.
- An unknown room fails with `unknown_room`.
- A new booking is `confirmed` and records the price paid in `paid_cents`.

## Change log

- 2025-01-10: First version.
"""

REMINDERS_1 = '''"""Reminder e-mails before a booking (ADR-0004: in-process timers)."""
import threading
from datetime import timedelta

LEAD_TIME = timedelta(hours=24)
RETRIES = 3


def reminder_time(booking):
    return booking["start"] - LEAD_TIME


def schedule(booking, now, send):
    delay = (reminder_time(booking) - now).total_seconds()
    if delay <= 0:
        return None
    timer = threading.Timer(delay, send_with_retries, args=(booking, send))
    timer.daemon = True
    timer.start()
    return timer


def send_with_retries(booking, send):
    for _ in range(1 + RETRIES):
        try:
            send(booking)
            return True
        except OSError:
            continue
    return False
'''
REMINDERS_2 = REMINDERS_1.replace("timedelta(hours=24)", "timedelta(hours=2)")

REMINDERS_DOC_1 = """# Reminders

`hall/reminders.py` e-mails members before their booking.

- Members get a reminder 24 hours before the booking starts.
- A booking made less than 24 hours ahead gets no reminder.
- Reminders run on in-process timers (ADR-0004), so a restart loses the ones
  still waiting.

## Change log

- 2025-03-02: First version.
"""
REMINDERS_DOC_2 = REMINDERS_DOC_1.replace("## Change log", """## Retries

A failed send (an `OSError` from the mail call) is retried up to 3 times
straight away, with no delay between attempts.

## Change log""") + "- 2026-09-20: Documented retries.\n"

AUTH_1 = '''"""Access tokens for the members API."""
from datetime import timedelta

TOKEN_LIFETIME = timedelta(minutes=60)


def token_expiry(issued_at):
    return issued_at + TOKEN_LIFETIME


def is_valid(issued_at, now):
    return issued_at <= now < token_expiry(issued_at)
'''
AUTH_2 = AUTH_1.replace("minutes=60", "minutes=30")

AUTH_DOC_1 = """# Access tokens

`hall/auth.py` decides whether a members API token is still valid.

- Access tokens expire 60 minutes after they are issued.
- A token is valid from its issue time up to, but not including, its expiry.

## Change log

- 2025-08-01: First version.
"""
AUTH_DOC_2 = AUTH_DOC_1.replace("expire 60 minutes", "expire 30 minutes") + \
    "- 2025-08-18: Token lifetime is 30 minutes.\n"

SLOTS = '''"""Which slots can be booked."""
from datetime import datetime, timedelta

OPENING_HOUR = 8
CLOSING_HOUR = 23


def is_bookable(start, hours, now=None):
    # careful with the time stuff here!!
    now = now or datetime.now()
    # check if start is in the past
    if start <= now:
        return False
    # TODO: add error handling
    if start.minute or start.second or start.microsecond:
        # TODO(#88): allow half-hour starts once the venue confirms staffing.
        return False
    # old version, keep just in case
    # if start.minute != 0:
    #     raise ValueError("slots start on the hour")
    # compute the end
    end = start + timedelta(hours=hours)
    # opening hours
    if start.hour < OPENING_HOUR:
        return False
    if end.date() != start.date() or end.hour > CLOSING_HOUR:
        return False
    return True
'''

OUTBOX = '''"""Outgoing e-mail queue (ADR-0007). A separate sender drains it."""
MESSAGES = []


def enqueue(to, template, **fields):
    MESSAGES.append({"to": to, "template": template, **fields})
'''

CANCEL_1 = '''"""Cancel bookings."""
from hall import outbox


def cancel(booking, now):
    if booking["status"] == "cancelled":
        return {"status": "cancelled", "refund_cents": booking["refund_cents"]}
    booking["status"] = "cancelled"
    booking["refund_cents"] = booking["paid_cents"]
    outbox.enqueue(booking["member_email"], "booking_cancelled",
                   refund_cents=booking["refund_cents"])
    return {"status": "cancelled", "refund_cents": booking["refund_cents"]}
'''
CANCEL_2 = '''"""Cancel bookings."""
from datetime import timedelta

from hall import outbox

LATE_WINDOW = timedelta(hours=24)
MAX_REASON_LENGTH = 200


class CancelError(Exception):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def cancel(booking, now, reason=None):
    if booking["status"] == "cancelled":
        raise CancelError(409, "already_cancelled", "This booking is already cancelled.")
    if reason is not None and len(reason) > MAX_REASON_LENGTH:
        raise CancelError(422, "reason_too_long", "Keep the reason to 200 characters.")
    late = booking["start"] - now < LATE_WINDOW
    if late and not (reason or "").strip():
        raise CancelError(422, "reason_required",
                          "Give a reason when cancelling less than 24 hours ahead.")
    refund = booking["paid_cents"] // 2 if late else booking["paid_cents"]
    booking["status"] = "cancelled"
    booking["refund_cents"] = refund
    booking["cancel_reason"] = reason
    outbox.enqueue(booking["member_email"], "booking_cancelled", refund_cents=refund)
    return {"status": "cancelled", "refund_cents": refund}
'''

API_1 = '''"""HTTP-shaped handlers. Each returns (status, body)."""
from hall import cancellations


def error(status, code, message):
    return status, {"error": {"code": code, "message": message}}


def handle_cancel(store, booking_id, body, now):
    booking = store.get(booking_id)
    if booking is None:
        return error(404, "not_found", "No booking with this id.")
    return 200, cancellations.cancel(booking, now)
'''
API_2 = API_1.replace(
    "    return 200, cancellations.cancel(booking, now)\n",
    '''    reason = (body or {}).get("reason")
    try:
        return 200, cancellations.cancel(booking, now, reason)
    except cancellations.CancelError as e:
        return error(e.status, e.code, e.message)
''')

API_DOC = """# Members API

Handlers live in `hall/api.py`. Every error body is
`{"error": {"code": ..., "message": ...}}`.

## POST /bookings/{id}/cancel

Cancels a booking and refunds the full amount paid.

Request body: none.

| Status | Body |
| --- | --- |
| 200 | `{"status": "cancelled", "refund_cents": <paid_cents>}` |
| 404 | error `not_found`: no booking with this id |

Cancelling a booking that is already cancelled returns 200 with the same body,
so clients can retry safely.

A cancellation e-mail is queued for the member (ADR-0007).
"""

NOTES = """# Reminders sync, 2026-11-18

Present: Rina Hartono (tech lead), Tomás Ibáñez, Ana Kovač.

## Problem

INC-311 (2026-11-12): the service was killed during a daytime deploy and 37
reminders still waiting on timers were never sent. Bookings are now about 900
a week (ADR-0004 assumed under 200), and we deploy in the daytime most weeks.

## Options discussed

1. Keep the timers and write pending reminders to disk on shutdown.
   Ana: does not help when the process is killed or crashes, which is what
   happened in INC-311.
2. A `reminders` table in SQLite (ADR-0003) and a separate worker process that
   polls it every 30 seconds and sends what is due.
3. A hosted task queue.
   Rina: needs a paid cloud account and someone on call for it; we have
   neither. Its client library would also break ADR-0002.

## Measurements

Ana ran the polling prototype once on staging: 1,200 reminders in one hour,
p95 delay 41 seconds after the due time, poll interval 30 seconds. The staging
database is a small copy (about 5% of production rows).

## Notes

- Only one worker may run. Two workers would both pick the same due row and
  send the reminder twice; we have not built row claiming yet.
- Tomás: the table and worker will scale to any load we will ever have.
- Sent reminders stay in the table; nobody has decided how long to keep them.

## Outcome

Option 2 is the proposal. Rina decides on Friday 2026-11-27 after reading the
write-up. Write it up as an ADR proposal now.
"""

# ---------------------------------------------------------------- tests

TEST_INIT = ""
TEST_PRICING_1 = '''import unittest

from hall.pricing import price_cents


class PricingTest(unittest.TestCase):
    def test_weekday_court(self):
        self.assertEqual(price_cents("court", 2, 0), 24000)

    def test_weekend_surcharge(self):
        self.assertEqual(price_cents("court", 2, 5), 27600)
'''
TEST_PRICING_3 = TEST_PRICING_1.replace("27600", "28800") + '''
    def test_studio(self):
        self.assertEqual(price_cents("studio", 1, 2), 8000)
'''

TEST_BOOKINGS = '''import unittest
from datetime import datetime

from hall.bookings import BookingError, create_booking


class BookingsTest(unittest.TestCase):
    def test_confirmed_with_price(self):
        booking = create_booking("court", datetime(2026, 12, 7, 10), 2, "m@example.test")
        self.assertEqual(booking["status"], "confirmed")
        self.assertEqual(booking["paid_cents"], 24000)

    def test_hours_out_of_range(self):
        for hours in (0, 5):
            with self.assertRaises(BookingError) as caught:
                create_booking("court", datetime(2026, 12, 7, 10), hours, "m@example.test")
            self.assertEqual(caught.exception.code, "invalid_hours")

    def test_unknown_room(self):
        with self.assertRaises(BookingError) as caught:
            create_booking("pool", datetime(2026, 12, 7, 10), 1, "m@example.test")
        self.assertEqual(caught.exception.code, "unknown_room")
'''

TEST_REMINDERS_1 = '''import unittest
from datetime import datetime

from hall import reminders


class RemindersTest(unittest.TestCase):
    def test_reminder_time(self):
        booking = {"start": datetime(2026, 12, 7, 10)}
        self.assertEqual(reminders.reminder_time(booking), datetime(2026, 12, 6, 10))

    def test_retries_then_gives_up(self):
        calls = []

        def send(booking):
            calls.append(booking)
            raise OSError("mail down")

        self.assertFalse(reminders.send_with_retries({}, send))
        self.assertEqual(len(calls), 4)
'''
TEST_REMINDERS_2 = TEST_REMINDERS_1.replace("datetime(2026, 12, 6, 10)", "datetime(2026, 12, 7, 8)")

TEST_AUTH_1 = '''import unittest
from datetime import datetime, timedelta

from hall import auth


class AuthTest(unittest.TestCase):
    def test_expiry(self):
        issued = datetime(2026, 1, 1, 12)
        self.assertEqual(auth.token_expiry(issued), issued + timedelta(minutes=60))
        self.assertFalse(auth.is_valid(issued, issued + timedelta(minutes=60)))
'''
TEST_AUTH_2 = TEST_AUTH_1.replace("minutes=60", "minutes=30")

TEST_SLOTS = '''import unittest
from datetime import datetime

from hall.slots import is_bookable

NOW = datetime(2026, 12, 1, 9)


class SlotsTest(unittest.TestCase):
    def test_future_slot_on_the_hour(self):
        self.assertTrue(is_bookable(datetime(2026, 12, 2, 10), 2, now=NOW))

    def test_past_start(self):
        self.assertFalse(is_bookable(datetime(2026, 12, 1, 8), 1, now=NOW))

    def test_half_hour_start(self):
        self.assertFalse(is_bookable(datetime(2026, 12, 2, 10, 30), 1, now=NOW))

    def test_before_opening(self):
        self.assertFalse(is_bookable(datetime(2026, 12, 2, 7), 2, now=NOW))

    def test_ends_at_closing(self):
        self.assertTrue(is_bookable(datetime(2026, 12, 2, 21), 2, now=NOW))

    def test_runs_past_closing(self):
        self.assertFalse(is_bookable(datetime(2026, 12, 2, 22), 2, now=NOW))

    def test_crosses_midnight(self):
        self.assertFalse(is_bookable(datetime(2026, 12, 2, 23), 1, now=NOW))
'''

TEST_CANCEL_1 = '''import unittest
from datetime import datetime

from hall import api, outbox


def store():
    return {1: {"start": datetime(2026, 12, 10, 10), "status": "confirmed",
                "paid_cents": 24000, "member_email": "m@example.test"}}


class CancelTest(unittest.TestCase):
    def setUp(self):
        outbox.MESSAGES.clear()

    def test_full_refund(self):
        status, body = api.handle_cancel(store(), 1, None, datetime(2026, 12, 1, 9))
        self.assertEqual((status, body), (200, {"status": "cancelled", "refund_cents": 24000}))
        self.assertEqual(len(outbox.MESSAGES), 1)

    def test_not_found(self):
        status, body = api.handle_cancel(store(), 2, None, datetime(2026, 12, 1, 9))
        self.assertEqual(status, 404)
        self.assertEqual(body["error"]["code"], "not_found")
'''
TEST_CANCEL_2 = TEST_CANCEL_1 + '''
    def test_late_needs_reason(self):
        status, body = api.handle_cancel(store(), 1, {}, datetime(2026, 12, 9, 12))
        self.assertEqual(status, 422)
        self.assertEqual(body["error"]["code"], "reason_required")
        self.assertEqual(outbox.MESSAGES, [])

    def test_late_half_refund(self):
        status, body = api.handle_cancel(store(), 1, {"reason": "ill"}, datetime(2026, 12, 9, 12))
        self.assertEqual((status, body), (200, {"status": "cancelled", "refund_cents": 12000}))

    def test_reason_too_long(self):
        status, body = api.handle_cancel(store(), 1, {"reason": "x" * 201}, datetime(2026, 12, 1, 9))
        self.assertEqual(status, 422)
        self.assertEqual(body["error"]["code"], "reason_too_long")

    def test_second_cancel_conflicts(self):
        bookings = store()
        api.handle_cancel(bookings, 1, None, datetime(2026, 12, 1, 9))
        status, body = api.handle_cancel(bookings, 1, None, datetime(2026, 12, 1, 9))
        self.assertEqual(status, 409)
        self.assertEqual(body["error"]["code"], "already_cancelled")
        self.assertEqual(len(outbox.MESSAGES), 1)
'''

# ---------------------------------------------------------------- history


def git(repo, *args, date=None):
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "Fixture Author",
        "GIT_AUTHOR_EMAIL": "author@example.test",
        "GIT_COMMITTER_NAME": "Fixture Author",
        "GIT_COMMITTER_EMAIL": "author@example.test",
    })
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"{date}T12:00:00+01:00"
    subprocess.run([*GIT, *args], cwd=repo, env=env, check=True,
                   stdout=subprocess.DEVNULL)


def commit(repo, date, message, files):
    for path, text in files.items():
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message, date=date)


def build(run_dir):
    repo = run_dir / "repo"
    repo.mkdir(parents=True)
    (run_dir / "out").mkdir()
    git(repo, "init", "-q")
    adrs = "architecture/decisions/"
    commit(repo, "2025-01-10", "Initial service", {
        ".gitignore": "__pycache__/\n",
        ".adr-dir": "architecture/decisions\n",
        "README.md": README,
        "CHANGELOG.md": CHANGELOG_1,
        adrs + "template.md": ADR_TEMPLATE,
        adrs + "README.md": adr_index(3),
        adrs + ADR_INDEX_ROWS[0][1]: ADR_0001,
        adrs + ADR_INDEX_ROWS[1][1]: ADR_0002,
        adrs + ADR_INDEX_ROWS[2][1]: ADR_0003,
        "hall/__init__.py": "",
        "hall/pricing.py": PRICING_1,
        "hall/bookings.py": BOOKINGS_1,
        "docs/modules/pricing.md": PRICING_DOC_1,
        "docs/modules/bookings.md": BOOKINGS_DOC,
        "tests/__init__.py": TEST_INIT,
        "tests/test_pricing.py": TEST_PRICING_1,
        "tests/test_bookings.py": TEST_BOOKINGS,
    })
    commit(repo, "2025-03-02", "Reminders with in-process timers (ADR-0004)", {
        adrs + ADR_INDEX_ROWS[3][1]: ADR_0004,
        adrs + "README.md": adr_index(4),
        "hall/reminders.py": REMINDERS_1,
        "docs/modules/reminders.md": REMINDERS_DOC_1,
        "tests/test_reminders.py": TEST_REMINDERS_1,
    })
    commit(repo, "2025-06-10", "Venue-local slot rules (ADR-0005)", {
        adrs + ADR_INDEX_ROWS[4][1]: ADR_0005,
        adrs + "README.md": adr_index(5),
        "hall/slots.py": SLOTS,
        "tests/test_slots.py": TEST_SLOTS,
    })
    commit(repo, "2025-07-01", "Studio room", {
        "hall/pricing.py": PRICING_2,
        "docs/modules/pricing.md": PRICING_DOC_2,
        "CHANGELOG.md": CHANGELOG_2,
    })
    commit(repo, "2025-07-15", "Cancellation endpoint and e-mail outbox (ADR-0006, ADR-0007)", {
        adrs + ADR_INDEX_ROWS[5][1]: ADR_0006,
        adrs + ADR_INDEX_ROWS[6][1]: ADR_0007,
        adrs + "README.md": adr_index(7),
        "hall/outbox.py": OUTBOX,
        "hall/cancellations.py": CANCEL_1,
        "hall/api.py": API_1,
        "docs/api.md": API_DOC,
        "tests/test_cancel.py": TEST_CANCEL_1,
    })
    commit(repo, "2025-08-01", "Access tokens", {
        "hall/auth.py": AUTH_1,
        "docs/modules/auth.md": AUTH_DOC_1,
        "tests/test_auth.py": TEST_AUTH_1,
    })
    git(repo, "checkout", "-q", "-b", "docs-auth")
    commit(repo, "2025-08-18", "Document 30-minute tokens", {
        "docs/modules/auth.md": AUTH_DOC_2,
    })
    git(repo, "checkout", "-q", "main")
    commit(repo, "2025-08-19", "Shorten token lifetime to 30 minutes", {
        "hall/auth.py": AUTH_2,
        "tests/test_auth.py": TEST_AUTH_2,
        "CHANGELOG.md": CHANGELOG_3,
    })
    git(repo, "merge", "-q", "--no-ff", "-m", "Merge branch 'docs-auth'", "docs-auth",
        date="2025-08-20")
    git(repo, "branch", "-q", "-D", "docs-auth")
    commit(repo, "2026-09-08", "Send reminders 2 hours ahead", {
        "hall/reminders.py": REMINDERS_2,
        "tests/test_reminders.py": TEST_REMINDERS_2,
    })
    commit(repo, "2026-09-20", "Document reminder retries", {
        "docs/modules/reminders.md": REMINDERS_DOC_2,
    })
    commit(repo, "2026-09-30", "Weekend surcharge 20%", {
        "hall/pricing.py": PRICING_3,
        "tests/test_pricing.py": TEST_PRICING_3,
    })
    commit(repo, "2026-10-02", "Release 1.4.0", {"CHANGELOG.md": CHANGELOG_4})
    commit(repo, "2026-10-14", "Rename internal booking variables", {
        "hall/bookings.py": BOOKINGS_2,
    })
    commit(repo, "2026-11-18", "Reminder sync notes; reserve ADR 0008 for rate limits", {
        "notes/2026-11-18-reminders-sync.md": NOTES,
        adrs + "README.md": adr_index(7, reserved=True),
    })
    commit(repo, "2026-11-20", "Require a reason for late cancellations", {
        "hall/cancellations.py": CANCEL_2,
        "hall/api.py": API_2,
        "tests/test_cancel.py": TEST_CANCEL_2,
    })


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    run_dir = Path(sys.argv[1])
    if run_dir.exists():
        print(f"refusing to overwrite {run_dir}", file=sys.stderr)
        return 1
    build(run_dir)
    print(f"built {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
