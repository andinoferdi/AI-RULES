# Survey architecture friction

Internal method ID: `architecture-survey`. Stable technique adapted to Andino ownership.

## Purpose and selection

Present evidence-backed deepening candidates without silently redesigning the codebase.

Activate for: A named architecture pain point or bounded request to find maintainability/testability friction.

Do not activate for: A routine feature fix, arbitrary whole-repo scan, or repeated search for findings after no worthwhile candidate.

## Inputs and dependencies

User scope or recent-change hotspots, relevant code/callers/tests, glossary, ADRs and accepted domain owners.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Scope before scanning: use the named subsystem, otherwise infer bounded hotspots from recent history. Read relevant domain terms and ADRs.

2. Trace one concept across actual files, looking for shallow modules, repeated caller policy, leaking seams or awkward public-interface tests. Apply the deletion test to each suspected wrapper.

3. Classify dependencies using deep-module-design. Record concrete files, observed friction and what a deeper interface could concentrate; do not propose a speculative implementation yet.

4. Produce an offline candidate report with before/after visuals, problem, solution direction, locality/leverage, test consequences, dependency category and strength Strong/Worth exploring/Speculative.

5. Flag an ADR conflict only when real evidence justifies reopening it. Recommend one candidate or say none worthwhile. Let the user or already accepted scope select before interface design.

6. Carry the selected candidate into the same Andino plan. Record a durable rejection reason only if it prevents future re-suggestion.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Each candidate has source evidence and meaningful before/after structure; report opens without network dependencies; survey itself changes no product code.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Survey this order subsystem for evidenced deepening opportunities.”

Negative request: “Rename this local variable.”

A CDN-dependent report, automatic interrogation about the first idea, speculative candidate inflation, or reading the entire codebase without a bounded question.

## Fallback

Use a small Markdown table and ASCII diagram when local HTML cannot be viewed. Architecture rescue keeps ownership of fragile-system stabilization.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/improve-codebase-architecture/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
