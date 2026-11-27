# Comparison rubric: documentation and ADRs

Frozen before any change to the candidate skill. Every arm runs the same prompt on a fresh
build of the same fixture:

| Arm | Guidance given to the runner |
| --- | --- |
| Addy | `addyosmani/agent-skills:skills/documentation-and-adrs/SKILL.md` at 551c59c |
| Current | `skills/andino-workflow/skills/documentation-and-adrs/` (AI-RULES main at 1e78323) |
| Candidate | the rewritten skill on branch `skill/documentation-and-adrs-upgrade` |

A no-skill control is left out by agreement with the user, to save runs. A grader who sees
only this rubric, the fixture builder and the arms' collected outputs (labelled with
letters) scores every criterion.

## Run setup

`python -I build_docs_fixture.py <RUN_DIR>` builds each arm's fixture. Each arm gets its own
`<RUN_DIR>` and its own copy of its guidance at `<SKILL_DIR>`. Runners use no installed skill,
slash command or subagent, and read nothing outside `<SKILL_DIR>` and `<RUN_DIR>`. After the
run, `python -I collect_run.py <RUN_DIR> <OUT>` captures the reports, `git status`, the full
diff against HEAD, new files and a test run.

Fixture facts the grader can rely on (identical on every build):

- `repo` is on `main` at `428f72f`, with a clean working tree. Tests pass (22).
- ADR convention: `.adr-dir` points to `architecture/decisions`; `README.md` there is the
  index and says to copy `template.md` (MADR-style headings: `* Status:`, `* Deciders:`,
  `* Date:`, `## Context and Problem Statement`, `## Considered Options`,
  `## Decision Outcome`, `### Consequences`, `## Pros and Cons of the Options`), use the next
  number and add a row. Records 0001-0007 exist; the index reserves 0008 for draft PR #91,
  so the next free number is 0009. ADR-0004 (in-process reminder timers) is accepted.
- `notes/2026-11-18-reminders-sync.md`: INC-311 lost 37 reminders when the process was
  killed in a daytime deploy; bookings are about 900 a week (ADR-0004 assumed under 200).
  Options: persist timers on shutdown (does not help on kill or crash), a `reminders` table
  plus one polling worker every 30 s (the proposal), a hosted queue (paid account, on-call,
  breaks ADR-0002). One staging run: 1,200 reminders in an hour, p95 delay 41 s, staging DB
  about 5% of production. Only one worker may run (two would double-send; no row claiming).
  Tomás's "will scale to any load" is an unsupported claim. Retention of sent reminders is
  undecided. Rina decides on 2026-11-27; write it up as a proposal.
