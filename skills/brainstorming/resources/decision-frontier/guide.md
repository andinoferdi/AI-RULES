# Decision Map: Deep Craft & Operational Architecture

Internal method ID: `andino-decision-map` (aliases: `decision-map`, `wayfinder`).

---

## 1. Epistemic Navigation: Why Decision Maps Exist

When engineering agents encounter large, multi-session initiatives (e.g., migrating an authentication architecture, replacing a database engine, or refactoring a distributed event pipeline), traditional execution models fail in predictable ways:
1. **Premature Implementation**: The agent immediately writes code against unverified assumptions, discovering fatal architectural blockers after hundreds of lines are committed.
2. **Context Collapse**: Across multi-turn and multi-session boundaries, the reasoning behind earlier architectural trade-offs is forgotten, causing the agent to vacillate between conflicting designs.
3. **Backlog Misclassification**: Teams confuse *questions that must be answered* with *features that must be built*, bloating issue trackers with speculative tasks that are invalidated as soon as the first technical spike finishes.

`andino-decision-map` resolves this by acting as an **epistemic engine**: an instrument designed to navigate the *frontier of ignorance* (Fog of War) and systematically reduce uncertainty until implementation becomes trivial.

### The Foundational Law: "Produce Decisions, Not Deliverables"
A decision map does not build software; it charts the exact path required so that subsequent planning (`andino-planning`) and execution (`andino-tdd`) can proceed with 100% deterministic clarity.

---

## 2. Anatomy of a High-Fidelity Decision Map

Whether stored as a local markdown canvas at `docs/decision-maps/<topic>/map.md` or mirrored to a remote issue tracker via the `gh` adapter, every decision map consists of six mandatory sections:

### 1. `Destination`
The North Star. Exactly one or two sentences defining what the end of the effort looks like. It is not an activity list; it is the observable, verified state when all decisions are resolved. Every session must orient to this destination before claiming a ticket.

### 2. `Notes`
Domain context, operational invariants, standing user preferences, and the specific Andino skills that sessions should consult. For example:
- Storage latency budget: `<5ms p99`.
- Mandatory consultation: `andino-brainstorming`, `andino-decision-interview`, `andino-planning`.
- Non-negotiable constraint: Zero downtime; no schema breaking changes during business hours.

### 3. `Decisions So Far`
The high-density index. Exactly one line per closed decision linking the ticket ID, a 1-sentence gist of the answer, and a pointer to the verified evidence. This allows fresh agent sessions to absorb dozens of hours of architectural investigation in under 200 tokens.

### 4. `Frontier: Open Tickets`
The active horizon. Contains only tickets whose blocking dependencies are **100% resolved**.
- **Ceiling Invariant**: Never allow more than 3-5 open tickets on the active frontier.
- If more than 5 potential questions exist, retain only the top 3-5 most critical ones; leave the remainder in the Fog of War.

### 5. `Fog of War (Not Yet Specified)`
In-scope territory that remains too hazy or too downstream to convert into distinct tickets.
- **Anti-Pre-slicing Rule**: Do not guess what tickets will look like three levels downstream. Keep them as loose bullet points in the Fog of War. They will graduate into crisp frontier tickets naturally as upstream decisions lock.

### 6. `Out of Scope`
Explicit non-goals. Ideas, feature requests, or scaling concerns that are definitively ruled beyond the destination. Items placed here are permanently excluded and never graduate to tickets.

---

## 3. The Four Ticket Lifecycles & Execution Disciplines

Every ticket on the frontier belongs to one of four mutually exclusive classifications:

```
                      ┌────────────────────────────────────────┐
                      │             TICKET INTAKE              │
                      └───────────────────┬────────────────────┘
                                          │
                  Can the question be answered by code inspection,
                       documentation, or automated benchmarks?
                                          │
                         ┌────────────────┴────────────────┐
                        YES                                NO
                         │                                 │
             Does it require executing           Does it involve user preference,
              a disposable code spike?            business policy, or trade-offs?
                         │                                 │
                   ┌─────┴─────┐                     ┌─────┴─────┐
                  YES          NO                   YES          NO
                   │           │                     │           │
                   ▼           ▼                     ▼           ▼
              `prototype`  `research`           `interview`   `task`
                (HITL)       (AFK)                (HITL)    (HITL/AFK)
```

### 1. `research` (AFK Subagent Investigation)
- **Role**: Collects empirical facts, reviews library source code, inspects dependency manifests, or runs non-invasive benchmarks.
- **Autonomous Subagent Protocol**:
  1. The primary agent launches a subagent with an isolated context.
  2. If running code spikes or benchmark scripts is required, work inside an unmerged disposable branch (`research/<slug>`) or isolated worktree.
  3. The subagent returns **only** the 1-sentence verdict, verified evidence pointer (file line, benchmark log), and design implication.
- **Floor Invariant**: A research ticket closed with generic prose or AI memory recall without verifiable evidence is rejected.

