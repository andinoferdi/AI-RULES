---
name: andino-decision-interview
description: An ambiguous ask, explicit interview request, or consequential choice with missing intent, including a known direction whose material user-owned requirement is open. Operates under Andino Workflow governance.
---

# Clarify the decision

Internal method ID: `andino-decision-interview` (alias: `decision-interview`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Resolve material uncertainty about the outcome before selecting an implementation.

Activate for: An ambiguous ask, explicit interview request, or consequential choice with missing intent.

Do not activate for: A clear accepted ticket, informational question, or simple mechanical edit.

## Inputs and dependencies

Current request, accepted decisions, repository facts, relevant prior artifacts and a responsive decision maker.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Read existing evidence first. Write a one-sentence hypothesis of the desired outcome and identify what is known, assumed and still consequentially unknown. Never turn a settled ticket into a new interview.

2. Start with a concrete moment: what happened last time, who needs this, and what would change. Probe conventional answers such as 'scalable' with a concrete failure or success observation. Distinguish goals, non-goals and anti-goals.

3. Separate discoverable facts from user decisions. Inspect available code or primary sources for facts; do not ask the user to enumerate files or commands you can inspect. Note material platform/medium decisions already made and defaults delegated to you.

4. Ask one discriminating question with a reasoned guess by default. If the user prefers rounds, ask only independent questions on the currently unblocked decision frontier. A question depending on an unanswered question waits. Recompute after each answer.

5. Play back outcome, user, why now, observable success, binding constraint and out of scope in the user's words. Mark your defaults as your calls. Clear ordinary approval and prior execution authorization count; do not demand magic wording or a numerical confidence ritual.

6. For a larger design, perform a builder-readiness check: what would a competent builder still need to guess, and how would a wrong guess change the plan? Fill answered items from evidence, settle minor delegated choices, and ask only material user-owned gaps.

7. Use a diagram or a throwaway spike only when it resolves a specific uncertainty; offer visual support at that moment. Existing UI ownership remains in force. Carry the result back to the same accepted plan. Proceed within existing authority once material gaps are resolved.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Output distinguishes facts, user decisions and agent defaults; every acceptance target traces to an answer or source; no unanswered material decision is silently filled.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “I asked for a dashboard but I am not sure what I actually need. Interview me.”

Negative request: “Implement the already approved invoice retry ticket.”

An interview that asks environmental facts, fabricates the human's answers, keeps asking after an accepted scope, or starts a second requirements lifecycle.

## Fallback

In unattended work use accepted decisions and safe reversible defaults. Record a genuinely missing user decision as blocked; continue independent authorized work.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `addyosmani/agent-skills:skills/interview-me/SKILL.md`
- `mattpocock/skills:skills/engineering/grill-with-docs/SKILL.md`
- `mattpocock/skills:skills/productivity/grilling/SKILL.md`
- `mattpocock/skills:skills/productivity/grill-me/SKILL.md`
- `obra/superpowers:skills/brainstorming/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
