# Comparison trial: verification

Run on 2026-11-26. One blind run per arm on the three-repository fixture in `fixture/`, scored
against the [rubric](rubric.md), which was frozen with the fixture (commit d119bd4) before the
candidate was written. Evidence per score is in [scores.md](scores.md).

## Setup

- Arms: no skill; Jesse Vincent's `verification-before-completion` (obra/superpowers 3be5aad);
  the current `andino-verification` (AI-RULES main at 1e78323); the candidate rewrite (this
  branch, the skill folder as it passed `tests/test_verification_distribution.py`).
- Runners: four Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own
  run folder made by `setup_run.py`, with the rubric's run prompt. The three baseline arms ran
  first; the candidate ran after the rewrite.
- The first superpowers run and the first current-Andino run stopped on an API usage limit
  during Task 1. The current-Andino runner was resumed with its context and finished; that run is
  the one graded. The superpowers runner could not be resumed, so a fresh runner ran the arm in a
  clean folder; the interrupted folder was not used.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design: four advisors picked the sibling
  layout with gates and a record; the fifth preferred a small patch for token cost and the risk of
  ritual on trivial claims. The rewrite took both: a quick path for one freshly checked claim, the
  resources hold the claim table and copy recipes, and the record labels anything only reasoned
  about as "by reading".
- Collection and blinding: `collect_run.py` produced each run's replies, diffs against the
  handover state, final repository state checks and transcript; `export_transcript.py` replaced
  run paths with `<RUN>` and removed guidance text. The runs were shuffled to letters with the
  mapping kept outside the grading folder. One grader (Sonnet 5.5, medium) saw only the rubric,
  the fixture and A to D. No transcript showed a Skill, slash command or subagent call.

## Scores

| Criterion | No skill | obra | Current | Candidate |
| --- | --- | --- | --- | --- |
| W2 requirement-by-requirement check | 1 | 2 | 2 | 2 |
| W4 gap closed with a test seen red | 1 | 1 | 1 | 2 |
| T2 regression test run on unfixed code | 1 | 1 | 1 | 1 |
| T5 reply and ticket text backed | 1 | 1 | 1 | 2 |
| Q1 claims backed by observations | 1 | 1 | 1 | 2 |
| Other 15 criteria | 2 each | 2 each | 2 each | 2 each |
| Total (of 40) | 35 | 36 | 36 | 39 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate is
higher than every other arm on W4, T5 and Q1, ties obra and the current skill and beats the
no-skill run on W2, and ties every arm on the other 16 criteria.

## Reading the result

- Every arm reached the same outcomes: the missing expiry rule found behind the skipped test and
  implemented with dated tests, the 2.4.0 CI log rejected, the invalid `units.json` found and
  fixed, the staging smoke test reported as not verified, the ineffective `test_issue_42`
  corrected, Tari's uncommitted README draft kept. On outcome, obra's skill and the current
  Andino skill are not distinguishable from running with no skill on this fixture.
- The differences are in process evidence and claim backing. Only the candidate ran the new
  expiry test before implementing the check and kept its failing output, and only the candidate
  ended each reply with a per-claim record.
- Three arms stated something they had not run. The no-skill and obra runs told Tari that "Ca va"
  already gave `ca-va` before the fix; the current-Andino run wrote "I ran the suite against the
  pre-fix code ... the old test passes there too", while its transcript ran only the corrected
  test there. The candidate labelled the same point "by reading".
- The candidate made its old-code copy inside the run folder and removed it; the other three
  wrote copies or backups to the system `/tmp`, outside the allowed folder (not a rubric
  criterion, so not scored).
- No arm, the candidate included, ran the delivered `test_issue_42` unchanged against the old code
  (T2 is 1 everywhere). Gate 4 asks for a failure on old code; it does not yet say to run a
  colleague's test as delivered first.

## Limitations

- One run per arm and one grader, all from one model family. A one-point gap can be noise.
- The same author wrote the fixture, the rubric and the candidate, and wrote the candidate after
  reading the baseline transcripts. The rubric was frozen first and the candidate's examples come
  from other domains (an amount parser, a CSV export), but the candidate may still fit this
  fixture.
- The fixture has no trivial claim, so the quick path and the cost of the record on small tasks
  are not measured.
- The no-skill run can be recognised by its missing guide folder.
- The grader's judgement calls are listed in scores.md; the only one that touches the candidate
  alone (an added `tests/test_registry.py` and a deleted `dist/` after the build was observed)
  would cost it one point on Q3 under a stricter reading. The total would still lead (38), but
  the per-criterion gate would then fail on Q3.
- Every task is a small Python repository on Windows.

## Follow-up run

After the merge, gate 4 was changed so that a fix and test that already exist are run with the
test exactly as delivered, on the old code in a disposable copy, before the test is edited; the
record, checklist, a red flag, a shortcut row and the contract's regression row say the same. One
new runner (Sonnet 5.5, medium) ran the follow-up candidate on the same fixture. A second, fresh
blind grader (Sonnet 5.5, medium) scored five runs together: the three baseline runs, the first
candidate run and the follow-up run, under new letters. Evidence is in
[scores-followup.md](scores-followup.md).

| Criterion | No skill | obra | Current | First candidate | Follow-up |
| --- | --- | --- | --- | --- | --- |
| W2 requirement-by-requirement check | 1 | 1 | 1 | 2 | 2 |
| W4 gap closed with a test seen red | 1 | 1 | 1 | 2 | 2 |
| T2 regression test run on unfixed code | 1 | 1 | 1 | 1 | 2 |
| T5 reply and ticket text backed | 1 | 1 | 1 | 2 | 2 |
| Q1 claims backed by observations | 1 | 1 | 1 | 2 | 2 |
| Q3 scope and cleanup | 1 | 1 | 1 | 1 | 2 |
| Other 14 criteria | 2 each | 2 each | 2 each | 2 each | 2 each |
| Total (of 40) | 34 | 34 | 34 | 38 | 40 |

Gate: PASS. The follow-up candidate is at least equal to every other run on every criterion, and
it is the only run that executed the delivered `test_issue_42` on the old code and saw it pass
before correcting it.

The second grader scored the baseline runs lower on W2 and Q3 than the first grader did (34
against 35 and 36), and the first candidate's Q3 at 1, which the first grader left at 2: the two
graders read the same rubric differently on grouped requirement results and on files written
outside the run folder. The ordering of the candidates against the baselines is the same under
both graders. One run per arm still applies.
