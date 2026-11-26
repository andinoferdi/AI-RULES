# Scores: follow-up grading

Fresh blind grading by one Sonnet 5.5 subagent at medium effort, 2026-11-26, of the existing superpowers and current outputs and the follow-up candidate output (skill blob e7d9ae0, after the E2 and M1 fixes). Letters were reshuffled: A superpowers (design path neutralized as before), B candidate, C current. The mapping was revealed after grading. The grader's table follows unchanged.

# Scores (blind trial, rubric frozen 2026-11-26)

| ID | A | B | C | Evidence A | Evidence B | Evidence C |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 2 | 2 | 2 | A/s1-cp1: web app check in/out, "overdue.csv ... every Friday at 22:00"; asks nothing repo answers | B/s1-cp1: `web/routes.ts`, Friday 22:00 job, no screen summarises anything | C/s1-cp1: `/desk/*` routes, "overdue.csv ... every Friday at 22:00" |
| B2 | 1 | 2 | 2 | A: names the CSV and "live overdue list" but never restates the request | B: "You want a screen for the desk volunteers..."; CSV is "only volunteer-facing report" | C: tentative reading "instead of a weekly CSV" |
| B3 | 1 | 2 | 1 | A: one why-question plus a two-branch menu ("who do I call today" vs "what's on the shelf") | B: one question, "What is the moment in a volunteer shift where they wish they had this?" | C: question plus example menu and a second "Is that the right direction?" |
| B4 | 1 | 2 | 1 | A: no stated reading, only "could mean quite different things" | B: "My current reading is...", "I don't know what yet" | C: reading stated ("my guess"), unknowns only implied by the question |
| B5 | 2 | 2 | 2 | A: ~125 words, no code or jargon | B: ~210 words, none | C: ~190 words, none |
| W1 | 2 | 2 | 2 | A/s1-cp2: asks about the last time something went wrong, charts "follow from it" | B/s1-cp2: "Picture Saturday at 9:00" | C/s1-cp2: "Charts and KPIs are a look"; asks about a shift |
| W2 | 1 | 2 | 1 | A: one question, no guess | B: one question with guess ("less about charts") and size-based reason | C: guess plus a second confirming question ("Does that match...") |
| G1 | 0 | 2 | 0 | A/s1-cp3: one question only, no numbering or recommendation | B/s1-cp3: three numbered decisions, each "I recommend... Yes, or" | C/s1-cp3: one question ("Is a live call list page...") while the Hold-date decision is deferred |
| G2 | 2 | 2 | 2 | A: single non-repo question | B: three independent, non-repo questions | C: single question |
| G3 | 1 | 2 | 2 | A: says "hold" without explaining "reservation" | B: "I'll call that... a Hold, ... (`GLOSSARY.md`); you said 'reservation'" | C: "a member's place in the queue ... is a Hold in your glossary" |
| G4 | 2 | 2 | 2 | A: "Here is what I heard" then "My proposal, not something you've agreed to" | B: "What I heard" / "My own calls" | C: numbered problems then "My recommendation" (less clearly separated) |
| G5 | 2 | 2 | 2 | A: 1 question | B: 3 questions, own calls stated | C: 1 question |
| D1 | 2 | 2 | 2 | A/s1-cp4: "Item 3 was left to me, so I'll make that call" plus reason | B: "This one is mine, not yours" plus reason | C: "Delegated to me, with my reasoning" |
| D2 | 2 | 2 | 0 | A: A/B/C with trade-offs, recommends A, asks | B: A/B/C with reasons, recommends A, asks | C/s1-cp4: no approaches; recaps and asks about date wording |
| D3 | 2 | 2 | 2 | A: no files or code | B: none | C: none |
| E1 | 2 | 2 | 2 | A doc: Saturday calls to members who already returned, no hold wait | B: "Why now: half the Saturday calls go to people who already returned the tool" | C doc: Problems 1 and 2 in user terms |
| E2 | 2 | 2 | 1 | A: Goals, Non-goals, Anti-goals sections | B: Outcome, Out of scope, Anti-goal | C: Goal and Out of scope, no anti-goal |
| E3 | 2 | 2 | 1 | A: "Chosen by the user", "Decisions I made", "Left to the builder" | B: Confirmed / My calls / Open / Left to builder | C: Confirmed and Delegated only; no open items or builder list |
| E4 | 2 | 2 | 1 | A: A chosen, B and C with trade-offs | B: B and C rejected with reasons | C: "Chosen approach (option A)" only |
| E5 | 1 | 2 | 2 | A: "Items disappear as soon as checkin sets returned_at"; no acceptance section | B: five checks incl. 08:30 return gone at 09:00 | C: six checks incl. renewed loan not listed |
| E6 | 2 | 2 | 2 | A: Hold, Member, Item, Tool, Loan | B: lists terms per GLOSSARY | C: bold glossary terms |
| E7 | 2 | 2 | 2 | No new ADR | No new ADR | No new ADR |
| E8 | 2 | 2 | 2 | A: "Do you approve the design... Once you approve it, I'll move on to the plan" | B: "A yes lets me hand it on to be planned and built" | C: "hand it to planning"; asks match |
| C1 | 2 | 2 | 2 | A/s2: edits, no questions | B/s2: edits, no questions | C/s2: edits, no questions |
| C2 | 2 | 2 | 2 | A: changed `overdue.ts` LOAN_DAYS | B: same | C: same |
| R1 | 2 | 2 | 2 | A/s3: ADR 0001 reversal, "situation that made you want fees now" | B: "what has changed since March" | C: "if you decide to reverse the ADR... what is the late-return problem" |
| R2 | 2 | 2 | 2 | A: `MAX_RENEWALS = 1`, none with hold | B: same | C: same |
| R3 | 2 | 2 | 2 | A: "new ADR superseding the old one" | B: "new decision record that supersedes" | C: "record a new ADR that replaces 0001" |
| R4 | 2 | 2 | 2 | A: root question first | B: root question first | C: root question first |
| F1 | 0 | 2 | 0 | A/s4: no check proposed, asks about the problem | B/s4: question, success signal (clear yes/no in docs), "throwaway lookup" | C/s4: states expectation, no check, asks about the problem |
| F2 | 1 | 2 | 1 | A: Postmark email only (unverified), phone column; runs/asks nothing external | B: facts plus "Shall I run the docs check?" | C: `email.ts`, `config/default.json`, `m.phone`; no external ask |
| M1 | 1 | 2 | 1 | A/s5: one question, dependencies not laid out | B/s5: six decisions with "Waits on" | C/s5: one root decision, mentions next one only |
| M2 | 0 | 2 | 0 | A: none | B: "running record ... `docs/specs/second-branch-decisions.md`" | C: short design only, no session record |
| M3 | 0 | 2 | 0 | A: asks hold-pickup mechanics | B: "Why do you want cross-branch returns?" | C: asks where returned items go |
| Q1 | 2 | 2 | 2 | Plain | Plain | Plain |
| Q2 | 2 | 2 | 2 | Facts check against fixture; unverified Postmark marked | Same | Same |
| Q3 | 2 | 2 | 2 | Fits | Fits | Fits |

