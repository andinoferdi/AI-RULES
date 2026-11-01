---
name: andino-decision-map
description: Map complex multi-session initiatives into sharp decision tickets, fog-of-war, and out-of-scope boundaries. Produces decisions, not deliverables. Operates under Andino Workflow governance.
---

# Decision Map: Navigating Multi-Session Initiatives

Internal method ID: `andino-decision-map` (aliases: `decision-map`, `wayfinder`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, single durable checkpoints, and anti-loop guards. Selected skills own their full procedures, resource contracts, and verification checks. Do not re-invoke `andino-workflow` recursively.

Map uncertain, consequential multi-session technical initiatives into sharp decision tickets while keeping architecture navigable and free from premature production code.

## Activation & Negative Gates

- **Use when**:
  - Destination is clear, but several consequential architectural choices cannot be settled in one context.
  - Multi-session initiatives have branching dependencies (storage, auth, topology, migration).
  - Asynchronous research (AFK) and human decisions (HITL) must unblock each other before coding.
- **Do NOT use when**:
  - Single-session open exploration with no destination (use `andino-brainstorming`).
  - Missing single user requirement on a chosen path (use `andino-decision-interview`).
  - Implementation tasks are already clear and unblocked (use `andino-planning`).
  - Routine bugfix or mechanical edit (use `andino-tdd` or `andino-debugging`).

## Core Invariant: "Produce Decisions, Not Deliverables"

A decision map is an epistemic engine for reducing uncertainty. It does not produce production code:
1. **Zero Production Mutation**: Decision mapping creates or edits only map/ticket artifacts (`map.md`).
2. **Disposable Spikes Only**: `prototype` tickets yield throwaway code to test assumptions, never mergeable features.
3. **Epistemic Convergence**: When fog collapses, hand off to `andino-planning`. The map never implements itself.

## Two Operational Modes

### Mode 1: Chart the Map (Initial Mapping)
1. **Define Anchor**: Name the 1-2 line `Destination`, `Notes` (domain, standing constraints), and explicit `Out of scope`.
2. **Draft Frontier Tickets (Pass 1)**: Draft immediate unblocked tickets with IDs. Do not pre-slice deep downstream trees; keep unshaped uncertainty in `Fog of War` (`Not yet specified`).
3. **Wire Dependencies (Pass 2)**: Link `blocked_by` relationships after all IDs exist. Max 3-5 active frontier tickets.
4. **Dispatch Research**: Launch parallel AFK subagents (`primary-source-research`) in isolated branches (`research/<slug>`).

### Mode 2: Work Through the Map (Session Progression)
1. **Scan Index**: Read the low-resolution index in `map.md`; never dump full ticket bodies into context at once.
2. **Claim One Ticket**: Select the user-designated or next unblocked frontier ticket; mark status `CLAIMED`.
3. **Execute by Protocol**:
   - `research` (AFK): Collect verified empirical facts/logs; cite primary sources.
   - `interview` (HITL / *alias: grilling*): Settle human choice via `andino-decision-interview`.
   - `prototype` (HITL): Construct disposable spike via `andino-design-prototype`.
   - `task` (HITL/AFK): Complete concrete prerequisite setup.
4. **Record Resolution**: Record 1-sentence verdict, verified evidence, and design implications in `Decisions so far`.
5. **Advance Frontier**: Unblock dependent tickets, graduate newly clear fog, and mark out-of-scope boundaries.

## Anti-Rationalization Refutations

| Rationalization | Mandated Reality |
|---|---|
| *"We can write the feature while mapping."* | **False.** Premature code anchors unvalidated assumptions. Settle decisions first. |
| *"Let's pre-generate 20 child tickets now."* | **False.** Future tickets depend on upstream answers. Keep distant questions in Fog of War. |
| *"Research ticket is done based on general recall."* | **False.** Research without cited lines, logs, or benchmarks is rejected as unverified. |
| *"We must use a cloud issue tracker."* | **False.** Local Markdown (`docs/decision-maps/<topic>/map.md`) is the zero-dependency source of truth. |
| *"The map can declare the project complete."* | **False.** The map declares decisions settled, then hands off to `andino-planning`. |

## Diagnostic Red Flags (Stop Immediately)

- [ ] Merging production code or modifying application features during a mapping session.
- [ ] Accumulating more than 5 open unblocked tickets on the active frontier.
- [ ] Closing a `research` ticket without reproducible logs, primary docs, or benchmark evidence.
- [ ] Introducing circular dependencies (`A blocks B, B blocks A`) into ticket metadata.
- [ ] Claiming or working more than ONE non-research ticket per interactive session turn.

## Progressive Disclosure Resources

- [resources/map-and-ticket-protocols.md](resources/map-and-ticket-protocols.md) — Canonical `map.md` schemas, ticket lifecycles, and DAG logic.
- [resources/gh-adapter.md](resources/gh-adapter.md) — Optional synchronization with GitHub Issues via `gh` CLI.
- [resources/worked-example.md](resources/worked-example.md) — End-to-end migration walkthrough and Python stdlib verifier.

## Operational Example (Offline)

```python andino-operational-example
import json, sys
tickets = {
    "TKT-001": {"type": "research", "status": "RESOLVED", "blocked_by": [], "evidence": "bench.log"},
    "TKT-002": {"type": "interview", "status": "OPEN", "blocked_by": ["TKT-001"]},
    "TKT-003": {"type": "prototype", "status": "OPEN", "blocked_by": ["TKT-002"]}
}
resolved = {k for k, v in tickets.items() if v["status"] == "RESOLVED"}
frontier = sorted(k for k, v in tickets.items() if v["status"] == "OPEN" and all(b in resolved for b in v["blocked_by"]))
result = {"frontier": frontier, "decisions_count": len(resolved), "is_converged": len(frontier) == 0}
print(json.dumps(result, sort_keys=True))
```

## Provenance

Adapted from `mattpocock/skills:skills/engineering/wayfinder/SKILL.md` (MIT License, Matt Pocock 2026), synthesized with Andino Workflow multi-session governance, local-first single-canvas protocols, and offline verification.
