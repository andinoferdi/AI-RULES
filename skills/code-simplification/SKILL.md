---
name: andino-code-simplification
description: Simplify working code when nesting, duplication, unclear names, or unnecessary abstractions make it hard to follow. Preserve exact behavior and protected regions. Operates under Andino Workflow governance.
---

# Behavior-Preserving Code Simplification

Internal method ID: `andino-code-simplification` (alias: `code-simplification`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, single durable checkpoints, and anti-loop guards. Selected skills own their full procedures, resource contracts, and verification checks. Do not re-invoke `andino-workflow` recursively.

Reduce demonstrated complexity while preserving accepted public behavior exactly. Use the **2 AM on-call test** as a review heuristic. Compare how quickly a reader can locate the decision, trace its effects, and explain the failure path before and after the edit.

## Activation & Negative Gates

- **Use when**: Working GREEN code with observed nesting, duplication, opaque names, or cognitive complexity.
- **Do NOT use when**:
  - Tests are failing or missing (apply **"No Test, No Touch"**; write characterization tests first).
  - Code is on a performance-critical hot path, SIMD loop, or cache-line buffer.
  - Code represents legal, regulatory, tax, or cryptographic compliance calculations.
  - The candidate is outside the authorized target. Default to the immediate diff when no standalone target is named.
  - The target is already clear or the reason for an existing guard, ordering constraint, or abstraction is still unknown.

## The Five Principles

1. **Preserve Behavior Exactly**: All inputs, outputs, side-effects, exception types, and error messages must remain 100% invariant.
2. **Follow Project Conventions**: Align with existing codebase idioms, import orders, and naming conventions.
3. **Prefer Clarity Over Cleverness**: Explicit 6-line code beats an unreadable 1-line chained ternary or dense regex.
4. **Maintain Balance**: Never inline named domain concepts, merge unrelated logic, or strip defensive checks.
5. **Keep the Diff Focused**: Stay within the authorized target. For changes over 500 lines, use AST/codemods.

## Procedure

1. **Establish the baseline.** Read project guidance and nearby idioms. Trace callers, tests and effect boundaries. Identify what must stay observable, including supported inputs, defaults, return shape, exception type and message, and the order and count of reads and effects. Check history when the reason for a suspicious guard or workaround is unclear. Run focused tests before editing. If relevant behavior is uncovered, characterize it before refactoring. If tests fail or the baseline cannot be established, report the gap and leave the candidate alone. Read the protected-region protocol and capture byte hashes before editing any file containing markers.
2. **Choose a concrete improvement.** Name the reading problem and the smallest change that removes it. Flatten nesting only if guards run in the same order and preserve exit behavior. Give a hard-to-read predicate a name when it exposes a domain decision. Consolidate duplicate logic only when it represents the same rule and its callers can keep their distinct defaults and errors. Remove a wrapper only after checking what it contributes at the boundary. Keep domain names, defensive checks and comments that explain constraints. Skip candidates whose benefit or equivalence remains unclear.
3. **Edit in reviewable slices.** Change one decision or structural concern at a time and rerun the focused checks. If a slice changes behavior, isolate and undo that slice while preserving other work. Keep feature and bug-fix changes separate from the simplification.
4. **Verify behavior and readability.** Run relevant existing tests with their expectations intact and any applicable project checks. Exercise the edge cases that could distinguish the old and new code. Compare protected-region hashes when present. Read the diff as a caller and as an on-call maintainer. Keep the change only if the behavior evidence holds and the reading improvement is concrete.

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

- [GUIDE.md](GUIDE.md) — Deeper method and verification guidance.

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

For each retained change, report the location, original reading problem, improvement, preserved behavior and supporting check in the Simplification Ledger. Include exact test results and protected-region status where applicable. If nothing was changed, report the specific reason and any missing evidence. Use the active Andino ticket for the ledger and one `NEXT ACTION` when a ticket exists. Never claim completion without test evidence.

## Provenance

Adapted from addyosmani/agent-skills, source `skills/code-simplification/SKILL.md`. Substantive adapted material is covered by the packaged Addy MIT notice ([references/license.md](references/license.md)). Upstream is audit/build provenance only; runtime requires no upstream installation or network fetch.

