# Failure-Form Matching and Bulletproofing Protocols

Supporting craft protocol for `andino-skill-maker`. Read with [SKILL.md](../SKILL.md) and [GUIDE.md](../GUIDE.md).

## 1. The Empirical Failure-Form Matrix

Before authoring guidance, classify the baseline defect observed in agent behavior. Empirical testing demonstrates that applying the wrong guidance form measurably degrades compliance—and in several cases produces worse results than providing no guidance at all.

| Baseline Failure Mode | Observable Defect | Correct Guidance Form | Toxic / Backfiring Form |
| :--- | :--- | :--- | :--- |
| **Discipline Failure** | Agent knows the rule but cuts corners under stress (urgency, fatigue, sunk cost). | **Prohibition + Rationalization Table + Red Flags** | Soft recommendations (*"prefer...", "consider...", "try to..."*). |
| **Shaping Failure** | Agent complies with the intent, but the output structure is bloated, inverted, or verbose. | **Positive Recipe or Explicit Ordering Contract** | Negative prohibitions (*"never narrate", "don't restate spec"*). |
| **Omission Failure** | Agent consistently forgets a required field, citation, error code, or invariant. | **Structural Slot / Required Field in Template** | Prose reminders or warnings placed near the prompt end. |
| **Contextual Failure** | Correct action depends on environment, branch, or file state. | **Conditional on Observable Predicate** | Unconditional rule + vague exemption clauses (*"unless necessary"*). |

### Why Prohibitions Backfire on Shaping Problems
When agents face competing cognitive pressures (such as brevity versus completeness), a prohibition like *"Do not summarize the task"* triggers semantic negotiation. In head-to-head wording experiments on prompt generation:
- The **Prohibition Arm** (*"Don't restate the background"*) generated **more** unwanted background text than the no-guidance control. The negative token primed the model to focus on the prohibited topic.
- The **Recipe Arm** (*"Output exactly three sections: 1. Target, 2. Diff, 3. Command"*) eliminated background text completely across all test repetitions.
A positive recipe leaves zero conversational space for negotiation: the output either matches the required slots or it fails inspection.

---

## 2. Universal Drafting Laws

Regardless of the guidance form selected, apply these strict linguistic invariants:

### 1. No Nuance Clauses
- **Anti-Pattern:** `"Do not edit production code directly, unless the change is trivial or urgent."`
- **Why It Fails:** Appending an escape clause (*"unless..."*, *"except when appropriate"*) reopens semantic bargaining. The agent will rationalize that its current task is always the exception.
- **Rule:** Express legitimate exceptions as distinct conditional branches keyed to falsifiable, observable state:
  `"If git diff < 10 lines and file count == 1, execute inline. Otherwise, require formal plan."`

### 2. Exemption Clauses Leak Scope
- **Anti-Pattern:** `"Keep response under 100 words. (This limit does not apply to code snippets)."`
- **Why It Fails:** The model compresses or truncates the code snippets anyway because the word count constraint contaminates the entire completion window.
- **Rule:** Restructure boundaries structurally. Place exempt content in dedicated artifacts, distinct files, or separate execution turns.

---

## 3. Bulletproofing Discipline Against Rationalization

Discipline-enforcing skills (such as TDD, verification gates, and code-review loops) require defensive armor against model shortcuts. LLMs are highly articulate and will invent persuasive justifications when under operational pressure.

### The Foundational Principle
Always embed this non-negotiable anchor in discipline skills:
```markdown
Violating the letter of the rules is violating the spirit of the rules.
```
This single sentence cuts off an entire family of *"I am adhering to the overarching intent while bypassing the formal ritual"* rationalizations.

### Loophole Elimination: Absolute Refusal to Compromise
Never leave a negative rule open to adaptation. Explicitly enumerate and forbid common workarounds:

```markdown
<!-- BAD: Open to rationalization -->
Write code before test? Delete it.

<!-- GOOD: Bulletproofed against all known loopholes -->
Write code before test? Delete it immediately. Start over with TDD.

No exceptions:
- Do NOT keep the code as a "reference".
- Do NOT "adapt" or copy snippets while writing tests.
- Do NOT comment it out to un-comment later.
- Do NOT look at it.
Delete means permanent deletion.
```

---

## 4. Comprehensive Anti-Rationalization Refutations

Every discipline skill must pair common model excuses with their objective mechanical reality:

| Model Rationalization Shortcut | Mechanical Reality & Required Response |
| :--- | :--- |
| *"This change is too simple to need a test."* | Simple changes break in production precisely because they were assumed trivial. Writing the test takes 30 seconds. |
| *"I will write the tests right after implementing the code."* | Tests written after implementation ask *"What does this code do?"* instead of *"What should this code do?"*. They prove nothing about regression resistance. |
| *"I already manually tested it in the terminal."* | Ephemeral manual checks leave zero persistent regression guards in the repository. Build the automated test first. |
| *"I am following the spirit, not the mechanical ritual."* | Violating the letter is violating the spirit. The mechanical ritual is the only verifiable invariant in unattended execution. |
| *"Deleting this working code is wasteful and inefficient."* | Sunk cost fallacy. Preserving unverified code guarantees compound debugging latency later. Delete and restart from RED. |
| *"The user is in a hurry; I should skip the verification step."* | Delivering broken code fast is strictly slower than delivering verified code cleanly. Complete the verification gate. |
| *"The test failed due to environment issues, not my change."* | Environment failures and flaky harnesses are bugs. Fix the test seam before claiming GREEN. |

---

## 5. Diagnostic Red Flags (Stop and Restart)

Train agents to self-monitor for cognitive shortcuts. When any of these internal thoughts occur, the agent must **STOP immediately and revert to Phase 1**:

1. **Code Before Assertion:** Writing implementation logic while the test suite is still empty or unrun.
2. **Post-Hoc Rationalization:** Explaining why a failed assertion *"doesn't really matter in this scenario"*.
3. **Assertion Erosion:** Loosening assertions, increasing tolerances, or deleting test cases to make a red build pass.
4. **Arbitrary Sleep Injections:** Adding `sleep(5000)` or `time.sleep(2)` to mask asynchronous race conditions.
5. **Batching Unrelated Edits:** Bundling opportunistic refactoring into a focused bug fix.
6. **Narrative Substitution:** Describing how a feature works in prose instead of providing a runnable test or verified artifact.
7. **Ignoring Linter / Compiler Warnings:** Treating compiler diagnostics as optional suggestions.
8. **Bypassing Verification:** Declaring a task complete based solely on exit code 0 without inspecting output content.
