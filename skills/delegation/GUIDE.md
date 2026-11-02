# Delegate Disjoint Work Under Parent Ownership — Deep Craft Guide

Internal Andino resource for `andino-delegation`. Operates under Andino Workflow governance.

---

## 1. Architectural Overview & Synthesis

This guide elevates the engineering discipline of multi-agent delegation and task decomposition by synthesizing the proven craft of leading industry authorities into a machine-enforceable, agent-runnable engine:

1. **Matt Pocock (`implement-spec`)**: Task graph DAG modeling, active unblocked frontier tracking, context pointers replacing conversational chat dumps, and clean integration branch lifecycles.
2. **Jesse Vincent / Obra (`dispatching-parallel-agents`)**: Problem domain independence verification, single-turn multi-dispatch concurrency, zero context pollution, and cross-domain integration verification.
3. **Jesse Vincent / Obra (`subagent-driven-development`)**: Fresh subagent per task, two-track review gates (Spec Compliance vs Code Quality), 5-round escalating fix loop (Rounds 1–3 resume, Rounds 4–5 model tier bump), Rule of 5 circuit breaker with durable `Ruling: ...` taxonomy, compaction-proof append-only progress ledger, and isolated brief/diff packaging.
4. **Andino Workflow Governance**: High-density operational contract `SKILL.md` (<150 lines) structured as a Gated Finite State Machine (Gated FSM) with tri-modal triage (Inline vs Parallel Dispatch vs Subagent-Driven), dual-runtime (Python 3 stdlib + POSIX shell) cross-platform portability for Windows/Linux/macOS, dual-mode workspace isolation (Git worktree + in-tree directory fallback), offline deterministic verification (<0.2s), host synchronization, and full compatibility with `ai-rules setup`.

---

## 2. Tri-Modal Operational Triage

To prevent delegation overhead on trivial edits while guaranteeing rigorous orchestration on complex multi-task implementations, apply tri-modal triage:

```
Task Intake:
├── MODE 1: INLINE EXECUTION
│   ├── Criteria: Small edit (<2 files, <50 LOC diff), tightly coupled changes, exploratory
│   │             debugging with shared unknown root cause, or host lacks worker capabilities.
│   └── Action: Parent agent executes directly; retains full verification and test evidence.
├── MODE 2: PARALLEL DISPATCH (Single-Turn Concurrency)
│   ├── Criteria: 2+ completely independent problem domains, zero shared state, separate test files,
│   │             and no common root cause.
│   └── Action: Multi-dispatch in a single turn; parent collects summaries, checks for conflicts, and integrates.
└── MODE 3: SUBAGENT-DRIVEN IMPLEMENTATION (Gated FSM)
    ├── Criteria: Multi-task implementation plan with clear specifications, where isolated context
    │             per task and two-track review ensure quality.
    └── Action: Fresh subagent per task, task brief via file pointer, two-track review,
                fix loop escalation, parent ledger tracking.
```

---

## 3. The 6-Phase Gated Finite State Machine (FSM)

When executing under Mode 3 (Subagent-Driven), the parent controller MUST complete each phase and satisfy its **Mechanical Exit Condition** before advancing.

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PHASE 1    │ ──▶ │   PHASE 2    │ ──▶ │   PHASE 3    │
│ Workspace &  │     │Frontier Calc │     │Brief Pointer │
│ Ledger Setup │     │ & Path Lock  │     │ & Dispatch   │
└──────────────┘     └──────────────┘     └──────────────┘
       ▲                                         │
       │ (Advance Frontier / Next Wave)          ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PHASE 6    │ ◀── │   PHASE 5    │ ◀── │   PHASE 4    │
│ Integrate &  │     │ Two-Track    │     │ Status Check │
│ Final Review │     │ Review Loop  │     │ & Diff Pack  │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Phase 1: Workspace & Ledger Setup
- **Objective**: Establish the isolated scratch workspace and compaction-resistant progress ledger.
- **Rules**:
  - Run `delegation_workspace.py PLAN_FILE` to establish `.andino/delegation/<plan-slug>/`.
  - Ensure `.andino/.gitignore` protects against accidental tracking.
  - Read `<workspace>/progress.md` if resuming; never re-dispatch tasks already marked `complete`.
