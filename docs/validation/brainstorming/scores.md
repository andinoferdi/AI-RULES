# Scores: first grading

Blind grading by one Sonnet 5.5 subagent at medium effort, 2026-11-26. Letters: A superpowers, B candidate (skill as first written, before the fixes in trial.md), C current. The mapping was revealed after grading. The grader's table follows unchanged.

# Blind trial scores

| ID | A | B | C | Evidence A | Evidence B | Evidence C |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 2 | 2 | 2 | s1-cp1: Friday 22:00 overdue.csv, web app check-in/out; asks nothing the repo answers | s1-cp1: "Friday 22:00 job that writes overdue.csv", shifts, 25 volunteers | s1-cp1: `/desk/*` routes, overdue.csv Friday 22:00 |
| B2 | 1 | 2 | 2 | No real restatement; "a dashboard could mean quite different things"; CSV mentioned only as current practice | "So the ask is a dashboard..."; guesses the overdue list "since it only arrives as a CSV once a week" | "my tentative reading is that dashboard means a screen ... instead of a weekly CSV" |
| B3 | 1 | 2 | 1 | One why-question plus a two-way mini menu ("If it's mostly who do I call... different page") | One question (what do they hunt for); the who-for point is not a second question | One question plus example menu plus a second "Is that the right direction?" |
| B4 | 1 | 2 | 2 | Unknowns implied; no stated current reading | "My current reading is ... I can't tell yet which part, or who it is for" | "tentative reading ... That is my guess, not something you told me" |
| B5 | 2 | 2 | 2 | About 150 words, no code or jargon | About 210 words, plain | About 230 words, plain |
| W1 | 1 | 2 | 2 | "Understood on the feel: modern, with charts and numbers" accepts the look, though asks a concrete situation | "I'd rather not guess at charts and KPIs yet"; Saturday 9:00 desk moment | "Charts and KPIs are a look"; shift-based question |
| W2 | 1 | 2 | 1 | One question, no guess | One question, guess (overdue CSV out of date) with reason | One question with recommendation, plus a confirm question ("Does that match...") |
| G1 | 0 | 2 | 0 | s1-cp3: one question only, no recommendation, while other decisions open | Four numbered decisions each with recommendation, "Yes?" | One question only (live call list), hold-wait deferred; recommendation present |
| G2 | 2 | 2 | 2 | Single question, independent, nothing the repo answers | Four independent decisions, no repo facts asked | Single question |
| G3 | 1 | 2 | 2 | Says "hold" without flagging the reservation term | "the project calls that a Hold, not a reservation, so I'll use Hold" | "a member's place in the queue ... is a Hold in your glossary" |
| G4 | 2 | 2 | 2 | "Here is what I heard" then "My proposal, not something you've agreed to" | "As I understand it" two problems, then separate recommended decisions | Two problems played back, then "My recommendation" |
| G5 | 2 | 2 | 2 | One question | Four product decisions; routine choices stated as own calls | One question |
| D1 | 2 | 2 | 2 | "Item 3 was left to me, so I'll make that call ... An estimate that turns out wrong becomes a promise" | Two options, "This is my pick"; refuses to decide silently | "Delegated to me, with my reasoning" |
| D2 | 2 | 0 | 0 | s1-cp4: A/B/C with trade-offs, recommends A, asks | s1-cp4: no approaches, asks two more questions | s1-cp4: no approaches, asks one more question |
| D3 | 2 | 2 | 2 | No doc or code | No doc or code | No doc or code |
| E1 | 2 | 2 | 2 | Design doc "Intent and why": Saturday calls to returned tools, cannot say how long a Hold will take | Message: "Why now: calls reach members who already returned their tool, desk cannot answer when it will be back" | Goal section lists both problems |
| E2 | 2 | 1 | 1 | Goals, Non-goals, Anti-goals sections | Goals and out-of-scope list; no anti-goal | Goal and out-of-scope list; no anti-goal |
| E3 | 2 | 2 | 1 | "Decisions I made (please check these)", "Left to the builder", agreed items inline | "Confirmed by you", "My calls", "Open" sections; no builder section | "Confirmed" and "Delegated to the agent"; no open items or builder section |
| E4 | 2 | 1 | 1 | "Approaches considered" with A chosen and trade-offs | Only "approach A" named | "Chosen approach (option A)" only |
| E5 | 1 | 2 | 2 | No acceptance section; only "disappear as soon as checkin sets returned_at" | "return a loan at 9:05 and it is gone ... two Holds shows two different dates" | "Acceptance checks" 1-6 incl. disappears after check-in |
| E6 | 2 | 2 | 2 | Hold, Member, Item, Tool, Loan consistent | Hold, Tool, Loan consistent | Bolded glossary terms consistent |
| E7 | 2 | 2 | 2 | No ADR (only cites ADR 0001) | No ADR | No ADR |
| E8 | 2 | 1 | 2 | "Do you approve the design as written... Once you approve it, I'll move on to the plan." | No document written; asks a further question then "I'll treat the design as approved, and then planning and building can start" | "Does this design match what you want to hand off for planning?" |
| C1 | 2 | 2 | 2 | s2: "Done." no questions | "clear request, so I made the change" | "Done." |
| C2 | 2 | 2 | 2 | overdue.ts LOAN_DAYS 21 ("keep in sync") | overdue.ts changed to 21 | overdue.ts changed to 21 |
| R1 | 2 | 2 | 2 | ADR 0001, "would reverse that decision", asks what made you want fees now | ADR cited, "What has changed since March 2025" | ADR cited, "What is the late-return problem you want fees to solve?" |
| R2 | 2 | 2 | 2 | "MAX_RENEWALS = 1, and none while another member has a hold" | same | same (`HOLD_WAITING`) |
| R3 | 2 | 0 | 2 | "a new ADR superseding the old one" | Only "change on purpose"; no ADR mention | "we record a new ADR that replaces 0001" |
| R4 | 2 | 2 | 2 | Asks why now; fee details deferred | Same | Same; notes fee design later |
| F1 | 0 | 0 | 0 | s4: answers from knowledge, asks why; no throwaway check or success signal | Same | Same ("check that before you pick a vendor" is advice, not a labelled check) |
| F2 | 2 | 2 | 2 | Postmark email only (marked "as far as I know"), phone column, read-only | Postmark email.ts, hold flow, phone column, read-only | email.ts, config/default.json, m.phone; read-only |
| M1 | 1 | 2 | 2 | One root question but folds hold-pickup into it; no explicit deferral | Item location first; "Then a Hold ... becomes a question of which branch" | Item location first; hold pickup "the next thing to decide" |
| M2 | 0 | 0 | 1 | No record proposed | No record proposed | "write a short design first and plan from that" |
| M3 | 1 | 0 | 0 | "The goal is that members can use either branch freely ... what's wrong or missing" | No outcome question | No outcome question |
| Q1 | 2 | 2 | 2 | Plain | Plain | Plain |
| Q2 | 2 | 1 | 2 | Facts correct; Postmark claim marked as unverified | s4: Postmark "can't send texts" stated flat, unmarked; other facts correct | Facts correct; Postmark claim marked unverified |
| Q3 | 2 | 1 | 2 | Lengths fit; full design doc | s1-cp5 too thin: no document though user said "write it up" | Lengths fit; full design doc |

