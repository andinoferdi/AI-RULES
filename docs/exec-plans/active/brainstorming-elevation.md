# Elevate Brainstorming & Consolidate Decision-Interview into Unified Discovery & Grilling Powerhouse

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 6 — Verification, Host Sync & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Elevate `skills/brainstorming/` and consolidate `skills/decision-interview/` on branch `andino-workflow` into a unified discovery, grilling, and decision refinery engine. The elevated skill synthesizes the premier craft of Addy Osmani's `interview-me` (1-question dialogue, confidence hypothesis `<70%`, buzzword stripping, 3-question predictability exit condition), Matt Pocock's `grilling`, `grill-me`, and `grill-with-docs` (relentless grilling to mutual consensus, DAG-based decision tree frontiers, recommended defaults for rapid steering, in-flight ADR and domain glossary generation), and Jesse Vincent's Obra Superpowers `brainstorming` (strict 3-path classification: Spike, Bounded, Architectural, hard gates before coding, 2-3 approaches with trade-offs) under Andino Workflow governance.

The consolidation satisfies the user's strict instruction to merge `decision-interview` into `brainstorming` while maintaining 100% backward compatibility for the 59-skill catalog via a forwarding shim in `skills/decision-interview/`, updating references in index and registry, creating offline deterministic Python stdlib verification, synchronizing to the local host directory, passing `ai-rules setup`, and completing git commit and push.

## Objective

