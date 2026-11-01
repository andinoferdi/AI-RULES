# Elevate Code Simplification to Match and Exceed Upstream Benchmarks

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Successfully elevated `skills/code-simplification/` on branch `andino-workflow` from an abstract, over-compressed 105-line guide into a premier, behavior-preserving code simplification engine. The elevated skill synthesizes the generative craft of Addy Osmani's `code-simplification` (The Five Principles, Chesterton's Fence, Rule of 500, Anti-Rationalization Refutation Table, 8 Diagnostic Red Flags, multi-language Before/After catalogs in TypeScript/JS, Python, and React) with Andino Workflow governance (lossless cognitive compression, semantic invariance, dominant negative gates, SHA-256 protected regions, subagent safety protocols, offline Python stdlib verification, and complete integration with `ai-rules setup`).

## Objective

Deliver an upgraded, self-contained `skills/code-simplification` bundle whose AI output quality, analytical rigor, behavior-preserving guarantees, and operational ergonomics match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/code-simplification/resources/worked-example.md` created with a realistic end-to-end refactoring walkthrough:
  - Multi-function before/after scenario addressing deep nesting, redundant async, boolean flags, and dead pass-throughs.
  - Byte-exact preservation of a high-performance `# simplify-ignore-start/end` block.
  - Embedded zero-dependency Python verification script (`run_verification.py`) asserting behavior parity (`observed(before, x) == observed(after, x)`), SHA-256 byte-exact region preservation, AST signature freezing, and anti-loop negative checks.
- [x] `skills/code-simplification/resources/protected-regions.md` overhauled with multi-language comment syntax support (`//`, `#`, `/* */`, `<!-- -->`), whitespace-exact hashing rules, and emergency rollback protocols.
- [x] `skills/code-simplification/resources/agent-simplification-protocols.md` created with subagent safety protocols:
  - Protocol A: Scoping & Requesting Simplification (bounded diff inspection, "No Test, No Touch" invariant).
  - Protocol B: Isolated Execution Constraints (prohibition of modifying error types, stripping defensive checks, or altering side-effect order).
  - Protocol C: Simplification Ledger & Verification Gate (recording complexity delta, zero test modification rule).
- [x] `skills/code-simplification/resources/patterns-and-anti-patterns.md` created with exhaustive, actionable multi-language transformation catalogs:
  - TypeScript / Modern JavaScript: Chained ternaries to lookup maps, async/await unwrapping invariants, nested reduces to imperative maps, boolean predicate extraction, optional chaining vs explicit guards.
  - Python: Dictionary comprehensions, guard clauses with early returns, context managers over manual cleanup, exception hierarchy preservation.
  - React / JSX: Flattening conditional render trees, extracting computed variant variables, prop drilling vs composition evaluation.
- [x] `skills/code-simplification/GUIDE.md` overhauled with deep craft chapters:
  - The Comprehension Standard: "Would an on-call engineer at 2 AM locate a bug in this function in 15 seconds?"
  - Cognitive Load Theory in code: Accidental complexity vs Essential complexity.
  - Chesterton's Fence & Git Blame Archeology.
  - The Rule of 500: Automated AST codemods vs manual micro-refactoring.
  - The 4-Step Simplification Lifecycle (Understand -> Identify -> Apply Incrementally -> Verify).
- [x] `skills/code-simplification/SKILL.md` overhauled as a high-density operational contract (<150 lines):
  - Progressive disclosure router pointing to specialized resources.
  - Dominant Negative Gates ("When NOT to simplify").
  - The Five Principles.
  - Anti-Rationalization Refutation Table.
  - 8 Diagnostic Red Flags.
  - Runnable standard-library operational example (`andino-operational-example`).
- [x] `references/legal/provenance.md` updated with comprehensive audit details and MIT attributions for Addy Osmani's `code-simplification`.
- [x] Deterministic Python verification script executed and passing in temporary directory (default parity=true, negative tamper=false).
- [x] Upgraded skill synchronized directly to local host directories:
  - `~/.claude/skills/andino-workflow/skills/code-simplification/`
  - `~/.claude/skills/andino-code-simplification/`
- [x] Git committed and pushed to `origin/andino-workflow`, verified compatible with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.

## Scope

### In Scope
- `skills/code-simplification/SKILL.md`
- `skills/code-simplification/GUIDE.md`
- `skills/code-simplification/resources/worked-example.md`
- `skills/code-simplification/resources/protected-regions.md`
- `skills/code-simplification/resources/agent-simplification-protocols.md`
- `skills/code-simplification/resources/patterns-and-anti-patterns.md`
- `references/legal/provenance.md`
- Host synchronization to `~/.claude/skills/`
- Verification with `ai-rules setup`

### Out of Scope
- Modifying unrelated Andino skills.
- Introducing external network or runtime npm/pip dependencies.
- Modifying test files during code simplification passes.

