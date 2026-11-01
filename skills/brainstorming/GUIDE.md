# Brainstorming & Decision Refinery: Craft Guide

Internal method ID: `andino-brainstorming` (alias: `brainstorming`). Stable technique adapted to Andino Workflow governance. Consolidates and elevates `decision-interview`.

---

## 1. Operational Architecture: Divergent Exploration to Convergent Grilling

Brainstorming turns ambiguous goals into builder-ready designs without guessing user intent. It resolves the classic tension between **divergence** (expanding the solution space) and **convergence** (eliminating unviable options) by structuring discovery into four discrete, ordered phases:

```
┌─────────────────────────┐
│ 1. Intent & Buzzwords   │ ──▶ Uncover unvarnished motivation; confidence score <70%.
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 2. Three-Path Scoping   │ ──▶ Spike vs. Bounded vs. Architectural (governance matches risk).
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 3. Frontier Grilling    │ ──▶ Relentless DAG frontier questioning with reasoned defaults.
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 4. Specs, ADRs & Terms  │ ──▶ Lazy emission of ADRs, Domain Glossary, and Builder Spec.
└─────────────────────────┘
```

---

## 2. Phase 1: Intent Hypothesis & De-buzzwording

### The Intent Hypothesis
Before proposing approaches, formulate a single-sentence hypothesis of the desired outcome and assign an explicit confidence score:
- If confidence is `< 70%`, explicitly enumerate what is unknown (persona, scale, latency, security boundary, operational limits).
- Distinguish discoverable repository facts (inspectable directly from code/configs) from user-owned decisions. Never interrogate the user on facts that can be read from files.

### De-buzzwording Rule
Users frequently describe intent using generic industry buzzwords ("scalable", "enterprise-grade", "flexible", "intuitive"). These abstractions conceal architectural risk:
- Challenge every adjective with a concrete operational scenario: *"What breaks first under load?"*, *"Whose workflow fails if this is missing?"*
- Convert adjectives into observable acceptance metrics before designing subsystems.

---

## 3. Phase 2: Friction-Proportional Three-Path Scoping

Governance must match epistemic risk. Announce the classification aloud at the start:

### 1. Spike (Throwaway Feasibility Probe)
- **Trigger**: Feasibility questions (*"Can we...", "Is it possible to...", "Spike out X"*).
- **Process**: Formulate question and 2-sentence probe plan; get a quick nod; execute as cheaply as possible.
- **Output**: An empirical answer and recommendation. Anything built remains strictly labeled throwaway. No spec file, no ADR.

### 2. Bounded (Scoped Edit to Existing Flow)
- **Trigger**: Changes to existing code, flags, one-file fixes, or localized endpoints where the affected flow already exists.
- **Process**: Inspect current code; ask only 1-2 clarifying questions if necessary; present a concise in-chat design (approach, files touched, test assertion); **STOP and wait for explicit approval**.
- **Output**: In-chat approval. Proceeds directly to TDD implementation. No external spec or planning doc.

### 3. Architectural (New Subsystems, Altered Interfaces, New Domains)
- **Trigger**: New repositories, new multi-file components, altered database models, or changes that restructure how subsystems interact.
- **Process**: Full frontier grilling, 2-3 alternative approaches with trade-off matrices, lazy in-flight ADR capture, and builder-ready specification.
- **Ratchet Rule**: One-way complexity ratchet. If a Bounded task uncovers hidden architectural friction, announce the escalation immediately and upgrade to Architectural. Tasks never downgrade mid-flight.
- **Multi-Session Decision Mapping Escalation**: If an Architectural exploration uncovers that the initiative cannot be resolved within a single session, or involves multiple branching technical forks (e.g., storage engine, auth protocol, cutover strategy), escalate directly to `andino-decision-map` (`skills/decision-map/SKILL.md`). `andino-decision-map` structures the multi-session effort into an explicit map (`map.md`), unblocking research tickets, and fog of war, preventing premature implementation while managing multi-session durability.

---

## 4. Phase 3: Frontier-Based Relentless Grilling

Adapts Matt Pocock's `grilling` and Addy Osmani's `interview-me`:

### The Decision DAG & Unblocked Frontier
Discovery decisions form a Directed Acyclic Graph (DAG). Dependencies must be respected:
- Identify the **unblocked frontier**: the set of decision nodes whose parent choices have all been resolved.
- Ask questions **only** on the active frontier. Asking about low-level leaf details while the root architecture remains undecided is prohibited.

