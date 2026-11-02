# Write a buildable specification

Internal method ID: `specification`. Stable technique adapted to Andino ownership.

## Purpose and selection

Record the accepted behavior, scope, test seams and constraints without repeating settled discovery.

Activate for: A significant accepted request lacks a buildable specification or its scope has materially changed.

Do not activate for: An existing current approved spec, a small unambiguous edit or a request to explore intent before it is known.

## Inputs and dependencies

Accepted intent/conversation, current repository/config, existing specification convention, relevant ADRs and actual verification commands.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Reuse the current approved spec if sufficient; synthesize known decisions rather than interviewing again. Surface assumptions separately from accepted facts.

2. Only if the request contains independently testable capabilities, write a small capability map first: stable IDs, responsibilities, providers and acyclic dependency direction/build order. Existing approved boundaries satisfy this step.

3. Describe objective/user/problem and solution, success criteria, non-goals and anti-goals. User stories help product behavior but must not be invented to pad architecture work.

4. Record actual stack, project structure, executable build/test/check commands and relevant style example by inspecting the repository. Existing specification tooling/storage owns the format; do not create a duplicate SPEC or task plan.

5. Prefer the highest useful existing public seams. State what each catches and misses, testing prior art and independently observable criteria. Material new seam decisions need resolution; agreed seams are reused.

6. Record interfaces, invariants, ordering, errors, data shape and accepted implementation decisions. Avoid stale line recipes; preserve a decision-rich reducer/schema/state-machine snippet when clearer than prose.

7. List Always/Ask/Never boundaries from actual user/project authority. Update scope and decisions when implementation teaches something; trace downstream tasks/tests back to criteria in the same durable plan.

8. Check builder readiness and open questions. Proceed under existing execution authorization; unresolved consequential user choices remain pending, without a forced extra-turn ceremony.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-specification` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Every criterion is falsifiable and owned by a capability/task, commands are real, scope reflects decisions, map is acyclic when needed and no requirement is invented.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Turn our settled billing discussion into a buildable spec.”

Negative request: “Start the accepted current spec again from scratch.”

A giant speculative user-story list, code before material scope is known, stale duplicate specs, fixed five-file rule or treating the agent-authored spec as extra authority.

## Fallback

For small work use a compact behavior/acceptance note in the existing plan. If commands or dependencies cannot be verified, name them NOT VERIFIED rather than guess.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `addyosmani/agent-skills:skills/spec-driven-development/SKILL.md`
- `mattpocock/skills:skills/engineering/to-spec/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