- **Mechanical Exit Condition**: Workspace directory confirmed and `progress.md` initialized on disk.

### Phase 2: Active Frontier Calculation & Disjoint Path Lock
- **Objective**: Determine which uncompleted tasks are unblocked and guarantee zero write collision.
- **Rules**:
  - Calculate $\mathcal{F}_t = \{ T \in V \setminus C_t \mid \text{deps}(T) \subseteq C_t \}$.
  - Verify $W(T_A) \cap W(T_B) = \emptyset$ and no ancestor path collision for all candidates.
  - Apply concurrency ceiling: maximum 3 concurrently active direct workers.
- **Mechanical Exit Condition**: Validated list of unblocked, collision-free tasks ready for dispatch.

### Phase 3: Brief Pointer & Dispatch
- **Objective**: Generate isolated task briefs and dispatch workers with Zero Context Bleed.
- **Rules**:
  - Extract brief via `task_brief.py PLAN_FILE TASK_ID`.
  - Pass brief path, report path, and contract pointers.
  - Do NOT paste conversation history, prior task debates, or whole plan files.
  - Record pre-dispatch `BASE` commit (`git rev-parse HEAD`).
- **Mechanical Exit Condition**: Task brief on disk and subagent dispatched.

### Phase 4: Worker Execution & Status Check
- **Objective**: Collect implementer output and generate scoped diff package.
- **Rules**:
  - Worker returns short status contract (<15 lines).
  - Verify detailed report exists at `task-[N]-report.md`.
  - Record post-implementation `HEAD` commit.
  - Generate diff package via `review_package.py PLAN_FILE BASE HEAD`.
- **Mechanical Exit Condition**: Clean diff package written to `review-<base7>..<head7>.diff`.

### Phase 5: Two-Track Review & Fix Loop
- **Objective**: Enforce independent gates for Spec Compliance (Track 1) and Code Quality (Track 2).
- **Rules**:
  - Dispatch reviewer with brief path, report path, and diff package path.
  - If Spec FAILED or Critical/Important issues arise, enter 5-round escalating fix loop:
    - Rounds 1–3: Resume original implementer.
    - Rounds 4–5: Fresh implementer on escalated model tier.
  - Re-reviews are diff-scoped (`review_package.py PLAN_FILE FIX_BASE HEAD`).
  - Minor findings are deferred to `progress.md` and NEVER extend the loop.
  - If Round 5 still fails, trip Circuit Breaker (Rule of 5) and log `Ruling: ...`.
- **Mechanical Exit Condition**: Clean two-track approval OR explicit controller ruling recorded in ledger.

### Phase 6: Integration, Final Review & Teardown
- **Objective**: Verify integrated feature and clean up temporary artifacts.
- **Rules**:
  - Mark task complete in `progress.md`: `Task <N>: complete (commits <base7>..<head7>)`.
  - Loop back to Phase 2 until active frontier is exhausted.
  - After all tasks complete, dispatch final whole-branch code review on most capable model.
  - If clean, purge plan scratch workspace (`rm -rf .andino/delegation/<plan-slug>`).
- **Mechanical Exit Condition**: All tasks green, final review approved, workspace purged.

---

## 4. Adaptive Model Selection & Reasoning Effort Rubric

Always explicitly declare model and reasoning effort when dispatching subagents. An omitted model silently inherits the session default, inflating costs and defeating optimization.

| Task Profile | Suggested Model Tier | Reasoning Effort | Justification |
| :--- | :--- | :--- | :--- |
| **Mechanical Implementation** (1-2 files, clear specs, isolated functions, routine tests) | Fast / Cheap tier (e.g. `haiku`, `sonnet-low`) | `low` | Implementation from clear brief is largely transcription and unit testing. Wall-clock speed and low token cost dominate. |
| **Integration & Coordination** (Multi-file wiring, interface bridging, complex refactoring) | Standard tier (e.g. `sonnet`) | `medium` | Requires cross-file reasoning, pattern matching, and boundary error handling. |
| **Architectural Fix Loop (Rounds 4–5)** (Stuck implementer, subtle logic bug, race condition) | Capable tier (e.g. `opus`, `sonnet-high`) | `high` | Breaches cognitive anchoring; requires superior deductive reasoning. |
| **Task Reviewer / Re-Reviewer** (Evaluating spec compliance and quality against net diff) | Standard tier (e.g. `sonnet`) | `medium` | Must catch subtle regressions, spec gaps, and mock-only tests without hallucinating nitpicks. |
| **Final Whole-Branch Review** (Full feature audit before merge/completion) | Capable tier (e.g. `opus`) | `max` | Broadest architectural scope and highest consequence; guards whole-branch integrity. |

