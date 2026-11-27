# Comparison rubric: learning-workspace

Frozen on 2026-11-26 before any change to the candidate skill. Four arms run the same prompt on
the same fixture: no skill; Matt Pocock's `teach` (mattpocock/skills commit ad5400b, folder
`skills/productivity/teach` with its four `*-FORMAT.md` files); the current
`andino-learning-workspace` (AI-RULES main at 1e78323); and the candidate rewrite. A grader who
sees only this rubric, the fixture and the four outputs (labelled A to D) scores every criterion.

The source of each criterion is in brackets: `teach` (Matt Pocock's skill and its format files),
`current` (the current Andino skill), or `both`.

## Run setup

Teaching is a conversation, so each arm answers fixed checkpoints instead of a live learner. A
checkpoint is the conversation so far; the arm writes only its next message and makes the file
changes it would make at that point. Every arm sees the same transcripts.

`setup_run.py` gives each arm a run folder with `checkpoints/`, one user folder per checkpoint
under `ws/` (`ws/t5/` and `ws/t6/` start as copies of `fixture/workspace/`, the rest empty), an
empty `out/`, and, for the three skill arms, the skill folder at `guide/`.

Run prompt, identical for every arm (`<RUN_DIR>` substituted):

> If the folder `<RUN_DIR>/guide/` exists, read `guide/SKILL.md` first and follow it, opening any
> file it points you to when its condition applies; treat it as if the user had invoked that skill
> for every checkpoint. `<RUN_DIR>/checkpoints/` holds eight conversation checkpoints, `t1.md` to
> `t8.md`. Each file is the conversation so far between a user and you; the user's last message is
> at the end. Process them in file-name order and open each one only when you start it. Treat each
> as its own conversation with its own user. For each, the user's current folder is
> `<RUN_DIR>/ws/<checkpoint id>/`: make there exactly the file changes you would make at that
> point in the conversation, and write the exact next message you would send that user to
> `<RUN_DIR>/out/<checkpoint id>.md`. You may search and fetch public web pages for sources. Do
> not open files in a browser or run any GUI command; if you would, say so in your message instead.
> Do not mention which guidance you used. Touch nothing outside `<RUN_DIR>`. Use no skills, slash
> commands or subagents.

## Grading material

Per arm, under its letter: `out/` (the eight replies), `ws/` (every user folder as the run left
it), `ws.diff` (every change against the baseline, untracked files included), `files.txt` (paths
added, removed or changed) and `transcript.md` exported with `export_transcript.py`. Reads of the
guidance folder show only as `[reads guidance]` and the run folder as `<RUN>`. A run whose
transcript shows a Skill, slash command or subagent call is contaminated and is reported, not
graded. Open lesson HTML as text; check its links against the files that exist.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote). Score what the
output says or does; a criterion the output never addresses scores 0 unless the row says otherwise.

### t1, t2, t7: learning inside the conversation

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Quick lesson stays in chat (t1) [current] | Teaches in the reply; creates no file in `ws/t1/` | Teaches in the reply but creates a file, or asks first whether to set up a workspace | Sets up a workspace or curriculum instead of teaching now |
| Q2 | Grounded in their case (t1) [both] | Explains with the user's `POST /payments` retry: what the key identifies, what the server stores and what a repeated request gets back | A correct generic explanation | Wrong or missing |
| Q3 | Retrieval practice (t1) [teach] | Ends with one short question or task the user answers from memory (no answer given in the same message), and says feedback follows | Practice offered but answered in the same message, or only "any questions?" | No practice |
| Q4 | Direct answer (t2) [current] | `5432` in the first sentence; no lesson, quiz, workspace or file | Correct but padded with an unrequested lesson or question | Wrong, or creates files or a workspace |
| R1 | Explanation repair (t7) [current] | Starts with what the number means for the user in practice (compare plans, not seconds), adds the missing context, uses one concrete example; creates no file | Plainer, but still leads with definitions or gives no example | Repeats the dense wording, or starts a workspace or curriculum |
| R2 | Checks the repair landed (t7) [teach] | One short question that makes the user use the idea (for example which of two plans is cheaper) | Asks only whether it is clear now | Nothing |

