# Elevate Deep Module Design to Match and Exceed Upstream Benchmarks

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Successfully elevated `skills/deep-module-design/` on branch `andino-workflow` from an abstract, over-compressed 80-line guide with duplicate `GUIDE.md` and minimal 22-line worked example into a premier, machine-enforced deep module architecture engine. The elevated skill synthesizes the generative craft of Matt Pocock's `codebase-design` and `improve-codebase-architecture` (The 8 Absolute Glossary Terms, The Deletion Test, The 2-Adapter Seam Rule, 4 Dependency Categories in `DEEPENING.md`, parallel subagent `DESIGN-IT-TWICE.md` protocols, and terminal-native visual before/after cards) with Andino Workflow governance (high-density <150 line operational contract `SKILL.md`, deep craft `GUIDE.md`, multi-ecosystem pattern catalogs in TypeScript, Python, Go, and Rust, cognitive compression for AI-navigability, zero-dependency offline Python stdlib verification, and complete integration with `ai-rules setup`).

## Objective

Deliver an upgraded, self-contained `skills/deep-module-design` bundle whose AI output quality, architectural rigor, leverage-maximizing interfaces, and operational ergonomics match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/deep-module-design/resources/dependency-and-seam-discipline.md` created:
  - The 4 Dependency Categories: In-process (pure computation), Local-substitutable (in-memory SQLite, PGLite, memory FS), Remote-owned (Ports & Adapters), and True external (Mocks).
  - Seam Discipline: The 2-Adapter Invariant (1 adapter = hypothetical indirection, 2 adapters = verified real seam).
  - Internal seams vs. External seams (never expose implementation seams through public interface for test convenience).
  - Testing Strategy: "Replace, Don't Layer" (interface is test surface; old shallow tests deleted; tests survive internal refactors).
- [x] `skills/deep-module-design/resources/design-it-twice-protocols.md` created:
  - Step 1: Problem Space Framing with constraints, dependency mapping, and grounding code sketches.
  - Step 2: Parallel Subagent Spawning Protocol across 4 divergent design constraints (Minimalist 1-3 entrypoints, Maximum extension, Common-caller simplicity, Ports & Adapters).
  - Technical brief format and context isolation rules to prevent cross-contamination.
  - Step 3: Comparative synthesis rubric (Depth/Leverage, Locality, Seam Placement) and opinionated hybrid recommendation.
- [x] `skills/deep-module-design/resources/leverage-rubric-and-catalogs.md` created:
  - Quantified Leverage Scorecard: Formula, caller conceptual burden vs. capability gained, interface method/parameter count.
  - Multi-Ecosystem Deep Module Transformation Catalogs:
    - TypeScript / Modern JavaScript: Collapsing fragmented pipeline handlers into high-leverage facade/domain modules.
    - Python: Consolidating scattered ETL/data processing steps into cohesive domain-driven entrypoints.
    - Go: Eliminating thin interface wrappers and consolidating struct-backed services with clean exported APIs.
    - Rust: Encapsulating complex state machines and validation behind clean trait/struct boundaries.
  - Terminal-Native Visual Cards (Mermaid flowchart/sequence, ASCII mass diagrams, and cross-section collapse).
- [x] `skills/deep-module-design/resources/worked-example.md` overhauled with end-to-end refactoring:
  - Realistic multi-module domain scenario: Shallow e-commerce checkout & order processing leaking pricing, inventory, tax, and notifications across 6 callers.
  - Execution of Deletion Test and Dependency Classification.
  - Design-It-Twice candidate exploration and selection of winning hybrid.
  - Test migration walkthrough ("Replace, Don't Layer").
  - Embedded zero-dependency Python stdlib verification harness (`run_verification.py`).
- [x] `skills/deep-module-design/GUIDE.md` overhauled with deep craft chapters:
  - Chapter 1: The Philosophy of Deep Modules (Ousterhout's depth-as-leverage vs. Feathers' seams).
  - Chapter 2: The 8 Absolute Glossary Terms (Module, Interface, Implementation, Depth, Seam, Adapter, Leverage, Locality) and explicitly forbidden vague nouns (*unit, component, service, API, boundary*).
  - Chapter 3: Designing for High Caller Leverage and Testability (accept dependencies, return values, small surface).
  - Chapter 4: Seam Justification & The 2-Adapter Rule.
  - Chapter 5: Parallel Exploration Protocol (Design-It-Twice).
  - Chapter 6: The AI-Navigability Advantage: How Deep Modules prevent agent hallucinations and context saturation.
  - Chapter 7: The Refactoring & Test Replacement Lifecycle.
- [x] `skills/deep-module-design/SKILL.md` overhauled as a high-density operational contract (<150 lines):
  - Progressive disclosure router to `resources/`.
  - Dominant Negative Gates ("When NOT to design a deep module").
  - The Five Deep Design Invariants.
  - Anti-Rationalization Refutations Table (5 critical debunked developer/AI excuses).
  - Diagnostic Red Flags (Stop Immediately checklist).
  - Runnable standard-library operational example (`andino-operational-example`) with normal passing state and adversarial `ANDINO_NEGATIVE=1` variant.
  - Output format & verification checklist.
- [x] `references/legal/provenance.md` updated with comprehensive audit details and MIT attributions for Matt Pocock's `codebase-design` and `improve-codebase-architecture`.
- [x] Deterministic Python verification script executed and passing in temporary directory (`default` exit 0, `ANDINO_NEGATIVE=1` exit 1).
- [x] Upgraded skill synchronized directly to local host directories:
  - `~/.claude/skills/andino-workflow/skills/deep-module-design/`
  - `~/.claude/skills/andino-deep-module-design/`
- [x] Git committed and pushed to `origin/andino-workflow`, verified compatible with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.

## Scope

### In Scope
- `skills/deep-module-design/SKILL.md`
- `skills/deep-module-design/GUIDE.md`
- `skills/deep-module-design/resources/dependency-and-seam-discipline.md`
- `skills/deep-module-design/resources/design-it-twice-protocols.md`
- `skills/deep-module-design/resources/leverage-rubric-and-catalogs.md`
- `skills/deep-module-design/resources/worked-example.md`
- `references/legal/provenance.md`
- Host synchronization to `~/.claude/skills/`
- Verification with `ai-rules setup`

### Out of Scope
- Modifying unrelated Andino skills (`andino-architecture-survey`, `andino-api-and-interface-design`, etc.).
- Introducing external network or runtime npm/pip dependencies.
- Modifying application test suites or external project files.

## User Decisions / Clarifications
- **Authorization & Cadence**: User authorized full recommendation and continuous end-to-end execution ("saya setuju semua rekomendasian anda").
- **Visual Reporting Scope**: Terminal-native visual cards (ASCII mass diagrams, cross-section collapse, and Mermaid in markdown) scoped to the module being designed, keeping macro whole-codebase HTML scans in `andino-architecture-survey`.
- **Language Focus**: Multi-ecosystem coverage across TypeScript/JavaScript, Python, Go, and Rust.
- **Verification Harness**: Pure Python 3 standard library with zero external dependencies, validating both default compliance and adversarial negative tamper.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Leverage Over Line Counts**: A deep module is measured by the leverage it gives callers (lots of functionality behind a compact, intuitive interface), never line-count ratios.
- **Seam Justification (2-Adapter Rule)**: Never introduce an abstraction seam without at least 2 concrete adapters (typically production + test stand-in). Single-adapter seams are useless indirection.
- **Replace, Don't Layer**: Do not hoard shallow unit tests when an interface is deepened; delete redundant tests and test through the new interface.
- **Glossary Discipline**: Enforce strict terminology (*module, interface, implementation, depth, seam, adapter, leverage, locality*) to eliminate ambiguity.
- **Progressive Disclosure**: Keep `SKILL.md` dense and under 150 lines to prevent agent context window bloat, delegating deep craft to `GUIDE.md` and specialized resources.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **Module Design vs Whole-Codebase Survey:**
   - *Risk*: Blurring boundaries with `andino-architecture-survey` by attempting full repository scanning.
   - *Resolution*: Negative Gates strictly rule out whole-codebase scans; focus purely on the target module and its immediate callers.
2. **Speculative Abstraction:**
   - *Risk*: AI inventing generic ports/adapters for hypothetical futures.
   - *Resolution*: Enforce the 2-Adapter Rule and the Deletion Test before any interface change.
3. **Internal vs External Seam Leakage:**
   - *Risk*: Exposing internal implementation seams just to make private logic unit-testable.
   - *Resolution*: Explicit invariant stating internal seams remain private; tests cross the external seam.

## Execution Plan & Task Breakdown

### Phase 1: Environment & Preflight Baseline
- [x] Inspect existing `skills/deep-module-design/` files.
- [x] Inspect upstream reference skills (`mattpocock/skills`).
- [x] Inspect peer elevated skills (`constraint-driven-development`, `code-simplification`).
- [x] Conclude Council consultation and receive user approval.
- [x] Initialize execution plan at `docs/exec-plans/active/deep-module-design-elevation.md`.

### Phase 2: Core Resources & Deep Protocols (`resources/`)
- [x] Task 2.1: Author `resources/dependency-and-seam-discipline.md`
- [x] Task 2.2: Author `resources/design-it-twice-protocols.md`
- [x] Task 2.3: Author `resources/leverage-rubric-and-catalogs.md`
- [x] Task 2.4: Overhaul `resources/worked-example.md` with end-to-end domain refactoring and verification harness

### Phase 3: Guide & Operational Contract Overhaul
- [x] Task 3.1: Overhaul `skills/deep-module-design/GUIDE.md`
- [x] Task 3.2: Overhaul `skills/deep-module-design/SKILL.md` (<150 lines)

### Phase 4: Provenance, Verification, Host Sync & Delivery
- [x] Task 4.1: Update `references/legal/provenance.md` with Matt Pocock attribution
- [x] Task 4.2: Execute offline Python verification harness in temporary directory
- [x] Task 4.3: Synchronize upgraded files to `~/.claude/skills/`
- [x] Task 4.4: Verify compatibility with `rtk ai-rules setup --dry-run`
- [x] Task 4.5: Git commit and push to `origin/andino-workflow`
- [x] Task 4.6: Update execution plan to COMPLETED
