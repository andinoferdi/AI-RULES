# Comparison trial: brainstorming

Run on 2026-11-26 on the fixture in `fixture/`, scored against the [rubric](rubric.md), which was
frozen (commit 560e9b3) before the candidate was written. The baseline arms ran once; the
candidate ran four times (first version, after one round of fixes, after a second round, and after
a follow-up change), and each candidate run was graded blind together with the two baseline
outputs by a fresh grader.

Result: the version merged in PR #20 scored 71 of 74 against 59 and 59, one point below one arm on
W2, E2 and M1. The follow-up version scored 74 of 74 against 58 for superpowers and 56 for the
current skill, and meets the per-criterion gate (see "Follow-up run").

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

## Re-run after the fixes

The user approved two more subagents. The candidate arm ran again with the fixed skill (SKILL.md
blob dc78f50), same prompt, fixture, model and effort. A fresh grader (Sonnet 5.5, medium) scored
the existing superpowers and current outputs and the new candidate output, reshuffled (A candidate,
B current, C superpowers). Evidence per score: [scores-rerun.md](scores-rerun.md).

| Criterion | Superpowers (C) | Current (B) | Candidate (A) |
| --- | --- | --- | --- |
| B2 echo and related path | 1 | 2 | 2 |
| B3 why first, open | 1 | 1 | 2 |
| B4 current read and gaps | 0 | 1 | 2 |
| B5 no build, no ceremony | 2 | 2 | 1 |
| W1 buzzword probe | 1 | 2 | 2 |
| W2 one question with a guess | 1 | 2 | 2 |
| G1 numbered round | 0 | 0 | 2 |
| G3 term challenge | 1 | 2 | 2 |
| G5 own calls, few questions | 2 | 2 | 1 |
| D2 approaches | 2 | 0 | 0 |
| E2 scope and anti-goals | 2 | 1 | 2 |
| E3 decisions and what is left | 2 | 1 | 2 |
| E4 approaches recorded | 2 | 1 | 2 |
| E5 observable acceptance | 1 | 2 | 2 |
| F1 spike framing | 0 | 0 | 2 |
| F2 facts and permission | 1 | 1 | 2 |
| M1 root decisions first | 1 | 2 | 1 |
| M2 decisions tracked across sessions | 0 | 1 | 2 |
| M3 outcome before technology | 1 | 0 | 2 |
| Other 18 criteria | equal across arms | equal | equal |
| Total (of 74) | 57 | 59 | 69 |

Gate: FAIL on four criteria. The candidate is at least equal to both arms on 33 of 37 criteria
and higher than both on B3, B4, G1, F1, F2, M2 and M3; it is below on B5 (first message about 264
words against a 250-word bound), G5 (one routine "where does the list live?" question in its
round), D2 (at s1-cp4 it still asked before laying out approaches) and M1 (at s5 it asked the
outcome question but named none of the decisions that depend on it). Every first-run failure
except D2 is closed.

The two gradings disagree on unchanged outputs: superpowers B4 1 to 0 and F2 2 to 1; current B4
2 to 1, W2 1 to 2 and F2 2 to 1. That is grader variance of about one point on judgement calls,
and it moved the unchanged arms' totals by one and two points.

### Second round of fixes

- D2: the answer table now treats "whatever you think" as delegation (make the call, say it is
  yours, carry on) and keeps two concrete options only for a choice that is hard to undo; step 5
  ends when no decision only the user can make is open, and step 6 starts as soon as the answers
  settle what gets built, with leftover small choices stated as calls inside the approaches.
- G5: step 5 names "where something lives in the app" among the agent's own calls and adds a
  strike test for questions the user would only rubber-stamp.
- B5: the first message is "200 words or fewer" instead of "about 200 words".
- M1: on the several-sessions route the first message also names the decisions already visible,
  in dependency order, while still asking only one question.

## Final run

The user approved one final run (two more subagents), agreed in advance as the last whatever its
result. The candidate ran with the skill as committed (SKILL.md blob b8fa794); a fresh grader
(Sonnet 5.5, medium) scored the existing current and superpowers outputs and the new candidate
output, reshuffled (A current, B superpowers, C candidate). Evidence per score:
[scores-final.md](scores-final.md).

| Criterion | Superpowers (B) | Current (A) | Candidate (C) |
| --- | --- | --- | --- |
| B2 echo and related path | 1 | 2 | 2 |
| B3 why first, open | 1 | 1 | 2 |
| B4 current read and gaps | 1 | 2 | 2 |
| W1 buzzword probe | 1 | 2 | 2 |
| W2 one question with a guess | 1 | 2 | 1 |
| G1 numbered round | 1 | 0 | 2 |
| G3 term challenge | 1 | 2 | 2 |
| D2 approaches | 2 | 0 | 2 |
| E2 scope and anti-goals | 2 | 1 | 1 |
| E3 decisions and what is left | 2 | 1 | 2 |
| E4 approaches recorded | 2 | 1 | 2 |
| E5 observable acceptance | 1 | 2 | 2 |
| F1 spike framing | 0 | 0 | 2 |
| F2 facts and permission | 1 | 1 | 2 |
| M1 root decisions first | 1 | 2 | 1 |
| M2 decisions tracked across sessions | 0 | 0 | 2 |
| M3 outcome before technology | 1 | 0 | 2 |
| Other 20 criteria | equal across arms | equal | equal |
| Total (of 74) | 59 | 59 | 71 |

