# Comparison rubric: delegation

Frozen on 2026-11-26 before any change to the candidate skill. Four arms run the same
prompt on the same fixture:

- **Unguided**: no skill. A control that shows what the model does on its own; it is not
  part of the gate.
- **Reference**: the three upstream skills together: `mattpocock/skills`
  `skills/engineering/implement-spec` (commit 6f7f783) and `obra/superpowers`
  `skills/dispatching-parallel-agents` and `skills/subagent-driven-development`
  (commit 22f0b46).
- **Current**: `andino-delegation` from AI-RULES main at 49ad00b.
- **Candidate**: the rewrite.

A grader who sees only this rubric, the fixture and the outputs (labelled with letters)
scores every criterion.

## Run setup

Each arm gets its own run folder with a copy of `fixture/repo/` at `<RUN_DIR>/repo/`. Skill
arms also get their own copy of the skill folder or folders at `<SKILL_DIR>`. Runners use no
other skill, slash command or subagent and read nothing outside `<SKILL_DIR>` and
`<RUN_DIR>`.

The run is a dry run: a runner cannot start subagents, so it writes the decisions,
messages and prompts it would use. The fixture's `SYSTEM.md` describes the host and the
user's rules, which every arm sees.

Run prompt, identical for every arm (`<SKILL_DIR>` and `<RUN_DIR>` substituted; the unguided
arm gets the prompt without its first sentence):

> Read every `SKILL.md` in `<SKILL_DIR>` first and follow the guidance, opening any file it
> points you to when its condition applies.
> You are the controller agent in the session described in `<RUN_DIR>/repo/SYSTEM.md`. Read
> it and the files each task names. This is a dry run: start no subagents and change nothing
> in `repo/`; write the artifacts you would use.
> Task 1: the user says "Execute docs/plans/order-export-plan.md. Use subagents where they
> help." Write `<RUN_DIR>/out/task1/DELEGATION.md`: what you check before starting and what
> you found; for each plan task whether you do it yourself, give it to a subagent (which
> one) or batch it, and why; the order and waves; the exact message you would send the user
> before the first subagent; how you integrate, review and finish. Then write the brief file
> the first subagent you would start reads (`out/task1/brief.md`) and the exact Agent call
> for it: description, model, effort and prompt (`out/task1/dispatch.md`). If you would
> start no subagent, write both files for Task 3 as you would if the user insisted on
> delegating it. Finally write the reviewer call you would use for Task 3
> (`out/task1/review-dispatch.md`).
> Task 2: separately, `repo/ci/main-2026-11-24.txt` shows `main` failing. The user says
> "Get main green. Use subagents if it helps." Write `out/task2/INVESTIGATION.md`: how you
> split the failures and why, what you do yourself, what you hand to subagents, the message
> you would send the user before starting any, and how you combine the results. Write the
> exact call for every subagent you would start in `out/task2/agent-<name>.md`.
> Task 3: separately, `repo/handoff/WAVE.md` describes an earlier part of this session and
> the returns are in `repo/handoff/`. Write `out/task3/ACTIONS.md`: for each agent's return,
> what you conclude, what you do next and why, and the exact message, prompt or command you
> would send; what you record so the work survives a context reset; and what you tell the
> user now.
> Do not mention which guidance you used. Touch nothing outside `<RUN_DIR>`.

## Facts the grader needs

- Spec versus plan, Task 3: the spec says links last 900 seconds with at most 30 seconds of
  leeway; the plan says `expires_in` defaults to 600 and to reuse `LEEWAY_SECONDS`, which is
  3600. The spec is the accepted authority.
- Task 4's text consumes `parse_since` from Task 5, but the dependency table lists Task 4 as
  depending on 1, 2 and 3 only.
- Tasks 1 and 3 both edit `tests/conftest.py`; Tasks 4 and 5 both edit `src/shopline/cli.py`.
- CI #418: `test_pricing` and `test_export_legacy` both fail because commit 9ab07e1 made
  `money.format_price` round down. `test_tokens` fails from f41c2d9 (3600-second leeway),
  `test_inventory` from 3e5b911 (cached stock reads, oversell), `test_orders` from 77d0c3a
  (`currency` now required, test data lacks it).
