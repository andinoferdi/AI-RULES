---
name: andino-pr-description
description: Writing or updating a PR description for a concrete diff. Operates under Andino Workflow governance.
---

# Describe a pull request

Internal method ID: `andino-pr-description` (alias: `pr-description`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Make an existing change reviewable through compact explanation, actual evidence and reversibility.

Activate for: Writing or updating a PR description for a concrete diff.

Do not activate for: Creating/publishing a PR without authority or triaging review comments.

## Inputs and dependencies

Current complete diff, originating spec, repository PR template, verified before/after evidence and irreversible effects.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Read the repository PR template and current final scope. Fit the technique into that template; do not overwrite required house sections.

2. Choose the smallest view that explains the change: pseudocode for logic, call tree for control flow, component tree for UI, file tree for ownership, Mermaid for relationships, shaped diff for local changes.

3. Explain concrete trigger and resulting behavior in domain language. Keep visuals beside the claim they support and omit abandoned conversational history.

4. Show before and after evidence from the relevant command or visual comparison. A statement 'tests green' is not an independent observation.

5. Classify reversibility: Git rollback does not undo sent emails, external writes or destructive migrations. State one-way/two-way door and realistic blast radius with unresolved validation.

6. Refresh the body after material changes. Keep this as a local reviewable draft until explicit external-write authority exists.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-pr-description` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

A reviewer can identify behavior, verification and risk from the body; claims refer to current bytes and the house template remains satisfied.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Draft the PR body using the current diff and recorded before/after tests.”

Negative request: “Push my branch without approval.”

A wall of every diagram type, unsupported 'small blast radius', a stale body, or treating body generation as PR publication permission.

## Fallback

Use a plain call tree or shaped text diff when Mermaid is not rendered. Missing evidence is labeled missing, never fabricated.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/pr/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
