# Concept Grounding Graph and Gap Naming Protocol

Internal method ID: `andino-article-shaping/concept-grounding-graph`.

This resource details the formal concept dependency discipline and the protocol for handling missing empirical evidence without fabrication.

---

## 1. The Grounding Invariant

A reader experiences cognitive friction whenever an article relies on a concept before that concept has been introduced and anchored. 

To make this verifiable, article shaping models concept flow as a Directed Acyclic Graph (DAG):

1. **Audience Prerequisites ($P$):** The baseline concepts that the target reader brings to the table prior to reading.
   - Example (Senior Backend Engineer): `HTTP requests`, `SQL queries`, `thread pools`.
   - Example (Non-Technical Executive): `cash flow`, `customer churn`, `quarterly burn`.
2. **Current Grounded Set ($G_t$):** The cumulative set of all grounded concepts at turn $t$.
   $$G_0 = P$$
   $$G_{t+1} = G_t \cup \text{grounds}(\text{beat}_t)$$
3. **Reachability Guard:** A candidate beat $\text{beat}_k$ may be proposed or drafted if and only if:
   $$\text{requires}(\text{beat}_k) \subseteq G_t$$
4. **Cognitive Invariant:** A beat cannot introduce an ungrounded concept $X$ into an argument unless that beat's explicit job is to introduce and ground $X$.

---

## 2. Resolving Reachability Blockers

When a tempting point requires concept $X$ but $X \notin G_t$, do **not** leap over the gap. The model must choose one of three explicit remedies:

| Remedy | Mechanism | Tradeoff |
| :--- | :--- | :--- |
| **Insert Grounding Beat** | Author an explicit prior beat whose sole job is to establish $X$. | Preserves accessibility; consumes pacing tokens. |
| **Promote to Prerequisite** | Ask author if target audience already understands $X$ ($P \leftarrow P \cup \{X\}$). | Keeps article fast; excludes novice readers. |
| **Rephrase via Grounded Terms** | Express the insight using existing concepts in $G_t$ without naming $X$. | Slightly less technical; zero cognitive friction. |

---

## 3. The "Name the Gap" Protocol (Zero Hallucination)

AI models have a notorious tendency to fabricate case studies, invent company names, or synthesize fake statistics when an argument feels incomplete.

In `andino-article-shaping`, this behavior is an absolute violation of the Floor Invariants.

### When Lived Evidence is Missing
If an argument requires:
- A real metric (*"How much did latency actually drop?"*)
- A concrete failure story (*"When did this break in production?"*)
- A direct quote or personal perspective

The agent must halt and **name the gap** explicitly:

```markdown
[GAP: We need a concrete lived example here. What happened the first time your team ran this migration? Give me the detail now, or we reframe the section without the personal anecdote.]
```

### The Three Laws of Evidence Preservation
1. **Never Invent Names or Metrics:** If the raw notes do not say 42%, do not write 42%.
2. **Never Synthesize Quotes:** Do not attribute words to the author that they never said.
3. **Never Fabricate War Stories:** If the notes describe an abstract architectural flaw, do not invent a fictional 3:00 AM pager incident unless the author confirms it happened.
