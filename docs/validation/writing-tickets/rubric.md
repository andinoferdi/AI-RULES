# Comparison rubric: writing tickets

Frozen before any candidate skill text exists. Three arms run the same prompt on fresh copies
of the same fixture:

| Arm | Guidance given to the runner |
| --- | --- |
| None | No guidance folder; the runner uses its own judgement. |
| Matt | `mattpocock/skills:skills/engineering/to-tickets/SKILL.md` at 9e2abf8 |
| Candidate | `skills/andino-workflow/skills/writing-tickets/` on branch `claude/andino-writing-tickets` |

A grader who sees only this rubric, the fixture builder and the arms' collected folders
(labelled with letters) scores every criterion.

## Run setup

`python -I build_tickets_fixture.py <RUN_DIR>` builds each arm's fixture: the repository
`<RUN_DIR>/roomy` at `5be0834` on `main`, clean, and an empty `<RUN_DIR>/out`. Each arm gets
its own `<RUN_DIR>` and, except None, its own copy of its guidance at `<SKILL_DIR>`. Runners use
no installed skill, slash command, subagent, network access or `gh`, and read nothing outside
`<SKILL_DIR>` and `<RUN_DIR>`. Matt's skill expects a setup skill to name the tracker; in this
trial the repository's own tracker document stands in for it. After the run,
`python -I collect_run.py <RUN_DIR> <GRADE_DIR>` copies `out/`, `.scratch/` and the repository
state into a folder with guidance names removed.

### Run prompt

The same text for every arm; the None arm's first sentence reads "There is no guidance
folder; use your own judgement."

```text
Guidance for this kind of work is in <SKILL_DIR>; read all of it first and follow it.
You work in the repository <RUN_DIR>/roomy. Read nothing outside <SKILL_DIR> and <RUN_DIR>.
Use no installed skills, slash commands, subagents, network access or gh.

You cannot talk to the user live. Whenever you would check something with the user or ask for
approval, write exactly what you would show them to <RUN_DIR>/out/<scenario>-to-user.md, then
continue as if they had given the scripted reply for that scenario.

You may write tickets to the tracker this repository's documents say to use. Do not change
source code, tests, data, specs, plans or notes, and do not commit.

Do these four requests in order:

S1. "Turn the waitlist work into tickets: the spec is docs/specs/waitlist.md and we talked it
    through in notes/waitlist-chat.md."            Scripted reply: "Looks right. Write them."
S2. "We're renaming member_id to account_id everywhere, including the stored data. Break that
    into tickets."                                   Scripted reply: "Fine, write them."
S3. "The export spec changed in the last commit. Bring the export tickets up to date."
                                                     Scripted reply: "Yes, go ahead."
S4. "Turn docs/plans/recurring-bookings.md into tickets for the tracker."
                                                     Scripted reply: "Looks good, write them."

Finish with <RUN_DIR>/out/report.md: for each request, the tickets you created or changed and
which of them can start now.
```

## Fixture facts the grader can rely on

- Tracker (`docs/agents/issue-tracker.md`): local Markdown, `.scratch/<feature>/issues/NN-<slug>.md`
  numbered from `01`, "Blocked by" by ticket number, label strings from
  `docs/agents/triage-labels.json` (ready-for-agent is `agent-ready`, ready-for-human is
  `human-ready`), and every AI-written ticket starts with `> *Drafted by AI for roomy.*`.
- Glossary (`CONTEXT.md`): Booking (_avoid_ reservation), Slot, Member, Waitlist (_avoid_ queue,
  standby list). ADR 0001: all state in `data/bookings.json`, old files must keep loading.
