# Andino Phase-Readiness Routing & Reliability Repair Report

Date: 2026-10-19  
Repository: https://github.com/andinoferdi/AI-RULES  
Candidate Ref: `andino-workflow` (`f99ec59c95f1889b08fa6d873dba1522a41608ea`)  
Runtime Base: `634585a45866261e0d981a68098fa7f1b4bf4c0e`  
Runtime Content SHA256: `50c24252afaf7ecc0564f1b089d5999ba0c3d1b83510929bf64954902d2e671d`  
Status: `LOCAL_CANDIDATE_UNPUBLISHED`  
Readiness State: `CONDITIONALLY_READY`

---

## A. Root Causes

### Confirmed Causes
1. **Missing Phase-Readiness Precedence in Routing Table (`references/routing.md`):**
   The pre-repair routing contract followed a flat precedence model: `Explicit choices/exclusions -> REQUIRED routes -> CONDITIONAL routes`. The UI design specialist routes (`design-taste-frontend` and `impeccable`) were marked as `REQUIRED` unconditionally whenever a visual or UI context was mentioned.
2. **Premature Specialist Route Triggering on Mixed Intent:**
   When given a prompt combining an execution verb and direction uncertainty (such as *"buatkan saya web crud, tapi saya bingung gimana"*), the mention of "web" or "crud" triggered the `REQUIRED` UI design route immediately. The agent activated `impeccable` or `design-taste-frontend` and began scaffold generation before establishing whether a valid product concept existed.
3. **Exploratory Methods Subordinated as Conditional:**
   Exploratory methods (`brainstorming`, `decision-interview`) were classified under `CONDITIONAL` rows, leaving them subservient to any matching `REQUIRED` capability route.
4. **Over-Aggressive Interpretation of Autonomous Directives in `SKILL.md`:**
   The directive *"Investigate before asking"* and *"explicit invocation does not force engineering questions"* were interpreted as an instruction to proceed immediately to implementation when given an execution verb ("buatkan"), bypassing the need to explore user-owned direction.

### Hypotheses Evaluated & Rejected
- **H2 (Internal Method Guide Defect):** REJECTED. The bundled guides (`brainstorming/GUIDE.md`, `decision-interview/GUIDE.md`) were functionally sound and correct. The failure was strictly orchestration routing and precedence gating.
- **H6 (Discovery Without Activation):** REJECTED as sole cause. Traces showed agents accurately discovered available routes, but the lack of phase readiness forced selection of the wrong phase.
- **H7 (Host-Specific Invocation Defect):** REJECTED. The premature implementation behavior was reproduced across multiple host environments (Claude Code and Antigravity CLI) under baseline conditions.

---

## B. Changes Made

### 1. Runtime Package (`andino-workflow` branch @ `f99ec59`)
- **`references/routing.md`**:
  - Added the **Phase readiness** contract establishing explicit precedence: `Explicit user choices/exclusions -> Phase readiness -> REQUIRED routes whose phase is current -> CONDITIONAL routes`.
  - Added classification rules distinguishing:
    - *Open product direction (undelegated):* REQUIRED `brainstorming`.
    - *Known direction with open material requirements:* Inspect evidence, then REQUIRED `decision-interview`.
    - *Rough idea needing sharpening:* `idea-refine`.
    - *Technical confusion about running/understanding existing work:* Direct guidance (`learning-workspace`, `human-procedure`, or `plain-language-repitch`), never ideation.
    - *Specified or delegated execution:* Proceed with reasonable defaults and implementation methods.
    - *Accepted work:* Preserve decisions; never reopen completed discovery.
  - Gated UI design routes (`design-taste-frontend`, `impeccable`): Added condition *"after product direction is resolved or delegated"*.
- **`SKILL.md`**:
  - Clarified that *"Investigate before asking"* applies to discoverable facts, not user-owned direction.
  - Linked root instruction directly to phase-readiness gating before design or implementation.
  - Qualified that explicit invocation does not force questions for settled work, but does not override phase readiness when direction is open.
- **`references/internal-method-index.md`**:
  - Updated `brainstorming` and `decision-interview` entries to explicitly address mixed execution plus uncertainty requests and exclude technical confusion.

### 2. Evaluation Harness & Test Infrastructure (`main` branch @ `31c5f4f`)
- **`evals/andino-workflow.json`**: Added 16 new semantic evaluation scenarios (bringing total to 82), including the raw Indonesian CRUD prompt (`crud-uncertain-id`).
- **`scripts/run_andino_capability_eval.py` & `scripts/validate_andino_capabilities.py`**:
  - Added dual evaluation modes: `read-only` and `isolated-writable`.
  - Implemented multi-host execution adapters for Claude Code, Codex, OpenCode, and Antigravity CLI.
  - Added workspace containment checks (sentinel file verification) and skill provenance validation (`CANDIDATE_ONLY` vs global leakage).
  - Maintained schema stability using `NOT_VERIFIED` with typed reasons (`HOST_UNAVAILABLE`, `CONTAINMENT_UNVERIFIED`, `INCONCLUSIVE_BEHAVIOR`).
- **`tests/test_andino_eval_modes.py` & `tests/test_andino_readiness_cases.py`**: Validated mode contracts, oracle hiding, and scenario metadata.
- **`tests/test_andino_routing_readiness.py`**: Contract tests proving phase-readiness enforcement (RED on baseline 634585a with 6/8 failures, GREEN on candidate f99ec59 with 8/8 passes).

---

## C. Routing Behavior

