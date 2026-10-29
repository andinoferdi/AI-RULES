---
name: andino-typescript-boundary-enforcement
description: An explicitly accepted TypeScript deep-package layout needs deterministic import enforcement. Operates under Andino Workflow governance.
---

# Enforce TypeScript package entrypoints

Internal method ID: `andino-typescript-boundary-enforcement` (alias: `typescript-boundary-enforcement`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Make a chosen package boundary reject deep imports and cycles through an actual project check.

Activate for: An explicitly accepted TypeScript deep-package layout needs deterministic import enforcement.

Do not activate for: Universal folder restructuring or a conceptual interface discussion without a chosen layout.

## Inputs and dependencies

Actual package manager/root/layout, TypeScript resolver config, existing dependency-cruiser/config/check scripts and authorized dependency changes.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Detect real package root and existing config; never infer layout solely from src existence when a different project convention exists. Reuse flat package ownership and root-file entrypoints.

2. Keep all package root files public and all subfolder implementation private. Multiple small entrypoints are valid; avoid a giant barrel. A package's own implementation may import internally.

3. Adapt five actual rules: app→package only root; other-package→package only root; tests→any package only roots or own tests fixtures; tests folders private from non-tests; no cycles.

4. Merge into existing boundary config and actual umbrella checks with inspected resolver settings. Do not invent path aliases or change tsconfig merely to fit the recipe.

5. Provide a copyable small example only where requested. Wire the available project tool with authorized devDependency changes; no global install or auto-commit.

6. Prove a valid graph passes, a deep test import fails, restore passes, and applicable app/cross-package/fixture/cycle negatives fail. Use a disposable fixture or reversible owned edit, never overwrite user files.

7. Document actual conventions and a short pointer from existing instruction docs. Record external tool execution separately from the local graph model example.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Rules reject the intended violations and accept valid entrypoint/fixture/intra-package cases; clean/fail/restored-clean observations exist under real tool when installed.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Enforce our selected package entrypoint rules and prove deep imports fail.”

Negative request: “Reorganize every TypeScript project into this layout by default.”

Saying four rules while omitting tests privacy, root-only giant barrel, regex config untested, arbitrary new package structure or model-only proof claimed as dependency-cruiser execution.

## Fallback

Use the stdlib graph exercise for rule semantics and mark dependency-cruiser/TypeScript resolver live execution NOT VERIFIED until available and authorized.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/in-progress/setup-ts-deep-modules/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
