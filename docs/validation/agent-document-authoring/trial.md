# Comparison trial: agent document authoring

Run on 2026-11-25. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen before the candidate was written.

## Setup

- Arms: Matt Pocock's `writing-for-agents` (mattpocock/skills commit 3216582); the current
  `andino-agent-document-authoring` (AI-RULES main at aa86828); the candidate rewrite
  (branch `skill/agent-document-authoring-upgrade`, skill folder identical to the one this
  change commits).
- Runners: three Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, run at
  the same time. Each got the rubric's run prompt, its own skill copy and its own run folder,
  and was told to read nothing else and to use no skills or slash commands.
- Blinding: arms were shuffled to letters (A candidate, B current, C Matt). The grader, one
  Sonnet 5.5 subagent at medium effort, saw only the rubric, the fixture and the three
  `out/` folders. Its evidence per score is in [scores.md](scores.md).

## Scores

| Criterion | Matt (C) | Current (B) | Candidate (A) |
| --- | --- | --- | --- |
| D1 restated commands and layout | 1 | 2 | 2 |
| D5 checkable completion criterion | 0 | 2 | 2 |
| D7 pointer with synonym triggers | 1 | 1 | 1 |
| D2-D4, D6, D8-D11 | 2 each | 2 each | 2 each |
| S1-S5 | 2 each | 2 each | 2 each |
| Q1-Q5 | 2 each | 2 each | 2 each |
| Task 1 | 18 | 21 | 21 |
| Task 2 | 10 | 10 | 10 |
| Quality | 10 | 10 | 10 |
| Total | 38 | 41 | 41 |

Gate (candidate at least equal to Matt on every criterion): PASS.

## Reading the result

- The candidate and the current skill both beat Matt's on D1 and D5: Matt's run kept the
  Makefile command list and left the AGENTS.md without a checkable done-when.
- The candidate did not beat the current skill on this fixture; both scored 41. The trial
  shows parity with the current skill, not an improvement over it.
- No arm collapsed the synonym triggers in the dbt pointer (D7 = 1 for all three), although
  all three skill texts state the one-trigger-per-branch rule.
- The grader flagged two judgement calls that could each move one point: D5 scored equal for
  A and B although only B added a criterion for `make dbt-build`, and B's description keeps
  one synonym pair (S2).

## Limitations

- One run per arm, so a one- or two-point gap can be noise.
- The same author wrote the fixture, the rubric and the candidate. The candidate was written
  after the rubric was frozen and may fit this fixture.
- Runners and grader come from one model family.
- Output style can hint at the arm (for example a preservation ledger), so blinding is partial.
- The rubric scores document properties. It does not measure how agents behave when they
  later follow the rewritten documents.