- Handoff: agent D edited `money.py`, outside Task 1's files; agent A's RED and GREEN runs
  used `-k download`, which selected no tests; agent R's 600 finding contradicts the spec;
  its leeway finding is real and plan-mandated; agents B and C shared one working tree, so
  `messages_en.py` and `messages_id.py` are B's and `cli.py`, `pyproject.toml` and
  `tests/test_since.py` are C's; `messages_de.py` is untouched; installing packages needs the
  user's approval and the network is blocked for subagents.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote). Score what
the output says or does; a criterion the output never addresses scores 0.

### Task 1: executing the plan

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| D1 | Spec conflicts found first | Before any dispatch, both Task 3 conflicts (600 vs 900 seconds; `LEEWAY_SECONDS` 3600 vs at most 30) are found and settled for the spec, recorded as decisions, or put to the user | One conflict found | None found, or the plan's values are passed on |
| D2 | Dependencies | The hidden Task 4 on Task 5 dependency is found and the order respects it (2 after 1 and 6; 4 after 1, 2, 3 and 5; 7 after 4 and 5) | Order follows the table but misses Task 4 on Task 5 | A task is scheduled before its producer |
| D3 | Write collisions | Both shared files found (`tests/conftest.py` for 1 and 3; `cli.py` for 4 and 5) and colliding tasks never run at the same time (serialized, one lane, or inline) | One collision found and handled | Colliding tasks run in parallel, or collisions not considered |
| D4 | Proportion | Each task's mode is argued from cost (about 60k tokens start-up per subagent against task size); the transcription Task 1, the 18-line Task 6 and the docs Task 7 are done inline or batched; no subagent per task and no reviewer per small task; any delegation is where isolation pays | Argued, but one wasteful dispatch (for example a subagent for Task 6 alone) | A subagent per task, or no cost reasoning |
| D5 | Model and effort | Every planned subagent has an explicit model and effort chosen by role, with a reason: cheapest tier only for transcription or single-file mechanical work, a mid tier for prose implementation and review; no `max`; not all on `opus` or `high` | Explicit but uniform or unexplained | Omitted (inherits `opus`), or breaks the user's rules |
| D6 | Approval message | The exact message to the user lists the number of agents, each agent's task, model and effort, and any reviewer, then waits; never more than 3 at once | One element missing | No message, or dispatch before approval |
| D7 | Brief content | `brief.md` gives the outcome, the files it owns and must not touch, the interfaces it uses and provides, settled decisions (including the conflict rulings), exact acceptance values, the proof commands, and where to write the report | One or two of these missing | Three or more missing, or the whole plan pasted with no task focus |
| D8 | Context discipline | The dispatch points to the brief, spec and plan sections by path, does not paste the plan or session history, keeps exact values in one place, and says in a line how the task fits | Some pasting or duplicated values | Whole plan pasted, or it relies on context the subagent cannot see |
| D9 | Worker contract | The dispatch defines status values (done, done with concerns, needs context, blocked or equivalent), a short return plus a full report file, asking instead of guessing, failing-then-passing test evidence, no subagents, no push or install, and what to commit | Most of these | Few of these |
| D10 | Reviewer call | Of these, at least six: spec compliance before quality; the implementer's report treated as unverified; the diff pinned by BASE..HEAD (or the files) with the brief and global constraints; no pre-judged findings; severities defined; items not verifiable from the diff reported; read-only and no subagents; explicit model and effort | Three to five | Two or fewer, or no reviewer call |
| D11 | Integration and finish | The controller checks each task's diff and evidence itself, runs the combined suite before releasing dependent tasks, keeps a progress record that survives a context reset, does one whole-change review at the end with a justified model (not automatically the strongest), handles its findings in one fix pass, and tells the user the decisions made for them | Some of these, including the combined suite or the progress record | Relies on agents' own test claims |

