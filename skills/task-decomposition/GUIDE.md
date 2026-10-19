# Slice work into dependent tasks

Internal method ID: `task-decomposition`. Stable technique adapted to Andino ownership.

## Purpose and selection

Convert accepted scope into independently verifiable vertical slices with genuine blockers.

Activate for: An accepted multi-step build needs bounded task deliverables and dependencies.

Do not activate for: A change already fits one clear slice or an attempt to create another mandatory plan.

## Inputs and dependencies

Accepted spec/current Andino plan, codebase structure, interface constraints and task verification obligations.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Read the source spec and existing graph in full, including relevant comments. Inspect the actual repository before assigning paths or interfaces. Reuse completed work and accepted task IDs; retain source pointers for verified signatures and mark unresolved ones explicitly.

2. Draft narrow complete paths through necessary layers, each with demoable behavior and verification fitting a focused context. Fold setup/docs into the behavior they support.

3. Do needed prefactoring first. For wide mechanical changes use expand, migrate bounded caller batches, contract after every caller migrates; allow a final integration gate where standalone batches cannot stay green.

4. Assign real blocking edges, not perceived importance. Record verified inputs/outputs/interfaces and falsifiable acceptance observations; each criterion must be meaningful at that task's start. If an interface is unresolved, keep the consumer blocked behind the task or inspection that will establish it.

5. Review granularity and overlapping shared files. An existing approved breakdown does not require repeated approval; ask about material scope/ownership ambiguity.

6. Write one local task artifact per ticket or update the existing plan convention. Publish remote tickets only when authorized, blockers first, real sub-issues/native dependencies where supported, textual fallback otherwise.

7. Work the ready frontier inside Andino. Keep the breakdown inside the existing plan/checkpoint and maintain its single `NEXT ACTION`. A parent issue/spec is context, not a duplicate AFK work item; do not silently close or modify it.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Every task has a demo/observable output, criteria fail when behavior is absent, graph is acyclic and prerequisites are actual gates.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Slice the accepted rename into expand, caller migrations and contract tasks.”

Negative request: “Make twelve tickets for this one-line typo.”

One task per layer with no demo, twelve tickets for three lines, duplicated shared board files, fake placeholder IDs or criteria another task alone can satisfy.

## Fallback

Keep a local reviewable graph when tracker access is unavailable. Serialize overlapping files even when conceptual tasks appear independent.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/to-tickets/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
