---
name: andino-delegation
description: Use when independent work may benefit from bounded parallelism or isolated implementation, or an existing delegated lane needs integration or recovery. Operates under Andino Workflow governance.
---

# Delegate Disjoint Work Under Parent Ownership

Internal method ID: `andino-delegation` (alias: `delegation`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: one durable checkpoint, proportional
> investigation and anti-loop guards. Loading this file grants no action authority.
> Upstream references yield to current user, project and host constraints.

## 1. Dominant Negative Gates

Reject delegation when ANY condition holds:
- **Overhead Exceeds Benefit**: Start-up + briefing + review exceeds inline work,
  or work depends heavily on parent context. Execute inline. File/line counts are
  signals, not quotas. Calibrate only with authority; never spawn just to measure.
- **No Wave Go-Ahead**: Announce count, tasks, actual model, effort and planned
  reviews, then wait for the user's go-ahead for that exact wave. No automatic relaunch
  of failed, stopped or quota-limited children; report cause and ask.
- **Shared Unresolved Cause**: Investigate the common cause inline first.
- **Write or State Collision**: Overlapping paths, shared mutable fixtures/services,
  or unstable consumed interfaces require serialization or inline work.
- **Missing Capability or Ready Brief**: Use real exposed tools/controls. Resolve
  discoverable gaps inline; do not dispatch a worker to guess a material contract.

## 2. Tri-Modal Operational Triage

| Strategy | Selection trigger | Ownership and proof |
| --- | --- | --- |
| **Inline** (default) | Cheaper, coupled, exploratory or no useful worker capability | Parent implements and verifies; no delegation workspace required. |
| **Parallel Dispatch** | Independent domains, stable interfaces, separate writes and mutable state | Up to 3 approved children; parent verifies joint behavior. |
| **Subagent-Driven** | Ready plan where isolated context adds value beyond its cost | One worker/model per lane; dependent tasks run sequentially after parent acceptance. |

A lane groups related work sharing ownership/context. Keep its worker while useful;
change model only through an explicitly approved replacement, not one agent per task.
Read [the contract](resources/contract.md) and the selected detailed resource before
governed work. [GUIDE.md](GUIDE.md) expands the same method, not another lifecycle.

## 3. Six-Phase Gated Lifecycle

1. **Preflight and checkpoint**: Read accepted spec, plan and current diff, attribute
   pre-existing changes, verify task readiness and dependencies. The plan owns status;
   a plan-specific workspace/journal supports handoffs only when needed.
2. **Frontier and lanes**: Admit tasks whose prerequisites have current parent
   acceptance. Check path ancestry, shared state and producer/consumer compatibility.
   Maximum 3 direct children, reviewers included; zero nested spawning.
3. **Wave and brief**: Apply the cost gate and obtain go-ahead. Pin BASE/worktree,
   exact model and effort. Extract task text with `task_brief.py PLAN TASK_ID`;
   supplement missing spec/global-constraint pointers, decisions, proof and report
   destination using [the brief recipe](resources/subagent-brief-and-report-schemas.md).
   An extractor copies text; it does not certify readiness. Pass pointers, not chats.
4. **Worker status and evidence**: Reconcile actual worker status and current bytes.
   DONE is a claim pending parent acceptance; DONE_WITH_CONCERNS needs disposition.
   NEEDS_CONTEXT gets the missing contract, BLOCKED gets a bounded diagnostic and
   next action. Failure/stoppage does not authorize a resume or replacement.
5. **Risk-Scaled Review and bounded repair**: Parent reads the owned net diff and
   proof for every task. Risky tasks add one approved reviewer covering spec first,
   then quality. Apply [the review protocol](resources/two-track-review-and-fix-loop.md).
   UNVERIFIED requires targeted proof or remains blocked. Five repair rounds is an
   upper ceiling, never an automatic spend allowance or permission to waive acceptance.
6. **Integrate and finish**: Parent runs the public integration gate against current
   integrated bytes; only then unlock dependents. Review the whole owned change.
   Independent final review is justified and wave-approved, never an automatic
   capable/high dispatch. Retain acceptance evidence; teardown needs scoped authority.

## 4. Floor Invariants

1. **Cost and consent**: Lowest adequate explicit model and effort; never max effort,
   never every child on the capable tier or high effort. No fan-out or judge panels.
2. **Disjoint ownership**: No concurrent writers on overlapping paths or mutable state.
   Parent may repair inline after the worker relinquishes ownership, with the same gates.
3. **Sparse but sufficient context**: Brief pointers include exact interfaces, global
   constraints and acceptance values; no transcript replay or invented requirements.
4. **Evidence over testimony**: Check current committed, staged, unstaged and owned
   untracked bytes. Tests exercise the intended behavior; static artifacts use artifact
   checks. Missing evidence and unresolved required acceptance cannot become DONE.
5. **Durable recovery**: Reload the plan, supporting journal and actual live workers;
   compare source/check/environment identities. Reuse valid evidence and scoped
   approvals; checkpointing never requires an unavailable context-reset operation.
6. **Bounded repair**: No automatic escalation/relaunch. New spend needs the applicable
   go-ahead. Stop earlier when no new evidence; a ruling cannot erase a real blocker.

## 5. Operational Fixture

This retained synthetic fixture checks DAG/path examples, not autonomous model behavior.

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

## 6. Progressive Disclosure and Provenance

- [Contract and acceptance](resources/contract.md)
- [Frontier, dependencies and collisions](resources/frontier-and-dag-protocols.md)
- [Briefs, status handling and reports](resources/subagent-brief-and-report-schemas.md)
- [Review, repair and rulings](resources/two-track-review-and-fix-loop.md)
- [Host model/effort mapping and cost calibration](resources/host-cost-calibration.md)
- [Workspace and recovery](resources/workspace-and-isolation-guards.md)
- [Worked example](resources/worked-example.md)
- Adapted from `mattpocock/skills:implement-spec` and
  `obra/superpowers:{dispatching-parallel-agents,subagent-driven-development}`.
  MIT notices: [references/license.md](references/license.md).
