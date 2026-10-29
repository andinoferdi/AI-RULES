---
name: andino-environment-retrospective
description: Established failure causes and an explicit prevention retrospective; unknown causes go to session-diagnostics first. Operates under Andino Workflow governance.
---

# Improve the working environment

Internal method ID: `andino-environment-retrospective` (alias: `environment-retrospective`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Turn observed session failures into proportionate improvements to navigation, checks and review context.

Activate for: An explicit retrospective or repeated evidenced friction worth preventing.

If the cause of the repeated failures is still unknown, select session-diagnostics
first. Use this retrospective once the failure evidence and causes are established
and the current need is prevention; do not collapse diagnosis and future safeguards.

Do not activate for: A smooth trivial task or an excuse to rewrite global instructions or unrelated code.

## Inputs and dependencies

Selected session evidence, existing check scripts/CI/hooks, standards/navigation docs and current write scope.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Read the selected actual session or narrowly scoped log; default to current work if requested generally. Use agent-document-authoring concepts before judging steering files.

2. For each candidate cite the concrete failure, its consequence and existing safeguard. Inspect actual check commands and wiring before proposing another tool.

3. Mechanical mistakes earn a deterministic lint/type/test/CI check when justified. A check already present but unwired is a wiring finding. Judgment calls belong in review standards.

4. Look for hidden dependencies, missing navigation, expensive repeated calls, inaccessible diagnostics, stale/no-op steering and duplicated facts. Distinguish tactical completion from strategic future improvement without interrupting current work.

5. Rank candidates by impact and cost; allow none. Recommend removal of harmful or obsolete instructions, not endless accumulation of prose.

6. Apply only authorized local improvements; access grants, global files, hooks and scheduled monitors require their own authority. Verify a new check both rejects the failure and accepts a valid case.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Every suggestion traces to observed session evidence; actual tooling was checked; a proposed new guard has discriminating positive/negative behavior.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “The repeated failure causes are already established in the session log. Inspect the existing checks and propose guardrail improvements.”

Negative request: “Change one typo in the README.”

Generic category-filling advice, 'always improve environment first', all work delegated by rule, or adding another AGENTS line for a mechanical violation.

## Fallback

Produce an evidence-backed recommendation without edits where scope is read-only. No memory service or recurring schedule is required.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/retro/SKILL.md`
- `mattpocock/skills:skills/in-progress/chief-of-staff/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
