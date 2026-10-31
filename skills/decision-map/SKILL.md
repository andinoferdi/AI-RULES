---
name: andino-decision-map
description: A destination is clear but several consequential questions cannot be resolved in one context. Operates under Andino Workflow governance.
---

# Map unresolved decisions

Internal method ID: `andino-decision-map` (alias: `decision-map`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Keep a bounded multi-session investigation navigable without confusing decisions with deliverable tasks.

Activate for: A destination is clear but several consequential questions cannot be resolved in one context.

Do not activate for: A small settled feature, routine task list or a second execution plan.

## Inputs and dependencies

Destination, accepted boundaries, existing Andino checkpoint, known decisions, tracker/local artifact convention and user-owned choices.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Name the bounded destination and distinguish planning from authorized execution. An agent-written Notes paragraph never expands permission. If no meaningful uncertainty remains, skip the map.

2. Create a low-resolution index: destination, notes, one-line linked decisions, not-yet-specified in-scope uncertainty, and explicit out of scope. Full decision detail has one home.

3. Create sharp question records with stable real IDs and types: research, prototype, interview, prerequisite task. A task earns a place only by unblocking a decision; it is not a hidden feature build.

4. Wire genuine blockers after IDs exist. Keep unshaped uncertainty as fog; a precise blocked question is already a ticket. Never pre-slice guesses into dozens of downstream questions.

5. Select an unclaimed unblocked question and record ownership within the existing checkpoint/adapter. User decisions require actual answers; AFK research can proceed with allowed tools and no nested spawning.

6. Resolve with answer, evidence and a context pointer; revise invalidated decisions and graduate newly precise fog. Out-of-scope questions leave the frontier with a reason, outside the decision history.

7. Collapse resolved linked decisions into the accepted spec/tasks when ready. The map itself neither declares DONE nor authorizes implementation, branches, remote issue writes or schedules.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-decision-map` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Map has one bounded destination, current frontier and evidence-backed resolutions; no unanswered human choice is silently closed, and duplicate fog/ticket entries are removed.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “We need a multi-session map of open storage decisions and their blockers.”

Negative request: “Build the next already specified API slice.”

Self-granted execution Notes, map tickets reading like production feature slices, deep speculative waterfall charting, stale assumption preservation or fake human feedback.

## Fallback

Use local question files/pointers and serial investigation under one checkpoint. No native tracker dependencies or one-ticket-per-session hard stop is mandatory.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/wayfinder/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
