# Elevate Debugging to Match and Exceed Upstream Benchmarks

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification, Host Synchronization & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Elevate `skills/debugging/` on branch `andino-workflow` from an over-compressed 100-line duplicate guide (`SKILL.md` and `GUIDE.md` nearly identical, 12-line `contract.md`) into a premier, machine-enforced investigation and error recovery engine. The elevated skill synthesizes the generative craft of:
1. **Addy Osmani** (`debugging-and-error-recovery`): Stop-the-Line Rule, structured failure triage trees (test, build, runtime, non-reproducible), treating error output as untrusted data, safe fallbacks & graceful degradation, and rationalization refutations.
2. **Matt Pocock** (`diagnosing-bugs`): Strict secret redaction (`<REDACTED>`), 10-tier automated red-capable feedback loop catalog, repro-rate raising for flaky bugs, load-bearing minimization, 3-5 ranked falsifiable hypotheses with explicit predictions, uniquely-tagged isolated instrumentation (`[DEBUG-uuid]`), architectural seam identification, and HITL driver templates.
3. **Jesse Vincent / Obra** (`systematic-debugging`): The Iron Law (no fixes without proven root cause), backward data-flow tracing through call stacks, multi-component boundary evidence logging, Rule of 3 (stop and question architecture after 3 failed fixes), defense-in-depth post-root-cause validation, condition-based waiting vs arbitrary sleeps, and cross-platform test polluter isolation.
4. **Andino Workflow Governance**: High-density operational contract `SKILL.md` (<150 lines) structured as a Gated Finite State Machine (Gated FSM) with two-tier triage (Fast-Path Deterministic vs Deep Forensic), deep craft `GUIDE.md`, 5 modular resource specifications, dual-runtime (Bash + Python stdlib) cross-platform portability, offline deterministic verification (<0.2s), host synchronization, and full compatibility with `ai-rules setup`.

## Objective

