# Scores: final grading

Fresh blind grading by one Sonnet 5.5 subagent at medium effort, 2026-11-26, of the existing current and superpowers outputs and the final candidate output (skill blob b8fa794, after the second round of fixes). Letters were reshuffled: A current, B superpowers (design path neutralized as before), C candidate. The mapping was revealed after grading. The grader's table follows unchanged.

# Scores: brainstorming trial (grade3)

| ID | A | B | C | Evidence A | Evidence B | Evidence C |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | 2 | 2 | 2 | s1-cp1: `/desk/*`, "`overdue.csv`... every Friday at 22:00", Sat/Wed shifts; asks nothing repo answers | s1-cp1: desk web app, "overdue.csv... every Friday at 22:00"; nothing repo-answerable asked | s1-cp1: desk check in/out, Friday 22:00 csv, "Nothing else gives volunteers a summary view" |
| B2 | 2 | 1 | 2 | "my tentative reading is that dashboard means a screen... instead of a weekly CSV" | Names CSV and "live overdue list" but no restatement of the request | "You want a dashboard for the volunteers"; CSV is up to a week old, live list instead |
| B3 | 1 | 1 | 2 | One why-question with two example answers, then a second confirm question ("Is that the right direction") | One question plus a two-page menu and "dive in" offer | One why-question ("a moment at the desk... wished they could see") |
| B4 | 2 | 1 | 2 | "my tentative reading... That is my guess"; unknown asked | No stated best reading, only "could mean quite different things" | "My guess is... a live list"; "If my guess is off, tell me" |
| B5 | 2 | 2 | 2 | No code, no jargon, ~190 words | Short, plain | Plain, ~190 words |
| W1 | 2 | 1 | 2 | "Charts and KPIs are a look... pick the look after"; "scalable is not the constraint"; Saturday desk | "Understood on the feel: modern, with charts and numbers"; says charts and KPIs would follow | Does not guess charts; Saturday 9:00 desk scene |
| W2 | 2 | 1 | 1 | Question with guess + reason (weekly file); trailing "Does that match" is a confirm of the guess | Question, no guess | Guess given, but two asks ("first thing see/what do" plus "last time... I wish X") and "Which of these" |
| G1 | 0 | 1 | 2 | One question only (live call list page) while hold-wait, audience decisions stay open | Two asks, no numbering, no per-question recommendation | Four numbered decisions each with "I recommend" |
| G2 | 2 | 2 | 2 | Single question | Two independent questions | Four independent decisions, none repo-answerable |
| G3 | 2 | 1 | 2 | "a Hold in your glossary" | Uses "hold" without noting the term swap | "your word was 'reservation'; the glossary uses Hold" |
| G4 | 2 | 2 | 2 | Numbered playback, then "I found", "My recommendation" | "Here is what I heard"; "My proposal, not something you've agreed to" | "What you want fixed" vs "My calls" |
| G5 | 2 | 2 | 2 | 1 question | 2 questions | 4 questions, routine choices stated as own calls |
| D1 | 2 | 2 | 2 | "Delegated to me, with my reasoning" | "I'll make that call... estimates go to volunteers only" with reason | "that is my call" with reason |
| D2 | 0 | 2 | 2 | s1-cp4 is a status recap only; no approaches offered | A/B/C with trade-offs, recommends A, asks | A/B/C with trade-offs, recommends A, asks |
| D3 | 2 | 2 | 2 | No files | No files | No files |
| E1 | 2 | 2 | 2 | spec: "Members are phoned about a Loan they already returned"; Hold wait | "Intent and why": Friday snapshot, no way to say Hold wait | "Why now: half of the Saturday calls go to people who already returned" |
| E2 | 1 | 2 | 1 | Goal and Out of scope; no anti-goal | Goals, Non-goals, Anti-goals sections | Success and Out of scope; no explicit anti-goal (only "never an old list that looks real") |
| E3 | 1 | 2 | 2 | Confirmed and Delegated; no open items or builder-left | Confirmed, "Decisions I made", "Left to the builder" | Confirmed, My calls, "Open: none"; no explicit builder-left |
| E4 | 1 | 2 | 2 | "Chosen approach (option A)" only | Options A/B/C, chosen A | "I rejected... CSV... and a separate dashboard, because..." |
| E5 | 2 | 1 | 2 | Six checks, e.g. loan disappears on next load after check-in; 2 Holds + due in 5 days | No acceptance section, only "Items disappear as soon as checkin sets returned_at" | Four checks, e.g. return then reload, Mar 3/Mar 10 example |
| E6 | 2 | 2 | 2 | Hold, Loan, Tool, Item, Member; "reservation" only to correct | Hold, Member, Item, Tool, Volunteer | Loan, Hold, Tool, Item, Overdue |
| E7 | 2 | 2 | 2 | No ADR | No ADR | No ADR |
| E8 | 2 | 2 | 2 | "match what you want to hand off for planning?" | "Once you approve it, I'll move on to the plan" | "I'll turn it into a step-by-step plan. I won't start writing code" |
| C1 | 2 | 2 | 2 | s2: done, no questions | Done, no questions | Done, no questions |
| C2 | 2 | 2 | 2 | Changed overdue.ts LOAN_DAYS to 21 | Same | Same |
| R1 | 2 | 2 | 2 | ADR 0001; "What is the late-return problem you want fees to solve?" | ADR 0001; "What's the situation that made you want fees now?" | "what has changed since March 2025" |
| R2 | 2 | 2 | 2 | `MAX_RENEWALS = 1`, `HOLD_WAITING` | Same | Same |
| R3 | 2 | 2 | 2 | "record a new ADR that replaces 0001" | "a new ADR superseding the old one" | "new decision record that supersedes this one" |
| R4 | 2 | 2 | 2 | Root first, fee design deferred | Root question; offers to dive in | Root question explicitly "not the fee amounts" |
| F1 | 0 | 0 | 2 | No check, no success signal; asks what problem | "check that if it matters"; no throwaway check | "Throwaway check: Question / What answers it / Cheapest check" |
| F2 | 1 | 1 | 2 | Postmark email-only facts; no research or permission ask | Postmark/phone facts; no permission step | Postmark facts; read-only check, "Can I go ahead and look it up?" |
| M1 | 2 | 1 | 1 | Names return-location, home branch, Hold pickup; asks only the first, "next thing to decide" | Lists many issues, asks only hold pickup, no explicit deferral | "decisions depend on each other", asks the reason first; only one example decision named |
| M2 | 0 | 0 | 2 | Design first, no decision record | None | "record... in `docs/specs/second-branch-decisions.md`" over a few sessions |
| M3 | 0 | 1 | 2 | Opens with where returned items go | States "The goal is... either branch freely" and invites correction, then asks design | "What do you expect members to gain from returning at a different branch?" |
| Q1 | 2 | 2 | 2 | Plain throughout | Plain | Plain |
| Q2 | 2 | 2 | 2 | Facts verified; unverified claims marked | Facts verified; "as far as I know" | Facts verified; "From memory... unverified" |
| Q3 | 2 | 2 | 2 | Lengths fit | Lengths fit | Lengths fit |

