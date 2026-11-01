---
name: andino-article-shaping
description: An explicit writing request with existing raw material ready to be shaped into a cohesive article or essay. Operates under Andino Workflow governance.
---

# Shape raw material into an article

Internal method ID: `andino-article-shaping` (alias: `article-shaping`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Transform an unstructured collection of notes, observations, or raw fragments into a compelling, high-retention article where every concept is grounded before subsequent claims depend on it, and every beat delivers a distinct rhetorical move.

Activate for:
- An explicit writing request with existing raw notes, interview transcripts, or fragments ready to be shaped.
- Structuring an article's narrative arc, sequencing dramatic/rhetorical beats, or generating distinct opening hooks.
- Refining a draft's concept dependencies, pacing, and eliminating conversational slop.

Do not activate for:
- Open-ended fragment exploration without an intention to structure (use `andino-writing-fragments`).
- Overwriting or editing raw source material in place without explicit permission.
- Fabricating personal anecdotes or hallucinating evidence not found in the raw pile.
- Automatic copy-publishing without collaborative user review.

## Inputs and dependencies

- Raw material source: notes, fragments, outline fragments, or interview transcripts.
- Separate destination path for the shaped article (never overwrite raw inputs).
- Target audience definition and baseline concept prerequisites.
- Author's desired thesis, tone, and format constraints.

Use resources progressively: [worked procedure and example](resources/worked-example.md) and [detailed craft guide](GUIDE.md). Resources are local and self-contained; upstream repositories are provenance, not runtime dependencies.

## Procedure

1. **Ingest Raw Material Read-Only**
   - Read the raw pile end to end without modifying it.
   - Confirm or establish a separate destination file for the article.
   - Extract the core tension, central thesis, and memorable original phrases.

2. **Map Concept Prerequisites and Grounding**
   - Identify what the target audience already understands (prerequisites).
   - Initialize the `grounded_concepts` set with audience prerequisites.
   - Enforce the Grounding Invariant: A claim or beat cannot introduce cognitive friction by relying on a concept before that concept has been introduced and grounded.

3. **Generate Three Radically Distinct Opening Hooks**
   - Offer the author 2 to 3 genuinely different openings, providing 1-2 sentences of *actual sample prose* for each, not merely descriptive bullet points:
     - *Angle A: Narrative / In Media Res* (drops the reader into a specific incident, visual scene, or sensory moment).
     - *Angle B: Provocative / Counter-Intuitive Claim* (directly confronts common wisdom or states a bold, defensible truth).
     - *Angle C: Tension / Problem-Driven Question* (surfaces an unresolved dilemma, paradox, or urgent reader stakes).
   - Let the author choose, combine, or calibrate voice. Never substitute the agent's preferred opening silently.

4. **Choose the Drafting Path: Beat-by-Beat vs. Paragraph Flow**
   - *Beat Path*: Best for complex conceptual journeys, essays, and technical narratives. Structure the piece as discrete rhetorical moves with explicit concept tracking and reachability.
   - *Paragraph Flow*: Best for straightforward opinion pieces or linear narrative arcs. Draft in cohesive blocks while respecting beat transitions.

5. **Execute Beats as Discrete Rhetorical Moves**
   - Each beat must perform exactly **one job**:
     - `scene`: Grounds the reader in a concrete setting, event, or sensory snapshot.
     - `claim`: Advances a core argument, insight, or proposition.
     - `question`: Opens a curiosity gap or challenges an assumption.
     - `aside`: Shares a personal reflection, nuance, or boundary caveat.
     - `pivot`: Shifts direction, reframes the premise, or introduces a surprising turn.
     - `payoff`: Resolves tension, cements the lesson, or lands the central insight.
   - Verify state change: Each beat must alter the reader's understanding, emotional tension, or concept state (delta != 0).

6. **Ground Missing Links & Name Gaps Faithfully**
   - Mine, split, and re-order raw material freely to serve narrative clarity.
   - When a transition or beat requires an example or lived detail not present in the raw notes, **name the gap** explicitly and request it from the author: *"We need a concrete example of when this failed in production."*
   - Never invent personal stories, synthetic numbers, or fake quotes.

7. **Apply Anti-Slop and Cadence Polish**
   - Cut throat-clearing openings (*"In the ever-evolving landscape of...", "It is important to understand that..."*).
   - Replace abstract nouns with specific, visceral verbs and objects.
   - Vary sentence lengths deliberately: interlock short punchy declarations with rhythmic multi-clause explanations.
   - Review draft collaboratively, append agreed blocks, update the grounded concept set, and stop when the journey is complete.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical checks.
Coordinator brevity/density never truncates these. User/project authority, Focus/research/domain
boundaries and real invocation controls still apply. Native `andino-article-shaping` and this guide
expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations,
external messages/tracker writes, credentials, global setup, deployments and recurring jobs require
their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

- The raw material source file remains byte-for-byte unchanged.
- The shaped article clearly fulfills the chosen opening hook and thesis.
- Concept dependencies are logically ordered with zero ungrounded prerequisites.
- Every beat executes a defined rhetorical job with varied rhythm and zero AI slop.
- Output respects the author's authentic voice and decisions.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic
result proves only that bounded procedure; it does not prove model routing, live host parity or
optional external tool execution. Record actual command/tool, current content identity, result and
unresolved limits before claiming success.

## Example and anti-patterns

Positive request:
- *"Here is my raw brain-dump on database migrations; shape it into a tight essay with grounded concepts and 3 distinct opening hook options."*
- *"Take these rough interview notes and sequence them into dramatic beats that build to our architectural breakthrough."*

Negative request:
- *"Rewrite my raw fragment notes file directly and publish it without asking."*

Anti-patterns:
- Introducing specialized jargon (e.g., "idempotency keys", "vector embeddings") without grounding the concept first.
- Forcing every single raw fragment into the article even when it dilutes focus or disrupts narrative flow.
- Homogeneous AI boilerplate: uniform sentence length, passive voice, predictable "In conclusion" summaries, or sycophantic padding.
- Inventing anecdotes or attributing experiences to the author that were never stated in the source notes.

## Fallback

When live interactive feedback is unavailable, generate a grounded beat outline alongside 3 proposed hook variations clearly labeled as `[PROPOSED - PENDING AUTHOR SELECTION]`, and draft the first two grounded beats as a working proof-of-concept.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/in-progress/writing-beats/SKILL.md`
- `mattpocock/skills:skills/in-progress/writing-shape/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
