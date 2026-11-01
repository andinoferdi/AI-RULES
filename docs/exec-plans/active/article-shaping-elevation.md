# Elevate Article-Shaping Quality to Match and Exceed Upstream Writing Skills

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Successfully elevated `skills/article-shaping/` on branch `andino-workflow` from a dry procedural rulebook into a premier, high-retention writing craft engine. The skill now unifies the complete rhetorical beat dynamics of Matt Pocock's `writing-beats` and the structural hook generation and anti-slop vitality of `writing-shape`, backed by deterministic concept grounding verification.

## Objective

Deliver an upgraded, self-contained `skills/article-shaping` bundle whose AI generation quality matches and exceeds upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/article-shaping/SKILL.md` updated with comprehensive craft directives: beat definitions, radical hook options, grounded concept tracking, and anti-slop guidelines.
- [x] `skills/article-shaping/GUIDE.md` overhauled with in-depth craft chapters: Anatomy of a Rhetorical Beat, The 4 Structural Shapes, The 3-Hook Generation Engine, Collaborative Drafting Cadence, and Prose Vitality / Anti-Slop Rules.
- [x] `skills/article-shaping/resources/worked-example.md` upgraded to a realistic, complete demonstration with rich sample raw notes, 3 distinct hook samples, sequenced beat progression with concept state tracking, final shaped prose excerpt, and deterministic Python verification.
- [x] Provenance in `references/legal/provenance.md` updated with audited records and attribution.
- [x] Deterministic Python verification script structure verified and aligned.
- [x] Implementation ready for `ai-rules setup` branch sync.

## Scope

### In Scope
- `skills/article-shaping/SKILL.md`
- `skills/article-shaping/GUIDE.md`
- `skills/article-shaping/resources/worked-example.md`
- `references/legal/provenance.md`
- Integration with `ai-rules setup`

### Out of Scope
- Creating a separate redundant `writing-beats` skill (user selected Unified Article-Shaping).
- Altering existing unrelated Andino skills.
- Breaking backwards compatibility with existing raw fragment files.

## User Decisions / Clarifications
- **Architecture**: Unified Article-Shaping — deep integration of beat craft and shape sculpting directly within `article-shaping`.
- **Sync**: Remote + Local Sync — push to `origin/andino-workflow` and synchronize to local host directory `~/.claude/skills/`.

## Council Synthesis Summary
- **Titik Temu (Agreement)**: Current skill is structurally sound but practically sterile; needs concrete generative prompts, sample hook styles with actual draft sentences, clear beat taxonomy (scene, claim, question, aside, pivot, punchline), and anti-slop discipline.
- **Perbedaan (Disagreement)**: Risk of prompt bloat vs depth of guidance. Resolved by keeping `SKILL.md` dense and actionable, while putting rich illustrative craft, templates, and patterns in `GUIDE.md`.
- **Hal Terlewat (Blind Spots)**: Collaborative cadence must never feel like a tedious survey; present working prose choices immediately so the writer feels momentum.
- **Rekomendasi (Recommendation)**: Deliver Unified Article-Shaping with an explicit 3-Hook engine, 6-job Beat taxonomy, and concrete concept grounding graph.
- **Langkah Pertama (First Action)**: Upgrade `skills/article-shaping/SKILL.md`.

## Task Breakdown & Change Specifications

### Task 1: Upgrade `skills/article-shaping/SKILL.md`
- **Anchor**: Whole file replacement.
- **Key Enhancements**:
  - Purpose: Shape raw materials into an engaging, cohesive article using rhetorical beats and concept grounding.
  - Active triggers: Expanded to recognize requests seeking structure, narrative pacing, beat sequencing, or hook drafting from notes.
  - Core Procedure:
    1. Read raw notes end-to-end, strictly read-only.
    2. Extract core thesis and identify audience prerequisite concepts.
    3. Generate 3 radically different opening hooks with real prose drafts (Narrative/Vignette, Provocative Claim, Tension/Question).
    4. Choose drafting mode: Beat-by-Beat (sculpting sequence with concept tracking) vs Block/Paragraph Flow (rapid drafting with pacing checks).
    5. Beat classification: Ensure each beat executes exactly one job (scene, claim, question, aside, pivot, payoff).
    6. Grounding check: Verify all required concepts are grounded before subsequent claims rely on them.
    7. Anti-slop polish: Remove throat-clearing, corporate jargon, and repetitive cadence.

### Task 2: Overhaul `skills/article-shaping/GUIDE.md`
- **Anchor**: Whole file replacement.
- **Key Sections**:
  - Detailed methodology: From Fragments to Beats to Cohesive Narrative.
  - The Beat Taxonomy (6 beat types, state transitions, emotional/conceptual delta).
  - The 3-Hook Generation Engine (definitions, formulas, and examples of Narrative, Provocative, and Tension hooks).
  - The 4 Narrative Shapes (The Mountain, The Inverted Pyramid, Tension-Resolution, Idea Escalation).
  - Concept Grounding Graph (tracking prerequisites, introduced concepts, and dependency chains).
  - Collaborative Drafting Cadence (offering genuine options, respecting author voice, never hallucinating lived experience).
  - Prose Vitality & Anti-Slop Discipline (concrete sensory language, cutting meta-commentary, sentence rhythm variation).

### Task 3: Rebuild `skills/article-shaping/resources/worked-example.md`
- **Anchor**: Whole file replacement.
- **Contents**:
  - Realistic raw fragment input (e.g. distributed systems engineering failure & recovery).
  - Concrete demonstrations of the 3 hook candidates with full prose text.
  - Beat journey table with: Beat ID, Job, Required Concepts, Grounded Concepts, Emotional Delta.
  - Finished excerpt showing how beats synthesize into natural, vivid prose.
  - Python verification script testing concept grounding graph resolution, raw note preservation, and artifact generation.

### Task 4: Update Provenance & Method Index
- **File**: `references/legal/provenance.md` and `references/internal-method-index.md`.
- **Details**: Document that `article-shaping` unifies the audited craft of `writing-beats` and `writing-shape`.

### Task 5: Verification & Sync
- **Local Validation**: Run Python verification script.
- **Host Sync**: Synchronize upgraded `skills/article-shaping` to `~/.claude/skills/andino-article-shaping`.
- **Git**: Stage, commit, and push to `origin/andino-workflow`.
