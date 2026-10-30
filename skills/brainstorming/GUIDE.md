# Brainstorming: Explore possible directions

Internal method ID: `brainstorming`. Exploratory technique adapted to Andino ownership.

---

## Purpose and selection

Help the user discover, shape, and compare possible directions when the goal, architecture, or solution space is still open. Good brainstorming extracts tacit constraints, prevents cognitive anchoring on the first obvious idea, and establishes clear boundaries before code crystallization introduces sunk-cost drag.

Activate for: An explicit request to brainstorm, a vague or open-ended goal with no settled architecture, exploring technical approaches before committing, or discovering unstated domain requirements.

Do not activate for: An accepted, sufficiently specified task; a routine bug or failing test; a request to explain a prior answer; or an approved specification ready for planning or implementation.

Positive request: "I want to build a real-time notification engine for our platform, but I am not sure whether to use WebSockets, SSE, or polling."

Negative request: "Implement this approved endpoint specification in the billing service."

These are selection fixtures, not a claim that a router or model was executed.

---

## Inputs and dependencies

The user's situation, motivation, desired outcome, known constraints, existing codebase architecture, and already accepted decisions. Inspect local files and context before asking questions; never ask the user to supply facts that can be read locally.

Use resources progressively: [worked procedure, design doc template, builder-check protocol, and diagnostic rubric](resources/worked-example.md). It provides end-to-end case studies, the production design document template, the subagent builder-check prompt, visual spike patterns, and a 6-point self-audit rubric.

---

## Core mental models

Effective ideation operates across five foundational principles:

### 1. Search-Space Reduction & Information Asymmetry
The human partner holds tacit domain constraints and unstated invariants; the AI holds broad combinatorial solution patterns. Brainstorming is an iterative probe to map boundary conditions and align on the problem's true shape before any code is written.

### 2. Adaptive Conversational Pacing & Bandwidth Matching
Cognitive overload destroys collaboration. 
- **For open-ended or ambiguous requests:** Ask exactly one high-leverage question per turn. Never bury the user under a bulleted questionnaire. Include a light escape hatch ("Or if you prefer to dive straight in, let me know").
- **For high-context requests:** Match the user's velocity. Synthesize their input, highlight unaddressed edge cases, and move directly to laying out concrete approaches.

### 3. Divergent Trade-Offs Before Convergence
LLMs suffer from greedy generation, anchoring prematurely on the single most obvious path. Before producing a design document, dedicate a standalone turn to presenting 2–3 genuinely distinct, viable approaches with honest trade-offs. Never present strawmen options to bias the choice.

### 4. Negative Boundary Delineation (Goals, Non-Goals, Anti-Goals)
Defining what *not* to build reduces the search space exponentially faster than positive features alone. Anti-goals define what would make the project a failure even if it technically works (e.g., introducing blocking synchronous network calls, creating vendor lock-in).

### 5. Pre-Implementation Hard Gate
Agentic execution is extremely fast, which makes premature building uniquely dangerous. Nothing gets implemented—no scaffolding, no dependency installation, no production code—until the human partner approves the structured design document.

---

## Procedure

### 1. Look before you ask & reflect the core intent
Inspect existing project files, dependencies, configuration, and recent commits.
- Read relevant code until you understand how the system works today and what this proposed change would touch.
- In your initial message, reflect the request in your own words: what they want, who it serves, and why.
- State any surprising constraints or existing patterns you uncovered.
- End with one incisive question that tackles the largest unsettled variable, plus a light opt-out offer.
- *Done when:* The problem is grounded in codebase reality and the user confirms the core intent.

### 2. Run adaptive Socratic dialogue
Engage in concise, focused exchanges to extract tacit requirements.
- Match vocabulary; avoid internal process jargon.
- Alternate chunked playback (synthesizing settled parts) with a single forward-looking question about the next unknown.
- Cover critical territory naturally: why now, success metrics, non-goals, anti-goals, and technical constraints.
- Offer lightweight recon (inspecting deeper code or data) when factual ambiguity arises.
- *Done when:* Core motivation, user invariants, and boundaries are clear.

### 3. Lay out the approaches in a dedicated turn
Once requirements are understood, present the architectural paths in a message of their own:
- Formulate 2–3 genuinely distinct, viable approaches. Discard weak options and strawmen.
- Ground each approach in the project's actual stack and detail concrete trade-offs (operational complexity, latency, scalability, maintenance).
- Recommend one approach with transparent justification, then ask the human partner to decide.
- *Done when:* The human partner explicitly selects an architectural approach.