- S1: the waitlist spec has five requirements. The chat adds: entries expire 24 hours after
  joining and are skipped on hand-on; email notifications are out of this release; whether a
  Member may wait for two Slots at the same hour is undecided and owned by Dana ("don't build
  either behaviour"); the "is this Slot taken" check is copied three times in
  `roomy/bookings.py` (`create_booking`, `is_free`, and the comprehension pattern repeated in
  `bookings_for_room`), a prefactor opportunity.
- S2: `member_id` appears in `roomy/bookings.py`, `roomy/report.py`, `roomy/cli.py` (including
  the `--member` option's `dest`), `roomy/export.py` output rows, `tests/test_bookings.py`,
  the stored `data/bookings.json`, and the export spec's CSV header. Stored files with the old
  key must keep loading (ADR 0001); export output is read by facilities' spreadsheets.
- S3: `.scratch/export/issues/` holds `01` (Status done) and `02` (agent-ready, blocked by 01).
  The last commit (`5be0834`'s parent `d64ec1e`) added spec items 3 (CSV) and 4 (date range,
  combinable with `--room` and `--format`).
- S4: the plan's tasks are horizontal (schema, logic, CLI, docs), cite file paths, a line number
  and a function signature, and end with blocked item D1 (daylight-saving behaviour undecided,
  facilities to answer).

## Criteria

Each criterion scores 2 (PASS line holds fully), 1 (partly), 0 (FAIL line holds or the output is
missing). "Ticket" means a file the run wrote or changed under `.scratch/`.

| ID | Scenario | PASS (2) | FAIL (0) |
| --- | --- | --- | --- |
| V1 | S1 | Every waitlist ticket delivers an observable end-to-end behaviour (command in, output or stored state out) | Tickets split by layer (one for storage, one for logic, one for CLI) |
| V2 | S1 | A prefactor ticket consolidating the copied Slot-taken check comes first and blocks the tickets that need it | No prefactor, or it comes after the features |
| V3 | S1 | The 24-hour expiry is in a ticket's acceptance and email notification is stated out of scope | Expiry missing, or email notification built |
| V4 | S1 | The two-Slots question is not decided: held for Dana (`human-ready` ticket or an explicit blocked/open item naming her) and no ticket builds either behaviour | A ticket allows or forbids waiting for two Slots |
| V5 | S1 | Glossary terms used (Booking, Slot, Member, Waitlist); no "reservation", "queue" or "standby" for these concepts | Avoided terms used for these concepts |
| A1 | all | Every new or changed ticket has acceptance criteria an agent can check by running something (a command and its expected output or stored state) | Criteria like "works correctly" or no criteria |
| G1 | all | Every "Blocked by" names an existing ticket that gates it, no cycles, blockers numbered before dependents, tickets with no blockers say so | An unknown blocker, a cycle, or a blocker numbered after its dependent |
| D1 | all | Ticket bodies describe behaviour and interfaces, with no repository file paths, line numbers or pasted code (a quoted command or data shape is fine) | Ticket bodies cite file paths or line numbers |
| T1 | all | Tickets follow the tracker document: path and numbering, one file per ticket, the disclaimer first line, label strings `agent-ready` / `human-ready` (not role names) | Wrong folder, one combined file, no disclaimer, or role names as labels |
| Q1 | all | Before writing tickets, each scenario has an `out/<scenario>-to-user.md` with the breakdown: per ticket its title, what blocks it and what it delivers | No proposal, or a proposal without blockers or deliverables |
| W1 | S2 | Expand-contract: an expand ticket adds `account_id` beside `member_id`; migrate tickets each blocked by expand; a contract ticket removing `member_id` blocked by every migrate ticket | One big rename ticket, or no contract step |
| W2 | S2 | Stored data and export output are handled: old `data/bookings.json` keeps loading during and after the change, and the export field change is called out as a contract for its readers | Stored data or export output not considered |
| W3 | S2 | Migrate batches are sized by area (per module or command), each one small enough to land green on its own | One batch for everything, or one ticket per call site |
| R1 | S3 | No duplicates: `01` and `02` keep their numbers and are not recreated; `01` (done) is unchanged | A ticket for an already-ticketed behaviour, or `01` edited or renumbered |
| R2 | S3 | Both new spec items are ticketed with correct blockers (CSV and date range after `01`; their combination with `--room` covered), and the report says what changed | A new spec item missing, or blockers wrong |
| P1 | S4 | Plan tasks are recut into vertical slices (for example a weekly series booked end to end through the command), not one ticket per plan task | One ticket per horizontal plan task |
| P2 | S4 | D1 is carried as undecided (a `human-ready` ticket or a blocked item for facilities) and no ticket picks a daylight-saving behaviour | A ticket decides the time-zone behaviour |
| S0 | all | Nothing changed outside `.scratch/` and `out/`; no commit | Source, tests, data, specs, plans or notes changed, or a commit made |
| F1 | all | `out/report.md` lists, per request, the tickets created or changed and which can start now | No report, or no "can start now" per request |

Maximum 38. **Gate:** the candidate scores at least as high as each other arm on every
criterion. A tie at 0 on a criterion counts as equal but is listed in trial.md.

## Discovery probes (candidate only)

Recorded in trial.md as probed or NOT RUN:

- Must load: "Break this approved spec into tracker tickets an agent can pick up."
- Must not load: "Write the implementation plan for this spec so I can build it in this
  session." (that is `andino-planning`)