- **User Uncertainty:** Contextual signals determine the opened methodology. Undelegated product ambiguity requires `brainstorming` to offer distinct directions with trade-offs. Material user choices in an existing project require evidence inspection followed by `decision-interview`. Confusion about running existing code routes to direct technical guidance without ideation.
- **Explicit Execution:** When scope is specified or delegated (*"bebas pilih stack, langsung kerjakan"*), the agent proceeds directly with stated defaults and implementation methods without unwanted interview cycles.
- **Internal Method Selection:** Bundled methods in `skills/<method>/GUIDE.md` are canonical. They must be resolved, read, and meaningfully executed before dependent output is generated.
- **Supporting Specialist Activation:** `design-taste-frontend` and `impeccable` activate only after product direction is settled or delegated. They no longer preempt exploration.
- **Tool Selection:** Focus remains the mandatory default communication skill across all invocations. Search First activates only upon actual external technical or dependency uncertainty.
- **Phase Transitions:** The workflow enforces discovery -> requirements -> planning/design -> implementation (TDD) -> verification.
- **Verification and Completion:** The verification guide must be read before claiming completion, and claims must cite actual execution evidence.

---

## D. Regression Results

### Contract & Unit Tests
- `tests/test_andino_routing_readiness.py`: **8 / 8 PASS** on candidate `f99ec59` (6 of 8 failed on baseline `634585a`).
- `tests/test_andino_readiness_cases.py` & `tests/test_andino_eval_modes.py`: **PASS**.
- Full test suite: **82 / 82** `test_andino*.py` unit tests pass; all installer test suites pass.

### Repository Validators
- `validate_skills.py --andino-ref andino-workflow`: **PASS** (7 skill packages, Focus references intact).
- `validate_threejs_family.py --runtime-ref origin/threejs-skills`: **PASS** (45 methods, 714 resources).
- `validate_andino_capabilities.py --runtime-ref andino-workflow`: **PASS** (74 eval schemas, 60 capability contracts; runtime SHA256 matches candidate `50c2425...`).
- `validate_skripsi_traceability.py`: **PASS** (335 requirements, 32 capabilities, 110 eval owners).
- `validate_andino_unified.py`: **PASS** (structural audit: 79 rows, 58 destinations, 0 collisions).

### Primary Regression Scenario (`crud-uncertain-id`)
- **Prompt:** `"gunakan andino-workflow dan metode metode yang ada, disini tolong buatkan saya web crud, tapi saya bingung gimana"`
- **Baseline Behavior:** Agent activated Focus and Impeccable, skipped `brainstorming/GUIDE.md`, generated CRUD files immediately (**FAIL**).
- **Candidate Behavior (`after-fix`):** Agent read `brainstorming/GUIDE.md`, presented 3 distinct conceptual options with trade-offs, deferred implementation until user decision, generated no files, and invoked no premature UI design skills (**PASS** on Claude Code and Antigravity CLI).

---

## E. Cross-Host Results

| Host | Availability | Actual Test Performed | Result | Evidence |
|---|---|---|---|---|
| **Claude Code** (v2.1.300) | Available | Live core & extended readiness matrix (28 runs) | **PASS** (15), **FAIL** (1), **NOT_VERIFIED** (12) | Inside writes confirmed, sentinel intact; 12 NOT_VERIFIED due to session quota limits; 1 FAIL on `unknown-bug-id` order. |
| **Codex** (v0.154.0) | Available (Restricted) | Live core readiness matrix in routing-only mode (9 runs) | **PASS** (4), **NOT_VERIFIED** (5) | Workspace containment probe failed (outside write); writable cases ran routing-only; global AGENTS.md policy caused partial blocks. |
| **Antigravity CLI** | Available | Live core readiness matrix in routing-only mode (7 runs) | **PASS** (4), **FAIL** (2), **NOT_VERIFIED** (1) | Primary CRUD prompt passed; 2 FAILs on headless edge cases (added brainstorming to interview / premature docs claim). |
| **OpenCode** (v2.0.29) | Unavailable | Smoke test attempt | **NOT_VERIFIED** | Server credential migration error (`Legacy credential file must contain an object`); no config altered. |
| **Antigravity IDE** | Unavailable | N/A | **NOT_VERIFIED** | No automated testing interface available; CLI results do not imply IDE parity. |

---

## F. Remaining Issues

1. **Host-Level Containment on Codex:** Codex OS sandbox failed containment probe on Windows (outside sentinel write was permitted while inside write was blocked). Evaluator correctly downgraded writable cases to routing-only.
2. **OpenCode Local Credential State:** OpenCode CLI is currently in an unmigrated state on this machine. Global credentials were not touched per safety constraints.
3. **Claude Code Session Quota:** Extended test repetitions in `after-fix/` were halted when Claude Code session limits were reached. Completed baseline/after-fix runs remain preserved.
4. **Antigravity CLI Headless Heuristics:** In isolated headless mode, Antigravity CLI occasionally over-generates planning artifacts on requirement-interview cases.
5. **Lineage Pre-Existing Mismatch:** Historical lineage hashes in `publication-lineage.json` and `capability-runtime-lineage.json` reflect a pre-existing divergence from `634585a`; left as found per non-publication directive.

---

## G. Final State

**`CONDITIONALLY_READY`**

The phase-readiness routing repair successfully eliminates the reported defect: ambiguous requests no longer bypass exploration or prematurely trigger design/implementation specialist skills. The contract is proven RED->GREEN on unit tests and verified via multi-host behavioral traces. Because production release manifests and publication lineage remain locked to published refs and several hosts have environment-level boundaries (quota limits, containment limits, or credential migrations), the candidate is classified as `LOCAL_CANDIDATE_UNPUBLISHED` and `CONDITIONALLY_READY` for local repository use.
