# Worked planning examples

Synthetic scenarios. Paths, signatures and commands are scenario inputs; a real plan takes them
from the repository it inspected. Every check below is planned, not run.

## STANDARD: a booking command with a price rule and one unknown

**Scenario.** A Python 3.10 study-room CLI, `rooms/`. Inspected: `rooms/cli.py::main(argv) ->
int` with an argparse `list` subcommand; `rooms/store.py::load(path) -> list[Booking]` and
`save(path, bookings)`; `rooms/models.py::Booking(room, day, start, end)` with `datetime.date`
and `datetime.time` fields; `tests/support.py::run(args) -> (code, out, err)`. Tests use
`unittest`; the README command is `python -m unittest -v` from the repository root, 6 tests,
all passing. `rooms/timeutil.py::minutes(a, b)` returns `abs` minutes between two times.

The accepted spec, `docs/specs/booking.md`:

- **B1** `book <room> <YYYY-MM-DD> <HH:MM> <HH:MM> --member <id>` saves a booking and prints
  `Booked <room> <date> <start>-<end>: Rp <price>`.
- **B2** Price: Rp 10.000 for each started 30 minutes. A member's first 60 minutes of a day are
  free. Prices are whole rupiah.
- **B3** A booking that overlaps another in the same room is refused with
  `Room <room> is taken <start>-<end>` on stderr, exit 1, nothing saved.
- **B4** After saving, send an SMS through the campus gateway. The gateway's reply format is
  not documented yet; IT will send an example.
- Constraints: standard library only; existing booking files must still load.

