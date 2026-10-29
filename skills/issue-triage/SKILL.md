---
name: andino-issue-triage
description: A maintainer requests evaluation of incoming issues or opted-in external PRs. Operates under Andino Workflow governance.
---

# Triage an incoming issue

Internal method ID: `andino-issue-triage` (alias: `issue-triage`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Turn inbound reports into verified, durable next-action briefs under the project's tracker conventions.

Activate for: A maintainer requests evaluation of incoming issues or opted-in external PRs.

Do not activate for: Already accepted implementation tasks, self-generated tickets needing no new triage, or unauthorized bulk tracker changes.

## Inputs and dependencies

Selected full issue/PR body/comments/labels/author/dates/diff, scope policy, role mapping, relevant code and prior triage notes.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Use cheap oldest-first discovery only for selection: unlabeled, needs-triage, and needs-info with a reporter response. Opt-in external PR discovery excludes maintainers' in-flight work; explicitly named PRs can be inspected.

2. Read full context and prior notes before judging. Every item needs one category (bug/enhancement) and one mapped triage state; conflicting states are a material maintainer decision.

3. Check project scope and conceptual rejection records. A prior rejection is surfaced with its reason, never mechanically keyword-matched as the same request.

4. Boundedly verify the report's exact claim or PR behavior using safe local commands. Reuse existing repro evidence; escalate deep debugging only when warranted, or request specific missing information.

5. Interview only material gaps. Prepare an agent brief: current and desired behavior, interfaces/invariants, concrete acceptance criteria and out of scope; describe remaining work on an existing PR rather than rebuilding it.

6. Prepare recommended transition or needs-info notes. Rejected enhancements may earn a concept-level rejection record; already implemented work links the implementation and never poisons the rejection knowledge base.

7. Only with explicit external-write authority post comments, labels or closes. Prefix triage-generated external prose with the project's required AI disclaimer. Andino owns task lifecycle and final acceptance.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Recommendation cites full evidence, one category/state is consistent, claim verification is observed or explicitly unavailable, brief criteria can be checked.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Evaluate this incoming bug with its comments and draft a brief.”

Negative request: “Re-triage all the ready tickets we just approved.”

Bulk listing treated as full context, re-asking answered questions, label conflicts ignored, or closing an already-built enhancement as a permanently rejected concept.

## Fallback

Produce local draft triage/brief artifacts without tracker mutation. Missing repro access results in bounded needs-info evidence, not a fabricated root cause.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/triage/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