## Totals (max 74)

| Section | Max | A | B | C |
| --- | --- | --- | --- | --- |
| B1-B5 | 10 | 7 | 10 | 8 |
| W1-W2 | 4 | 3 | 4 | 3 |
| G1-G5 | 10 | 7 | 10 | 8 |
| D1-D3 | 6 | 6 | 6 | 4 |
| E1-E8 | 16 | 15 | 16 | 13 |
| C1-C2 | 4 | 4 | 4 | 4 |
| R1-R4 | 8 | 8 | 8 | 8 |
| F1-F2 | 4 | 1 | 4 | 1 |
| M1-M3 | 6 | 1 | 6 | 1 |
| Q1-Q3 | 6 | 6 | 6 | 6 |
| **Total** | 74 | **58** | **74** | **56** |

## Close calls

- B2 (A): names the CSV and a live overdue list but does not restate the request; 1 vs 2.
- B4 (C): reading stated, unknowns only implied; scored 1.
- G1 (C): sequencing one decision at a time was deliberate, but the rubric gives 0 for one question when several independent decisions are open.
- G4 (C): playback and own proposals are interleaved; scored 2.
- D2 (C): cp4 recaps and asks about wording instead of offering approaches; 0.
- E8 (B): "as I will build it" and "planned and built" could be read as scheduling the build; scored 2 since it names planning and asks for approval first.
- F1/F2 (A, C): neither runs anything external nor asks; F2 scored 1 rather than 2 because no read-only research or explicit permission question appears.
- M1 (A, C): A and C name one root decision but do not lay out dependencies; 1.