## User Decisions / Clarifications
- **Authorization & Cadence**: User authorized full recommendation and continuous end-to-end execution ("saya ikut rekom anda pokonya").
- **Language Focus**: TypeScript/JavaScript, Python, and React provide the concrete catalogs, with core heuristics remaining language-agnostic.
- **Safety Stance**: Negative gates ("When NOT to simplify") take precedence over transformation catalogs to prevent *Law of the Instrument* over-refactoring.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Lossless Cognitive Compression**: True simplification reduces state space and accidental complexity without removing essential complexity or error handling.
- **Semantic Invariance**: External behavior, side-effect order, and exception contracts must be 100% preserved. Zero modifications to existing tests are allowed.
- **Progressive Disclosure**: Keep `SKILL.md` dense and under 150 lines to prevent context window saturation, routing to deep `GUIDE.md` and on-demand `resources/`.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **Law of the Instrument vs Rich Catalogs:**
   - *Risk*: A huge catalog makes AI act as an over-aggressive pattern matcher, forcing one-liners on already clean code.
   - *Resolution*: Dominant **Negative Gates** placed before transformation catalogs, enforcing "No Test, No Touch" and prohibiting changes to hot-paths or domain compliance logic.
2. **Short vs Simple Confusion:**
   - *Risk*: AI compresses readable 10-line logic into 2 impenetrable chained ternary lines.
   - *Resolution*: The 2 AM On-Call Engineer test ("Can someone debug this in 15 seconds?") and explicit Anti-Rationalization rules against line-count optimization.
3. **Silent Semantic Erosion:**
   - *Risk*: Removing defensive checks that AI misidentifies as "redundant boilerplate".
   - *Resolution*: Agent simplification protocol forbids deleting defensive guards or changing exception types unless explicitly proven unreachable by caller invariant proofs.

### Hal Terlewat (Blind Spots Addressed)
- **Protected Regions Across Comment Formats**: Protected markers must work seamlessly across `//`, `#`, `/* */`, and HTML/JSX `<!-- -->` without syntax breakages.
- **Simplification Ledger**: Subagents must produce a brief summary of complexity reduction and invariant proofs for the durable ticket.

### Rekomendasi (Recommendation)
Execute the complete 6-file elevation bundle, run zero-dependency offline Python tests, synchronize locally to host skills, commit, push, and verify with `ai-rules setup`.

### Langkah Pertama (First Action)
Create `skills/code-simplification/resources/worked-example.md`.

---

## Task Breakdown & Change Specifications

### Task 1: Create `skills/code-simplification/resources/worked-example.md`
- **File**: `skills/code-simplification/resources/worked-example.md`
- **Dependencies**: None
- **Spec**: Comprehensive end-to-end scenario demonstrating real-world refactoring, protected region preservation, and an embedded zero-dependency Python test suite (`run_verification.py`).

### Task 2: Create `skills/code-simplification/resources/protected-regions.md` & `skills/code-simplification/resources/agent-simplification-protocols.md`
- **Files**:
  - `skills/code-simplification/resources/protected-regions.md`
  - `skills/code-simplification/resources/agent-simplification-protocols.md`
- **Dependencies**: Task 1
- **Spec**: Robust multi-comment hash preservation procedure and subagent safety protocol (bounded scope, negative checks, invariant ledger).

### Task 3: Create `skills/code-simplification/resources/patterns-and-anti-patterns.md`
- **File**: `skills/code-simplification/resources/patterns-and-anti-patterns.md`
- **Dependencies**: Task 1
- **Spec**: Exhaustive Before/After transformation tables for TypeScript/JavaScript, Python, and React, contrasting flawed compact code with readable clear code.

### Task 4: Overhaul `skills/code-simplification/GUIDE.md`
- **File**: `skills/code-simplification/GUIDE.md`
- **Dependencies**: Tasks 1-3
- **Spec**: Deep craft guide incorporating Chesterton's Fence, Cognitive Load Theory, Rule of 500, 4-step process, and verification rubrics.

### Task 5: Overhaul `skills/code-simplification/SKILL.md`
- **File**: `skills/code-simplification/SKILL.md`
- **Dependencies**: Tasks 1-4
- **Spec**: High-density operational router (<150 lines), The Five Principles, Negative Gates, Anti-Rationalization Table, 8 Red Flags, and standard operational example.

### Task 6: Update `references/legal/provenance.md`
- **File**: `references/legal/provenance.md`
- **Dependencies**: Tasks 1-5
- **Spec**: Audit notes and MIT attribution for Addy Osmani 2025.

### Task 7: Deterministic Offline Python Test Verification
- **Dependencies**: Tasks 1-6
- **Spec**: Run embedded verification scripts in temporary directory asserting bit-for-bit behavior parity and negative tamper detection.

### Task 8: Local Host Synchronization
- **Directories**:
  - `~/.claude/skills/andino-workflow/skills/code-simplification/`
  - `~/.claude/skills/andino-code-simplification/`
- **Dependencies**: Task 7
- **Spec**: Copy all elevated files directly to local host skill stores.

### Task 9: `ai-rules setup` Dry-Run, Commit & Push
- **Dependencies**: Task 8
- **Spec**: Verify with `rtk ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`, commit with conventional commit message, and push to `origin/andino-workflow`.
