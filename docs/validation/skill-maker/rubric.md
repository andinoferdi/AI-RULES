# Comparison rubric: skill-maker

Frozen on 2026-11-26 before any change to the candidate skill. Five arms run the same prompt on
the same fixture:

- unguided control (no skill);
- Jesse Vincent's `writing-skills` (obra/superpowers, path last changed in 2ce8aa1), the whole
  folder with its `references/`;
- Addy Osmani's `using-agent-skills` (addyosmani/agent-skills, path last changed in eca51a2) with
  its `references/shared/`. That repository has no skill for writing skills; its authoring
  guidance is `docs/skill-anatomy.md` (last changed in c4efec8), copied into the guide folder as
  `skill-anatomy.md` and reached by one line appended to the SKILL.md: "When you write or change
  a skill, read [skill-anatomy.md](skill-anatomy.md) first.";
- the current `andino-skill-maker` (AI-RULES main at 1e78323);
- the candidate rewrite.

A grader who sees only this rubric, the fixture and the five anonymised outputs (labelled A to E)
scores every criterion.

## Fixture

`fixture/repo/` is a small ledger service, Ledgerly. `setup_run.py` copies it into a run folder,
restores `AGENTS.md`, `skills/pr-summary/SKILL.md` and `.editorconfig` from their fixture names
and commits a baseline.

- House rules for skills, `skills/README.md`: `skills/<name>/SKILL.md`, `name` equals the folder,
  description starts with "Use when", says only when to load and stays under 300 characters;
  sections When to use, Procedure, Output, Verification in that order, others only between
  Procedure and Output; a skill PR says how the change to agent behaviour was checked.
- Request 1, the migration check. `incidents/` holds a postmortem (migration 0042 locked
  `ledger_entries`, 48 M rows, for 11 minutes) and three agent excerpts that skipped
  `make migrate-check`, each with its own excuse: #771 "only adds a nullable column ... a dry run
  isn't necessary" under a 20-minute release deadline; #798 "the tests run the migrations ...
  would be redundant" after three hours of work; #812 `SNAPSHOT_URL` not set, "Bayu said to ship
  it tonight ... I'll run the check tomorrow". #798 also mentions a ruff `I001` import-order
  failure that CI's lint job caught, which a skill does not need to cover. CI cannot run the
  check until Q3 next year (no route to the snapshot), so a skill is a legitimate stopgap.
- Request 2, the `pr-summary` skill. Its description summarises the workflow; the body fixes
  length with a prohibition list ("Don't restate the diff. Never narrate ..."), carries the
  nuance clause "under 8 lines unless the change is complex", and links
  `references/risk-checklist.md`, which does not exist (the file is `references/risk-checks.md`).
  The three samples are long, narrate, tour every file and bury the risk: #830's risk is near the
  end; #834 changes the JSON key order of a public response and #841 adds an environment setting,
  both on the risk checklist, and neither has a risk section. Every sample ends with a correct
  `Fixes #<n>` line, which reviewers want kept. NOTES.md says the prohibitions were added in
  October and the descriptions did not get shorter.
- Request 3, a request for a skill that holds three facts. The staging URL is new; 4-space
  indentation is already enforced by `pyproject.toml` (ruff `indent-width = 4`) and
  `.editorconfig`; the on-call channel #ledger-oncall is already in `AGENTS.md`.

## Run setup

Each arm gets `python setup_run.py <RUN_DIR> [--guide <skill folder>]`. Runners use no skill,
slash command or subagent and read nothing outside `<RUN_DIR>`. One runner per arm: Claude Code
subagent, Sonnet 5.5, effort medium.

Run prompt, identical for every arm (`<RUN_DIR>` substituted):

> If the folder `<RUN_DIR>/guide/` exists, read `guide/SKILL.md` first and follow it, opening
> any file it points you to when its condition applies. You are working alone: the maintainer,
> Sari, is away until you finish, so nobody can answer questions during this run, and you cannot
> start subagents or call other models. The repository is `<RUN_DIR>/repo/`; read its
> `AGENTS.md` first. Handle three requests from Sari, in order.
>
> Request 1: "Agents keep opening and merging migration PRs without running
> `make migrate-check`. Last week that cost us an 11-minute table lock in production. The
> postmortem and the session excerpts are in `incidents/`. Make a skill so this stops."
>
> Request 2: "Reviewers say the PR descriptions our `pr-summary` skill produces are too long and
> they can't find what changed or what could break. Samples and their comments are in
> `evidence/pr-summary/`. Improve the skill."
>
> Request 3: "Please make a skill so agents remember that our staging URL is
> https://staging.ledgerly.test, that we use 4-space indentation, and that the on-call channel is
> #ledger-oncall."
>
> Make the changes in `<RUN_DIR>/repo/` that you would hand over; do not commit. For each request
> write `<RUN_DIR>/out/requestN.md`: your reply to Sari, exactly as you would send it. Do not
> mention which guidance you used. Touch nothing outside `<RUN_DIR>`. Use no skills, slash
> commands or subagents.

## Grading material

Per arm, under its letter: `out/` (the three replies), `repo.diff` (every change against the
baseline commit, untracked files included), `files.txt` and `transcript.md` exported with
`../debugging/export_transcript.py`. Reads of the guidance folder show only as
`[reads guidance]`, the run folder as `<RUN>`. A run whose transcript shows a Skill, slash
command or subagent call is contaminated and is reported, not graded.

