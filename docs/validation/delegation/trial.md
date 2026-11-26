# Comparison trial: delegation

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (commit 8d62b90) before the candidate was written. One
amendment (commit 4839def) was made after the unguided and current arms had run and before the
candidate existed; it applies to every arm and is quoted in the rubric.

## Setup

- Arms:
  - Unguided: no skill (control, outside the gate).
  - Reference: the three upstream skills together, `mattpocock/skills`
    `skills/engineering/implement-spec` (commit 6f7f783) and `obra/superpowers`
    `skills/dispatching-parallel-agents` and `skills/subagent-driven-development` (commit 22f0b46),
    full folders including scripts and references.
  - Current: `andino-delegation` from AI-RULES main at 49ad00b.
  - Candidate: the rewrite on branch `skill/delegation-upgrade`, skill folder as committed with
    this record.
- Runners: four Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each with the
  rubric's run prompt, its own copy of the fixture and of its skill folder, told to read nothing
  else and to use no skills, slash commands or subagents. The three baseline arms ran first; the
  candidate ran after the rewrite. The task is a dry run: execute a 7-task plan, get a failing CI
  green, and handle five subagent returns.
- Blinding: outputs were copied to letters (A current, B unguided, C candidate, D reference) with
  the same redactions for every arm: run-folder paths (which contained the arm name), the scratch
  folders `.andino/delegation` and `.superpowers/sdd`, and helper script names were replaced by
  neutral tokens. A scan found no remaining skill or arm names. The grader, one Sonnet 5.5
  subagent at medium effort, saw only the rubric, the fixture and the four letter folders. Its
  evidence per score is in [scores.md](scores.md).

## Scores

| Criterion | Unguided (B) | Reference (D) | Current (A) | Candidate (C) |
| --- | --- | --- | --- | --- |
| D7 brief content | 2 | 1 | 2 | 2 |
| D9 worker contract | 2 | 2 | 1 | 2 |
| D11 integration and finish | 1 | 2 | 2 | 2 |
| I4 real fixes | 1 | 1 | 1 | 2 |
| R3 Task 3 findings | 1 | 2 | 1 | 2 |
| Q3 plain and proportionate | 2 | 1 | 1 | 1 |
| Other 19 criteria | 2 each | 2 each | 2 each | 2 each |
| Task 1 (D1-D11, of 22) | 21 | 21 | 21 | 22 |
| Task 2 (I1-I5, of 10) | 9 | 9 | 9 | 10 |
| Task 3 (R1-R6, of 12) | 11 | 12 | 11 | 12 |
| Quality (Q1-Q3, of 6) | 6 | 5 | 5 | 5 |
| Total (of 50) | 47 | 47 | 46 | 49 |

Gate (candidate at least equal to the reference and to the current skill on every criterion):

- Against the reference: PASS. Equal or higher on all 25; higher on D7 and I4.
- Against the current skill: PASS. Equal or higher on all 25; higher on D9, I4 and R3.

## Reading the result

- On this small plan every arm, the unguided one included, chose to implement the tasks itself and
  found the main traps: both spec conflicts, the hidden Task 4 on Task 5 dependency, both shared
  files, the out-of-scope `money.py` edit, the empty test evidence and the shared working tree.
  The model already makes the delegate-or-not call well here; the differences are in the artifacts.
- The candidate gained where the rewrite added guidance: a complete worker contract (D9), a
  fix round sent to the idle approved worker with a scoped re-review (R3), and an explicit refusal
  to weaken tests (I4). The current skill had treated messaging that idle worker as needing a new
  approval and did the fixes itself.
- The candidate kept the current skill's strengths that the reference lacks on this fixture: a
  complete brief (D7) with owned and must-not-touch paths and rulings.
- The candidate chose to delegate Task 3 (security, independent files) to one implementer plus one
  reviewer; the other arms kept it inline with an optional reviewer. The rubric accepts both.
- Quality (Q3): the grader penalized the three longest outputs (reference 62 KB, candidate 51 KB,
  current 44 KB) for length and jargon; the unguided output was shortest (32 KB). The candidate's
  terms (envelope, frontier, lane) are defined in the skill but not in its output.

## Limitations

- One run per arm and one grading, so a one-point difference can be noise. The grader flagged D8
  (a short "900 s / 30 s" reminder repeated in three dispatches) as a judgement call scored 2.
- The same author wrote the fixture, the rubric and the candidate. The rubric was frozen first, and
  its one amendment came before the candidate existed, but the candidate may still fit this fixture.
- Runners and grader come from one model family.
- The fixture is a small plan where delegation mostly does not pay. Lanes, the rolling frontier and
  parallel investigators are described in the skill and its worked example but were not exercised.
- No arm started an investigation subagent in Task 2, so the investigator prompt was scored only
  through the amendment's inline-plan rule.
- The outputs are plans, prompts and messages. Nothing was executed against a real agent host.
