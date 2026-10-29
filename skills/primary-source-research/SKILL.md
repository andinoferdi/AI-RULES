---
name: andino-primary-source-research
description: A concrete technical/factual question needs documentation or source investigation. Operates under Andino Workflow governance.
---

# Capture primary-source findings

Internal method ID: `andino-primary-source-research` (alias: `primary-source-research`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Produce bounded findings whose factual claims trace to sources that own them.

Activate for: A concrete technical/factual question needs documentation or source investigation.

Do not activate for: An unresolved user preference, uncited speculative answer, or duplicate research with unchanged valid evidence.

## Inputs and dependencies

Question and scope, Search First ownership, available local/official sources, dates/revisions and existing notes convention.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Define the question and what decision the answer changes. Reuse current verified local evidence before searching; Search First remains the external research owner.

2. Read primary sources: official docs, source code, standards/specifications and first-party APIs. A summary of a source is not its owner. Follow important claims to exact support.

3. Separate observed facts, interpretation and unresolved gaps; record version/date and source location. Cite near each material claim and note contradictions.

4. Write one findings artifact in the existing convention, with a pointer from the consuming task/spec. Avoid write-once notes with no consumer.

5. Delegate bounded reading only if actual authority/tools permit and no nested research spawning occurs. Otherwise read sequentially and say how the work was done.

6. Verify key citations and close on the question, not an arbitrary source count. No fetch/install/auto-update becomes a runtime requirement.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Every conclusion has directly supporting source evidence and scope/date, contradictory or unavailable facts remain explicit, and a task can consume the result.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Investigate the retry contract in official sources and cite findings.”

Negative request: “Decide my personal preference for dashboard colors.”

A confident report from secondary summaries, recursive background agents, a source dump with no conclusion or automatic research branch/push.

## Fallback

Use local checked-in sources and disclose unavailable network/current-version verification. Material facts that cannot be established remain unknown.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/research/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
