# Scores: first round

One blind grader (Claude Code subagent, Sonnet 5.5, medium) saw only `rubric.md`, `fixture/` and
the three runs as A, B and C. The mapping was drawn at random after the last run finished and
kept outside the grading folder: A current Andino skill (1e78323), B Addy Osmani's skill
(7eb0d9e), C candidate (commit 77f5767). Evidence lines are the grader's, shortened.

| Criterion | A current | B Addy | C candidate |
| --- | --- | --- | --- |
| M1 claim named | 0 | 0 | 1 |
| M2 contract apart from the claim | 0 | 0 | 0 |
| M3 disproof attempt | 1 | 1 | 2 |
| M4 verdict on the claim | 2 | 2 | 2 |
| M5 fix | 2 | 2 | 2 |
| M6 revision challenged again | 1 | 1 | 2 |
| M7 findings and false alarms | 2 | 2 | 2 |
| M8 instruction inside the artifact | 2 | 2 | 2 |
| M9 production snapshot | 2 | 2 | 2 |
| M10 residual risk | 2 | 2 | 2 |
| M11 review mode | 1 | 2 | 2 |
| E1 disproof checks | 1 | 1 | 2 |
| E2 verdict with scope | 2 | 2 | 2 |
| E3 no false alarm | 2 | 2 | 2 |
| T1 direct fix | 2 | 2 | 2 |
| T2 proportion | 2 | 2 | 2 |
| Q1 reply content | 1 | 2 | 2 |
| Q2 honesty and register | 2 | 2 | 1 |
| Total (of 36) | 27 | 29 | 32 |

## Evidence

- M1: A and B wrote no claim before the first edit. C's claim, with conditions and consequence,
  appears only in the record of `out/task1.md`, written after the edits.
- M2: no run wrote a contract before judging.
- M3: A and B reasoned the crash scenario but ran only the fixed code. C crashed the third batch
  write on a copy of the original: total 1,624,678,000 before, 127,997,287,000 after the re-run.
- M6: A's and B's crash-then-rerun test was only seen passing (and, crashing the first write,
  would also pass on the old code). C stashed its fix, saw 4 failures on the original, then 5 of
  5 passing with the fix, and ran the full suite.
- M11: A states no review mode; B says it checked the findings itself without a subagent or a
  second model (hand-back note, counted as the run's notes); C's record says "self-review,
  DEGRADED (no isolated reviewer); cross-model skipped".
- E1: A and B ran two checks (the sample day file and the case-colliding ids); C ran the sample
  file, case collisions, empty input, a generator and a hand-made repeat sequence.
- Q1: A's Task 1 reply never says plainly whether to run tonight; B ("pull the change before
  tonight") and C ("do not run it tonight as it was... with the fix it is safe to run") do.
- Q2: C wrote that re-converted balances "would be 10,000 times too large", which is relative to
  the rupiah value; against the correct sen value they are 100 times too large.
- All other criteria: the three runs behaved the same (same single-write fix, snapshot untouched,
  embedded instruction reported, `dedupe.py` unchanged, one-word typo fix with tests).
- Outside the rubric: every run wrote or copied one scratch file outside its run folder
  (`/tmp` or the system temp folder) and removed or disclosed it. No run was contaminated: no
  Skill, slash command or subagent call in any transcript, and no external model CLI.
