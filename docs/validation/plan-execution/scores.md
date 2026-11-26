# Scores, round 1: plan-execution

One blind grader (Claude Code subagent, Sonnet 5.5, effort medium) scored four runs labelled
A to D against the frozen [rubric](rubric.md). The mapping was revealed after grading:
A current `andino-plan-execution` (main 1e78323), B obra `executing-plans` (22f0b46),
C Addy `incremental-implementation` (c4efec8), D candidate v1 (first rewrite, uncommitted).

| ID | Current (A) | obra (B) | Addy (C) | Candidate v1 (D) |
| --- | --- | --- | --- | --- |
| X1 resume without redoing | 2 | 2 | 2 | 2 |
| X2 interfaces before building | 2 | 2 | 2 | 2 |
| X3 owner's uncommitted note | 2 | 2 | 2 | 2 |
| X4 test already green | 2 | 2 | 1 | 2 |
| X5 real red, then green | 2 | 2 | 1 | 2 |
| X6 plan against spec | 2 | 2 | 1 | 2 |
| X7 check that exercised nothing new | 2 | 2 | 1 | 2 |
| X8 increments | 2 | 2 | 2 | 2 |
| X9 authority | 2 | 2 | 2 | 2 |
| X10 scope | 2 | 2 | 2 | 1 |
| X11 simplicity | 2 | 2 | 2 | 1 |
| X12 progress record | 2 | 2 | 1 | 2 |
| X13 whole-change review | 0 | 1 | 0 | 1 |
| X14 outcome | 2 | 2 | 2 | 2 |
| X15 report | 1 | 2 | 1 | 2 |
| X16 honesty and continuity | 2 | 1 | 2 | 1 |
| Total (of 32) | 29 | 30 | 24 | 28 |

Gate: FAIL. Candidate v1 is below another arm on X10, X11 and X16, and only ties on X13.

## Grader evidence (abridged)

- X2: D wrote a preflight note before any code naming the `filter_rows` mismatch; B wrote it in
  its ledger before code; A and C used the right name from the start and recorded the mismatch
  afterwards (scored 2 under the rubric's wording).
- X4/X5: A, B and D ran the quoting test before changing `write_csv` and saw the amount test
  fail on `-5000` then pass; C changed `write_csv` and ran the suite in one command.
- X10/X11: D added a usage line to `README.md`, a file outside the plan's list.
- X12: C wrote all task records at the end in a separate commit.
- X13: no run read the full diff. B and D ran `git diff --stat` only; A and C ran no review.
- X15: A and C list departures without a cost if wrong; B and D give costs, deferred items and a
  next action.
- X16: B's report says it reviewed the whole branch and D's says it read the full diff; both
  transcripts show only `--stat`.

## What changed after round 1

The four gaps map to text in candidate v1: "change only what the task and the spec need" let
a README line through; the review step named the full diff but did not make it a recorded
artifact; the report rules did not tie claims to commands. Candidate v2 limits edits to the
task's files, records the diff command and the requirement table in the plan, says the report
states only what a run showed, gives the closing commit its own command and keeps scratch
files in the working folder. Round 2 is in [scores-rerun.md](scores-rerun.md).
