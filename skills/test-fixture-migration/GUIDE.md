# Migrate TypeScript test fixtures

Internal method ID: `test-fixture-migration`. Conditional adaptation: use only for the concrete requested context; upstream beta/frozen status does not imply general readiness.

## Purpose and selection

Express partial and intentionally invalid test data clearly without changing the tested behavior.

Activate for: An explicit TypeScript test-fixture assertion problem or requested shoehorn migration.

Do not activate for: Production code, runtime validation, or blanket replacement of every type assertion.

## Inputs and dependencies

Selected test files, fixture intent, current TypeScript/package setup, accepted dependency policy and verified current library API.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Inspect the exact assertion and what behavior the test exercises. Distinguish a valid partial fixture from deliberately malformed input for a negative case.

2. Verify current official API/package compatibility before adopting optional @total-typescript/shoehorn. Reuse installed tooling and the detected manager; dependency changes remain scoped project actions.

3. Replace a valid partial 'as Type' fixture with fromPartial only where it preserves intent; replace deliberate double assertions with fromAny so wrong data remains wrong. fromExact means full object completeness.

4. Use test-only imports and devDependency policy. Do not apply helpers to production or imply they validate runtime data.

5. Keep expected outcomes independent. Run typechecking and affected tests, comparing before/after behavior, including negative cases.

6. Review the diff for removed required setup or accidental weakening. Leave unrelated assertions and user edits untouched.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Affected tests/typecheck pass, malformed cases still test the failure, no production import is added and the optional API was actually verified.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Replace these selected partial test casts without weakening invalid-input cases.”

Negative request: “Use fromAny throughout production request validation.”

Claiming fromAny is type-safe runtime validation, mass regex replacement, changing wrong input into correct input or silently installing dependencies.

## Fallback

Keep explicit test fixture builders or existing assertions if optional dependency is unavailable/unauthorized. The local example checks migration intent, not installed TypeScript compilation.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/misc/migrate-to-shoehorn/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
