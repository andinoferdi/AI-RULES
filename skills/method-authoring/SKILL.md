---
name: andino-method-authoring
description: Legacy authoring shim forwarding to andino-skill-maker under Andino Workflow governance.
---

# Method Authoring (Compatibility Forwarding Shim)

Internal method ID: `andino-method-authoring` (aliases: `method-authoring`, `writing-skills`).

Forwarding contract: redirects to canonical `andino-skill-maker` for skill,
runbook, procedural authoring, evaluation, and craft.

## Forwarding Directive

Invocations as `method-authoring`, `andino-method-authoring`, or `writing-skills`
resolve to canonical `andino-skill-maker`. Locate resources by active layout:
- Nested: `../skill-maker/SKILL.md`, `GUIDE.md`, `resources/contract.md`
- Native: `../andino-skill-maker/SKILL.md`, `GUIDE.md`, `resources/contract.md`

Select containing layout first; avoid broken unconditional markdown links.
Enforce dual-mode authoring, line budgets, and honest NOT_VERIFIED fallbacks.

## Backward-Compatible Verification Example

```python andino-operational-example
import sys

FORWARDING_MAP = {
    "method-authoring": "andino-skill-maker",
    "andino-method-authoring": "andino-skill-maker",
    "writing-skills": "andino-skill-maker",
}
LAYOUT_TARGETS = {
    "nested": "../skill-maker/SKILL.md",
    "native": "../andino-skill-maker/SKILL.md",
}

def resolve_authoring_route(name):
    target = FORWARDING_MAP.get(name)
    if not target:
        return {"resolved": False, "canonical": name, "status": "UNKNOWN"}
    return {
        "resolved": True,
        "canonical": target,
        "status": "FORWARDED",
        "supported_layouts": tuple(sorted(LAYOUT_TARGETS.keys())),
    }

if __name__ == "__main__":
    result = resolve_authoring_route("andino-method-authoring")
    if not (result["resolved"] and result["canonical"] == "andino-skill-maker"):
        sys.exit(1)
    print("FORWARDING_VERIFIED: andino-skill-maker")
    sys.exit(0)
```

## Provenance

Legacy identifier preserved for backward compatibility under existing package
MIT attribution. Consolidated into canonical `skills/skill-maker/`.
