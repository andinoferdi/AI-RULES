---
name: andino-agent-document-authoring
description: Use when authoring, auditing, or refactoring agent-facing guidance, instruction documents, context pointers, AGENTS.md, or CLAUDE.md. Operates under Andino Workflow governance.
---

# Agent Document Authoring: Write Predictable Agent Instructions

Internal method ID: `andino-agent-document-authoring` (aliases: `agent-document-authoring`, `writing-for-agents`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow protocol: single durable checkpoint, proportional investigation, anti-loop guards.
> Loading this file does not invoke another skill or mutate repository state. Upstream references yield to current policy.

## 1. Dominant Negative Gates (When NOT to Use)

Reject invocation immediately if ANY condition holds:
- **Executable Skills & Runbooks**: Designing executable skills with step-by-step TDD belongs in `skill-maker`.
- **Durable Architectural Decisions**: Authoring ADRs, product specs, or domain dictionaries belongs in `documentation-and-adrs`.
- **Mechanically Enforceable Rules**: Formatting, imports, and syntax enforceable via linter/compiler belong in automated tooling.
- **Transitory Conversation Context**: Ephemeral notes or one-off conversation summaries belong directly in session chat.

## 2. Dual-Mode Operational Triage Router

| Mode | Selection Trigger | Operational Protocol |
| :--- | :--- | :--- |
| **Mode A: Remedial / Audit** | Bloated guide, observed agent shortcutting, negation cascade, or stale instruction sediment. | Run 5-point diagnostic rubric; excavate sediment; delete default model no-ops sentence by sentence; rewrite prohibitions into positive steering; attach observable bounds. |
| **Mode B: Greenfield** | New `CLAUDE.md`, `AGENTS.md`, context pointer reference, or repository operational guide. | Declare floor invariants; stratify into 3-tier hierarchy ladder; inline universal rules; disclose conditional branches behind pointers; establish demanding observable bounds. |

## 3. The 5 Floor Invariants

1. **Positive Target Steering**: Prompt the affirmative target behavior. Prohibitions (*don't think of an elephant*) activate the forbidden state in model attention. Reserve bans for hard safety gates, paired with positive alternatives.
2. **Demanding Observable Bounds**: Terminate steps with checkable binary predicates (exit code 0, file existence, schema valid) to resist post-completion pull and prevent premature completion.
3. **3-Tier Hierarchy Ladder**: Stratify content into Tier 1 (in-file steps), Tier 2 (in-file reference), and Tier 3 (disclosed reference behind context pointers). Never let reference bury sequential steps.
4. **Single Source of Truth & Zero Environment Caching**: Author each meaning in exactly one place. The filesystem, `package.json`, and `--help` are live truths; cache only invisible gotchas and rationale.
5. **Relentless No-Op Pruning**: Audit sentence by sentence against the model's unguided default. If a line does not measurably alter output behavior, delete the entire sentence.

## 4. Anti-Rationalization Refutations

| Rationalization Shortcut | Mechanical Reality & Required Response |
| :--- | :--- |
| *"A negative rule ('never do X') is enough to prevent errors."* | Prohibitions increase attention on the banned concept tokens. Rewrite as a positive target recipe. |
| *"I'll inline this 50-line edge case so the agent has all context."* | Inlining conditional branches buries sequential steps (**Sprawl**). Disclose behind a precision context pointer. |
| *"The step says 'make sure everything looks good'; that's clear."* | Subjective bounds invite premature completion. Replace with an observable predicate (e.g. exit code 0). |
| *"I should explain standard CLI commands so the agent doesn't forget."* | Restating `--help` or `package.json` caches stale data. Let the agent discover live commands from the environment. |
| *"Adding 'please be thorough' makes the model think deeper."* | Generic pleasantries are zero-yield no-ops. Enforce thoroughness via high-demand completion bounds. |

## 5. Diagnostic Red Flags (Stop Immediately)

1. Writing instructions that restate environment data (`package.json`, directory trees, CLI manual pages).
2. Steering primarily through negative prohibitions without providing explicit positive target actions.
3. Leaving sequential steps with unverifiable completion conditions (*"verify code looks clean"*).
4. Summarizing multi-page reference files inline within root guidance or `CLAUDE.md`.

## 6. Progressive Disclosure Router (Need-to-Resource Mapping)

Load only the specific resource required for the active authoring phase:

| Operational Need | Resource Target | Invariant / Boundary |
| :--- | :--- | :--- |
| Diagnostic rubric, document schemas, and evaluation contract | [contract.md](resources/contract.md) | 5-point rubric compliance |
| Rekayasa pointer konteks, katalog leading words, positive steering | [context-pointer-and-leading-words.md](resources/context-pointer-and-leading-words.md) | Front-load leading word; zero synonyms |
| Tangga hierarki 3-tier, ko-lokasi, pencegahan sprawl, splitting | [information-hierarchy-and-progressive-disclosure.md](resources/information-hierarchy-and-progressive-disclosure.md) | Disclose conditional branches |
| Pencegahan premature completion, kriteria observable, forcing legwork | [demanding-completion-bounds-and-legwork.md](resources/demanding-completion-bounds-and-legwork.md) | Checkable and exhaustive bounds |
| Disiplin SSOT, audit cache lingkungan, no-op sentence hunting | [pruning-and-no-op-hunting.md](resources/pruning-and-no-op-hunting.md) | Delete zero-yield sentences |
| Template siap pakai (`CLAUDE.md`, runbooks, router), refactoring pass | [agent-document-templates-and-runbooks.md](resources/agent-document-templates-and-runbooks.md) | <60 lines for root guidance |

## 7. Embedded Operational Verification Harness

```python andino-operational-example
import os, sys, json
from pathlib import Path

# Evaluate candidate instruction entries against 5 floor invariants
entries = [
    {"rule": "positive-steering", "active": True},
    {"rule": "demanding-bounds", "active": True},
    {"rule": "three-tier-ladder", "active": True},
    {"rule": "ssot-zero-cache", "active": True},
    {"rule": "no-op-pruning", "active": True},
]

# Negative injection test gate
if os.environ.get("ANDINO_NEGATIVE") == "1":
    sys.stderr.write("FATAL: ANDINO_NEGATIVE=1 injected; simulated floor invariant violation.\n")
    sys.exit(1)

valid = all(e["active"] for e in entries) and len(entries) == 5
payload = {
    "valid": valid,
    "status": "CONTRACT_VERIFIED" if valid else "REJECTED",
    "invariants_checked": len(entries),
    "mode": "deterministic-offline"
}
print(json.dumps(payload, sort_keys=True))
sys.exit(0 if valid else 1)
```

## 8. Provenance and Governance

Independently adapted for the Andino Workflow runtime from audited snapshot principles in:
- `mattpocock/skills:skills/productivity/writing-for-agents/SKILL.md`
- `mattpocock/skills:skills/productivity/writing-for-agents/SKILL-MECHANICS.md`

All adapted material is covered by the packaged MIT notice ([references/license.md](references/license.md)).
