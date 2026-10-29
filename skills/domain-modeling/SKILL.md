---
name: andino-domain-modeling
description: Overloaded domain terms, contradictory code/user vocabulary, or a meaningful architecture decision. Operates under Andino Workflow governance.
---

# Sharpen domain terms

Internal method ID: `andino-domain-modeling` (alias: `domain-modeling`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Keep domain concepts and durable decisions precise while the work develops.

Activate for: Overloaded domain terms, contradictory code/user vocabulary, or a meaningful architecture decision.

Do not activate for: Merely reading existing glossary terms or adding generic programming definitions.

## Inputs and dependencies

Relevant glossary or glossary map, actual code examples, existing ADR location/conventions and decisions made by the user.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Read a root glossary map first if present, then only relevant context glossaries and ADRs. Missing documents do not block ordinary work; create them lazily when an actual resolved term or decision exists.

2. Challenge an overloaded word with a concrete scenario and check the code. 'Account' may mean customer organization or login identity; never collapse distinct concepts by picking a fashionable synonym.

3. Resolve a canonical domain term and avoided aliases with the user or accepted source. Write a tight one- or two-sentence definition inline. Keep implementation recipes, specs and activity notes outside the glossary.

4. Stress-test relationships with a concrete edge case such as partial cancellation, duplicate payment or cross-context ownership. Surface code/statement contradictions as decisions rather than quietly treating one as true.

5. Record an ADR only when a real trade-off is hard to reverse and surprising without context. Reuse the project's location/template; otherwise a numbered title plus context/decision/reason paragraph suffices.

6. Update resolved terms immediately, preserve user edits and link contextual glossaries where multiple bounded contexts genuinely exist. Store operational progress in Andino's checkpoint.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Every canonical term names a real domain distinction, aliases are consistent, implementation details stay outside the glossary, and qualified decisions retain their reason.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Customer and account mean different things in code and our glossary. Resolve them.”

Negative request: “Run the existing test suite.”

An agent-invented unreviewed glossary, a glossary that becomes a spec, an ADR for every reversible choice, or rewriting an existing house ADR format.

## Fallback

Use established code vocabulary and flag an unresolved material term. No domain-document ceremony is required for a small clear edit.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/domain-modeling/SKILL.md`
- `mattpocock/skills:skills/engineering/grill-with-docs/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
