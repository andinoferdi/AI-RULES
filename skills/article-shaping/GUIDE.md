# Shape raw material into an article: Craft and Reference Guide

Internal method ID: `article-shaping` (alias: `andino-article-shaping`).

This guide details the complete authoring discipline for transforming raw thoughts, unstructured notes, and fragmented observations into a compelling, high-retention essay or article. It combines the rigorous rhetorical architecture of **Writing Beats** with the sculpting mastery and hook craftsmanship of **Writing Shape**.

---

## 1. The Core Philosophy: Grounding & Movement

Weak AI writing suffers from two fatal flaws:
1. **Cognitive Disconnection**: Concepts appear out of nowhere. The reader is hit with ungrounded jargon or abstract principles before understanding why they matter.
2. **Static Homogeneity**: Every paragraph has the same weight, the same tone, and the same length. The writing describes rather than *moves*.

High-craft article shaping fixes this through two non-negotiable disciplines:
- **Concept Grounding**: A strict dependency graph where every new idea builds only on audience prerequisites or previously grounded concepts.
- **Rhetorical Beats**: Pacing the piece as an intentional sequence of dramatic moves where every unit has a single job and produces a tangible state change in the reader.

---

## 2. Anatomy of a Rhetorical Beat

A **beat** is the atomic unit of rhetorical momentum. It can span a single punchy sentence or several interconnected paragraphs, but it must perform **exactly one primary job**.

### The 6 Beat Types

| Beat Type | Primary Job | Emotional / Conceptual Delta | When to Use |
| :--- | :--- | :--- | :--- |
| `scene` | Visceral grounding in physical reality or concrete moment | Observer → Witness | In openings, before abstract theory, or after heavy exposition to re-anchor reality. |
| `claim` | Stating an authoritative argument, rule, or core proposition | Curious → Informed | When establishing the central thesis or key milestone in the argument. |
| `question` | Opening a curiosity gap or destabilizing existing belief | Settled → Questioning | To pull the reader into the next section or challenge accepted dogma. |
| `aside` | Sharing a candid nuance, authorial doubt, or practical boundary | Formal → Intimate | To build trust, address counter-arguments, or prevent misapplication. |
| `pivot` | Executing a sharp directional or conceptual turn | Expectant → Surprised | When revealing the non-obvious solution, twist, or hidden failure mode. |
| `payoff` | Delivering the promised resolution, insight, or lasting punchline | Tense → Satisfied | Climax of a section or concluding note of the entire piece. |

### The Beat State Contract
For every beat drafted, ensure:
1. **Preconditions**: What concepts must the reader already know? If an ungrounded concept is required, pause and insert an introductory beat first.
2. **Grounds**: What new concept, principle, or mental model does this beat permanently establish?
3. **Pacing Delta**: How did the reader's state change? (e.g., from skepticism to realization, or from confusion to clarity).

---

## 3. The 3-Hook Generation Engine

Never begin drafting body paragraphs until the opening hook is deliberately chosen. The opening hook dictates voice, stakes, and narrative velocity.

When presented with raw material, formulate **three genuinely different hooks**, providing **1-2 sentences of full, finished prose** for each:

### Angle 1: Narrative / In Media Res (The Vignette)
- **Mechanism**: Drops the reader directly into a moment of sensory crisis, specific dialogue, or a high-stakes turning point without preamble.
- **Formula**: `[Specific physical setting/timestamp] + [immediate tactile conflict or failure]`.
- **Example**:
  > *"At 3:14 AM on a freezing Tuesday in November, our primary Postgres cluster stopped accepting writes. The issue wasn't disk space or network partitioning—it was a single five-character line in a background worker."*

### Angle 2: Provocative / Counter-Intuitive Claim (The Gauntlet)
- **Formula**: `[Direct refutation of accepted dogma] + [uncomfortable reality]`.
- **Mechanism**: Forces the reader to stop scrolling by declaring that the standard way they do things is fundamentally backwards.
- **Example**:
  > *"Most software teams don't have a communication problem; they have an excess of consensus. The fastest way to kill engineering momentum is inviting everyone into the decision room."*

### Angle 3: Tension / Paradoxical Question (The Curiosity Gap)
- **Formula**: `[Two irreconcilable facts] + [the urgent question they create]`.
- **Mechanism**: Highlights an obvious contradiction that the reader experiences daily but has never heard articulated clearly.
- **Example**:
  > *"Every startup preaches agile velocity, yet the average developer spends 60% of their week waiting on CI pipelines and PR approvals. If speed is our highest virtue, why do we build systems optimized for waiting?"*

**Author Collaboration Rule**: Present these three options to the author. Ask: *"Which hook best captures your natural voice, or would you like to fuse elements of two?"* Never pick silently.

---

## 4. The 4 Structural Shapes

Raw notes are not shaped into articles by organizing headings sequentially; they are shaped by matching the material to an archetypal narrative curve:

```
1. The Mountain (Narrative Arc)
       /\ Climax / Core Revelation
      /  \
     /    \
____/      \____ Resolution / Next Steps

2. The Inverted Pyramid (Insight-First)
\=======================/ Core Claim / The News
 \                     / Context & Mechanics
  \                   / Edge Cases & Nuance
   \                 /
    \_______________/ Call to Action

3. Tension and Resolution (Problem-Agitation-Solution)
[Status Quo] ---> [The Hidden Fracture] ---> [Crisis / Agitation] ---> [The Breakthrough]

4. Idea Escalation (Micro to Macro)
[Small Everyday Detail] ---> [Underlying Pattern] ---> [Universal Principle]
```

