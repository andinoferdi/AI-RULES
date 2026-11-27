# Postmortem: ledger_entries locked for 11 minutes

Date: 2026-11-12, 19:04-19:15 WIB. Severity 2.

## What happened

PR #812 added migration `0042_entry_reference_unique`, which builds a unique index on
`ledger_entries.reference` with plain `CREATE UNIQUE INDEX` instead of `CONCURRENTLY`. The table
holds 48 million rows. The index build took an ACCESS EXCLUSIVE lock for 11 minutes; every
payment posting in that window timed out and 2,310 customer payments had to be replayed.

## Why it was not caught

The PR was opened and merged by a coding agent. `make migrate-check` was not run. Run against
the snapshot afterwards, it fails with:

    0042_entry_reference_unique: CREATE UNIQUE INDEX ... ACCESS EXCLUSIVE on ledger_entries
    (48,112,904 rows) -- above LOCK_ROW_LIMIT

We found two earlier migration PRs from agents (#771 and #798) where the check was also
skipped. Both were harmless by luck. Excerpts from the three sessions are in this folder.

## Actions

1. Run `make migrate-check` in CI. Blocked: CI has no route to the snapshot. Infra estimates
   Q3 next year.
2. Until then, agents must run `make migrate-check` themselves before they open, approve or
   merge a PR that adds or edits a file under `migrations/`, and paste its output in the PR.
3. Humans: same rule, already in the onboarding doc.
