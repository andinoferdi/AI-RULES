# Comparison trial: brainstorming

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (commit 560e9b3) before the candidate was written.

## Setup

- Arms: Jesse Vincent's superpowers `brainstorming` (obra/superpowers commit 22f0b46, its three
  Markdown files; the visual-companion scripts were not used); the current `andino-brainstorming`
  (AI-RULES main at 49ad00b); the candidate rewrite (branch `skill/brainstorming-upgrade`, skill
  folder as first written, before the fixes below).
- Runners: three Claude Code subagents, Sonnet 5.5 at medium effort, one per arm. The two baseline
  arms ran first; the candidate ran after the rewrite. Each got the rubric's run prompt, its own
  skill copy and its own run folder, and was told to read nothing else and to use no skills,
  slash commands or subagents.
- Blinding: outputs were shuffled to letters (A superpowers, B candidate, C current) and checked for
  mentions of the guidance used. The superpowers arm's design path `docs/superpowers/specs/` named
  its source, so it was renamed to `docs/specs/` in the message and the folder; nothing else was
  changed. The grader, one Sonnet 5.5 subagent at medium effort, saw only the rubric, the fixture and
  the three output folders. Its evidence per score is in [scores.md](scores.md).

## Scores

| Criterion | Superpowers (A) | Current (C) | Candidate (B) |
| --- | --- | --- | --- |
| B2 echo and related path | 1 | 2 | 2 |
| B3 why first, open | 1 | 1 | 2 |
| B4 current read and gaps | 1 | 2 | 2 |
| W1 buzzword probe | 1 | 2 | 2 |
| W2 one question with a guess | 1 | 1 | 2 |
| G1 numbered round | 0 | 0 | 2 |
| G3 term challenge | 1 | 2 | 2 |
| D2 approaches | 2 | 0 | 0 |
| E2 scope and anti-goals | 2 | 1 | 1 |
| E3 decisions and what is left | 2 | 1 | 2 |
| E4 approaches recorded | 2 | 1 | 1 |
| E5 observable acceptance | 1 | 2 | 2 |
| E8 gate and next step | 2 | 2 | 1 |
| R3 superseding ADR | 2 | 2 | 0 |
| M1 root decisions first | 1 | 2 | 2 |
| M2 decisions tracked across sessions | 0 | 1 | 0 |
| M3 outcome before technology | 1 | 0 | 0 |
| Q2 honest facts | 2 | 2 | 1 |
| Q3 length fits the turn | 2 | 2 | 1 |
| F1 spike framing | 0 | 0 | 0 |
| Other 17 criteria | equal across arms | equal | equal |
| Total (of 74) | 59 | 60 | 60 |

Gate (candidate at least equal to superpowers and to the current skill on every criterion): FAIL.
The candidate is higher than both arms on B3, W2 and G1, and below at least one arm on D2, E2,
E4, E8, R3, M2, M3, Q2 and Q3.

## The failures and the fixes

Each failure traced to the skill text, not to the fixture:

- D2: procedure step 5 let how-questions into the decision rounds, and the agent kept asking
  (including whether "overdue" means past the due date, which `GLOSSARY.md` already defines)
  instead of moving to the approaches.
- E2, E4, E8, Q3: step 7 said to write the restate block and ask before writing the document, so
  when the user said "write it up" the agent sent a restate and another question, and announced
  that it would treat a later answer as approval.
- R3: the rule for a request that reverses a recorded decision did not say that going ahead
  needs a superseding ADR.
- M2, M3: the several-sessions route did not tell the agent to say it would keep a decision record,
  and the first message did not ask for the agent's reading of success.
- Q2: no rule asked the agent to mark claims from its own knowledge (what a vendor offers) as
  unverified.
- F1 (0 for all three arms): the first message had no branch for a "can we...?" question.

Fixes applied after grading, all in `SKILL.md` (mirrored in `GUIDE.md`):

- Step 5 holds only decisions about what gets built and for whom; how to build it is settled in
  the approaches or as the agent's call; a question the project already answers is applied, not
  asked; when the frontier is empty the next message lays out the approaches.
- Step 7 writes the design in the turn the user picks an approach or asks for the write-up, with
  the restate block opening its Intent section and every template heading (Approaches and
  Anti-goals included) present even in a short design.
- Step 8 asks for an explicit yes to the design and counts nothing else as approval.
- "Look before you ask" adds the superseding ADR and marks claims from the agent's own knowledge
  as unverified.
- Step 3 asks for the agent's reading of success, adds a branch for "can we...?" questions (the
  throwaway check), turns the known-why branch into one numbered round, and on the
  several-sessions route says that a decision record will be kept and where.
- Two red flags and two verification items cover the same points.

These fixes are not verified by a run yet.

## Limitations

- One run per arm per grading, so a one-point gap can be noise.
- The same author wrote the fixture, the rubric and the candidate. The rubric was frozen first, but
  the candidate may still fit this fixture.
- Runners and grader come from one model family.
- Checkpoints fix the user's replies, so the trial measures single turns, not a whole live
  conversation; the earlier agent turns in each transcript were written by the author.
