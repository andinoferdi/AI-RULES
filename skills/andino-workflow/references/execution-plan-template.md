# [TASK / OUTCOME TITLE]

Status: TODO
Plan Depth: LITE / STANDARD / DEEP
Current Phase: Phase 1 — [name]
Last Updated: YYYY-MM-DD
Active Agent: [optional context only; never an ownership lock]

<!-- Optional coordinator checkpoint scaffold, not an override for a selected
skill's artifact format or depth. One progress source may link full specs, plans,
designs and reports; these are deliverables, not duplicate lifecycle tracking.
Only for CHECKPOINTED work. Keep the minimum fields required by the selected
plan density in execution-plan.md; remove optional sections that do not help this
task. Research, daily work and decisions do not require code or file-edit phases. -->

## Executive Snapshot

[Outcome, current progress, critical finding or decision, and immediate next action.
LITE may use a compact Current State instead.]

## Objective

[Desired outcome, not an activity list.]

## Acceptance Criteria

- [ ] [Observable/testable result.]

## Scope

### In Scope

- [Material boundary.]

### Out of Scope

- [Material exclusion.]

## User Decisions / Clarifications

- [Only decisions that materially constrain the outcome or approach.]

## Current Context

[Relevant artifacts, sources, environment, data or project state; technical details only when applicable.]

## Baseline / Starting Evidence

- [Relevant observation, source/date, reproduction, metric or starting state needed to assess the outcome.]

## Constraints & Invariants

- [Task-specific compatibility, behavior, safety, security, or referenced project rule.]

## Architecture / Approach

[Approach and why it fits; relevant sources, decision criteria or system contracts.]

## Artifact / System Impact Map

### Create

- `path` — purpose

### Modify

- `path` — purpose

### Delete

- `path` — reason

### Temporary

- `path` — lifecycle

Use `UNKNOWN — update after investigation` instead of inventing paths. Remove empty categories.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — [name] | IN_PROGRESS | [goal] | [verified artifacts/sources/areas or UNKNOWN] | [actual result when known] |
| Phase 2 — [name] | TODO | [goal] | [scope] | Pending. |

# Detailed Execution

## Phase 1 — [Name]

Status: IN_PROGRESS
Goal: [Outcome.]
Why: [Only when ordering is not obvious.]
Relevant Scope: [Artifacts/sources/systems; paths/symbols when applicable.]

### Artifacts / Areas (when applicable)

- Create: [path and purpose]
- Modify: [path and purpose]
- Delete: [path and reason]
- Temporary: [path and lifecycle]

### Outcome Contract

Input: [input/state]
Output: [observable output]
Preconditions: [required state]
Postconditions / invariants: [what remains true]

### Context / Known Evidence

- [Confirmed behavior or prior result required for correct execution.]

### Action Steps

<!-- For implementation, expand each deliverable below using
skills/planning/resources/contract.md and its worked example. A milestone plus
acceptance is only a roadmap; it does not replace task-level change instructions.
For research/decision work use concrete source/artifact operations instead. -->

#### T1 - [Observable deliverable]

Status: TODO
Readiness: [READY only after detail below; otherwise NEEDS_DETAIL / WAITING_ON D1]
Requirements: [accepted requirement IDs and exact values]
Depends on: [task IDs or none]
Owns: [Create/Modify/Delete exact paths and symbol/section anchors]
Interfaces: [consumed/produced names, signatures and producer reference; or none]
Acceptance: [input/state -> literal output/side effects and relevant failure case]

Change Specification:

- [Inspected current state at file::anchor; add/replace/remove what, into what.]
- [Exact names/imports/values/error behavior; named pattern and differences if reused.]

```text
[Decision-bearing code/diff/config or exact before/after text, not "implement here".
Use the appropriate language fence. Omit routine bodies, retain actual decisions.]
```

- [ ] [Add named regression with decisive fixture/assertion code; for static work inspect exact old text.]
- [ ] [Run exact focused command from directory with prerequisites; expected missing-behavior signal.]
- [ ] [Apply the Change Specification at its exact file/symbol anchors.]
- [ ] [Rerun command; expected assertions/output, nonempty test count and exit 0.]

Verification prerequisites: [runtime/fixtures/services or none beyond repo setup]
Integration gate: [public-flow command/observation at the task boundary when applicable]
Result / Evidence: Not run - planned checks only.

<!-- Include decisive assertion code for executable checks. Static artifacts use
inspect/change/validate; no invented test runner. Discovery names source/experiment,
decision artifact, exit criterion and blocked tasks, then fills their details. -->

### Verification

- Planned: `[targeted command/check]`
- Expected/pass criteria: [observable result]

### Result / Evidence

- Actual: [concise outcome after execution]

### Deviations

- [What changed, why, and evidence.]

### Completion Criteria

- [Condition for DONE.]

### Next

[Concrete transition.]

## Decisions Log

- D-001 — Decision: [choice]. Reason/evidence: [why]. Impact: [scope].

## Findings / Root Cause

### CONFIRMED

- [Evidence-backed finding.]

### REJECTED

- [Tested hypothesis and rejecting evidence.]

### UNKNOWN

- [Question requiring investigation.]

## Plan Revisions

- R-001 — [Change]. Reason/evidence: [why]. Impact: [phase, dependency, or depth].

## Verification Matrix

| Requirement | Verification | Status | Evidence |
| --- | --- | --- | --- |
| [Acceptance criterion] | [command/check] | TODO | Pending. |

## Files / Areas Touched

- `path` — actual change and purpose.

## Progress Log

- YYYY-MM-DD — [Meaningful checkpoint only.]

## Approval Gates

### APPROVAL GATE — [Action]

Required before: [destructive, external, irreversible, or manual-acceptance action]
Status: WAITING / APPROVED

## Known Limitations

- [Evidence-backed remaining limitation.]

## Handoff Notes

- Do not repeat: [completed work with valid evidence.]
- First inspect: [relevant source/artifact/state; path/symbol when applicable].
- Then: [specific action and check.]

## NEXT ACTION

[First source/artifact/state or material question; exact action; next verification.]

<!--
Use only for CHECKPOINTED work. Reasoning depth does not select plan density.
Adapt before use. LITE keeps the minimum checkpoint fields. STANDARD adds useful
coordination detail. DEEP expands only evidence-backed contracts, dependencies,
findings, revisions and gates. Delete every optional section or field that does not
reduce ambiguity, rework, risk or handoff cost. Never leave placeholders in a mature plan.
-->
