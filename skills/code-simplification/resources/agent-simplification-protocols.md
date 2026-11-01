# Agent Simplification Protocols & Safety Guardrails

This document establishes the operational protocols governing subagents and AI actors during code simplification. It prevents the most common failure modes of automated refactoring: aggressive over-simplification, silent semantic erosion, and sycophantic regression.

---

## Protocol A: Scoping & Requesting Simplification

### 1. Bounded Diff Scope
- **Rule of Locality**: An agent must only simplify code within the immediate boundary of the current task or recently modified diff.
- **Prohibition on Drive-By Refactoring**: Do not clean up unrelated files or functions outside the assigned task unless the user explicitly requested a repository-wide sweep.
- **Blast Radius Budget**: A manual simplification pass touching more than 200 lines without automated codemods/AST tooling is a red flag. Split the change into discrete, reviewable commits.

### 2. The "No Test, No Touch" Invariant
- Simplification requires a functioning automated safety net.
- If the target code has **zero automated test coverage**, the agent is strictly FORBIDDEN from refactoring it.
- **Action Required**: First write characterization tests (using `andino-tdd`) asserting current behavior. Only after the suite is GREEN may simplification proceed.

---

## Protocol B: Isolated Execution Constraints (Anti-Regression Guards)

When performing simplifications, agents must treat existing behavior as an immutable contract. The following actions are classified as critical defects:

### 1. Prohibition on Error & Exception Modification
- **Never delete or relax error handling**: Do not remove `try/catch`, error return tuples, or guard clauses under the assumption that "this condition shouldn't happen."
- **Never alter exception types or messages**: If a function raises `ValueError("Invalid ID")`, replacing it with `TypeError` or a generic message breaks downstream callers relying on exact error matching.

### 2. Prohibition on Side-Effect Reordering
- If function $A$ logs a metric and then mutates a cache, an agent must NOT reorder them.
- In asynchronous code (e.g. JavaScript Promises, Python `asyncio`), never alter the concurrency model (e.g., converting sequential `await` calls to `Promise.all` without verifying that the operations are strictly independent and thread-safe).

### 3. Prohibition on Stripping Intent-Bearing Comments
- **Comments explaining "WHAT"** (e.g. `// increment i by 1`) should be deleted when the code itself is self-explanatory.
- **Comments explaining "WHY"** (e.g. `// WORKAROUND: Safari 15 WebKit bug where canvas alpha is cleared prematurely`) carry vital historical intent. Deleting a "WHY" comment is an unacceptable defect.

### 4. Prohibition on Mixed-Intent Branches
- Never combine a simplification pass with a feature addition or a bug fix.
- If an agent discovers a genuine bug while reading code to simplify it:
  1. Record the bug in the durable ticket / plan ledger.
  2. Finish the behavior-preserving simplification pass.
  3. Address the bug in a separate, dedicated task with a new test case.

---

## Protocol C: Simplification Ledger & Verification Gate

Before any simplified code is presented or committed, the agent must compile and verify the **Simplification Ledger**:

### 1. The Simplification Ledger Format

```markdown
### Simplification Ledger: `<file_path>::<function_name>`

- **Observed Complexity**: [e.g. 5-level nested `if/else`, duplicated validation, unclear variables]
- **Applied Remedy**: [e.g. Top-level guard clauses, extracted predicate `is_valid_session()`, lookup dictionary]
- **Cognitive Delta**:
  - Nesting depth: `5` → `2`
  - Cyclomatic paths: `8` → `4`
  - Lines of code: `62` → `41` (or neutral if readability improved without line count reduction)
- **Preserved Invariants**:
  - Exact error types and messages verified.
  - Side-effect ordering confirmed unchanged.
  - Protected regions verified byte-for-byte (SHA-256 intact).
- **Test Invariance**:
  - [x] All pre-existing tests pass.
  - [x] Zero lines changed in test files.
```

### 2. The Verification Gate Checklist
The agent must verify every item before declaring the task DONE:
- [ ] Existing test suite passes without modifying a single assertion or fixture.
- [ ] Linter and static type-checker report zero new errors or warnings.
- [ ] Diff is minimal and readable—no stylistic churn, arbitrary renames, or unrelated formatting tweaks.
- [ ] The Comprehension Standard is satisfied: *"Would an on-call engineer at 2 AM locate a bug in this function in 15 seconds?"*
