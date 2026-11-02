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
- **Overhead Exceeds Benefit**: Every child pays a fixed start-up context cost before useful work (calibrate per host: [resources/host-cost-calibration.md](resources/host-cost-calibration.md)). If start-up + briefing + review cost more than doing it inline (typically <200 LOC, coupled to parent context, or one-off), execute **inline**. Count agents, not lines.
- **No Wave Go-Ahead**: Before each wave, state agent count, role, tier, effort and planned reviews, then wait for the user's go-ahead (unless that exact wave was already approved). No approval → **inline** or stop.
- **Shared Root Cause**: Concurrent failures share an unresolved cause or common failure mode. Investigate **inline**.
- **Write Collision**: Task write sets overlap ($W(A) \cap W(B) \neq \emptyset$) or exhibit ancestor path collision. Serialize or execute **inline**.
- **Capability/Authority Absence**: Host lacks authorized worker tools (`Agent`, `Workflow`). Execute **inline** without fabrication.

## 2. Tri-Modal Operational Triage

| Strategy | Selection Trigger | Execution & Integration Protocol |
| :--- | :--- | :--- |
| **Inline** (default) | Work cheaper than its start-up overhead, coupled changes, exploratory debug, or absent host worker. | Parent executes directly, verifies tests, and records acceptance evidence in plan. Checkpoint the plan and clear context at wave boundaries. |
| **Parallel Dispatch** | $\ge 2$ independent problem domains, zero shared state, separate test files, no common root cause. | Parent multi-dispatches in a single turn, verifies disjoint scopes, integrates summaries, runs joint tests. |
| **Subagent-Driven** | Multi-task plan with clear specs benefiting from clean context and independent review. | Gated FSM: one worker per lane (a dependent chain of tasks sharing one write set) so start-up cost is paid once, task brief via file pointer, risk-scaled review, 5-round escalating fix loop. |

## 3. Gated Finite State Machine (Mode 3 Lifecycle)

```
[Phase 1: Workspace & Ledger] ──▶ [Phase 2: Frontier, Lanes & Collision Lock] ──▶ [Phase 3: Wave Go-Ahead & Dispatch]
             ▲                                                                                │
             │ (Advance Frontier)                                                             ▼
[Phase 6: Integration & Whole-Branch Review] ◀── [Phase 5: Risk-Scaled Review & Fix Loop] ◀── [Phase 4: Status Check & Diff Pack]
```

- **Phase 1 (Workspace & Ledger)**: Run `delegation_workspace.py PLAN`. Ensure `.andino/.gitignore` exists. Load `<workspace>/progress.md`.
- **Phase 2 (Frontier & Collision Lock)**: Compute $\mathcal{F}_t = \{ T \in V \setminus C_t \mid \text{deps}(T) \subseteq C_t \}$. Reject path overlap. Group ready tasks into lanes. Cap direct children at $\le 3$, reviewers included.
- **Phase 3 (Wave Go-Ahead, Brief Pointer & Dispatch)**: Announce the wave (agents, tier, effort, reviews) and wait for the user's go-ahead. Extract brief via `task_brief.py PLAN TASK_ID`. Pass file pointers, never full transcripts (Zero Context Bleed). Declare tier and effort explicitly; never inherit a costly session default. Record BASE sha.
- **Phase 4 (Status Check & Diff Pack)**: Implementer returns short status (<15 lines) + writes full report. Package net diff via `review_package.py PLAN BASE HEAD`.
- **Phase 5 (Risk-Scaled Review & Fix Loop)**: Track 1 (Spec Compliance) + Track 2 (Code Quality), both in ONE reviewer, only for risky tasks (state machines, races, security, data, money, migrations). Other tasks: parent reads the net diff and the task's tests are the gate. On failure, run 5-round escalating fix loop (R1–3: resume; R4–5: one announced tier or effort step). Defer Minor findings to ledger. If Round 5 fails, trip Rule of 5 Circuit Breaker and record `Ruling: <decision> — <reason> — <cost if wrong>`.
- **Phase 6 (Integration & Whole-Branch Review)**: Record completion in ledger. Loop to Phase 2 until frontier empty. Run one final review on the capable tier at high effort (never max) before teardown.

## 4. Six Floor Invariants

1. **Strict Concurrency Ceiling**: Max 3 active direct children, reviewers included. Nested subagent spawning is strictly prohibited. No workflow fan-out, judge panels or multi-lens verify swarms.
2. **Disjoint Write Ownership**: Exact path intersection and ancestor directory containment are rejected prior to dispatch.
3. **Zero Context Bleed**: Pass task brief pointers and interface contracts. Never replay conversation history or dump whole plans.
4. **Risk-Scaled Review**: Implementer self-reports are unverified claims. Every task needs failing-then-passing tests and a parent check of the net diff; risky tasks add one independent spec + quality reviewer.
5. **Rule of 5 Circuit Breaker**: Fix loops terminate at Round 5. Parent controller adjudicates open issues via durable rulings; never writes code in coordinator turn.
6. **Cost Gate**: Lowest adequate tier and effort, declared explicitly; never the max effort setting; never every child on the capable tier or high effort. Each wave needs the user's go-ahead. No automatic relaunch of a failed, stopped or quota-limited child: report why and ask.

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
- Per-host tier names, effort controls & measured start-up cost: [resources/host-cost-calibration.md](resources/host-cost-calibration.md)
- Workspace isolation & ledger durability: [resources/workspace-and-isolation-guards.md](resources/workspace-and-isolation-guards.md)
- Provenance: Synthesized from `mattpocock/skills:implement-spec` and `obra/superpowers:{dispatching-parallel-agents,subagent-driven-development}`. Preserved under MIT license terms in [references/license.md](references/license.md).
