---
name: andino-brainstorming
description: Explore ambiguous goals, relentlessly grill decision frontiers, capture in-flight ADRs and domain glossaries, and produce builder-ready designs before implementation. Operates under Andino Workflow governance.
---

# Brainstorming: Explore, Grill & Refine Decisions

Internal method ID: `andino-brainstorming` (aliases: `brainstorming`, `decision-interview`, `interview-me`, `grilling`, `grill-me`, `grill-with-docs`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, and single durable checkpoints. Hand off to `andino-planning` or `andino-tdd`; do not re-invoke the workflow recursively.

## Purpose and Selection

Turn open-ended goals into builder-ready designs without guessing user intent. Synthesizes intent extraction, relentless decision-tree grilling, in-flight ADR generation, and 3-path classification.

- **Activate for**: Ambiguous requests, open product directions, architectural decisions, missing intent, or explicit interview/grilling prompts. Multi-session initiatives with branching dependencies escalate to `andino-decision-map`.
- **Do not activate for**: Clear accepted tickets, settled specifications, routine bug fixes, or minor mechanical edits. Never reopen settled decisions merely because this skill was named.

## Inputs and Progressive Resources

Inspect repository code, configs, and recent commits for discoverable facts before asking questions. Use local resources progressively:
- [Relentless Grilling Protocol](resources/grilling-protocol.md): Decision DAGs, unblocked frontiers, 1-question contracts, and fatigue breakers.
- [In-Flight ADR & Glossary Templates](resources/adr-and-glossary-template.md): Schemas for ADR capture and Ubiquitous Language glossaries.
- [End-to-End Worked Example](resources/worked-example.md): Real-world scenario from vague intake to builder-ready design.

## Procedure

1. **Hypothesis & De-buzzwording**: State a 1-sentence hypothesis of desired intent with an explicit confidence score. If `<70%`, state missing variables. Decompose buzzwords ("scalable", "flexible", "intuitive") into falsifiable criteria. Read repo facts directly; never ask users for discoverable code details.
2. **Three-Path Classification**: Announce path aloud before proposing solutions:
   - **Spike**: Feasibility probe (*"Can we..."*). 2-sentence plan, quick nod, throwaway output. No spec or ADR.
   - **Bounded**: Scoped edit to an existing flow. Short in-chat design (approach, touched files, test assertion). **STOP and wait for explicit approval**.
   - **Architectural**: New subsystems, altered interfaces, or cross-cutting boundaries. Full grilling, trade-off matrix, lazy ADR, and formal written spec. For multi-session efforts with branching decisions, escalate to `andino-decision-map` to chart the map and manage the fog of war. Complexity ratchet is one-way: escalate upon discovering hidden scope.
3. **Frontier Grilling with Reasoned Defaults**: Probe only unblocked nodes on the decision DAG. Present **one** question at a time, paired with a recommended default (*"Recommended default: [Option A] because [reason]. Reply 'agree' or steer"*). Cap sequential questions at 3. If user replies are terse (`<10` words), trip the **Fatigue Breaker**: halt questioning and present remaining defaults in a table for bulk confirmation.
4. **Lazy Documentation & Predictability Exit**: Terminate upon frontier exhaustion or **3-Question Predictability** (>90% confidence in predicting next 3 answers). Emit:
   - **Builder-Ready Design Spec**: Context, components, failure modes, acceptance targets.
   - **In-Flight ADR**: Context, chosen approach, alternatives rejected, and floor invariants.
   - **Domain Glossary**: Ubiquitous terms, anti-terms (synonyms to avoid), and code mappings.

<HARD-GATE>
Zero production code, scaffolding, or dependency installation before explicit user consensus on the design. Conversational design approval permits writing the spec; written spec approval permits invoking `andino-planning`.
</HARD-GATE>

## Anti-Rationalization Refutations

| Rationalization Shortcut | Required Operational Response |
|---|---|
| *"Task is obvious; I'll start coding."* | Hard gate: classify path and obtain explicit design consensus before writing code. |
| *"I'll ask 5 questions in one message."* | Cognitive flooding: ask exactly 1 question on the active DAG frontier with a recommended default. |
| *"I'll emit full ADR docs mid-conversation."* | Lazy emission: maintain latent models during dialogue; emit formal ADRs only upon design consensus. |
| *"User gave 1-word answer, so I'll keep probing."* | Fatigue breaker: halt sequential turns, present remaining items in a table with defaults for bulk sign-off. |

## Diagnostic Red Flags (Stop Immediately)

1. Writing or modifying code before obtaining design consensus.
2. Asking open-ended questions without proposing a reasoned default.
3. Interrogating users about codebase facts inspectable via search or file tools.
4. Reciting a static generic checklist instead of traversing the unblocked decision frontier.

## Outputs, Verification and Fallback

Deliver approved Design Specification, ADR-0001, and Domain Glossary. Hand off cleanly to `andino-planning` or `andino-tdd`. In unattended mode, use safe reversible defaults and record missing decisions as blocked.

## Runnable Operational Example

```python andino-operational-example
import os, sys

def evaluate_discovery_turn(path_type, confidence, frontier_unblocked, consecutive_questions, user_word_count):
    if path_type not in ("spike", "bounded", "architectural"):
        return {"status": "FAIL", "reason": "Invalid path classification"}
    if path_type == "architectural" and confidence < 0.70 and not frontier_unblocked:
        return {"action": "INTERROGATE_INTENT", "gate": "LOCKED"}
    if consecutive_questions >= 3 or user_word_count < 10:
        return {"action": "FATIGUE_BREAKER_TABLE", "gate": "LOCKED"}
    if not frontier_unblocked:
        return {"action": "EMIT_ADR_AND_SPEC", "gate": "UNLOCKED"}
    return {"action": "GRILL_FRONTIER_WITH_DEFAULT", "gate": "LOCKED"}

if __name__ == "__main__":
    is_neg = os.environ.get("ANDINO_NEGATIVE") == "1"
    res = evaluate_discovery_turn(
        path_type="invalid" if is_neg else "architectural",
        confidence=0.85,
        frontier_unblocked=False,
        consecutive_questions=1,
        user_word_count=20
    )
    if is_neg:
        sys.exit(1 if res["status"] == "FAIL" else 0)
    sys.exit(0 if res["action"] == "EMIT_ADR_AND_SPEC" and res["gate"] == "UNLOCKED" else 2)
```

## Provenance

Adapted from `addyosmani/agent-skills:skills/interview-me`, `mattpocock/skills:skills/productivity/grilling`, `grill-me`, `engineering/grill-with-docs`, and `obra/superpowers:skills/brainstorming` under MIT license.