Gate 1 finds the trap: `minutes()` is absolute, so an end before the start would look like a
valid booking. Gate 2 records two gaps (end before start; what "first 60 minutes" means when a
day's earlier booking was 45 minutes) and turns B4 into D1.

````markdown
# Room booking implementation plan

Status: TODO
Plan Depth: STANDARD
Spec: docs/specs/booking.md
Last Updated: 2026-11-26

## Executive Snapshot
T1-T3 (B1-B3) are READY; start with T1. B4 waits on D1: IT's example gateway reply.

## Goal
Members book study rooms from the CLI, see the price, and cannot double-book a room.

## Global Constraints
- Standard library only.
- Existing booking files must still load.
- Prices are whole rupiah (`int`).

## Decisions the spec leaves open
- End time not after start time: refused with `End must be after start`, exit 2 (same code as
  argparse errors).
- "First 60 minutes free" counts the member's minutes already booked that day: 45 earlier
  minutes leave 15 free minutes.
- Started 30 minutes are counted on the paid minutes after the free ones.

## Review Focus
1. End equal to start: refused (decision 1). Test in T1.
2. A booking that ends exactly when another starts: not an overlap. Test in T3.
3. A member's second booking on the same day: free minutes already used. Test in T2.
4. Exactly 30 paid minutes: Rp 10.000, not 20.000. Test in T2.
5. A booking file written before this change: still loads. Test in T1.

## File map
- `rooms/pricing.py` (create): the price rule only.
- `rooms/cli.py` (modify): `book` subcommand and its checks.
- `tests/test_pricing.py` (create), `tests/test_cli.py` (modify).

## Execution Board
| Task | Status | Readiness | Depends on | Files |
| --- | --- | --- | --- | --- |
| T1 book saves a booking | TODO | READY | none | cli.py, test_cli.py |
| T2 price rule | TODO | READY | none | pricing.py, test_pricing.py |
| T3 overlap refusal and price in output | TODO | READY | T1, T2 | cli.py, test_cli.py |
| D1 gateway reply format | BLOCKED | - | IT's example | none |
| T4 SMS after save | TODO | WAITING_ON D1 | T3, D1 | cli.py, sms.py |

## Coverage
| Requirement | Task | Check |
| --- | --- | --- |
| B1 | T1, T3 | `test_book_saves`, `test_book_prints_price` |
| B2 | T2 | `test_price_*` |
| B3 | T3 | `test_overlap_refused_nothing_saved` |
| B4 | D1, T4 | blocked |

## Tasks

### T2 - Price rule (B2)
Status: TODO
Readiness: READY
Requirements: B2
Depends on: none
Files: Create `rooms/pricing.py`; Test `tests/test_pricing.py`
Interfaces:
- Produces: `price(minutes: int, free_left: int) -> int` in `rooms/pricing.py`.
Acceptance: the spec rule in integers; values below.

Change Specification:
- `rooms/pricing.py` (proposed): `price` charges each started 30 minutes of
  `max(0, minutes - free_left)` at 10000. Started blocks in integers: `-(-paid // 30)`. No float.

Steps:
- [ ] 1. Write `tests/test_pricing.py`:

```python
class PriceTest(unittest.TestCase):
    def test_price_counts_started_half_hours(self):
        self.assertEqual(price(30, 0), 10000)
        self.assertEqual(price(31, 0), 20000)
        self.assertEqual(price(90, 0), 30000)

    def test_price_member_free_minutes(self):
        self.assertEqual(price(60, 60), 0)
        self.assertEqual(price(90, 60), 10000)
        self.assertEqual(price(90, 15), 30000)   # 75 paid minutes -> 3 started blocks
```

- [ ] 2. Create `rooms/pricing.py` with `def price(minutes: int, free_left: int) -> int:
      return 0`. RED: `python -m unittest tests.test_pricing -v` from the repository root;
      expect `AssertionError: 0 != 10000` in `test_price_counts_started_half_hours`.
- [ ] 3. Implement `price` per the Change Specification.
- [ ] 4. GREEN: same command, 2 tests OK; then `python -m unittest -v`, 8 tests OK.

Result / Evidence: Not run - planned checks only.

### T3 - Overlap refusal and price in output (B1, B3)
Status: TODO
Readiness: READY
Requirements: B1, B3
Depends on: T1, T2
Files: Modify `rooms/cli.py` (`_cmd_book`); Test `tests/test_cli.py`
Interfaces:
- Consumes: `price(minutes, free_left)` (T2); `_cmd_book` (T1).
Acceptance: overlap refused with the exact message and nothing saved; success prints the price.

Change Specification:
- `rooms/cli.py::_cmd_book`, order of checks: end after start (decision 1, exit 2); overlap in
  the same room and day, where `new.start < old.end and old.start < new.end` (touching is not an
  overlap), print `Room <room> is taken <old.start>-<old.end>` to stderr and return 1 before
  `save`; then price with `free_left = max(0, 60 - minutes already booked by the member that
  day)`; save; print `Booked <room> <date> <start>-<end>: Rp <price with dots>`.
- Do not use `timeutil.minutes` for durations: it is absolute. Use
  `(end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)`.

Steps:
- [ ] 1. Add to `tests/test_cli.py`, using `support.run` and a temporary booking file:

```python
def test_overlap_refused_nothing_saved(self):
    self.write_bookings([("R1", "2026-12-01", "09:00", "10:00", "M7")])
    code, out, err = run(["book", "R1", "2026-12-01", "09:30", "10:30", "--member", "M8"])
    self.assertEqual((code, err.strip()), (1, "Room R1 is taken 09:00-10:00"))
    self.assertEqual(len(self.read_bookings()), 1)

def test_touching_is_not_overlap(self):
    self.write_bookings([("R1", "2026-12-01", "09:00", "10:00", "M7")])
    code, out, err = run(["book", "R1", "2026-12-01", "10:00", "10:30", "--member", "M8"])
    self.assertEqual(code, 0)

def test_book_prints_price(self):
    code, out, err = run(["book", "R1", "2026-12-01", "09:00", "10:30", "--member", "M8"])
    self.assertEqual(out.strip(), "Booked R1 2026-12-01 09:00-10:30: Rp 10.000")
```

- [ ] 2. RED: `python -m unittest tests.test_cli -v`; expect
      `AssertionError: Tuples differ: (0, '') != (1, 'Room R1 is taken 09:00-10:00')` and
      `'Booked R1 2026-12-01 09:00-10:30' != 'Booked R1 2026-12-01 09:00-10:30: Rp 10.000'`.
- [ ] 3. Change `_cmd_book` per the Change Specification.
- [ ] 4. GREEN: same command OK; full suite OK. Then run
      `python -m rooms.cli book R1 2026-12-01 09:00 10:30 --member M8 --data <temp copy>` and
      expect `Booked R1 2026-12-01 09:00-10:30: Rp 10.000`.

Result / Evidence: Not run - planned checks only.

## Blocked and discovery items

### D1 - Gateway reply format (B4)
Missing: what the campus SMS gateway returns on success and on failure. Provider: IT (example
reply promised in the spec). Questions: success shape and status field; failure codes; timeout
behaviour. Without it: T1-T3 ship; bookings save and print as today. Seam: `_cmd_book` calls one
function `notify(booking) -> None` after `save`, added in T4. Exit check: the example reply is
in the repository and T4's Change Specification names the success field and failure handling.

## Risks
| Risk | Effect | Covered by |
| --- | --- | --- |
| Absolute `minutes()` reused for durations | Reversed times accepted | T1 decision 1, T3 note |
| Float price arithmetic | Off-by-one blocks | T2 integer rule and tests |

## NEXT ACTION
T1: write `test_book_saves` in `tests/test_cli.py` and run it red.
````

T1 is left out above for length; it follows the same template. Notice what the plan does not
contain: no body for `_cmd_book`, no argparse code, no imports. The tests, the overlap
condition, the order of checks and the integer price rule are the decisions; the rest is the
developer's.

The reply to the requester:

```text
Plan: docs/exec-plans/active/room-booking.md
Ready to build: T1, T2, T3 (booking, price, overlap), in that order.
Blocked on IT: the SMS gateway's example reply (success and failure). SMS (B4) waits for it;
  everything else ships without it.
Decisions to confirm: end time must be after start (else refused); free 60 minutes count across
  the member's bookings that day; started 30 minutes count after the free ones.
Not done: nothing is built or tested yet.
```

## LITE: one file, one rule

Request: "Reject booking dates in the past." One file, one check.

````markdown
# Reject past booking dates
Status: TODO | Plan Depth: LITE | Spec: user request 2026-11-26
Goal: `book` refuses a date before today with `Date <date> is in the past`, exit 2.
Decision: today is allowed; "today" is the machine's local date.

### T1 - Refuse past dates
Readiness: READY | Files: Modify `rooms/cli.py` (`_cmd_book`, first check); Test `tests/test_cli.py`
Test: `run(["book", "R1", "2000-01-01", "09:00", "10:00", "--member", "M8"])` gives
`(2, "", "Date 2000-01-01 is in the past\n")`; a booking for today is accepted.
RED: `python -m unittest tests.test_cli -v` fails on the exit code (0 != 2).
Change: compare `day < date.today()` before the overlap check.
GREEN: same command OK; full suite OK.
NEXT ACTION: write the test and run it red.
````

## Anti-pattern: the plan that writes the code

A plan for the booking spec whose T3 holds the whole `_cmd_book` function (forty lines of
argparse wiring, file loading, loops and prints) and whose T2 holds the full `pricing.py`. It
is three times longer than the code it describes. The overlap rule and the integer rounding are
buried in the body, so a reviewer cannot see what was decided, and the first review comment
makes the pasted body stale.

Fix: replace each body with the signature, the tests as code and the lines that decide
something (the overlap condition, `-(-paid // 30)`, the order of checks and their messages).
Then run the step scan: each step should still yield exactly one reasonable thing.
