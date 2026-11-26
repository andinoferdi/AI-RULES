# Scores: re-run grading

Fresh blind grading by one Sonnet 5.5 subagent at medium effort, 2026-11-26, of the existing superpowers and current outputs and the new candidate output (skill blob dc78f50, after the first round of fixes). Letters were reshuffled: A candidate, B current, C superpowers (design path neutralized as in the first grading). The mapping was revealed after grading. The grader's table follows unchanged.

# Scores

| ID | A | B | C | Evidence A | Evidence B | Evidence C |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 2 | 2 | 2 | s1-cp1: desk check in/out, Friday 22:00 `overdue.csv`, 25 volunteers; asks nothing the repo answers | s1-cp1: `/desk/*` routes, `overdue.csv` Friday 22:00 | s1-cp1: web app desk, `overdue.csv` Friday 22:00 |
| B2 | 2 | 2 | 1 | "A dashboard for the volunteers, so the 25 people..."; CSV is only overview and stale after Friday | "means a screen... instead of a weekly CSV"; recommends starting from the first case, "needs no new data" | Names the CSV but only as context, little restatement ("live overdue list" as one option) |
| B3 | 2 | 1 | 1 | One why-question (last hard shift, what did they want to know); "go ahead" is an offer, not a question | One question plus two example cases, then a second "Is that the right direction?" | One question but with a two-branch menu ("who do I call today" vs "what is on the shelf") |
| B4 | 2 | 1 | 0 | "My current reading: ... I don't yet know which moment" | States tentative reading ("my guess, not something you told me"); unknown only implied by the question | No best reading; "could mean quite different things" |
| B5 | 1 | 2 | 2 | About 280 words, slightly over 250; no code or jargon | About 230 words, no lapses | About 150 words, no lapses |
| W1 | 2 | 2 | 1 | s1-cp2: "'modern and proper' tells me what it should feel like"; asks Saturday 9:00 scene | "Charts and KPIs are a look"; asks first-minute question; charts only if a decision needs them | "Understood on the feel: modern, with charts and numbers"; says charts and KPIs "would follow" |
| W2 | 2 | 2 | 1 | One question with guess and reason (CSV frozen Friday 22:00); coordinator variant is conditional | One question, recommendation with reason (job that runs on a weekly file) | One question, no guess |
| G1 | 2 | 0 | 0 | s1-cp3: five numbered decisions, each with "I recommend", "Answer with numbers" | Single question while the hold-wait decision is open and it says that one does not depend on the first | Single closing question plus "what is wrong or missing"; proposal, not a numbered round |
| G2 | 2 | 2 | 2 | No dependent questions, nothing the repo answers | One question | One question |
| G3 | 2 | 2 | 1 | "you said 'reservation'. The library's term is Hold" | "a Hold in your glossary" | Uses lowercase "hold" without saying why |
| G4 | 2 | 2 | 2 | "As I understand it, two problems..." then separate findings and recommendations | Two numbered problems in user's terms, recommendation separate | "Here is what I heard" then "My proposal, not something you've agreed to" |
| G5 | 1 | 2 | 2 | Five questions (within limit) but Q1 "where does the list live" is a routine how it asks | One question, own calls stated | One question, own proposal stated |
| D1 | 2 | 2 | 2 | s1-cp4: refuses "whatever you think" as a decision; options A/B with pick and reason | "Delegated to me, with my reasoning" | "Item 3 was left to me, so I'll make that call" with reason |
| D2 | 0 | 0 | 2 | No approaches given; asks A/B on Q3 plus two more questions | No approaches; asks about hold-wait wording | A/B/C repository-grounded with trade-offs, recommends A, asks |
| D3 | 2 | 2 | 2 | No doc or code | No doc or code | No doc or code |
| E1 | 2 | 2 | 2 | s1-cp5: "Why now: half of the Saturday calls go to members who already returned..." | spec: "Problems this fixes: 1... phoned about a Loan they already returned... 2. cannot tell how long a Hold will take" | spec: "Intent and why" with Friday snapshot, annoyed members, Hold wait |
| E2 | 2 | 1 | 2 | Success, Out of scope list, "Anti-goals" | Goal and Out of scope present, no anti-goal | "Goals", "Non-goals", "Anti-goals" |
| E3 | 2 | 1 | 2 | "Confirmed by you / My calls / Open / Left to the builder" | "Confirmed" and "Delegated" only; no open items or left-to-builder section | "Decisions I made (please check these)", "Left to the builder", confirmed choices noted inline; no explicit open list |
| E4 | 2 | 1 | 2 | Chosen approach; CSV and texting rejected with reasons | Chosen approach only | "Approaches considered" A/B/C with chosen |
| E5 | 2 | 2 | 1 | Four checks incl. "Check in an overdue Item, reload: gone", Hold earliest date | Six acceptance checks incl. 5-day due date and "overdue, no date" | No acceptance section; only "Items disappear as soon as checkin sets returned_at" |
| E6 | 2 | 2 | 2 | Hold, Loan, Item, Tool; no "reservation" | Same, glossary-bound | Same |
| E7 | 2 | 2 | 2 | No ADR | No ADR | No ADR |
| E8 | 2 | 2 | 2 | "I won't write any code until you say yes, and then I'll go on to planning" | "match what you want to hand off for planning?" | "Do you approve... Once you approve it, I'll move on to the plan" |
| C1 | 2 | 2 | 2 | s2: "Done. The loan period is now 21 days" | s2: "Done." | s2: "Done." |
| C2 | 2 | 2 | 2 | Changed `overdue.ts` own `LOAN_DAYS` | Same | Same |
| R1 | 2 | 2 | 2 | s3: cites ADR 0001, "what changed since March 2025 that makes fees right now?" | Cites ADR 0001; asks what problem fees should solve; new ADR if reversed | Cites ADR 0001; "What's the situation that made you want fees now?" |
| R2 | 2 | 2 | 2 | `MAX_RENEWALS` one renewal, none while a Hold waits | `MAX_RENEWALS = 1`, `HOLD_WAITING` | Same |
| R3 | 2 | 2 | 2 | "a new ADR that supersedes 0001" | "record a new ADR that replaces 0001" | "a new ADR superseding the old one" |
| R4 | 2 | 2 | 2 | Root question first, no fee details | Root problem question, fee design deferred | Root question, deferred |
| F1 | 2 | 0 | 0 | s4: question, success signal (docs statement or none), "throwaway work" | Answers from repo, asks about the problem; no check proposed | Answers from repo, asks about the problem; no check proposed |
| F2 | 2 | 1 | 1 | Postmark email-only, `phone` in members; "Can I go ahead and read the documentation?" | Facts correct; runs nothing external but proposes no research | Facts correct, mentions Twilio from memory; no research |
| M1 | 1 | 2 | 1 | s5: lists findings, "settle the decisions in a few conversations" but no dependent-decision map | Root decision (stays vs home branch); "a Hold needs to know where... the next thing to decide" | Asks hold-ready question; no explicit deferral of dependents |
| M2 | 2 | 1 | 0 | "running record ... in `docs/specs/`" | "write a short design first" only | No record proposed |
| M3 | 2 | 0 | 1 | "what do you want to be true next summer?" | No outcome question; goes to item location | States goal as an assumption, invites correction; outcome not asked |
| Q1 | 2 | 2 | 2 | Plain | Plain | Plain |
| Q2 | 2 | 2 | 2 | Facts verified against fixture; renewal/CSV mismatch correct | Facts verified; unverified Postmark claim marked | Facts verified; Postmark claim marked |
| Q3 | 2 | 2 | 2 | Fits turns (cp1 slightly long) | Fits | Fits |

