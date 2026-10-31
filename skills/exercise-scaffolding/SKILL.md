---
name: andino-exercise-scaffolding
description: An explicit exercise/course-section scaffolding or renumbering request. Operates under Andino Workflow governance.
---

# Scaffold a course exercise

Internal method ID: `andino-exercise-scaffolding` (alias: `exercise-scaffolding`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Create a coherent numbered learning exercise with meaningful content and verifiable structure.

Activate for: An explicit exercise/course-section scaffolding or renumbering request.

Do not activate for: Creating unsolicited course material or installing a proprietary linter as a prerequisite.

## Inputs and dependencies

Course plan, naming conventions, requested variants, meaningful content and available validation commands.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Parse sections/exercises and variants from the accepted plan. Reuse existing numbering/conventions; default a readme-only stub to explainer only when the plan leaves variant open.

2. Create section XX-name and exercise XX.YY-name under the course convention. Each exercise needs problem or explainer as a primary accessible variant; solution alone is insufficient.

3. Write meaningful non-empty readme content and valid local links for each variant. Code variants require the actual course entry file (upstream main.ts convention); readme-only exercises do not.

4. Respect course exclusions such as no .gitkeep, speaker-notes or obsolete run instructions. Do not fabricate full teaching content from a title when only scaffolding was requested.

5. Validate with an actually installed course linter where available; otherwise check directory/README/link/entry invariants locally and name that narrower coverage.

6. For moves/renumbering preserve files and references, confirm collisions before mutation and verify afterward. No git mv/stage/commit occurs automatically.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-exercise-scaffolding` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Requested variants/content exist, numbering is consistent, readme links resolve and code-entry requirements match actual course configuration.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Scaffold section 05.02 with explainer, problem and solution variants.”

Negative request: “Install a course CLI globally to answer one question.”

Empty title-only placeholders presented as lessons, solution-only exercises, overwriting existing directories, fake linter success or automatic commits.

## Fallback

Use filesystem/link checks and explicitly report ai-hero-cli NOT VERIFIED when unavailable; no mandatory network/package install.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/misc/scaffold-exercises/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
