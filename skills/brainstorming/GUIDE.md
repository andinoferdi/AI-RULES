# Brainstorming: Explore possible directions

Internal method ID: `brainstorming`. Exploratory technique under Andino ownership.

## Purpose and selection

Discover what matters, explore credible directions, and leave a design a capable
builder can use without guessing consequential intent. Depth comes from testing
understanding against concrete situations, not from more questions or longer docs.
This applies to software, research, creative work and everyday problems.

Activate for: Exploring an uncertain goal or solution space, including a build
request whose direction remains open and has not been delegated.

Do not activate for: Accepted specifications, routine bugs, explanations of existing
work, settled alternatives needing assessment, or choices already delegated.
A chosen direction with a missing user-owned requirement belongs to decision-interview;
one rough idea needing refinement belongs to idea-refine. Do not reopen settled
decisions merely because this skill was named.

Positive request: "Our neighborhood needs help, but I don't know what would help most."
Negative request: "Implement the approved billing endpoint; choose internal details yourself."

## Inputs and dependencies

Use the request, accepted decisions and relevant current evidence. Inspect referred
project files and enough connections to understand what changes. Outside software,
use the available situation/materials; do not invent a repository requirement.
Stop looking when the next decision is grounded.

Read [the worked procedure and design examples](resources/worked-example.md) for
question patterns, project design contents or the builder-check prompt. Resources
are local; upstream repositories are provenance, not runtime dependencies.

## Procedure

### 1. Establish what is actually open

Distinguish facts with sources, user decisions, your proposals and unknowns.
Reflect the outcome and its reason only as far as known. Don't invent motivation
or treat a desired guarantee as a proven property of a solution.

Choose the next move by what could change the result:
- Factual gap: inspect relevant accessible evidence before asking.
- Open direction: ask about a concrete situation, outcome or trade-off.
- Accepted or delegated choice: reuse it and continue through the normal workflow.

For an underspecified request, start with one open question about the most important
unknown, with a reason when its consequence is unclear. Avoid a technology menu
before understanding the problem. A rich brief may settle this step already;
do not require an introductory confirmation turn.

### 2. Ask questions that can change the decision

Default to one primary question at a time, grounded in the last answer or a finding.
Identify what a different answer changes: direction, scope, acceptance or treatment
of a material risk. If it changes none of these, omit it. Offer a short menu when
the user is stuck; respect requested batches of independent questions. Never hide
several dependent questions inside one sentence.

Probe the live uncertainty rather than reciting a checklist:
- Replace adjectives with a concrete incident: what happened, to whom, and what
  would success look like in that same situation?
- Test boundaries: where does the normal case fail, whose needs conflict, and
  what must still hold under that exception?
- Challenge the leading assumption: what evidence would make a smaller intervention
  sufficient, or make the current favorite wrong?
- Separate outcomes from suggested means: what has been tried, what mattered in
  admired examples, and which cost or failure is unacceptable?

Play back settled parts in useful chunks; label your defaults as proposals with
reasons. Incorporate corrections in the same artifact. Don't repeatedly summarize
everything or request approval after every answer.

If a consequential factual claim remains unknown, investigate or propose a bounded
experiment with a discriminating outcome. Agreement cannot establish durability,
performance, demand or compatibility. Use required research/domain support under
Andino when applicable; no automatic council, graph or subagent.

### 3. Compare viable directions before committing

Develop alternatives, then screen them against goals, constraints and anti-goals.
Present the strongest two or three genuinely different surviving approaches before
the final design. Explain how each works here, gains, costs, and what must be true.
Include the existing workaround, a smaller intervention or doing nothing when credible.

Recommend one using those criteria and state what evidence would reverse it.
Don't manufacture options: if only one survives, explain why other paths fail.
A path violating a hard requirement is rejected, not another viable choice.
Avoid unsupported guarantees and precision; planned measurements remain unverified.

When the user owns the open choice, give the comparison space of its own and ask
which direction to take. When delegated, choose, state the reason and continue
within existing authority; don't force a separate selection turn.

### 4. Check readiness and write a proportionate design

