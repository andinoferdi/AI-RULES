# Bidirectional Agent Code Review Protocols

This document defines the bilateral operational contracts for AI coding agents participating in code reviews under Andino Workflow governance. It establishes rigorous guardrails across three roles: **Requesting Review**, **Conducting Review**, and **Receiving Review**.

---

## Protocol 1: Requesting Code Review (Author / Coordinator)

Use the same brief for a handoff or a self-review checkpoint. Dispatch an
independent reviewer only when isolation adds value and the governing
delegation method and user authorize it.

### Review brief

- **Change and intent:** What changed and which behavior should hold.
- **Requirements and standards:** Exact source pointers and any known gaps.
- **Scope:** Requested mode, resolved base and head, and any relevant
  staged, unstaged or untracked content. For WIP provide the patch and
  included new-file bytes or a reproducible read-only snapshot. A path list
  alone is insufficient. Exclude unrelated and sensitive material.
- **Verification:** Existing checks and observed results, separately from
  checks the reviewer should inspect or run.
- **Return:** The findings and verdict format from [the skill](../SKILL.md).

The reviewer checks that the provided bytes match the requested scope and
reports missing or drifted evidence before drawing conclusions from it.

---

## Protocol 2: Conducting Isolated Review (Reviewer Subagent)

### 2.1 Read-Only Execution Boundary
- The reviewer must **never mutate** the repository.
- Do not run commands that alter state (`git checkout`, `git reset`, `git commit`, `rm`, file edits).
- If checking out a different tree is required, use read-only tree inspection (`git show`) or a disposable snapshot provided by the coordinator.

### 2.2 Two-Axis Evaluation Framework
Use the Spec and Standards passes and the severity table from
[the skill](../SKILL.md). Cross-reference shared root causes. Report both
verdicts, then distinguish observed verification from open evidence gaps.

### 2.4 Providing Named Structural Remedies
Never submit a vague critique like *"This method is messy"* or *"Consider refactoring."* Provide the named structural remedy:
- **Problem:** Repeated if/else checks on an entity's status string.
  - **Remedy:** *Replace Conditional with Typed Dispatcher* or *Lookup Map*.
- **Problem:** Method accesses internal fields of another object 5 times.
  - **Remedy:** *Move Method to Data Owner* (resolving Feature Envy).
- **Problem:** Function takes 6 primitive parameters that travel together.
  - **Remedy:** *Introduce Parameter Object / Typed Interface* (resolving Data Clump).

---

## Protocol 3: Receiving Code Review (Author / Implementer)

### 3.1 Anti-Sycophancy & Forbidden Responses
AI agents receiving feedback frequently fall into performative sycophancy, agreeing with hallucinated or inaccurate feedback.
**Strictly Forbidden Responses:**
- [FORBIDDEN] *"You're absolutely right!"*
- [FORBIDDEN] *"Great catch! Excellent point!"*
- [FORBIDDEN] *"Thank you for the brilliant suggestion, implementing now!"*

**Required Mindset:**
- Technical verification over emotional agreement.
- Do not start editing code until the critique has been verified against the codebase.
- Actions and tests speak louder than flattering words.

### 3.2 The 6-Step Reception Workflow
When feedback arrives:
```
1. READ: Ingest the complete review without defensive or eager reactions.
2. UNDERSTAND: Restate the technical requirement or invariant in your own words.
3. VERIFY: Check the claim against the codebase reality (run tests, grep calls, inspect schema).
4. EVALUATE: Is the remedy technically sound for THIS codebase and architecture?
5. RESPOND: Acknowledge valid findings or push back with technical evidence.
6. IMPLEMENT: Apply authorized fixes in dependency order and verify the affected behavior.
```

### 3.3 1-Cycle Deadlock Prevention & Technical Pushback
If a reviewer flags an issue that is factually incorrect, hallucinated, or violates project constraints:
1. **Never Loop in Endless Debate:** Issue exactly **one** technical pushback containing concrete proof:
   - Citing passing regression test output.
   - Citing language specification or library documentation.
   - Demonstrating why the suggested change breaks existing invariants or introduces regression.
2. **Pushback Format:**
   ```markdown
   Pushback on [file:line]:
   The review noted that `calculateDiscount` fails when `rate == 0`.
   However, line 14 explicitly guards `if (rate <= 0) return 0;`, verified by
   unit test `test_zero_rate_returns_zero` in `tests/test_pricing.py:28`.
   Proceeding with implementation as-is.
   ```
3. **Escalation Boundary:** If the reviewer or peer insists on a disputed point after 1 cycle of technical pushback, halt autonomous modification and escalate directly to the human user or workflow coordinator. Do not loop.

### 3.4 YAGNI Filter for Speculative "Professional" Enhancements
If a reviewer suggests adding abstractions, configuration layers, or generic interfaces for future flexibility:
1. Grep the codebase for actual current usage.
2. If current callers or constraints provide no concrete benefit, decline the addition:
   *"Applying YAGNI: This helper currently serves a single internal call site. Introducing a plugin registry adds indirection without current architectural justification."*