### 4. Size the work and draft the written design document
Categorize the scope and draft the document according to [the design doc template](resources/worked-example.md):
- **Small Change:** Short written design covering intent, chosen approach, and key constraints.
- **Project:** Full written design document covering Intent, Goals, Non-Goals, Anti-Goals, Technical Invariants, Evaluated Approaches, Explicit Decisions vs. Builder Discretion, and Testability Seeds.
- Store software design docs in `docs/specs/YYYY-MM-DD-<topic>-design.md` (or repo convention).
- *Done when:* A complete, self-contained design document exists.

### 5. Execute builder check and adversarial stress-test
Before handing the document to the user for final sign-off:
- **In multi-agent environments:** Dispatch an independent subagent with the Builder-Check Prompt from [the worked example resource](resources/worked-example.md) to inspect the document for missing requirements or unstated assumptions.
- **In single-agent environments:** Run the 6-point diagnostic self-audit rubric from [the worked example resource](resources/worked-example.md) to stress-test your own draft.
- Settle minor engineering details under "Builder Discretion" and present only true user-level decisions to the human partner.
- *Done when:* All blocking ambiguities are resolved or surfaced to the user.

### 6. Enforce hard gate and hand off cleanly
<HARD-GATE>
Zero implementation code may be written until the human partner explicitly approves the design document. Building includes generating boilerplate, running scaffolding CLI tools, modifying files, or installing packages.
</HARD-GATE>
- Once approved, hand off cleanly under Andino Workflow to `andino-specification` (if formal type/interface contracts are needed), `andino-planning` (for task decomposition and ordering), or `andino-tdd` (for test-driven implementation).
- *Done when:* Design document is approved by the user and clean handoff to the next workflow phase is complete.

---

## Cognitive biases & red flags

| Thought / Rationalization | Reality & Corrective Action |
|---|---|
| "I'll offer a menu of 5 technologies right away." | Options steer and anchor. Get the user describing the problem in their own words first. |
| "I will assume sensible defaults silently." | Unspoken defaults are decisions the user never had a chance to reject. State them plainly. |
| "They answered my questions, so I can start coding." | Answers clarify intent; they do not approve architecture. Lay out approaches first. |
| "The user said 'sounds great', so the design is approved." | Approval of a concept is not approval of a design document. No code until the doc is approved. |
| "The spike prototype works, let's keep building on it." | Spikes bypass tests and quality gates. Discard or freeze as reference, then build via TDD. |
| "I should provide 1 good approach and 2 obviously terrible strawmen." | Strawmen waste time. Every presented approach must be a credible, defensible option. |

---

## Inputs and operational ownership

Read the accepted request, repository code, and relevant evidence first. Andino Workflow owns discovery, investigation depth, the single durable plan/checkpoint, delegation, permissions, and final acceptance. Brainstorming explores and shapes intent; it does not replace the planning or implementation phases. Explicit user choices outrank generic exploration defaults. Downstream methods (`andino-specification`, `andino-planning`, `andino-tdd`) maintain their separate operational boundaries.

---

## Permissions and safety

Brainstorming grants no authority to modify production code, install packages, create branches, or make external mutations. Visual spikes or throwaway prototypes must be explicitly agreed to, labeled as exploratory, and kept separate from production code. Preserve existing user work and secrets.

---

## Outputs, verification and fallback

Return distinct options, trade-offs, and the structured design document. Verify all statements against local code and evidence. Never claim a visual spike, subagent check, or user approval occurred unless verified by evidence. Store accepted artifacts in the agreed project location.

If tools are restricted or the user requests immediate progress, switch to rapid convergence mode: state consequential assumptions plainly, lay out the most viable approach, and produce a concise design brief.

---

## Bounded routing example

This standard-library example checks the boundary between exploration, a missing decision, and an accepted specification. It selects a route only; it does not invoke a method or create an artifact.

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

---

## Provenance

Adapted and elevated from `obra/superpowers:skills/brainstorming/SKILL.md` and independently enriched under Andino Workflow governance. Upstream licensing and attribution are preserved in [the package provenance record](../../references/legal/provenance.md). External shell/daemon scripts are replaced with host-native visual patterns and standard Markdown contracts.
