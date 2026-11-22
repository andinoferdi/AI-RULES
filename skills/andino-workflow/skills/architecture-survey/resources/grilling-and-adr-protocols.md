# Grilling Loop and ADR Protocols

Internal method ID: `architecture-survey`. Supporting resource for `skills/architecture-survey`.

This resource defines the interactive deliberation protocol (*grilling loop*), domain glossary synchronization, durable ADR recording, and handoff to interface design once the user selects a candidate.

---

## 1. Interactive Decision Grilling Loop

Once the HTML report is generated and the user selects a candidate, do not immediately write implementation code. Transition into an interactive decision grilling session to stress-test the proposal:

1. **Verify Seam Justification:**
   - Apply the Two-Adapter Rule: Will this seam have at least two concrete adapters (e.g. production database adapter and in-memory test fake)? If only one adapter will ever exist, challenge whether the seam is hypothetical bloat.
2. **Clarify Encapsulation Boundaries:**
   - Exactly what state, validation, and side-effects will be absorbed inside the deep module?
   - What becomes private? What single public method or interface remains exposed?
3. **Audit Test Survival:**
   - Which brittle unit tests mocking internal wrappers can be deleted?
   - What high-value end-to-end or integration tests will assert behavior against the new public seam?
4. **Evaluate Blast Radius:**
   - How many callers are impacted? Can callers be migrated incrementally via a backward-compatible facade, or is an atomic cutover required?

---

## 2. Domain Glossary Synchronization (`GLOSSARY.md`)

Architectural seams must speak the language of the business domain, not incidental technology layers:

- **Naming a Deepened Module:** If a deepened module introduces a domain concept not currently defined in `GLOSSARY.md`, add the term immediately. Create `GLOSSARY.md` lazily if it does not yet exist.
- **Refining Fuzzy Terms:** If the grilling discussion sharpens the definition of an ambiguous term, update `GLOSSARY.md` in place.
- **Example:** If `GLOSSARY.md` defines an "Order", name the module `OrderIntake` or `OrderBook`, never `OrderService`, `OrderHandler`, or `OrderManager`.

---

## 3. Durable ADR Recording for Rejected Proposals

When a user rejects an architecture survey candidate, distinguish between ephemeral hesitation and enduring architectural constraints:

### A. Ephemeral Reasons (Do NOT record an ADR)
- *"Not right now; we have a tight deadline."*
- *"We don't have time to refactor this sprint."*
- *"I agree it's shallow, but let's revisit next quarter."*
These are transient scheduling decisions. Do not pollute `docs/adr/` with backlog notes.

### B. Enduring Reasons (Record an ADR)
- *"We cannot consolidate OrderValidator and OrderPricing because pricing rules must execute in a separate isolated WASM sandbox for regulatory compliance."*
- *"We must keep this database wrapper separated because an external enterprise customer requires swapping out the persistence engine for custom SAP backends."*

### C. The ADR Offer Prompt
When an enduring constraint is voiced, prompt the user:
> *"Want me to record this as an Architecture Decision Record (ADR) so future architecture surveys do not re-suggest this consolidation?"*

### D. ADR Template (`docs/adr/ADR-xxxx-<slug>.md`)
```markdown
# ADR-{{id}}: Reject consolidation of {{subsystem_name}}

## Status
Decided

## Context
An architecture survey proposed consolidating {{shallow_wrappers}} into a deep {{target_module}} to improve locality and testability.

## Decision
We deliberately retain the separation of {{module_a}} and {{module_b}}.

## Consequences
- **Positive:** Preserves {{enduring_constraint_benefit}} (e.g. WASM sandbox isolation).
- **Negative:** Callers retain the coordination burden of managing both modules independently.
- **Guidance:** Future architecture surveys must not propose collapsing this seam unless the aforementioned constraint is retired.
```

---

## 4. Handoff to Interface Design

Once the candidate direction and constraints are crystallized through grilling:
1. Do not start hacking product files directly.
2. Seamlessly transition to `andino-api-and-interface-design` (or `deep-module-design`).
3. Leverage the **Design-It-Twice** pattern: dispatch two parallel subagents to generate competing interface proposals under contrasting constraints (e.g., Option A: Command/Receipt pattern vs Option B: Fluent state machine), then synthesize the superior contract.
