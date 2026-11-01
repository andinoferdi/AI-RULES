# Decision Map & Ticket Protocols

This document defines the canonical schemas, templates, and operational lifecycle protocols for `andino-decision-map`.

---

## 1. Architectural Philosophy: Decisions, Not Deliverables

A decision map is an **epistemic tool** for reducing uncertainty across multi-session initiatives. It is not an implementation task backlog.

| Task Backlog (`andino-planning`) | Decision Map (`andino-decision-map`) |
|---|---|
| **Objective**: Produce code deliverables. | **Objective**: Produce decisions that make code trivial. |
| **Premise**: Direction, interfaces, and architecture are settled. | **Premise**: Destination is known, but consequential branches remain unsettled. |
| **Ticket Meaning**: "Construct component X according to spec." | **Ticket Meaning**: "Answer question Y so we know whether X is needed." |
| **Output**: Merged production pull requests. | **Output**: Evidence-backed decision records and collapsed fog. |

---

## 2. Canonical Single-Canvas Template (`map.md`)

By default, maintain the entire decision map in a single canonical file at `docs/decision-maps/<topic>/map.md`. This eliminates file sprawl, reduces token I/O churn, and prevents drift.

```markdown
# Decision Map: <Topic Name>

Status: ACTIVE | CONVERGED
Destination: <1-2 sentences defining observable end state — what reaching the end looks like>
Last Updated: YYYY-MM-DD

## Notes
- **Domain Context**: <Key architectural boundaries or existing constraints>
- **Guiding Principles**: <Standing preferences or non-negotiables for this effort>
- **Associated Skills**: `andino-brainstorming`, `andino-decision-interview`, `andino-planning`

## Decisions So Far
<!-- High-density chronological ledger. Exactly one line per closed decision. -->
- **DEC-001**: [<Ticket Title>](#tkt-001) — **Resolution**: <1-sentence core answer> | **Evidence**: <file path / benchmark / user statement>

## Frontier: Open Tickets
<!-- Only tickets whose dependencies are 100% resolved belong on the active frontier. Max 3-5 open tickets. -->

### TKT-002: <Concise Action-Oriented Question>
- **Type**: `research` | `interview` | `prototype` | `task`
- **Status**: `OPEN` | `CLAIMED (@agent/user)` | `BLOCKED`
- **Blocked By**: `TKT-001` (or `None`)
- **Question**: What exact unknown must be resolved to unblock the next decision?
- **Acceptance Criterion**: What concrete evidence constitutes a definitive answer?
- **Assigned Execution**: AFK Subagent (`primary-source-research`) | HITL (`decision-interview`)

## Fog of War (Not Yet Specified)
<!-- In-scope uncertainty that cannot yet be sharply ticketed until upstream tickets resolve. -->
- [ ] *Storage layer abstraction*: Needs resolution of DEC-002 (DB engine choice) before drafting.
- [ ] *Cache invalidation strategy*: Depends on write-throughput findings from research.

## Out of Scope
<!-- Explicitly ruled beyond the destination. Permanently excluded; never graduates to tickets. -->
- Multi-region active-active replication (deferred to Year 2 enterprise milestone).
- Custom cryptographic token signing (standard OAuth2/JWT libraries mandatory).
```

---

## 3. The Four Ticket Types & Execution Protocols

Every ticket must be classified under exactly one of four types:

### 1. `research` (AFK Subagent Investigation)
- **Role**: Collects concrete empirical facts from source code, documentation, benchmarks, or ecosystem packages without human intervention.
- **Agent Mode**: Asynchronous Subagent (AFK) using `primary-source-research`.
- **Branch Isolation**: When code inspection requires running spikes, execute in a disposable git branch (`research/<slug>`) or isolated worktree.
- **Floor Invariant**: Drowsy summaries without code line citations or reproduction benchmarks are rejected. Must cite primary evidence.

