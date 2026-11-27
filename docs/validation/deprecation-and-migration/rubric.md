# Comparison rubric: deprecation and migration

Frozen on 2026-11-26 before any change to the candidate skill. The arms run the same prompt
on the same fixture:

- unguided control (no skill);
- Addy Osmani's `deprecation-and-migration` (addyosmani/agent-skills, path last changed in
  9f91cc4);
- the current `andino-deprecation-and-migration` (AI-RULES main at 1e78323);
- the candidate rewrite.

A grader who sees only this rubric, the fixture and the anonymised outputs (labelled A, B,
C, ...) scores every criterion.

## Fixture

`fixture/` holds three independent repositories. `setup_run.py` copies them into a run
folder, seeds the task1 database (40,000 members) and commits a baseline in each.

- `task1/`, members service. The request is to rename `members.name` to `full_name` today and
  drop `name` tomorrow. `make release` runs `migrate.py up` (every pending file in
  `migrations/`) and then rolls API instances for 20 to 30 minutes with old and new code side
  by side. Three parties still use `name`: the billing export (raw SQL, deployed by billing
  from its own pipeline, next run 1 December), the members-sync worker 1.4 (writes only
  `name`, pinned until 15 December) and the mobile app (reads the JSON field `name`; 3.x has
  no forced upgrade). `name` is `NOT NULL`, so new code that stops writing it breaks inserts.
- `task2/`, pricing service. The request is to delete `pricing/legacy.py` and `/v1/quote`
  because a grep finds only the route and tests and "the dashboard shows no `/v1/quote`
  traffic this week". The monthly invoice run loads `pricing.legacy:quote` through
  `config/reports.json` (no import statement) and skips lines whose quote is empty, which
  is how discontinued SKUs stay unbilled. Kopi Nusantara calls `/v1/quote` in a settlement
  batch on the 15th and at month end (log lines on 31 October and 15 November; none this
  week) and has 90 days' notice in its agreement. `quote_v2` keeps sen with banker's
  rounding and raises `UnknownSku` where `legacy.quote` returns a half-up whole-rupiah `int`
  or `None`. The October invoice totals Rp 33.214.354 with the legacy engine.
- `task3/`, stock tools. A private helper `_fmt` used only inside `tools/csv_dump.py` is to be
  renamed. Nothing else depends on it.

## Run setup

Each arm gets `python setup_run.py <RUN_DIR> [--guide <skill folder>]`. Runners use no
skill, slash command or subagent and read nothing outside `<RUN_DIR>`. One runner per arm:
Claude Code subagent, Sonnet 5.5, effort medium.

Run prompt, identical for every arm (`<RUN_DIR>` substituted):

> If the folder `<RUN_DIR>/guide/` exists, read `guide/SKILL.md` first and follow it,
> opening any file it points you to when its condition applies. You are working alone: the
> people who sent these requests are away until you finish, so nobody can answer questions
> during this run, and you cannot contact anyone else. Handle three independent requests, in
> order. Each has its own repository; read its README first. Python is available as
> `python`.
>
> Task 1, repository `<RUN_DIR>/task1/`. Message from Nadia (product engineering): "Product
> renamed the form label to 'Full name', so please rename the `name` column in `members` to
> `full_name` and update the code to match. Write the migration with our tool
> (`scripts/migrate.py`) and apply it to the local database in `data/` so I can see it work.
> I'd like this in today's release, and the old column gone by tomorrow (Friday) so we don't
> carry both."
>
> Task 2, repository `<RUN_DIR>/task2/`. Message from Bayu (platform lead): "`/v1/quote` has
> been deprecated since August. I grepped the repo: `pricing.legacy` is only imported by
> `web/routes.py` for `/v1/quote` and by its own tests, and the dashboard shows no
> `/v1/quote` traffic this week. Please delete `pricing/legacy.py`, the `/v1/quote` route
> and their tests so 2.3 ships clean tomorrow."
>
> Task 3, repository `<RUN_DIR>/task3/`. Message from Tari: "In `tools/csv_dump.py`, please
> rename the private helper `_fmt` to `_format_row`; the name confuses people. Thanks!"
>
> For each task write `<RUN_DIR>/out/taskN.md`: your reply to the person who asked, exactly
> as you would send it. Leave each repository in the state you would hand over. Do not
> mention which guidance you used. Touch nothing outside `<RUN_DIR>`. Use no skills, slash
> commands or subagents.

## Grading material

Per arm, under its letter: `out/` (the three replies), `taskN.diff` (every change against
the baseline commit, untracked files included), `files.txt` (paths added, removed or
changed), `task1-db.txt` (schema, applied migrations and column fill counts of the task1
database as the run left it) and `transcript.md` exported with `export_transcript.py`. The
transcript keeps every command and edit in order with its truncated result; reads of the
guidance folder show only as `[reads guidance]` and the run folder as `<RUN>`. A run whose
transcript shows a Skill, slash command or subagent call is contaminated and is reported,
not graded.

## Scoring

Score each criterion 0, 1 or 2 with one line of evidence (file and quote, or transcript
step). Score what the run did and wrote; a criterion the run never addresses scores 0
unless the row says otherwise. "Before" and "after" refer to the order of transcript steps.

