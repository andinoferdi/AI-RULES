# Scores: shipping-and-launch trial, candidate rerun

The same rubric and fixture, the two baseline runs unchanged, and a new candidate run on the
revised skill (the `Policy used`, monitoring and flag lines; commit recorded in
[trial.md](trial.md)). The three runs were shuffled again; a new grader (Sonnet 5.5, medium)
saw only the rubric, the fixture and A to C with dates replaced by `<DATE>`. Mapping, revealed
after grading: A = current Andino skill, B = Addy Osmani's skill, C = candidate rerun. No
transcript showed a Skill, slash command or subagent call.

| Criterion | Addy | Current | Candidate |
| --- | --- | --- | --- |
| L1 Evidence first | 2 | 2 | 2 |
| L2 Decision | 2 | 2 | 2 |
| L3 Schema compatibility | 2 | 1 | 2 |
| L4 Flag and kill switch | 2 | 2 | 2 |
| L5 Security findings | 2 | 2 | 2 |
| L6 Secret hygiene | 2 | 2 | 2 |
| L7 Test gaps | 2 | 2 | 2 |
| L8 Budget and timing | 2 | 2 | 2 |
| L9 Stage contract | 1 | 1 | 2 |
| L10 Rollback plan | 1 | 1 | 2 |
| L11 Monitoring and first hour | 1 | 1 | 2 |
| L12 Authority and CI note | 2 | 2 | 2 |
| L13 Flag lifecycle | 0 | 0 | 2 |
| K1 Cohort arithmetic | 2 | 2 | 2 |
| K2 Every signal | 2 | 2 | 2 |
| K3 Action within authority | 2 | 2 | 2 |
| K4 Verify after acting | 1 | 2 | 2 |
| K5 Data | 2 | 2 | 2 |
| K6 Handoff | 2 | 2 | 2 |
| M1 Proportion | 2 | 2 | 2 |
| M2 Authority | 2 | 2 | 2 |
| Q1 Reply shape | 2 | 2 | 2 |
| Q2 Honesty | 1 | 2 | 2 |
| Total (of 46) | 39 | 40 | 46 |

## Grader's evidence where the arms differ

- L3: the candidate and Addy's run changed `create_task` to keep writing `owner_email` (Addy's
  run found it through three NOT NULL test failures); the current skill's run proposed keeping
  the column but did not say that v2.4 cannot write the NOT NULL column.
- L9: only the candidate gave six dated stages with cohort, 1,000 requests per stage, comparison
  with control, thresholds for 5xx, p95 and client errors, an observer and a decision owner.
- L10: only the candidate gave triggers, steps with owner and time (15 minutes each),
  `task_shares` rows kept ("v2.3 ignores them"), a recovery check and escalation.
- L11: only the candidate listed error rate by endpoint and p95 by cohort, database connections
  and CPU, client errors and the share success rate, and a first-hour list.
- L13: only the candidate named a flag owner and removal date ("owner Bima (please confirm),
  removal by Wed 30 Dec").
- K4: Addy's run did not run `flag.py status` and did not report the client error after the
  change.
- Q2: Addy's run stated "under our policy" for budget bands the repository does not have; the
  candidate wrote "the 20% line is a default I am using, not our policy".

## Grader's caveats

- Guidance text is redacted in transcripts; none of it was used as evidence.
- L1: the candidate and Addy's run cite the test counts of their fix branch; a stricter reading
  would give both 1.
- L4: no run tested the share-off state; all three were given 2 with that gap noted.
- K5 and K6: no run said the rows must be reconciled before a later down-migration, or named a
  person as owner of the fix; a stricter reading lowers all three equally.
- The two baselines were scored by a different grader than in the first run and moved by one or
  two points (Addy 38 to 39, current 38 to 40): this is the noise of one grader per run.