## Totals

| Section | A | B | C | Max |
| --- | --- | --- | --- | --- |
| B1-B5 | 7 | 10 | 9 | 10 |
| W1-W2 | 2 | 4 | 3 | 4 |
| G1-G5 | 7 | 10 | 8 | 10 |
| D1-D3 | 6 | 4 | 4 | 6 |
| E1-E8 | 15 | 13 | 13 | 16 |
| C1-C2 | 4 | 4 | 4 | 4 |
| R1-R4 | 8 | 6 | 8 | 8 |
| F1-F2 | 2 | 2 | 2 | 4 |
| M1-M3 | 2 | 2 | 3 | 6 |
| Q1-Q3 | 6 | 5 | 6 | 6 |
| Total | 59 | 60 | 60 | 74 |

## Close calls

- G1 C: one question deliberately sequencing two problems, with a recommendation; scored 0 per the rubric (one question while several independent decisions are open). A 1 is arguable.
- F1 all: nobody framed a throwaway feasibility check; A and C told the user to verify Postmark docs, which a lenient reading could score 1.
- B's s1-cp5 message was counted as the design document; if a real file is required, B's E1-E5 and E8 drop.
- E3 A: confirmed items are inline, not a section; scored 2 since own calls and builder list are explicit.
- E8 B: asks for review but says it will treat the design as approved after one answer; 1.
- W2 C and B3 C: the extra confirm question counted as a second question.
- Q2 B: Postmark capability stated without marking it unchecked; 1.
- M2 C: a short design before planning is a weak durable record; 1.
- B2 A: no clear restatement; 1.
