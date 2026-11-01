# Design-It-Twice Protocols

This resource defines the parallel subagent exploration protocol for designing alternative deep module interfaces. Based on John Ousterhout's *Design It Twice* principle: your initial interface design is rarely your best because it inherits the structural biases of the existing codebase.

---

## 1. Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          DESIGN-IT-TWICE WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 1. FRAME PROBLEM SPACE    ──▶ Extract constraints, dependencies, & sketch code │
│ 2. SPAWN DIVERGENT AGENTS ──▶ 3-4 parallel subagents with conflicting briefs    │
│ 3. STRUCTURED SYNTHESIS   ──▶ Score on Leverage, Locality, & Seam Placement     │
│ 4. OPINIONATED HYBRID     ──▶ Recommend superior candidate or clean synthesis   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Step 1: Frame the Problem Space

Before generating any interfaces or launching subagents, construct a grounded, user-visible problem brief:

1. **The Friction**: Which callers are currently repeating policy, orchestrating multiple shallow helpers, or leaking internal state?
2. **The Constraints**: What invariants, performance budgets, and error guarantees must any viable interface satisfy?
3. **The Dependency Classification**: Classify all dependencies into the 4 categories (In-process, Local-substitutable, Remote-owned, True external) per `dependency-and-seam-discipline.md`.
4. **Illustrative Grounding Sketch**: A 10-20 line snippet showing how callers are currently forced to interact with the fragmented code. This is *not* a proposal—it grounds the constraints in concrete reality.

---

## 3. Step 2: Spawn Divergent Subagents

Launch 3 to 4 independent subagents with fresh context windows. Each subagent is assigned a radically different architectural objective:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      PARALLEL EXPLORATION FLEET                        │
├───────────────────┬────────────────────────────────────────────────────┤
│ Subagent Lens     │ Architectural Directive                            │
├───────────────────┼────────────────────────────────────────────────────┤
│ Agent 1: Minimal  │ 1-3 entrypoints max. Hide all configuration.       │
│ Agent 2: Flexible │ Pluggable strategies, lifecycle hooks, extension. │
│ Agent 3: Common   │ Zero-config for 90% common case, optional escape.  │
│ Agent 4: Ports    │ Hexagonal ports & adapters for cross-seam network. │
└───────────────────┴────────────────────────────────────────────────────┘
```

### Prompt Brief Specifications

Each subagent prompt must contain:
1. **Repository Context**: Bounded file paths and domain vocabulary from the project glossary.
2. **Technical Constraints**: Data types, persistence requirements, and concurrency rules.
3. **The Specific Directive**:
   - **Agent 1 (Minimalist)**:
     > *"Design the most compact interface possible. Target at most 1 to 3 public functions. Maximize leverage: callers should accomplish complex domain tasks with a single function call. Push all configuration, validation, and sequencing behind the seam."*
   - **Agent 2 (Flexible / Extensible)**:
     > *"Design an interface optimized for extension and variability. Expose explicit strategy hooks, middleware, or policy objects. Allow callers to customize internal decisions while keeping the core engine behind the seam."*
   - **Agent 3 (Common-Case Simplicity)**:
     > *"Optimize ruthlessly for the 90% common-case caller. The standard invocation must require zero configuration and minimal arguments. Provide an options bag or fluent builder only as an escape hatch for the 10% advanced cases."*
   - **Agent 4 (Ports & Adapters - when network/external I/O is involved)**:
     > *"Design around strict Ports & Adapters. Define clean domain-shaped ports at the boundary. Provide a concrete in-memory adapter for testability and an infrastructure adapter for production."*

### Mandatory Subagent Output Contract

Every subagent must return its design adhering strictly to this 6-part schema:

```markdown
### 1. Interface Signature & Types
[Exact signatures, parameter objects, return types, and exceptions]

### 2. Invariants & Error Semantics
[Ordering constraints, validation rules, and error recovery behaviors]

### 3. Caller Usage Examples
[2 realistic code snippets showing standard and advanced call sites]

### 4. Hidden Internals
[List of internal helpers, state machines, and caches hidden behind the seam]

### 5. Dependency & Adapter Strategy
[Exact ports, in-memory fakes, and local stand-ins used]

### 6. Trade-Off Analysis
- Leverage: High / Moderate / Low (justification)
- Locality: High / Moderate / Low (justification)
- Fragility / Complexity risks
```

---

## 4. Step 3: Comparative Synthesis Rubric

Once all subagents return, do not simply dump their outputs on the user. Evaluate the candidates across the **4 Deep Dimensions**:

```
┌───────────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ EVALUATION DIMENSION  │ 1. Minimal  │ 2. Flexible │ 3. Common   │ 4. Ports    │
├───────────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Caller Leverage       │ Highest     │ Moderate    │ High        │ High        │
│ Maintainer Locality   │ Highest     │ Moderate    │ High        │ Highest     │
│ Surface Area (Simp.)  │ 1-2 methods │ 6+ methods  │ 2 methods   │ 3 methods   │
│ Testing Ergonomics    │ Direct      │ Complex     │ Direct      │ In-Memory   │
│ Speculative Risk      │ Lowest      │ High        │ Low         │ Low         │
└───────────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

### Rubric Questions
1. **Leverage Test**: How many discrete concepts must a caller understand before they can invoke this interface correctly? (Fewer concepts = higher depth).
2. **Deletion Test**: If we delete this module, does complexity disappear or distribute across callers?
3. **Seam Placement**: Are the seams justified by at least two concrete adapters, or is this speculative layering?
4. **AI-Navigability**: Can an autonomous coding agent read this interface signature in a prompt and use it correctly without reading the implementation?

---

## 5. Step 4: The Opinionated Hybrid Recommendation

A great architectural review does not present a passive menu; it delivers an authoritative verdict:

1. **State the Winner**: Name the strongest candidate and justify why it provides the highest leverage.
2. **Graft the Best Ideas**: Incorporate high-value elements from runners-up (e.g., take the minimal single-entrypoint interface from Agent 1, but graft the zero-config default options from Agent 3).
3. **Explicit Rejections**: State plainly which parts of the other candidates were rejected and why (e.g., *"Agent 2's builder pattern was rejected because it introduces 5 new classes for variation that does not currently exist"*).
4. **Concrete Migration Path**: Outline the exact sequence for introducing the new interface, migrating callers, and deleting old shallow tests.
