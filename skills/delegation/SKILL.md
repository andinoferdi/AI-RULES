---
name: andino-delegation
description: Bounded independent tasks, parallel dispatch, or subagent-driven implementation under parent ownership. Operates under Andino Workflow governance.
---

# Delegate Disjoint Work Under Parent Ownership

Internal method ID: `andino-delegation` (alias: `delegation`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: single durable checkpoint, proportional investigation, anti-loop guards.
> Loading this file does not invoke another skill or mutate repository state. Upstream references yield to current policy.

## 1. Dominant Negative Gates

Reject delegation immediately if ANY condition holds:
- **Trivial/Mechanical**: Edit touches <2 files, <50 LOC diff, or linear boilerplate. Execute **inline**.
- **Shared Root Cause**: Concurrent failures share an unresolved cause or common failure mode. Investigate **inline**.
- **Write Collision**: Task write sets overlap ($W(A) \cap W(B) \neq \emptyset$) or exhibit ancestor path collision. Serialize or execute **inline**.
- **Capability/Authority Absence**: Host lacks authorized worker tools (`Agent`, `Workflow`). Execute **inline** without fabrication.

## 2. Tri-Modal Operational Triage

| Strategy | Selection Trigger | Execution & Integration Protocol |
| :--- | :--- | :--- |
| **Inline** | Small edit (<50 LOC), coupled changes, exploratory debug, or absent host worker. | Parent executes directly, verifies tests, and records acceptance evidence in plan. |
| **Parallel Dispatch** | $\ge 2$ independent problem domains, zero shared state, separate test files, no common root cause. | Parent multi-dispatches in a single turn, verifies disjoint scopes, integrates summaries, runs joint tests. |
| **Subagent-Driven** | Multi-task plan with clear specs benefiting from clean context and independent review. | Gated FSM: fresh subagent per task, task brief via file pointer, two-track review, 5-round escalating fix loop. |

## 3. Gated Finite State Machine (Mode 3 Lifecycle)

```
[Phase 1: Workspace & Ledger] ──▶ [Phase 2: Frontier & Collision Lock] ──▶ [Phase 3: Brief Pointer & Dispatch]
             ▲                                                                           │
             │ (Advance Frontier)                                                        ▼
[Phase 6: Integration & Whole-Branch Review] ◀── [Phase 5: Two-Track Review & Fix Loop] ◀── [Phase 4: Status Check & Diff Pack]
```

- **Phase 1 (Workspace & Ledger)**: Run `delegation_workspace.py PLAN`. Ensure `.andino/.gitignore` exists. Load `<workspace>/progress.md`.
- **Phase 2 (Frontier & Collision Lock)**: Compute $\mathcal{F}_t = \{ T \in V \setminus C_t \mid \text{deps}(T) \subseteq C_t \}$. Reject path overlap. Cap direct workers at $\le 3$.
- **Phase 3 (Brief Pointer & Dispatch)**: Extract brief via `task_brief.py PLAN TASK_ID`. Pass file pointers, never full transcripts (Zero Context Bleed). Record BASE sha.
- **Phase 4 (Status Check & Diff Pack)**: Implementer returns short status (<15 lines) + writes full report. Package net diff via `review_package.py PLAN BASE HEAD`.
- **Phase 5 (Two-Track Review & Fix Loop)**: Track 1 (Spec Compliance) + Track 2 (Code Quality). On failure, run 5-round escalating fix loop (R1–3: resume; R4–5: bump model tier). Defer Minor findings to ledger. If Round 5 fails, trip Rule of 5 Circuit Breaker and record `Ruling: <decision> — <reason> — <cost if wrong>`.
- **Phase 6 (Integration & Whole-Branch Review)**: Record completion in ledger. Loop to Phase 2 until frontier empty. Run final review on capable model before teardown.

## 4. Five Floor Invariants

1. **Strict Concurrency Ceiling**: Max 3 active direct workers. Nested subagent spawning is strictly prohibited.
2. **Disjoint Write Ownership**: Exact path intersection and ancestor directory containment are rejected prior to dispatch.
3. **Zero Context Bleed**: Pass task brief pointers and interface contracts. Never replay conversation history or dump whole plans.
4. **Mandatory Two-Track Review**: Implementer self-reports are unverified claims. Every task requires independent spec + quality review on net diff.
5. **Rule of 5 Circuit Breaker**: Fix loops terminate at Round 5. Parent controller adjudicates open issues via durable rulings; never writes code in coordinator turn.

## 5. Operational Contract & Verification Harness

```andino-operational-example
{
  "concurrency_limit": 3,
  "max_fix_rounds": 5,
  "tasks": [
    {"id": "t1", "deps": [], "files": ["src/auth/signer.py"]},
    {"id": "t2", "deps": [], "files": ["src/auth/store.py"]},
    {"id": "t3", "deps": ["t1", "t2"], "files": ["src/auth/middleware.py"]}
  ],
  "collision_pairs": [
    {"t_a": ["src/core"], "t_b": ["src/core/utils.py"], "valid": false},
    {"t_a": ["src/api/v1.py"], "t_b": ["src/api/v2.py"], "valid": true}
  ],
  "expected_frontier_step_0": ["t1", "t2"],
  "expected_frontier_step_1": ["t3"]
}
```

## 6. Progressive Disclosure & Provenance

- Complete method craft, FSM specifications, model tiering, anti-rationalizations: [GUIDE.md](GUIDE.md)
- DAG mathematics & collision algorithms: [resources/frontier-and-dag-protocols.md](resources/frontier-and-dag-protocols.md)
- Task brief & two-track review schemas: [resources/subagent-brief-and-report-schemas.md](resources/subagent-brief-and-report-schemas.md)
- Review gates & circuit breaker rulings: [resources/two-track-review-and-fix-loop.md](resources/two-track-review-and-fix-loop.md)
- Workspace isolation & ledger durability: [resources/workspace-and-isolation-guards.md](resources/workspace-and-isolation-guards.md)
- Provenance: Synthesized from `mattpocock/skills:implement-spec` and `obra/superpowers:{dispatching-parallel-agents,subagent-driven-development}`. Preserved under MIT license.
