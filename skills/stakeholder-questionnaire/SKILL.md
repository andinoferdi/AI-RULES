---
name: andino-stakeholder-questionnaire
description: Progress depends on facts/decisions held by a named other person. Operates under Andino Workflow governance.
---

# Draft a questionnaire for someone else

Internal method ID: `andino-stakeholder-questionnaire` (alias: `stakeholder-questionnaire`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Get decision-relevant knowledge from the person who holds it through a usable local document.

Activate for: Progress depends on facts/decisions held by a named other person.

Do not activate for: The user can answer directly, environmental facts the agent can inspect, or an instruction to send messages without authority.

## Inputs and dependencies

Recipient role/expertise/relationship, decisions the user needs back, known context, desired local destination and any genuine deadline.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Clarify the send, not the subject: who holds the missing knowledge and what the user must be able to decide after reading answers. Reuse this information when already available.

2. Map every requested decision gap to a question aimed at that recipient's expertise. Use one recipient per document unless a multi-role design is explicitly requested.

3. Order most important first and group by theme only when useful. Every question covers one idea with an answer stub; explain why only when ambiguity would invite a throwaway response.

4. Include purpose, sender/recipient, context, how answers will be used, actual deadline/effort if known and permission for partial answers or 'I don't know'.

5. Write a local Markdown draft, preserve edits and report its path. Check coverage from gap to question; do not pretend static questions adapt to answers.

6. Delivery by email/chat/tracker is separate and requires explicit messaging authority. Returned answers become inputs to the same accepted decision process.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Each required gap is covered, tone matches recipient knowledge, document stands alone and no unstated deadline or delivery action is invented.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Draft questions for our platform owner about launch capacity and retention.”

Negative request: “Send this questionnaire to the owner without my instruction.”

Interviewing the sender about unknown subject facts, a giant compound question, copied internal jargon, fictional urgency or automatic sending.

## Fallback

Draft with explicit missing sender/recipient/context slots if non-material; ask only what is necessary to make it usable.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/productivity/to-questionnaire/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
