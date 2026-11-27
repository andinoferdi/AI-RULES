# Comparison trial: andino-workflow orchestration

Run on 2026-11-27. One run per arm and scenario on the fixture built by
[build_orchestration_fixture.py](build_orchestration_fixture.py), scored against the
[rubric](orchestration-rubric.md). S1-S3 were frozen at abe8e28 and S4 at c981485, both before
any candidate text existed. Evidence per score: [orchestration-scores.md](orchestration-scores.md).
Design: [the approved design](../../specs/2026-11-27-andino-workflow-orchestration-design.md);
research: [ultracode-research.md](ultracode-research.md).

## Setup

- Arms: Current, `skills/andino-workflow/` at 1997a24; Candidate, the same folder on branch
  `claude/andino-workflow-orchestration` (round 1 at 52e3ef2, round 2 at df01389).
- Scenarios: S1 an 18-handler authorization audit with 7 planted gaps; S2 resuming a half-done
  billing audit whose code changed after its checkpoint; S3 a one-line fix; S4 a 49-handler audit
  with 14 gaps and checks hidden in other files. Both answer keys were confirmed by
  [probe_orchestration_oracle.py](probe_orchestration_oracle.py).
- Runners: Claude Code general-purpose subagents, `sonnet` at `medium`, one per scenario and arm,
  each on a fresh fixture with its own guidance copy and the rubric's run prompt; no installed
  skills, subagents, network or `gh`. The current arm ran before the candidate text existed.
- Collection: [collect_orchestration_run.py](collect_orchestration_run.py) copied each run's
  `out/`, repository state and untracked files, and wrote the tool trace and token totals from
  the runner's transcript.

## Rulings made during the trial

1. `add_expense` stores a row under a body-supplied id; the fixture did not intend that weakness.
   It counts neither toward recall nor against precision in either arm. Cost if wrong: one A2
   point for an arm that reports it as a gap.
2. Leads outside the requested folder are not graded under A1 or A2. Cost if wrong: one A2 point
   for the current arm, whose out-of-scope note wrongly named `get_invoice`.
3. A module line that gives one verdict for all of a module's handlers counts as listing them for
   X3 when the count matches. Applied to both arms. Cost if wrong: the current arm drops to 1 on X3.
4. A5 is read strictly: a coverage count that disagrees with the list it summarises is partial
   (1), even when the list itself is complete. Cost if wrong: the candidate's round-1 A5 would be 2.

## Scores

| Scenario | Current | Candidate round 1 |
| --- | --- | --- |
| S1 (of 14) | 13 | 13 (A5 -1, A6 +1) |
| S2 (of 12) | 12 | 12 |
| S3 (of 8) | 8 | 8 |
| S4 (of 14) | 12 | 12 (X3 -1, X6 +1) |
| Total (of 48) | 45 | 45 |

Gate, round 1: **FAIL** on A5, X3 and K1 (S3 cost 0.86% over 1.25x).

## Reading the result

- The current coordinator was already strong at both sizes: every planted gap found, no false
  positive, the drifted unit reopened on resume, and a short answer for the one-line fix. The
  owner's sense that andino loses to ultracode did not reproduce at 18 or 49 units with Sonnet at
  medium effort.
- What the loop added showed up where it aimed: both audits now name their stop reason and a
  second sweep by another method (A6, X6), and every candidate audit reproduced its findings by
  calling the handlers as another account instead of only reading the code. That proof is not
  scored by the rubric.
- What it cost: the reproduction step and extra turns raised S4 by 80% and S1 by 6.5%; S3 took one
  extra turn (26%, all of it that turn) without reading any orchestration text.
- Both lost points came from one gap in the recipe: the report step did not require every unit
  to appear once with its verdict, or the coverage total to match that list. Round 2 (df01389)
  adds exactly that.

## Limits

- One run per arm and scenario: model variance is not measured. A single extra tool turn costs
  about 73k tokens here, a quarter of the S3 budget, so K1 cannot separate skill cost from turn
  variance with one sample.
- The grader wrote the candidate and knew the mapping. Every score cites its evidence so another
  grader can redo it from the collected folders.
- Goal drift after compaction and fresh-context verification (the Thorough agent form) were not
  exercised: no runner could start agents, and no run was long enough to compact.
- No ultracode arm ran, so parity with ultracode stays NOT_VERIFIED.
- Discovery probes: NOT RUN. Prompts for a fresh session with the candidate installed: "Audit every
  route handler in this repository for missing authorization checks and report each finding with
  its evidence." (must load andino-workflow) and "What does the `--source` flag of `ai-rules setup`
  do?" (must be answered directly).