Gate: FAIL on three criteria, each by one point. The candidate is at least equal to both arms on
34 of 37 criteria and higher than both on B3, G1, F1, F2, M2 and M3. D2, B5 and G5 from the
re-run are closed. It is below on:

- W2 (1 against the current skill's 2): at s1-cp2 it asked two things. The re-run's candidate
  scored 2 on the same criterion with the same step 4, so this is run-to-run variation as far as
  one run can show.
- E2 (1 against superpowers' 2): the design had goals and an out-of-scope list but no explicit
  anti-goal, although step 7 names Anti-goals. It scored 2 in the re-run and 1 in the first run.
- M1 (1 against the current skill's 2): at s5 it asked the outcome question and said the decisions
  depend on each other, but named only one of them. The current skill's arm asked the root decision
  instead and scored 0 on M3; the candidate scored 2 on M3. Asking why first and naming the root
  decision pull against each other on this checkpoint.

No further change was made after this run, so the shipped skill is the one graded here.

Across the three gradings of unchanged outputs, the current skill's total was 60, 59 and 59 and
superpowers' 59, 57 and 59; single criteria moved by one point between graders.

## Follow-up run

After PR #20 merged, the user asked for a follow-up on E2 and M1 and approved two more subagents.
Both gaps were omissions, so the fixes are structural slots:

- E2: the restate block gains a seventh line, `Anti-goal: <what would make this a failure even if
  it works as specified>`, and the red flag and verification items name it; the worked example's
  restate gains an anti-goal. In the final run the candidate wrote its design in chat with the
  restate block as its scope section, and that block had no anti-goal slot.
- M1: on the several-sessions route the first message lists every decision already visible as a
  numbered list, root first, each later one saying which earlier one it waits on, and still asks
  one question. In the final run the candidate named a single example decision.

The candidate ran with SKILL.md blob e7d9ae0; a fresh grader (Sonnet 5.5, medium) scored it with the
existing superpowers and current outputs, reshuffled (A superpowers, B candidate, C current).
Evidence per score: [scores-followup.md](scores-followup.md).

| Criterion | Superpowers (A) | Current (C) | Candidate (B) |
| --- | --- | --- | --- |
| B2 echo and related path | 1 | 2 | 2 |
| B3 why first, open | 1 | 1 | 2 |
| B4 current read and gaps | 1 | 1 | 2 |
| W2 one question with a guess | 1 | 1 | 2 |
| G1 numbered round | 0 | 0 | 2 |
| G3 term challenge | 1 | 2 | 2 |
| D2 approaches | 2 | 0 | 2 |
| E2 scope and anti-goals | 2 | 1 | 2 |
| E3 decisions and what is left | 2 | 1 | 2 |
| E4 approaches recorded | 2 | 1 | 2 |
| E5 observable acceptance | 1 | 2 | 2 |
| F1 spike framing | 0 | 0 | 2 |
| F2 facts and permission | 1 | 1 | 2 |
| M1 root decisions first | 1 | 1 | 2 |
| M2 decisions tracked across sessions | 0 | 0 | 2 |
| M3 outcome before technology | 0 | 0 | 2 |
| Other 21 criteria | 2 each | 2 each | 2 each |
| Total (of 74) | 58 | 56 | 74 |

Gate: PASS. The candidate is at least equal to both arms on all 37 criteria and higher than both
on 9 (B3, B4, W2, G1, F1, F2, M1, M2, M3). The output shows the two fixes at work: the s1-cp5 design has an anti-goal ("a volunteer
calls someone who already returned the tool, or a member is promised a date that then proves
wrong"), and the s5 message lists six decisions with what each waits on before asking one
question. The grader named one close call: E8, where the candidate ends with "A yes lets me hand it
on to be planned and built"; it asks for approval first and names planning, so it scored 2, but a
stricter reading could give 1.

A perfect score from one run and one grader is a ceiling on this rubric, not proof of a ceiling in
use. Across the four gradings the unchanged arms' totals moved between 56 and 60, so a one or two
point difference remains within grader variance.

## Limitations

- One run per arm per grading, so a one-point gap can be noise.
- The same author wrote the fixture, the rubric and the candidate. The rubric was frozen first, but
  the candidate may still fit this fixture.
- Runners and grader come from one model family.
- Checkpoints fix the user's replies, so the trial measures single turns, not a whole live
  conversation; the earlier agent turns in each transcript were written by the author.
