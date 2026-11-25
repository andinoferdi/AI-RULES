# Worked example: reminder scheduler

One compact Stabilize run, for orientation. The scenario is synthetic; its paths,
counts and results illustrate the method and are not evidence about any real project.

## Request and eligibility

"Users get the same reminder twice on the night clocks change, and some reminders never
arrive although the dashboard says sent. Several quick patches did not hold. Fix it; you
may edit and commit on this branch."

Eligible: repeated regressions in a bounded subsystem (`reminders/`) after patch-on-patch
fixes, with two user-visible symptoms. Edits are authorized, so the mode is Stabilize.
Baseline: `python -m unittest discover -s tests` -> 9 tests OK at `a41c0de`. Test trust is
low: no test runs a DST date, and `test_send_never_raises` asserts that a provider error
still ends with status `sent`.

## Where to start

```sh
git log --since=12.months --format=format: --name-only -- reminders | grep -v '^$' | sort | uniq -c | sort -rg | head
```

| Rank | Area | Symptom / contract | Churn | Size / branches | Consumers | Test trust | First action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | reminders/schedule.py | Duplicate on DST night; README: one reminder per day at local 09:00 | 7 (5 fix) | 140 lines, 11 branches | sender, display, admin API | none on DST | Pin next_send_time across a DST date |
| 2 | reminders/sender.py | "Sent" without delivery | 6 (3 fix) | 90 lines | worker, dashboard | test enshrines the bug | Pin send with a failing provider |
| 3 | reminders/display.py | Displayed time differs from actual send on DST days | 4 | 40 lines | settings page | none | Diff against schedule.py |
| - | reminders/templates.py | none | 2 | 60 lines | sender | 6 meaningful tests | KEEP |

AI-signal sweep on these files: display.py holds a second copy of the time conversion
(fixed UTC offset instead of the zone database); sender.py catches every exception and
marks the job done; provider_client.py calls `client.send_batch`, which the lockfile's
SDK version 2.3 does not provide (only `send`), on the branch for more than 50 jobs.

## Findings

| ID | Finding | Severity | Confidence | Disposition |
| --- | --- | --- | --- | --- |
| RSC-001 | Next run is computed as last run + 24 h in UTC, so local 09:00 shifts on the DST night and the catch-up rule sends again; display uses a divergent fixed-offset copy | HIGH | HIGH (reproduced for Europe/Berlin 2026-03-29) | REFACTOR: one owner for local send time |
| RSC-002 | sender marks the job done before the provider confirms; provider errors are logged and swallowed | HIGH | HIGH (failing fake provider) | REFACTOR: done only after confirmation |
| RSC-003 | `send_batch` does not exist in the installed SDK; batches over 50 raise AttributeError | MEDIUM | HIGH (resolved against installed package) | REFACTOR: loop over `send`; SDK upgrade is an owner decision |
| RSC-004 | templates.py | - | HIGH | KEEP |

## Pins before any change

Fourteen characterization tests at two pinch points (`next_send_time` and
`process_due_jobs`), with the clock injected through the existing `now` parameter of
`process_due_jobs` and a patched clock for `next_send_time`. Two pins record known bugs:

```python
def test_dst_night_sends_twice(self):
    # KNOWN BUG RSC-001: two sends on 2026-03-29 in Europe/Berlin. Flip in the fix step.
    self.assertEqual(len(run_day("2026-03-29", tz="Europe/Berlin")), 2)

def test_provider_error_marks_job_done(self):
    # KNOWN BUG RSC-002: job is done although nothing was delivered. Flip in the fix step.
    job = process_due_jobs(now=T0, provider=FailingProvider())[0]
    self.assertEqual(job.status, "done")
```

All 14 pins pass on the unmodified code. The old `test_send_never_raises` stays until
the RSC-002 step replaces it.

## Steps

| Step | Concern | Kind | Files | Check and result |
| --- | --- | --- | --- | --- |
| 1 | Pin current behavior | tests only | tests/test_char_reminders.py | 23 tests pass on unmodified code |
| 2 | Route display through schedule.local_send_time | structure (attempted) | display.py, schedule.py | 3 display DST pins red: routing changes displayed output, so it is a behavior change. Reverted |
| 2b | Extract local_send_time inside schedule.py only | structure | schedule.py | 23 pass |
| 3 | Compute next run in local time with the zone database | behavior | schedule.py, char test | RSC-001 pin flipped to 1 send; 23 pass |
| 4 | Display uses local_send_time; delete the copy after a consumer check (only display.py imported it) | behavior | display.py, char test | 3 display pins flipped; 23 pass |
| 5 | Mark done only after provider confirmation; failures become `failed` with the error | behavior | sender.py, tests | RSC-002 pin flipped; old test replaced with the contract reason; 24 pass |
| 6 | Replace send_batch with a loop over send | behavior | provider_client.py, tests | autospec fake without send_batch; 25 pass |

Each kept step was one commit with only its files staged.

## Final report (abridged)

Outcome: one reminder per local day across DST for the tested zones; failed deliveries
now show as failed. Reminders already marked done without delivery are not repaired.

Downstream impact: the dashboard and the admin API read job status; `failed` is a new
value for both (the dashboard shows it as "unknown" today). Jobs marked done without a
provider message id since the sender patch of 2026-08-14 need reconciliation:
`SELECT id FROM jobs WHERE status = 'done' AND provider_message_id IS NULL AND done_at >= '2026-08-14'`.

| Check | Command or procedure | Result |
| --- | --- | --- |
| Full suite | python -m unittest discover -s tests | PASS (25 tests) |
| Zones other than Europe/Berlin and America/New_York | not run | UNVERIFIED |
| Real provider | sandbox not available | UNVERIFIED |

Decisions for the owner: re-send or notify for the unreconciled jobs; add `failed` to the
dashboard legend; upgrade the SDK for batch sending or keep the loop.

Next action: run the reconciliation query read-only and share the count with the owner.
