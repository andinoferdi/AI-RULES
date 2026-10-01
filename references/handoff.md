# Resume without chat history

1. Read the Executive Snapshot and NEXT ACTION first, then the active phase and
   only the referenced context needed to execute it.
2. Inspect current relevant artifacts, source freshness and environment state.
   For repository work, check working directory, branch/status and relevant changed
   files; a recorded commit alone does not prove an uncommitted checkpoint exists.
   For research or daily work, check the referenced document, data, source or task
   state instead. Do not require Git or a repository where none is involved.
3. Compare current evidence and previous verification with CURRENT STATE. Treat
   conflicting current evidence as drift; amend only affected plan facts/phases.
4. Read applicable project constraints that are not already loaded.
5. Resume NEXT ACTION. Do not repeat initialization, investigation, or verification
   already supported by current evidence. Reopen DONE phases only with conflicting
   evidence and record the revision.
6. Keep the Execution Board, active phase, actual files/evidence and snapshot in
   sync. Checkpoint material progress and leave a concrete next action before stopping.

Resolve authority and factual drift separately. For intent, scope, constraints and
decisions, follow the latest user instruction, project/repository rules and explicit
written decisions/checkpoints before recommendations or old chat. For factual state,
current artifact, source, environment, repository, config and test evidence updates
stale recorded facts but does not silently override those explicit decisions.

The plan plus relevant artifacts must answer WHAT/WHY, what is known and done, material
decisions or deviations, what must not be repeated, and the first next file/symbol
and check, or the next source/decision for non-code work. Do not restart project
bootstrap, reread every source, reconstruct full chat, require claude-mem, or assign
permanent host roles. If an artifact is missing, search its task/name in the relevant
available location (and Git state for repository work) before asking a focused question.

## Compact review views

`PM / REVIEW HANDOFF` and `DEVELOPER HANDOFF` are compact projections of the execution
plan plus current relevant evidence, not plans, lifecycles or independent state stores.
Include only the relevant objective, scope, evidence, blockers, decisions/deviations,
stop condition and NEXT ACTION. Amend durable plan state when the view reveals material
factual drift or a new explicit decision; do not let the handoff silently diverge.
For EPHEMERAL work, answer with the result and necessary evidence or limitation;
do not create a plan or formal handoff merely to end a conversation.

Example NEXT ACTION: `Inspect retryPayment() in src/payments/retry.ts; reuse the
existing idempotency key on retry; run the checkout retry regression test named
in package.json.` Replace examples with repository-verified names and commands.

Non-code example: `Compare the supplied survey's response dates with the revised
research cutoff; update the included-source decision and verify the sample count.`
Use actual referenced artifacts, not hypothetical sources, in a real checkpoint.
