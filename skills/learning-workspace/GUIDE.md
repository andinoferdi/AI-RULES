# Build a learning workspace

Internal method ID: `learning-workspace`. Stable technique adapted to Andino ownership.

## Purpose and selection

Support quick learning in the current conversation and intentional, persistent learning across sessions. Structured learning uses trusted sources and demonstrated understanding rather than mere content coverage.

Activate for: An explicit request to learn a concept or process in this conversation, or an intentional multi-session learning goal. Use the quick branch for immediate explanation and optional practice; use the structured branch only when persistence is requested or clearly part of the user's goal.

Do not activate for: An ordinary factual question that needs a direct answer, a confusing prior explanation that needs repair, or an assumption that the user wants a persistent workspace, curriculum or recurring schedule.

## Inputs and dependencies

For quick learning: the current question, known context and any prior knowledge that materially changes the explanation. For structured learning: the user's selected workspace, mission, prior records/resources, reusable lesson assets and source evidence.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Choose the depth from the user's intent. A one-off factual question gets a direct answer. For an explicit quick-learning request, explain in the current conversation; do not create a workspace, files, HTML lesson or curriculum. For a persistent goal, read the selected workspace and prior records before extending it.

2. In the quick branch, give a contextual explanation and a concrete example. Assess prior knowledge only when it changes what should be explained; otherwise make a reasonable starting assumption and invite correction. Offer a short exercise when it would help practice, then give feedback and handle follow-up questions naturally.

3. Start or continue the structured branch only when the user wants learning to persist. Read the mission and existing records; establish motivation, observable success, constraints and out of scope when they are not already clear. Do not ask the user to repeat evidence already in the workspace. If no workspace is selected, ask where the user wants persistent materials before creating them.

4. Use trustworthy primary/reference sources for structured lesson claims and record them with useful annotations in the resources register. Use Search First when external research is actually needed and state source gaps; do not teach a precise procedure from unsupported guesses. A stable one-off concept does not require a research ritual.

5. Choose one short lesson tied to the mission and the learner's current knowledge. Keep knowledge acquisition clear, then provide relevant skill practice with timely feedback. Contextual judgment develops through real use; do not imply a quiz alone demonstrates it.

6. Reuse the workspace's existing assets and reference formats. Keep paths relative to the user's learning workspace, link related lessons and sources, and use the smallest useful artifact set; do not add reusable components just for uniformity.

7. Record stated prior knowledge and genuine demonstrated understanding, corrected misconceptions and evidence. Material merely covered is not a learning record. Vary correct quiz positions and avoid answer-length clues. Preserve superseded records; confirm mission changes and compare success criteria to decide whether to practice, review or finish. Do not schedule recurring learning unless separately requested.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-learning-workspace` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Quick answers stay in the conversation and remain understandable without setup; optional practice receives feedback. For structured learning, lesson claims cite sources, exercises give feedback, records reflect demonstrated learning, and a new session can resume from user-selected workspace files. The linked workspace example applies only to structured local artifacts; its deterministic result proves that bounded procedure, not model routing or host parity. Record actual actions and unresolved limits when claiming completion.

## Example and anti-patterns

Positive request: “Teach me safe retry design over several lessons in this learning folder.”

Negative request: “What does retry mean in one sentence?”

Invented move sequences/medical procedures, quizzes leaking correct answers, treating exposure as mastery, writing into skill installation or creating schedules/community accounts.

## Fallback

A sourced Markdown lesson with manual exercise feedback works without browser tools. State interaction, print rendering or topic correctness limitations honestly.

## Learning mode example

This standard-library example classifies intent only. The quick branch stays in chat; the structured branch is selected only for an explicit persistent goal; explanation repair remains separate.

```python evolution-example
import json

def choose_mode(request):
    if request["last_explanation_unclear"]:
        return {"mode": "repair", "persistent_goal": False}
    if request["multi_session_goal"]:
        return {"mode": "structured", "persistent_goal": True}
    if request["explicit_learning_request"]:
        return {"mode": "quick", "persistent_goal": False}
    return {"mode": "direct-answer", "persistent_goal": False}

RESULT = {
    "ordinary": choose_mode({"last_explanation_unclear": False, "multi_session_goal": False, "explicit_learning_request": False}),
    "teach_now": choose_mode({"last_explanation_unclear": False, "multi_session_goal": False, "explicit_learning_request": True}),
    "deliberate": choose_mode({"last_explanation_unclear": False, "multi_session_goal": True, "explicit_learning_request": True}),
    "confused": choose_mode({"last_explanation_unclear": True, "multi_session_goal": False, "explicit_learning_request": True}),
}
print(json.dumps(RESULT, sort_keys=True))
```

Expected result:

```json
{"confused": {"mode": "repair", "persistent_goal": false}, "deliberate": {"mode": "structured", "persistent_goal": true}, "ordinary": {"mode": "direct-answer", "persistent_goal": false}, "teach_now": {"mode": "quick", "persistent_goal": false}}
```

This example demonstrates mode selection; it creates no workspace or learning record.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/productivity/teach/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
