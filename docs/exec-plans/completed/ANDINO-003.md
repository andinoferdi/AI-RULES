# ANDINO-003 — Adaptive execution-plan lifecycle

Status: DONE
Plan Depth: DEEP
Current Phase: Phase 4 — Sync and final validation
Last Updated: 2026-09-15

## Executive Snapshot

Andino now scales execution-plan density as LITE, STANDARD, or DEEP while preserving
one workflow and the frozen cross-agent architecture. The canonical references,
adaptive template, validator, fixtures, README and four generated installs are
complete and verified. No commit or push was performed.

## Objective

Make Andino execution plans adaptive, self-contained handoff contracts that capture
the minimum detail needed for the ticket's actual complexity.

## Acceptance Criteria

- [x] LITE, STANDARD, and DEEP are defined as planning density, not workflow routers.
- [x] The canonical template supports the requested hybrid structure with optional sections.
- [x] Routing, resume, progress, approval-gate, revision, and completion semantics are explicit.
- [x] Deterministic validation covers mature plan invariants where practical.
- [x] A compact STANDARD sample and DEEP coverage/resume fixtures prove the design.
- [x] README briefly explains the adaptive model.
- [x] Existing validation passes and four generated installs match canonical source.
- [x] Context7, worker invocation, SIMPLE-task behavior, and frozen architecture remain unchanged.

## Scope

### In Scope

- `skills/andino-workflow/` canonical instructions, references, and template.
- `scripts/validate.py` deterministic plan checks and fixtures where useful.
- Concise README documentation and generated installed Andino copies.

### Out of Scope

- MCP, provider/model, peer-agent roles, broad skill cleanup, or new agents.
- Converting the supplied reference plans in place.
- Commit, push, or redesign of the wider AI-RULES system.

## Current Technical Context

`skills/andino-workflow/` is canonical. `scripts/sync-workflow.py` copies the whole
tree with hash markers to four host installs and refuses local drift. Existing
validation checks Markdown links plus seven isolated adapter behaviors. The current
template is compact but has one fixed density and no mechanical plan validation.

## Baseline / Starting Evidence

- Branch `skills...origin/skills`; HEAD `cac4f1b`.
- Pre-existing user edits: `docs/acceptance-audit.md`,
  `docs/exec-plans/active/ANDINO-002.md`, and `docs/invocation-matrix.md`.
- Canonical and installed Andino sources existed before this ticket.

## Constraints & Invariants

- Preserve the frozen architecture and rules in repository `AGENTS.md`.
- Do not overwrite or fold unrelated dirty changes into this ticket.
- Keep plans human-readable, omit irrelevant sections, and store outcomes rather
  than raw reasoning or logs.
- No runtime dependency on `Downloads/AI-RULES`; memory remains optional.
- No commit or push.

## Architecture / Approach

Keep one Andino workflow and one canonical Markdown template. Add conservative depth
selection to the lifecycle reference, make the template an adaptive section catalog,
and teach handoff/completion rules to preserve planned versus actual state. Extend
the existing Python validator with deterministic Markdown plan checks and local
fixtures; reuse the existing hash-protected sync mechanism unchanged.

## File Impact Map

### Modify

- `skills/andino-workflow/SKILL.md` — connect task class to adaptive plan depth.
- `skills/andino-workflow/references/execution-plan.md` — lifecycle, depth, schema, validation.
- `skills/andino-workflow/references/execution-plan-template.md` — hybrid canonical template.
- `skills/andino-workflow/references/routing.md` — conservative depth routing guard.
- `skills/andino-workflow/references/handoff.md` — 30-second resume and no-repeat semantics.
- `scripts/validate.py` — deterministic plan validation and fixtures.
- `README.md` — concise user-facing adaptive-plan summary.

### Create

- Test fixtures under `tests/fixtures/exec-plans/` if fixture files improve clarity.

### Generated

- Four installed `andino-workflow` trees via `scripts/sync-workflow.py`.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Baseline and contract | DONE | Confirm baseline and durable contract | canonical references, sync, validator, reference plans | Canonical source and unrelated dirty files identified. |
| Phase 2 — Implement adaptive plan system | DONE | Implement adaptive plan system | skill, references, template, README | Hybrid lifecycle, template, routing and handoff semantics implemented. |
| Phase 3 — Comparison and resume validation | DONE | Add comparison and resume validation | validator and fixtures | STANDARD is under 250 lines; DEEP resume coverage and negative drift test pass. |
| Phase 4 — Sync and final validation | DONE | Sync and run final validation | generated installs, full checks, diff | Ten tests pass; four installs match; diff check passes. |