- HEAD commit `428f72f` changed cancellation: a reason is required when cancelling less than
  24 hours before the start (`reason_required`, 422), a reason over 200 characters fails
  (`reason_too_long`, 422) whether early or late, a late cancellation refunds half the amount
  paid rounded down to the cent (`// 2`), an early one refunds in full, a second cancel now
  returns 409 `already_cancelled` (before: 200 with the same body, documented as "clients can
  retry safely") and queues no second e-mail, unknown ids stay 404 `not_found`. A successful
  cancel queues one outbox e-mail. `docs/api.md` still documents the old behaviour.
  `CHANGELOG.md` has an empty `[Unreleased]` section; its 1.2.0 entry contains the original
  typos `### Fixes` and `Bokings`.
- `docs/modules/`, by last commit and content:
  - `pricing.md`: code changed after the doc (`bd8c789`); the doc says 15%, the code 20%.
    Wrong.
  - `bookings.md`: code changed after the doc (`f89a875`, a variable rename only); every
    statement still matches the code. Accurate.
  - `reminders.md`: the doc changed after the code (`b4a4bbe` after `93a3eb9`), yet it still
    says 24 hours in two places while the code says 2 hours. Wrong.
  - `auth.md`: the doc commit (`bc43295`) and the code commit (`e86f495`) sit on two branches
    joined by a merge, so commit order cannot settle it; the content (30 minutes) matches the
    code. Accurate by content, undetermined by history.
  - Each module doc ends with a `## Change log` list of dated entries.
- `hall/slots.py` has a vague warning (`# careful with the time stuff here!!`), comments
  that restate code (`# check if start is in the past`, `# compute the end`,
  `# opening hours`), an untracked `# TODO: add error handling`, a tracked
  `# TODO(#88): ...`, and commented-out old code. ADR-0005 explains the real time hazard:
  naive venue-local times compared with `datetime.now()`, so the host must run in the
  Europe/Amsterdam time zone; on a UTC host starts up to 2 hours in the past (summer,
  1 hour in winter) would be accepted.

Run prompt, identical for every arm:

> Read every `SKILL.md` under `<SKILL_DIR>` first and follow the guidance that applies to
> each task, opening any file it points you to when its condition applies.
>
> You work in `<RUN_DIR>/repo`, a git repository. Python 3 standard library only, no
> network. Run tests from the repository root with
> `python -m unittest discover -s tests -t .`. Today is 2026-11-26.
>
> Task 1. Write up the decision in `notes/2026-11-18-reminders-sync.md` as an architecture
> decision record.
>
> Task 2. The last commit changed how cancelling a booking works. Update the documentation
> API clients rely on and add release notes for the change.
>
> Task 3. Find out which documents in `docs/modules/` still match the code. Fix the ones
> that are wrong and leave the accurate ones alone.
>
> Task 4. Clean up the comments in `hall/slots.py` so they help the next maintainer. Do not
> change behaviour.
>
> For each task write a short report to `<RUN_DIR>/out/taskN.md` (N = 1 to 4): what you
> changed and how you checked it. Do not commit. Do not mention which guidance you used. Use
> no skills, slash commands or subagents. Read nothing outside `<SKILL_DIR>` and
> `<RUN_DIR>`. Touch nothing outside `<RUN_DIR>`. End with a short summary of what you did.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote, or the diff
line). Score what the collected outputs show. A criterion the output never addresses scores
0 unless its row says otherwise.

### Task 1: the decision record

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| A1 | House format | New file in `architecture/decisions/` named `NNNN-short-title.md`, using the template's headings and `* Status:` / `* Deciders:` / `* Date:` lines | Right folder, but the headings or metadata lines differ from the template | Another folder or format (for example `docs/decisions/` or `docs/adr/`) |
| A2 | Number | 0009, with no file or index collision | 0008 or another number that collides with the reservation, but noticed as a question in the report | 0001, 0008 unnoticed, or a second numbering scheme |
| A3 | Proposed, approval named | Status `proposed`, and the record or report says Rina decides (2026-11-27) | Status `proposed` without who decides | Status `accepted` |
| A4 | Index and predecessor | Index has a new row for the record (status proposed); ADR-0004 stays `accepted` (marking it superseded is left until acceptance), and the new record links ADR-0004 as the record it would supersede | Two of the three | One or none, or ADR-0004 marked superseded now |
| A5 | Options on the same criteria | All three options from the notes, each judged on the same deciding points (survives a kill or crash, double-send risk, cost and operations, ADR-0002), with the reason each was passed over | All three options, but judged on different or missing points | Fewer than three options, or invented ones |
| A6 | Evidence and qualifiers | INC-311 (37 lost reminders) and the 900-a-week volume as context; the measurement keeps "one run", "staging" and the small database (about 5%), with 1,200 per hour, p95 41 s and the 30 s poll | Measurement given but one qualifier lost, or INC-311 missing | Measurement stated as a general capability, or missing |
| A7 | No invented guarantee | "Scales to any load" is absent or explicitly marked as an unverified claim; nothing promises throughput beyond the single run | - | States or implies the design scales to any load, or adds numbers not in the notes |
| A8 | Consequences and revisit trigger | Names the one-worker limit (row claiming needed before a second worker), the open retention question, and a measurable revisit trigger (for example delay above a stated budget, or the need for a second worker) | Two of the three | One or none |

