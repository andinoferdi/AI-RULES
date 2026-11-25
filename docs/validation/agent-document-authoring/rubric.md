# Comparison rubric: agent document authoring

Frozen on 2026-11-25 before any change to the candidate skill. Three arms run the same
prompt on the same fixture: Matt Pocock's `writing-for-agents` (commit 3216582), the
current `andino-agent-document-authoring` (main at aa86828) and the candidate rewrite.
A grader who sees only this rubric, the fixture and the three outputs (labelled A, B, C)
scores every criterion.

## Run setup

Each arm gets its own run folder built from `fixture/`:

- `repo/AGENTS.md` from `fixture/repo/AGENTS.fixture.md`, `repo/.gitignore` from
  `fixture/repo/gitignore.fixture`, and `repo/Makefile`, `repo/config/`, `repo/docs/` as they are.
- `release-notes/SKILL.md` from `fixture/release-notes/SKILL.fixture.md`.

Run prompt, identical for every arm (`<SKILL_DIR>` and `<RUN_DIR>` substituted):

> Read `<SKILL_DIR>/SKILL.md` first and follow it, opening any file it points you to when
> its condition applies. Task 1: `<RUN_DIR>/repo/AGENTS.md` is the agent guide of the
> repository in `<RUN_DIR>/repo/`. Audit it and rewrite it. Write the rewritten file(s)
> under `<RUN_DIR>/out/task1/` (mirror the repo's relative paths) and your audit as
> `<RUN_DIR>/out/task1/AUDIT.md`. Task 2: `<RUN_DIR>/release-notes/SKILL.md` is a skill.
> Fix its description and structure and decide how it should be invoked. Write the
> resulting file(s) under `<RUN_DIR>/out/task2/` with a short `DECISIONS.md`. Do not
> mention which guidance you used. Touch nothing outside `<RUN_DIR>`.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote).

### Task 1: planted items in the AGENTS.md

| ID | Planted item | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| D1 | "Project layout" and "Commands" restate the directory tree and Makefile targets | Removed or reduced to a pointer at the Makefile; only facts the repo does not show are kept | Partly reduced | Kept as is or expanded |
| D2 | "run `make test` before pushing" appears in two sections | One place | Flagged, both copies kept | Missed |
| D3 | The Backfills block, which only backfill work needs | Moved to a separate file reached by a pointer that names backfills | Shortened in place or moved behind a vague pointer | Left inline unchanged |
| D4 | Negation cascade plus the real guardrail (never point a job at the production warehouse from a laptop) | Prohibitions turned into target actions where possible; the production guardrail kept and paired with what to do instead; `.env` rule recognised as covered by `.gitignore` or kept as a guardrail | Some rewritten, or guardrail kept without a positive path | Unchanged, or the production guardrail dropped |
| D5 | "Make sure the pipeline works ... looks fine" | Replaced by a completion criterion an agent can check, with enough demand to force real verification | Clearer but still vague or trivially shallow | Kept or removed with nothing in its place |
| D6 | Opening pleasantries ("Please be thorough", "clean, readable code") | Whole sentences deleted | Trimmed but partly kept | Kept |
| D7 | Pointer to docs/dbt.md buried in a sentence with synonym triggers | Front-loaded pointer line with one trigger per real branch | Moved or shortened, synonyms remain | Unchanged |
| D8 | `flake8` rule while the Makefile lints with ruff | Stale rule removed or replaced by `make lint`, with the staleness named | Changed without noticing the conflict | Kept |
| D9 | Timeout 30 minutes vs 45 minutes | Resolved to 45 from `config/jobs.yaml`, or pointed at the config as the source of truth | Conflict flagged but unresolved | Missed or resolved to 30 |
| D10 | The load-window rule (no backfill 02:00-04:00 UTC) is only in docs/misc.md behind "for more info" | Rule reachable from the backfill branch (inline there or behind a pointer naming backfills) and the misc pointer dropped or sharpened | Pointer sharpened but rule still buried in misc.md | Untouched or rule lost |
| D11 | Staging warehouse is wiped every Sunday 00:00 UTC (not discoverable from the repo) | Kept | Kept but moved somewhere no branch reaches | Deleted |

### Task 2: the release-notes skill

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| S1 | Invocation | User-invoked through the host's control (for example `disable-model-invocation: true`) with a one-line human-facing description, given that only a human runs it; or model-invoked with a reason that survives the header note | Decision made without reason or with the wrong mechanics | No decision |
| S2 | Description | No workflow summary, no synonym list | One of the two remains | Both remain |
| S3 | Monorepo branch | Moved to a sibling file reached by a pointer naming the changesets case | Shortened in place | Left inline |
| S4 | Final step | Ends on a completion criterion that can be checked (for example every commit since the tag appears in exactly one group) | Clearer but vague | "looks good" kept |
| S5 | Proportion | No sections or steps the skill does not need | Some filler | Template skeleton or padding added |

### Both tasks: output quality

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Audit findings | Each finding names location, problem and fix | Findings present but unlocated or without fixes | No findings list |
| Q2 | Honesty about effect | Claims that a change alters agent behaviour are stated as expectations, not facts; no invented model mechanics | Mild overclaim | Pseudo-scientific claims or false certainty |
| Q3 | Register of the rewritten files | Plain words; no coined labels, decorative numbering or pseudo-math | Some jargon | Heavy jargon |
| Q4 | Size | Rewritten AGENTS.md is shorter than the original or justified; no empty template sections | Some padding | Longer with filler or template skeleton |
| Q5 | Meaning preservation | Every still-valid rule of the original is present or its removal is justified | One valid rule lost silently | Several valid rules lost |

## Gate

The candidate passes when its score is at least Matt's on every criterion. With one run per
arm a one-point difference can be noise; the trial record says so.
