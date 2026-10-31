# Answer one design question

Internal method ID: `design-prototype`. Stable technique adapted to Andino ownership.

## Purpose and selection

Make a specific unresolved logic or visual choice concrete without presenting prototype code as production.

Activate for: A design question cannot be answered reliably in conversation alone.

Do not activate for: An already settled implementation ticket, full-app sales demo, or a production feature disguised as throwaway work.

## Inputs and dependencies

One explicit question, accepted prototype scope, project UI owner/conventions, representative safe data and artifact location.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Write the question visibly and select logic/state versus visual layout. State a safe assumption if the branch is obvious; ask only a material ambiguity.

2. For logic, make one self-contained HTML file around a pure portable reducer, state machine or functions. Keep DOM outside the logic. Show readable current state, free-play actions and resettable guided scenarios for happy, awkward and illegal cases.

3. For UI, prefer variants embedded in an existing page with existing context/data fetching. Build three structurally different variants (maximum five), selectable by shareable ?variant= keys and a visibly separate development-only switcher.

4. Arrow-key switching wraps but ignores input, textarea and contenteditable focus. Variants must disagree about layout/hierarchy, not merely color; do not over-share a layout that prevents differences.

5. Use memory or clearly marked scratch persistence. Never connect UI experiments to real mutations. Keep code obviously labeled prototype and trivially runnable, with no speculative abstractions.

6. Observe feedback rather than choosing for the user. Capture the verdict, why and primary-source artifact using current local evidence conventions. Preserve user edits and do not require a new branch/commit.

7. Implement the validated behavior through normal production checks and remove prototype controls from production. The logic decision may survive; the no-tests HTML shell is not production quality.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-design-prototype` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

The question is answered by actual interaction/feedback, logic is separable, scenarios reset predictably and unsafe actions cannot mutate live state.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Make a local state demo to decide whether empty checkout is legal.”

Negative request: “The design is accepted; implement its production behavior.”

Prototyping a whole app, color-only variants, shipping the switcher, real backend writes, unapproved artifact branches or promoting unverified prototype code.

## Fallback

Provide an explicit state-transition table and static layout comparisons when no browser is available, labeling interaction unverified. Existing Taste/Impeccable or other explicit UI owner remains authoritative.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/prototype/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
