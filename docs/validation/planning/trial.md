# Comparison trial: planning

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (with the fixture) before the candidate was written.
Evidence per score is in [scores.md](scores.md).

## Setup

- Arms: Jesse Vincent's `writing-plans` (obra/superpowers, main on 2026-11-26); Addy Osmani's
  `planning-and-task-breakdown` with its shared definition-of-done reference
  (addyosmani/agent-skills, main on 2026-11-26); the current `andino-planning` (AI-RULES main at
  1e78323) with the workflow files it names; the candidate rewrite (branch
  `claude/andino-planning-skill-upgrade-dfc355`).
- Runners: four Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own
  run folder made by `setup_run.py`, with the rubric's run prompt. The three baseline arms ran
  first (the current-andino runner hit a usage limit and was resumed from its own transcript
  after the reset, with the user's approval); the candidate ran after the rewrite.
- Between the baseline runs and the rewrite, a council of five advisors (Sonnet 5.5, medium) and
  three anonymous reviewers (Haiku 5.5, low) chose the design: rewrite the skill in the sibling
  layout (four of five advisors), keeping the Change Specification, readiness and discovery
  items, coverage table and fresh-developer review. The reviewers' main caution, that one run
  per arm cannot prove what caused the current arm's long plan, is why the candidate trial is
  the test.
- Collection and blinding: `collect_run.py` produced each run's plan files, reply and changed
  paths, replacing skill and product names with `[guide]` and plan folders with `<plan>`. The
  four runs were shuffled to letters with a random mapping kept outside the grading folder. One
  grader (Sonnet 5.5, medium) saw only the rubric, the fixture and A to D. Blinding is partial:
  a plan's structure can hint at its guide.

## Scores

| Criterion | obra | Addy | Current | Candidate |
| --- | --- | --- | --- | --- |
| F5 existing code reused | 1 | 2 | 2 | 2 |
| T2 tests as code | 1 | 1 | 2 | 2 |
| T3 red, then green | 1 | 0 | 2 | 2 |
| T5 order and shared files | 1 | 2 | 2 | 2 |
| T8 runnable checks | 2 | 2 | 2 | 1 |
| U1 first step without questions | 2 | 1 | 2 | 2 |
| U2 proportion | 2 | 1 | 1 | 2 |
| U3 risks and review focus | 2 | 2 | 1 | 2 |
| Other 12 criteria | 2 each | 2 each | 2 each | 2 each |
| Total (of 40) | 36 | 35 | 38 | 39 |
| Plan length (lines) | 228 | 287 + 15 | 766 | 446 |

Gate (candidate at least equal to every other arm on every criterion): FAIL on one criterion,
T8. The candidate is the highest total, at least equal to every arm on 19 of 20 criteria, and
higher than every other arm on none alone; it is the only arm with 2 on both T3 (red, then
green) and U2 (proportion).

## Reading the result

- On outcome the four arms are close: all found the absolute `days_between` trap, kept old data
  files loading, fixed the fee in integer arithmetic, left R8 blocked with a seam, changed no
  source and claimed nothing as run. The skills differ in how the plan is written.
- The current skill wrote a 766-line checkpoint that transcribes most of the implementation (U2
  = 1) and has no risk list tied to tasks (U3 = 1). Its text encouraged this ("code snippets
  inside the plan are encouraged", "use a complete small body when that is the clearest
  specification"). The candidate replaces that guidance with obra's proportion rule and the
  "one reasonable thing" test; its plan keeps tests as code and the fee rule but no routine
  bodies, at 446 lines.
- obra's arm lost on prose-only RED steps, missing test helpers and unsequenced shared files;
  Addy's arm described tests in prose and had no failing run before a change. The candidate
  keeps the current skill's exact RED expectations and shared-file ordering.
- The candidate's one loss: its end-to-end run on the sample data said to check the lines by
  hand instead of stating the expected output (T8 = 1). The skill had no instruction for this.
  Gate 5, the contract's Coverage section and the Verification list now require each
  user-facing path to end with the real command on concrete data and its exact expected output.
  The re-run below tests that fix.

## Re-run after the T8 fix

With the user's approval, the patched candidate ran once more (run-5, Sonnet 5.5 medium, same
prompt) and a fresh grader (Sonnet 5.5, medium) scored it with the same three baseline runs
under a new shuffle. Evidence is in [scores-rerun.md](scores-rerun.md).

| Criterion | obra | Addy | Current | Candidate |
| --- | --- | --- | --- | --- |
| T2 tests as code | 1 | 1 | 2 | 2 |
| T3 red, then green | 1 | 0 | 2 | 2 |
| T5 order and shared files | 1 | 2 | 2 | 2 |
| T8 runnable checks | 1 | 1 | 1 | 2 |
| U1 first step without questions | 2 | 1 | 2 | 2 |
| U2 proportion | 2 | 2 | 1 | 2 |
| U3 risks and review focus | 2 | 2 | 1 | 2 |
| Other 13 criteria | 2 each | 2 each | 2 each | 2 each |
| Total (of 40) | 36 | 35 | 37 | 40 |
| Plan length (lines) | 228 | 287 + 15 | 766 | 388 |

Gate: PASS. The candidate is at least equal to every arm on all 20 criteria and the only arm
with a final task that runs both commands on concrete data with exact expected outputs (T8).
Its expected `arrears` totals for `--as-of 2026-04-10` (Rp 1.833.333 overdue, Rp 152.166 in
fees) agree with the spec's rules on the sample data.

The second grader was stricter on T8 for the baseline runs (2 -> 1 for obra, Addy and current)
and gave obra 2 on F5 where the first gave 1. The same files scored differently by one point on
a few criteria, which is the size of grader noise in this trial.

## Limits

- One run per arm, one fixture, one runner model: a one-point difference can be noise, as the
  two graders' differences on unchanged baseline files show.
- The candidate was patched once between the two gradings, on the one criterion it lost; the
  re-run tests that patch on the same fixture, not on a new one.
- The graders are the same model family as the runners.
