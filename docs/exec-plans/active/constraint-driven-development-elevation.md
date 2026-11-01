# Elevate Constraint-Driven Development to Match and Exceed Upstream Benchmarks

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Elevate `skills/constraint-driven-development/` on branch `andino-workflow` from an over-compressed 102-line guide and duplicate `GUIDE.md` into a premier, machine-enforced quality contract engine. The elevated skill synthesizes the generative craft of Addy Osmani's `constraint-driven-development` (4-question intake discipline with sane defaults, de facto tooling matrices, diff-scoped floor guard catching the 5 evasion moves, circularity rank, ratcheting mechanics, and scanner exit-code normalization) with Andino Workflow governance (high-density <150 line operational contract `SKILL.md`, deep craft `GUIDE.md`, dual-runtime Python stdlib and Node.js floor guards, multi-language catalog across TS/JS, Python, Go, Rust, and Web UI, zero-dependency offline Python stdlib verification, and complete integration with `ai-rules setup`).

## Objective

Deliver an upgraded, self-contained `skills/constraint-driven-development` bundle whose AI output quality, analytical rigor, mechanical enforcement, and operational ergonomics match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/constraint-driven-development/SKILL.md` overhauled as a high-density operational contract (<150 lines):
  - 4-Question Intake Discipline with sane defaults and cost trade-offs.
  - Dominant Negative Gates ("When NOT to use").
  - The 5 Floor Invariants (always enforced, zero setup required).
  - Anti-Rationalization Refutations Table.
  - Diagnostic Red Flags (Stop Immediately).
  - Progressive disclosure router to `resources/`.
  - Runnable standard-library operational example (`andino-operational-example`) with default passing and adversarial `ANDINO_NEGATIVE=1` variant.
- [x] `skills/constraint-driven-development/GUIDE.md` overhauled with deep craft chapters:
  - Irreversible Quality Ratcheting & Lossless Quality Preservation.
  - The 3-Tier Circularity Hierarchy: External vs. Project vs. Suite checks.
  - 4-Stage Lifecycle Integration (BUILD <5s, VERIFY <90s, REVIEW minutes, SHIP in CI).
  - The Ratchet Mechanism: "Measure today and hold the line".
  - The 5 AI Evasion Moves and detection mechanics.
  - Exception Management & Lifecycle (W/E ID, path, reason, owner, 90-day expiry).
- [x] `skills/constraint-driven-development/resources/floor-guard.md` created with complete dual-runtime diff-scoped implementations:
  - Node.js ESM script (`floor-guard.mjs`) for modern JS/TS stacks.
  - Pure Python 3.8+ stdlib script (`floor_guard.py`) with zero external dependencies for Python/Go/Rust/C++ stacks.
  - Cross-platform Windows/POSIX path handling, NUL-separated path inventories, and CRLF normalization.
  - Exit codes: `0` clean, `1` floor violation, `2` execution error / unreadable diff.
- [x] `skills/constraint-driven-development/resources/quality-gate-protocols.md` created:
  - Exit code normalization for third-party tools (Semgrep, Axe-core, Lighthouse, Stryker).
  - Mandatory `--redact` security scan protocol to prevent secret leakage in agent transcripts.
  - Automated translation of CLI JSON reports to binary block/pass verdicts.
- [x] `skills/constraint-driven-development/resources/constraint-catalog.md` created with exhaustive presets:
  - TypeScript & JavaScript: Typecheck, Biome/ESLint, Vitest/Jest coverage, size-limit.
  - Python: Ruff check/format, Mypy/Pyright, Pytest-cov, Semgrep.
  - Go: `go test -cover`, `golangci-lint`, `govulncheck`.
  - Rust: `cargo test`, `clippy -- -D warnings`, `cargo-audit`, `cargo-tarpaulin`.
  - Frontend Web: Lighthouse performance budgets (LCP <= 2500ms, CLS <= 0.1), Axe-core WCAG AA accessibility.
- [x] `skills/constraint-driven-development/resources/worked-example.md` created with an end-to-end scenario:
  - Interactive intake walk-through.
  - Production `CONSTRAINTS.md` template generation.
  - Baseline ratchet initialization for legacy deficits.
  - Real-world PR review rejecting an evasion attempt (loosened threshold, removed assertion, skipped test).
  - Embedded zero-dependency verification script.
- [x] `references/legal/provenance.md` updated with audit trail and MIT attribution to Addy Osmani.
- [x] Deterministic Python verification script executed and passing in temporary directory (`default` exit 1 with expected rules, `ANDINO_NEGATIVE=1` exit 2).
- [x] Upgraded skill synchronized directly to local host directory `~/.claude/skills/andino-workflow/skills/constraint-driven-development/`.
- [x] Git committed and pushed to `origin/andino-workflow`, verified compatible with `ai-rules setup`.

## Scope

### In Scope
- `skills/constraint-driven-development/SKILL.md`
- `skills/constraint-driven-development/GUIDE.md`
- `skills/constraint-driven-development/resources/floor-guard.md`
- `skills/constraint-driven-development/resources/quality-gate-protocols.md`
- `skills/constraint-driven-development/resources/constraint-catalog.md`
- `skills/constraint-driven-development/resources/worked-example.md`
- `references/legal/provenance.md`
- Host synchronization to `~/.claude/skills/andino-workflow/skills/constraint-driven-development/`
- Verification with `ai-rules setup`

### Out of Scope
- Modifying unrelated Andino skills.
- Introducing third-party npm or pip dependencies for the floor guards.
- Altering existing project test suites or application source code.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Mechanical Invariants**: Prose quality goals erode across LLM turns; binary exit codes (`0` vs `1`) maintain mechanical integrity.
- **Diff-Scoping**: Checking the delta (`merge-base -> working-tree + untracked`) is essential to prevent penalizing agents for legacy debt.
- **Progressive Disclosure**: Keep `SKILL.md` lean (<150 lines) for the runtime agent loop, routing deep craft and multi-language catalogs to `GUIDE.md` and `resources/`.
- **Zero-Dependency Portability**: Python stdlib + Node built-ins only; no mandatory global installs for the core guard.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **Context Window Saturation vs. Rich Catalogs**:
   - *Risk*: A sprawling 5-ecosystem catalog inside `SKILL.md` causes prompt dilution.
   - *Resolution*: Place all detailed matrices in `resources/constraint-catalog.md`. `SKILL.md` holds only the 4-question intake, sane defaults, and the 5 floor invariants.
2. **Dual-Runtime Maintenance Tax**:
   - *Risk*: Node and Python scripts drifting in regex logic or failing on Windows CRLF/paths.
   - *Resolution*: Implement identical regex patterns, strict test fixtures, and universal path/line normalization across both scripts.
3. **CI vs. Agent Loop Confusion**:
   - *Risk*: Teams view `CONSTRAINTS.md` as redundant with existing CI.
   - *Resolution*: Frame `CONSTRAINTS.md` strictly as in-loop agent boundaries (fast feedback <5s mid-task) that protect code before it ever reaches CI.

### Hal Terlewat (Blind Spots Addressed)
- **Windows Path & CRLF Handling**: Diff collectors must handle Windows backslashes and line endings reliably.
- **Lightweight Exception Schema**: Support standard `W1`, `E1` tracked exception rows with owner and 90-day expiry to prevent ratchet deadlocks.

---

## Execution Plan & Phased Tasks

### Phase 1: Invariant Anchoring & Floor Guard Engine
- [x] Task 1.1: Author `skills/constraint-driven-development/resources/floor-guard.md` with complete dual-runtime Node.js and Python stdlib diff-scoped implementations.
- [x] Task 1.2: Author `skills/constraint-driven-development/resources/quality-gate-protocols.md` with exit-code normalizer and secret redaction rules.

### Phase 2: Presets & Real-World Walkthrough
- [x] Task 2.1: Author `skills/constraint-driven-development/resources/constraint-catalog.md` with multi-language tooling matrices and sane defaults.
- [x] Task 2.2: Author `skills/constraint-driven-development/resources/worked-example.md` with interactive intake, ratchet setup, and anti-evasion verification.

### Phase 3: Core Craft Guide & Operational Contract
- [x] Task 3.1: Overhaul `skills/constraint-driven-development/GUIDE.md` with deep craft chapters, 4-stage lifecycle, circularity guards, and ratchet mechanics.
- [x] Task 3.2: Overhaul `skills/constraint-driven-development/SKILL.md` as a high-density (<150 lines) operational contract with runnable Python stdlib operational example.
- [x] Task 3.3: Update `references/legal/provenance.md` with complete audit provenance and Addy Osmani MIT attribution.

### Phase 4: Deterministic Verification & Validation
- [x] Task 4.1: Execute offline Python operational example probe in temporary directory (assert default exit 1 on violations, exit 2 on baseline failure).
- [x] Task 4.2: Verify file sizes, progressive disclosure links, and format consistency across all 6 files.

### Phase 5: Host Synchronization, Setup Verification & Git Delivery
- [x] Task 5.1: Synchronize updated skill files to `~/.claude/skills/andino-workflow/skills/constraint-driven-development/`.
- [x] Task 5.2: Test compatibility with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
- [x] Task 5.3: Git commit with descriptive message and push to `origin/andino-workflow`.

---

## Next Action
None — task complete. All acceptance criteria satisfied, verified offline, synchronized to host, committed, and pushed.
