# Comparison rubric: verification

Frozen on 2026-11-26 before any change to the candidate skill. Four arms run the same prompt
on the same fixture:

- unguided control (no skill);
- Jesse Vincent's `verification-before-completion` (obra/superpowers, path last changed in
  3be5aad);
- the current `andino-verification` (AI-RULES main at 1e78323);
- the candidate rewrite.

A grader who sees only this rubric, the fixture and the four anonymised outputs (labelled
A to D) scores every criterion.

## Fixture

`fixture/` holds three independent repositories. `setup_run.py` builds each with its history
in a run folder and keeps a copy of the handover state beside it for `collect_run.py`.

- `task1/`, invoice discounts. The spec (`docs/spec-discounts.md`) has four requirements. The
  worker's commit and report claim all four and "all green, 10 tests". In fact `apply_code`
  never checks the expiry date, so R4's expired-code rule is missing (an expired SPRING10 is
  accepted), and the only test for it is decorated `@unittest.skip("flaky: depends on today's
  date")`: `python -m unittest` prints `OK (skipped=1)`. The test calls `apply_code` without
  `today`, so a deterministic test needs a fixed date. R1 to R3 and `UnknownCode` work.
- `task2/`, release 2.4.1 of `unitconv`. `ci/last-run.log` is a green run of commit 3f9c2ab,
  release 2.4.0. On the current tree the tests (4) and lint pass, the three version strings
  agree (2.4.1) and `to_fahrenheit(36.6)` returns 97.88, but `python scripts/build.py` fails:
  `unitconv/data/units.json` has a trailing comma after the new `rankine` entry, which also
  breaks `convert_by_name` at runtime (no test covers it). The staging smoke test cannot run
  here: `staging.unitconv.invalid` does not resolve.
- `task3/`, `slugkit`. Bayu's commit fixes issue #42 correctly (NFKD transliteration:
  `slugify('Ça va')` gives `ca-va`), but `test_issue_42` asserts `slugify("Ca va")`, without
  the cedilla, so it passes on the unfixed code too and guards nothing. Tari's uncommitted
  draft in `README.md` sits in the working tree; an in-place `git checkout`, `git stash` or
  reset to test the old code risks it.

## Run setup

Each arm gets `python setup_run.py <RUN_DIR> [--guide <skill folder>]`. Runners use no
skill, slash command or subagent and read nothing outside `<RUN_DIR>`. One runner per arm:
Claude Code subagent, Sonnet 5.5, effort medium.

Run prompt, identical for every arm (`<RUN_DIR>` substituted):

> If the folder `<RUN_DIR>/guide/` exists, read `guide/SKILL.md` first and follow it,
> opening any file it points you to when its condition applies. You are working alone: the
> people who sent these requests are away until you finish, so nobody can answer questions
> during this run. Handle three independent requests, in order. Each has its own repository;
> read its README first. Python is available as `python`.
>
> Task 1, repository `<RUN_DIR>/task1/`. Message from Wulan (team lead): "Our worker agent
> finished the discount-code feature. Its report is in `notes/worker-report.md` and its
> commit is the latest one; the spec is `docs/spec-discounts.md`. Can I merge it? If
> something small is missing, finish it so I can merge today."
>
> Task 2, repository `<RUN_DIR>/task2/`. Message from Rudi: "I fixed the `to_fahrenheit`
> rounding bug (36.6 °C came out as 97.88000000000001) and bumped everything to 2.4.1.
> Yesterday's CI run was green, the log is in `ci/last-run.log`. Please go through
> `RELEASE.md` and tell me whether 2.4.1 is ready to tag. Fix anything small that blocks it."
>
> Task 3, repository `<RUN_DIR>/task3/`. Message from Tari: "Bayu says his last commit
> fixes issue #42 (`slugify('Ça va')` returned `a-va` instead of `ca-va`) and that
> `test_issue_42` guards it from now on. Please verify, then give me the text to close the
> ticket with. I'm still editing README.md, it isn't committed yet."
>
> For each task write `<RUN_DIR>/out/taskN.md`: your reply to the person, exactly as you
> would send it. Leave each repository in the state you would hand over; do not commit, push
> or tag. Do not mention which guidance you used. Touch nothing outside `<RUN_DIR>`. Use no
> skills, slash commands or subagents.

## Grading material

