---
name: andino-handoff
description: Work moves to another host/directory/person or requires an explicit portable continuation. Operates under Andino Workflow governance.
---

# Prepare a portable handoff

Internal method ID: `andino-handoff` (alias: `handoff`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Let another context continue from verified artifacts and a concrete next action.

Activate for: Work moves to another host/directory/person or requires an explicit portable continuation.

Do not activate for: Routine continuation in the same context with enough room, or duplicating the existing Andino checkpoint.

## Select a resource, not a second lifecycle

Load only the resource matching the current need. A direct resource selection uses
that procedure and current authority; it does not run this parent's other modes,
reopen accepted requirements or require a second execution plan.

| Current need | Resource | Exclusion |
| :--- | :--- | :--- |
| Context window budgeting, prompt packing, attention discipline | [context-packing](resources/context-packing/guide.md) | Standard short sessions within normal context capacity |

## Inputs and dependencies

Existing checkpoint/spec/diff/test evidence, destination focus, permissions, current revision/dirty state and durable artifact paths.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Choose the boundary and recipient. Continue in place when the same context can
   take the next step. For a portable continuation, identify the recipient's
   assignment, destination, and authorized scope from the request and current
   checkpoint. If several assignments are possible, label the recommended one.
2. Collect the sources needed for that assignment. Lead with the authoritative
   checkpoint and active section, then link the spec, changed code or research,
   and verification evidence where the next step needs them. Use destination-
   relative paths with a named root or accessible URLs. Preserve the reason for
   each decision that constrains the recipient, including rejected approaches
   they could plausibly repeat.
3. Identify the state being transferred. For repository work, record the branch,
   base revision, and whether relevant edits are staged, unstaged or untracked.
   Give a reachable pointer to the exact work in progress and its prerequisites.
   If any required bytes exist only on the source host, identify what is missing
   and make obtaining it the first action. For non-repository work, identify the
   document revision or other observable source state.
4. Write the handoff using the output contract below. Separate observed results,
   pending checks and assumptions. Redact credentials, private data and session
   tokens from the handoff and any transferred attachments. Suggested methods
   use internal IDs and are conditional on the recipient's available capabilities.
5. Check the artifact from the destination's perspective. Resolve the first
   pointer against the destination root, confirm the expected revision and
   access, and trace the first action to its expected signal. Label any access
   you could not check and give the recipient the narrowest way to resolve it.
   Choose durable storage for cross-host use and keep the authoritative
   checkpoint as the owner of progress.
6. Deliver the artifact with its location and the first action. Use a supported
   continuation adapter only within current authority. Pass the file as data
   through a structured interface and keep summary text out of shell commands.
   Otherwise give the recipient a manual start from the handoff file.
7. On receipt, compare the relevant destination state and project rules with the
   recorded baseline. Recheck only the evidence invalidated by drift, then
   resume the first action and update the authoritative checkpoint.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-handoff` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Use these sections in order. Keep entries proportional to what the recipient
needs for the assignment.

- **Resume here** gives the outcome, recipient assignment, current phase and
  checkpoint path with the relevant section.
- **Current state and evidence** identifies the transferred revision or work in
  progress, what was actually checked, and what is pending. Link evidence with
  a short explanation of what it establishes.
- **Decisions and boundaries** captures material rationale, ownership and
  permissions that constrain the next step.
- **NEXT ACTION** names one file, command or source to start with, where to start,
  and the expected signal. When blocked, name who can unblock it, the missing
  input and the observable condition for resuming the intended action.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Prepare a portable handoff for a colleague in another checkout.”

Negative request: “Keep working in this context on the next ready step.”

A confident unverified 'done', duplicate plan, vanished temp pointers, shell-expanded summary or automatic new host/background task without authority.

## Fallback

Write a file-based handoff and report sequential/manual mode if host continuation is unavailable.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/ask-matt/SKILL.md`
- `mattpocock/skills:skills/productivity/handoff/SKILL.md`
- `mattpocock/skills:skills/in-progress/claude-handoff/SKILL.md`

Snapshot identities and licensing are recorded in [references/license.md](references/license.md). Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
