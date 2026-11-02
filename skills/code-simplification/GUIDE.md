# The Craft of Behavior-Preserving Code Simplification

This guide defines the comprehensive methodology for reducing cognitive complexity in software while preserving exact behavior under Andino Workflow governance.

---

## 1. Foundations: Lossless Cognitive Compression

In software engineering, complexity is not measured in lines of code or character counts. It is measured in **cognitive load**—the amount of working memory required for a human engineer or peer AI agent to trace, reason about, and modify a piece of code.

### The Three Forms of Cognitive Load
1. **Intrinsic Load**: The irreducible complexity of the domain problem itself (e.g. calculating tax brackets across jurisdictions, implementing a cryptographic handshake).
2. **Germane Load**: The cognitive effort spent organizing and understanding domain concepts (e.g. well-named abstractions, domain models).
3. **Accidental Load**: The unnecessary friction introduced by awkward implementation choices (e.g. 5 levels of nested `if/else`, inconsistent variable names, dead pass-throughs, boolean parameter flags).

**The Core Axiom**: Simplification is **Lossless Cognitive Compression**. Its sole objective is to eliminate *accidental load* while safeguarding *intrinsic domain rules* and *germane domain vocabulary*.

---

## 2. The Comprehension Standard

Every proposed simplification must satisfy a simple, rigorous benchmark:

> **The 2 AM On-Call Test**:
> *"Can an engineer on call at 2:00 AM, woken up by an alert, locate a defect and trace control flow in this function within 15 seconds without guessing?"*

If a refactor makes the code shorter but requires a mental pause to decipher operator precedence, hidden type coercions, or nested ternaries, it has **failed** the Comprehension Standard.

---

## 3. Chesterton's Fence & Git Blame Archeology

Before modifying, re-ordering, or deleting any line of code, an engineer or agent must understand why it exists.

> *"If you find a fence built across a road and see no reason for it, do not tear it down. First find out why it was built. Once you understand the reason, only then may you judge whether it still applies."* — G.K. Chesterton

### The Pre-Simplification Archeology Checklist
Before touching code:
1. **Trace Callers & Callees**: What systems consume this function? Does any caller rely on a specific exception type or null return?
2. **Inspect Git Blame & Commit Messages**: Was this check added to fix an emergency production incident? Was it a workaround for a browser bug or race condition?
3. **Check Existing Tests**: What invariants are explicitly covered? What edge cases (e.g. empty strings, negative numbers, null values) are expected?
4. **Inspect Protected Regions**: Are there `# simplify-ignore-start/end` or `// simplify-ignore-start/end` pragmas? If so, record their exact SHA-256 byte hashes immediately.

---

## 4. Dominant Negative Gates (When NOT to Simplify)

Simplification is prohibited when any of the following gates apply:

1. **Gate 1: Untested Legacy Code ("No Test, No Touch")**
   If a component has zero automated test coverage, refactoring it is reckless. First author characterization tests under `andino-tdd`. Only after tests are GREEN may simplification begin.
2. **Gate 2: Performance-Critical Hot Paths**
   Unrolled loops, bitwise manipulations, in-place array mutations, and pre-allocated buffers are intentionally unidiomatic to avoid garbage collection and CPU pipeline stalls. Never "clean up" a hot path.
3. **Gate 3: Compliance & Legal Calculations**
   Tax, accounting, and cryptographic procedures are written explicitly and step-by-step so that non-technical regulators and auditors can verify them against official specs. Do not compress them into clever one-liners.
4. **Gate 4: Unrelated Scope**
   Do not perform "drive-by" refactors on files untouched by the current task. Limit changes to the immediate diff.

---

