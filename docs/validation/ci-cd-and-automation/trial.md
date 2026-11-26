# Comparison trial: CI/CD and automation

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (commit 29ca948) before the candidate was written.

## Setup

- Arms: Addy Osmani's `ci-cd-and-automation` (addyosmani/agent-skills commit
  a05781556f8999e42ad884500053804720b4e568); the current `andino-ci-cd-and-automation`
  (AI-RULES main at 49ad00b); the candidate rewrite (branch
  `skill/ci-cd-and-automation-upgrade`: the skill folder of commit 049a6c0 without the Q3
  fix below; the two differ only in the fix lines of SKILL.md and its GUIDE.md mirror).
- Runners: three Claude Code subagents, Sonnet 5.5 at medium effort, one per arm. The two
  baseline arms ran first; a five-advisor council read their outputs before the rewrite; the
  candidate ran after it. Each runner got the rubric's run prompt, its own skill copy and its
  own run folder, and was told to read nothing else and to use no skills, slash commands or
  subagents.
- Blinding: outputs were copied to letters (A current, B candidate, C Addy) and checked for
  mentions of the guidance used (none found). The grader, one Sonnet 5.5 subagent at medium
  effort, saw only the rubric, the fixture and the three output folders. Its evidence per
  score is in [scores.md](scores.md).

## Scores

| Criterion | Addy (C) | Current (A) | Candidate (B) |
| --- | --- | --- | --- |
| C8 token and action hygiene | 1 | 2 | 2 |
| F1 evidence first | 1 | 2 | 2 |
| F3 red herring | 2 | 1 | 2 |
| Q3 proportion | 2 | 2 | 1 |
| Other 25 criteria | 2 each | 2 each | 2 each |
| Task 1 (C1-C11) | 21 | 22 | 22 |
| Task 2 (F1-F6) | 11 | 11 | 12 |
| Task 3 (D1-D8) | 16 | 16 | 16 |
| Quality (Q1-Q4) | 8 | 8 | 7 |
| Total (of 58) | 56 | 57 | 57 |

Gate (candidate at least equal to Addy and to the current skill on every criterion):

- Against Addy: FAIL on Q3 (1 versus 2); higher on C8 and F1; equal elsewhere.
- Against the current skill: FAIL on Q3 (1 versus 2); higher on F3; equal elsewhere.

## The Q3 failure and the fix

The candidate added `.github/dependabot.yml` and a web staging and promotion flow that the
tasks did not ask for. The rewrite caused the first: its least-privilege rule said Dependabot
or Renovate "updates" the pinned actions, and its verification checklist required that
Dependabot or Renovate keep actions current, so the runner added a configuration to satisfy
the checklist. Neither baseline skill pushes for that file.

Fix applied after grading (included in commit 049a6c0, together with two shortened
sentences that keep SKILL.md at 470 lines): procedure step 1 now says to
change only what the request covers and to list anything else the rules suggest (a gate,
environment, deploy target or automation such as Dependabot) as a follow-up; the
least-privilege rule makes Dependabot a follow-up unless the request covers dependency
updates; the checklist accepts "Dependabot, Renovate or a follow-up"; the output gains a
Follow-ups field.

## Re-run after the fix

On 2026-11-26 the candidate arm ran again with the fixed skill (branch commit b6f4b2f), same
prompt, fixture, model and effort. A fresh grader (Sonnet 5.5, medium) scored the existing
Addy and current outputs and the new candidate output, reshuffled (A candidate, B Addy,
C current). Evidence per score: [scores-rerun.md](scores-rerun.md).

| Criterion | Addy (B) | Current (C) | Candidate (A) |
| --- | --- | --- | --- |
| C8 token and action hygiene | 1 | 2 | 2 |
| F1 evidence first | 1 | 2 | 2 |
| F3 red herring | 2 | 1 | 2 |
| Q3 proportion | 2 | 2 | 2 |
| Q4 honesty and register | 2 | 2 | 1 |
| Other 24 criteria | 2 each | 2 each | 2 each |
| Total (of 58) | 56 | 57 | 57 |

Gate: FAIL on Q4 only (1 versus 2 against both arms); Q3 is fixed (the candidate listed
Dependabot under "Follow-ups (not built)" instead of adding it); higher than Addy on C8 and
F1 and than the current skill on F3; equal elsewhere.

The Q4 point: the candidate wrote that the action majors were "checked 2026-11-26 in the
guidance I follow; not fetched here". The grader read the mention of guidance as an implied
check and noted that the content is otherwise honest. The phrase repeats the date stamp in
the skill's least-privilege rule and breaks the run prompt's instruction not to mention the
guidance; the first candidate output, which used the same versions without that phrase,
scored 2 on Q4. The two graders gave identical scores to the unchanged Addy and current
outputs (56 and 57), so this is a difference in the candidate's text, not grader drift.

Across both runs the candidate scored 57, the current skill 57 and Addy 56. In each run the
candidate was at least equal to both arms on 28 of 29 criteria; the criterion it lost
differed (Q3, then Q4).

## Reading the result

- All three arms were strong: 56 to 57 of 58, full marks on Task 3 and on most of Task 1.
  On this fixture and runner model the skills move a few judgement calls, not whole tasks.
- The candidate improved on both baselines where the rewrite added guidance: it was the only
  arm on current action majors (`checkout@v7`, `setup-node@v7`, `upload-artifact@v7`) with
  the third-party AWS action pinned to a commit SHA, the only arm that explained the start-up
  retries in the logs as present in the passing attempt (F3, against the current skill), and
  it cited commits and the first failing step (F1, against Addy).
- It lost Q3 through a rule the rewrite added, which the fix above narrows.

## Limitations

- One run per arm per grading (two candidate runs), so a one-point gap can be noise; the
  graders marked Q3 and Q4 for the candidate, C8 and F1 for Addy and F3 for the current skill
  as uncertain.
- The re-run candidate output mentions "the guidance I follow" three times without naming it;
  the outputs were not edited before grading.
- The same author wrote the fixture, the rubric and the candidate. The rubric was frozen
  first, but the candidate may still fit this fixture.
- Runners and grader come from one model family. No unguided control arm was run.
- The rubric scores designs, workflows and scripts. Nothing was executed against GitHub, AWS
  or Vercel; the grader read workflows by eye (no YAML parser) and ran `bash -n` on scripts.
