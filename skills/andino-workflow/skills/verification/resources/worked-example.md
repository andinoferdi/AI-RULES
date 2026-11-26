# Worked example: accepting a subagent's CSV export

A subagent reports: "Implemented CSV export for the orders page per `docs/spec-export.md` (E1-E3).
Added `tests/test_export.py`, 6 passed. Migration added. Ready for review." The parent must decide
whether to accept it. The repository is a small Flask app with pytest.

## Prerequisites

`git status` shows the subagent's work uncommitted on top of `main` at `a41c9e0`, plus the user's
own unrelated edit in `templates/base.html`. `pytest -q` on `main` before the change: 41 passed.

## Gate 1: list the claims

From the spec and the report:

1. E1: `GET /orders/export.csv` returns `text/csv` with a header row.
2. E2: fields containing commas, quotes or newlines are quoted as RFC 4180 requires.
3. E3a: only orders the user can see are exported. E3b: the export is capped at 10,000 rows.
4. Report: "6 passed". 5. Report: "migration added" (an `exported_at` column).

Done when: five claims, each with a check (the export tests, a request with a tricky field, a
row-count check, a migration run).

## Gate 2: reports are claims

`git diff a41c9e0 --stat` shows `app/export.py`, `tests/test_export.py`, and a new untracked
`migrations/0012_exported_at.py`. Reading the diff: no row cap anywhere (E3b), and the CSV writer
is built with `quoting=csv.QUOTE_NONE`. The "6 passed" covered which state? The report has no
commit; it is rerun.

## Gate 3: run and read

```text
$ pytest -q tests/test_export.py
....s.                                         5 passed, 1 skipped
SKIPPED [1] tests/test_export.py:48: needs postgres
$ pytest -q
46 passed, 1 skipped
```

The skipped test is `test_visibility_filter`: E3a is not verified by the suite. A request with a
customer named `Smith, Jones` returns `Smith, Jones` unquoted: E2 failed. The migration runs
on SQLite: `flask db upgrade` -> `Running upgrade 0011 -> 0012`.

## Gate 4: regression checks can fail

The parent adds `test_quotes_commas` (E2) and `test_row_cap` (E3b), runs them before changing any
code: both fail (`AssertionError: 'Smith, Jones' != '"Smith, Jones"'`, `10450 != 10000`). It
switches the writer to `csv.QUOTE_MINIMAL` and adds the cap; both pass. For the skipped E3a test it
starts the project's `docker compose up -d db` and runs it: passes. To check that it guards, it runs
it against `a41c9e0` in `git worktree add .scratch/old a41c9e0`, where the export does not exist:
it fails with 404, so it cannot be red for the reason it guards. Recorded as "guards by reading".

## Gate 5: re-check after the last change

```text
$ pytest -q
49 passed
$ git status --short
 M app/export.py
 M templates/base.html        (user's edit, untouched)
 M tests/test_export.py
?? migrations/0012_exported_at.py
```

`git worktree remove .scratch/old` done; no scratch files remain.

## Gate 6: decide and report

To the user: "Not ready as delivered: CSV quoting was wrong and the 10,000-row cap was missing.
I fixed both with tests that failed first. With Postgres running, all 49 tests pass. Ready for your
review; nothing is committed."

```text
Claims checked: 5, from docs/spec-export.md and the subagent's report
- E1 header and content type - passed: `pytest -q tests/test_export.py` -> test_csv_header passed
- E2 quoting - fixed: `Smith, Jones` unquoted -> QUOTE_MINIMAL -> test_quotes_commas passed
- E3a visibility - passed with Postgres: `pytest -q -k visibility` -> 1 passed (skipped without db)
- E3b row cap - fixed: 10450 rows -> cap added -> test_row_cap passed
- "6 passed" - failed as stated: 5 passed, 1 skipped on rerun
- migration - passed: `flask db upgrade` -> 0011 -> 0012
Reused results: none
Regression checks: test_quotes_commas, test_row_cap fail before the change (output above) and pass
  after; test_visibility_filter by reading (no old revision has the endpoint)
Last run after last edit: yes; git status: 3 intended changes + user's base.html untouched
Verdict: complete for review; not committed
```
