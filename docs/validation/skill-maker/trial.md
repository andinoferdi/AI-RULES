# Comparison trial: skill-maker

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (with the fixture) before the candidate was written.
Evidence per score is in [scores.md](scores.md).

## Setup

- Arms: no skill; Jesse Vincent's `writing-skills` (obra/superpowers, path last changed in
  2ce8aa1) with its `references/`; Addy Osmani's `using-agent-skills` (addyosmani/agent-skills,
  eca51a2) with `docs/skill-anatomy.md` (c4efec8) linked by one added line, since that repository
  has no skill for writing skills; the current `andino-skill-maker` (AI-RULES main at 1e78323);
  the candidate rewrite (branch `claude/andino-skill-maker-quality-6687b5`, skill folder identical
  to the one this change commits).
- Runners: five Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own
  run folder made by `setup_run.py`, with the rubric's run prompt. The four baseline arms ran
  first; the candidate ran after the rewrite. Runners could not start subagents, so the trial
  measures the skills they wrote and how they reported verification, not whether they would run
  baselines when they can.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design: the sibling layout with seven
  gates, each ending in a "Done when" line naming a visible artifact (routing table, scenarios
  with PASS/FAIL lines, evaluation record or labelled self-review with a runbook). All five
  advisors picked it; the reviewers ranked the answer that asked for artifacts a future reader
  needs, with self-review as the default path, first.
- Collection and blinding: `collect_run.py` produced each run's replies, diff, file list and
  transcript, hiding guidance paths and file names. The five runs were shuffled to letters with a
  random mapping kept outside the grading folder. One grader (Sonnet 5.5, medium) saw only the
  rubric, the fixture and A to E. No transcript showed a Skill, slash command or subagent call.

## Scores

| Criterion | No skill | Addy | obra | Current | Candidate |
| --- | --- | --- | --- | --- | --- |
| M5 lint-enforced item left to tooling | 1 | 1 | 1 | 1 | 2 |
| M8 test scenarios written | 0 | 0 | 0 | 0 | 2 |
| E2 positive recipe | 1 | 1 | 2 | 2 | 2 |
| E3 risk becomes a required slot | 1 | 2 | 1 | 2 | 2 |
| E8 evaluation of the revision | 0 | 1 | 1 | 1 | 2 |
| N1 routing of the three facts | 1 | 2 | 2 | 2 | 2 |
| Q2 honesty and register | 1 | 1 | 1 | 2 | 2 |
| Other 16 criteria | 2 each | 2 each | 2 each | 2 each | 2 each |
| Total (of 46) | 37 | 40 | 40 | 42 | 46 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate is
higher than every other arm on M5, M8 and E8, and ties the best arm on the other 20 criteria.

## Reading the result

- On the outcome of each request the arms look alike: every arm wrote a hard rule with an excuse
  table answering the three excuses, a stop when the check cannot run, a trigger-only
  description, an ordered output shape for `pr-summary`, the broken link fixed, `Fixes #` kept,
  and no skill for the three facts. The reference skills did not beat the current skill on this
  fixture, and the no-skill run was close behind.
- The candidate's lead is in the artifacts its gates name. It was the only run to write test
  scenarios with PASS and FAIL lines (six for the migration skill, five for `pr-summary`), to
  route the import-order failure to `make lint` in writing, and to score the old and new
  `pr-summary` on the same input against criteria fixed first, labelled as its own check. The
  current skill demands baselines and NOT_VERIFIED honesty in strong words; its run reported
  honestly but produced none of these artifacts.
- The current skill's gains over no skill (E2, E3, N1, Q2) held in the candidate: the rewrite
  kept what worked.

## Limitations

- One run per arm and one grader, all from one model family. A one- or two-point gap can be
  noise. The grader names E2, E3, E8, M7 and Q2 as readings that could move a point; none of them
  changes the gate, since the candidate scored 2 on each.
- The same author wrote the fixture, the rubric and the candidate, and wrote the candidate after
  reading the baseline runs. The rubric was frozen first and the candidate's examples come from
  another domain (generated protobuf code), but its gates target the three gaps the baselines
  showed, and its worked example routes a lint-caught item to the linter, the same lesson M5
  scores. The candidate may fit this fixture.
- Blinding is partial: the candidate ran 18 tool calls against 4 to 7 for the others, and its
  outputs carry gate artifacts no other arm wrote.
- The rubric's stated maximum (42) did not match its 23 rows; the grader scored all 23 and the
  rubric's arithmetic was corrected after grading, with no row changed.
- The trial cannot show whether agents run real baselines when they can start a fresh agent,
  since no runner could.
