# Comparison trial: API and interface design

Run on 2026-11-25 and 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored
against the [rubric](rubric.md), which was frozen (commit f372011) before the candidate was
written.

## Setup

- Arms: Addy Osmani's `api-and-interface-design` (addyosmani/agent-skills commit 63128d0);
  the current `andino-api-and-interface-design` (AI-RULES main at 83e0c3e); the candidate
  rewrite (branch `skill/api-and-interface-design-upgrade`, skill folder as it stood before
  the Q1 fix described below).
- Runners: three Claude Code subagents, Sonnet 5.5 at medium effort, one per arm. The two
  baseline arms ran first; the candidate ran after the rewrite. Each got the rubric's run
  prompt, its own skill copy and its own run folder, and was told to read nothing else and to
  use no skills, slash commands or subagents.
- Blinding: outputs were shuffled to letters (A current, B candidate, C Addy) and checked for
  mentions of the guidance used (none found). The grader, one Sonnet 5.5 subagent at medium
  effort, saw only the rubric, the fixture and the three output folders. Its evidence per
  score is in [scores.md](scores.md).

## Scores

| Criterion | Addy (C) | Current (A) | Candidate (B) |
| --- | --- | --- | --- |
| H7 mobile compatibility | 1 | 2 | 2 |
| H10 boundary validation | 1 | 1 | 2 |
| H11 webhook delivery | 1 | 2 | 2 |
| Q1 contract files | 1 | 2 | 1 |
| Q2 consumer impact | 1 | 2 | 2 |
| Other 22 criteria | 2 each | 2 each | 2 each |
| Task 1 (H1-H13) | 23 | 25 | 26 |
| Task 2 (M1-M6) | 12 | 12 | 12 |
| Task 3 (P1-P3) | 6 | 6 | 6 |
| Quality (Q1-Q5) | 8 | 10 | 9 |
| Total (of 54) | 49 | 53 | 53 |

Gate (candidate at least equal to Addy and to the current skill on every criterion):

- Against Addy: PASS. Equal or higher on all 27 criteria; higher on H7, H10, H11 and Q2.
- Against the current skill: FAIL on Q1 (1 versus 2); higher on H10; equal elsewhere.

## The Q1 failure and the fix

The candidate output defined `PaymentId` and `RefundId` brands but kept `Payment.id` as a
plain `number` and `RefundInput.paymentId` as a plain `string`, so the IDs stayed
interchangeable. The current skill's checklist had two items the rewrite dropped when it
merged its checklist with Addy's: "Branded Types for Identifiers" and "Discriminated Unions
for States". That broke preservation-ledger row P25 in the execution plan.

Fix applied after grading: procedure step 3 now says to use the identifier's type everywhere
the identifier appears (inputs, outputs, signatures, SDK methods, parsed values) and that a
brand can wrap a numeric wire type; the verification checklist regains both items; the
example adds a numeric brand. The fix restores dropped guidance.

## Re-run after the fix

On 2026-11-26 the candidate arm ran again with the fixed skill (branch commit fd8fda9), same
prompt, fixture, model and effort. A fresh grader (Sonnet 5.5, medium) scored the existing
Addy and current outputs and the new candidate output, reshuffled (A Addy, B current,
C candidate). Evidence per score: [scores-rerun.md](scores-rerun.md).

| Criterion | Addy (A) | Current (B) | Candidate (C) |
| --- | --- | --- | --- |
| H10 boundary validation | 1 | 2 | 2 |
| H11 webhook delivery | 1 | 2 | 2 |
| Q1 contract files | 1 | 1 | 2 |
| Q2 consumer impact | 1 | 2 | 2 |
| Other 23 criteria | 2 each | 2 each | 2 each |
| Total (of 54) | 50 | 53 | 54 |

Gate: PASS. The candidate is at least equal to both other arms on every criterion and higher
than the current skill on Q1, where only the candidate carried branded payment, refund and
customer ids through its types, handlers and events.

The two gradings disagree on the same unchanged outputs: the current skill's Q1 went from 2 to
1 and its H10 from 1 to 2, and Addy's H7 from 1 to 2. That is grader variance on one-point
judgement calls, which both graders flagged; it is the size of noise to expect here.

## Reading the result

- The candidate beat Addy on four criteria and tied on the rest. The current skill also beat
  Addy on four, so on this fixture both Andino versions are ahead of Addy's skill.
- The candidate improved on the current skill where the rewrite added guidance: H10 (webhook
  event shape parsed after the signature check, internal re-validation removed).
- The first candidate lost Q1 because the rewrite dropped a checklist item, which is the
  regression risk the council warned about. Restoring the item closed it in the re-run.
- The candidate answers a reused key with a different body with 422 (IETF draft -09); the
  current skill's arm answered 409. The rubric accepts both, so this does not show in the scores.

## Limitations

- One run per arm per grading, so a one-point gap can be noise; the two gradings moved three
  scores on unchanged outputs.
- The same author wrote the fixture, the rubric and the candidate. The rubric was frozen first,
  but the candidate may still fit this fixture.
- Runners and grader come from one model family.
- No unguided control arm was run; only the three skill arms were approved.
- The rubric scores design documents and code sketches. Nothing in the outputs was compiled
  or executed.