### 2. `interview` (HITL Guided Clarification) — *Alias: `grilling`*
- **Role**: Resolves human preference, product trade-offs, risk tolerance, or organizational boundaries that cannot be determined by code inspection.
- **Agent Mode**: Human-in-the-Loop (HITL) using `andino-decision-interview`.
- **Intake Discipline**: Present at most one focused question at a time with a proposed default and explicit trade-off impact.

### 3. `prototype` (HITL Throwaway Spike)
- **Role**: Creates a disposable code, layout, or query spike to test feasibility, performance, or developer ergonomics.
- **Agent Mode**: Isolated spike using `andino-design-prototype`.
- **Floor Invariant**: Code written during a prototype ticket is **strictly throwaway**. Merging prototype code into production branches during a decision mapping session is an absolute violation.

### 4. `task` (HITL/AFK Prerequisite Action)
- **Role**: A non-code prerequisite action required to enable an upcoming decision (e.g., obtaining API sandbox credentials, dumping sanitized sample dataset, configuring test environment).
- **Agent Mode**: Direct execution or structured checklist provided to human.

---

## 4. Standalone Ticket Protocol (`tickets/TKT-xxx.md`)

When a ticket requires extensive research logs, tabular benchmark results, or lengthy interview transcripts, extract it into a standalone file under `docs/decision-maps/<topic>/tickets/TKT-<ID>-<slug>.md`:

```markdown
---
id: TKT-003
title: Evaluate Redis Cluster vs. DynamoDB for Session Store
type: research
status: RESOLVED
claimant: claude-subagent-1
blocked_by: [TKT-001]
resolved_at: 2026-11-01
---

## Question
Which storage engine satisfies our latency constraint (<5ms p99) under 50k concurrent websockets within our infrastructure budget?

## Investigation Findings
- Benchmark script executed in `research/session-bench`:
  - Redis Cluster p99 read: 1.2ms, write: 2.1ms.
  - DynamoDB with DAX p99 read: 4.8ms, write: 8.5ms.
- Cost model: DynamoDB DAX exceeds current monthly budget by 3.2x at projected peak QPS.

## Resolution
Adopt Redis Cluster with existing sentinel topology.

## Evidence Pointer
- Benchmark results: `docs/benchmarks/2026-11-01-session-storage.log`
- Configuration verified: `infra/redis/sentinel.conf:42`

## Design Implication
Invalidates DynamoDB schema fog item; unblocks TKT-004 (Redis Sentinel client pooling).
```

---

## 5. Topological Frontier Evaluation (DAG Algorithm)

A ticket is on the **Frontier** (ready for claiming) if and only if:
1. `status == OPEN`
2. `all(dependencies.status == RESOLVED for dependency in blocked_by)`
3. No circular dependencies exist in the graph.

```
       [TKT-001: Storage Engine] (RESOLVED)
                  │
         ┌────────┴────────┐
         ▼                 ▼
  [TKT-002: Pool Size]  [TKT-003: Auth Hook]  <-- FRONTIER (Unblocked, Claimable)
         │                 │
         └────────┬────────┘
                  ▼
         [TKT-004: Migration Plan]            <-- BLOCKED (Waits for 002 & 003)
```

---

## 6. Circuit Breakers (Anti-Loop & Anti-Paralysis)

1. **Max Active Frontier**: Never keep more than 5 unblocked tickets open simultaneously. If more than 5 emerge, move the lower-priority ones into `Fog of War`.
2. **Anti-Pre-slicing Guard**: Never create tickets more than two levels deep from the active frontier. Remote downstream details must remain in `Fog of War` until upstream decisions lock.
3. **Session Claiming Limit**: Never claim and resolve more than ONE ticket per interactive user turn (except for parallel autonomous research sweeps).
4. **Handoff Convergence**: When `Fog of War` is empty and all active frontier tickets are resolved, the decision map is **CONVERGED**. Promptly execute handoff to `andino-planning` or `andino-specification`.
