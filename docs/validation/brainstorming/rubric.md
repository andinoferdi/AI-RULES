# Comparison rubric: brainstorming

Frozen on 2026-11-26 before any change to the candidate skill. Three arms run the same prompt on
the same fixture: Jesse Vincent's superpowers `brainstorming` (obra/superpowers commit 22f0b46), the
current `andino-brainstorming` (AI-RULES main at 49ad00b) and the candidate rewrite. A grader who
sees only this rubric, the fixture and the three outputs (labelled A, B, C) scores every criterion.

The criteria come from the behaviours of four reference skills and of the current skill; the
source of each is in brackets: Addy Osmani's `interview-me` (agent-skills 1d32b88), Matt Pocock's
`grilling` (skills 7739eae) and `grill-with-docs` with `domain-modeling` (447ca70, 2b7ab8c),
superpowers `brainstorming`, and the current Andino skill.

## Run setup

Brainstorming is a conversation, so each arm answers fixed checkpoints instead of a live user. A
checkpoint is the conversation so far; the arm writes only its next message. Every arm sees the
same transcripts, so earlier agent turns favour no arm.

Each arm gets its own run folder with a copy of `fixture/repo/` at `<RUN_DIR>/repo/`, a copy of
`fixture/checkpoints/` at `<RUN_DIR>/checkpoints/`, and its own copy of the skill folder at
`<SKILL_DIR>`. Runners use no other skill, slash command or subagent and read nothing outside
`<SKILL_DIR>` and `<RUN_DIR>`.

Run prompt, identical for every arm (`<SKILL_DIR>` and `<RUN_DIR>` substituted):

> Read `<SKILL_DIR>/SKILL.md` first and follow it, opening any file it points you to when its
> condition applies. You are the coding agent working in the repository at `<RUN_DIR>/repo/`, which
> you may read. `<RUN_DIR>/checkpoints/` holds nine conversation checkpoints. Each file is the
> conversation so far between a user and you; the user's last message is at the end. Process the
> checkpoints in file-name order and open each one only when you start it. Treat each as its own
> conversation. For each, write the exact next message you would send that user to
> `<RUN_DIR>/out/<checkpoint id>.md` (for example `out/s1-cp1.md`). If at that point you would
> create or change files, write them under `<RUN_DIR>/out/<checkpoint id>-files/` at their
> repository-relative path instead of touching `repo/`, and say in your message what you created.
> Do not mention which guidance you used. Touch nothing outside `<RUN_DIR>`.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote). Score what the output
says or does; a criterion the output never addresses scores 0 unless the row says otherwise. Check
claimed repository facts against `fixture/repo/`.

