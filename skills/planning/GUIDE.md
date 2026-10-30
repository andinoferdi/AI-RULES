# Refine one dependency-aware implementation plan

Internal method ID: `andino-planning` (alias: `planning`). Planning technique under Andino ownership.

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Turn accepted requirements into verifiable vertical slices without competing task state.

Transform broad feature specifications into lean, deterministic execution plans that an agent or engineer can execute without ambiguity. Invisible guardrails keep governance in the background: avoid meta-planning overhead and focus tokens on exact file localities, interface boundaries, and binary test oracles.

Adjust cognitive density proportionally (`LITE`, `STANDARD`, or `DEEP`) to match task risk and scope. Refine only the decisions needed to execute and verify the accepted work; do not force deep planning ceremony on small changes.

## Trigger and non-trigger

Use when: Accepted multi-step work lacks exact interfaces, dependency order, or verification steps.

Do not select for: Simple targeted single-file edits, routine bug fixes with known root causes, or an already complete accepted task graph ready to execute.

## Prerequisites

Locate the active Andino plan, checkpoint, spec, and constraints. Check the default location `docs/exec-plans/active/YYYY-MM-DD-<name>.md` or the repository's convention (`docs/plans/` or `tasks/plan.md`).

**Plan Overwrite Guard:** Never overwrite an existing, incomplete plan belonging to different work without explicit confirmation. If replanning the current ticket, update the existing document in place.

## Procedure

### 1. Grounded Locality (Enter Plan Mode)
Operate in read-only mode during planning. Inspect the repository, existing architecture, and relevant schemas before recording paths or interfaces. Map each accepted requirement to an observable outcome and owning boundary. Do NOT write implementation code during planning.

### 2. Vertical Slicing and Dependency DAG
Decompose work into independent vertical slices delivering end-to-end functionality (database, domain logic, API, test) rather than horizontal layers. Fold configuration, setup, and documentation into the slice that requires them. Validate that the task graph is a strict Directed Acyclic Graph (DAG); cycles or dangling nodes are planning defects. Tasks sharing a file write frontier must be serialized to avoid merge collisions.

### 3. The 3-Tuple Task Contract
Structure every task with three orthogonal components:
- **Target & Interfaces:** Exact files to create/modify/test and explicit `Consumes` / `Produces` signatures (names, parameter types, return types). Mark unverified dependencies as `UNKNOWN` or isolate them into a discovery spike.
- **Delta Actions:** Bite-sized TDD micro-steps (Step 1: Write failing test with spec assertions, Step 2: Run to verify failure, Step 3: Implement minimal code matching signature, Step 4: Run to verify pass, Step 5: Commit).
- **Binary Oracle:** Deterministic shell/test command with explicit expected signal (e.g. exit code or specific assertion output).

### 4. Review Focus (Edge Failure Modes)
Identify up to five implicit failure modes that the spec implies but happy-path tests miss (empty/malformed payloads, concurrency/race conditions, restart during commit, downstream timeouts, unauthorized requests). Assign each failure mode an observable test in its owning task.

### 5. Checkpoints and Dynamic Mutation Protocol
Insert integration checkpoints every 2-3 tasks to verify end-to-end health (full test suite, linter, typecheck). If a task oracle fails during execution due to local implementation details, patch the task in place. If an architectural boundary is invalidated, stop, record evidence, and re-baseline downstream tasks before continuing.

### 6. Self-Review and Handoff
Review the plan for complete spec coverage, type consistency across tasks, and absence of redundant pseudocode. A plan longer than the code it describes is an anti-pattern. Set the single `NEXT ACTION` pointing to the first executable task and step, then hand off to [plan-execution](../plan-execution/GUIDE.md).

## Ownership

When this plan is accepted and execution is authorized, hand off to [plan-execution](../plan-execution/GUIDE.md) for the next dependency-ready task. A planning-only request ends with the saved plan; plan acceptance does not by itself grant implementation or publication authority. Reuse the existing Andino checkpoint.

Andino owns selection, depth, scope, the existing durable checkpoint, delegation, and completion. The parent workflow owns final acceptance.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external messaging, environment installation, or destructive cleanup is authorized by this guide. Reuse earlier permissions without redundant confirmation; disclose unavailable actions and continue safe independent work.

## Output

One refined implementation plan with vertical slices, exact interfaces, TDD micro-steps, verification commands, and a single `NEXT ACTION`.

## Verification

Topological order satisfies dependencies; reject cycles and dangling tasks. Shared files cannot occupy the same write frontier concurrently. Verification commands produce deterministic pass/fail signals.

## Local resources

Read [the supporting contract](resources/contract.md) and [the worked procedure and plan examples](resources/worked-example.md) for artifact schemas, vertical slice decomposition, TDD micro-step patterns, and the standing quality floor. Resources are local; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- addyosmani/agent-skills:skills/planning-and-task-breakdown/SKILL.md
- obra/superpowers:skills/writing-plans/SKILL.md
- addyosmani/agent-skills:references/definition-of-done.md

MIT attribution and notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct, or Anthropic best-practices expression is included.