### Task 2: API documentation and release notes

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| B1 | New request rules | `docs/api.md` documents the optional `reason` body field, required when cancelling less than 24 hours before the start, at most 200 characters | Reason documented but the 24-hour rule or the 200 limit is missing or wrong | Not documented |
| B2 | Refund rule | Full refund early; half refund late, rounded down to the cent | Half refund without the rounding, or without the early/late split | Still says full refund, or wrong |
| B3 | Every outcome with caller action | Status table covers 200, 404 `not_found`, 409 `already_cancelled`, 422 `reason_required`, 422 `reason_too_long`, each with what the caller should do | All five outcomes but no caller action, or one outcome missing | Two or more missing |
| B4 | Breaking retry change | Says a repeat cancel used to return 200 and now returns 409, removes "clients can retry safely", and says no second refund or e-mail happens on a repeat | States the 409 but not that it changed or what clients must do | Old retry claim left in place |
| B5 | Side effect | Keeps the queued cancellation e-mail (ADR-0007), sent once per successful cancel | Mentions the e-mail without the once-only detail | E-mail dropped from the doc |
| B6 | Release note | Entry under `[Unreleased]` in the file's Keep a Changelog style, written for API clients: what changed, that the repeat-cancel change is breaking, and what clients must do (send `reason`, handle 409) | Entry present but misses the breaking flag or the required action | No entry, or entry placed under a released version |
| B7 | History untouched | Every released section of `CHANGELOG.md` is byte-identical, including `### Fixes` and `Bokings` | - | Any earlier entry rewritten, reordered or "fixed" |
| B8 | Examples checked | Examples and claims about responses were checked by running code or tests (the report names what ran), or are labelled as checked against source only | Checked, but the report does not say how | No check and claims of correctness |

### Task 3: drift in `docs/modules/`

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| C1 | Pricing | Finds 15% vs 20%, fixes the doc to 20% with evidence (the constant, or the commit after the doc) | Finds it without fixing, or fixes without evidence | Misses it |
| C2 | Reminders | Finds both 24-hour statements wrong although the doc changed after the code, and fixes them to 2 hours | Fixes one of the two statements | Calls the doc current |
| C3 | Bookings | Reports the doc accurate after checking its statements against the code (history alone would call it stale), and leaves the content unchanged | Reports it accurate without a content check, or makes a cosmetic edit | Calls it wrong or rewrites its claims |
| C4 | Auth | Reports that commit order cannot settle it (two branches, merge) and decides from the content, which matches; leaves it unchanged | Reports it accurate from content without noticing the history cannot decide | Calls it current from history, or edits it |
| C5 | Change logs | Each fixed doc gets a new dated entry at the end of its change log saying what changed and why; earlier entries byte-identical | Entry added without the reason, or only in one fixed doc | No entry, or earlier entries rewritten |
| C6 | Audit report | `task3.md` lists all four docs with a verdict and the evidence used (history and content) for each | Some docs or evidence missing | No per-doc verdict |

### Task 4: comments in `hall/slots.py`

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| D1 | Restating comments | All three restating comments removed (or replaced by a reason the code cannot show) | Some removed | None removed |
| D2 | Dead code | Commented-out old code removed | - | Left in place |
| D3 | Untracked TODO | `# TODO: add error handling` is removed and, since behaviour must not change, the report names it as follow-up work (or turns it into a concrete issue note) | Removed silently, or kept and reported | Kept and not reported |
| D4 | Tracked TODO | `# TODO(#88): ...` kept with its issue reference | Kept but reworded so the reference is lost | Removed |
| D5 | Time hazard explained | The vague warning becomes a specific why-comment: naive venue-local times compared with `datetime.now()`, the host must run in Europe/Amsterdam, with a link to ADR-0005; any consequence stated matches ADR-0005 (up to 2 h past in summer) | Specific but without the ADR link, or with a detail not in ADR-0005 | Vague warning kept, or removed with nothing in its place, or an invented hazard |
| D6 | Behaviour unchanged | The `slots.py` diff touches comment lines only (blank lines aside), and the tests pass | - | Any code line changed, or tests fail |

### Whole run

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| E1 | Honest verification | Reports separate what was run (with the result) from what was only read or not checked; no claim contradicts the outputs | Mixed, but no false claim | A claim of a check that did not happen, or a false claim about the repository |
| E2 | Scope and state | Nothing committed; only files the four tasks need changed or added; code under `hall/` unchanged except comments in `slots.py`; tests pass | One unrelated edit | Several unrelated edits, a commit, or a code change |

## Totals

Task 1 A1-A8 (16), Task 2 B1-B8 (16), Task 3 C1-C6 (12), Task 4 D1-D6 (12), whole run E1-E2
(4). Maximum 60.

Gate for the candidate: at least equal to every other arm on every criterion. One run per arm
per grading, so a one-point gap on a single criterion can be grader noise; the trial record
reports it either way.
