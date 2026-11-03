# Prepare a human-only procedure

Internal method ID: `human-procedure`. Stable technique adapted to Andino ownership.

## Purpose and selection

Make manual prerequisite steps concrete, resumable and safe without asking the agent to handle secrets.

Activate for: A required step needs human dashboard access, secret entry or another action the agent cannot perform.

Do not activate for: A task the agent can already safely execute or generic setup guidance with no human-only prerequisite.

## Inputs and dependencies

Verified manual journey, named stages, input sources/destinations/secrecy, current shell and authorized local/external operations.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. **Scope the handoff.** Identify current and target state, account, project,
   environment and the human-owned actions. Inspect config schemas, examples
   and CI references for names only. Map each stage's value from source to
   approved destination and consumer, with its sensitivity. Include actions
   that produce no value. Resolve consequential unknowns before authoring
   executable steps and carry forward existing decisions and authority.
2. **Map the journey.** Use one outcome per stage. Start with Stage N of M,
   purpose, prerequisites and a verified URL or command. Give the exact click
   path or command, what to select or enter, and the observable success signal.
   Show the URL before requesting input and provide a manual-open path. Verify
   labels against current sources or the user's view. If a path is unknown,
   name the missing observation and stop dependent steps there.
3. **Choose the format.** Use a checklist for short or dashboard-only tasks
   and when secure automation is unavailable. Use a native-shell wizard when
   requested and guided prompts or safe persistence add value. Preview the
   effects, show one stage at a time and offer a way to stop. Keep one-off
   artifacts in an agreed scratch location. A reusable repository artifact
   requires separate scope.
4. **Protect inputs and effects.** Use hidden terminal input for script-collected
   secrets. Keep values out of chat, logs, command arguments and checkpoints.
   For dotenv writes, preserve unrelated bytes and existing permissions, reject
   symlinks and paths outside the agreed directory, and use a safe idempotent
   update. Fall back to human entry when those guarantees cannot be established.
   Name exact external targets and require explicit authority for writes.
   Describe irreversible effects and require affirmative confirmation at the
   point of action.
5. **Make progress resumable.** Record stage status and applied effects using
   names only. Cancellation, EOF or failure leaves the current stage incomplete
   until its success signal is observed. On resume, recheck target and signals,
   reuse saved values privately and reconcile ambiguous effects before retrying.
   Never replay a completed irreversible action.
6. **Verify and hand off.** Trace each input to its destination and consumer.
   Check target-shell syntax and test safe local branches with disposable data.
   Leave live interactive steps to the human. Provide the exact run location
   and command or first checklist action, intended effects, pending stages and
   next action. Request only non-sensitive evidence of completion.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-human-procedure` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations, external messages/tracker writes, credentials, global setup, deployments and recurring jobs require their actual authority. A source example never grants it. Preserve user edits, secrets and current staging.

## Outputs and verification

Stages are concrete, values have correct secrecy/destinations, syntax/data flow are checked, restart behavior is explicit and no secret reaches logs/model context.

Apply the worked example to observe an artifact and independent expected outcomes. Its deterministic result proves only that bounded procedure; it does not prove model routing, live host parity or optional external tool execution. Record actual command/tool, current content identity, result and unresolved limits before claiming success.

## Example and anti-patterns

Positive request: “Prepare exact manual steps for the credential dashboard I must access myself.”

Negative request: “Paste my secret into the chat and configure it for me.”

Blind upstream Bash copy, follow-symlink credential rewrite, plaintext terminal echo, recording tokens in evidence or executing gh secret set as implicit setup.

## Fallback

A precise human checklist is sufficient when no suitable interpreter exists. Mark dashboard/UI paths unverified if current evidence is unavailable.

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never reads or installs those repositories):

- `mattpocock/skills:skills/engineering/wizard/SKILL.md`

Snapshot identities and licensing are recorded in the package provenance/legal records ([references/license.md](references/license.md)). Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