## 5. The 4-Step Simplification Lifecycle

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  1. Understand  │ ──▶ │   2. Identify    │ ──▶ │ 3. Apply Increm. │ ──▶ │   4. Verify     │
│ Context & Fence │     │ Concrete Smells  │     │ One Change/Test  │     │ Parity & Hash   │
└─────────────────┘     └──────────────────┘     └──────────────────┘     └─────────────────┘
```

### Step 1: Understand Before Touching
Read the full surrounding context. Record the public contract:
- Input domain and boundary conditions.
- Output shapes and return types.
- Exception contracts (exact types and error messages).
- Side-effect ordering (I/O, database writes, metric logging).

### Step 2: Identify Concrete Opportunities
Scan against the catalogs in [resources/patterns-and-anti-patterns.md](resources/patterns-and-anti-patterns.md):
- Structural complexity: Deep nesting, monolithic functions, boolean flags.
- Naming & readability: Generic names (`data`, `temp`), misleading names, redundant "what" comments.
- Redundancy: Dead pass-throughs, duplicated logic, redundant type assertions.

### Step 3: Apply Changes Incrementally (The Rule of 500)
- Make **one small structural change at a time**.
- Run the test suite after each change.
- **The Rule of 500**: If a refactoring pass touches more than 500 lines across a codebase, stop manual editing. Invest in automated AST transforms, codemods, or regex scripts. Manual edits at scale inevitably introduce regressions.

### Step 4: Verify the Result
- Run existing tests unchanged: 100% must pass with zero modifications to test files.
- Verify protected regions: compute post-edit SHA-256 and confirm it matches pre-edit baseline.
- Review the diff: ensure no stylistic churn or accidental renames occurred.

---

## 6. Anti-Rationalization Refutation Table

| Agent Rationalization | Reality & Mandated Rule |
|---|---|
| *"Fewer lines of code is always simpler."* | **False.** A 1-line nested ternary or dense regex is far harder to debug than a 6-line `if/else`. Simplicity is comprehension speed, not line count. |
| *"It's working, so there's no need to touch it."* | **False.** Working code with deep nesting and tangled logic is an incident waiting to happen during the next urgent change. Simplify while tests are green. |
| *"I'll just quickly clean up this other file while I'm here."* | **False.** Unscoped refactoring creates noisy PR diffs, bloats git history, and risks regressions in unmonitored code. Stay within your bounded task. |
| *"The types make it self-documenting; names don't matter."* | **False.** Type signatures describe structure, not intent. A variable named `res` typed as `UserRecord` is still opaque compared to `authenticatedUser`. |
| *"I can remove this defensive check because the caller shouldn't pass null."* | **False.** In real-world distributed systems, unexpected inputs happen. Never remove defensive error handling unless invariants mathematically prove it unreachable. |
| *"I'll refactor this while implementing the new feature."* | **False.** Never mix refactoring with feature delivery. A PR that does both is impossible to bisect and review cleanly. Separate them into two distinct commits. |

---

## 7. Diagnostic Red Flags

Halt and re-evaluate immediately if you observe any of these 8 red flags:
1. **Test Modification Required**: You had to alter an existing test assertion or fixture to make it pass (you almost certainly introduced a behavioral regression).
2. **Exception Drift**: A function that previously raised `KeyError` now raises `ValueError` or returns `None`.
3. **Protected Region Hash Mismatch**: The SHA-256 digest of a block fenced by `# simplify-ignore-start/end` changed.
4. **Diff Explosion**: A routine refactor bloated into hundreds of lines of stylistic changes.
5. **Over-Inlining**: Named domain concepts were eliminated and their low-level math pasted into call sites.
6. **Side-Effect Reordering**: Async operations or database writes had their execution sequence inverted.
7. **Breaking Public Signatures**: Exported function parameters or return shapes were altered.
8. **Removed "WHY" Comments**: Critical intent comments explaining platform bugs or workarounds were deleted.

---

## 8. Integration with Andino Workflow

In the Andino Workflow lifecycle, `andino-code-simplification` operates primarily as the **Refactor gate**:
- **After TDD (`andino-tdd`)**: Once a feature is GREEN, code often contains quick implementation scaffolding. Run simplification to clean up nesting and naming before finalizing.
- **Before Code Review (`andino-code-review`)**: Running simplification first strips accidental complexity and diff noise, allowing peer reviewers to focus on architecture, correctness, and security.
- **Durable Checkpoint**: Record the Simplification Ledger in the active ticket (`docs/exec-plans/active/<ticket>.md`).

---

## 9. Operational Example (Offline)

The following runnable standard-library example is executed during verification passes to validate behavior parity and protected-region hash integrity.

```python andino-operational-example
import hashlib, json, os
from pathlib import Path

def before(x):
    if x is None: raise TypeError("missing")
    if x < 0: raise ValueError("negative")
    return x * 2

def after(x):
    if x is None: raise TypeError("missing")
    if x < 0: raise ValueError("negative")
    return 2 * x

def observed(fn, x):
    try: return ("value", fn(x))
    except Exception as e: return (type(e).__name__, str(e))

def probe():
    protected = b"# simplify-ignore-start\nFAST = 7\n# simplify-ignore-end\n"
    p = Path("protected.txt")
    p.write_bytes(protected)
    if os.getenv("ANDINO_NEGATIVE"):
        p.write_bytes(protected.replace(b"7", b"8"))
    equal = all(observed(before, x) == observed(after, x) for x in [None, -2, -1, 0, 1, 2, 100])
    return {
        "behavior_equal": equal,
        "protected_equal": hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256(protected).digest(),
        "cases": 7
    }

print(json.dumps(probe(), sort_keys=True))
```

Expected output:
```json
{"behavior_equal": true, "cases": 7, "protected_equal": true}
```

Adversarial variant (`ANDINO_NEGATIVE=1`):
```json
{"behavior_equal": true, "cases": 7, "protected_equal": false}
```

---

## 10. Local Resources

- [resources/patterns-and-anti-patterns.md](resources/patterns-and-anti-patterns.md) — Comprehensive Before/After catalogs for TypeScript, Python, and React.
- [resources/protected-regions.md](resources/protected-regions.md) — Multi-language comment syntax and SHA-256 verification rules.
- [resources/agent-simplification-protocols.md](resources/agent-simplification-protocols.md) — Subagent safety constraints and the Simplification Ledger.
- [resources/worked-example.md](resources/worked-example.md) — Complete walkthrough with runnable verification script.

---

## 11. Provenance

Adapted from addyosmani/agent-skills, source `skills/code-simplification/SKILL.md`. Substantive adapted material is covered by the packaged Addy MIT notice ([references/license.md](references/license.md)). Upstream is audit/build provenance only; runtime requires no upstream installation or network fetch.