- **The Mountain**: Ideal for war stories, personal journeys, and case studies. Builds tension progressively toward a single breakthrough moment.
- **The Inverted Pyramid**: Ideal for tactical developer guides, architectural decisions, and announcements. Front-loads the conclusion, then deepens understanding.
- **Tension and Resolution**: Ideal for persuasive essays and reframing industry trends. Shows why current solutions are breaking before revealing the alternative.
- **Idea Escalation**: Ideal for philosophical or conceptual essays. Starts with an ultra-specific, familiar observation and scales it into a broad law of work or craft.

---

## 5. Concept Grounding Graph

To guarantee that the reader never gets lost, treat concepts as nodes in a directed acyclic graph:

1. **Audience Baseline ($P$)**: Concepts the target reader already understands prior to reading (e.g., for senior backend engineers: HTTP, SQL queries, thread pools).
2. **Current Grounded Set ($G_t$)**: $G_0 = P$. As each beat is accepted, any concept it successfully introduces and explains is unioned into the grounded set:
   $$G_{t+1} = G_t \cup \text{grounds}(\text{beat}_t)$$
3. **Reachability Condition**: A beat $\text{beat}_k$ can be introduced if and only if:
   $$\text{requires}(\text{beat}_k) \subseteq G_t$$
4. **Cognitive Trap Prevention**: If a desired claim requires concept $X$, and $X \notin G_t$, do not attempt to write the claim. Either:
   - Introduce an explicit explanatory beat to ground $X$.
   - Re-evaluate audience prerequisites (if $X$ is actually common knowledge for this reader).
   - Cut $X$ and rephrase the claim using currently grounded terminology.

---

## 6. Collaborative Drafting Cadence

The shaping process is a partnership with the author, conducted in clear iterative loops:

1. **Intake & Filter**: Read raw notes. Identify gold (sharp phrasing, lived observations, unique stances) and separate it from gravel (redundancies, half-baked tangents). Keep raw files strictly read-only.
2. **Angle Selection**: Present the 3 radical hook choices. Wait for author selection or direction.
3. **Beat Mapping**: Present 3-5 sequenced beats forming the spine of the chosen shape. Show reachable beats and the concepts they unlock.
4. **Drafting Moves**:
   - Offer the author a choice of path:
     - **Beat Path**: Draft beat-by-beat, checking each transition and grounding milestone.
     - **Block Path**: Draft full thematic sections, maintaining internal beat rhythm.
5. **Handling Lived Evidence Gaps**:
   - If an argument requires a real-world failure, metric, or personal quote:
   - **Do**: Mark it explicitly: `[GAP: Need a real example of what broke when cache invalidated]`.
   - **Do NOT**: Make up a story about a fictional company or fabricate numbers.

---

## 7. Anti-Slop & Prose Vitality Discipline

Elevating output above typical AI writing requires ruthless enforcement of vitality standards:

### Banned Patterns (The AI Slop Index)
- **Throat-Clearing Openings**:
  - *Slop*: "In today's fast-paced digital world...", "It goes without saying that..."
  - *Fix*: Start on the action or the claim immediately.
- **Empty Intensifiers and Buzzwords**:
  - *Slop*: "Leveraging cutting-edge paradigms to seamlessly orchestrate synergies."
  - *Fix*: "Using Redis queues to stop requests from dropping."
- **Passive Drone Cadence**:
  - *Slop*: "It has been demonstrated by numerous practitioners that performance can be improved..."
  - *Fix*: "Teams that cache early cut latency in half."
- **Predictable Symmetric Triads**:
  - *Slop*: "It requires diligence, dedication, and determination."
  - *Fix*: Use the exact right word; stop grouping adjectives in threes.
- **The Sychophantic Summary Wrap-up**:
  - *Slop*: "In conclusion, by embracing these transformative strategies, we can unlock..."
  - *Fix*: End on a punchline, an open challenge, or a sharp memorable sentence.

### Vitality Levers
- **Noun-Verb Precision**: Prioritize strong physical verbs over weak verbs burdened with adverbs (*"shattered"* instead of *"broke very quickly"*).
- **Sentence Cadence Variation**: Alternating short staccato sentences (3-6 words) with flowing, textured observations (20-30 words) creates natural reading cadence.
- **Preserve the Author's Idiom**: When the author uses a colloquialism, a dry technical quip, or an unusual metaphor in their raw notes, protect and foreground it.

---

## 8. Summary Checklist for High-Quality Output

Before declaring an article shaped:
- [ ] Raw source files remain untouched.
- [ ] Opening hook hooks the reader within 3 seconds using concrete prose.
- [ ] Every technical or domain concept is grounded before being relied upon.
- [ ] Each section contains distinct rhetorical beats (scene, claim, question, aside, pivot, payoff).
- [ ] Zero fabricated lived experiences, metrics, or quotes.
- [ ] Slop-free: no throat-clearing, no passive filler, varied sentence rhythms.
- [ ] The ending pays off the promise made in the opening.
