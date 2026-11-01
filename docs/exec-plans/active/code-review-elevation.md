# Elevate Code Review to Match and Exceed Upstream Benchmarks

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Successfully elevated `skills/code-review/` on branch `andino-workflow` from an abstract, over-compressed 103-line guide into a premier, bidirectional code review engine. The elevated skill synthesizes the multi-axis quality craft of Addy Osmani's `code-review-and-quality` (5-axis review, named structural remedies, change sizing, dead code hygiene, dependency discipline, and deep security/performance checklists), Matt Pocock's `engineering/code-review` (strict 2-track isolation of Spec Axis vs Standards Axis, 12 Fowler smells catalog), and Obra Superpowers (`requesting-code-review` and `receiving-code-review` protocols, context window isolation, "Spec is a vision document", "Declined to judge" logging, and anti-sycophantic receiving rules) under Andino Workflow governance (proportional investigation, non-recursive anti-loop guards, single durable checkpoints, deterministic offline Python test verification, and complete integration with `ai-rules setup`).

## Objective

Deliver an upgraded, self-contained `skills/code-review` bundle whose AI output quality, analytical rigor, bidirectional lifecycle discipline, and operational ergonomics match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/code-review/resources/checklists.md` created with exhaustive, actionable engineering audit rubrics:
  - Security checklist: STRIDE threat modeling, trust boundaries, credential leak prevention, auth/IDOR checks, input validation & sanitization, destructive path containment (`realpath`, allowlisted roots, race-condition defense), SQL/NoSQL injection defense, and OWASP Top 10 + LLM Top 10 rubrics.
  - Performance checklist: Core Web Vitals targets, TTFB diagnosis, N+1 query detection, database indexing strategies & EXPLAIN ANALYZE baselining, connection pooling invariants, frontend bundle budgets, and read/write caching patterns.
- [x] `skills/code-review/resources/agent-review-protocols.md` created with complete bidirectional subagent lifecycle protocols:
  - Protocol A: Requesting Code Review (subagent prompt template, bounded context handoff without conversational history pollution, "Spec is a vision document" philosophy, and mandatory "Declined to judge" ledger).
  - Protocol B: Conducting Isolated Review (read-only execution, 2-track evaluation, 5-axis scoring, and named structural remedies).
  - Protocol C: Receiving Code Review (anti-sycophancy rules, "Verify before implementing" protocol, 1-cycle deadlock prevention, technical pushback rules, and YAGNI filter).
- [x] `skills/code-review/resources/worked-example.md` created with a realistic end-to-end review walkthrough:
  - Multi-file diff scenario with dual violations (Spec logic failure + Standards security flaw).
  - Concrete pull request comment formatting.
  - Embedded zero-dependency Python verification script (`run_verification.py`) asserting two-axis isolation, severity prefix parsing (`[CRITICAL]`, `[REQUIRED]`, `[SUGGESTION]`, `[NIT]`), and anti-loop negative checks.
- [x] `skills/code-review/GUIDE.md` overhauled with deep craft chapters:
  - The Approval Standard: continuous improvement over perfectionism.
  - Change Sizing and Splitting Strategies: Stack, By File Group, Horizontal, Vertical.
  - The 12 Martin Fowler Smells Catalog mapped directly to Named Structural Remedies.
  - Hierarchy of Disagreement Resolution: technical data > style guides > software design principles > codebase consistency.
  - Dead Code Hygiene and Dependency Discipline.
- [x] `skills/code-review/SKILL.md` overhauled as a high-density operational contract (<150 lines):
  - 2-Axis evaluation router (Spec vs Standards).
  - 5-Axis quality dimensions (Correctness, Readability, Architecture, Security, Performance).
  - Rationalization Refutation Table (anti-shortcuts).
  - 10 Diagnostic Red Flags.
  - Explicit directives pointing to specialized resource files.
- [x] `references/legal/provenance.md` updated with comprehensive audit details and MIT attributions for Addy Osmani, Matt Pocock, and Obra Superpowers.
- [x] Deterministic Python verification script executed and passing in temporary directory.
- [x] Upgraded skill synchronized directly to local host directories:
  - `~/.claude/skills/andino-workflow/skills/code-review/`
  - `~/.claude/skills/andino-code-review/`
- [x] Git committed and pushed to `origin/andino-workflow`, verified compatible with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.

## Scope

### In Scope
- `skills/code-review/SKILL.md`
- `skills/code-review/GUIDE.md`
- `skills/code-review/resources/checklists.md`
- `skills/code-review/resources/agent-review-protocols.md`
- `skills/code-review/resources/worked-example.md`
- `references/legal/provenance.md`
- Host synchronization to `~/.claude/skills/`
- Verification with `ai-rules setup`

### Out of Scope
- Modifying unrelated Andino skills.
- Introducing external network or runtime npm/pip dependencies.
- Breaking backward compatibility with existing Andino method dispatch.

## User Decisions / Clarifications
- **Bidirectional Lifecycle (Decision 1)**: Setuju. The skill covers all three roles: Reviewer (conducting review), Requester (dispatching subagents with bounded context), and Receiver (technical verification, anti-sycophancy, YAGNI defense).
- **Ecosystem Focus (Decision 2)**: Setuju. TypeScript/Node.js, Python, and SQL provide the primary concrete patterns in templates and checklists, while foundational rules remain language-agnostic.
- **Workflow Cadence (Decision 3)**: Setuju ("yoi gas"). Continuous end-to-end execution authorized: Council -> Planning -> Plan Execution -> Verification -> Local Sync -> Commit & Push -> `ai-rules setup` check.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Bilateral Protocol Contract**: Unifying Requesting, Reviewing, and Receiving into a symmetrical protocol eliminates polite hallucinated agreement, which is the root cause of agent regression cascading.
- **Strict 2-Axis Isolation**: Spec Axis (functional requirements) and Standards Axis (code health & smells) must never dilute each other. A clean style cannot pardon a broken feature; a minor smell cannot mask a sound implementation.
- **Falsifiable Findings**: Every actionable defect must provide a concrete failure scenario, `file:line` location, and a named structural remedy rather than vague design critique.
- **Architectural Separation**: `SKILL.md` remains a dense, compact router (<150 lines) to prevent context pollution, delegating detailed operational rubrics to `GUIDE.md` and `resources/`.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **Attention Dilution vs 17-Lens Monolith:**
   - *Risk*: Piling 17 evaluation lenses on every micro-diff overwhelms the LLM and produces noisy, hallucinated false positives on trivial changes.
   - *Resolution*: Proportional activation tiers. Small/mechanical changes receive a lightweight sanity check. High-risk/structural changes activate the full 5-axis review. Cosmetic nits are capped at at most 3 per pass.
2. **Autonomous Reception Deadlocks:**
   - *Risk*: An anti-sycophantic receiver agent argues in an infinite loop against a hallucinating reviewer agent.
   - *Resolution*: 1-cycle verification protocol. The receiver checks the claim against codebase reality. If unverified or inaccurate, it issues a single technical pushback with evidence. If the dispute is unresolved, it escalates to the user/coordinator instead of continuing to debate.
3. **Subjective Smells Halting Delivery:**
   - *Risk*: A reviewer blocking a pull request over subjective aesthetic preferences or debatable naming choices.
   - *Resolution*: Priority gating. Only `[CRITICAL]` (security flaw, data corruption, catastrophic bug) and `[REQUIRED]` (spec violation, hard linter failure) can block completion. `[SUGGESTION]` and `[NIT]` are strictly non-blocking.

### Hal Terlewat (Blind Spots Addressed)
- **Untracked and Staged Scope**: Many reviews fail to review new untracked files or working tree changes because they only diff `HEAD~1..HEAD`. The protocol explicitly enforces pinning `BASE` to `HEAD` plus staged, unstaged, and owned untracked files.
- **Declined to Judge Ledger**: The reviewing agent must explicitly document behaviors outside the review scope, ensuring that silent omissions do not occur.

### Rekomendasi (Recommendation)
Execute the complete 5-file elevation bundle, run zero-dependency offline Python tests, synchronize locally to host skills, commit, push, and verify with `ai-rules setup`.

### Langkah Pertama (First Action)
Create `skills/code-review/resources/checklists.md`.

---

## Task Breakdown & Change Specifications

### Task 1: Create `skills/code-review/resources/checklists.md`
- **File**: `skills/code-review/resources/checklists.md`
- **Contents**:
  - Security Audit Checklist:
    - Threat Modeling (STRIDE, Trust Boundaries, Asset Identification)
    - Pre-Commit Secret Scanning Patterns
    - Authentication & Authorization (IDOR, Role Verification, JWT lifecycle)
    - Input Validation, Type Coercion, Parameterized SQL queries
    - Destructive Path Containment (`realpath`, allowlisted roots, race-condition defense, minimum depth)
    - CORS, Security Headers, and AI/LLM Security (Prompt injection quarantine, untrusted tool inputs)
  - Performance Audit Checklist:
    - Core Web Vitals benchmarks (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1)
    - TTFB diagnostic waterfall
    - Database Query Optimization (N+1 query detection, EXPLAIN ANALYZE baselining, indexing rules)
    - Connection Pooling invariants
    - Caching patterns (Cache-Aside, Read-Through, Write-Through, Negative caching)

### Task 2: Create `skills/code-review/resources/agent-review-protocols.md`
- **File**: `skills/code-review/resources/agent-review-protocols.md`
- **Contents**:
  - Protocol 1: Requesting Code Review (Author / Coordinator)
    - Scope pinning (Base SHA, Head SHA, untracked files)
    - Context isolation (never pass full conversation history to the reviewer)
    - Subagent dispatch prompt template
    - "Spec is a vision document" directive
    - Mandatory "Declined to judge" section
  - Protocol 2: Conducting the Review (Reviewer Subagent)
    - Read-only execution guarantee (no working tree mutations)
    - 2-Axis evaluation (Spec Axis vs Standards Axis)
    - 5-Axis rating taxonomy (Correctness, Readability, Architecture, Security, Performance)
    - Severity prefixes: `[CRITICAL]`, `[REQUIRED]`, `[SUGGESTION]`, `[NIT]`, `[FYI]`
    - Named structural remedies with code snippets
  - Protocol 3: Receiving Code Review (Author / Implementer)
    - 6-step cycle: Read -> Understand -> Verify -> Evaluate -> Respond -> Implement
    - Forbidden responses (prohibiting performative sycophancy: "You're absolutely right!", "Great point!")
    - 1-cycle deadlock prevention and technical pushback format
    - YAGNI check for speculative "enterprise/professional" suggestions

### Task 3: Create `skills/code-review/resources/worked-example.md`
- **File**: `skills/code-review/resources/worked-example.md`
- **Contents**:
  - End-to-end realistic scenario: multi-file payment gateway integration with a subtle boundary failure (Spec) and dynamic eval/untrusted deserialization (Standards/Security).
  - Formatted Pull Request comment example illustrating two-axis separation and named structural remedy.
  - Complete, runnable standard-library Python verification script (`run_verification.py`) testing:
    - Spec vs Standards separation
    - Severity prefix enforcement
    - Anti-loop deadlock defense
    - Negative test scenario via `ANDINO_NEGATIVE=1`

### Task 4: Overhaul `skills/code-review/GUIDE.md`
- **File**: `skills/code-review/GUIDE.md`
- **Contents**:
  - The Approval Standard: continuous improvement over perfectionism
  - Change Sizing & Splitting: Stack, File Group, Horizontal, Vertical
  - The 12 Martin Fowler Smells Catalog mapped to Named Structural Remedies:
    - Mysterious Name -> Rename to domain intent
    - Duplicated Code -> Extract canonical helper
    - Feature Envy -> Relocate logic to data owner
    - Data Clumps -> Group into typed domain model
    - Primitive Obsession -> Wrap in branded/value types
    - Repeated Switches -> Polymorphic dispatcher or lookup table
    - Shotgun Surgery -> Consolidate related changes into single module
    - Divergent Change -> Split responsibilities
    - Speculative Generality -> Delete unused abstractions (YAGNI)
    - Message Chains -> Hide delegation
    - Middle Man -> Inline useless pass-through wrappers
    - Refused Bequest -> Replace inheritance with composition
  - Hierarchy of Disagreement Resolution (Technical facts > Style guides > Design principles > Consistency)
  - Dead Code Hygiene & Dependency Discipline

### Task 5: Overhaul `skills/code-review/SKILL.md`
- **File**: `skills/code-review/SKILL.md`
- **Contents**:
  - Frontmatter: name `andino-code-review`, description, internal method ID
  - Purpose & 2-Axis / 5-Axis overview
  - ASCII 2-Axis Quality Architecture flowchart
  - Scope Pinning & Prerequisites (committed + staged + unstaged + untracked)
  - Execution Procedure (6 strict operational steps)
  - Rationalization Refutations Table (7 common agent bypass excuses)
  - 10 Diagnostic Red Flags
  - Resource pointers to `GUIDE.md`, `checklists.md`, `agent-review-protocols.md`, and `worked-example.md`
  - Provenance & MIT attribution statement
  - Length constraint: <150 lines

### Task 6: Update `references/legal/provenance.md`
- **File**: `references/legal/provenance.md`
- **Contents**:
  - Add elevation record for `code-review` detailing adaptation from Addy Osmani, Matt Pocock, and Obra Superpowers.

### Task 7: Deterministic Python Verification
- Execute `run_verification.py` in isolated temporary directory.
- Verify positive path passes and negative path (`ANDINO_NEGATIVE=1`) fails as expected.

### Task 8: Local Host Synchronization
- Synchronize elevated skill files directly to `~/.claude/skills/andino-workflow/skills/code-review/` and `~/.claude/skills/andino-code-review/`.

### Task 9: Git Commit, Push, and Setup Verification
- Git commit with standard conventional message.
- Git push to `origin/andino-workflow`.
- Verify with `rtk ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
