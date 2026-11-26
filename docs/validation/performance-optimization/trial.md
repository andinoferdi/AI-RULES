# Comparison trial: performance-optimization

Run on 2026-11-26. One blind run per arm on the four-repository fixture in `fixture/`, scored
against the [rubric](rubric.md), which was frozen (with the fixture) before the candidate was
written. Evidence per score is in [scores.md](scores.md).

## Setup

- Arms: Addy Osmani's `performance-optimization` (addyosmani/agent-skills, path last changed in
  783c41e, with its `references/`); ruvnet's `v3-performance-optimization` (ruvnet/agentic-flow,
  230611a); the current `andino-performance-optimization` (AI-RULES main at 1e78323); the
  candidate rewrite (this branch).
- Runners: four Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own
  run folder made by `setup_run.py`, with the rubric's run prompt. The three baseline arms ran
  first; the candidate ran after the rewrite.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design: the sibling layout with a quick
  path and six evidence gates, `SKILL.md` under 250 lines, detail in resources read on demand,
  and a record with an attempts table. Reviewer ranking put the Executor and First Principles
  responses first; the Contrarian (status quo) and Outsider (expand the current structure)
  responses last.
- Collection and blinding: `collect_run.py` produced each run's replies, diffs, file list and
  transcript; `export_transcript.py` replaced run paths with `<RUN>` and removed guidance text.
  The four runs were shuffled to letters with a random mapping kept outside the grading folder.
  One grader (Sonnet 5.5, medium) saw only the rubric, the fixture and A to D. No transcript
  showed a Skill, slash command, subagent call or package install.

## Scores

| Criterion | Addy | ruvnet | Current | Candidate |
| --- | --- | --- | --- | --- |
| B1 baseline | 1 | 1 | 2 | 2 |
| B2 locate by measurement | 1 | 1 | 1 | 2 |
| B5 after measurement | 2 | 1 | 2 | 2 |
| B6 regression guard | 2 | 0 | 0 | 2 |
| W6 next capture and guard | 1 | 1 | 1 | 2 |
| M2 locate by measurement | 1 | 1 | 1 | 2 |
| M5 after measurement | 2 | 1 | 2 | 2 |
| N3 reply | 2 | 1 | 2 | 2 |
| L1 attempt record | 1 | 1 | 1 | 2 |
| Q2 honesty and register | 2 | 2 | 1 | 2 |
| Other 14 criteria | 2 each | 2 each | 2 each | 2 each |
| Total (of 48) | 43 | 38 | 41 | 48 |

Gate (candidate at least equal to every other arm on every criterion, and the highest total):
PASS.

## Reading the result

- Every arm reached the same outcomes: N+1 replaced by two joined queries with the same
  checksum, the date-keyed cache declined for the tenant and billing reasons, the LCP image made
  eager without breaking the carousel, no invented LCP number, the cache key fixed with the
  locale kept, and `slugify` left unchanged after timing it. On outcome the three references and
  the current skill are not distinguishable on this fixture.
- The differences are in process evidence. Only the candidate attributed both bottlenecks by
  measurement before editing (round-trip cost times query count; the logger stubbed out and
  measured, 22.5 MB against 22.7 MB), ran its guards against the old code (51 != 1027;
  500 != 1) and against the new, and ended each reply with an attempts table that includes the
  declined cache and the ruled-out logger.
- Task 2 shows the honesty branch: the candidate's reply says the new LCP is NOT MEASURED, gives
  an expectation labelled as one, and names the capture (same Lighthouse mobile settings, three
  or more runs, median).
- The quick path held: the candidate timed `slugify`, compared it with the upload, changed
  nothing and wrote no record.

## Limitations

- One run per arm and one grader, all from one model family. A one-point gap can be noise.
- The same author wrote the fixture, the rubric and the candidate, and wrote the candidate after
  reading the baseline runs' command sequences. The rubric was frozen first and the skill's
  examples come from other domains (search API, comments, exchange rates), but the candidate may
  still fit this fixture. No held-out task set was run.
- The grader names judgement calls that a stricter reading would change. Two touch the
  candidate alone: W3 (only the hero image was sized; the team images were not, scored 2 under
  "preferably") and W6 (a unit-test guard and the exact capture, but no Lighthouse CI
  assertion). Under the strict reading the candidate drops to 1 on W3, below the other arms, and
  the gate would fail on that criterion. B1 and W5 would drop for the candidate and the current
  skill alike.
- The candidate's replies are longer: 2,260 words across four tasks against about 1,350 for each
  baseline arm, mostly the record. The quick-path reply (321 words) is longer than "a few lines".
- The candidate runner copied a file to `/tmp` and deleted it, outside the run folder the prompt
  allowed. It is not contamination under the rubric, but it broke the prompt's boundary.
- Every task is a small Python or static-HTML repository on Windows; no browser or Lighthouse
  was available to any runner.
