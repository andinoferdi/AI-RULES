# Elevate Context Engineering to Match and Exceed Upstream Benchmarks

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Host Synchronization, Setup Verification & Git Delivery
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Elevate `skills/context-engineering/` on branch `andino-workflow` from an over-compressed 100-line guide with duplicate `GUIDE.md` into a premier, machine-enforced context engineering and memory architecture engine. The elevated skill synthesizes the generative craft of Addy Osmani's `context-engineering` (5-level context hierarchy, trust-level boundaries, multi-harness rules-file templates, selective include/brain dump/project map packing patterns, lost-in-the-middle recency ordering, context budget management, and confusion triage protocols) with Andino Workflow governance (high-density <150 line operational contract `SKILL.md`, deep craft `GUIDE.md`, prefix-stable KV-cache alignment, untrusted prompt injection quarantine, multi-harness rules catalogs across Claude Code, Codex, Cursor, and Windsurf, and offline deterministic Python stdlib verification).

## Objective

Deliver an upgraded, self-contained `skills/context-engineering` bundle whose AI output quality, analytical rigor, mechanical enforcement, and operational ergonomics match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/context-engineering/SKILL.md` overhauled as a high-density operational contract (<150 lines):
  - 4-Question Intake Discipline with sane defaults and budget trade-offs.
  - Dominant Negative Gates ("When NOT to use").
  - The 5 Context Hierarchy Invariants (Rules -> Spec -> Source -> Error/Logs -> History).
  - Anti-Rationalization Refutations Table.
  - Diagnostic Red Flags (Stop Immediately).
  - Progressive disclosure router to `resources/`.
  - Runnable standard-library operational example (`andino-operational-example`) with default passing and adversarial `ANDINO_NEGATIVE=1` variant.
- [x] `skills/context-engineering/GUIDE.md` overhauled with deep craft chapters:
  - The Context Hierarchy & Trust Boundaries (Trusted vs Verify vs Untrusted Quarantine).
  - Working Desk vs Filing Cabinet: Cognitive Capacity & Attention Budgets.
  - Positional Encoding & Lost-in-the-Middle Recency Ordering.
  - Prefix-Stable KV-Cache Optimization (Static prefixes for prompt cache reuse).
  - Multi-Turn Compaction & Pruning Heuristics (What to cut first vs What to protect).
  - Confusion Management & Inline Planning Patterns (A/B/C triage).
  - Restartable Session Boundary Handoff Protocols.
- [x] `skills/context-engineering/resources/context-budget-and-packing.md` created:
  - Budget math and line/token heuristics (<2,000 lines per task rule).
  - Three Packing Strategies: Brain Dump, Selective Include, Hierarchical Project Map.
  - Token-efficient log and diff sanitization (collapsing stack traces, stripping lockfiles/AST noise).
  - Recency ordering algorithms and multi-turn compaction procedures.
- [x] `skills/context-engineering/resources/rules-file-catalog.md` created with multi-harness presets:
  - Claude Code (`CLAUDE.md`)
  - OpenAI Codex (`AGENTS.md`)
  - Cursor (`.cursorrules` & `.cursor/rules/*.md`)
  - Windsurf (`.windsurfrules`)
  - Stack presets: TypeScript/Next.js, Python/FastAPI, Go/Rust.
- [x] `skills/context-engineering/resources/confusion-and-ambiguity-protocols.md` created:
  - Formal A/B/C triage schemas for conflicting specs/code.
  - 3-step Inline Planning Pattern before multi-step executions.
  - Hallucination circuit-breakers & missing requirements procedures.
  - Untrusted data boundary quarantine (preventing prompt injection via data/web/logs).
- [x] `skills/context-engineering/resources/worked-example.md` created with an end-to-end scenario:
  - Interactive intake walk-through.
  - Session restart with bounded context reconstruction.
  - Active ambiguity detection and A/B/C triage in action.
  - Bounded handoff package generation without context dilution.
  - Embedded zero-dependency verification script in Python 3.8+ stdlib.
- [x] `references/legal/provenance.md` updated with audit trail and MIT attribution to Addy Osmani.
- [x] Deterministic Python verification script executed and passing in temporary directory (`default` exit 0, `ANDINO_NEGATIVE=1` exit 2).
- [x] Upgraded skill synchronized directly to local host directory `~/.claude/skills/andino-workflow/skills/context-engineering/`.
- [x] Verified compatible with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
- [x] Git committed and pushed to `origin/andino-workflow`.

## Scope

### In Scope
- `skills/context-engineering/SKILL.md`
- `skills/context-engineering/GUIDE.md`
- `skills/context-engineering/resources/context-budget-and-packing.md`
- `skills/context-engineering/resources/rules-file-catalog.md`
- `skills/context-engineering/resources/confusion-and-ambiguity-protocols.md`
- `skills/context-engineering/resources/worked-example.md`
- `references/legal/provenance.md`
- Host synchronization to `~/.claude/skills/andino-workflow/skills/context-engineering/`
- Verification with `ai-rules setup`
- Git commit & push

### Out of Scope
- Modifying unrelated Andino skills or core orchestrator code.
- Introducing third-party npm or pip dependencies.
- Creating runtime external network dependencies or mandatory API services.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Attention as Finite Zero-Sum Resource**: Attention softmax competing weights mean noise directly dilutes instruction compliance. Signal-to-noise ratio (SNR) is the primary determinant of agent output quality.
- **Lost-in-the-Middle Recency Pinning**: Placing active constraints and current errors at the tail (closest to generation) is critical.
- **Progressive Disclosure Discipline**: `SKILL.md` must remain strictly compact (<150 lines) so loading the skill does not itself pollute the agent's context window. Supporting catalogs and deep theory must reside in `resources/` and be loaded only when explicitly needed.
- **Bounded Verification**: The Python test runner must deterministically verify packing math, budget boundaries, and recency ordering invariants, without falsely claiming to measure LLM attention quality.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **The Meta-Bloat Irony (Contrarian Risk)**:
   - *Risk*: A sprawling multi-file skill teaching context thrift consumes thousands of prompt tokens if dumped into context.
   - *Resolution*: Enforce strict progressive disclosure. `SKILL.md` holds only the operational contract (<150 lines), 4-question intake, negative gates, core invariants, anti-rationalization table, and the Python test. All templates and catalogs live in `resources/` on disk and are referenced by path.
2. **Multi-Harness Template Maintenance Drag**:
   - *Risk*: Static templates for 4 harnesses across multiple stacks rotting over time.
   - *Resolution*: Focus on foundational structural patterns (commands, tech stack, code conventions, hard boundaries, patterns) rather than ephemeral vendor-specific quirks.
3. **Cognitive Stalling on Trivial Ambiguity**:
   - *Risk*: Agents generating excessive A/B/C questionnaires for minor ambiguities instead of writing code.
   - *Resolution*: Mandate in `confusion-and-ambiguity-protocols.md` that agents ONLY surface material, blocking contradictions. Trivial details with clear codebase precedent must be resolved inline using existing patterns.

### Hal Terlewat (Blind Spots Addressed)
- **Prefix-Stable KV-Cache Alignment**: Ensuring rules files and invariant definitions stay static at the head of context to maximize provider prompt-cache reuse.
- **Untrusted Input Quarantine**: Treating external logs, configs, and web data as passive strings inside clear delimiters to prevent indirect prompt injection.

---

## Execution Plan & Phased Tasks

### Phase 1: Foundational Resource Modules
- [x] Task 1.1: Author `skills/context-engineering/resources/context-budget-and-packing.md` (budget calculations, desk vs filing cabinet, lost-in-the-middle recency ordering, prefix-stable KV-cache alignment, log token sanitization, multi-turn compaction heuristics).
- [x] Task 1.2: Author `skills/context-engineering/resources/rules-file-catalog.md` (multi-harness rules templates for Claude Code `CLAUDE.md`, Codex `AGENTS.md`, Cursor `.cursorrules`, Windsurf `.windsurfrules` across TS/Next.js, Python/FastAPI, Go/Rust).
- [x] Task 1.3: Author `skills/context-engineering/resources/confusion-and-ambiguity-protocols.md` (structured A/B/C triage, inline planning pattern, hallucination circuit-breakers, untrusted input quarantine).

### Phase 2: Verification Harness & End-to-End Walkthrough
- [x] Task 2.1: Author `skills/context-engineering/resources/worked-example.md` (end-to-end scenario: session restart -> context budgeting -> selective include -> confusion triage -> clean handoff, plus zero-dependency deterministic Python stdlib verification probe).

### Phase 3: Core Craft Guide & Operational Contract
- [x] Task 3.1: Overhaul `skills/context-engineering/GUIDE.md` (deep craft manual: 5-level hierarchy, trust levels, recency ordering, prefix stability, memory handoff protocol).
- [x] Task 3.2: Overhaul `skills/context-engineering/SKILL.md` (high-density <150 line operational contract, 4-question intake discipline with sane defaults, dominant negative gates, anti-rationalization table, diagnostic red flags, runnable Python stdlib operational example).
- [x] Task 3.3: Update `references/legal/provenance.md` with complete audit provenance and Addy Osmani MIT attribution.

### Phase 4: Deterministic Verification & Validation
- [x] Task 4.1: Execute offline Python operational example probe in temporary directory (assert default exit 0 on valid packing, exit 2 on `ANDINO_NEGATIVE=1`).
- [x] Task 4.2: Verify file sizes (<150 lines for SKILL.md), progressive disclosure links, and format consistency across all 6 files.

### Phase 5: Host Synchronization, Setup Verification & Git Delivery
- [x] Task 5.1: Synchronize updated skill files to `~/.claude/skills/andino-workflow/skills/context-engineering/`.
- [x] Task 5.2: Test compatibility with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
- [x] Task 5.3: Git commit with descriptive message and push to `origin/andino-workflow`.

---

## Next Action
None — task complete. All acceptance criteria satisfied, verified offline, synchronized to host, committed, and pushed.
