# Worked documentation examples

These fixtures illustrate how source evidence becomes reader-facing text.
Use the repository's names, format and checks on real tasks.

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
