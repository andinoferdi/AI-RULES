---
name: andino-brainstorming
description: Explore possible directions for an uncertain goal, creative idea, research topic or everyday problem, including a build request whose direction the user says is unclear and has not delegated. Operates under Andino Workflow governance.
---

# Explore possible directions

Internal method ID: `andino-brainstorming` (alias: `brainstorming`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Help the user discover and compare possible directions when the goal or solution
is still open. This is useful across software, writing, research, planning, art
and everyday choices.

Activate for: An explicit request to brainstorm, a vague goal with no clear direction, or a request to explore possibilities before choosing.

Do not activate for: An accepted, sufficiently specified task; a request to explain a confusing prior answer; a rough direction that is ready for focused refinement; or a fixed consequential choice whose missing criteria need resolution.

Positive request: “I want to make something useful for my neighborhood, but I have no idea what.”

Negative request: “Implement this approved endpoint specification.”

These are selection examples, not a claim that any router or method was executed.

## Inputs and dependencies

The user's situation, motivation, desired outcome, known constraints, already accepted decisions and any relevant current artifacts. Inspect available evidence for facts; do not ask the user to supply facts that can be read locally.

## Procedure

1. Read the request and relevant artifacts. Identify the user's situation,
   motivation and desired outcome. Separate stated needs and decisions from your
   assumptions, and respect explicit constraints and anything already settled.

2. If a material piece of context is missing, ask one natural, open question about the user's situation, motivation or desired outcome. Ask only when the answer would change the exploration. When the user asks you to make a reasonable start or skip questions, state consequential assumptions briefly and proceed.

3. Explore several meaningfully different directions before favoring one. Anchor them in what the user said; use examples, analogies or a small set of lenses only when they help reveal new possibilities. Do not turn the first response into an exhaustive catalog or force a choice too early.

4. Compare promising directions against the user's desired outcome, constraints, likely trade-offs and ways each could fail. Label guesses as guesses. Use research only when an external factual claim matters, following Search First; brainstorming alone does not make speculation evidence.

5. Reflect the useful shape of the conversation: what the user is trying to achieve, candidate directions, meaningful trade-offs, unresolved decisions and any defaults you chose. Ask a focused follow-up only if the answer changes the next step. If the user has delegated the choice, recommend one direction and explain the basis.

6. Offer a sketch, diagram, mockup or throwaway prototype only when seeing or trying it would resolve a concrete uncertainty and the available tools and current authorization support it. Mark experiments as exploratory; do not treat a prototype as approved product work.

7. Hand off to the narrowest existing method when exploration has done its job:
   `decision-interview` resolves consequential missing requirements;
   `idea-refine` sharpens one emerging direction; `decision-map` organizes
   several coupled or complex decisions; `design-prototype` tests a question
   better answered by a visual or runnable artifact; `specification` records a
   sufficiently chosen direction for planning. Council offers independent
   perspectives when that is the user's intent and Council is available. Continue
   under the current Andino task and plan.

## Ownership, precedence and permissions

Andino owns lifecycle, routing, the durable plan/checkpoint, delegation, permissions and acceptance. This guide explores; it is not a mandatory prerequisite, secondary router, second plan or implementation lifecycle. Explicit user choices and current project contracts override generic exploration defaults. `decision-interview`, `idea-refine`, `decision-map`, Council and the other methods keep their separate purposes; do not collapse them into a generic interview.

Brainstorming grants no authority to contact people, search externally, create or
change project files, keep a prototype, install tools, or make external writes.
Use only actions already authorized for the task. Search First owns needed
external research. Preserve existing work and state.

## Outputs, verification and fallback

Return distinct options, why they may fit, their material trade-offs, and the
assumptions or user decisions behind them. Verify the summary against the
conversation and current artifacts; do not report a direction as user-approved
unless they chose it. Store an accepted outcome in the existing Andino ticket or
artifact convention rather than creating a competing record.

If the user is unavailable or a useful tool is missing, make a bounded text-only
exploration from known facts, label unresolved points and give one concrete next
action. Do not claim a visual test, external research or user decision that did
not happen.

## Bounded routing example

This standard-library example checks the boundary between exploration, a missing decision and an accepted specification. It selects a route only; it does not invoke a method or create an artifact.

```python andino-example
import json

def route(request):
    if request["accepted_spec"] and not request.get("reopen", False):
        return "normal-workflow"
    if request["fixed_options"]:
        if request["material_criteria_missing"]:
            return "decision-interview"
        if request.get("complex_choice", False):
            return "decision-map"
        return "normal-workflow"
    return "brainstorming"

RESULT = {
    "explore": route({"accepted_spec": False, "fixed_options": False, "material_criteria_missing": False}),
    "fixed_choice": route({"accepted_spec": False, "fixed_options": True, "material_criteria_missing": True}),
    "known_complex_choice": route({"accepted_spec": False, "fixed_options": True, "material_criteria_missing": False, "complex_choice": True}),
    "known_simple_choice": route({"accepted_spec": False, "fixed_options": True, "material_criteria_missing": False}),
    "specified": route({"accepted_spec": True, "fixed_options": False, "material_criteria_missing": False}),
}
print(json.dumps(RESULT, sort_keys=True))
```

Expected result:

```json
{"explore": "brainstorming", "fixed_choice": "decision-interview", "known_complex_choice": "decision-map", "known_simple_choice": "normal-workflow", "specified": "normal-workflow"}
```

The example demonstrates route selection only. It does not establish that a router activated the method or that an implementation ran.

## Provenance

Adapted in original wording from the audited local snapshot path
`obra/superpowers:skills/brainstorming/SKILL.md`. The snapshot identity and
license are recorded in [the package provenance record](../../references/legal/provenance.md);
upstream defaults that conflict with Andino ownership, authorization or current
user intent are not imported.
