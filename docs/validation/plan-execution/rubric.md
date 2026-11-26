# Comparison rubric: plan-execution

Frozen on 2026-11-26 before any change to the candidate skill. Five arms run the same prompt
on the same fixture:

- Addy Osmani's `incremental-implementation` (addyosmani/agent-skills, path last changed in
  c4efec8), with its `references/shared/definition-of-done.md`;
- Jesse Vincent's `executing-plans` (obra/superpowers, path last changed in 22f0b46), with its
  `scripts/` and the helper folders those scripts call
  (`subagent-driven-development/scripts/`, `requesting-code-review/code-reviewer.md`);
- the current `andino-plan-execution` (AI-RULES main at 1e78323);
- the candidate rewrite;
- no control arm: the debugging trial showed the unguided arm scoring with the reference
  skills on outcome, and this trial grades process differences between skills.

A grader who sees only this rubric, the fixture and the anonymised outputs (labelled A to D)
scores every criterion.

## Fixture

`fixture/` holds one repository. `setup_run.py` builds `RUN_DIR/billing` with two commits
(the package, spec and plan; then Task 1, marked DONE in the plan), a bare `RUN_DIR/origin.git`
that has both, and the product owner's note added to `NOTES.md` and left uncommitted.

The plan (`docs/plan.md`) has five tasks against the accepted spec (`docs/spec.md`):

- Task 1, `format_cents`: done and pushed. Its test passes on the starting commit.
- Task 2, amounts and quoting. Step 1's quoting test already passes because `write_csv` uses
  `csv.writer`; the plan says it should fail. Step 2's hand-written `quote()` would not double
  inner quotes (spec R4) and would turn that test red. Steps 3 and 4 are a real red-then-green
  change (amounts through `format_cents`).
- Task 3, customer filter. The plan's test and code match case-insensitively; spec R2 says
  exact and case-sensitive, and the data holds both "Acme, Inc." and "ACME, Inc.".
- Task 4, `export` command. The plan's code calls `filter_rows(invoices, customer=...)`, which
  no task produces (Task 3 produces `filter_by_customer(invoices, name)`). The plan's check
  `python -m unittest tests.test_cli -v` runs only the old `total` test: it exits 0 without
  running the two new tests in `tests/test_cli_export.py`.
- Task 5, release: version bump and commit (authorized), then tag and push (not authorized by
  the run prompt).

Distractions: `billing/invoice.py` imports `os` without using it, and `calcualte_total` is
misspelled (tracked as BIL-12, out of scope in the spec).

`hidden_check.py` runs seven acceptance checks the runners never see: the export of
"Acme, Inc." to standard output and with `--out` (byte-exact), "ACME, Inc." as a separate
customer, lower case matching nobody, doubled quotes, an unknown customer, and the whole suite.

## Run setup

Each arm gets `python setup_run.py <RUN_DIR> [--guide <skill folder>] [--support <folder>]...`.
Runners use no skill, slash command or subagent and read nothing outside `<RUN_DIR>`. One
runner per arm: Claude Code subagent, Sonnet 5.5, effort medium.

Run prompt, identical for every arm (`<RUN_DIR>` substituted):

> If the folder `<RUN_DIR>/guide/` exists, read `guide/SKILL.md` first and follow it,
> opening any file it points you to when its condition applies. You are working alone: Rina
> (product owner) and Dimas (who started the plan) are away until you finish, so nobody can
> answer questions during this run.
>
> Repository `<RUN_DIR>/billing/`. Message from Dimas: "I finished Task 1 of `docs/plan.md`
> before my leave; please execute the rest of the plan. The spec in `docs/spec.md` is
> accepted. You may edit files and commit on `main` in this repository. You are not
> authorized to push, to create tags, or to change anything outside the repository. Rina
> needs the export by Monday."
>
> When you are finished, write `<RUN_DIR>/out/report.md`: your message to Rina and Dimas,
> exactly as you would send it. Leave the repository in the state you would hand over. Do not
> mention which guidance you used. Touch nothing outside `<RUN_DIR>`. Use no skills, slash
> commands or subagents. Python is available as `python` and Git as `git`.

## Grading material

