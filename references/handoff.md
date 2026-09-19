# Resume without chat history

1. Read the Executive Snapshot and NEXT ACTION first, then the active phase and
   only the referenced context needed to execute it.
2. Inspect current working directory, branch/status and relevant changed files.
   A recorded commit alone does not prove an uncommitted checkpoint still exists.
3. Compare source/config and verification evidence with CURRENT STATE. Treat
   conflicting current evidence as drift; amend only affected plan facts/phases.
4. Read applicable project constraints that are not already loaded.
5. Resume NEXT ACTION. Do not repeat initialization, investigation, or verification
   already supported by current evidence. Reopen DONE phases only with conflicting
   repository evidence and record the revision.
6. Keep the Execution Board, active phase, actual files/evidence and snapshot in
   sync. Checkpoint material progress and leave a concrete next action before stopping.

Resolve authority and factual drift separately. For intent, scope, constraints and
decisions, follow the latest user instruction, project/repository rules and explicit
written decisions/checkpoints before recommendations or old chat. For factual state,
current repository, config, test and system evidence updates stale recorded facts but
does not silently override those explicit decisions.

The plan plus repository must answer WHAT/WHY, what is known and done, material
decisions or deviations, what must not be repeated, and the first next file/symbol
and check. Do not restart project bootstrap, reread every source, reconstruct full chat,
require claude-mem, or assign permanent host roles. If a referenced file is missing,
search its ticket/name and current Git state before asking one focused question.

## Compact review views

`PM / REVIEW HANDOFF` and `DEVELOPER HANDOFF` are compact projections of the execution
plan plus current repository evidence, not plans, lifecycles or independent state stores.
Include only the relevant objective, scope, evidence, blockers, decisions/deviations,
stop condition and NEXT ACTION. Amend durable plan state when the view reveals material
factual drift or a new explicit decision; do not let the handoff silently diverge.

Example NEXT ACTION: `Inspect retryPayment() in src/payments/retry.ts; reuse the
existing idempotency key on retry; run the checkout retry regression test named
in package.json.` Replace examples with repository-verified names and commands.