## Totals

| Section | Max | A | B | C |
| --- | --- | --- | --- | --- |
| B (s1-cp1) | 10 | 9 | 7 | 10 |
| W | 4 | 4 | 2 | 3 |
| G | 10 | 8 | 8 | 10 |
| D | 6 | 4 | 6 | 6 |
| E | 16 | 13 | 15 | 15 |
| C | 4 | 4 | 4 | 4 |
| R | 8 | 8 | 8 | 8 |
| F | 4 | 1 | 1 | 4 |
| M | 6 | 2 | 2 | 5 |
| Q | 6 | 6 | 6 | 6 |
| Total | 74 | 59 | 59 | 71 |

## Close calls

- B3 A and B: one-point calls; A's second confirm question and B's menu could each be 0 or 2.
- W2 A vs C: A's trailing "Does that match" counted as confirming the guess (2); C's extra alternative asks scored 1.
- G1 A: scored 0 (one question while independent decisions remain); could be 1 as it gave a recommendation.
- G1 B: 1 vs 0 depending on whether the missing per-question recommendation counts.
- E2 C: anti-goal only implicit; E3 C: no explicit "left to builder"; both could be 1 or 2.
- E3 B: no open-items section (none open) but scored 2.
- M1: all three are close; C names only one example decision but defers explicitly.
- F2 A/B: no external action at all, so "permission" half is moot; scored 1.
