# In-Flight ADR and Domain Glossary Protocols

Internal resource for `andino-brainstorming`. Adapts and elevates `mattpocock/skills:engineering/grill-with-docs` and `domain-modeling`.

---

## 1. The In-Flight Documentation Philosophy

Architectural Decision Records (ADRs) and Domain Glossaries must not be post-hoc administrative chores. They are captured **in-flight** as decisions resolve during the discovery dialogue, then emitted as persistent artifacts once mutual consensus is reached.

### The Lazy Emission Rule
- **During the Dialogue**: Track ADR candidates and emerging domain vocabulary in the agent's latent mental model. Reflect settled decisions succinctly in chat checkpoints.
- **Upon Design Consensus**: Persist an ADR for consequential decisions and a glossary for terms whose meaning affects behavior. Use the agreed project location or append them to the design specification.
- **Anti-Pattern**: Emitting sprawling Markdown document files mid-turn before the user has agreed to the core direction.

---

## 2. Canonical ADR Schema

When an architectural decision resolves during brainstorming, format it using this schema:

```markdown
# ADR-0001: [Short Title of Decision]

- **Status**: Accepted
- **Date**: YYYY-MM-DD
- **Decision Makers**: [User, Agent]
- **Target Path**: Architectural

### Context
[What was the core problem, user goal, and technical forces? What constraints shaped this problem?]

### Decision
[What is the chosen approach, pattern, or architectural direction? State it directly in active voice.]

### Alternatives Considered & Trade-offs
1. **[Chosen Option]**:
   - *Pros*: [Direct alignment with goal, minimal complexity, etc.]
   - *Cons / Costs*: [Specific trade-off accepted]
2. **[Alternative Option A]**:
   - *Pros*: [Why someone might choose it]
   - *Why Rejected*: [Binding constraint violated, disproportionate cost, or anti-goal]
3. **[Alternative Option B]**:
   - *Pros / Why Rejected*

### Consequences & Invariants
- **Positive**: [What becomes easier or reliable]
- **Negative**: [What overhead, migration, or limitation is incurred]
- **Floor Invariants**: [Non-negotiable constraints downstream executors must hold]
```

---

## 3. Domain Glossary Schema (Ubiquitous Language)

To prevent semantic drift between the user's intent, the architectural spec, and the code written by downstream executors (TDD/Implementation), capture new or overloaded terms using this table:

```markdown
### Domain Glossary

| Domain Term | Canonical Definition | Anti-Terms (Do NOT Use) | Code Representation |
|---|---|---|---|
| **Session** | A continuous connection lifecycle between CLI and runtime. | "Connection", "Instance", "Worker" | `SessionContext` (`session.py`) |
| **Frontier** | The unblocked set of decision DAG nodes whose parents are resolved. | "Queue", "Pending List", "Backlog" | `DecisionFrontier` (`frontier.py`) |
| **Ratcheted Floor** | A quality metric threshold that can never be weakened without an ADR. | "Lint rule", "Warning", "Suggestion" | `FloorGuard` (`guard.py`) |
```

### De-Aliasing Rules:
1. **One Concept, One Name**: If the user calls an entity an "account", but the code calls it "workspace", resolve the ambiguity during the interview and record the canonical name in the glossary.
2. **Anti-Terms**: Explicitly document words that must **not** be used interchangeably. Semantic ambiguity in specifications is the #1 cause of downstream implementation defects.

---

## 4. Integration with Downstream Skills

The output of `grill-with-docs` serves as the explicit input for the next workflow phases:

- **andino-planning**: Consumes the ADR's chosen approach and constraints to decompose tasks without re-evaluating rejected alternatives.
- **andino-tdd**: Consumes the Domain Glossary to name test fixtures, assertions, and domain entities accurately.
- **andino-code-review**: Consumes the ADR's *Consequences & Invariants* to verify that pull requests respect the agreed architectural boundaries.
