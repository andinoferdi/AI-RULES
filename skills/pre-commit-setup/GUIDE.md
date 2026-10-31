# Prepare project pre-commit checks

Internal method ID: `pre-commit-setup`. Conditional adaptation: use only for the concrete requested context; upstream beta/frozen status does not imply general readiness.

## Purpose and selection

Wire existing project quality checks without disturbing staging or replacing established hooks.

Activate for: An explicit request for commit-time formatting/checks or an evidenced missing guardrail.

Do not activate for: Committing work, global installation or running staged-file mutations on the user's index without authority.

## Inputs and dependencies

Detected package manager, package scripts, existing hooks/prepare script/formatter config and project scope.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Inspect lockfiles and actual scripts/config. Identify existing hook tooling before selecting optional Husky/lint-staged/Prettier.

2. Prepare devDependency changes with the detected manager only when authorized. Preserve existing prepare behavior; combine or use current hook mechanism rather than overwrite.

3. Run staged-only formatter first, then existing typecheck/tests where appropriate. Missing scripts are omitted with an explicit limitation, never fabricated.

4. Reuse formatter config; create one only if absent and requested scope permits. Preserve ignore rules and hook contents, inserting the smallest necessary calls.

5. Verify in a disposable fixture or isolated index with explicit scope; lint-staged may write files/stash/index state and is not read-only.

6. Check hook execution/command failures without a commit. A later real commit remains separately authorized.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-pre-commit-setup` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Existing hook/prepare/config behavior is preserved, intended checks execute/fail properly in isolation and user staging is unchanged.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Prepare project pre-commit checks while preserving prepare and current staging.”

Negative request: “Stage everything and make a smoke commit without permission.”

npx husky init blindly overwriting prepare, replacing formatter style, stage-all smoke commits or claiming a hook exists means it works.

## Fallback

Produce an integration patch/checklist using current toolchain when optional packages are absent; mark actual package/hook execution NOT VERIFIED.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/misc/setup-pre-commit/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