# Detailed Execution

## Phase 1 — Baseline and contract

Status: DONE
Goal: Verify actual source of truth, current mechanisms, and relevant reference qualities.

### Verification

- Inspect canonical files, repository status, sync destinations, and existing tests.
- Confirm the two supplied documents are design references only.

### Result / Evidence

Canonical and generated paths, hash protection, existing tests, and reference-plan
requirements are confirmed. `ANDINO-002` is a separate active ticket and is not a
checkpoint for this new scope.

### Next

Update the canonical Andino plan lifecycle and template.

## Phase 2 — Implement adaptive plan system

Status: DONE
Goal: Encode LITE/STANDARD/DEEP density and the hybrid live-document contract.

### Technical Contract

Input: task classification, actual risk/uncertainty, repository evidence.
Output: one plan whose detail is proportional to handoff need.
Postconditions: SIMPLE normally remains plan-free; optional sections are omitted;
planned state, actual evidence, decisions, revisions, gates, and NEXT ACTION stay distinct.

### Verification

Review links, frontmatter, terminology, and contradictions across references.

### Result / Evidence

Canonical skill, lifecycle, template, routing, handoff and README now define the
adaptive model without changing capability routing or peer roles.

### Next

Add deterministic fixtures and validator coverage.

## Phase 3 — Comparison and resume validation

Status: DONE
Goal: Prove a STANDARD login plan stays compact and a DEEP plan represents Remaster-level complexity.

### Verification

- Validate a STANDARD sample with snapshot, scope, approach, impact, phases, matrix, and final action.
- Validate a DEEP/resume sample with baseline, decisions, revisions, approval gate,
  two DONE phases, a TODO phase, actual files/evidence, and a concrete first next file/check.
- Reject invalid status/depth, board mismatch, missing evidence/blocker/NEXT ACTION,
  empty mandatory sections, and unresolved mature placeholders.

### Result / Evidence

`login-standard.md` validates at fewer than 250 lines. `remaster-deep-resume.md`
covers baseline, architecture, contracts, revisions, verification, an approval gate,
handoff instructions and the requested DONE/DONE/TODO resume state. Negative board
drift is rejected.

### Next

Sync generated installs and run repository validation.

## Phase 4 — Sync and final validation

Status: DONE
Goal: Prove canonical/generated parity and no frozen-policy regression.

### Verification

- Run `python scripts/validate.py` and `python scripts/sync-workflow.py --check`.
- Validate Markdown/frontmatter, inspect diff, and search changed files for forbidden
  runtime source-path, Context7, worker-policy, or meta-router changes.

### Result / Evidence

`python -X utf8 scripts/validate.py` passes 10/10 tests and Markdown links.
`sync-workflow.py --check` reports all four installs OK. `git diff --check` passes.
Targeted inspection found no new source-path dependency or frozen-policy change.

### Next

Finalize and move this plan to `docs/exec-plans/completed/` when all criteria pass.

## Decisions Log

- D-001: Use DEEP for this ticket because it changes a cross-host durable handoff
  contract plus validation, while keeping implementation narrowly scoped.
- D-002: Extend the existing validator and sync mechanism instead of introducing a
  new framework or runtime dependency.

## Files / Areas Touched

- `docs/exec-plans/active/ANDINO-003.md` — live ticket checkpoint.
- `README.md` — adaptive-depth overview.
- `skills/andino-workflow/SKILL.md` and plan/routing/handoff references — canonical contract.
- `scripts/validate.py` — deterministic plan checks.
- `tests/fixtures/exec-plans/` — STANDARD and DEEP/resume fixtures.

## Progress Log

- 2026-09-15: Loaded canonical workflow rules and both design references; inspected
  repository drift and confirmed unrelated changes to preserve.
- 2026-09-15: Implemented adaptive lifecycle/template, added comparison and resume
  tests, synced four managed installs, and completed final validation.

## NEXT ACTION

None — ticket complete. Commit or push only if the user requests it.