### The 1-Question Turn Contract
Every grilling turn must maintain high cognitive momentum:
1. **Context Anchor**: 1 sentence summarizing the current fact or previous answer.
2. **Discriminating Question**: Exactly one focused question probing the live decision frontier.
3. **Reasoned Default Recommendation**: Always propose a high-conviction default with technical justification:
   *"Recommended default: [Option A] because [concrete reason]. Reply 'agree' (or press Enter) to confirm, or provide your constraint."*

### Fatigue Breakers & Impatience Detection
Interrogation must never become an interrogation trial:
- Never exceed 3 sequential questions on the same architectural branch without a checkpoint.
- If the user provides terse answers (`< 10` words) or expresses impatience, immediately halt 1-question dialogue, summarize all remaining frontier nodes in a table with recommended defaults, and seek single-turn bulk consensus.

---

## 5. Phase 4: In-Flight Documentation & Lazy Emission

Adapts `mattpocock/skills:engineering/grill-with-docs` and `domain-modeling`:

### Lazy Emission
- Track emerging decisions and domain terminology mentally during the dialogue.
- Do not clutter turns with verbose Markdown files mid-interview.
- Once design consensus is reached, formally emit:
  1. **Architectural Decision Record (ADR)**: Context, Decision, Alternatives Considered, Trade-offs, Consequences, and Floor Invariants.
  2. **Domain Glossary**: Ubiquitous language mapping, anti-terms (confusing synonyms to avoid), and code-level symbol mappings.
  3. **Builder-Ready Design Specification**: Stored under `docs/specs/YYYY-MM-DD-<topic>-design.md`.

### Deterministic Exit Conditions
Terminate the discovery interview when:
1. All material nodes on the decision frontier are resolved; OR
2. The agent achieves **3-Question Predictability** (>90% certainty on the user's reaction to the next 3 hypothetical questions).

---

## 6. Anti-Rationalization Refutations

| Rationalization Shortcut | Required Operational Response |
|---|---|
| *"The task is simple, I'll skip the path classification."* | Every request must be classified into Spike, Bounded, or Architectural before implementation code is written. |
| *"I already know how to implement this, no need to interview."* | Knowing a solution does not equal knowing the user's operational constraints, scale, or anti-goals. Validate the hypothesis. |
| *"I'll dump 5 questions at once to save turns."* | Cognitive flooding causes shallow answers. Ask exactly 1 question on the active frontier with a recommended default. |
| *"I'll start scaffolding while they review the design."* | Hard gate violation. Zero code, scaffolding, or dependency installation before explicit design consensus. |
| *"The user gave a one-word answer, so I'll keep interrogating."* | Terse answers trigger the Fatigue Breaker: halt questioning, present remaining defaults in a table, and request bulk confirmation. |
| *"I will write the ADR file before we agree on the approach."* | Premature formalization anchors on unverified assumptions. Use lazy emission: emit ADRs only after consensus. |
| *"The user asked for a quick script, I'll create a full ADR and spec."* | Governance must match risk. Spikes and small bounded fixes do not get formal ADR files. |
| *"I will ask the user which files need to be changed."* | Inspect discoverable repository facts directly. Never ask users to enumerate files or commands you can read. |

---

## 7. Diagnostic Red Flags (Stop Immediately)

1. **Premature Implementation**: Agent starts editing code or running scaffold commands before the user confirms the design.
2. **Checklist Theater**: Agent recites a static generic questionnaire instead of following the decision DAG frontier.
3. **Empty Recommendations**: Agent asks open-ended exam questions without providing a reasoned default option.
4. **Bureaucratic Flooding**: Agent generates 100-line Markdown documents for a one-line bug fix.
5. **Ignoring Codebase Evidence**: Agent asks the user what frameworks or database versions are used instead of inspecting `package.json`, `pyproject.toml`, or configuration files.
6. **Endless Drift**: Agent continues asking questions after 3-question predictability has been achieved.

---

## 8. Handoff to Downstream Skills

- **andino-planning**: Receives the approved Builder-Ready Design Spec, ADR, and unblocked frontier to produce an executable, dependency-ordered task plan.
- **andino-tdd**: Uses the Domain Glossary and Floor Invariants to author failing test assertions (RED) before writing code.
- **andino-code-review**: Verifies that the delivered PR adheres strictly to the ADR's *Consequences & Invariants*.

---

## 9. Provenance & Attribution

This skill adapts operational techniques and structural patterns from:
- `addyosmani/agent-skills:skills/interview-me` (MIT License, Addy Osmani 2025)
- `mattpocock/skills:skills/productivity/grilling`, `grill-me`, and `engineering/grill-with-docs` (MIT License, Matt Pocock 2026)
- `obra/superpowers:skills/brainstorming` (MIT License, Jesse Vincent 2025)

Upstream repositories serve as provenance. All code and operational contracts are independently implemented for Andino Workflow governance.
