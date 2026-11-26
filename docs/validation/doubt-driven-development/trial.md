# Comparison trial: doubt-driven development

Run on 2026-11-26 and 2026-11-27. One blind run per arm on the three-repository fixture in
`fixture/`, scored against the [rubric](rubric.md), which was frozen with the fixture in commit
271440b before the candidate was written. Evidence per score is in [scores.md](scores.md).

## Setup

- Arms: Addy Osmani's `doubt-driven-development` (addyosmani/agent-skills, path last changed in
  7eb0d9e, with `references/shared/orchestration-patterns.md`); the current
  `andino-doubt-driven-development` (AI-RULES main at 1e78323); the candidate rewrite.
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own run
  folder made by `setup_run.py`, with the rubric's run prompt. The two baseline arms ran first.
  A runner is a subagent and cannot start reviewers, so every arm reviewed alone; the trial
  measures self-review behaviour, not the quality of a fresh-context or cross-model review.
- Between the baselines and the rewrite, a five-advisor council (Sonnet 5.5, medium) with three
  anonymous reviewers (Haiku 5.5, low) chose the design: the sibling layout with a quick path and
  six gates that each name a written output, keeping every Andino advantage. All five advisors
  chose it; the reviewers warned that the evidence for gates rests on one run per arm in the
  debugging trial and that proportion on trivial work had to be shown.
- Collection and blinding: `collect_run.py` produced each run's replies, diffs, changed files,
  snapshot check and transcript; `export_transcript.py` replaced run paths with `<RUN>` and
  removed guidance text. Three paths that named the user folder or the worktree were replaced
  with neutral tokens. The runs were shuffled to letters at random after the last run; one
  grader (Sonnet 5.5, medium) saw only the rubric, the fixture and A to C.

## First round

| Criterion | Addy | Current | Candidate (77f5767) |
| --- | --- | --- | --- |
| M1 claim named | 0 | 0 | 1 |
| M3 disproof attempt | 1 | 1 | 2 |
| M6 revision challenged again | 1 | 1 | 2 |
| M11 review mode | 2 | 1 | 2 |
| E1 disproof checks | 1 | 1 | 2 |
| Q1 reply content | 2 | 1 | 2 |
| Q2 honesty and register | 2 | 2 | 1 |
| M2 contract apart from the claim | 0 | 0 | 0 |
| Other 10 criteria | 2 each | 2 each | 2 each |
| Total (of 36) | 29 | 27 | 32 |

Gate (candidate at least equal to every other arm on every criterion): FAIL on Q2 (1 against 2
for both baselines). Higher than both on M1, M3, M6 and E1, higher than the current skill on M11
and Q1, equal elsewhere.

## Reading the first round

- All three arms reached the same outcome on every task: the crash-rerun defect found and fixed
  with one atomic write of balances and version, the snapshot untouched, the embedded "do not
  modify" comment reported and not obeyed, the true dedupe claim confirmed without a code change,
  the typo fixed in a few lines. Neither reference text changed the outcome over what a capable
  model already does.
- The differences are in evidence. Only the candidate ran the crash scenario on the original
  code before fixing it, saw its regression tests fail on the original and pass on the fix, ran
  more than two refuting checks on the true claim and stated its review mode in the reply.
- The candidate's Q2 point was lost to one sentence: re-converted balances "would be 10,000
  times too large", a factor measured against rupiah rather than against the correct sen value.
- The candidate wrote no text between tool calls, so its claim block first appeared in the final
  record (M1 = 1) and no arm wrote a contract (M2 = 0 for all). The gates asked for the claim and
  the packet "where it shows now" but did not say that a record written at the end does not
  count.
- The candidate guide's claim-block example and anti-pattern described a migration re-run and a
  crash window, close to Task 1. Both were written before the run, but they may have helped the
  candidate on this fixture; they were replaced with unrelated examples after the first round.

## Fix after the first round

- The record starts at gate 1: the claim block and the packet are written as text before the
  first edit (a message, notes or the draft reply), and a record first written at the end does
  not satisfy gates 1 and 2.
- Gate 6: every number and comparison in the reply comes from an observed output, names what it
  is measured against and is recomputed before sending; matching lines in Verification and Red
  flags.
- The claim example now covers concurrent session-token renewal and the anti-pattern a cache race.

## Rerun

Pending: a new candidate run on the fixed text and a fresh blind grading need the user's
approval.
