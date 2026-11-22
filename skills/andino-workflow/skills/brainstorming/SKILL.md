---
name: andino-brainstorming
description: Use for ambiguous goals, unclear success criteria, open product or architecture decisions, or requests to interview, grill or stress-test a design.
---

# Brainstorming: Explore, Grill & Refine Decisions

Internal method ID: `andino-brainstorming` (aliases: `brainstorming`, `interview-me`, `grilling`, `grill-me`, `grill-with-docs`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, and single durable checkpoints. Hand off to `andino-planning` or `andino-tdd`; do not re-invoke the workflow recursively.

## Purpose and Selection

Turn open-ended goals into builder-ready designs without guessing user intent. Synthesizes intent extraction, relentless decision-tree grilling, in-flight ADR generation, and 3-path classification.

- **Activate for**: Ambiguous requests, open product directions, architectural decisions, missing intent, or explicit interview/grilling prompts. Multi-session initiatives with branching dependencies use [decision-frontier](resources/decision-frontier/guide.md).
- **Do not activate for**: Clear accepted tickets, settled specifications, routine bug fixes, or minor mechanical edits. Never reopen settled decisions merely because this skill was named.

## Select a resource, not a second lifecycle

Load only the resource matching the current need. A direct resource selection uses
that procedure and current authority; it does not run this parent's other modes,
reopen accepted requirements or require a second execution plan.

| Current need | Resource | Exclusion |
| :--- | :--- | :--- |
| Branching decision mapping, multi-session dependency tracking | [decision-frontier](resources/decision-frontier/guide.md) | Single-session linear decision exploration |
| Fast throwaway spike, visual/interactive proof-of-concept | [feasibility-probe](resources/feasibility-probe/guide.md) | Settled architecture ready for production implementation |
| Concept stress-testing, value proposition validation | [idea-validation](resources/idea-validation/guide.md) | Settled concept ready for engineering specification |
| Structured async stakeholder questionnaire, boundary gathering | [async-questions](resources/async-questions/guide.md) | Active synchronous dialogue or settled requirements |

## Inputs and Progressive Resources

Inspect repository code, configs, and recent commits for discoverable facts before asking questions. Use local resources progressively:
- [Relentless Grilling Protocol](resources/grilling-protocol.md): Decision DAGs, unblocked frontiers, 1-question contracts, and fatigue breakers.
- [In-Flight ADR & Glossary Templates](resources/adr-and-glossary-template.md): Schemas for ADR capture and Ubiquitous Language glossaries.
- [End-to-End Worked Example](resources/worked-example.md): Real-world scenario from vague intake to builder-ready design.

## Procedure

1. **Ground the intent.** Inspect the relevant code, configuration and project vocabulary. Play back the likely outcome, who benefits and the constraint that matters, using the user's terms. Distinguish observed facts from your assumptions. Translate vague goals into observable behavior. When the goal itself is unclear, offer a tentative interpretation and ask about the outcome before choosing technology.
2. **Choose a path.** Use a **Spike** for a feasibility question, **Bounded** for a scoped change to an existing flow, and **Architectural** for new subsystems or changed boundaries. Escalate if discovery reveals a wider impact. Explain the practical consequence of the path when it affects what the user needs to decide.
3. **Resolve the next material decision.** Read the [grilling protocol](resources/grilling-protocol.md). Anchor each turn in a repo finding or the user's last answer. Ask one question whose answer changes the design. Give a revisable recommendation and its reason. When multiple viable approaches remain, explain the concrete trade-off between them. Accept a clear short answer and recompute which decisions are ready to discuss.
4. **Play back and confirm.** Summarize settled decisions when they change the design, after three questions on the same branch, or when the user asks to accelerate. Separate confirmed decisions, delegated choices and open decisions. Offer defaults for independent choices when useful. Material open decisions stay open until answered or explicitly delegated. Ask the user to confirm the resulting design before starting production work. Reuse design confirmation and downstream authorization already given for the same scope.

## Outputs, verification and handoff

| Path | Output | Handoff |
| --- | --- | --- |
| Spike | Question, success signal, and a short throwaway probe plan. Report the observation and its design implication. | Obtain authorization for the probe. Use the result to resolve the design question. |
| Bounded | Short design with the intended behavior, affected area and an observable acceptance check. | Confirm the design, then continue through the authorized execution route. |
| Architectural | Builder-ready design covering goal, scope, component boundaries, failure behavior and acceptance scenarios. Capture a consequential decision in an ADR and ambiguous domain terms in a glossary when they affect the build. | Confirm the written design, then hand off to `andino-planning` or `andino-tdd` as appropriate. |

If the user is unavailable, document confirmed decisions and reversible proposals
separately. Identify the unresolved decision that blocks any affected work.

## Runnable Operational Example

This fixture checks the distinction between resolved prerequisites, a material
open frontier and design confirmation. It does not measure interview quality.

```python andino-operational-example
import os

def next_step(decisions, design_confirmed):
    pending = {name for name, (_, settled) in decisions.items() if not settled}
    frontier = tuple(
        name for name, (dependencies, _) in decisions.items()
        if name in pending and pending.isdisjoint(dependencies)
    )
    if pending:
        return ("ask", frontier) if frontier else ("blocked", ())
    return ("handoff", ()) if design_confirmed else ("confirm", ())

if __name__ == "__main__":
    decisions = {
        "roles": ((), True),
        "sharing": (("roles",), False),
        "expiry": (("sharing",), False),
    }
    assert next_step(decisions, False) == ("ask", ("sharing",))
    assert next_step(decisions, True) == ("ask", ("sharing",))
    decisions["sharing"] = (("roles",), True)
    assert next_step(decisions, False) == ("ask", ("expiry",))
    decisions["expiry"] = (("sharing",), True)
    assert next_step(decisions, False) == ("confirm", ())
    assert next_step(decisions, True) == ("handoff", ())
    raise SystemExit(1 if os.environ.get("ANDINO_NEGATIVE") == "1" else 0)
```

## Provenance

Adapted from `addyosmani/agent-skills:skills/interview-me`, `mattpocock/skills:skills/productivity/grilling`, `grill-me`, `engineering/grill-with-docs`, and `obra/superpowers:skills/brainstorming` under MIT license ([references/license.md](references/license.md)).