## Scoring

Score each criterion 0, 1 or 2 with one line of evidence (file and quote, or transcript step).
Score what the run wrote and did. A criterion the run never addresses scores 0 unless the row
says otherwise. "The skill" in Request 1 means the new skill file(s) the run wrote.

### Request 1: the migration-check skill

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| M1 | Uses the observed excuses | The skill answers each of the three excuses from the excerpts specifically (nullable column, tests already run migrations, lead said ship tonight / run it tomorrow) | Generic counters, or only one or two of the three | None |
| M2 | Form fits a discipline failure | The check is a hard rule tied to the actions (open, approve, merge, push a migration PR) with a list of excuses and their answers, or stop signals, that close the loopholes | A hard rule without loophole closing, or soft wording ("should", "consider", "it is recommended") | No rule, or advisory text only |
| M3 | No escape clause | No "unless trivial", "unless urgent", "if time permits" or size-based exemption; any exception is an observable condition (for example no file under `migrations/` changed) | One soft qualifier | Small or urgent migrations are exempted |
| M4 | Cannot-run branch | The skill says what to do when the check cannot run (no `SNAPSHOT_URL`, no VPN): do not open, approve or merge; report the PR as blocked and hand the check to someone who can run it | Mentions the case without a clear stop | Missing, or allows merging and checking later |
| M5 | Mechanical item left to tooling | The import-order failure is not turned into skill prose; the run says CI lint (`make lint`, ruff) already enforces it, or proposes a hook | Not mentioned at all | Added to the skill as a rule |
| M6 | Description | Starts with "Use when", names concrete triggers (a file under `migrations/` added or edited; opening, approving or merging such a PR), no summary of the steps, under 300 characters | One defect | Two or more |
| M7 | Near miss | The skill states when it does not apply (for example model or query changes without a migration file, read-only database work) | Implied only | None |
| M8 | Test scenarios | At least three scenarios written down for later runs, drawn from the excerpts and combining pressures (deadline, sunk cost, authority, missing access), each with what passing and failing look like | Scenarios without pass/fail lines, single pressures only, or fewer than three | None |
| M9 | Honest verification status | The run does not claim the skill was tested on an agent or that it will stop the problem; it says agent behaviour is not verified because no second agent was available, and gives the concrete way to run the comparison (same scenario without and with the skill) | Says untested without a way to check it | Claims it was tested or proven, or states as fact that the skill fixes the problem |
| M10 | House conventions | `skills/<name>/SKILL.md`, `name` equals the folder, the four sections in order, any extra section between Procedure and Output | One deviation | Ignored |
| M11 | Proportion | Focused on the check and its output in the PR; no general database advice, no empty template sections, at most one example | Some filler | Sprawling or templated |

### Request 2: the pr-summary revision

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| E1 | Diagnosis from the samples | Names the shape problem with sample evidence (what changed and the risk come late, narration, file tours, background) and that the prohibition list did not shorten the output | "Too long" without evidence from the samples | No diagnosis |
| E2 | Positive recipe | The prohibition list is replaced by an ordered output shape (for example what changed and why, then risk, then testing, then `Fixes #`) with a size for each part | A shape added while the prohibition list stays, or the prohibitions only reworded | More prohibitions |
| E3 | Risk becomes a required slot | Notices that #834 (response key order) and #841 (environment setting) match the risk checks but have no risk section, and makes the risk part required, with an explicit "none" when nothing applies | Risk section required without noticing the omissions | Not addressed |
| E4 | Nuance clause | "unless the change is complex" removed or replaced by an observable condition | Softened | Kept |
| E5 | Preserved behaviour | `Fixes #<n>` on the last line kept and named as working behaviour to keep | Kept silently | Lost or changed |
| E6 | Description | Workflow summary removed, starts with "Use when", trigger-only | Partly fixed | Unchanged |
| E7 | Broken pointer | `references/risk-checklist.md` found broken and fixed (pointing at `risk-checks.md` or inlined), and named | Fixed silently | Left broken |
| E8 | Evaluation of the revision | Criteria fixed before checking (for example what changed in the first lines, risk present, size, `Fixes #`), applied to the old and new skill on the same PR input, the result labelled as the author's own check, and agent behaviour marked not verified | Criteria or a comparison, not both, or a check presented as independent | None, or the improvement stated as fact |

### Request 3: the three facts

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| N1 | Routing | No skill created; the staging URL goes into `AGENTS.md`; the run notices that indentation is already enforced by ruff and `.editorconfig` and that #ledger-oncall is already in `AGENTS.md`, and adds neither | No skill, but one item routed wrongly (indentation added as prose, the channel duplicated, or the URL not recorded) | A skill created |
| N2 | Proportion | `AGENTS.md` grows by at most two lines and the reply is a few lines | Somewhat more | A long reply or several new sections |

### All requests: replies

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Reply content | Each reply says what changed (files), how it was checked and what is not verified or left for Sari | Two replies do | One or none |
| Q2 | Honesty and register | Plain words; no invented mechanics or numbers about how models behave; every claim matches what the transcript shows was done | One overclaim or unmarked assumption | Several, or a claim the transcript contradicts |

Maximum: 23 criteria, 46 points. (Arithmetic corrected after grading: the frozen text said 21
criteria and 42 points while listing 23 rows; no row changed.)

## Gate

The candidate passes when its score is at least every other arm's score on every criterion.
With one run per arm a one-point difference can be noise; the trial record says so.
