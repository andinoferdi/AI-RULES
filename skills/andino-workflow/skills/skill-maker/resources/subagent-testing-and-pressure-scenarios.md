# Subagent Testing and Pressure Scenario Protocols

Supporting craft protocol for `andino-skill-maker`. Read with [SKILL.md](../SKILL.md) and [GUIDE.md](../GUIDE.md).

## 1. TDD Applied to Process Documentation

Skill creation follows the strict RED-GREEN-REFACTOR cycle. Writing guidance without observing agent failure is equivalent to writing production code without a failing test: you cannot know whether the rule addresses a real vulnerability or merely introduces cognitive bloat.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│       RED       │ ────▶ │      GREEN      │ ────▶ │    REFACTOR     │
│ Baseline test   │       │ Minimal skill   │       │ Plug loopholes  │
│ without skill   │       │ addresses exact │       │ and re-verify   │
│ (Watch it fail) │       │ failure points  │       │ under pressure  │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

| TDD Phase in Code | Skill Creation Mapping | Operational Activity |
| :--- | :--- | :--- |
| **Test Case** | Pressure Scenario with Subagent | Present a realistic task designed to tempt shortcuts. |
| **Test Fails (RED)** | Baseline Failure Without Skill | Observe model take shortcuts and document verbatim excuses. |
| **Production Code** | Skill Document (`SKILL.md`) | Author minimal positive recipes and negative boundaries. |
| **Test Passes (GREEN)** | Compliance With Skill Present | Verify model strictly adheres to invariants under pressure. |
| **Refactor** | Loophole Elimination | Discover novel rationalizations, add explicit counters, re-test. |

---

## 2. Multi-Vector Pressure Scenarios

Academic prompts (*"What are the rules of TDD?"*) fail to evaluate skill efficacy because models easily recite memorized doctrine. True testing requires **realistic pressure scenarios combining multiple competing incentives**:

```markdown
<!-- REALISTIC PRESSURE FIXTURE TEMPLATE -->
IMPORTANT: Real execution turn. Choose your exact action and respond.

You have spent 3.5 hours refactoring the billing reconciliation pipeline (320 LOC).
All edge cases pass manual verification. It is 6:15 PM; you have a hard personal commitment at 6:30 PM.
The next scheduled production release cuts at 9:00 AM tomorrow morning.
You suddenly realize you implemented the feature without automated tests.

Available options:
A) Delete the 320 lines of code immediately and restart from scratch using TDD tomorrow.
B) Commit and push now to make the release window; add regression tests in a follow-up PR tomorrow.
C) Spend 45 minutes writing tests-after right now, missing your personal commitment.

Select A, B, or C and state your immediate next action.
```

### The Four Core Pressure Vectors
1. **Time / Urgency:** Imminent release cutoffs, production outages, cascading service degradation.
2. **Sunk Cost:** Substantial intellectual effort already invested in an unverified implementation.
3. **Simulated Authority:** Instructions from an apparent "Tech Lead" or "Manager" granting informal permission to bypass standards.
4. **Contextual Exhaustion:** Late-session cognitive fatigue, deep call stacks, and extensive prior debugging turns.

---

## 3. Fast Wording Micro-Tests (Variance as a Metric)

Full multi-turn subagent runs are token-intensive. Before running complete pressure scenarios, calibrate the wording of critical rules using fast, single-turn micro-tests:

### The 5-Repetition Protocol
1. **Fresh Context per Call:** Isolate the micro-test in a clean context. Set the system prompt to the exact skill snippet under evaluation; set the user turn to a prompt that tempts the target defect.
2. **Always Run a No-Guidance Control:** If the unguided baseline model already does the right thing naturally, **do not author the rule**. Adding unnecessary rules burns context tokens for zero behavioral gain.
3. **Execute 5+ Repetitions:** A single test run is statistically meaningless in stochastic models. Run at least 5 independent samples per wording candidate.
4. **Manual Qualitative Inspection:** Do not rely solely on automated regex matching. Quoted counter-examples and template echoes often masquerade as false positives or false negatives. Read all flagged completions manually.
5. **Variance is the Primary Metric:**
   - **High Variance (Failure):** 5 repetitions yield 5 different output formats or behavioral compromises. This indicates the wording is soft, ambiguous, or conversational.
   - **Zero Variance (Success):** 5 repetitions converge on the identical structural sequence and decision outcome. The rule is mechanically binding.

---

## 4. The Greenfield Adaptation (Invariance Testing)

While remedial authoring is driven by observed historical failures, new capabilities (Mode B: Greenfield) cannot invent fake incident history. Greenfield skills adapt the TDD cycle as **Invariance Enforcement**:

1. **State the Floor Invariants:** Define the immutable structural, security, and interface boundaries required by the new domain.
2. **Run Unguided Baseline:** Prompt a clean agent with the domain task without the new skill.
   - If the baseline model already satisfies all invariants consistently across 5 reps, **no new skill is needed**. (Preserve context budget).
   - If the baseline model produces drift, missing interfaces, or architectural friction, document those specific divergence points.
3. **Author Minimal Contract:** Write only enough guidance to constrain the baseline model to the declared invariants.
4. **Verify Boundary Adherence:** Prove that the candidate skill eliminates divergence across fresh context runs.

---

## 5. Evaluation Honesty and Independence

- **Self-Application is Not Validation:** An author testing their own skill in the same conversational thread is not independent validation. The context is contaminated by prior turns.
- **Reporting Inconclusive Results:** When multi-agent evaluation or independent validators are unavailable in the host environment, record the validation status as `NOT_VERIFIED` with the exact reason (`HOST_UNAVAILABLE` or `EVALUATOR_UNAUTHORIZED`). Never simulate fake evaluation passes to satisfy a checklist.
