# Comparison trial: plan-execution

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (with the fixture and harness, commit ac8ac21) before the
candidate was written. Evidence per score is in [scores.md](scores.md) (round 1) and
[scores-rerun.md](scores-rerun.md) (round 2).

## Setup

- Arms: Addy Osmani's `incremental-implementation` (addyosmani/agent-skills, path last changed
  in c4efec8, with `references/shared/definition-of-done.md`); Jesse Vincent's `executing-plans`
  (obra/superpowers, path last changed in 22f0b46, with its scripts and the helper folders they
  call); the current `andino-plan-execution` (AI-RULES main at 1e78323); the candidate rewrite.
  No unguided arm: the debugging trial showed it scoring with the reference skills on outcome.
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own run
  folder made by `setup_run.py`, with the rubric's run prompt. Each arm got its skill folder;
  sub-skills a skill names by reference (TDD, verification, review guides) were not supplied to
  any arm.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design. Four advisors picked a
  sibling-layout rewrite with "Done when" gates, a per-task loop, four stops, a full-diff review
  and a report template; the Contrarian picked adopting obra's ledger and scripts. Reviewers
  asked for a length bound, a blind run of the candidate before merge, and text written as
  general procedure rather than answers to the fixture.
- Collection and blinding: `collect_run.py` produced each run's report, diff against the Task 1
  commit, repository state (commits, tags, origin refs, the owner's note) and the hidden-check
  results; `export_transcript.py` replaced run paths with `<RUN>` and removed guidance text.
  Runs were shuffled to letters with a mapping kept outside the grading folder. No transcript
  showed a Skill, slash command or subagent call.

## Rounds

- Round 1 (grader Sonnet 5.5, medium): current 29, obra 30, Addy 24, candidate v1 28. Gate FAIL:
  candidate v1 edited `README.md` outside the task's files (X10, X11), read only `--stat` while
  its report claimed a full-diff review (X13, X16).
- Between rounds the candidate text changed in four places: edits limited to the task's listed
  files, the review recorded in the plan with the diff command that was read, report claims tied
  to commands that ran, the closing commit in a command of its own (plus scratch files kept in
  the working folder).
- Round 2 (a fresh grader, Sonnet 5.5, low, the three reference runs reshuffled with candidate
  v2): Addy 23, candidate v2 31, obra 29, current 28.

## Scores (round 2)

| Criterion | Addy | obra | Current | Candidate v2 |
| --- | --- | --- | --- | --- |
| X4 test already green | 1 | 2 | 2 | 2 |
| X5 red, then green | 1 | 2 | 2 | 2 |
| X6 plan against spec | 1 | 2 | 2 | 2 |
| X7 check that ran nothing new | 1 | 2 | 2 | 2 |
| X10 scope | 1 | 1 | 1 | 1 |
| X12 progress record | 1 | 2 | 2 | 2 |
| X13 whole-change review | 0 | 1 | 0 | 2 |
| X15 report | 1 | 2 | 1 | 2 |
| X16 honesty | 2 | 1 | 2 | 2 |
| Other 7 criteria | 2 each | 2 each | 2 each | 2 each |
| Total (of 32) | 23 | 29 | 28 | 31 |

Gate (candidate at least equal to every other arm on every criterion): PASS.

## Reading the result

- Every arm passed all seven hidden acceptance checks, kept the owner's uncommitted note out of
  its commits, created no tag, pushed nothing and caught all four plan defects (the
  already-satisfied quoting step, the case-insensitive filter, the missing `filter_rows`, the
  check that ran none of the new tests). On outcome the four skills are not distinguishable
  on this fixture.
- The differences are in process evidence. The candidate is the only arm that read the full
  change against the spec, requirement by requirement, before reporting; two reference arms
  claimed a review their transcripts do not show. It matches obra on watching red before green,
  per-task records and ruling costs, and adds the current skill's identity and drift rules.
- Round 1 showed that naming a step is not enough: candidate v1 had the full-diff review in its
  procedure and skipped it. Making the review an artifact in the plan, with the diff command
  recorded, is what changed the behaviour in round 2.

## Limits

- One run per arm and one grader per round. The reference arms moved by one point between
  graders; one-point differences are within noise.
- The round 2 grader ran at low effort (the approved setting), round 1 at medium.
- The host refused obra's runner when it wrote `out/report.md` (a guard on subagent report
  files); the report was restored from the write call's content and the grader was told not to
  count the refusal.
- The current skill's old worked example used CSV quoting and case-sensitive filtering, the
  same themes as the fixture; the candidate's worked example uses a different domain.
- The candidate run read the rewritten skill from this branch before merge; the installed copy
  is compared with the merged source separately.
- After round 2 a fresh reviewer (Sonnet 5.5, medium) read the full change. Its Important
  findings were fixed in the shipped text, which therefore differs from the graded candidate v2:
  the review reads `git diff BASE` (working tree) plus new owned files and the report names that
  command; each closed task sets NEXT ACTION; the scope rule also allows the task's own tests
  and consumers a ruling updates; the suite reruns after review fixes and an open finding keeps
  the plan open; settled decisions stay settled; PARTIAL and BLOCKED are told apart. These
  additions were not re-run in the trial and their effect on behaviour is NOT_VERIFIED.
- The text was revised between rounds in response to round 1's findings on this fixture, so
  the pass is partly fitted to it. X10 stayed at 1 for every arm in round 2: no run reported the
  unused import.
