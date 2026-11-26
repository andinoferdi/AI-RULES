# Comparison trial: constraint-driven development

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (commit b645fe4, cherry-picked from 45a2f87) before the
candidate was written.

## Setup

- Arms: Addy Osmani's `constraint-driven-development` (addyosmani/agent-skills commit 9c7f62d);
  the current `andino-constraint-driven-development` (AI-RULES main at 49ad00b); the candidate
  rewrite (branch commit 713bfd4); an unguided control with no skill.
- Runners: four Claude Code subagents, Sonnet 5.5 at medium effort, one per arm. The three baseline
  arms ran first (they were stopped once by a usage limit and resumed with the user's approval);
  the candidate ran after the rewrite. Each got the rubric's run prompt, its own skill copy and its
  own run folder, and was told to read nothing else and to use no skills, slash commands or
  subagents.
- The candidate runner's Write tool refused to save `REPORT.md`, `REVIEW.md` and `RESPONSE.md`
  (a harness rule for subagent report files). It returned their content as text, which the chair
  saved unchanged into its `out/` folder. Its `INTAKE.md` and repository changes were written by
  the runner itself.
- Blinding: outputs were shuffled to letters (A control, B candidate, C current, D Addy), run paths
  were replaced with a neutral name, and two generic phrases in D's report ("the skill's reference
  guard", "copied from the skill") were reworded to "a reference guard" and "copied from a
  reference". No output named the guidance it used. The grader, one Sonnet 5.5 subagent at medium
  effort, saw only the rubric, the fixture and the four folders. Its evidence is in
  [scores.md](scores.md).

## Scores

| Criterion | Addy (D) | Current (C) | Candidate (B) | Control (A) |
| --- | --- | --- | --- | --- |
| S2 intake questions | 2 | 2 | 2 | 0 |
| S3 contract shape | 2 | 2 | 2 | 1 |
| S5 both deployables | 2 | 1 | 1 | 2 |
| S7 coverage mechanics | 2 | 1 | 2 | 2 |
| S8 security | 2 | 2 | 1 | 2 |
| S11 stage placement | 1 | 2 | 2 | 2 |
| S15 exception policy | 1 | 2 | 2 | 1 |
| V6 no false alarms | 1 | 2 | 2 | 1 |
| V8 guard evidence and redaction | 2 | 2 | 2 | 1 |
| P2 unattended run | 2 | 1 | 2 | 1 |
| Other 17 criteria | 2 each | 2 each | 2 each | 2 each |
| Total (of 54) | 51 | 51 | 52 | 47 |

Gate (candidate at least equal to Addy and to the current skill on every criterion):

- Against Addy: FAIL on S5 (1 versus 2) and S8 (1 versus 2). Higher on S11, S15 and V6.
- Against the current skill: FAIL on S8 (1 versus 2). Higher on S7 and P2.

## The S5 and S8 failures and the fix

The candidate left api coverage and dependency scanning pending: the Vitest coverage provider could
not be installed in the sandbox, and the copy had no lockfile. The candidate skill told it to: its
Fallback said "A tool cannot be installed here (no network, no approval): write its row as pending
... do not mark it enforced". Addy's skill has no such line, and its arm declared the provider in
`package.json` and wired the scanner in CI.

Fix applied after grading (not yet re-run): the Fallback now says that a tool CI can install is
declared and enforced at the CI stage, with only the local proof recorded as unavailable, and that a
row stays pending only when it cannot run anywhere yet. Step 5 now says to add a missing coverage
provider to the manifest even when it cannot be installed locally, and that a missing lockfile does
not drop the dependency dimension (scan what CI installs). The step's completion criterion and the
verification checklist say the same.

## Guard battery

`battery.py` (13 scenarios) on the guards extracted from the skill's `resources/floor-guard.md`:

| Guards | Passed |
| --- | --- |
| Current skill, Node | 8 of 13 (fails G6, G7, G8, G12, G13) |
| Current skill, Python | 8 of 13 (same failures) |
| Candidate, Node | 13 of 13 |
| Candidate, Python | 13 of 13 |

Run on Windows 11 with Git for Windows 2.56, Node 26.13 and Python 3.15.2. Addy's guard was not
executed: running code taken from the third-party repository was declined, so the trial compares
skills only through graded agent output.

## Reading the result

- On totals the candidate is ahead of both other skills (52 against 51 and 51) and the control
  trails at 47, mainly on intake questions, the exception schema, the key it quoted and the
  unattended run.
- The candidate kept the current skill's wins (exception schema, edit-hook use) and gained Addy's
  (changed-line coverage, floor-only unattended run). It lost two criteria to a Fallback sentence
  that made it under-wire tools CI could install.
- All four arms caught nearly every problem in the agent's change and refused to lower the
  threshold under pressure; those criteria do not separate skills on this fixture.

## Limitations

- One run per arm and one grader, so a one-point gap can be noise; the grader named its least
  certain calls in scores.md.
- The same author wrote the fixture, the rubric, the battery and the candidate. The rubric and
  battery were frozen first, but the candidate may still fit this fixture.
- Runners and grader come from one model family.
- The candidate's report files were saved by the chair from the runner's text, not by the runner.
- Nothing in the outputs that needs `node_modules`, a network or CI (lint, tests, scanners) was
  executed by any arm.
