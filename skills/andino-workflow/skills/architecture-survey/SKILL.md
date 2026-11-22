---
name: andino-architecture-survey
description: Use when surveying codebase architecture friction, identifying shallow modules to deepen, diagnosing leaky seams, or generating visual before/after reports. Operates under Andino Workflow governance.
---

# Survey Architecture Friction: Deepen Modules and Encapsulate Seams

Internal method ID: `andino-architecture-survey` (aliases: `architecture-survey`, `improve-codebase-architecture`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: single durable checkpoint, proportional investigation, anti-loop guards.
> Non-destructive: inspects code and writes self-contained visual reports to OS temporary storage only.

## 1. Dominant Negative Gates (When NOT to Use)

Reject an architecture survey immediately if ANY condition holds:
- **Cosmetic Refactoring**: Pure variable, function, or file renames belong to routine mechanical refactoring.
- **Unbounded Global Scans**: Whole-repository scans across hundreds of files without churn hotspots or named targets.
- **Dormant Code Refactoring**: Proposing refactorings on stable, untouched code with zero commit churn violates YAGNI.
- **In-Survey Code Editing**: Modifying, refactoring, or creating product files during survey is strictly prohibited.

## 2. Tri-Mode Operational Triage Router

| Mode | Selection Trigger | Operational Protocol |
| :--- | :--- | :--- |
| **Mode A: Hotspot Churn-Driven** | Open exploration with no named subsystem. | Inspect recent commits (`rtk git log --oneline -n 100`) to find churn hotspots; bound exploration to active files. |
| **Mode B: Subsystem Bounded** | Explicit subsystem or pain point specified. | Bound exploration strictly to named target; walk callers, test suites, and internal dependencies. |
| **Mode C: Cross-Seam Leakage** | Suspected leaky abstractions or mock-heavy tests. | Trace caller-side coupling, database transaction leaks, and caller-side policy duplication. |

## 3. The 5 Floor Invariants

1. **The Deletion Test**: Propose deepening only if deleting the shallow module concentrates complexity rather than scattering it.
2. **The Two-Adapter Rule**: Never introduce an interface without proven variation; a justified seam requires at least two concrete adapters.
3. **Locality Over Fragmented Helpers**: Consolidate atomized helper files when production defects hide in caller-side coordination.
4. **Interface As The Test Surface**: Public interface of a deep module is its test surface; eliminate tests mocking internal wrappers.
5. **Zero In-Survey Refactoring**: Output lands in OS temp storage (`$TMPDIR`/`%TEMP%`); zero product code or Git changes occur.

## 4. Anti-Rationalization Refutations

| Rationalization Shortcut | Mechanical Reality & Required Response |
| :--- | :--- |
| *"This dormant file is messy; let's refactor it."* | Dormant code has zero ROI. Direct attention only to active commit churn hotspots. |
| *"I'll write the new interface in code right now."* | Premature editing violates survey safety. Present visual candidate cards first. |
| *"I used 'service' because it's standard industry term."* | Vague jargon. Use strictly the 10 canonical terms (`module`, `interface`, `seam`, etc.). |
| *"A text-only summary in chat is sufficient."* | Architecture surveys must be visual. Render side-by-side Before/After diagrams in HTML. |
| *"Wins can be summarized as 'cleaner code'."* | Empty fluff. Wins must be $\le 6$ words and follow `[Glossary Category]: [Claim]`. |

## 5. Diagnostic Red Flags (Stop Immediately)

1. Writing, modifying, or deleting product code files during the survey phase.
2. Scanning the entire repository without scoping or inspecting commit churn hotspots.
3. Generating a text-only report without side-by-side Before/After visual diagrams.
4. Drift into prohibited vocabulary (*component*, *service*, *unit*, *API*, *layer*, *wrapper*).
5. Proposing interfaces or seams that will only ever have a single concrete implementation adapter.

## 6. Progressive Disclosure Router

- Complete authoring methodology and deep craft: [GUIDE.md](GUIDE.md)
- 10 canonical terms, prohibited substitutions, and wins formula: [resources/architectural-vocabulary.md](resources/architectural-vocabulary.md)
- 5 visual Before/After diagram patterns (~320px height): [resources/diagram-patterns.md](resources/diagram-patterns.md)
- Hybrid HTML report scaffold and launcher protocol: [resources/html-report-scaffold.md](resources/html-report-scaffold.md)
- Subagent exploration brief and prompt templates: [resources/subagent-exploration-brief.md](resources/subagent-exploration-brief.md)
- Grilling loop, glossary synchronization, and ADR protocols: [resources/grilling-and-adr-protocols.md](resources/grilling-and-adr-protocols.md)
- End-to-end worked case study (Order Intake pipeline): [resources/worked-example.md](resources/worked-example.md)

## 7. Runnable Operational Contract & Verification Harness

```python andino-operational-example
import json, os, re, sys

def evaluate_survey_contract(data):
    if not isinstance(data, dict): return {"valid": False, "error": "Contract must be a dict"}
    mode = data.get("mode")
    if mode not in ("hotspot", "subsystem", "leakage"): return {"valid": False, "error": "Invalid mode"}
    name = data.get("name", "")
    if not re.fullmatch(r"andino-[a-z0-9]+(?:-[a-z0-9]+)*", name): return {"valid": False, "error": "Invalid name"}
    lines = data.get("contract_lines")
    if type(lines) is not int or lines < 1: return {"valid": False, "error": "contract_lines must be positive int"}
    if lines >= 150: return {"valid": False, "error": "Strict contracts require <150 lines"}
    if data.get("has_negative_gates") is not True: return {"valid": False, "error": "Missing negative gates"}
    if data.get("has_sdo_isolation") is not True: return {"valid": False, "error": "Missing SDO isolation"}
    if data.get("has_five_invariants") is not True: return {"valid": False, "error": "Missing five invariants"}
    return {"valid": True, "mode": mode, "status": "CONTRACT_VERIFIED"}

if __name__ == "__main__":
    is_neg = os.environ.get("ANDINO_NEGATIVE") == "1"
    payload = {
        "name": "andino-architecture-survey",
        "mode": "hotspot",
        "contract_lines": 150 if is_neg else 118,
        "has_negative_gates": True,
        "has_sdo_isolation": not is_neg,
        "has_five_invariants": True,
    }
    result = evaluate_survey_contract(payload)
    if not result["valid"]:
        sys.stderr.write(f"Verification failed: {result['error']}\n")
        sys.exit(1)
    print(json.dumps(result, sort_keys=True))
    sys.exit(0)
```

## 8. Provenance

Independently adapted from `mattpocock/skills:skills/engineering/improve-codebase-architecture` ([references/license.md](references/license.md)). Upstream bootstrap, automatic commit/push, and installers are not imported as authority.