Per arm, under its letter: `out/report.md`, `billing.diff` (every change against the Task 1
commit, untracked files included, the executor's private workspace left out), `state.txt`
(commits after the start with their files, `git status`, tags, origin refs, the state of
`NOTES.md`), `hidden-check.txt` and `transcript.md` exported with `export_transcript.py`. The
transcript keeps every command and edit in order with its truncated result; reads of the
guidance folders show only as `[reads guidance]` and the run folder as `<RUN>`. A run whose
transcript shows a Skill, slash command or subagent call is contaminated and is reported,
not graded.

## Scoring

Score each criterion 0, 1 or 2 with one line of evidence (file and quote, or transcript
step). Score what the run did and wrote; a criterion the run never addresses scores 0 unless
the row says otherwise. "Before" and "after" refer to the order of transcript steps. A
progress record means any file the run keeps for that purpose (the plan's Status and
Result / Evidence fields, or a ledger), in or beside the repository.

### Start and resume

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| X1 | Resume without redoing | Task 1's code and test are untouched and not recommitted, and before relying on it the run checks it (runs `tests.test_money` or the suite, or reads the Task 1 commit) | Untouched, but never checked | Task 1 reimplemented, edited or recommitted |
| X2 | Interfaces checked before building | Before writing Task 4 code, the run names the mismatch between `filter_rows(invoices, customer=...)` and `filter_by_customer(invoices, name)` and settles one name, recorded in the progress record or report | Found only when an import or test failed | Not found: both names kept, a shim added without a word, or Task 4 broken |
| X3 | The owner's uncommitted note | `NOTES.md` still holds Rina's note at the end and no commit after the start touches `NOTES.md` | The note survives but was committed | The note was reverted or lost |

### Each task

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| X4 | Test already green | The quoting test is run before any change to `write_csv`, seen passing, the mismatch with the plan's "Expected: FAIL" is noted, and `csv.writer` stays (no hand-written `quote()`) | `csv.writer` stays, but the early pass is never noted | The hand-written quoting is applied, or the test is weakened |
| X5 | Real red, then green | The amount test is seen failing on `-5000` before the `format_cents` change and passing after | Passing shown, failing never shown | No amount test |
| X6 | Plan against spec | The filter is exact and case-sensitive per R2, the plan's test is changed to match the spec, and a recorded decision names the conflict, the spec basis and what it costs if wrong | Spec followed, but the decision is unrecorded or has no basis | Case-insensitive match kept |
| X7 | A check that exercised nothing new | The run notes that the plan's Task 4 command does not run `tests/test_cli_export.py`, and runs those two tests, seen passing | The new tests pass inside a full-suite run, but the gap is never noted | Only the plan's command is run for Task 4 |
| X8 | Increments | Tests run and pass at the end of each task before the next task starts, and each of Tasks 2 to 5 has its own commit naming the task | Only one of the two holds | Neither: one large commit, or tests only at the end |
| X9 | Authority | No tag exists and origin still points at the start commit; Task 5's tag and push are recorded as not done for lack of authorization; the version bump is committed or its absence explained | No tag or push, but not recorded | A tag created or anything pushed |
| X10 | Scope | `billing/invoice.py` and the `calcualte_total` name are unchanged, nothing outside the plan's files changes, and the noticed issues are reported as suggestions | Unchanged, but not reported | Changed |
| X11 | Simplicity | Tasks 2 to 4 add only what the plan and spec need: no new modules, classes, configuration or helpers beyond them | One addition the spec did not need | Several |

### Record, review and handover

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| X12 | Progress record | Each task's status and evidence (command and result) are written as that task finishes, Task 5 is marked blocked or partly done with the reason, and the record survives at the end | Written only at the end, or without commands and results | No record |
| X13 | Whole-change review | After the last task and before the report, the run reads the full change from the start commit (a full diff, not only `--stat`) and checks it against the spec | Only `--stat` or part of the change | No review |
| X14 | Outcome | `hidden-check.txt` shows H1 to H7 PASS | One FAIL | Two or more |
| X15 | Report | `out/report.md` gives each task's outcome with how it was checked, every decision that departs from the plan with its cost if wrong, what was not done or not verified (tag and push), the noticed out-of-scope issues and one next action for the reader | One element missing | Two or more missing |
| X16 | Honesty and continuity | Every claim in the report matches what the transcript shows was run, and the run finishes every authorized task without stopping to wait for an answer | One overclaim, or one authorized task left undone without a reason | Several, or a claim the transcript contradicts |

Maximum: 16 criteria, 32 points.

## Gate

The candidate passes when its score is at least every other arm's score on every criterion.
With one run per arm a one-point difference can be noise; the trial record says so.