Converge when outcome and why, observable success, scope boundaries, constraints,
selected/delegated direction and consequential failure cases are clear enough for
the next safe step. Remaining uncertainty needs an owner and treatment: evidence
to obtain, an agreed experiment, or a stated reversible builder choice. Material
user-owned gaps remain pending; critical assumptions cannot hide in builder discretion.
Do not demand certainty about every internal detail.

Write once in the existing artifact convention. In a software repo without one,
use `docs/specs/YYYY-MM-DD-<topic>-design.md` when persistence is useful. Outside a
repo, use the agreed document or conversation. Extend sufficient accepted documents
rather than duplicating them. A design is not a second execution plan.

- Small change: brief intent, alternatives/rationale, constraints, relevant failure
  behavior, acceptance example, and agent discretion.
- Project: also cover responsibilities/flow, affected interfaces or materials,
  failure/recovery, evidence/assumptions, concrete acceptance cases, open questions
  with owners, and handoff. Include only applicable sections; invent no infrastructure,
  schemas or success metrics just to fill a template.

### 5. Perform a builder-readiness check

Read as the person carrying out the design: what consequential choice must they
still guess? For a substantial project, use independent review only when authority,
available tools and expected benefit justify delegation. Follow Andino's worker
limit of at most three concurrent direct children and no nested spawning. Otherwise
check inline and state that boundary
honestly. Small briefs need a proportional self-check.

Triage findings:
- Answered already: incorporate the answer and source.
- Builder call: settle the reversible detail and mark it as your call.
- User-owned: ask only the consequential unresolved choice.
- Evidence gap: inspect/test; don't ask the user to approve a claim as fact.

Check grounding, viable alternatives, scope/invariants, failure behavior, observable
acceptance and decision authority. Every applicable material check must pass;
no average or 5/6 score can waive a blocker. Repair findings and recheck affected
parts. Don't loop reviewers or interviews without new evidence.

### 6. Respect the decision boundary and hand off

Do not implement against unresolved material user-owned choices. For exploration
where execution has not been delegated, present the concrete design and agent-made
calls for review before dependent implementation. Approval covers what was shown;
assent to an idea doesn't approve unseen details. Ordinary clear assent counts,
without magic wording.

Existing authorization and explicit delegation persist. If asked to choose and
proceed, state consequential choices and continue; don't demand document approval
again. If the user opts out of discovery, end this technique, state safe defaults
and follow the normal workflow. A high-consequence choice outside that delegation
still needs its owner; silence is not approval.

Hand off only what is missing: specification for buildable contracts, planning for
task ordering, or the accepted implementation/TDD route when already ready. Do not
force all of them or rewrite a sufficient approved specification.

## Ownership and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-brainstorming` and this guide expose one method, without recursive workflow invocation.

This method grants no Git, installation, external-write or deployment authority.
Reuse actual authorization; preserve user work/secrets and staging. Don't commit
designs automatically. A sketch or throwaway spike may answer one agreed uncertainty
within existing authority; label its limits and carry findings back to the design.
It doesn't authorize production scope or waive checks. Use host-native visuals
when seeing resolves a specific question; honor explicit UI choices and don't
start an unsolicited companion server.

## Outputs, verification and fallback

Return the decision/design, reasons/evidence, consequential open questions and next
useful action. An experiment can be the result instead of an architecture.
Never fabricate approval, research, reviewer use or passing checks. Restricted
tools mean named evidence gaps and conditional claims, not weaker acceptance.

The example below checks routing only. Fresh-context consumer observations are
needed for questioning/design behavior; structural checks do not prove autonomous
routing, cross-host parity or superiority to upstream.

## Bounded routing example

```python andino-example
import json

def route(request):
    if request.get("delegated", False):
        return "normal-workflow"
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

## Provenance

Adapted from `obra/superpowers:skills/brainstorming/SKILL.md`, with independent
Andino-specific questioning, readiness and ownership guidance. Attribution and
licensing remain in package legal references. No upstream server/scripts,
automatic commits or mandatory downstream invocation are imported.