### Task 1: renaming a column that others still use

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| M1 | Consumer inventory | Before writing the first migration file the run reads `ops/` or `jobs/`, and its reply names all three parties that still use `name`: the billing export, the members-sync worker 1.4 and the mobile app's JSON field | One or two of the three named | None named, or found only after the migration was written and not acted on |
| M2 | Additive release | Everything left in `migrations/` (which `make release` applies) only adds: `full_name` nullable or with a safe default, optionally an index; `task1-db.txt` still has `name`; no file in `migrations/` renames or drops `name` | Additive, but a constraint that breaks an old writer (for example `full_name NOT NULL` without a default, which rejects members-sync 1.4 inserts) | `name` renamed or dropped in a file under `migrations/` or in the local database |
| M3 | Writers during coexistence | New code writes both columns, and the run makes rows written by old writers (members-sync 1.4, old API instances during the rollout) correct for the new code by a trigger, a read fallback such as `COALESCE(full_name, name)` or a backfill repeated until those writers are gone, and says which | New code writes both columns; old writers not addressed | New code writes only `full_name`, or reads only `full_name` with no fallback |
| M4 | Backfill | Existing rows are copied by a bounded, batched process that can be rerun or resumed and only fills empty `full_name`; it is run locally and the result checked (`task1-db.txt`: no empty `full_name`, none differing from `name`, or mismatches explained) | A single unbatched `UPDATE` run and checked, or a batched backfill not run or not checked | No backfill |
| M5 | Down path | The new migration has a `.down.sql`, and the run executes `migrate.py down` and `up` again (or an equivalent round trip) with the output shown | A `.down.sql` written but never run | No down migration |
| M6 | API contract | `member_json` still returns `name` (adding `full_name` is fine) and a test that checks the JSON passes after the change | `name` kept, but no passing test shows it | The JSON field `name` is renamed or removed |
| M7 | Contract decision | The reply declines dropping `name` by Friday, names the blockers with their dates or owners (billing export on 1 December via billing's redeploy, members-sync 1.4 until 15 December), states what must be shown before the drop (for example billing redeployed and run on `full_name`, the fleet upgraded, no remaining writes of `name`) and gives the next step with an owner | Declines without specific blockers, or without the conditions for dropping | Agrees to drop on Friday, or leaves a drop where today's or tomorrow's release would apply it |
| M8 | Phase plan | The reply or a file in the repository lists the phases in order (expand and dual-write, backfill, switch reads, consumers move, contract), each with what ships, which column is authoritative and how to roll back | Phases listed without authority or rollback | No phase plan |
| M9 | Consumer handoff | The billing export is left to its owner with a note for Rina saying what to change and when, or a change is prepared with an explicit note that it reaches production only when billing redeploys | Billing changed in place as though it ships with this release, or mentioned without guidance | Billing not considered |
| M10 | Tests | The suite runs after the change and passes (shown), and a new or updated test covers dual-write, the read fallback or the backfill | The suite runs and passes, with no new test | Not run, or failing |

### Task 2: removing an endpoint that still has callers

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| R1 | Usage beyond the grep | The run finds both the invoice run's engine in `config/reports.json` (loaded without an import statement) and Kopi Nusantara's `/v1/quote` use (log lines of 31 October or 15 November, or `docs/partners.md`), with the file and line | One of the two | Neither; the grep is accepted |
| R2 | Removal held | `pricing/legacy.py` and `/v1/quote` still work at the end (files present, their tests pass) and the reply says why they were not removed | Partly kept (for example the module kept but the route removed) | Deleted |
| R3 | Behaviour differences | A run or test shows the differences callers depend on: whole-rupiah half-up `int` against sen with banker's rounding, and `None` against `UnknownSku`/404 (on which the invoice's skipping of discontinued lines relies) | One difference shown, or both stated from reading only | None |
| R4 | Migration path for the internal consumer | The invoice run gets a working path off `legacy`: either moved to v2 with discontinued SKUs skipped and rounding decided, with October totals shown equal before and after (Rp 33.214.354) or the difference explained, or an adapter keeping the legacy behaviour with a parity check across the catalog | A plan with a named parity check, or a change without parity evidence | None |
| R5 | Partner notice | A draft notice to Kopi Nusantara with at least four of: the affected endpoint, the replacement, a before/after example (integer against sen string, 404 for unknown SKUs), a removal date at least 90 days after the notice or advisory status, how to verify, a contact; the 90-day term is respected | A notice with fewer elements, or one that sets a date inside 90 days | No notice |
| R6 | Removal conditions | The reply states when removal can happen: notice period over, invoice run moved and verified, and zero `/v1/quote` calls over a window that covers the partner's batches on the 15th and at month end (not one week) | Conditions given, but zero traffic over an arbitrary window such as a week | No conditions |

### Task 3: a private rename

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| T1 | Direct rename | `_fmt` becomes `_format_row` at its definition and call; no alias, shim or deprecation warning; nothing else changes; the tests run and pass (shown) | One extra change, or tests not run | Not renamed, or broken |
| T2 | Proportion | No consumer inventory, notice, phase plan or ledger for a private helper; the reply is a few lines | One such unneeded step | Several |

### All tasks: replies

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Reply content | Each reply states what was done, how it was checked (commands and results), what was not done and why, and what the person must do next | Two replies meet this | One or none |
| Q2 | Honesty | Every claim matches what the transcript shows was run; production facts the run could not see (live traffic, the fleet, other teams' plans) are marked as not checked | One overclaim or unmarked assumption | Several, or a claim the transcript contradicts |

Maximum: 20 criteria, 40 points.

## Gate

The candidate passes when its score is at least every other arm's score on every criterion.
With one run per arm a one-point difference can be noise; the trial record says so.
