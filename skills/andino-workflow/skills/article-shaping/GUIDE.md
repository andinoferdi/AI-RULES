# Shape Raw Material into an Article: Authoritative Master Craft Guide

Internal method ID: `andino-article-shaping` (aliases: `article-shaping`, `writing-beats`, `writing-shape`).

This guide details the end-to-end authoring and editorial discipline for transforming raw thoughts, unstructured notes, fragmented observations, and transcripts into a compelling, high-retention essay or article. It combines the rigorous epistemic architecture of **Writing Beats** with the sculpting mastery, hook craftsmanship, and ruthless editorial grilling of **Writing Shape**.

---

## 1. The Core Philosophy: Grounding and Narrative Momentum

Weak AI-generated writing suffers from two fatal flaws:
1. **Cognitive Disconnection (The Ungrounded Leap):** Concepts appear out of nowhere. The reader is assaulted with ungrounded jargon or abstract principles before understanding why they matter or how they connect to reality.
2. **Static Homogeneity (Regression to the Mean):** Long batch drafts default to predictable, uniform sentences. Every paragraph has the same weight, the same tone, and the same length. The writing describes rather than *moves*.

High-craft article shaping resolves both flaws through two non-negotiable disciplines:
- **Concept Grounding:** A strict dependency graph where every new claim builds exclusively on audience prerequisites or previously established concepts.
- **Rhetorical Beats & Grilling:** Pacing the piece as an intentional sequence of dramatic moves where every unit performs exactly one job, and a ruthless editor actively interrogates weak transitions before committing text to disk.

---

## 2. Anatomy of a Rhetorical Beat

A **beat** is the atomic unit of rhetorical momentum. It can span a single punchy sentence or several interconnected paragraphs, but it must perform **exactly one primary job**.

### The 6 Beat Types

| Beat Type | Primary Job | Emotional / Conceptual Delta | When to Use |
| :--- | :--- | :--- | :--- |
| `scene` | Visceral grounding in physical reality or concrete moment | Observer -> Witness | In openings, before abstract theory, or after heavy exposition to re-anchor reality. |
| `claim` | Stating an authoritative argument, rule, or core proposition | Curious -> Informed | When establishing the central thesis or key milestone in the argument. |
| `question` | Opening a curiosity gap or destabilizing existing belief | Settled -> Questioning | To pull the reader into the next section or challenge accepted dogma. |
| `aside` | Sharing a candid nuance, authorial doubt, or practical boundary | Formal -> Intimate | To build trust, address counter-arguments, or prevent misapplication. |
| `pivot` | Executing a sharp directional or conceptual turn | Expectant -> Surprised | When revealing the non-obvious solution, twist, or hidden failure mode. |
| `payoff` | Delivering the promised resolution, insight, or lasting punchline | Tense -> Satisfied | Climax of a section or concluding note of the entire piece. |

### The Beat State Contract
For every beat drafted, verify:
1. **Preconditions:** What concepts must the reader already know? If an ungrounded concept is required, pause and insert an introductory beat first.
2. **Grounds:** What new concept, principle, or mental model does this beat permanently establish?
3. **Pacing Delta:** How did the reader's state change? (e.g., from skepticism to realization, or from confusion to clarity).

---

## 3. The 3-Hook Generation Engine

Never begin drafting body paragraphs until the opening hook is deliberately chosen. The opening hook dictates voice, stakes, and narrative velocity.

When presented with raw material, formulate **three genuinely different hooks**, providing **1-2 sentences of full, finished prose** for each:

### Angle 1: Narrative / In Media Res (The Vignette)
- **Mechanism:** Drops the reader directly into a moment of sensory crisis, specific dialogue, or a high-stakes turning point without preamble.
- **Formula:** `[Specific physical setting/timestamp] + [immediate tactile conflict or failure]`.
- **Example:**
  > *"At 3:14 AM on a freezing Tuesday in November, our primary Postgres cluster stopped accepting writes. The issue wasn't disk space or network partitioning—it was a single five-character line in a background worker."*

### Angle 2: Provocative / Counter-Intuitive Claim (The Gauntlet)
- **Formula:** `[Direct refutation of accepted dogma] + [uncomfortable reality]`.
- **Mechanism:** Forces the reader to stop scrolling by declaring that the standard way they do things is fundamentally backwards.
- **Example:**
  > *"Most software teams don't have a communication problem; they have an excess of consensus. The fastest way to kill engineering momentum is inviting everyone into the decision room."*

### Angle 3: Tension / Paradoxical Question (The Curiosity Gap)
- **Formula:** `[Two irreconcilable facts] + [the urgent question they create]`.
- **Mechanism:** Highlights an obvious contradiction that the reader experiences daily but has never heard articulated clearly.
- **Example:**
  > *"Every startup preaches agile velocity, yet the average developer spends 60% of their week waiting on CI pipelines and PR approvals. If speed is our highest virtue, why do we build systems optimized for waiting?"*

**Author Collaboration Rule:** Present these three options to the author. Ask: *"Which hook best captures your natural voice, or would you like to fuse elements of two?"* Never pick silently.

---

## 4. The 4 Structural Shapes

Raw notes are not shaped into articles by organizing headings sequentially; they are shaped by matching the material to an archetypal narrative curve:

1. **The Mountain (Narrative Arc):**
   - `Status Quo -> Rising Conflict -> Climax / Core Revelation -> Resolution`
   - Ideal for war stories, personal journeys, and case studies. Builds tension progressively toward a single breakthrough moment.
