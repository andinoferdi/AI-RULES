---
name: andino-code-simplification
description: Behavior-preserving code simplification. Reduces cognitive complexity while preserving exact public behavior. Operates under Andino Workflow governance.
---

# Behavior-Preserving Code Simplification

Internal method ID: `andino-code-simplification` (alias: `code-simplification`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, single durable checkpoints, and anti-loop guards. Selected skills own their full procedures, resource contracts, and verification checks. Do not re-invoke `andino-workflow` recursively.

Reduce demonstrated complexity while preserving accepted public behavior exactly. The benchmark is **Comprehension Speed**: *"Can an on-call engineer at 2 AM locate a defect in this function within 15 seconds?"*

## Activation & Negative Gates

- **Use when**: Working GREEN code with observed nesting, duplication, opaque names, or cognitive complexity.
- **Do NOT use when**:
  - Tests are failing or missing (apply **"No Test, No Touch"**; write characterization tests first).
  - Code is on a performance-critical hot path, SIMD loop, or cache-line buffer.
  - Code represents legal, regulatory, tax, or cryptographic compliance calculations.
  - Changes touch code outside the immediate task diff (no drive-by refactoring).

## The Five Principles

1. **Preserve Behavior Exactly**: All inputs, outputs, side-effects, exception types, and error messages must remain 100% invariant.
2. **Follow Project Conventions**: Align with existing codebase idioms, import orders, and naming conventions.
3. **Prefer Clarity Over Cleverness**: Explicit 6-line code beats an unreadable 1-line chained ternary or dense regex.
4. **Maintain Balance**: Never inline named domain concepts, merge unrelated logic, or strip defensive checks.
5. **Scope to What Changed**: Limit refactoring to the immediate diff. For changes over 500 lines, use AST/codemods.

## Anti-Rationalization Refutations

| Rationalization | Mandated Reality |
|---|---|
| *"Fewer lines is always simpler."* | **False.** Line count is not complexity. Comprehension speed is the true metric. |
| *"It's working; leave it alone."* | **False.** Working code with high accidental complexity breeds regressions during urgent fixes. |
| *"I'll clean up unrelated files too."* | **False.** Unscoped changes bloat diffs and create unreviewed blast radiuses. |
| *"The types make it self-documenting."* | **False.** Types document structure, not domain intent. Descriptive names are required. |
| *"I'll refactor while adding this feature."* | **False.** Never mix feature additions with refactoring. Split them into discrete commits. |

## Diagnostic Red Flags (Stop Immediately)

- [ ] Modifying an existing test assertion or fixture to pass (indicates a behavioral regression).
- [ ] Altering an exception type, error string, or relaxing validation logic.
- [ ] Modifying any byte within a `# simplify-ignore-start/end` or `// simplify-ignore-start/end` block.
- [ ] Inlining a helper that names an essential domain concept.
- [ ] Inverting the execution order of async operations or I/O side-effects.

## Progressive Disclosure Resources

- [resources/patterns-and-anti-patterns.md](resources/patterns-and-anti-patterns.md) — Before/After catalogs for TS/JS, Python, and React.
- [resources/protected-regions.md](resources/protected-regions.md) — Multi-comment syntax and SHA-256 byte-hash integrity rules.
- [resources/agent-simplification-protocols.md](resources/agent-simplification-protocols.md) — Subagent safety constraints and Simplification Ledger.
- [resources/worked-example.md](resources/worked-example.md) — Complete walkthrough with runnable verification harness.

## Operational Example (Offline)

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
    p = Path("protected.txt"); p.write_bytes(protected)
    if os.getenv("ANDINO_NEGATIVE"): p.write_bytes(protected.replace(b"7", b"8"))
    equal = all(observed(before, x) == observed(after, x) for x in [None, -2, -1, 0, 1, 2, 100])
    return {"behavior_equal": equal, "protected_equal": hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256(protected).digest(), "cases": 7}
print(json.dumps(probe(), sort_keys=True))
```

Default output: `{"behavior_equal": true, "cases": 7, "protected_equal": true}`  
Adversarial output (`ANDINO_NEGATIVE=1`): `{"behavior_equal": true, "cases": 7, "protected_equal": false}`

## Output & Verification

Return the concrete Simplification Ledger, modified file identifiers, exact test results, and one `NEXT ACTION` in the active Andino ticket. Never claim completion without test evidence.

## Provenance

Adapted from addyosmani/agent-skills, source `skills/code-simplification/SKILL.md`. Substantive adapted material is covered by the packaged Addy MIT notice ([references/license.md](references/license.md)). Upstream is audit/build provenance only; runtime requires no upstream installation or network fetch.