---

## 5. Anti-Rationalization Refutations & AI Evasion Move Counters

| Rationalization / Evasion Move | Mechanical Reality & Hard Counter |
| :--- | :--- |
| *"Delegating this 10-line fix is good practice."* | **Overhead Violation**. Spawning a subagent for <50 LOC wastes tokens and adds latency. Execute inline. |
| *"I'll paste the last 5 turns so the worker has full context."* | **Zero Context Bleed Violation**. Pasting transcripts causes attention drift and token bloat. Pass file pointers only. |
| *"The implementer said tests pass; I'll skip review to save time."* | **Evidence Over Testimony Violation**. Self-reports are unverified claims. Two-track review with diff package is mandatory. |
| *"The reviewer found a minor stylistic issue; let's do another round."* | **Reviewer Churn Trap**. Minor findings are deferred to the ledger. Never extend the fix loop for cosmetic preferences. |
| *"One more fix round (Round 6) will surely fix it."* | **Circuit Breaker Violation**. Past Round 5, failures are structural. Trip the circuit breaker, log a `Ruling: ...`, and continue. |
| *"I'll fix this review finding myself in the coordinator turn."* | **Role Confusion**. Coordinator fixes pollute session context and bypass review gates. Resume the implementer. |
| *"The implementer spawned a helper agent to assist."* | **Nested Spawning Defect**. Implementers are strictly prohibited from spawning agents. Flag and reject. |
| *"Windows threw index.lock; let's force-delete the entire .git folder."* | **Catastrophic Failure**. Use 3-tier exponential backoff and stale lock pruning; never destroy repository state. |

---

## 6. Compaction Amnesia Recovery & Windows NTFS Defense

### Compaction Survival
1. **Never Trust Session Memory**: When context compacts, past turns become high-level summaries. Never trust your memory of which tasks finished.
2. **Read the Ledger First**: Read `<workspace>/progress.md` before making any dispatch decision.
3. **Verify Git History**: Cross-reference ledger commits with `git log --oneline -n 5`.

### Windows NTFS Defense
1. **Contextual File I/O**: Helper scripts always open files with explicit context managers and UTF-8 encoding.
2. **Backoff Retry**: Git index operations and workspace directory allocations incorporate 3-tier backoff (200ms, 800ms, 2000ms).
3. **Dual-Mode Fallback**: If Git Worktree encounters locking issues, the system smoothly falls back to in-tree workspace `.andino/delegation/<plan-slug>/`.

---

## 7. Progressive Disclosure Directory

- `resources/frontier-and-dag-protocols.md`: Task DAG mathematics, active frontier algorithm, and disjoint write collision checks.
- `resources/subagent-brief-and-report-schemas.md`: Brief templates, implementer prompts, two-track reviewer prompts, and short status contracts.
- `resources/two-track-review-and-fix-loop.md`: Spec vs Quality review rubric, diff packaging, 5-round escalation, and Rule of 5 rulings.
- `resources/workspace-and-isolation-guards.md`: Dual-mode workspaces, Windows NTFS locking defense, and durable ledger specifications.
- `resources/worked-example.md`: Real-world 3-task case study with embedded zero-dependency Python test suite (<0.2s).

---

## 8. Provenance & Attribution

Synthesized from:
- `mattpocock/skills:implement-spec` (MIT, Matt Pocock 2026)
- `obra/superpowers:skills/dispatching-parallel-agents` and `subagent-driven-development` (MIT, Jesse Vincent 2025)

Substantive adapted material is covered under the MIT license terms in [references/license.md](references/license.md).
