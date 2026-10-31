# Classify Git operation authority

Internal method ID: `git-operation-guard`. Conditional adaptation: use only for the concrete requested context; upstream beta/frozen status does not imply general readiness.

## Purpose and selection

Recognize publishing/destructive Git intent under the actual host permission boundary.

Activate for: An operation would publish, discard, rewrite or stage repository state, or an optional guard is explicitly requested.

Do not activate for: Treating an upstream regex hook as a complete security control or installing global hooks automatically.

## Inputs and dependencies

User authorization, exact proposed Git operation, current repository state and host permission mechanisms.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Identify semantic effect: read-only inspection, local reversible edit, staging/commit, publish, history rewrite or discard. Check current user/project authority before any mutation.

2. Treat global options such as git -C path and reordered flags as still the same operation. A textual substring search is advisory and cannot secure arbitrary shell commands.

3. Prefer the host's actual tool/permission enforcement. If a project hook is explicitly requested, preserve existing settings and restrict to that scope; never install globally from a method trigger.

4. Any optional command parser must fail closed on malformed input/unsupported syntax/missing dependencies, reject known dangerous forms and state shell/alias/wrapper limitations.

5. Verify safe and rejected fixtures without running actual push/reset/clean. Include global-option and malformed-input cases. A model permission check remains required even if a hook accepts.

6. Keep original Git state/user work untouched. Request material permission only when absent, and honor explicit prohibitions without an alternative invocation.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-git-operation-guard` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

No denied action is performed, known destructive/publishing operations are recognized across supported forms, and unsupported syntax cannot be called safe.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Review whether git -C repo push is allowed by the current authority.”

Negative request: “Install the upstream global regex hook automatically.”

Copying the Bash/jq grep hook, missing-jq fail-open, pretending regex handles aliases/shell grammar or using another tool to bypass denial.

## Fallback

Do not execute an unclassifiable mutation; present the exact operation/effect for an authority decision. Read-only inspection can continue.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/misc/git-guardrails-claude-code/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
