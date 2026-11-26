# Comparison trial: browser testing with DevTools

Run on 2026-11-26. One run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (commit 41b997a) before the candidate was written.

## Setup

- Arms: Addy Osmani's `browser-testing-with-devtools` (addyosmani/agent-skills commit 57bfe5d);
  the current `andino-browser-testing-with-devtools` (AI-RULES main at 49ad00b); the candidate
  rewrite (branch `skill/browser-testing-with-devtools-upgrade`), first as skill snapshot
  3ad4fd42 (SHA-1 of SKILL.md), then after the fixes below as eaa78799.
- Runners: Claude Code subagents on the `sonnet` model alias at medium effort, one per arm. Each
  got the rubric's run prompt, its own skill copy, its own run folder and its own server port,
  and was told to read nothing else and to use no skills, slash commands or subagents. Arms ran
  one at a time because they share one Chrome DevTools MCP browser. All runners used Chrome
  DevTools MCP.
- Blinding: outputs were copied to letter folders, absolute paths and file timestamps were
  removed from the diffs, server-log times were made relative to server start, and the folders
  were checked for mentions of the guidance (none found). Each grader (`sonnet`, medium effort)
  saw only the rubric, the fixture and the three letter folders. Its evidence per score is in
  [scores.md](scores.md) and [scores-rerun.md](scores-rerun.md).
- Council: before the rewrite, a five-advisor council (Sonnet, medium) with three anonymous
  reviewers (Haiku, low) chose a sibling-layout rewrite over a targeted patch, a re-base on Addy
  or a split into playbooks, on the baseline outputs read without grading. Four advisors chose
  the rewrite; the dissent asked for a preservation ledger, which the execution plan kept.

## First grading

| Criterion | Addy | Current | Candidate |
| --- | --- | --- | --- |
| T4 rapid ticking | 0 | 2 | 1 |
| T5 replay after fix | 1 | 2 | 2 |
| L1 narrow-width overflow | 2 | 1 | 1 |
| L2 viewport verification | 1 | 1 | 2 |
| A1 accessible name | 1 | 2 | 2 |
| A2 dialog keyboard | 0 | 2 | 2 |
| A3 contrast | 0 | 1 | 2 |
| A4 heading order | 0 | 0 | 2 |
| Q3 scoped changes | 2 | 1 | 1 |
| Q4 conditions recorded | 1 | 2 | 2 |
| Other 12 criteria | same in all arms (T3 1 each, the rest 2) | | |
| Total (of 44) | 31 | 37 | 40 |

Gate (candidate at least equal to Addy and to the current skill on every criterion): FAIL.

- T4, below the current skill: the candidate probed repeated ticking on the success path only
  and added no in-flight guard.
- L1, below Addy: the candidate measured the toolbar overflow but listed the unbreakable title
  without showing that it widened the grid.
- Q3, below Addy: the candidate raised tap targets to 44 px and restyled the focus ring with no
  failing observation. The candidate's own release pass caused part of this: it required
  44 x 44 px tap targets, which is WCAG 2.5.5 (AAA); the AA minimum (2.5.8) is 24 x 24 px.

## Fixes after grading

All in the candidate's `SKILL.md` (mirrored by `GUIDE.md`) and resources:

- Step 4: every element the overflow snippet lists gets a cause; a flex or grid item widened by
  its content's min-content width is its own cause with its own measurement.
- Step 5: change only what an observation showed failing, and list other improvements as
  recommendations; a failed optimistic update returns to the last state the server confirmed,
  and its control sends nothing new while its request is in flight.
- Step 6: the repeat probe runs on the failure path as well as the success path, with an odd and
  an even count; the overflow snippet runs again after each layout fix.
- Release pass, accessibility checklist and test-plan template: tap targets at least
  24 x 24 px (WCAG 2.2 AA), 44 x 44 px as a recommendation.

## Re-run after the fixes

The candidate arm ran again with snapshot eaa78799, same prompt, fixture, model and effort. A
fresh grader scored the existing Addy and current outputs and the new candidate output,
reshuffled (A current, B candidate, C Addy).

| Criterion | Addy | Current | Candidate |
| --- | --- | --- | --- |
| T2 cause | 1 | 1 | 1 |
| T3 fix | 1 | 1 | 2 |
| T4 rapid ticking | 0 | 1 | 2 |
| L1 narrow-width overflow | 1 | 1 | 2 |
| L2 viewport verification | 1 | 1 | 2 |
| A1 accessible name | 1 | 2 | 2 |
| A2 dialog keyboard | 0 | 2 | 2 |
| A3 contrast | 0 | 1 | 2 |
| A4 heading order | 0 | 0 | 2 |
| Q1 claims match evidence | 2 | 1 | 2 |
| Q4 conditions recorded | 1 | 2 | 2 |
| Other 11 criteria | 2 each | 2 each | 2 each |
| Total (of 44) | 30 | 35 | 43 |

Gate: PASS. The candidate is at least equal to both arms on all 22 criteria and higher than
both on T3, T4, L1, L2, A3 and A4.

The committed `SKILL.md` (eebf9a12) differs from the re-run snapshot eaa78799 only by the line
wrapping of one paragraph in step 6; the words are identical.

## Limits

- One run per arm. A one-point difference can be noise.
- The two graders scored the same Addy and current outputs differently: current 37 then 35,
  Addy 31 then 30. The largest shifts are T2 (2 for every arm in the first grading, 1 in the
  second, for not naming the unhandled rejection as a cause), current T4 (2 then 1), Addy L1
  (2 then 1) and current Q3 (1 then 2). Totals from different graders are not comparable;
  compare arms within one grading.
- The candidate author wrote the rubric and saw the first grading before the fixes. The fixes
  are general rules (overflow attribution, failure-path probes, scoped changes, the WCAG 2.2
  target size), but they were chosen because of the criteria that failed.
- Only Chrome DevTools MCP on one Windows host was exercised. Playwright MCP and host-browser
  paths of the skill were not run.
- Neither candidate run recorded a DevTools performance trace; both measured layout shift with a
  `PerformanceObserver`, which the rubric accepts.