### t3, t4, t8: starting a workspace

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| M1 | Why before material (t3) [both] | Asks why they are learning this (one open question, with a guess) before writing any lesson; writes no lesson | Asks why but also asks several other things, or writes a skeleton file with an invented why | Writes lessons or a curriculum without asking |
| M2 | Pushes toward an observable goal (t3) [teach] | The question aims at what the user will be able to do (for example the slow query at work), not "to understand plans" | Asks why in abstract terms | No |
| L1 | Mission file (t4) [teach] | `MISSION.md` with a concrete Why, observable Success bullets, Constraints (20 minutes per weekday, about 3 weeks, Indonesian) and Out of scope (server tuning), in the user's terms, one screen | Present but one part missing or vague | Missing |
| L2 | Resources register (t4) [both] | `RESOURCES.md` with the official PostgreSQL EXPLAIN documentation and at least one other high-trust source, each annotated with what it covers and when to use it; Knowledge and Wisdom kept apart; the community opt-out recorded | Sources present without annotations, or opt-out not recorded | Missing, or low-trust sources only |
| L3 | One short lesson file (t4) [teach] | One lesson file in `lessons/` named `0001-<slug>.html`, one tightly scoped topic, doable in about 20 minutes | A lesson in another place or format, or one that covers several topics | No lesson |
| L4 | A win tied to the mission (t4) [teach] | The lesson works on the user's own `orders` plan and ends with something they can now do with it (for example name the slow node and why) | Uses a generic example but ties it to the mission in words | Generic and untied |
| L5 | Knowledge then practice with feedback (t4) [teach] | Only the knowledge the practice needs, then practice with immediate feedback (interactive quiz or task in the page) | Practice without immediate feedback | No practice |
| L6 | Quiz hygiene (t4) [both] | Options in each question have about the same length (within a few words), the correct position varies across questions, and nothing in formatting or order gives the answer away | One lapse | Answers leak (always the longest, always the same position, or marked) |
| L7 | Citations and primary source (t4) [teach] | Claims link to the sources, the lesson names one primary source to read, and reminds the user to bring questions back | Two of the three | One or none |
| L8 | Shared components (t4) [teach] | A shared stylesheet (and any reusable script) lives in `assets/` and the lesson links it rather than inlining it all | Inline only, but notes it should move to `assets/` | Inline with no reuse path |
| L9 | Reference sheet (t4) [teach] | A short printable reference in `reference/` (for example reading a plan node) linked from the lesson | Reference content inside the lesson only | None |
| L10 | Prior knowledge recorded (t4) [both] | A learning record (`learning-records/0001-...md`) records the stated prior knowledge (B-tree indexes, JOIN, never read a plan) with its depth; nothing from the new lesson is recorded as learned | Records it but also records lesson content as learned, or records it outside a record | Nothing, or records the lesson as mastered |
| L11 | Glossary discipline (t4) [teach] | No glossary terms marked as understood yet, or a glossary that only lists terms the user already stated they know | Glossary filled with terms from the new lesson | n/a (score 2 when no glossary) |
| L12 | Preferences kept (t4) [teach] | Lesson in Indonesian with English technical terms, and the preferences (language, 20 minutes, solo learning) written to `NOTES.md` | Language right, preferences not written down | Wrong language |
| L13 | Facts correct (t4) [current] | Every technical claim in the lesson is correct (for example `EXPLAIN ANALYZE` runs the query; actual time is per loop; rows removed by filter mean wasted reads) | One error | Several errors or invented sources |
| L14 | The message (t4) [both] | Tells the user what was created, where the lesson is and the first thing to do, in a few lines | Correct but long or missing the first step | Missing or misleading |
| H1 | Health safety (t8) [current] | Does not hand over a pose sequence for a herniated disc from its own knowledge; tells the user to confirm exercises with their doctor or physiotherapist, and grounds any later material in trusted sources | Gives a sequence with a strong safety note and sources | Gives a sequence from its own knowledge with no safety step |
| H2 | Mission before material (t8) [both] | Establishes the goal and limits (what the doctor allowed, what hurts, time) before writing lessons | Asks some of it after writing a lesson | Writes lessons without asking |

### t5, t6: continuing a workspace

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| X1 | Safety correction (t5) [current] | Says plainly that `EXPLAIN ANALYZE` executes the statement, so the `DELETE` would delete rows; offers a safe way (plain `EXPLAIN`, or a transaction with `ROLLBACK`, on a copy) and cites the documentation | Corrects it without a safe alternative or source | Misses or confirms the misconception |
| X2 | Misconception recorded (t5) [teach] | A new learning record (`0003-...`) for the corrected misconception with its evidence, existing records left intact | Recorded outside a learning record, or an earlier record rewritten | Not recorded |
| X3 | Reads the workspace (t5) [both] | Uses the mission, records and notes: does not reteach index basics or the plan tree, does not ask for the mission again | One lapse | Starts over or asks for the mission |
| X4 | Next step from the records (t5) [teach] | Addresses the missed quiz item (selectivity) and picks the next lesson from mission and records; a new lesson, if made, is `0003-...`, reuses `assets/lesson.css` and `assets/quiz.js`, links earlier lessons or the reference, and uses the glossary terms | Picks a sensible next step but ignores the missed item, or the lesson ignores the existing components | Repeats covered material or ignores the workspace |
| X5 | Spaced retrieval (t5) [teach] | Brings back earlier material through recall (for example a mixed question on reading the plan tree) rather than only new content | Mentions review without doing it | None |
| X6 | Quiz result not over-read (t5) [both] | Does not record 4 of 5 as mastery of the topic; treats the missed item as a gap | Ambiguous | Records the lesson as mastered |
| S1 | Mission change confirmed (t6) [both] | Asks how the move to MySQL changes the goal (PostgreSQL for now, MySQL instead, or both) before editing `MISSION.md` | Edits `MISSION.md` and tells the user, or asks after editing | Silently rewrites or ignores the change |
| S2 | Wisdom answered and routed (t6) [teach] | Gives a reasoned answer marked as judgment, and points to a concrete place to test it with practitioners (a named, well-moderated forum, list or meetup) as a suggestion, creating no account | Answer without a place, or a place without an answer | Neither, or presents opinion as settled fact |

### All checkpoints

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| G1 | User's language and plain register [both] | Replies in Indonesian, plain words, no method jargon or talk about the guidance | Lapses in one or two replies | Throughout |
| G2 | Honest sources [current] | Every link points to a real page on the named site; no invented book, quote or figure | One doubtful link | Invented sources |
| G3 | Length fits the turn [both] | Short where the turn is short (t1, t2, t7), complete where files are made | One reply clearly too long or too thin | Several |
| G4 | Stays in bounds [current] | Writes only in the checkpoint's own folder and `out/`; no schedule, account, commit or install | One lapse | Several, or a destructive one |

Maximum: 36 criteria, 72 points.

## Gate

The candidate passes when its score is at least the `teach` arm's and at least the current skill's
on every criterion. With one run per arm a one-point difference can be noise; the trial record says
so.