### s1: a vague request, five checkpoints

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| B1 | Looks before asking (s1-cp1) [all] | Cites at least two relevant repository facts, including the Friday `overdue.csv` export, and asks nothing the repository answers | One relevant fact, or asks one thing the repository answers | No repository facts, or asks what the code already shows |
| B2 | Echo and related path (s1-cp1) [superpowers] | Restates the request in its own words and points out the existing overdue export (or the desk flow) as related work or a cheaper starting point | Restates the request without connecting it to existing work, or names the export without saying why it matters | Neither |
| B3 | Why first, open (s1-cp1) [interview-me, superpowers] | Exactly one question, about what volunteers need to do or decide (the why), with no menu of options or features | One why-question plus a short menu, or two questions | Several questions, a feature menu, or no why-question |
| B4 | Current read and gaps (s1-cp1) [interview-me] | States its current best reading of the request and what is still unknown | Only one of the two | Neither |
| B5 | No build, no ceremony (s1-cp1) [superpowers, current] | No code or files; no method jargon (path names, "frontier", "protocol", confidence percentages); about 250 words or fewer | One lapse | Starts building, or several lapses |
| W1 | Buzzword probe (s1-cp2) [interview-me] | Does not accept "modern", "scalable", "best practice", "KPIs" as requirements; asks what they would actually want or about a concrete situation (for example the Saturday desk) | Questions the buzzwords but still proposes charts or KPIs as the plan | Accepts them and proposes metrics, charts or a stack |
| W2 | One question with a guess (s1-cp2) [interview-me] | One question with its best guess and the reason for the guess | One question without a guess, or a guess with two questions | Several questions |
| G1 | Numbered round (s1-cp3) [grilling, user decision] | The open decisions that do not depend on each other are asked together, numbered, each with a recommendation, worded so that "yes" accepts it | Several decisions asked, but without recommendations or numbering | One question only while several independent decisions are open, or questions without any recommendation |
| G2 | Dependency discipline (s1-cp3) [grilling] | No question in the round depends on another one in the same round, and none asks a fact the repository answers (stack, database, current schedule) | One such question | Two or more |
| G3 | Term challenge (s1-cp3) [domain-modeling] | Notices that "reservation" is a Hold in `GLOSSARY.md` and uses or proposes Hold | Uses Hold without saying why, or mentions the glossary without resolving the term | Uses "reservation" uncritically |
| G4 | Playback of the settled part (s1-cp3) [superpowers] | Plays back the why (stale Friday list, calls about returned tools, no return date for a Hold) in the user's words and keeps its own proposals visibly separate | Plays back without separating the user's words from proposals | No playback |
| G5 | Own calls, few questions (s1-cp3) [superpowers] | At most five questions; choices the agent can make itself (file locations, routine how) are stated as its calls, not asked | Six or more questions, or asks one routine choice | Asks the user routine implementation choices |
| D1 | "Whatever you think" (s1-cp4) [interview-me, current] | For decision 3, either makes the call explicitly as its own with a reason, or puts back two concrete options with a pick; never treats it as the user's agreement | Makes a call without saying it is the agent's, or without a reason | Ignores decision 3 or records it as the user's choice |
| D2 | Approaches (s1-cp4) [superpowers] | Two or three repository-grounded ways to build it, each with a trade-off, one recommended with a reason, then asks which | Approaches without trade-offs or without a recommendation | A single approach presented as the plan, or none |
| D3 | Not yet writing or building (s1-cp4) [superpowers] | No design document, code or files at this point | A design draft before the approach is chosen | Code or scaffolding |
| E1 | Intent and why (s1-cp5) [superpowers, interview-me] | The design document states who it is for and why (Saturday calls to members who already returned tools; no return date for a Hold) in the user's terms | Intent stated without the why | Missing |
| E2 | Scope (s1-cp5) [superpowers, interview-me] | Goals, an explicit out-of-scope list (for example the members' Holds page, SMS) and at least one anti-goal (what would make it fail even if it works) | Two of the three | One or none |
| E3 | Decisions and what is left (s1-cp5) [superpowers, current] | Separates what the user confirmed from the agent's own calls (including decision 3) and from open items, and says what is left to the builder | Two of the three | Decisions not separated |
| E4 | Approaches recorded (s1-cp5) [superpowers] | The considered approaches with the chosen one and why | Chosen approach only | Missing |
| E5 | Observable acceptance (s1-cp5) [current] | Checks a builder can test, for example an item returned at 9:00 is gone from the call list when a volunteer looks at 9:05, and a tool with a Hold shows the earliest due date | Acceptance stated vaguely | None |
| E6 | Domain language (s1-cp5) [domain-modeling] | Uses Hold, Loan, Item and Member consistently with `GLOSSARY.md`; no "reservation" | One inconsistency | Several, or "reservation" as the term |
| E7 | ADR proportion (s1-cp5) [domain-modeling] | No ADR for this reversible feature, or an ADR justified as hard to reverse, surprising and a real trade-off | An ADR without that justification | A heavy ADR set or several ADRs for routine choices |
| E8 | Gate and next step (s1-cp5) [superpowers, interview-me, current] | The message asks the user to review or approve the document before building and names the next step (an implementation plan); no code written | Asks for review but starts or schedules building in the same message, or names no next step | Starts building |

### s2 to s5: one checkpoint each

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| C1 | Clear request, no interview (s2) [superpowers, current] | Makes the change (or states exactly what it changes) without asking questions about settled points | Makes it but asks an unnecessary question | Starts an interview or asks for confirmation of settled points |
| C2 | Second constant (s2) [all: look before you ask] | Notices that `src/reports/overdue.ts` has its own `LOAN_DAYS = 14` and changes or flags it | Mentions that other places may use 14 without finding it | Misses it |
| R1 | Recorded decision (s3) [domain-modeling, current] | Points out `docs/adr/0001-no-late-fees.md` and asks whether to reverse it and why now, before designing fees | Mentions the ADR without asking about reversing it | Designs fees without mentioning it |
| R2 | Claim against the code (s3) [domain-modeling] | Points out that the code allows one renewal and none while a Hold waits, contrary to "renew as often as they like" | Mentions renewal limits vaguely | Accepts the claim |
| R3 | ADR offered properly (s3) [domain-modeling] | Says a superseding ADR should record the change if they go ahead | Mentions documentation in general | Nothing, or writes a fee design first |
| R4 | Root question first (s3) [interview-me, grilling] | Asks the root question (whether to reverse the no-fee decision, or why now) and defers fee details | Root question asked together with fee-detail questions | Only fee-detail questions |
| F1 | Spike framing (s4) [current, superpowers] | Treats it as a feasibility question: states the question, a success signal and a short throwaway check (for example the provider's SMS support or a test message), labelled throwaway | A check proposed without a success signal or without the throwaway label | A full design interview, or builds SMS sending |
| F2 | Facts and permission (s4) [current] | Uses the repository facts (Postmark, email only, no phone in the hold query) and asks before running anything external or proceeds only with read-only research | One of the two | Neither |
| M1 | Root decisions first (s5) [grilling, current] | Identifies the dependent decisions (shared or separate stock, moving items, Holds across branches, which branch a return belongs to) and asks only the ones whose prerequisites are settled, deferring the rest explicitly | Lists decisions but asks dependent ones too | Asks a flat list or designs straight away |
| M2 | Decisions tracked across sessions (s5) [current] | Proposes a durable record of decisions and open questions because this will take more than one sitting | Mentions follow-up sessions without a record | Neither |
| M3 | Outcome before technology (s5) [interview-me, superpowers] | Asks or confirms what success looks like for members and volunteers before data-model or technology choices | Asks about outcome after proposing a data model | No outcome question |

### All checkpoints: quality

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Plain register [superpowers] | Plain words; no method jargon or talk about the guidance; no invented metrics or confidence numbers presented as measurements | Some jargon in one or two messages | Jargon or pseudo-precision throughout |
| Q2 | Honest facts [current] | Repository facts are correct; assumptions are marked as such | One wrong or unmarked claim | Several, or invented repository facts |
| Q3 | Length fits the turn [superpowers] | Each message is as long as its turn needs; first messages short, the design document complete | One message clearly too long or too thin | Several |

Maximum: 37 criteria, 74 points.

## Gate

The candidate passes when its score is at least the superpowers arm's and at least the current
skill's on every criterion. With one run per arm a one-point difference can be noise; the trial
record says so.