## Totals

| Section | Max | A | B | C |
| --- | --- | --- | --- | --- |
| s1 cp1-cp2 (B1-B5, W1-W2) | 14 | 13 | 12 | 8 |
| s1 cp3-cp4 (G1-G5, D1-D3) | 16 | 13 | 12 | 13 |
| s1 cp5 (E1-E8) | 16 | 16 | 13 | 15 |
| s2 (C1-C2) | 4 | 4 | 4 | 4 |
| s3 (R1-R4) | 8 | 8 | 8 | 8 |
| s4 (F1-F2) | 4 | 4 | 1 | 1 |
| s5 (M1-M3) | 6 | 5 | 3 | 2 |
| Quality (Q1-Q3) | 6 | 6 | 6 | 6 |
| Overall | 74 | 69 | 59 | 57 |

## Close calls

- B2 (C): names the CSV but restates little; scored 1. A scored 2 though it does not say "cheaper starting point".
- B4 (B): reading stated, unknown only implied by the question; scored 1.
- W2 (A, B): A's coordinator variant and B's closing "Does that match?" could count as a second question; scored 2.
- G5 (A): five questions is within the limit, but Q1 is a routine how; scored 1.
- E3 (C): confirmed items scattered inline and no explicit open list; scored 2 for own calls plus left-to-builder. B scored 1 for lacking open and left-to-builder.
- E5 (C): no acceptance section; vague statement only, scored 1.
- F2 (B, C): no external action taken or proposed; scored 1 (facts correct, no research or permission step).
- M3 (C): goal stated as an assumption with an invitation to correct; scored 1.
- B5 (A): about 280 words, one lapse.