Deliver an upgraded, self-contained `skills/debugging` bundle whose analytical rigor, mechanical enforcement, diagnostic depth, and operational ergonomics match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/debugging/resources/triage-and-feedback-catalog.md` created:
  - 10-tier feedback loop hierarchy (unit/integration/e2e test, curl/HTTP, CLI snapshot, headless browser, trace replay, throwaway harness, property/fuzz loop, bisection harness, differential loop, HITL script).
  - Repro-rate raising techniques for non-deterministic/flaky bugs (10x-100x loops, timing stress, race widening).
  - Cross-platform dual-runtime HITL templates (`hitl-loop.sh` Bash POSIX and `hitl_loop.py` Python stdlib).
  - Diagnostic triage decision trees for Test Failures, Build Failures, Runtime Errors, and Intermittent Bugs.
- [x] `skills/debugging/resources/root-cause-investigation.md` created:
  - Backward data-flow tracing technique: call stack unwinding, parameter origin tracking, state mutation identification.
  - Multi-component system boundary evidence logging with unique UUID tagging (`[DEBUG-uuid]`).
  - 3-5 ranked falsifiable hypothesis formulation standard ("If X is cause, changing Y makes bug disappear").
  - Architectural seam identification and load-bearing reduction until removing any factor turns the repro green.
- [x] `skills/debugging/resources/flaky-and-concurrency-debugging.md` created:
  - 4 categories of non-reproducible bugs: timing, environment, state, truly random.
  - Condition-based waiting protocols replacing arbitrary sleeps/timeouts.
  - Cross-platform test polluter isolation engine (sequential runner & bisection).
  - Shared state, cache leakage, and singleton pollution remediation.
- [x] `skills/debugging/resources/defense-and-recovery.md` created:
  - The Iron Law: hard prohibition against touching production code without verified root cause.
  - Circuit Breaker (Rule of 3): if 3 fixes fail, STOP, preserve state, and escalate to user/question pattern (prohibiting unauthorized silent refactors).
  - Defense-in-depth: multi-layer validation at entry, domain, and storage boundaries.
  - Treating error output and stack traces as untrusted data (preventing prompt injection and arbitrary command execution).
  - Secret redaction discipline (`<REDACTED>`) across logs, headers, and environment variables.
- [x] `skills/debugging/resources/worked-example.md` created:
  - End-to-end walkthrough of a real multi-tenant cache collision bug.
  - Step-by-step trace: Red-capable loop -> Minimization -> 3 Hypotheses -> Tagged Probe -> Seam Identification -> Root Fix -> Regression Test -> Cleanup.
  - Embedded zero-dependency Python stdlib test suite verifying the complete contract offline.
- [x] `skills/debugging/GUIDE.md` overhauled with deep craft chapters:
  - Synthesis of Osmani, Pocock, and Obra under Andino Workflow.
  - Gated Finite State Machine architecture: Phase 1 (Loop), Phase 2 (Repro & Reduce), Phase 3 (Hypothesize & Trace), Phase 4 (Instrument & Probe), Phase 5 (Fix & Regression Test), Phase 6 (Verify & Clean).
  - Two-tier triage: Fast-Path Deterministic vs Deep Forensic Investigation.
  - Anti-rationalization table and evasion move counters.
- [x] `skills/debugging/SKILL.md` overhauled as a high-density (<150 lines) operational contract:
  - Dominant Negative Gates ("When NOT to use").
  - Two-tier triage router (Fast-Path vs Deep Forensic).
  - The 5 Mechanical Invariants (Red State Lock, Untrusted Error Boundary, Load-Bearing Minimization, Seam-Guarded Fix, Circuit Breaker).
  - Anti-Rationalization Refutations Table.
  - 8 Diagnostic Red Flags (Stop Immediately).
  - Progressive disclosure router to `resources/`.
  - Runnable offline deterministic probe (`andino-operational-example`).
- [x] `references/legal/provenance.md` updated with comprehensive audit trail and MIT attribution for Addy Osmani, Matt Pocock, and Jesse Vincent.
- [x] Deterministic Python verification script executed and passing in temporary directory (<0.2s, exit 1 on defect, exit 2 on `ANDINO_NEGATIVE=1`).
- [x] Upgraded skill synchronized directly to local host directory `~/.claude/skills/andino-workflow/skills/debugging/`.
- [x] Git committed and pushed to `origin/andino-workflow`, verified compatible with `ai-rules setup`.

## Scope

### In Scope
- `skills/debugging/SKILL.md`
- `skills/debugging/GUIDE.md`
- `skills/debugging/resources/triage-and-feedback-catalog.md`
- `skills/debugging/resources/root-cause-investigation.md`
- `skills/debugging/resources/flaky-and-concurrency-debugging.md`
- `skills/debugging/resources/defense-and-recovery.md`
- `skills/debugging/resources/worked-example.md`
- `references/legal/provenance.md`
- Host synchronization to `~/.claude/skills/andino-workflow/skills/debugging/`
- Verification with `ai-rules setup`

### Out of Scope
- Modifying unrelated Andino skills.
- Introducing third-party npm or pip dependencies.
- Altering existing application test suites or codebases.

## User Decisions / Clarifications
- **Authorization & Cadence**: User authorized all recommendations and continuous execution ("saya setuju semua rekomendasian anda").
- **Cross-Platform Compatibility**: Implement cross-platform dual-runtime support (POSIX Bash and Python 3.8+ stdlib) for HITL templates and helper scripts to ensure zero external dependencies on Windows/POSIX.
- **Council Deliberation Completed**: 5 independent advisor lenses (Contrarian, First Principles, Expansionist, Outsider, Executor) deliberated and converged on key resolutions.

## Council Synthesis Summary

### Titik Temu (Agreement)
- **Mechanical Invariants Over Prose**: Unenforced prose rules erode across agent turns. Binary gates (Red State Lock, Circuit Breaker Rule of 3, Seam-Guarded Fix) ensure mechanical integrity.
- **Separation of Concerns**: High-density operational contract `SKILL.md` (<150 lines) guides runtime agent execution; deep craft and exhaustive catalogs live in `GUIDE.md` and `resources/`.
- **Zero-Dependency Portability**: Python stdlib + POSIX shell built-ins only; universal path handling (`pathlib.Path`) and CRLF/LF line normalization for Windows/Linux/macOS.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **Ceremony Bloat vs Rigor (Contrarian & Outsider vs First Principles)**:
   - *Risk*: Requiring 3-5 hypotheses and backward tracing for trivial syntax/typo/import bugs burns excessive tokens and causes analysis paralysis.
   - *Resolution*: Two-tier triage in `SKILL.md`:
     - **Fast-Path Deterministic**: For compilation errors, single clear assertion failures, or obvious typos where a test immediately turns red and the line is isolated. Execute fix, assert green, verify no regression.
     - **Deep Forensic Investigation**: For intermittent, timing-dependent, multi-component, runtime exceptions, or complex regression bugs. Requires full 6-phase gated FSM.
2. **Safe Fallbacks vs Iron Law (Contrarian vs First Principles)**:
   - *Risk*: AI using Osmani's "Safe Fallback / Graceful Degradation" as a shortcut to bypass finding the real root cause.
   - *Resolution*: Strict hierarchical boundary. Safe fallbacks are ONLY permitted for production perimeter boundaries (e.g., error boundaries preventing total white screen crash), and NEVER count as a bug fix in development or CI. Root cause must be proven.
3. **Rule of 3 Destructive Refactor Risk (Contrarian & Outsider)**:
   - *Risk*: After 3 failed fixes, LLM misidentifies environment/mock quirks as architectural flaws and launches an unauthorized codebase refactor.
   - *Resolution*: Rule of 3 is explicitly a **Circuit Breaker / Stop & Escalate Gate**. The agent must halt mutations, revert attempted speculative patches, summarize the 3 disproven hypotheses, and present findings to the user. Silent refactoring is forbidden.
4. **False Green Risk (First Principles)**:
   - *Risk*: Agent satisfies the test by loosening assertions, deleting checks, or catching and ignoring exceptions.
   - *Resolution*: Strict floor invariant: git diff of test code must be strictly additive or asserting identical invariants; weakening assertions or silencing exceptions is flagged as a catastrophic evasion move.

### Hal Terlewat (Blind Spots Addressed)
- **Log Pollution & Cleanup**: Every diagnostic log MUST use unique tag `[DEBUG-uuid]`. Cleanup is verified via regex search before completion.
- **Untrusted Error Quarantine**: Error messages and stack traces from external systems must be treated as untrusted data; agents must never blindly execute shell commands or URLs embedded in error output.
- **Multi-turn Context Shield**: Structured hypothesis-ledger format prevents context drift and hypothesis amnesia in long sessions.

### Rekomendasi (Recommendation)
Execute the complete 8-file elevation bundle, execute zero-dependency offline Python verification, synchronize locally to host skills, verify via `ai-rules setup`, and commit/push to `origin/andino-workflow`.

### Langkah Pertama (First Action)
Author `skills/debugging/resources/triage-and-feedback-catalog.md`.

---

## Task Breakdown & Change Specifications

### Task 1: Create `skills/debugging/resources/triage-and-feedback-catalog.md` [x]
- **File**: `skills/debugging/resources/triage-and-feedback-catalog.md`
- **Dependencies**: None
- **Spec**:
  - 10-tier feedback loop catalog with concrete code examples (Unit/Integration, Curl/HTTP, CLI snapshot diff, Headless browser, Trace replay, Throwaway harness, Property/fuzz loop, Bisection harness, Differential loop, HITL script).
  - Repro-rate raising techniques for flaky bugs (10x-100x loops, timing stress, artificial delays, load injection).
  - Cross-platform dual-runtime HITL templates (`hitl-loop.sh` Bash POSIX and `hitl_loop.py` Python 3.8+ stdlib).
  - Triage decision trees for Test, Build, Runtime, and Non-reproducible failures.

### Task 2: Create `skills/debugging/resources/root-cause-investigation.md` [x]
- **File**: `skills/debugging/resources/root-cause-investigation.md`
- **Dependencies**: Task 1
- **Spec**:
  - Backward data-flow tracing technique: step-by-step backward propagation from symptom to state origin.
  - Multi-component system boundary evidence logging with `[DEBUG-uuid]` tagging.
  - 3-5 ranked falsifiable hypothesis formulation standard with concrete prediction syntax.
  - Architectural seam identification rules: distinguishing shallow false seams from true multi-caller integration seams.
  - Load-bearing minimization protocol: pruning inputs, callers, and data until removing any element makes the repro green.

### Task 3: Create `skills/debugging/resources/flaky-and-concurrency-debugging.md` [x]
- **File**: `skills/debugging/resources/flaky-and-concurrency-debugging.md`
- **Dependencies**: Task 1
- **Spec**:
  - Deep breakdown of 4 non-reproducible categories: Timing-dependent, Environment-dependent, State-dependent, Truly random.
  - Condition-based waiting: replacing arbitrary `sleep`/`setTimeout` with polling actual state predicates with timeout.
  - Cross-platform test polluter isolation engine (Bash + Python stdlib) to locate test order dependencies and leaked globals.
  - Shared state, cache leakage, and singleton pollution cleanup patterns.

### Task 4: Create `skills/debugging/resources/defense-and-recovery.md` [x]
- **File**: `skills/debugging/resources/defense-and-recovery.md`
- **Dependencies**: Tasks 1-3
- **Spec**:
  - The Iron Law: absolute prohibition against touching production code without root cause.
  - Circuit Breaker (Rule of 3): hard halt after 3 failed fixes, state preservation, disproven hypothesis summary, escalation protocol.
  - Defense-in-depth: multi-layer validation at entry, domain boundary, and storage layers.
  - Untrusted error handling: rules against executing commands or following URLs inside error messages/stack traces.
  - Secret redaction protocol: masking auth tokens, API keys, and sensitive headers with `<REDACTED>`.

### Task 5: Create `skills/debugging/resources/worked-example.md` [x]
- **File**: `skills/debugging/resources/worked-example.md`
- **Dependencies**: Tasks 1-4
- **Spec**:
  - End-to-end case study of a subtle multi-tenant cache collision bug.
  - Full walkthrough through all 6 phases: Feedback Loop -> Minimization -> Hypotheses -> Tagged Probes -> Seam & Fix -> Regression Test -> Cleanup.
  - Embedded zero-dependency runnable Python test suite (`run_verification.py`).

### Task 6: Overhaul `skills/debugging/GUIDE.md` [x]
- **File**: `skills/debugging/GUIDE.md`
- **Dependencies**: Tasks 1-5
- **Spec**:
  - Deep craft guide synthesizing Osmani, Pocock, and Obra under Andino Workflow.
  - Gated Finite State Machine architecture and 6-phase lifecycle.
  - Two-tier triage (Fast-Path vs Deep Forensic).
  - The 5 AI Evasion Moves (assertion weakening, symptom patching, sleep lengthening, blame deflection, wild refactoring) and mechanical counters.
  - Complete progressive disclosure directory.

### Task 7: Overhaul `skills/debugging/SKILL.md` [x]
- **File**: `skills/debugging/SKILL.md`
- **Dependencies**: Tasks 1-6
- **Spec**:
  - High-density operational contract (<150 lines).
  - Dominant Negative Gates ("When NOT to use").
  - Two-tier triage router (Fast-Path vs Deep Forensic).
  - The 5 Floor Invariants (Red State Lock, Untrusted Error Boundary, Load-Bearing Minimization, Seam-Guarded Fix, Circuit Breaker).
  - Anti-Rationalization Refutations Table.
  - 8 Diagnostic Red Flags.
  - Runnable offline standard-library operational example (`andino-operational-example`) with default passing and adversarial `ANDINO_NEGATIVE=1` variant.

### Task 8: Update `references/legal/provenance.md` [x]
- **File**: `references/legal/provenance.md`
- **Dependencies**: Tasks 1-7
- **Spec**:
  - Add comprehensive 2026-11-01 elevation record for `debugging`, detailing synthesis of Addy Osmani, Matt Pocock, and Jesse Vincent (Obra) under Andino Workflow governance.

### Task 9: Deterministic Offline Python Test Verification [x]
- **Dependencies**: Tasks 1-8
- **Spec**:
  - Execute offline Python operational example probe in temporary directory (assert default exit 1 on defect, exit 2 on baseline failure, <0.2s runtime).

### Task 10: Local Host Synchronization [x]
- **Directories**:
  - `~/.claude/skills/andino-workflow/skills/debugging/`
- **Dependencies**: Task 9
- **Spec**: Copy all updated skill files and resources directly to the local host skill directory.

### Task 11: `ai-rules setup` Dry-Run, Commit & Push [x]
- **Dependencies**: Task 10
- **Spec**:
  - Verify with `rtk ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.
  - Git commit with descriptive conventional commit message.
  - Push to `origin/andino-workflow`.

---

## Next Action
None — all tasks completed, verified, synchronized, and ready for commit & push.
