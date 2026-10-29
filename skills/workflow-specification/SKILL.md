---
name: andino-workflow-specification
description: An explicit request to design a repeatable workflow or identify a delegable recurring pattern. Operates under Andino Workflow governance.
---

# Specify a recurring workflow

Internal method ID: `andino-workflow-specification` (alias: `workflow-specification`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Describe a recurring pattern precisely without creating schedules or automation implicitly.

Activate for: An explicit request to design a repeatable workflow or identify a delegable recurring pattern.

Do not activate for: Starting a monitor/schedule, replacing Andino lifecycle or forcing AI/checkpoints into every activity.

## Inputs and dependencies

User's actual recurring pattern, tools/channels, desired outcome, constraints and authorized design scope.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Read existing workflow specs/notes and learn the concrete recurring activity. If context is thin, clarify the user's world and terminology before inventing automation.

2. Describe the trigger: event or schedule, choosing an event when it efficiently matches the need. Identify input sources, operations and observable outputs.

3. Identify decisions that truly need a human. Push each checkpoint late enough that a decision-ready brief and linked artifact are prepared first; a brief explains result/why/choice rather than dumping raw output.

4. Specify scope, dependencies, failure/retry/idempotence behavior, permissions and stopping condition. Some workflows need no AI, no checkpoint or no schedule.

5. Write one workflow spec with unresolved material questions explicit. Keep contextual notes separate from the runnable contract and preserve user edits.

6. Check that an implementer can build it without guessing consequential details. Actual scheduling, messaging, access grants or external writes require their own explicit authority.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Trigger/input/output/checkpoint/permissions and failure behavior are concrete; no unanswered material requirement or implied schedule activation remains.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Specify a recurring support-response drafting workflow without activating it.”

Negative request: “Create a scheduled job automatically from this design discussion.”

Designing from generic life advice, mandating AI everywhere, raw-output checkpoints or creating recurring jobs while only specifying them.

## Fallback

Record a manual repeatable procedure and open dependencies when service/tool integration is unavailable. Beta adaptation remains conditional on a concrete request.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/in-progress/loop-me/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
