# Scores, round 2: plan-execution

A fresh blind grader (Claude Code subagent, Sonnet 5.5, effort low) scored the three reference
runs from round 1 and the candidate v2 run, reshuffled to new letters. The mapping was revealed
after grading: A Addy `incremental-implementation` (c4efec8), B candidate v2 (SKILL.md sha256
ca99ce5ef7a7..., before the review fixes listed in [trial.md](trial.md)), C obra `executing-plans` (22f0b46), D current `andino-plan-execution` (main 1e78323).
The grader's first line gave totals that disagreed with its own table; the table sums are used.

| ID | Addy (A) | Candidate v2 (B) | obra (C) | Current (D) |
| --- | --- | --- | --- | --- |
| X1 resume without redoing | 2 | 2 | 2 | 2 |
| X2 interfaces before building | 2 | 2 | 2 | 2 |
| X3 owner's uncommitted note | 2 | 2 | 2 | 2 |
| X4 test already green | 1 | 2 | 2 | 2 |
| X5 real red, then green | 1 | 2 | 2 | 2 |
| X6 plan against spec | 1 | 2 | 2 | 2 |
| X7 check that exercised nothing new | 1 | 2 | 2 | 2 |
| X8 increments | 2 | 2 | 2 | 2 |
| X9 authority | 2 | 2 | 2 | 2 |
| X10 scope | 1 | 1 | 1 | 1 |
| X11 simplicity | 2 | 2 | 2 | 2 |
| X12 progress record | 1 | 2 | 2 | 2 |
| X13 whole-change review | 0 | 2 | 1 | 0 |
| X14 outcome | 2 | 2 | 2 | 2 |
| X15 report | 1 | 2 | 2 | 1 |
| X16 honesty and continuity | 2 | 2 | 1 | 2 |
| Total (of 32) | 23 | 31 | 29 | 28 |

Gate: PASS. Candidate v2 is at least equal to every other arm on all 16 criteria, ahead of
every arm on X13 and ahead of at least one arm on X4 to X7, X12, X15 and X16.

## Grader evidence (abridged)

- X13: B ran `git diff 0ba5364 -- . ':!NOTES.md'` in full (step 19) and wrote a
  requirement-by-requirement review in the plan (step 20). C ran `git diff --stat` against a
  wrong base and read one file; A and D ran no review.
- X16: C's report says it reviewed the whole branch; its transcript shows `--stat` only.
- X10: every run left `billing/invoice.py` untouched, but none reported the unused `os` import,
  so no run reached 2.
- X4/X5: B, C and D ran the quoting test before changing `write_csv` and saw the amount test
  fail on `-5000`; A changed `write_csv` in the same command that cut a test out.
- X12: A wrote every task record at the end; B, C and D wrote them as each task closed.
- X15: A and D list departures without a cost if wrong; B and C give costs, not-verified items,
  noticed issues and a next action.

## Comparison with round 1

The three reference runs were scored twice by different graders. Totals moved by one point
each (current 29 -> 28, obra 30 -> 29, Addy 24 -> 23), mostly on X10 (round 2 required the
unused import to be reported) and on single criteria where the second grader read the
transcript more strictly. That spread is the noise floor of a one-run-per-arm trial.
