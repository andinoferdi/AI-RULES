---
name: andino-deep-module-design
description: Designs high-leverage interfaces that hide internal complexity behind clean seams. Operates under Andino Workflow governance.
---

# Design a Deep Module

Internal method ID: `andino-deep-module-design` (alias: `deep-module-design`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, single durable checkpoints, and anti-loop guards. Selected skills own their full procedures, resource contracts, and verification checks. Do not re-invoke `andino-workflow` recursively.

Concentrate significant domain behavior behind a compact, intuitive interface at a justified seam. The benchmark is **Caller Leverage**: *"Does this module maximize capability while minimizing the concepts a caller must learn?"*

## Activation & Negative Gates

- **Use when**:
  - Callers repeatedly duplicate policy, orchestration, or error compensation across multiple call sites.
  - An interface is shallow—nearly as complex to learn and configure as the underlying code.
  - Testing is brittle because tests mock internal helpers rather than testing observable outcomes.
  - Refactoring micro-modules into a cohesive domain facade to improve AI-navigability.
- **Do NOT use when**:
  - Request is for a whole-codebase macro survey (use `andino-architecture-survey`).
  - Speculative abstraction where only one caller exists and no variation is planned.
  - Pure in-process utility code with zero observed caller friction.

## The Five Deep Design Invariants

1. **Depth is Leverage, Not Line Count**: Maximize functionality per interface concept. Padding implementation lines does not create depth.
2. **The 2-Adapter Invariant**: A seam requires at least two concrete adapters (e.g. production transport + in-memory test fake). One adapter is useless indirection.
3. **The Deletion Test**: If deleting the module causes complexity to return across N callers, it is deep. If complexity vanishes, it was a pass-through wrapper.
4. **The Interface is the Test Surface**: Callers and tests cross the exact same external seam. Never expose internal seams merely to enable unit tests.
5. **Replace, Don't Layer**: When deepening shallow modules, delete their superseded unit tests once the new interface tests pass.

## Anti-Rationalization Refutations

| Rationalization | Mandated Reality |
|---|---|
| *"More micro-files make the codebase more modular."* | **False.** Fragmented files destroy locality, force callers to orchestrate policy, and blow up AI context windows. |
| *"We need an interface port in case we change databases."* | **False.** Until a second concrete adapter exists, an interface is speculative indirection. Program to the concrete class. |
| *"We must export internal helpers to unit test them."* | **False.** Testing private implementation details creates brittle tests. Test observable outcomes through the public interface. |
| *"A smaller class is always a better class."* | **False.** Classes with 10 lines that require 8 parameters and 4 sister classes create shallow architecture. Deep classes hide complexity. |
| *"We should keep old unit tests alongside new interface tests."* | **False.** Layering obsolete tests locks in dead abstractions. Delete superseded unit tests ("Replace, Don't Layer"). |

## Diagnostic Red Flags (Stop Immediately)

- [ ] Creating an interface (`IOrderRepo`) with only one concrete implementation across the entire codebase.
- [ ] Exporting an internal class, helper function, or private state variable purely to write a unit test.
- [ ] Asking a caller to pass more than 3 mandatory configuration parameters for the 90% common case.
- [ ] Maintaining unit tests that assert on internal method execution order rather than returned domain values.
- [ ] Introducing a deep module wrapper without running the Deletion Test.

## Progressive Disclosure Resources

- [resources/dependency-and-seam-discipline.md](resources/dependency-and-seam-discipline.md) — The 4 dependency categories, seam rules, and testing surface alignment.
- [resources/design-it-twice-protocols.md](resources/design-it-twice-protocols.md) — Parallel subagent exploration across divergent constraints and synthesis rubric.
- [resources/leverage-rubric-and-catalogs.md](resources/leverage-rubric-and-catalogs.md) — Leverage Index formula, terminal visual cards, and TS/Python/Go/Rust catalogs.
- [resources/worked-example.md](resources/worked-example.md) — End-to-end checkout refactoring walkthrough and runnable verification harness.

## Operational Example (Offline)

```python andino-operational-example
import json, os
def eval_module(methods, params, hidden_behaviors, seams):
    burden = len(methods) + params
    if burden == 0: return {"status": "REJECTED", "error": "zero entrypoints"}
    leverage = round(hidden_behaviors / burden, 2)
    hypothetical = [s["name"] for s in seams if len(s.get("adapters", [])) < 2]
    is_deep = leverage >= 2.5 and len(hypothetical) == 0
    return {"deep": is_deep, "hypothetical_seams": hypothetical, "leverage": leverage, "status": "VERIFIED" if is_deep else "REJECTED"}
def probe():
    if os.getenv("ANDINO_NEGATIVE"):
        return eval_module(["v", "t", "r", "s", "p"], 5, 2, [{"name": "SinglePort", "adapters": ["ProdOnly"]}])
    return eval_module(["processOrder"], 1, 6, [{"name": "ShippingPort", "adapters": ["Prod", "InMemory"]}])
print(json.dumps(probe(), sort_keys=True))
```

Default output: `{"deep": true, "hypothetical_seams": [], "leverage": 3.0, "status": "VERIFIED"}`  
Adversarial output (`ANDINO_NEGATIVE=1`): `{"deep": false, "hypothetical_seams": ["SinglePort"], "leverage": 0.2, "status": "REJECTED"}`

## Output & Verification

Return the concrete module interface specification, dependency classification matrix, Design-It-Twice trade-off scorecard, and one `NEXT ACTION` in the active Andino ticket. Never claim completion without test evidence.
