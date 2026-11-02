# Architecture Survey: Deep Craft Guide

Internal method ID: `architecture-survey`. Authoritative craft guide for `skills/architecture-survey`.

---

## 1. Core Philosophy: Deep vs Shallow Modules

The objective of an architectural survey is not to produce theoretical taxonomies or celebrate "clean architecture" abstractions. It is to surface real maintainability and testability friction in active code and propose **deepening opportunities**: refactoring shallow, fragmented wrappers into deep, high-leverage modules.

### The Problem with Shallow Modules
A shallow module has an interface nearly as complex as its implementation. When a system decomposes operations into dozens of tiny single-function classes or pass-through wrappers:
1. **Locality is destroyed:** Business rules, validation, and invariant enforcement scatter across disparate files. Understanding one operation requires jumping across multiple directories.
2. **Defects hide in caller coordination:** Real production bugs rarely lurk inside pure, atomized helper functions; they hide in the inconsistent ways callers stitch those helpers together.
3. **Tests become mock-heavy and brittle:** Unit tests must mock 4 or 5 intermediate wrappers just to assert that a single business operation executed, coupling tests to ephemeral internal plumbing.

### The Power of Deep Modules
A deep module provides a powerful, high-leverage implementation behind a simple, stable public interface.
- **High leverage:** Callers invoke one cohesive method (`submitOrder`) and are shielded from transactional lifecycles, database locks, tax math, and event dispatching.
- **The interface is the test surface:** Callers test meaningful business outcomes against the public contract without reaching into private internals or mocking internal helper methods.
- **Invariants concentrate:** State transitions and business constraints are enforced centrally in the module, making invalid states unrepresentable.

---

## 2. The 6-Phase Operational Procedure

```
[1. Scope & Churn] ──► [2. Organic Friction Walk] ──► [3. Structure Candidates]
                                                              │
                                                              ▼
[6. Carry into Plan] ◄─── [5. Grilling & ADR Loop] ◄─── [4. Hybrid HTML Report]
```

### Phase 1: Scope Before Scanning (YAGNI & Hotspots)
Never scan an entire repository without bounding attention. Deepening a module pays dividends by making future modifications simpler and safer; refactoring dormant, stable code yields zero or negative ROI.
- **If a subsystem or pain point is named:** Immediately bound investigation to that target directory, its immediate callers, and its test suite.
- **If no target is named:** Inspect recent commit churn using `rtk git log --oneline -n 100`. Identify files and directories that change frequently. Let code churn guide investigation.
- **Consult constraints:** Check `GLOSSARY.md` for accepted domain language and `docs/adr/` for settled architectural decisions to avoid re-litigating settled trade-offs.

### Phase 2: Organic Friction Walk with Fresh Subagent
Dispatch a subagent with an isolated context window to walk the bounded codebase without preconceptions (see [resources/subagent-exploration-brief.md](resources/subagent-exploration-brief.md)).
- Walk callers and implementations: note where understanding one concept forces jumping across 4+ small files.
- Spot caller-side policy duplication: where multiple callers perform identical validation, transaction setup, or parameter mapping before calling a downstream dependency.
- Detect leaky seams: where callers must pass or manage database connection handles, ORM transaction contexts, or transport-specific types.
- **Apply the Deletion Test:** For every suspected wrapper, ask: *"If this module were deleted, would complexity vanish or merely disperse back into callers?"*
  - If complexity concentrates into one cohesive place, the wrapper is shallow and ripe for deepening.
  - If complexity scatters across disparate callers, the seam is load-bearing and must be preserved.

### Phase 3: Structure Candidate Deepening Proposals
Synthesize findings into crisp, structured candidate proposals using strictly the 10 canonical terms (see [resources/architectural-vocabulary.md](resources/architectural-vocabulary.md)):
- **Title:** Action-oriented deepening statement (e.g. *"Collapse Order Intake Pipeline"*).
- **Recommendation Strength:** `Strong` (high churn, blatant shallowness), `Worth exploring` (moderate leverage), or `Speculative` (lower frequency, trade-offs present).
- **Dependency Classification:** `in-process`, `local-substitutable`, `ports & adapters`, or `mock`.
- **Problem:** Exactly one sentence stating what hurts today.
- **Solution:** Exactly one sentence describing the structural consolidation.
- **Wins:** Bullet points ($\le 6$ words each) formatted as `[Glossary Category]: [Claim]`.
- **ADR Callout:** Flag existing ADR contradictions only if concrete friction warrants reopening the decision.

