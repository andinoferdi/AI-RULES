# Systematic Debugging and Error Recovery — Deep Craft Guide

Internal Andino resource. Operates under Andino Workflow governance.

---

## 1. Architectural Overview & Synthesis

This guide elevates the engineering discipline of debugging by synthesizing the proven craft of three industry authorities into a machine-enforceable, agent-runnable engine:

1. **Addy Osmani (`debugging-and-error-recovery`)**: The Stop-the-Line Rule, structured failure triage trees (test, build, runtime, non-reproducible), treating error output as untrusted data, safe fallbacks & graceful degradation, and rationalization refutations.
2. **Matt Pocock (`diagnosing-bugs`)**: Strict secret redaction (`<REDACTED>`), 10-tier automated red-capable feedback loop catalog, repro-rate raising for flaky bugs, load-bearing minimization, 3-5 ranked falsifiable hypotheses with explicit predictions, uniquely-tagged isolated instrumentation (`[DEBUG-uuid]`), architectural seam identification, and HITL driver templates.
3. **Jesse Vincent / Obra (`systematic-debugging`)**: The Iron Law (no fixes without proven root cause), backward data-flow tracing through call stacks, multi-component boundary evidence logging, Rule of 3 (stop and question architecture after 3 failed fixes), defense-in-depth post-root-cause validation, condition-based waiting vs arbitrary sleeps, and cross-platform test polluter isolation.

---

## 2. Two-Tier Operational Triage

To prevent ceremony bloat on straightforward bugs while guaranteeing rigorous forensic analysis on complex defects, apply two-tier triage:

```
Incident Intake:
├── TIER A: FAST-PATH DETERMINISTIC
│   ├── Criteria: Syntax error, missing import, single clear assertion typo, obvious compile error.
│   ├── Pre-condition: Error message points directly to an unambiguous single line/token.
│   └── Action: Apply fix, run focused test, assert green, run full build/suite check.
└── TIER B: DEEP FORENSIC INVESTIGATION
    ├── Criteria: Intermittent bugs, race conditions, multi-component boundary failures,
    │             logic regressions, wrong output without explicit crash, or >= 2 failed attempts.
    └── Action: Strict 6-Phase Gated Finite State Machine execution.
```

---

## 3. The 6-Phase Gated Finite State Machine (FSM)

When operating under Tier B, an agent MUST complete each phase and satisfy its **Mechanical Exit Condition** before advancing. Jumping ahead to hypothesize or mutate code is strictly forbidden.

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PHASE 1    │ ──▶ │   PHASE 2    │ ──▶ │   PHASE 3    │
│Feedback Loop │     │Reproduce &   │     │Hypothesize & │
│ (<5s, Red)   │     │   Minimise   │     │  Trace Flow  │
└──────────────┘     └──────────────┘     └──────────────┘
       ▲                                         │
       │ (Rollback on failed probe)              ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PHASE 6    │ ◀── │   PHASE 5    │ ◀── │   PHASE 4    │
│ Verify E2E & │     │ Fix at Seam  │     │ Instrument & │
│Clean Tagged  │     │ & Regress    │     │ Tagged Probe │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Phase 1: Build a Tight Feedback Loop
- **Objective**: Establish one single command (test invocation, CLI script, curl, or headless browser) that runs unattended in under 5 seconds and goes **RED** on the user's exact symptom.
- **Rules**:
  - Do not read implementation code to form theories before this command exists.
  - If the bug is flaky, raise the reproduction rate (run 100x loop, widen timing windows) until it fails predictably.
  - See `resources/triage-and-feedback-catalog.md` for the 10-tier loop hierarchy.
- **Mechanical Exit Condition**: A runnable command string that has been executed and demonstrated failing (exit $\ne 0$ or assertion error).

### Phase 2: Reproduce and Minimize
- **Objective**: Shrink the failure scenario to the smallest possible load-bearing state.
- **Rules**:
  - Cut inputs, config options, database rows, and calling steps one by one.
  - Re-run the Phase 1 loop after each cut.
  - If cutting a component keeps the test red, that component was noise; discard it.
  - If cutting it turns the test green, that component is load-bearing; keep it.
- **Mechanical Exit Condition**: Minimal reproducer where removing ANY remaining property makes the failure disappear.

### Phase 3: Hypothesize and Trace Data Flow
- **Objective**: Unwind the call stack backward from the failure point to find the true origin of state corruption, then formulate 3–5 falsifiable hypotheses.
- **Rules**:
  - Trace backward: who supplied the bad value? Where was the invariant violated?
  - Formulate 3–5 hypotheses formatted as: *"If X is the cause, then changing Y will make the bug disappear."*
  - Rank them from highest to lowest probability.
  - See `resources/root-cause-investigation.md`.
