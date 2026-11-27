# Worked documentation examples

These fixtures illustrate how source evidence becomes reader-facing text.
Use the repository's names, format and checks on real tasks. The first three
cover steps 2-5 and 10, the last two cover steps 6-8.

## Proposed replacement for a storage decision

The decisions index and `.adr-dir` both point to `Documentation/Decisions`.
The newest record is `ADR-004-Store.rst`. It is accepted and describes a local
spool. A controlled test measured 50 requests per minute with one worker.
The two-worker recovery test reproduced duplicate delivery after a crash.
The project sets a 200 ms claim latency budget for its two-worker load test.
The team has requested a proposal and has yet to approve it.

Draft `ADR-005-Queue.rst` using the repository headings.

```rst
ADR-005 Queue
=============

Status: Proposed
Date: 2026-11-03

Context
-------
The local spool delivered duplicates after a worker crash in the two-worker
recovery test. The single-worker test measured 50 requests/minute on the
fixture workload. That measurement establishes one operating point.

Decision
--------
Use the shared database as the job queue, with a unique job key and a
transactional claim. This would replace the local spool in ADR-004-Store.rst.

Alternatives
------------
The local spool has no additional service dependency but failed the recovery
test. A managed broker provides shared delivery but still requires consumer
deduplication and adds a service to operate.

Consequences
------------
The database would own claim and deduplication state. Workers would need a
retention policy for completed jobs. Revisit the choice if claim latency
exceeds the existing 200 ms budget in the two-worker load test.
```

Use the latency figure only if the project establishes it. Confirm the number
and reference resolve, leave ADR-004 accepted while the proposal is open, and
preserve both records once the decision is approved. The new ADR documents a
proposed design. Queue performance still needs a test of that design.

## Public API conflict response

The existing API contract test sends a duplicate reservation to
`POST /reservations` and asserts a 409 with error code `slot_taken`. The
handler returns before the insert. Update the endpoint's response table:

| Outcome | Contract | Caller action |
| --- | --- | --- |
| 409 `slot_taken` | The requested slot is already reserved. No reservation was created by this request. | Refresh availability and select a different slot before retrying. |

Update the existing schema and link to the endpoint from the release note
if the change shipped. Run the contract test to verify the status and
response body. Check the handler for the side-effect claim and record whether
the test also asserts it. Label an HTTP example as source-checked if it was
written from the contract without sending a request.

## Quickstart correction

The README currently says `npm ci` followed by `npm run start`. The package
declares `dev` and the existing quickstart requires Node 22 plus a populated
`.env`. Update the
command in place and keep those prerequisites:

> With Node 22 and your `.env` in place, run `npm ci` and then `npm run dev`
> from the repository root.

Verify the script from `package.json` and run the quickstart where dependencies
and configuration are available. If configuration is missing, record that the
script name was checked against source and startup remains unchecked.

## Drift audit across three export documents

The user asks which documents under `docs/exports/` still match the code. Each
document names its code file. The history commands from the drift audit resource
and a claim-by-claim read give:

| Document | History verdict | Content verdict | Action |
| --- | --- | --- | --- |
| `formats.md` | code changed after the document (`7c41e2a`) | wrong: "CSV only" vs `FORMATS = ("csv", "xlsx")` in `exports/formats.py:3` | fix, log |
| `limits.md` | code changed after the document (`9d0b113`, renamed a helper) | accurate: 10,000 rows matches `MAX_ROWS = 10_000` | none |
| `schedule.md` | can't tell (both commits on branches joined by merge `e52f0aa`) | accurate: nightly at 02:00 matches the cron entry in `exports/jobs.py:12` | none |

`limits.md` shows why history alone misleads: the code moved, the claim did not.
`schedule.md` is reported as "can't tell" with the content check that settled it,
not as current. The fix to `formats.md` changes the one wrong sentence and appends
to its change log, after the existing entries:

```markdown
- 2026-11-26: Formats corrected to CSV and XLSX; `FORMATS` gained "xlsx" in 7c41e2a.
```

The report lists all three rows, the commands run and the lines read.

## Comment cleanup in a rate limiter

Before:

```python
def allow(client, now):
    # be careful here
    window = WINDOWS[client]
    # check the window
    if now - window.start > WINDOW_SECONDS:
        window.start, window.count = now, 0
    # TODO: make this better
    # if window.count > LIMIT: log.warning("limited")
    window.count += 1  # TODO(#311): per-plan limits
    return window.count <= LIMIT
```

`docs/decisions/0009-fixed-window-limits.md` explains the real hazard: the window
starts at a client's first request, so a client can spend the full limit just
before and just after a reset. After:

```python
def allow(client, now):
    # Fixed window from the client's first request (ADR-0009): a client can use the
    # full LIMIT just before and just after a reset, so bursts reach 2 x LIMIT.
    window = WINDOWS[client]
    if now - window.start > WINDOW_SECONDS:
        window.start, window.count = now, 0
    window.count += 1  # TODO(#311): per-plan limits
    return window.count <= LIMIT
```

The vague warning became the hazard from ADR-0009, with its link. The restating
comment and the commented-out logging are gone. `TODO(#311)` stays with its issue.
"make this better" names no work, so it is removed and the report lists it as a
follow-up question for the owner. The diff touches comment lines only and the tests
pass, which is the behaviour check.