Deliver an upgraded, self-contained `skills/brainstorming` bundle that merges and elevates `decision-interview`, matching and exceeding upstream benchmarks in conversational rigor, architectural clarity, and developer momentum, verified through deterministic test fixtures and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/brainstorming/SKILL.md` overhauled as a high-density operational contract (<150 lines hard ceiling, measured at 96 lines):
  - Actionable triggers and dominant negative gates (skips routine edits, settled specs).
  - 4-Phase Core Procedure:
    1. Intent Hypothesis & Buzzword Stripping (confidence score `<70%`).
    2. Friction-Proportional Three-Path Classification (Spike, Bounded, Architectural).
    3. Frontier-Based Relentless Grilling with Proposed Defaults (DAG unblocked frontier, max 3 questions before fatigue breaker).
    4. In-Flight ADR & Domain Glossary Capture with 3-Question Predictability Termination.
  - Hard pre-implementation gates (zero code or scaffolding before explicit design consensus).
  - Anti-Rationalization Refutation Table & 6 Diagnostic Red Flags.
  - Progressive disclosure routing to `resources/`.
  - Runnable standard-library operational example (`andino-operational-example`) with default passing and adversarial `ANDINO_NEGATIVE=1` variant.
- [x] `skills/brainstorming/GUIDE.md` overhauled with deep craft chapters:
  - Divergent Exploration vs. Convergent Grilling lifecycles.
  - The Decision DAG & Unblocked Frontier Mechanics.
  - De-buzzwording Taxonomy: Translating "Scalable", "Intuitive", "Robust" into falsifiable observable criteria.
  - Proposing Default Recommendations: Cognitive momentum vs. inquisitor fatigue.
  - In-Flight ADR & Glossary Generation Protocols (Lazy emission after consensus).
  - 3-Path Operational Deep-Dive (Spike throwaway probes, Bounded chat designs, Architectural specs).
- [x] `skills/brainstorming/resources/grilling-protocol.md` created:
  - Frontier DAG traversal rules.
  - The 1-Question Turn Contract: Context + Question + Reasoned Default.
  - Exit conditions: Frontier exhaustion or 3-Question Predictability.
  - User fatigue circuit breakers.
- [x] `skills/brainstorming/resources/adr-and-glossary-template.md` created:
  - Canonical ADR schema: Context, Decision, Consequences, Status, Alternatives.
  - Domain Glossary template: Ubiquitous Language mappings, anti-terms, definitions.
- [x] `skills/brainstorming/resources/worked-example.md` created with end-to-end scenario:
  - Ambiguous intake -> buzzword stripping -> 3-path classification -> frontier grilling with defaults -> ADR capture -> builder-ready specification.
- [x] `skills/decision-interview/SKILL.md` and `GUIDE.md` updated as clean backward-compatibility shims:
  - Retains internal method ID `andino-decision-interview`.
  - Forwards canonically to `andino-brainstorming`.
  - Zero disruption to existing workflows or 59-skill catalog.
- [x] Reference indexes and registries updated:
  - `references/internal-method-index.md`: updates `decision-interview` and `brainstorming` entries, maps source aliases (`grill-me`, `grilling`, `grill-with-docs`, `interview-me`) to `brainstorming`.
  - `references/capability-registry.md`: updates alias and canonical method references.
  - `references/routing.md`: reflects the consolidated discovery and grilling route.
  - `references/legal/provenance.md`: logs the 2026-11-01 elevation of `brainstorming` and merge of `decision-interview` with full MIT provenance.
  - `README.md`: reflects the enhanced unified capability.
- [x] Deterministic Python 3.8+ stdlib verification script (`scripts/verify_brainstorming_elevation.py`):
  - Validates line count `<150` lines in `SKILL.md`.
  - Verifies presence of frontmatter, triggers, gates, 4 phases, red flags, and runnable operational example.
  - Executes operational example in normal mode (`exit 0`) and adversarial mode (`exit 1`).
  - Verifies 59/59 skill directory presence and alias forward resolution.
- [x] Synchronized to local host directory `~/.claude/skills/andino-workflow/`.
- [x] Verified compatible with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
- [x] Clean git commit and push to `origin/andino-workflow`.

## Scope

### In Scope
- `skills/brainstorming/SKILL.md`
- `skills/brainstorming/GUIDE.md`
- `skills/brainstorming/resources/grilling-protocol.md`
- `skills/brainstorming/resources/adr-and-glossary-template.md`
- `skills/brainstorming/resources/worked-example.md`
- `skills/decision-interview/SKILL.md`
- `skills/decision-interview/GUIDE.md`
- `references/internal-method-index.md`
- `references/capability-registry.md`
- `references/routing.md`
- `references/legal/provenance.md`
- `README.md`
- `scripts/verify_brainstorming_elevation.py`
- Host synchronization to `~/.claude/skills/andino-workflow/`
- Verification with `ai-rules setup`

### Out of Scope
- Altering unrelated Andino skills.
- Introducing third-party npm or pip dependencies.
- Modifying repository code outside skills, references, tests, and documentation.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Unified Discovery Engine**: Consolidating open exploration, relentless grilling, and intent extraction creates a high-leverage decision refinery that prevents building the wrong thing.
- **Cognitive Momentum via Defaults**: Always pair questions with a high-conviction recommended default ("I recommend Option A because [reason]. Press Enter to confirm or steer"). This shifts user effort from generation to rapid evaluation.
- **Friction-Proportional Gating**: Casual/bounded changes bypass heavy grilling; deep grilling, ADRs, and glossary generation are strictly quarantined to high-consequence architectural tasks.
- **Deterministic Exit**: Discovery terminates on frontier exhaustion or 3-question predictability, preventing infinite exploratory drift.
- **Zero-Breakage Shimming**: Keep `skills/decision-interview` as a forwarding adapter so the 59-member catalog remains intact.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **Divergence vs. Convergence Clash**:
   - *Risk*: Brainstorming expands options; grilling ruthlessly narrows them. Merging them risks mode confusion and interrogation fatigue.
   - *Resolution*: Structural 4-step sequence: Step 1 Intent Extraction (unvarnished goals), Step 2 Three-Path Scoping (Spike/Bounded/Architectural), Step 3 Frontier Grilling (only for Architectural, capped at 3 questions max before presenting defaults), Step 4 Specification & Lazy ADR emission.
2. **Premature Formalization (The ADR Trap)**:
   - *Risk*: Emitting verbose ADRs and glossary files mid-conversation stalls momentum and anchors tentative ideas.
   - *Resolution*: Maintain ADRs and glossary as latent mental models during the dialogue; emit formal Markdown artifacts only upon mutual design consensus.
3. **150-Line Density vs. 4 Upstream Traditions**:
   - *Risk*: Squeezing Addy, Pocock, Obra, ADRs, and Python tests into <150 lines causes prompt dilution.
   - *Resolution*: Keep `SKILL.md` strictly focused on the operational contract and state machine; route comprehensive mechanics, schemas, and worked examples to `resources/`.

### Hal Terlewat (Blind Spots Addressed)
- **Fatigue Breaker**: If user replies become terse (<10 words) or impatient, immediately halt sequential questioning and present all remaining frontier items with recommended defaults for bulk approval.
- **Strict Fact vs. Decision Separation**: Inspect repo files, configs, and git history directly; never interrogate the user on discoverable code facts.

---

## Execution Plan & Phased Tasks

### Phase 1: Progressive Disclosure Resources & Protocols
- [x] Task 1.1: Author `skills/brainstorming/resources/grilling-protocol.md` with DAG frontier mechanics, 1-question turn contracts, and exit criteria.
- [x] Task 1.2: Author `skills/brainstorming/resources/adr-and-glossary-template.md` with schemas for in-flight ADRs and ubiquitous domain glossaries.
- [x] Task 1.3: Author `skills/brainstorming/resources/worked-example.md` with full end-to-end walkthrough from vague ask to builder-ready design.

### Phase 2: Core Operational Contract & Craft Guide
- [x] Task 2.1: Author `skills/brainstorming/GUIDE.md` with deep craft chapters, de-buzzwording taxonomy, 3-path lifecycle, and anti-patterns.
- [x] Task 2.2: Author `skills/brainstorming/SKILL.md` as a high-density (<150 lines, 96 lines actual) operational contract with runnable Python stdlib operational example.

### Phase 3: Backward Compatibility Forwarding Shim
- [x] Task 3.1: Author `skills/decision-interview/SKILL.md` as a clean forwarding contract to `andino-brainstorming`.
- [x] Task 3.2: Author `skills/decision-interview/GUIDE.md` explaining the consolidation and delegation protocol.

### Phase 4: References, Index & Legal Updates
- [x] Task 4.1: Update `references/internal-method-index.md` and `references/routing.md`.
- [x] Task 4.2: Update `references/capability-registry.md` and `README.md`.
- [x] Task 4.3: Update `references/legal/provenance.md` with full synthesis audit trail and MIT attributions.

### Phase 5: Deterministic Verification Test
- [x] Task 5.1: Create `scripts/verify_brainstorming_elevation.py` validating line count, structural sections, inline operational example (normal & adversarial), and catalog integrity.
- [x] Task 5.2: Execute test offline with pure Python stdlib (ALL 18 CHECKS PASSED).

### Phase 6: Host Synchronization, CLI Setup Verification & Git Delivery
- [x] Task 6.1: Synchronize updated skill files to `~/.claude/skills/andino-workflow/skills/brainstorming/` and `~/.claude/skills/andino-workflow/skills/decision-interview/`.
- [x] Task 6.2: Test compatibility with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
- [x] Task 6.3: Git commit with descriptive message and push to `origin/andino-workflow`.

---

## Next Action
None — task complete. All acceptance criteria satisfied, verified offline, synchronized to host, committed, and pushed.
