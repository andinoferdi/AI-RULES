---
name: andino-decision-interview
description: Clarifies missing requirements and relentlessly grills decision frontiers. Consolidated into andino-brainstorming under Andino Workflow governance.
---

# Decision Interview (Consolidated into Brainstorming)

Internal method ID: `andino-decision-interview` (alias: `decision-interview`).

> **Andino Workflow Member Skill (Forwarding Contract)**
> `andino-decision-interview` has been elevated and consolidated into [`andino-brainstorming`](../brainstorming/SKILL.md).
> All interview, grilling, intent-extraction, and decision-refinery capabilities operate canonically under `andino-brainstorming`.

## Purpose and Routing

Resolve material uncertainty about requirements, scope, or architecture through single-question grilling on active decision frontiers before implementation.

- **Canonical Destination**: [`skills/brainstorming/SKILL.md`](../brainstorming/SKILL.md)
- **Craft Guide**: [`skills/brainstorming/GUIDE.md`](../brainstorming/GUIDE.md)
- **Active Grilling Protocol**: [`skills/brainstorming/resources/grilling-protocol.md`](../brainstorming/resources/grilling-protocol.md)

## Forwarding Directive

When invoked directly as `/decision-interview` or `/andino-decision-interview`, or routed via Andino Workflow:
1. Load and execute the canonical [`andino-brainstorming`](../brainstorming/SKILL.md) procedure.
2. Formulate intent hypothesis (`<70%` trigger), classify path (Spike, Bounded, Architectural), and probe active frontier nodes with reasoned defaults.
3. Emit in-flight ADRs, Domain Glossary, and Builder-Ready Specification upon mutual consensus.

## Backward-Compatible Verification Example

```python andino-operational-example
import sys

def resolve_method_route(method_id):
    if method_id in ("decision-interview", "andino-decision-interview", "interview-me", "grilling", "grill-me"):
        return {"canonical": "andino-brainstorming", "status": "FORWARDED"}
    return {"canonical": method_id, "status": "DIRECT"}

if __name__ == "__main__":
    res = resolve_method_route("andino-decision-interview")
    sys.exit(0 if res["canonical"] == "andino-brainstorming" and res["status"] == "FORWARDED" else 1)
```

## Provenance

Consolidated under `andino-brainstorming`. Adapts Addy Osmani (`interview-me`), Matt Pocock (`grilling`, `grill-me`, `grill-with-docs`), and Obra Superpowers (`brainstorming`).
