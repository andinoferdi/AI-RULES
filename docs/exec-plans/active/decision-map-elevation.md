# Elevate Decision-Map to Match and Exceed Upstream Wayfinder

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification, Host Sync & Delivery
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Elevate `skills/decision-map/` on branch `andino-workflow` from an over-compressed 81-line abstract guide and duplicate `GUIDE.md` into a premier, multi-session epistemic navigation engine that matches and surpasses Matt Pocock's `wayfinder`. The elevated skill synthesizes the core operational power of upstream `wayfinder` ("Produce decisions, not deliverables", explicit 5-part map body, 4-tier ticket taxonomy: `research` [AFK], `interview/grilling` [HITL], `prototype` [HITL], and `task` [HITL/AFK prerequisite], dual operational modes: *Chart the map* & *Work through the map*, and 2-pass dependency wiring) with Andino Workflow governance (<150 line operational contract `SKILL.md`, deep craft `GUIDE.md`, local-first single-canvas default with zero external dependencies, optional `gh` CLI adapter, bidirectional cross-wiring with `andino-brainstorming`, offline Python stdlib verification, and complete integration with `ai-rules setup`).

## Objective

Deliver an upgraded, self-contained `skills/decision-map` bundle whose AI output quality, epistemic rigor, multi-session durability, and operational ergonomics match and exceed upstream `wayfinder`, verified through deterministic standard library artifact checks and ready for deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/decision-map/SKILL.md` overhauled as a high-density operational contract (<150 lines):
  - 4-Question Intake Discipline with sane defaults and cost trade-offs.
  - Dominant Negative Gates ("When NOT to use").
  - The Invariant: "Produce decisions, not deliverables" (no production code in decision maps).
  - Two Operational Modes: *Chart the Map* and *Work Through the Map*.
  - 4-Tier Ticket Classification Matrix (`research`, `interview`, `prototype`, `task`) with wayfinder aliases (`grilling`).
  - Anti-Rationalization Refutations Table.
  - Diagnostic Red Flags (Stop Immediately).
  - Progressive disclosure router to `resources/`.
  - Offline runnable Python standard-library operational example (`andino-operational-example`) with default passing and adversarial `ANDINO_NEGATIVE=1` variant.
  - Provenance citation to Matt Pocock's `wayfinder`.
- [x] `skills/decision-map/GUIDE.md` overhauled with deep craft chapters (>200 lines):
  - Epistemic Navigation: Entropy Reduction vs. Task Backlog Execution.
  - The Anatomy of a Decision Map (Destination, Notes, Decisions so far, Not yet specified / Fog of War, Out of scope).
  - Single-Canvas Default vs. Standalone Ticket Lifecycles.
  - 2-Pass Dependency Wiring (Draft first, link blockers second).
  - Autonomous AFK Subagent Research Protocols on isolated branches (`research/<slug>`) with context quarantine.
  - Bidirectional Cross-Wiring with `andino-brainstorming`, `andino-decision-interview`, and `andino-planning`.
  - Managing Fog-of-War Evolution: from vague fog to crisp unblocked tickets to permanent out-of-scope.
  - Circuit Breakers: Anti-Analysis Paralysis and Evasion Maneuver Countermeasures.
- [x] `skills/decision-map/resources/map-and-ticket-protocols.md` created:
  - Canonical Single-Canvas `map.md` Markdown Template.
  - Standalone Ticket Template (`tickets/TKT-xxx-<slug>.md`) with strict YAML frontmatter schema.
  - Ticket resolution format: Verdict + Verified Empirical Evidence + Design Implication.
  - Topological Dependency (DAG) sorting and frontier calculation algorithms.
- [x] `skills/decision-map/resources/gh-adapter.md` created:
  - Protocol for optional GitHub Issues integration via `gh` CLI.
  - Read/Propose-First safety guard preventing unauthorized remote issue mutation.
  - Label mapping (`wayfinder:map`, `wayfinder:research`, `wayfinder:interview`, `wayfinder:prototype`, `wayfinder:task`).
  - Issue comment resolution and milestone/dependency linking.
- [x] `skills/decision-map/resources/worked-example.md` created:
  - Realistic end-to-end multi-session architecture scenario (e.g. distributed auth & token session migration).
  - Complete simulation of Charting the Map, dispatching parallel research, conducting user interview, resolving blockers, and graduating fog.
  - Embedded zero-dependency executable Python script validating map integrity and floor invariant enforcement.
- [x] Bidirectional cross-wiring updated in `skills/brainstorming/SKILL.md` and `skills/brainstorming/GUIDE.md`.
- [x] `references/legal/provenance.md` updated with the 2026-11-01 elevation notice for `decision-map`.
- [x] Deterministic Python verification script executed and passing in temporary directory (`default` exit 0, `ANDINO_NEGATIVE=1` exit 1).
- [x] Upgraded skill synchronized directly to local host directory `~/.claude/skills/andino-workflow/skills/decision-map/`.
- [x] Git committed and pushed to `origin/andino-workflow`, verified compatible with `ai-rules setup`.

## Scope

### In Scope
- `skills/decision-map/SKILL.md`
- `skills/decision-map/GUIDE.md`
- `skills/decision-map/resources/map-and-ticket-protocols.md`
- `skills/decision-map/resources/gh-adapter.md`
- `skills/decision-map/resources/worked-example.md`
- `skills/brainstorming/SKILL.md` & `GUIDE.md` (cross-wiring references)
- `references/legal/provenance.md`
- Host synchronization to `~/.claude/skills/andino-workflow/skills/decision-map/`
- Verification with `ai-rules setup`

### Out of Scope
- Modifying unrelated Andino skills.
- Introducing external third-party python or npm packages.
- Directly mutating remote GitHub issues without user request.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Epistemic Entropy Reduction**: Decision maps navigate uncharted uncertainty rather than tracking feature production. The core invariant is *"Produce decisions, not deliverables"*.
- **Single-Canvas Default**: Centralizing map state in `map.md` with inline tickets prevents file sprawl, context thrashing, and token tax. Standalone ticket files are reserved for deep AFK investigations.
- **Empirical Evidence Floor**: `research` tickets cannot be resolved without concrete evidence (diffs, verified code paths, or primary citations).
- **Zero-Dependency Local-First**: Core mechanics run 100% offline via standard Markdown and Python stdlib; `gh` CLI is strictly an optional adapter.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **File Sprawl vs. Single Ledger**:
   - *Risk*: Spreading tickets into dozens of `.md` files creates massive I/O churn and context fragmentation for agents.
   - *Resolution*: Default to a single-canvas `map.md` holding inline tickets in a structured section; allow standalone files in `tickets/` only when deep research logs require isolation.
2. **Dual-Master Synchronization Drift**:
   - *Risk*: Simultaneous mutations to local markdown and remote GitHub Issues create split-brain state.
   - *Resolution*: Markdown in the repository is the authoritative single source of truth. The `gh` adapter is an export/mirror tool, never an authoritative dual master.
3. **Infinite Analysis Paralysis**:
   - *Risk*: Agents loop indefinitely splitting decisions without ever reaching implementation.
   - *Resolution*: Implement a circuit breaker: maximum 3-5 active frontier tickets, mandatory convergence handoff to `andino-planning`, and maximum 1 cross-wiring bounce before human input is required.

### Hal Terlewat (Blind Spots Addressed)
- **Strawman Alternative Detection**: Rules enforcing genuine trade-offs rather than manufactured fake options.
- **Cycle Detection**: Topological DAG validation in the operational example ensuring circular dependencies are trapped cleanly.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Specification & Architecture Design | COMPLETED | Council synthesis & durable execution plan | `docs/exec-plans/active/decision-map-elevation.md` | Plan documented & accepted |
| Phase 2 — Supporting Resources Authoring | COMPLETED | Create protocols, adapter, and worked example | `skills/decision-map/resources/*` | `map-and-ticket-protocols.md`, `gh-adapter.md`, `worked-example.md` created |
| Phase 3 — Core Skill & Guide Elevation | COMPLETED | Author high-density SKILL.md and deep craft GUIDE.md | `skills/decision-map/SKILL.md`, `GUIDE.md` | `SKILL.md` (<150 lines) & `GUIDE.md` (>170 lines) elevated |
| Phase 4 — Cross-Wiring & Provenance | COMPLETED | Bridge with brainstorming and update legal notice | `skills/brainstorming/*`, `references/legal/provenance.md` | Bidirectional cross-wiring and provenance updated |
| Phase 5 — Verification, Host Sync & Delivery | COMPLETED | Run test script, sync to ~/.claude, verify setup, commit & push | Python test, host sync, git push | Offline tests passing (exit 0/1), host synced, pushed to remote |