- **Mechanical Exit Condition**: Written list of 3–5 ranked falsifiable predictions.

### Phase 4: Instrument and Probe
- **Objective**: Validate or invalidate the top-ranked hypothesis using isolated, tagged telemetry.
- **Rules**:
  - Tag every log with a unique tag, e.g., `[DEBUG-4a1f]`.
  - Mutate **only one variable at a time**.
  - If the probe disproves the hypothesis, **immediately revert the probe**. Do not leave speculative edits.
  - If 3 hypotheses fail, trip the **Circuit Breaker** (see Section 4).
- **Mechanical Exit Condition**: Log evidence proving or disproving the active hypothesis.

### Phase 5: Root Fix and Regression Test
- **Objective**: Lock down the fix at a legitimate architectural seam with a permanent regression test before applying the fix.
- **Rules**:
  - Write a regression test at the true seam (exercising the real multi-caller or integration boundary).
  - Watch the regression test fail against the unpatched code.
  - Apply the root fix to production code.
  - Watch the regression test pass.
  - **False Green Guard**: Strictly verify that the test passed because the code was fixed, NOT because assertions were deleted or exceptions silenced.
- **Mechanical Exit Condition**: Passing regression test and clean root fix.

### Phase 6: Verify and Clean
- **Objective**: Prove no regressions exist across the broader system and eliminate all diagnostic artifacts.
- **Rules**:
  - Re-run the original (un-minimized) scenario from Phase 1.
  - Run the full test suite and build pipeline.
  - Search and destroy all tagged instrumentation: `git diff | grep "\[DEBUG-"`.
  - Ensure zero sensitive data or tokens leak in commit artifacts.
- **Mechanical Exit Condition**: Zero tagged logs remaining, full test suite green, build passes.

---

## 4. The Circuit Breaker Protocol (Rule of 3)

LLMs exhibit an escalating failure spiral when hypotheses fail: models generate increasingly desperate, broad, and destructive mutations.

```
Failed Attempt 1 ──▶ Restore owned attempt changes. Move to Hypothesis 2.
Failed Attempt 2 ──▶ Restore owned attempt changes. Move to Hypothesis 3.
Failed Attempt 3 ──▶ TRIP CIRCUIT BREAKER:
                     1. Preserve user edits; restore only verified attempt-owned changes.
                     2. STOP all autonomous mutations.
                     3. Prohibit silent codebase refactoring.
                     4. Escalate disproven evidence and architectural gap to user.
```

The Rule of 3 limits compounding damage. Record the pre-attempt baseline and compare exact changes before recovery. Whole-tree checkout/reset/clean is forbidden; overlapping or uncertain ownership means preserve the diff and report the boundary, not discard it.

---

## 5. Countering the 5 AI Evasion Moves

| Evasion Move | AI Rationalization | Mechanical Counter-Protocol |
| :--- | :--- | :--- |
| **1. The False Green** | "I'll catch the error and return an empty array so it doesn't fail." | Forbid swallowing errors or weakening assertions; review git diff of test strictly. |
| **2. The Symptom Patch** | "I'll deduplicate items in the React component with `[...new Set()]`." | Backward trace to data origin (fix SQL JOIN, not the UI view). |
| **3. Sleep Lengthening** | "Increasing sleep from 1000ms to 5000ms makes the test pass." | Condition-based waiting: poll actual state predicates with timeout. |
| **4. Blame Deflection** | "This is an upstream framework bug or environment flake; ignore it." | Raise repro rate (100x loop) or isolate test polluter with `find_polluter.py`. |
| **5. Wild Refactor** | "The architecture is bad; let me rewrite this entire subsystem." | Circuit breaker: 3 failures requires escalation, not an unauthorized rewrite. |

---

## 6. Progressive Disclosure Directory

Detailed references and runnable tooling are packaged locally under `resources/`:

- **`resources/triage-and-feedback-catalog.md`**: Complete 10-tier feedback loop catalog, repro-rate raising protocols, and cross-platform HITL driver templates (`hitl-loop.sh` & `hitl_loop.py`).
- **`resources/root-cause-investigation.md`**: Backward data-flow tracing technique, multi-component boundary logging, falsifiable hypothesis formatting, and architectural seam analysis.
- **`resources/flaky-and-concurrency-debugging.md`**: 4 categories of non-reproducible bugs, condition-based waiting patterns, and test polluter isolation engine.
- **`resources/defense-and-recovery.md`**: The Iron Law, Rule of 3 circuit breaker specification, defense-in-depth, untrusted error quarantine, and secret redaction.
- **`resources/worked-example.md`**: Complete end-to-end multi-tenant cache collision case study with embedded zero-dependency Python verification harness.