2. **The Inverted Pyramid (Insight-First):**
   - `Core Claim / The News -> Context & Mechanics -> Edge Cases & Nuance -> Call to Action`
   - Ideal for tactical developer guides, architectural decisions, and announcements. Front-loads the conclusion, then deepens understanding.
3. **Tension and Resolution (Problem-Agitation-Solution):**
   - `Status Quo -> The Hidden Fracture -> Crisis / Agitation -> The Breakthrough`
   - Ideal for persuasive essays and reframing industry trends. Shows why current solutions are breaking before revealing the alternative.
4. **Idea Escalation (Micro to Macro):**
   - `Small Everyday Detail -> Underlying Pattern -> Universal Principle`
   - Ideal for philosophical or conceptual essays. Starts with an ultra-specific, familiar observation and scales it into a broad law of work or craft.

---

## 5. Concept Grounding Graph & Reachability Mathematics

To guarantee that the reader never gets lost, treat concepts as nodes in a directed acyclic graph:

1. **Audience Baseline ($P$):** Concepts the target reader already understands prior to reading (e.g., for senior backend engineers: HTTP, SQL queries, thread pools).
2. **Current Grounded Set ($G_t$):** $G_0 = P$. As each beat is accepted, any concept it successfully introduces and explains is unioned into the grounded set:
   $$G_{t+1} = G_t \cup \text{grounds}(\text{beat}_t)$$
3. **Reachability Condition:** A beat $\text{beat}_k$ can be introduced if and only if:
   $$\text{requires}(\text{beat}_k) \subseteq G_t$$
4. **Cognitive Trap Prevention:** If a desired claim requires concept $X$, and $X \notin G_t$, do not attempt to write the claim. Either:
   - Introduce an explicit explanatory beat to ground $X$.
   - Re-evaluate audience prerequisites (if $X$ is actually common knowledge for this reader).
   - Cut $X$ and rephrase the claim using currently grounded terminology.

---

## 6. The Ruthless Editor Stance & Grilling Moves

High-craft article shaping requires an active editorial partner who pushes back against lazy thinking. Deploy these five core grilling moves during drafting:

1. **"What does this paragraph do for the reader that the previous one didn't?"**
   If a paragraph merely repeats an earlier point in different words, cut it.
2. **"If we cut this, what actually breaks?"**
   If removing a section leaves the argument completely intact, that section was vanity flab.
3. **"This sentence is doing two jobs: split it or pick one."**
   Compound sentences that introduce a new premise while trying to deliver a punchline fail at both.
4. **"The opening promised X. We have drifted to Y. Do we re-thread back or change the opening?"**
   Catch premise drift before drafting downstream arguments.
5. **"We need a concrete example here and the raw notes don't have one. Give me one now or we cut this section."**
   The *name the gap* move. Never invent an example on the author's behalf.

---

## 7. Format Arguments to Have Out Loud

Weigh visual and structural tradeoffs deliberately with the author:
- **Prose vs. List:** Prose carries narrative argument and causal momentum. Lists carry truly parallel items. If items are not parallel, prose is superior.
- **Inline vs. Callout:** Callouts (`> [!NOTE]`, `> [!WARNING]`) belong only on tips or boundary warnings that would derail the narrative flow inline.
- **Table vs. Repeated Structure:** If the same entity shape repeats 3+ times with matching attributes, render a table. Otherwise, use prose with bold lead-ins.
- **Quote vs. Paraphrase:** Quote when the author's original phrasing is the point. Paraphrase when only the underlying concept matters.
- **Code Block vs. Inline Code:** Multi-line or runnable logic belongs in a block. Single identifiers or tokens belong inline.

---

## 8. Cadence and Sentence-Length Engineering

Monotonous rhythm puts readers to sleep. Alternate sentence lengths deliberately:
- **Staccato Declarations (3-6 words):** Deliver conclusions and visceral impact (*"The race condition vanished."*).
- **Legato Explanations (15-25 words):** Weave mechanics, nuance, and causality (*"When cellular towers drop connections mid-flight, mobile client libraries re-dispatch identical HTTP payloads across independent server pods within milliseconds."*).
- **Active Verbs:** Prioritize concrete physical verbs over weak verbs propped up by adverbs (*"shattered"* instead of *"broke very quickly"*).
- **Nominalization Ban:** Never convert strong verbs into abstract Latinate nouns (*"optimize"* instead of *"perform an optimization of"*).

---

## 9. Protecting Authentic Voice & Focus Alignment

The ruthless editor attacks weak arguments and logical gaps, **never** the author's personal identity or voice:
- Preserve idiosyncratic metaphors, dry technical humor, and colloquialisms found in raw notes.
- Avoid forcing a cynical, arrogant tech-Twitter persona onto an author who writes with quiet, rigorous precision.
- Follow the communication principles of `focus`:
  - **In Indonesian:** Communicate naturally like a sharp colleague at a coffee shop (warkop)—active, direct, warm, and free of corporate jargon or robotic textbook phrasing.
  - **In English:** Cut throat-clearing preambles immediately; start on the action.

---

## 10. Summary Verification Checklist

Before declaring an article shaped:
- [ ] Raw source files remain untouched byte-for-byte.
- [ ] The article lives in a separate destination file (`article.md`).
- [ ] Opening hook hooks the reader within 3 seconds using concrete sample prose.
- [ ] Every domain concept is grounded before being relied upon.
- [ ] Every beat performs exactly one rhetorical job.
- [ ] Zero fabricated lived experiences, metrics, or synthetic quotes.
- [ ] Slop-free: no throat-clearing, no symmetric triads, varied sentence rhythms.
- [ ] The ending pays off the promise made in the opening hook.
- [ ] All agreed beats are committed directly to disk before proposing next moves.
