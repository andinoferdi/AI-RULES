---
name: andino-deep-module-design
description: A known module interface is hard to use, hard to verify or spreads changes across callers. Operates under Andino Workflow governance.
---

# Design a deep module

Internal method ID: `andino-deep-module-design` (alias: `deep-module-design`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Concentrate behavior behind a small useful interface at a justified seam.

Activate for: A known module interface is hard to use, hard to verify or spreads changes across callers.

Do not activate for: A request for a whole-codebase survey or speculative abstraction without observed friction.

## Inputs and dependencies

Actual callers and obligations, observable behaviors, current tests, domain terms, relevant ADRs and dependency facts.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Describe the module, interface and implementation separately. Interface means signatures plus invariants, ordering, errors, configuration and performance obligations; depth means caller leverage, never a line-count ratio.

2. Apply the deletion test: if the module disappears, does complexity vanish or return in every caller? Identify evidence of leakage, scattered changes and tests reaching through private parts.

3. Choose the external seam callers and tests should cross. Hide internal organization unless something genuinely varies. Name the second concrete adapter before introducing a port; a single hypothetical adapter earns no indirection.

4. Classify each dependency: pure in-process; locally substitutable infrastructure; remote-but-owned transport behind a port; true third-party dependency behind an injected external adapter. Prefer real local stand-ins where useful.

5. For a consequential interface choice, frame constraints and compare radically different designs: minimal entrypoints, maximum extension, common-caller simplicity, optionally ports/adapters. For each give signatures, invariants, ordering/errors, usage, hidden behavior and dependency strategy.

6. Recommend using depth, locality and seam placement. Implement only within accepted scope; prove new public-interface tests preserve behavior before removing superseded shallow tests. Keep internal seams private.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

A real caller can exercise the required behavior without internal knowledge; dependency strategy is testable and justified; no coverage disappears during test replacement.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Callers repeat order policy in six places. Compare smaller interfaces.”

Negative request: “List all files in the repository.”

A pass-through wrapper, implementation-line padding, giant barrel export, port with no real variation, or deleting old tests before equivalent interface coverage.

## Fallback

Compare designs sequentially when delegation is unavailable. If the interface is already sound, record no change rather than invent depth work.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/codebase-design/SKILL.md`
- `mattpocock/skills:skills/engineering/improve-codebase-architecture/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