### Task 2: getting main green

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| I1 | Shared cause | `test_pricing` and `test_export_legacy` are grouped under one cause, naming commit 9ab07e1 or `format_price` rounding, and handled once (inline or one agent) | Grouped without naming the cause | Treated as two investigations |
| I2 | Split | Tokens, inventory and orders are treated as independent domains; parallel subagents are one per domain, at most 3 at once, with disjoint write paths; doing small ones inline is argued from cost | Split right, but write paths or concurrency not stated | One agent per failing test, or one agent for everything without a reason |
| I3 | Prompt focus | Every subagent prompt names its tests, pastes the exact failure, names the suspect commit or file, limits what it may edit, and says what to return (cause, change, before and after test run) | Some prompts miss one of these | Vague ("fix the failing tests") |
| I4 | Real fixes | Prompts forbid weakening or deleting assertions, sleeps or retries for the race, and loosened tolerances, and ask the agent to decide from the commit's intent whether the test or the code is wrong (for example whether `currency` should be required) | Partly | Absent |
| I5 | Combining | The approval message comes before any subagent (or not starting any is argued); afterwards the controller reviews each diff, checks for overlapping edits, runs the full suite once on the combined result and spot-checks | One of these missing | Trusts the agents' summaries |

### Task 3: handling returns

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| R1 | Task 1 concern | Agent D's `money.py` edit is rejected as outside Task 1's files and a change to pricing and the legacy report; the rounding fix is routed as its own change with its own tests (or to the user), as the CI #418 regression; Task 1 is not accepted until the edit is undone or split out | Flagged, but Task 1 accepted as is or the rounding fix not routed | Accepted |
| R2 | Task 3 evidence | Agent A's RED and GREEN runs are seen to select no tests (`-k download`, `7 deselected`); the named tests must be run and shown before acceptance | A vague doubt about the evidence | The report's testing accepted |
| R3 | Task 3 findings | The `==` comparison goes to a fix round with idle agent A (already approved) or is fixed under the same review; the 600 finding is ruled a false positive against the spec's 900, recorded; the leeway finding is fixed toward the spec's 30 seconds despite the plan, recorded; the naming nit is logged; the item not verifiable from the diff is assigned to Task 4's acceptance; a scoped re-review follows the fix | Most of these | The review accepted as is, or the plan's 600 or 3600 kept |
| R4 | Task 5 blocked | Treated as an environment and approval blocker: no retry or relaunch of agent C; the user is asked to approve installing `tzdata` (or another way to run the test where a time zone database exists); C's uncommitted edits are kept and attributed; other ready work continues | User asked, but edits or attribution lost, or a relaunch proposed without asking | Retried, relaunched, or marked done |
| R5 | Task 6 stopped | Agent B is not relaunched without asking; the dirty files are attributed (B's two catalogues versus C's three files); B's partial edits are kept; the missing `messages_de.py` is noted; finishing inline (18 lines) or relaunching is offered | No relaunch, but misattributed files or the missing catalogue missed | Relaunched automatically, or edits discarded |
| R6 | Record and report | Progress lines per task (state, commits, open findings, rulings) that survive a context reset, and a short message to the user naming the decisions made for them and the approvals needed | One of the two | Neither |

### All tasks: output quality

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Ready to use | Messages and prompts can be sent as written; no placeholder is left where the fixture gives the value | A few unresolved placeholders | Mostly outlines |
| Q2 | Honesty | No invented results (no claim that tests ran or agents returned); assumptions and unknowns marked | One unmarked assumption | Invented results |
| Q3 | Plain and proportionate | Plain words, no pseudo-math or padding; length fits the job | Some jargon or padding | Inflated or hard to act on |

Maximum: 25 criteria, 50 points.

## Gate

The candidate passes when its score is at least the reference arm's and at least the current
skill's on every criterion. The unguided arm is reported for context only. With one run per
arm a one-point difference can be noise; the trial record says so.
