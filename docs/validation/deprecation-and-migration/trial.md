# Comparison trial: deprecation and migration

Run on 2026-11-26. One blind run per arm on the three-repository fixture in `fixture/`, scored
against the [rubric](rubric.md), which was frozen with the fixture (commit 0e34191) before the
candidate was written. Evidence per score is in [scores.md](scores.md).

## Setup

- Arms: Addy Osmani's `deprecation-and-migration` (addyosmani/agent-skills, path last changed in
  9f91cc4); the current `andino-deprecation-and-migration` (AI-RULES main at 1e78323); an
  unguided control with no skill; the candidate rewrite (this branch).
- Runners: four Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own
  run folder made by `setup_run.py`, with the rubric's run prompt. The three baseline arms ran
  first; the candidate ran after the rewrite. The control stopped on an API usage limit during
  task 1 and was resumed from its own transcript with the user's approval; its prompt and
  workspace did not change.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design: the sibling layout with a quick
  path and six gates that each end on a named artifact, load-bearing rules (backfill, consumer
  map, notice contents) in the body, and only patterns, templates and the worked example in
  resources. All five advisors chose this option; the reviewers ranked the Executor's answer
  first.
- Collection and blinding: `collect_run.py` produced each run's replies, diffs, file list,
  database report and transcript; `export_transcript.py` replaced run paths with `<RUN>` and
  removed guidance text. The four runs were shuffled to letters with a random mapping kept
  outside the grading folder. One grader (Sonnet 5.5, medium) saw only the rubric, the fixture
  and A to D. No reply mentions the guidance, and no transcript shows a Skill, slash command or
  subagent call.

## Scores

| Criterion | Unguided | Addy | Current | Candidate |
| --- | --- | --- | --- | --- |
| M4 backfill | 1 | 1 | 1 | 2 |
| M8 phase plan | 1 | 1 | 1 | 2 |
| M9 consumer handoff | 1 | 1 | 1 | 2 |
| M10 tests | 1 | 2 | 2 | 2 |
| R3 behaviour differences | 1 | 1 | 1 | 2 |
| R4 migration path for the internal consumer | 0 | 0 | 1 | 1 |
| R5 partner notice | 0 | 0 | 1 | 2 |
| R6 removal conditions | 1 | 1 | 2 | 2 |
| Q2 honesty | 1 | 2 | 2 | 2 |
| Other 11 criteria | 2 each | 2 each | 2 each | 2 each |
| Total (of 40) | 29 | 31 | 34 | 39 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate is
higher than every other arm on M4, M8, M9, R3 and R5, ties the current Andino skill on R4 and R6,
and ties every arm on the other criteria.

## Reading the result

- On the outcomes that protect production, every arm did the same thing: an additive migration
  with triggers for the old worker, the JSON field kept, the Friday drop declined with named
  blockers, a down/up round trip, the endpoint kept, and both the config-loaded invoice engine
  and the partner's twice-monthly calls found. The fixture's traps were caught with or without a
  skill.
- The differences are in the artifacts handed over. Only the candidate wrote a batched,
  resumable backfill script and reran it to show it resumes (the other three ran one `UPDATE`
  and flagged it as a risk), a phase ledger with reads and writes per phase, handoff notes for
  the three owning teams, a run comparing the legacy and v2 engines on the October orders, and
  a draft partner notice. These are the artifacts the gates' "Done when" lines name.
- The current Andino skill already beat Addy's and the control on R4, R5 and R6 (consumer path,
  notice, removal window), the points its transition table and observation-window rule cover.
- No arm moved the invoice run off the legacy engine or built an adapter with a parity check
  (R4 at most 1): the candidate ran the comparison and left the choice to finance.

## Limitations

- One run per arm and one grader, all from one model family. A one-point gap can be noise. The
  grader names M8 (the candidate's ledger gives rollback for one phase only), R4, R5, M7 and Q2
  as readings that could go either way; none of them, read either way, puts another arm above
  the candidate on any criterion.
- The same author wrote the fixture, the rubric and the candidate, and wrote the candidate after
  reading the baseline outputs. The rubric was frozen first and the worked example uses another
  domain, but rules such as "a drop file in the migrations folder ships with the next release"
  and the usage-window shortcut target situations this fixture contains.
- The unguided run can be recognised by the absence of guidance text in its transcript.
- The control's run was split by a usage limit; it resumed from its own transcript.
- Every task is a small Python repository on Windows with SQLite; production locking, online
  DDL and real traffic were not exercised.
