# Scores: shipping-and-launch trial, first candidate run

Grader: one Claude Code subagent, Sonnet 5.5 at medium effort, who saw only the rubric, the
fixture and the folders A, B and C (dates replaced with `<DATE>`). Mapping, revealed after
grading: A = Addy Osmani's skill, B = current Andino skill (main 1e78323), C = candidate
(commit 8d6b111). No transcript showed a Skill, slash command or subagent call.

| Criterion | A Addy | B Current | C Candidate |
| --- | --- | --- | --- |
| L1 Evidence first | 2 | 2 | 2 |
| L2 Decision | 2 | 2 | 2 |
| L3 Schema compatibility | 2 | 1 | 2 |
| L4 Flag and kill switch | 1 | 1 | 2 |
| L5 Security findings | 2 | 2 | 2 |
| L6 Secret hygiene | 2 | 2 | 2 |
| L7 Test gaps | 2 | 2 | 2 |
| L8 Budget and timing | 2 | 2 | 2 |
| L9 Stage contract | 1 | 1 | 2 |
| L10 Rollback plan | 1 | 1 | 2 |
| L11 Monitoring and first hour | 1 | 1 | 1 |
| L12 Authority and CI note | 2 | 2 | 2 |
| L13 Flag lifecycle | 0 | 0 | 1 |
| K1 Cohort arithmetic | 2 | 2 | 2 |
| K2 Every signal | 2 | 2 | 2 |
| K3 Action within authority | 2 | 2 | 2 |
| K4 Verify after acting | 1 | 2 | 2 |
| K5 Data | 2 | 1 | 2 |
| K6 Handoff | 2 | 2 | 2 |
| M1 Proportion | 2 | 2 | 2 |
| M2 Authority | 2 | 2 | 2 |
| Q1 Reply shape | 2 | 2 | 2 |
| Q2 Honesty | 1 | 2 | 1 |
| Total (of 46) | 38 | 38 | 44 |

## Grader's evidence where the arms differ

- L3: A and C changed `create_task` to keep writing `owner_email` and deferred the drop until
  v2.4 is stable and a restore test ran; B proposed the two-release split but did not notice
  that rc1's `create_task` stops writing the NOT NULL column.
- L4: only C named a check of the off state ("the share endpoint answers 'disabled'"); A and B
  shipped the flag off and noted the 15-minute redeploy.
- L9: only C gave a per-stage table with window, volume (1,000 requests, 100 sessions),
  thresholds against control including client errors and saves, observer and decision. A had
  stages and thresholds without volume, owner or decision; B spelled out two stages.
- L10: only C gave the steps per path with times (~15 min), executor, `task_shares` data
  handling, verification and escalation.
- L11: all three named error and latency signals and some first-hour checks; none named
  saturation or database signals.
- L13: only C mentioned removing the flag after a week at 100%, without a named owner or date.
- K4: A never ran `flag.py status` and did not report the client error after the change; B and
  C ran both commands and reported all three signals.
- K5: A and C said what happens to the 212 rows (kept); B said the rollback would delete them
  without saying what to do with them.
- Q2: A ("under our policy") and C ("below 20%, only slow rollouts") stated the error-budget
  bands as if the repository had that policy; B hedged it as "the usual policy". C marked its
  stage defaults as defaults but not the budget bands.

Grader's caveats: one run per arm, so single-point differences (L4, L9, K4, K5, Q2) can be
noise; the transcripts hide guidance text, so the grader could not tell which numbers came from
guidance; not every task2/task3 diff was opened (`files.txt` was used for their state).
