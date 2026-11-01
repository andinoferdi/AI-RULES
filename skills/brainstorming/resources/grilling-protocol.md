# Relentless Grilling & Decision Frontier Protocol

Internal resource for `andino-brainstorming`. Adapts and elevates techniques from Matt Pocock (`grilling`, `grill-me`, `grill-with-docs`) and Addy Osmani (`interview-me`).

---

## 1. Core Architecture: The Decision DAG

Discovery and decision interviews are not linear checklists. They form a **Directed Acyclic Graph (DAG)** of architectural dependencies:

```
                  [Root Problem / Intent]
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
     [Architectural Path]          [Execution Constraint]
        ┌─────┴─────┐                       │
        ▼           ▼                       ▼
   [Option A]   [Option B]            [Boundaries]
        │
   ┌────┴────┐
   ▼         ▼
[Leaf 1]  [Leaf 2]
```

### The Unblocked Frontier
- **Definition**: The set of decision nodes whose prerequisite dependencies have all been resolved.
- **Rule of Locality**: The agent must **only** probe questions located on the current unblocked frontier. Asking questions about `Leaf 1` while `Architectural Path` remains undecided is prohibited.
- **Dynamic Recomputation**: Every user answer prunes invalid branches and dynamically recomputes the new unblocked frontier.

---

## 2. The 1-Question Turn Contract

To avoid cognitive flooding and preserve forward momentum, every interrogation turn must obey this strict contract:

1. **Context Anchor**: 1 sentence summarizing the current fact or previous answer.
2. **Discriminating Question**: Exactly **one** focused question targeting the most critical node on the unblocked frontier.
3. **Reasoned Default Recommendation**:
   - Never ask open-ended exam questions in a vacuum.
   - Always supply the agent's high-conviction recommendation and rationale.
   - *Formula*: `"Recommended default: [Option X] because [concrete reason]. Reply 'agree' (or press Enter) to accept, or steer otherwise."*

---

## 3. Intent Hypothesis & Confidence Scoring

Before deep grilling begins:
1. **State the Intent Hypothesis**: Summarize the perceived core intent in one unvarnished sentence.
2. **Assign Confidence Score**:
   - If confidence is `< 70%`, state exactly which material factors are missing (e.g., target user persona, concurrency load, failure tolerance, budget/deadline).
   - Only probe factors that cannot be discovered by inspecting repository code, configuration, or documentation.

---

## 4. De-buzzwording Taxonomy

Qualitative abstractions conceal architectural hazards. Decompose conventional buzzwords into falsifiable, observable criteria:

| Buzzword | Agent Challenge & Translation | Observable Criterion |
|---|---|---|
| **"Scalable"** | What specific metric breaks first under load? | Target req/sec, p99 latency threshold, data volume growth per month. |
| **"Flexible / Extensible"** | What concrete second use case will be built within 90 days? | Specific plugin interface, alternative storage engine, external API consumer. |
| **"Secure"** | What is the threat model and trust boundary? | Auth provider, tenant isolation mechanism, input sanitization perimeter. |
| **"Fast"** | Fast to build, or fast to execute at runtime? | Time-to-market trade-off vs. sub-50ms endpoint budget. |
| **"Simple"** | Simple for the end-user, or low cognitive load for maintainers? | Minimal UI surfaces vs. zero external dependencies. |

---

## 5. Fatigue Breaker & Circuit Breakers

Interrogation must never become an adversarial inquisitor trial.

- **Sequential Cap**: Never exceed 3 sequential questions on the same architectural branch without delivering a synthesis checkpoint.
- **Impatience Detection**: If the user provides terse answers (`< 10` words), one-word replies ("yes", "sure", "idk"), or signals fatigue:
  1. **Immediately halt** sequential 1-question dialogue.
  2. Synthesize all remaining frontier decisions into a structured **Recommendation Matrix**.
  3. Propose safe, reversible defaults for all remaining nodes.
  4. Ask for a single bulk approval: *"Based on our conversation, I recommend adopting defaults for the remaining items [list]. Shall we lock this design and proceed?"*

---

## 6. Deterministic Exit Conditions

The grilling phase must terminate immediately when **either** of the following conditions is met:

1. **Frontier Exhaustion**: All material user-owned decisions on the DAG are resolved, leaving only implementation-level choices delegated to the builder.
2. **3-Question Predictability**: The agent can confidently state: *"I can predict with >90% certainty how the user would answer the next 3 hypothetical questions on this topic."*

Upon termination, immediately proceed to emit the in-flight ADRs, Domain Glossary, and Builder-Ready Design Specification.