### Phase 4: Generate and Deliver the Hybrid HTML Report
Write a single self-contained HTML file to the OS temporary directory (`$TMPDIR` or `%TEMP%`, e.g. `architecture-survey-<timestamp>.html`) to prevent repository pollution (see [resources/html-report-scaffold.md](resources/html-report-scaffold.md)).
- Use the **Hybrid Report Scaffold**: load Tailwind CSS and Mermaid via CDN for rich rendering when online, with embedded fallback CSS and inline SVG geometry for offline or air-gapped resilience.
- Provide a side-by-side **Before / After diagram** (~320px height) for every candidate, selecting the most expressive visual pattern from [resources/diagram-patterns.md](resources/diagram-patterns.md):
  1. *Mermaid graph:* Call flows, sequence round-trips, and leaky seams (`#dc2626`).
  2. *Hand-built boxes-and-arrows (CSS/SVG):* Deep module consolidation with faded internals.
  3. *Cross-section:* Collapsing multiple thin horizontal layers into one solid band.
  4. *Mass diagram:* Interface width shrinking relative to deep implementation volume.
  5. *Call-graph collapse:* Nested call trees consolidated behind a single public seam.
- Include a **Top Recommendation** card highlighting the highest-ROI opportunity.
- Launch the file in the default browser (`start` on Windows, `open` on macOS, `xdg-open` on Linux) and print the absolute path in chat alongside a terminal-native Executive Summary Card.

### Phase 5: Interactive Grilling Loop and Domain Synchronization
Do NOT immediately draft implementation code or refactor product files. Prompt the user: *"Which of these candidates would you like to explore?"*
- Walk through the grilling loop (see [resources/grilling-and-adr-protocols.md](resources/grilling-and-adr-protocols.md)): challenge whether the seam satisfies the Two-Adapter Rule, verify what state/validation is encapsulated, and audit test survival.
- **Domain alignment:** If a deepened module introduces a new domain concept, update or lazily create `GLOSSARY.md`.
- **Durable ADR recording:** If the user rejects a candidate for an enduring architectural reason (e.g. regulatory isolation), offer to record an ADR so future surveys do not re-suggest it.
- Seamlessly transition into `andino-api-and-interface-design` for interface specification using the Design-It-Twice pattern.

### Phase 6: Carry Selected Candidate into the Execution Plan
Record the chosen candidate, affected files, public interface seam, and migration strategy into the active Andino execution plan checkpoint (`docs/exec-plans/active/<ticket>.md`).

---

## 3. Modular Resource Index

This skill organizes its specialized techniques into 6 focused resources:

| Resource | Purpose |
| :--- | :--- |
| [resources/architectural-vocabulary.md](resources/architectural-vocabulary.md) | 10 canonical terms, prohibited substitution table, output shaping rules, and deletion test criteria. |
| [resources/diagram-patterns.md](resources/diagram-patterns.md) | 5 Before/After visual diagram patterns (~320px height) in Mermaid and CSS/SVG. |
| [resources/html-report-scaffold.md](resources/html-report-scaffold.md) | Progressive enhancement HTML scaffold (CDN + offline fallback) and delivery protocols. |
| [resources/subagent-exploration-brief.md](resources/subagent-exploration-brief.md) | Prompt templates and operational invariants for isolated subagent exploration. |
| [resources/grilling-and-adr-protocols.md](resources/grilling-and-adr-protocols.md) | Post-survey decision grilling, glossary synchronization, and durable ADR recording. |
| [resources/worked-example.md](resources/worked-example.md) | Comprehensive Order Intake case study with before/after code and invariant checks. |

---

## 4. Ownership and Non-Destructive Invariants

- **Read-Only Investigation:** The architecture survey phase is strictly non-destructive. Product files, Git tracking state, and project configurations are never modified during a survey.
- **Temporary Storage Only:** Generated HTML reports are written exclusively to `$TMPDIR` / `%TEMP%`.
- **Single Plan Checkpoint:** All accepted directions are recorded in the active Andino execution plan checkpoint, maintaining continuity across session boundaries without memory fragmentation.