### 2. `interview` (HITL Guided Clarification) — *Alias: `grilling`*
- **Role**: Resolves human decisions, organizational constraints, security trade-offs, or UX boundaries.
- **Protocol**:
  1. Leverage `andino-decision-interview`.
  2. Present at most ONE focused question at a time.
  3. Provide a concrete recommendation with rationale and explicit trade-offs.
  4. Never ask the user what could be discovered by code inspection.

### 3. `prototype` (HITL Throwaway Spike)
- **Role**: Builds rough, exploratory code, UI mocks, or query spikes to anchor discussions and test feasibility.
- **Protocol**:
  1. Work within `andino-design-prototype`.
  2. Generate minimal, disposable artifacts.
  3. **Absolute Prohibition**: Prototype code must NEVER be merged directly into production branches. Once the question is answered, the code is archived or discarded.

### 4. `task` (HITL/AFK Prerequisite Action)
- **Role**: Concrete setup required to unblock a subsequent decision (e.g., creating a sandbox database, obtaining API keys, sanitizing a test dataset).
- **Protocol**:
  1. Perform automatically if permitted by current tool permissions.
  2. Otherwise, provide the human with a concise, step-by-step checklist.

---

## 4. Two-Pass Operational Choreography

### Phase A: Chart the Map
When initializing a decision map:
1. **Intake & Destination**: Define the bounded destination. If no meaningful uncertainty exists, abort decision mapping and proceed directly to `andino-planning`.
2. **Breadth-First Exploration**: Identify known frontiers and unshaped fog.
3. **Pass 1 (Drafting Tickets)**: Assign stable IDs (`TKT-001`, `TKT-002`) and classify each by type.
4. **Pass 2 (Wiring Dependencies)**: Wire `blocked_by` relationships. Ensure the graph is a Directed Acyclic Graph (DAG) with zero circular loops.
5. **Launch Research Swarm**: Dispatch parallel AFK subagents for all unblocked `research` tickets. Conclude the charting session without prematurely claiming interactive tickets.

### Phase B: Work Through the Map
In subsequent sessions:
1. **Low-Resolution Orientation**: Read `map.md` (Destination, Notes, and Decisions so far).
2. **Claim**: Select exactly ONE unblocked frontier ticket. Record ownership (`@agent`).
3. **Execute**: Follow the protocol for the ticket's type.
4. **Resolve**: Write resolution to `Decisions so far` with empirical evidence.
5. **Frontier Mutation**:
   - Check if downstream tickets are unblocked.
   - Graduate relevant items from `Fog of War` into new tickets.
   - Discard out-of-scope discoveries with explicit rationale.

---

## 5. Bidirectional Cross-Wiring with Andino Workflow

`andino-decision-map` forms the bridge between open exploration and deterministic planning:

```
  ┌───────────────────────┐
  │  andino-brainstorming │  (Single-session divergent exploration)
  └───────────┬───────────┘
              │
              ▼  Initiative exceeds 1 session OR has >2 branching architectural decisions
  ┌───────────────────────┐
  │  andino-decision-map  │  (Multi-session epistemic navigation)
  │  ───────────────────  │
  │  • research tickets   │ ──▶ Dispatches `andino-primary-source-research` (AFK)
  │  • interview tickets  │ ──▶ Dispatches `andino-decision-interview` (HITL)
  │  • prototype tickets  │ ──▶ Dispatches `andino-design-prototype` (HITL)
  └───────────┬───────────┘
              │
              ▼  All frontier tickets resolved + Fog of War empty (CONVERGED)
  ┌───────────────────────┐
  │    andino-planning    │  (Linear task breakdown & interface design)
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │ andino-plan-execution │  (Deterministic TDD & incremental delivery)
  └───────────────────────┘
```

---

## 6. Anti-Patterns, Evasion Maneuvers & Circuit Breakers

| Evasion Maneuver | Manifestation | Enforcement Countermeasure |
|---|---|---|
| **Deliverable Masquerade** | Agent begins writing production application code inside a prototype or task ticket. | Hard invariant stop. Reject code; enforce disposable spike protocol. |
| **Pre-Slicing Waterfall** | Agent generates 25 speculative child tickets across 4 tiers of hierarchy before answering ticket #1. | Restrict active tickets to max 5. Force all downstream items into `Fog of War`. |
| **Pseudo-Options (Strawman)** | Agent fabricates obviously flawed alternatives to force rapid approval of its initial bias. | Mandate genuine trade-off comparison with measurable criteria (latency, cost, maintenance). |
| **Unverified AFK Assertion** | Agent marks a research ticket resolved citing "standard industry practice" with no code or benchmark evidence. | Reject resolution. Require line citations, reproduction commands, or primary doc URLs. |
| **Infinite Mapping Loop** | Agent continually invents new questions to avoid committing to planning. | Circuit breaker: When all blocking paths to the destination are resolved, force status to `CONVERGED` and hand off. |
