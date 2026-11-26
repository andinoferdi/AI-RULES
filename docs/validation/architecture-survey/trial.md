# Comparison trial: architecture survey

Run on 2026-11-26. Blind runs on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (commit 9063dcc) before the candidate was written.

## Setup

- Arms: Matt Pocock's `improve-codebase-architecture` with the skills it calls
  (mattpocock/skills commit 7739eae: `improve-codebase-architecture`, `codebase-design`,
  `grilling`, `domain-modeling`); the current `andino-architecture-survey` (AI-RULES main at
  49ad00b); the candidate rewrite on branch `skill/architecture-survey-upgrade`. Both Andino
  arms had `api-and-interface-design` beside them, as installed.
- Repository: every run got a fresh copy built by `fixture/build_repo.py` (26 commits).
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, with the rubric's run prompt
  verbatim and no other skill, slash command or subagent. The Matt and current arms ran once,
  in parallel, while the candidate was being written. The candidate ran three times, once per
  revision below.
- Blinding: before each grading the three output sets were shuffled to new letters, the run
  folder paths were replaced with `<RUN_DIR>`, the report file prefixes (which differ between
  the arms) were renamed, and the files were scanned for mentions of the guidance used (only
  false positives such as "formatting"). Each grader was a fresh Sonnet 5.5 subagent at medium
  effort that saw only the rubric, the fixture and the three output folders.
- Rubric count: the rubric says 25 criteria and 50 points; it has 24 criteria, so the maximum
  is 48. The graders copied "50" into their headings. Scores below are out of 48. The frozen
  rubric was not edited.

## Scores

| Grading | Candidate revision | Candidate | Matt | Current | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | 53315eb | 43 | 44 | 38 | [scores.md](scores.md) |
| 2 | 01c4d26 | 45 | 44 | 39 | [scores-rerun.md](scores-rerun.md) |
| 3 | c0a6277 | 47 | 42 | 39 | [scores-round3.md](scores-round3.md) |

Gate (candidate at least equal to Matt and to the current skill on every criterion):

- Grading 1: FAIL. Below Matt on F4, F5, R7 and G1; below current on G1.
- Grading 2: FAIL. F4, F5, R7 and G1 fixed. Below Matt on D2 and R4; below both on G4.
- Grading 3: PASS. At least equal to both arms on all 24 criteria; above Matt on R2, R5, V1,
  G2 and S2, and above the current skill on F4, F5, R4, R6, V1, V2, S1 and S2.

Per-section totals in grading 3:

| Section (max) | Candidate | Matt | Current |
| --- | --- | --- | --- |
| Findings (10) | 10 | 10 | 8 |
| Discrimination (8) | 8 | 8 | 8 |
| Report (14) | 14 | 12 | 12 |
| Vocabulary (4) | 4 | 3 | 2 |
| Grilling and side effects (8) | 7 | 6 | 7 |
| Safety and honesty (4) | 4 | 3 | 2 |
| Total (48) | 47 | 42 | 39 |

## What failed and how it was fixed

Each loss was traced to a sentence in the candidate output and the skill text that produced it.

| Grading | Criterion | What the candidate did | Fix |
| --- | --- | --- | --- |
| 1 | F5 | Dropped the untested webhook: "PayGate would have only one adapter" | 01c4d26: an injected third-party client has a second adapter; inline-built clients are a candidate; "Also found" list |
| 1 | G1 | Deferred tests and caller migration to a second grilling round | 01c4d26: the first round covers all five decisions |
| 1 | R7 | Named a "renew call" in the turn-1 solution, copying the vocabulary example "whose submit call owns the transaction" | 01c4d26: examples and diagrams name no method before grilling |
| 1 | F4 | Changed the correct pure `prorate` function as the fix | 01c4d26: say where the defect lives; gather the callers' computation |
| 2 | G4 | Refused to name the interface after "settle the design" (over-applied the 01c4d26 rule) | c0a6277: the settled shape names the interface |
| 2 | D2 | Counted `jest.mock` as a second adapter (from the 01c4d26 wording "the test's mock") | c0a6277: an adapter is passed in at the seam; module mocking is not one |
| 2 | R4 | One diagram pattern on every card | c0a6277: at least two patterns per report |

The council had advised trying a shorter SKILL.md body first if the candidate lost a
criterion. None of the losses traced to length, so the wording was fixed instead; the ruling
is recorded in the execution plan.

## Reading the result

- On this fixture the final candidate finds everything Matt's skill finds (F1-F5 all 2 in
  grading 3) and keeps the Andino advantages the rubric scores: one-sentence cards with short
  wins (R2), a report that reads without the CDNs (R5), the ADR offer and record (G2) and
  checked claims (S2).
- Matt's arm never recorded the ADR the user asked for (G2 0, 0, 0): it judged ADR-0002 already
  covered the decision. Both Andino arms extended ADR-0002 instead of duplicating it.
- The current skill trails both on proration and the webhook (F4, F5), on vocabulary (the
  invented "Quote module", depth shown as line counts) and on report links and diagram variety.
- Two of the five fixes repaired defects the previous fix introduced. Each wording change can
  move behaviour; the preservation test guards the text, only a run shows the behaviour.

## Limitations

- One run per arm per grading. The Matt and current outputs were graded three times without
  changing, and their totals moved (Matt 44, 44, 42; current 38, 39, 39). Extending an existing
  ADR scored 2 in gradings 1 and 2 and 1 in grading 3. A one-point gap on one criterion is
  within that noise.
- The candidate was revised twice after seeing the gradings; the final revision was graded
  once. Revising against a fixed rubric risks fitting this fixture; the fixes were written as
  general rules and no fixture name appears in the skill.
- The same author wrote the fixture, the rubric and the candidate. The rubric was frozen
  first, but the candidate may still fit this fixture.
- The runners' one-paragraph hand-back reports from the Matt and current arms (which files
  they changed, and that neither wrote a new ADR) were seen before the candidate was final.
  Their outputs were not read until grading 1 was done. The rule to extend an existing ADR
  instead of duplicating it was written after those reports.
- In grading 3 the candidate's runner left a `gen_report.py` helper next to the report in the
  temporary directory; delivery.txt told the grader. It does not affect the scored criteria.
- Runners and graders come from one model family. No unguided control arm was run.
- The rubric scores what the agent said and wrote. No report was opened in a browser and no
  fixture code was compiled or executed.
