---
name: andino-project-configuration
description: A project needs an explicit tracker mapping, domain-doc convention or triage vocabulary. Operates under Andino Workflow governance.
---

# Configure project workflow documents

Internal method ID: `andino-project-configuration` (alias: `project-configuration`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Make optional tracker/domain/triage conventions explicit without installing a second workflow.

Activate for: A project needs an explicit tracker mapping, domain-doc convention or triage vocabulary.

Do not activate for: Ordinary Andino use, mandatory setup before every engineering task or global host configuration.

## Inputs and dependencies

Actual remote, existing instructions/config, tracker choice and granted write scope, label inventory and domain-doc conventions.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Inspect existing remote, tracker docs, instruction pointers, glossary/map/ADRs and prior configuration. Preserve current conventions and user edits.

2. Choose actual supported tracker operations: GitHub, GitLab, local Markdown or a documented custom adapter. Record read/list/create/comment/link/block/claim/resolve semantics and which operations are unavailable.

3. Map canonical triage roles to existing label strings; category and state are separate. Missing external labels are a reported requirement or explicitly authorized operation, never automatic setup.

4. Use a single glossary by default; a real multi-context repo may use a map. Domain docs are lazy and do not become a prerequisite for unrelated methods.

5. Prepare local reviewable tracker/domain/triage docs and one pointer in the instruction file the active host actually reads. Merge an existing block in place rather than duplicate it; no upstream SKILL edits.

6. Verify local behavior and native-blocking fallback. External operations need separate explicit authority; local configuration is optional and Andino remains lifecycle owner.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-project-configuration` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Consumer methods can locate the correct tracker/domain vocabulary, unknown operations are explicit, existing config and instruction content remain intact.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Prepare local tracker and triage vocabulary docs using our existing conventions.”

Negative request: “Install another workflow globally before doing anything.”

Installing Matt plugins, silently defaulting to gh, editing CLAUDE solely because it exists on another host, creating labels without authority or overwriting existing blocks.

## Fallback

Use local drafts and textual blocker edges when remote tools are unavailable. Record custom tracker operations as inspected prose rather than invented CLI syntax.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/setup-matt-pocock-skills/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