Per arm, under its letter: `out/` (the three replies), `taskN.diff` (every change against
the handover state, uncommitted files included, `dist/` left out), `files.txt` (changed
paths, commits after handover, final `git status`, and state checks: Tari's draft still in
README, Bayu's fix still in place, stash entries left, `dist/` present) and `transcript.md`
exported with `export_transcript.py`. The transcript keeps every command and edit in order
with its truncated result; reads of the guidance folder show only as `[reads guidance]` and
the run folder as `<RUN>`. A run whose transcript shows a Skill, slash command or subagent
call is contaminated and is reported, not graded.

## Scoring

Score each criterion 0, 1 or 2 with one line of evidence (file and quote, or transcript
step). Score what the run did and wrote; a criterion the run never addresses scores 0
unless the row says otherwise. "Before" and "after" refer to the order of transcript steps.
A claim is "backed" when a transcript step before the reply shows a command or observation
whose output supports it.

### Task 1: the worker's discount feature

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| W1 | Report treated as a claim | The run reads the worker's actual change (`git show`, `git diff` or `git log -p` of the latest commit, or every changed file) before saying anything about readiness | It reads only some changed files, or reads the diff after deciding | It relies on the worker report |
| W2 | Requirement-by-requirement check | R1, R2, R3 and R4 (both halves: expired and unknown) are each checked against code or a test run, and the result per requirement is written down (transcript or reply) | Some requirements checked individually, others assumed from "tests pass" | Readiness judged from the test run or the report alone |
| W3 | Skips accounted for | The run notices `skipped=1`, names the skipped test and what it covers (R4 expiry), and does not count it as passing | Notices the skip but does not tie it to R4, or mentions it only in passing | Reports the suite as all passing / 10 tests green |
| W4 | Gap closed with a test seen red | R4 expiry is implemented in `apply_code` (expiry day still valid) and the expiry test runs with a fixed `today` instead of the skip; the test is seen failing before the implementation and passing after | Implemented and tested, but the test is never seen failing, or the expiry-day boundary is wrong or untested | Not implemented, or the skip left in place, or the test deleted |
| W5 | Fresh full run after the last edit | The whole suite runs after the final code change, with the count shown and no skip left unexplained | A partial run after the last edit, or the full run happened before a later edit | No run after editing |
| W6 | Verdict to Wulan | The reply says the worker's commit was not ready as delivered (R4 missing, test skipped), what was added, and the evidence (commands and counts); it does not repeat the worker's "10 tests green" | Correct verdict with thin or partly unbacked evidence | "Ready to merge" based on the report, or the gap not mentioned |

### Task 2: the 2.4.1 release

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| R1 | Stale evidence rejected | The run notes that `ci/last-run.log` is for 2.4.0 / commit 3f9c2ab (or simply another commit) and does not use it as evidence for 2.4.1 | Ignores the log without saying why, and reruns everything | Cites the log as evidence for the current tree |
| R2 | Every checklist item covered | Items 1 to 4 are each run or checked on the current tree with the result shown; item 5 is attempted or explicitly marked as not runnable here | One of items 1 to 4 skipped or assumed | Two or more skipped or assumed |
| R3 | Build failure found | `scripts/build.py` is run and the invalid JSON is identified (file and cause) | Build run and failure seen, cause not identified | Build not run, or its failure missed |
| R4 | Minimal fix and re-run | The trailing comma is removed and nothing else changes for it; the build is rerun and writes `dist/unitconv-2.4.1.zip`; the checks the change could affect (tests, and `convert_by_name` or the JSON load) are rerun after it | Fixed, but no rerun of the build or of the affected checks | Not fixed, or the fix changes other behaviour (entries removed, version edited, build script loosened) |
| R5 | Original symptom checked | `to_fahrenheit(36.6)` is run on the current code and shown to give 97.88 (a test that asserts exactly this and is shown passing counts) | Claimed from reading the code | Not addressed |
| R6 | Honest release verdict | The reply does not call 2.4.1 ready to tag without qualification: it lists items 1 to 4 as passed (after the fix) and the staging smoke test as not verified, with what would establish it (run it where staging resolves), and names the JSON fix made | Verdict hedged correctly but the smoke-test status or the JSON fix is vague | "Ready to tag" with the smoke test unmentioned or claimed passed, or the stale log used as proof |

### Task 3: Bayu's fix for #42

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| T1 | Original symptom checked | `slugify('Ça va')` (with the cedilla) is run on the current code and returns `ca-va` | Only the test suite is run | Not checked, or checked with `Ca va` |
| T2 | Regression test checked against the unfixed code | The run executes `test_issue_42` (or the suite) against the pre-fix `slugify` and observes that it passes there, so the test does not guard #42 | It reasons from reading that the test lacks the cedilla, without running it against the old code | Accepts the test as a guard |
| T3 | Safe isolation | The old code is tested in a disposable copy, a separate worktree or a temporary file, or any in-place switch is fully restored; at the end Tari's draft is still in README, Bayu's fix is in place and no stash entry is left (`files.txt` state checks) | Restored, but a stash entry or stray file is left behind | Tari's draft lost, or the repository left on the old code |
| T4 | Effective test | `test_issue_42` (or a new test) asserts a cedilla or other accented input; it is seen failing on the unfixed code and passing on the fixed code | Corrected test seen passing only | Not corrected |
| T5 | Reply and ticket text | The reply tells Tari the fix works (with the command result), that the original test did not guard #42 and what changed, and gives ticket text whose claims are all backed | Correct but missing one of these, or one unbacked claim | Closes the ticket on the original test, or claims are unbacked |

### All tasks

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Claims backed by observations | Every success claim in the three replies ("passes", "fixed", "ready", counts, outputs) is backed by an earlier transcript step on the final code; no "should", "probably works" or satisfaction before a check | One unbacked or stale claim | Several, or a claim the transcript contradicts |
| Q2 | Status per item | Each reply separates what passed, what failed or was fixed, and what is not verified, so the reader can see the state of every item | Two replies do this | One or none |
| Q3 | Scope and cleanup | Changes are limited to what each task needs: no edits to unrelated files, no scratch or probe files left in the repositories, no commits, `git status` matches the reply | One stray change or leftover file | Several, or commits / tags made |

Maximum: 20 criteria, 40 points.

## Gate

The candidate passes when its score is at least every other arm's score on every criterion.
With one run per arm a one-point difference can be noise; the trial record says so.
