# Prepare a portable handoff

Internal method ID: `handoff`. Conditional adaptation: use only for the concrete requested context; upstream beta/frozen status does not imply general readiness.

## Purpose and selection

Let another context continue from verified artifacts and a concrete next action.

Activate for: Work moves to another host/directory/person or requires an explicit portable continuation.

Do not activate for: Routine continuation in the same context with enough room, or duplicating the existing Andino checkpoint.

## Inputs and dependencies

Existing checkpoint/spec/diff/test evidence, destination focus, permissions, current revision/dirty state and durable artifact paths.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Decide at a natural boundary whether continuation suffices. Clear only irrelevant context, compact only where necessary and supported; a portable file is useful when something actually travels.

2. Reference existing artifacts by exact accessible path/URL rather than copying specs/plans/diffs. Preserve why decisions were made and distinguish observed evidence from assumptions.

3. Record current state, active phase, accepted decisions, unresolved blockers, edit ownership/permissions and the first concrete safe next action.

4. Redact credentials, private data and session tokens. Suggested methods are internal method IDs, not mandatory upstream Skill calls.

5. Choose a destination that survives the handoff: OS temp may be useful for immediate transfer but is not durable across reboot/host changes. Preserve the authoritative checkpoint and ensure referenced files are reachable.

6. Use a current authorized host delegation/continuation adapter only when genuinely supported; never interpolate summary text into a shell or hardcode claude --bg. Otherwise deliver the file for manual use.

7. Recipient checks repository drift and evidence before resuming, rather than re-auditing unchanged completed phases.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

A cold reader can locate evidence and the next action without chat history; references survive the destination and permissions remain explicit.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Prepare a portable handoff for a colleague in another checkout.”

Negative request: “Keep working in this context on the next ready step.”

A confident unverified 'done', duplicate plan, vanished temp pointers, shell-expanded summary or automatic new host/background task without authority.

## Fallback

Write a file-based handoff and report sequential/manual mode if host continuation is unavailable.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/ask-matt/SKILL.md`
- `mattpocock/skills:skills/productivity/handoff/SKILL.md`
- `mattpocock/skills:skills/in-progress/claude-handoff/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
