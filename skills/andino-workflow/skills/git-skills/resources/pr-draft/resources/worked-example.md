# Worked example: a PR body with a one-way door

Scenario: a search service replaces its nightly full reindex with incremental updates and deletes
the old `search_snapshots` storage bucket in a cleanup job. The repository has no PR template, so
the default sections are used. Ticket SRCH-311. A teammate pushed a commit to the branch noting
that analytics still reads last month's snapshot.

## Default template (when the repository has none)

```markdown
## Summary

<one sentence on why> <one view: pseudocode, call tree, component tree, file tree, Mermaid or shaped diff>

## Evidence

- **Before:** <command and observed output on the base, or "not observed" and why>
  **After:** <command and observed output on this branch>

## Merge danger

**Door:** <one-way or two-way>: <each effect a revert does not undo>
**Blast radius:** <who or what, with counts from the repository>
**Rollback:** <the protecting step first, then how to restore>
```

## The body

````markdown
> **Blocker:** analytics still reads the October snapshot (note from Dimas on this branch,
> 2026-11-24). Copy `search_snapshots/2026-10/` to the analytics bucket before running the
> cleanup job.

## Summary

SRCH-311. The nightly full reindex took 3 hours and blocked writes; updates now go to the index
as documents change, and the snapshot bucket that only the full reindex used is deleted.

```diff
 on(document_saved)
-  mark_dirty(document)
+  index.upsert(document)
 nightly()
-  rebuild_full_index()
-  write_snapshot(search_snapshots)
+  cleanup_job: delete_bucket(search_snapshots)
```

## Evidence

- **Before:** `pytest tests/test_indexing.py -k saved` on the base (temporary worktree at
  `a41c9e2`, new tests copied in): `test_saved_document_is_searchable` FAILED, document not found.
  **After:** same command on this branch: 6 passed.
- Full suite: `pytest` -> 214 passed. Load test of the incremental path: not run here.

## Merge danger

**Door:** one-way. The cleanup job deletes `search_snapshots`; reverting the code does not bring
the 41 monthly snapshots back.
**Blast radius:** the analytics export (the only other reader, `analytics/export.py`) and any
restore that relied on a snapshot.
**Rollback:** before the cleanup job runs, copy the bucket (`gsutil -m cp -r ...`); code rollback
is `git revert <merge>` plus re-enabling `nightly()` until a full index is rebuilt.
````

## Why it is written this way

- The blocker from a commit the author did not write is at the top.
- One shaped diff shows the change in the call shape reviewers know.
- The before run happened on the base with the new test; the load test is labelled not run.
- The door names the effect a revert cannot undo, with the count, and the rollback protects the
  data first.
