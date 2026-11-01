# Elevate Delegation to Match and Exceed Upstream Benchmarks

Status: COMPLETE_PENDING_PUSH
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification, Host Sync & Delivery
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Elevate `skills/delegation` on branch `andino-workflow` from an over-compressed 209-line duplicate guide (`SKILL.md` and `GUIDE.md` nearly identical, 16-line `contract.md`) into a premier, machine-enforced multi-agent orchestration and task decomposition engine. The elevated skill synthesizes the generative craft of:
1. **Matt Pocock** (`implement-spec`): Task graph DAG modeling, active unblocked frontier tracking, context pointers replacing chat history dumps, and clean integration branch lifecycle.
2. **Jesse Vincent / Obra** (`dispatching-parallel-agents`): Problem domain independence testing, single-turn multi-dispatch concurrency, zero context pollution, and cross-domain integration verification.
3. **Jesse Vincent / Obra** (`subagent-driven-development`): Fresh subagent per task, two-track review gate (Spec Compliance vs Code Quality), 5-round escalating fix loop (Rounds 1-3 resume, Rounds 4-5 model tier bump), Rule of 5 circuit breaker with durable `Ruling: ...` taxonomy, compaction-proof append-only progress ledger, and isolated brief/diff packaging.
4. **Andino Workflow Governance**: High-density operational contract `SKILL.md` (<150 lines) structured as a Gated Finite State Machine (Gated FSM) with tri-modal triage (Inline vs Parallel Dispatch vs Subagent-Driven), deep craft `GUIDE.md`, 5 modular resource specifications, dual-runtime (Python 3 stdlib + POSIX shell) cross-platform portability for Windows/Linux/macOS, dual-mode workspace isolation (Git worktree + in-tree directory fallback), offline deterministic verification (<0.2s), host synchronization, and full compatibility with `ai-rules setup`.

## Objective

