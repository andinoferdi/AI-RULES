# Prepare a human-only procedure

Internal method ID: `human-procedure`. Stable technique adapted to Andino ownership.

## Purpose and selection

Make manual prerequisite steps concrete, resumable and safe without asking the agent to handle secrets.

Activate for: A required step needs human dashboard access, secret entry or another action the agent cannot perform.

Do not activate for: A task the agent can already safely execute or an unrequested setup wizard.

## Inputs and dependencies

Verified manual journey, named stages, input sources/destinations/secrecy, current shell and authorized local/external operations.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It is local and self-contained. Optional project tools are discovered when needed, never installed merely to load this method.

## Procedure

1. Inspect safe configuration names and CI references, not secret values, to discover prerequisites. Name every stage in dependency order and each produced value's source, destination and secret/public classification.

2. Use actual current documentation or user-confirmed dashboard journeys. Never invent a UI path, provisioning command or irreversible cutover step.

3. Prepare a local reviewable checklist or native-shell script with stage progress, open-before-request instruction, hidden secret input, explicit confirmation before irreversible actions and no secret echo.

4. Keep credentials in the human's terminal/environment and storage approved for them; never ask the user to paste secrets into chat. Persist only needed values with path/permission checks and safe idempotent update.

5. Preserve existing dotenv bytes/permissions and reject a symlink or destination escaping the agreed directory. External secret/variable writes are separate actions needing explicit authority.

6. Statically trace every input to its intended destination, check script syntax with an available interpreter and report skipped dependencies. Do not run an interactive wizard end-to-end as the agent.

7. Hand over exact run instructions and summary of intended effects. Reuse saved values only without revealing them; cancellation/restart must not claim a stage completed.

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, one durable plan/checkpoint, delegation, permission decisions and final acceptance. This guide contributes the selected technique; it is not a native skill, router or second lifecycle. Current user/project contracts and accepted decisions override upstream defaults. Focus owns communication; Search First owns required external solution research; existing domain/UI sibling ownership and manual-only/denied controls remain authoritative.

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

Snapshot identities and licensing are recorded in the package provenance/legal records. Upstream bootstrap, automatic commit/push, hooks and installers are not imported as authority.
