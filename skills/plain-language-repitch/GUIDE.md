# Re-explain a confusing message

Internal method ID: `plain-language-repitch`. Stable technique adapted to Andino ownership.

## Purpose and selection

Restore shared understanding by adding missing context and concrete domain language.

Activate for: The user says the last explanation did not land or asks what a technical message means.

Do not activate for: A new research/implementation task, a request to learn a new concept, or an opportunity to change project files. Quick learning can stay in the current conversation; `learning-workspace` owns intentional learning across sessions.

## Inputs and dependencies

Previous message, user's confusion, already known context and relevant existing glossary terms.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Identify the main point the user needs and the missing context in the previous explanation. Use existing evidence; do not begin a new investigation by default.

2. Lead with the practical outcome in familiar words and add one concrete example. Introduce necessary terms before using them, with the project's established vocabulary.

3. State consequential assumptions plainly and remove unexplained process jargon, abbreviations and incidental detail. Simplified language must retain the original technical meaning.

4. Follow Focus communication ownership and the user's language/tone. Check the reply actually answers the confusion; ask a narrow follow-up only if needed.

5. Continue the original authorized task after clarification; repitching grants no file-edit, tool, host or external-write authority.

If clarification reveals a different learning goal, answer the new concept directly or use the quick-learning branch. Do not turn explanation repair into persistent teaching unless the user asks for that.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-plain-language-repitch` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

The corrected explanation preserves the original claim while giving enough context to understand its consequence.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “I do not understand your last message about task blockers. Explain plainly.”

Negative request: “Research a new unrelated framework.”

Restating the same jargon, changing the factual answer to simplify it, adding unsolicited warnings or editing files during a communication repair.

## Fallback

Use a short concrete analogy or example with an explicit limit. No special tool or corpus is required.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/productivity/wait-what/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