Deliver an upgraded, self-contained `skills/delegation` bundle whose orchestration precision, mechanical enforcement, token efficiency, and cross-platform reliability match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/delegation/resources/frontier-and-dag-protocols.md` created:
  - DAG task graph modeling, dependency validation, and active frontier resolution.
  - Disjoint write path analyzer, lexical prefix overlap detection, and lock collision prevention.
  - Tri-modal execution selection heuristics (when to use Inline vs Parallel vs Subagent-Driven).
- [x] `skills/delegation/resources/subagent-brief-and-report-schemas.md` created:
  - Zero Context Bleed: Pure pointer-based brief schema (task ID, spec anchor, owned paths, contract interfaces, test command, report path).
  - Strict Boundary enforcement: Prohibition against subagents spawning subagents, mutating unowned files, or hiding errors.
  - Standardized short-status contract (<15 lines terminal return, detailed evidence in report file).
- [x] `skills/delegation/resources/two-track-review-and-fix-loop.md` created:
  - Two-Track Review Gates: Track 1 (Spec Compliance: ✅/❌/⚠️) vs Track 2 (Code Quality: Approved / Needs fixes).
  - Scoped diff packaging (`review-package`) ensuring reviewers only inspect the net diff with context.
  - 5-Round Fix Loop: Rounds 1-3 resume original implementer; Rounds 4-5 model tier escalation.
  - Rule of 5 Circuit Breaker and `Ruling: <decision> — <reason> — <cost if wrong>` taxonomy in progress ledger.
- [x] `skills/delegation/resources/workspace-and-isolation-guards.md` created:
  - Dual-mode workspace: Git Worktree vs in-tree `.andino/delegation/<plan-id>/` directory with automatic `.gitignore`.
  - Windows file-locking defense: retry with backoff on `EBUSY`/`EPERM`, `index.lock` cleanup.
  - Compaction-resistant append-only ledger (`progress.md`) format and recovery protocols.
  - Safe workspace teardown and cleanup protocols without touching sibling plans.
- [x] `skills/delegation/resources/worked-example.md` created:
  - Real-world end-to-end case study (auth token service decomposition into 3 independent modules: token signer, refresh store, auth middleware).
  - Embedded zero-dependency Python stdlib operational test suite verifying the complete contract offline (<0.2s, exit 0 default, exit 1 on defect or negative mode).
- [x] Dual-runtime cross-platform helper scripts created in `skills/delegation/scripts/`:
  - `delegation_workspace.py` & `delegation-workspace` (wrapper)
  - `task_brief.py` & `task-brief` (wrapper)
  - `review_package.py` & `review-package` (wrapper)
- [x] `skills/delegation/GUIDE.md` overhauled with deep craft chapters:
  - Synthesis of Pocock, Vincent (Obra), and Andino Workflow governance.
  - Tri-modal execution FSM: Inline -> Parallel Dispatch -> Subagent-Driven.
  - Model & reasoning effort selection tiering rubric.
  - Anti-rationalization table and 8 AI evasion move counters.
  - Compaction amnesia recovery and Windows file-locking survival guide.
- [x] `skills/delegation/SKILL.md` overhauled as a high-density (<150 lines) operational contract:
  - Dominant Negative Gates ("When NOT to use").
  - Tri-modal Operational Triage Router.
  - The 5 Floor Invariants (Zero Context Bleed, Disjoint Write Ownership, Two-Track Evidence Gate, Fix Loop Escalation, Circuit Breaker Rulings).
  - Progressive disclosure router to `resources/`.
  - Runnable offline deterministic probe (`andino-operational-example`).
- [x] `references/legal/provenance.md` updated with comprehensive audit trail and MIT attributions for Matt Pocock and Jesse Vincent.
- [x] `references/internal-method-index.md`, `references/capability-registry.md`, and `README.md` verified and aligned.
- [x] Deterministic Python verification script `scripts/verify_delegation_elevation.py` passing (<0.25s runtime).
- [x] Upgraded skill synchronized directly to local host directory `~/.claude/skills/andino-workflow/skills/delegation/`.
- [x] Verified compatible with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
- [x] Git committed and pushed to `origin/andino-workflow`.

## Scope

### In Scope
- `skills/delegation/SKILL.md`
- `skills/delegation/GUIDE.md`
- `skills/delegation/resources/frontier-and-dag-protocols.md`
- `skills/delegation/resources/subagent-brief-and-report-schemas.md`
- `skills/delegation/resources/two-track-review-and-fix-loop.md`
- `skills/delegation/resources/workspace-and-isolation-guards.md`
- `skills/delegation/resources/worked-example.md`
- `skills/delegation/scripts/delegation_workspace.py` & `delegation-workspace`
- `skills/delegation/scripts/task_brief.py` & `task-brief`
- `skills/delegation/scripts/review_package.py` & `review-package`
- `scripts/verify_delegation_elevation.py`
- `references/legal/provenance.md`
- Local host synchronization to `~/.claude/skills/andino-workflow/skills/delegation/`
- Verification with `ai-rules setup`

### Out of Scope
- Modifying unrelated Andino skills.
- Introducing third-party npm or pip dependencies.
- Modifying project application code outside AI-RULES control plane and skills.

## User Decisions / Clarifications

- **Workspace Isolation Mode**: Dual-Mode approved. Uses Git Worktree when host/platform supports cleanly; falls back to in-tree `.andino/delegation/<plan-id>/` directory workspace with auto-generated `.gitignore` when worktree is unsupported or blocked by Windows file locks.
- **Helper Scripts Runtime**: Dual-Runtime approved. Python 3 standard library (`scripts/*.py`) for universal cross-platform execution (Windows PowerShell / cmd / POSIX) with lightweight shell wrappers (`scripts/*`).
- **Branch Strategy**: Local working branch/trunk default approved. Retains single-branch atomic progression with compaction-proof ledger checkpoints; integration branch / draft PR is an explicit opt-in setting.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Mechanical Invariants Over Prose**: Textual rules erode across LLM turns. Binary gates (Zero Context Bleed, Disjoint Write Ownership, Two-Track Review, Circuit Breaker Rule of 5) ensure structural execution integrity.
- **Tri-Modal Elastic Architecture**: Inline (fast, small, coupled) -> Parallel Dispatch (single-turn multi-dispatch for independent domains) -> Subagent-Driven (fresh subagent + two-track review loop for multi-task plans).
- **Separation of Concerns**: High-density operational contract `SKILL.md` (<150 lines) drives live execution; deep craft and exhaustive schemas live in `GUIDE.md` and `resources/`.
- **Zero-Dependency Cross-Platform Portability**: Python stdlib + POSIX built-ins only; universal path handling (`pathlib.Path`) and CRLF/LF line normalization for Windows/Linux/macOS.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **Reviewer Churn vs Spec Rigor (Contrarian vs First Principles)**:
   - *Risk*: Isolated reviewers falling into stylistic nitpicking or spec pedantry, generating infinite fix loops that burn rate limits.
   - *Resolution*: Review rubric strictly separates Spec Compliance (must fix) from Code Quality. Minor findings are immediately deferred to ledger (`Task <N>: minor (deferred): ...`) and NEVER enter the fix loop. Only Critical/Important spec gaps or structural flaws trigger fix rounds.
2. **Windows File Locks & Collision (Contrarian & Outsider vs Expansionist)**:
   - *Risk*: Rapid worktree creation/destruction, branch hopping, or concurrent git operations hitting Windows `index.lock` / `EBUSY`.
   - *Resolution*: Dual-mode workspace isolation. If Git Worktree encounters lock or is disabled, system gracefully falls back to in-tree workspace `.andino/delegation/<plan-id>/`. Helper scripts incorporate 3-tier exponential backoff retry on file handle operations.
3. **Compaction Amnesia (Contrarian & First Principles)**:
   - *Risk*: Claude Code auto-compaction wiping the active DAG frontier, task statuses, or dispatch state, causing parent agent to re-dispatch completed tasks or overwrite commits.
   - *Resolution*: Append-only durable progress ledger (`progress.md`) on disk. Ledger records every state transition, commit range, and ruling. Controllers always read disk state over conversation memory.
4. **Model Tier Escalation Discipline (Expansionist & Contrarian)**:
   - *Risk*: Always dispatching top-tier expensive models for simple mechanical diffs or trivial fixes.
   - *Resolution*: Adaptive Model & Effort Tiering rubric. Mechanical tasks use fast/cheap models; standard models for integration; escalation to top-tier only for fix loop rounds 4-5 and the final whole-branch review.

### Hal Terlewat (Blind Spots Addressed)
- **Worker Subagent Recursion Trap**: Implementers or reviewers attempting to spawn their own subagents, doubling token spend. Prompts strictly forbid subagent creation.
- **Untrusted Subagent Testimony**: Parent controller must never accept verbal "I tested it and it works" claims. Concrete diff (`review-package`) and verifiable test output are mandatory preconditions for marking any task complete.
- **Fail-Safe Eject**: When Circuit Breaker (Rule of 5) trips, the controller records `Ruling: ...` in the ledger, releases all locks, and emits a single clean git command for human review.

### Rekomendasi (Recommendation)
Implement the complete 5-phase elevation plan, execute zero-dependency offline Python verification, synchronize locally to host skills, verify via `ai-rules setup`, and commit/push to `origin/andino-workflow`.

### Langkah Pertama (First Action)
Author `skills/delegation/resources/frontier-and-dag-protocols.md`.

---

## Task Breakdown & Change Specifications

### Phase 1: Progressive Disclosure Resources & Protocols

#### Task 1: Create `skills/delegation/resources/frontier-and-dag-protocols.md`
- **File**: `skills/delegation/resources/frontier-and-dag-protocols.md`
- **Spec**:
  - DAG task graph modeling, dependency validation, active frontier resolution.
  - Lexical path collision detection (exact match, parent/child ancestor path collision).
  - Tri-modal selection decision matrix (Inline vs Parallel vs Subagent-Driven).
  - Concurrency caps (max 3 active direct workers, wave scheduling).

#### Task 2: Create `skills/delegation/resources/subagent-brief-and-report-schemas.md`
- **File**: `skills/delegation/resources/subagent-brief-and-report-schemas.md`
- **Spec**:
  - Pure pointer-based brief format (Task ID, Spec anchor, owned file paths, contract interfaces, test command, report path).
  - Strict boundary rules (no nested agents, no unapproved mutations).
  - Standardized short-status contract (<15 lines terminal output: Status, commits, 1-line test summary, concerns, report path).

#### Task 3: Create `skills/delegation/resources/two-track-review-and-fix-loop.md`
- **File**: `skills/delegation/resources/two-track-review-and-fix-loop.md`
- **Spec**:
  - Two-Track Review Gates: Track 1 (Spec Compliance: ✅/❌/⚠️) vs Track 2 (Code Quality: Approved / Needs fixes).
  - Scoped diff packaging (`review-package`) methodology.
  - 5-Round Fix Loop: Rounds 1-3 resume implementer; Rounds 4-5 fresh implementer with model tier escalation.
  - Rule of 5 Circuit Breaker and `Ruling: <decision> — <reason> — <cost if wrong>` taxonomy.

#### Task 4: Create `skills/delegation/resources/workspace-and-isolation-guards.md`
- **File**: `skills/delegation/resources/workspace-and-isolation-guards.md`
- **Spec**:
  - Dual-mode workspace isolation (Git Worktree vs In-Tree `.andino/delegation/<plan-id>/`).
  - Windows file-locking mitigation (`EBUSY`, `index.lock`, retry backoff).
  - Compaction-resistant append-only ledger (`progress.md`) specification.
  - Workspace teardown and safe cleanup.

#### Task 5: Create `skills/delegation/resources/worked-example.md`
- **File**: `skills/delegation/resources/worked-example.md`
- **Spec**:
  - End-to-end case study: Auth Token Service decomposition into 3 independent modules (Token Signer, Refresh Token Store, Auth Middleware).
  - Complete execution walkthrough: Frontier calculation -> Parallel dispatch -> Two-track review -> Fix loop & ruling -> Integration.
  - Embedded zero-dependency Python stdlib operational test suite verifying the complete contract offline (<0.2s runtime).

### Phase 2: Dual-Runtime Cross-Platform Helper Scripts

#### Task 6: Author Helper Scripts in `skills/delegation/scripts/`
- **Files**:
  - `skills/delegation/scripts/delegation_workspace.py` & `delegation-workspace`
  - `skills/delegation/scripts/task_brief.py` & `task-brief`
  - `skills/delegation/scripts/review_package.py` & `review-package`
- **Spec**:
  - Python 3 standard library implementation with zero external dependencies.
  - Universal path handling (`pathlib.Path`), Windows/POSIX compatibility.
  - Lightweight POSIX shell wrappers delegating to Python or bash built-ins.

### Phase 3: Core Operational Contract & Deep Craft Guide

#### Task 7: Overhaul `skills/delegation/GUIDE.md`
- **File**: `skills/delegation/GUIDE.md`
- **Spec**:
  - Comprehensive craft guide synthesizing Pocock, Vincent (Obra), and Andino Workflow.
  - Deep chapters on Tri-Modal FSM, Adaptive Model Selection, Two-Track Review Calibration, Circuit Breaker Protocols, and Compaction Survival.
  - Anti-rationalization table and 8 AI evasion move counters.

#### Task 8: Overhaul `skills/delegation/SKILL.md`
- **File**: `skills/delegation/SKILL.md`
- **Spec**:
  - High-density operational contract (<150 lines).
  - Dominant Negative Gates ("When NOT to use").
  - Tri-modal Operational Triage Router.
  - The 5 Floor Invariants.
  - Anti-Rationalization Refutations Table.
  - 8 Diagnostic Red Flags.
  - Progressive Disclosure Router to `resources/`.
  - Runnable offline deterministic probe (`andino-operational-example`).

### Phase 4: References, Index & Legal Provenance

#### Task 9: Update References, Index & Catalog
- **Files**:
  - `references/internal-method-index.md`
  - `references/capability-registry.md`
  - `README.md`
- **Spec**: Verify descriptions and aliases for `delegation`, ensuring alignment with elevated capabilities.

#### Task 10: Update `references/legal/provenance.md`
- **File**: `references/legal/provenance.md`
- **Spec**: Add comprehensive 2026-11-01 elevation record for `delegation`, detailing synthesis of Matt Pocock and Jesse Vincent under Andino Workflow governance.

### Phase 5: Verification, Host Sync & Delivery

#### Task 11: Create & Execute Deterministic Offline Verification Script
- **File**: `scripts/verify_delegation_elevation.py`
- **Spec**: Python script validating file existence, line counts (<150 lines), mandatory sections, operational example (normal & adversarial), helper scripts, and catalog integrity (<0.2s runtime).

#### Task 12: Local Host Synchronization
- **Directories**: `~/.claude/skills/andino-workflow/skills/delegation/`
- **Spec**: Copy all elevated skill files, resources, and scripts to local host directory.

#### Task 13: `ai-rules setup` Dry-Run, Commit & Push
- **Spec**:
  - Run `rtk ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
  - Git commit with descriptive conventional commit message.
  - Push to `origin/andino-workflow`.

---

## Next Action
Completed all tasks. Ready for final commit and push.
