# Resume without chat history

1. Read the supplied checkpoint (smallest relevant section if already known).
2. Inspect current working directory, branch/status and relevant changed files.
   A recorded commit alone does not prove an uncommitted checkpoint still exists.
3. Compare source/config and verification evidence with CURRENT STATE. Treat
   conflicting current evidence as drift; amend only affected plan facts/phases.
4. Read applicable project constraints that are not already loaded.
5. Resume NEXT ACTION. Reopen DONE phases only with evidence that invalidates them.
6. Checkpoint material progress and leave a concrete next action before stopping.

Do not restart project bootstrap, reread every source, reconstruct full chat,
require claude-mem, or assign permanent host roles. If a referenced file is missing,
search its ticket/name and current Git state before asking one focused question.

Example NEXT ACTION: `Inspect retryPayment() in src/payments/retry.ts; reuse the
existing idempotency key on retry; run the checkout retry regression test named
in package.json.` Replace examples with repository-verified names and commands.
