# Comparison trial: test-driven development

Run on 2026-11-26 on the three-repository fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen with the fixture (commit a1e102c) before the candidate was
written. Evidence per score: [scores.md](scores.md) (first candidate) and
[scores-rerun.md](scores-rerun.md) (second candidate).

## Setup

- Arms: no skill; Addy Osmani's `test-driven-development` (addyosmani/agent-skills, path last
  changed in df50a6d, with `references/shared/testing-patterns.md`); Matt Pocock's `tdd`
  (mattpocock/skills, 3f59913, with `tests.md` and `mocking.md`); Jesse Vincent's
  `test-driven-development` (obra/superpowers, 5bf4e78, with `writing-good-tests.md`); the current
  `andino-tdd` (AI-RULES main at 1e78323); the candidate rewrite (this branch).
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own run
  folder made by `setup_run.py`, with the rubric's run prompt. The five baseline arms ran first.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design: the sibling layout, a written
  slice list, six gates with "Done when" lines and a test record. All three reviewers ranked the
  first-principles answer first.
- Collection and blinding: `collect_run.py` produced each run's replies, diffs, file list, hidden
  checks (`check_run.py`) and transcript; `export_transcript.py` replaced run paths with `<RUN>`
  and removed guidance text. After the baseline runs, and before any grading, the exporter was
  changed to also drop the runner's final hand-back message to the chair, which could name the
  guidance (one baseline hand-back did); the replies are graded from `out/`. Outputs were shuffled
  to letters with a seeded random mapping kept outside the grading folder. Each grader (Sonnet 5.5,
  medium) saw only the rubric, the fixture and folders A to F. No transcript showed a Skill, slash
  command or subagent call.

## First candidate (v1)

| Criterion | No skill | Addy | Matt | obra | Current | v1 |
| --- | --- | --- | --- | --- | --- | --- |
| F1 vertical slices | 0 | 1 | 1 | 1 | 1 | 2 |
| F2 red for the right reason | 0 | 2 | 2 | 2 | 2 | 1 |
| F7 correct and minimal | 2 | 1 | 2 | 2 | 2 | 2 |
| B1 reproduce before changing | 0 | 2 | 1 | 2 | 1 | 2 |
| B2 failing test first | 1 | 2 | 2 | 2 | 2 | 2 |
| G1 no redundant production change | 2 | 1 | 2 | 2 | 2 | 2 |
| G2 test proven to catch the bug | 2 | 1 | 2 | 2 | 2 | 2 |
| Q3 clean handover | 2 | 1 | 2 | 2 | 2 | 2 |
| Other 11 criteria | 2 each, Q2 1 | same | same | same | same | same |
| Total (of 38) | 30 | 32 | 35 | 36 | 35 | 36 |

Gate (candidate at least equal to every arm on every criterion): FAIL on F2. v1 was the only arm
that built the two task-1 rules in separate red-green cycles (F1), and it reproduced the reported
invoice before editing. It wrote its `close_ticket` tests in the same step as the production
change and showed them failing only by restoring the old code, which the grader scored as no red
of their own.

The fix (v2): gate 1 names every seam a row needs, including any entry point the requester names;
gate 2 writes and runs every test that guards the row before its production change; gate 3 edits
production code only; gate 4 never stands in for gate 2 on a test written after the change.

## Second candidate (v2)

One runner and a fresh grader on the unchanged fixture, the five baseline outputs reshuffled with
it.

| Criterion | No skill | Addy | Matt | obra | Current | v2 |
| --- | --- | --- | --- | --- | --- | --- |
| F1 vertical slices | 0 | 1 | 1 | 1 | 1 | 1 |
| F2 red for the right reason | 0 | 2 | 2 | 2 | 2 | 2 |
| F7 correct and minimal | 2 | 1 | 2 | 2 | 2 | 2 |
| B1 reproduce before changing | 0 | 2 | 1 | 2 | 1 | 2 |
| B2 failing test first | 1 | 2 | 2 | 2 | 2 | 2 |
| Q2 replies | 1 | 1 | 1 | 1 | 1 | 2 |
| Q3 clean handover | 2 | 1 | 2 | 2 | 2 | 2 |
| Other 12 criteria | 2 each | 2 each | 2 each | 2 each | 2 each | 2 each |
| Total (of 38) | 30 | 34 | 35 | 36 | 35 | 37 |

Gate: PASS. v2 is at least equal to every arm on all 19 criteria and ahead on Q2: its replies end
with the test record, giving the commands, the failing-then-passing runs and what was not
verified. Both candidate runs proved the task-3 test in a temporary worktree of the pre-fix
commit; every other arm proved it by editing the production code temporarily.

## Reading the result

- On outcome every arm is the same: all hidden behaviour checks pass, and every arm's new tests
  fail on the code before the change. The reference skills, like the current one, are not
  distinguishable from each other or from the candidate by what the code does.
- The differences are in process evidence: reproducing a reported bug before editing, red runs
  tied to a change, the record in the reply.
- One rule per cycle (F1) is not yet reliable. v1 did it; v2, with stronger gate wording, wrote
  all task-1 tests for both rules first, like every reference arm, although Matt, obra and the
  current skill also tell the agent to work one slice at a time. The council's flip condition
  (the candidate still batches both rules) has therefore been met once and missed once.
- Q2 (replies with commands, before-and-after results and what is not verified) was 1 for every
  arm in both gradings except v2, whose replies end with the test record.

## Limitations

- One run per arm, and two graders from one model family. The two gradings of the unchanged
  baseline outputs disagree for Addy (32 then 34, on G1 and G2), so a one-point difference can be
  noise. The graders name F2, B1, Q2 and the
  line-ending rewrite of `accounts/service.py` after `git checkout` on Windows as readings that
  could go either way.
- v1 and v2 were graded by different graders against different shuffles; their totals do not
  compare v1 with v2.
- The same author wrote the fixture, the rubric and the candidate, and wrote the candidate after
  reading the baseline transcripts. The rubric was frozen first and the candidate's examples come
  from another domain (library loans); an early draft that used the fixture's domain in examples
  was replaced before any candidate run.
- The unguided run can be recognised by its failed attempt to list the guidance folder.
- Every task is a small Python repository on Windows.
