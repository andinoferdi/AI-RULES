# Delegate disjoint work under parent ownership — supporting contract

## Sparse handoff

Frontier means ready work, not all unchecked tasks. A stale completed producer is unsatisfied. Define interfaces before concurrency. Overlapping reads are safe only against stable/pinned artifact versions.

Worker brief fields: task id and user outcome, accepted spec/plan pointer, exact owned paths, verified consumed/produced interfaces, dependencies, known decisions, open uncertainties, explicit no-nested-agent and mutation boundary, acceptance cases, verification commands/expected signals and report path. Keep source pointers within approved access and include the minimum context needed to act.

Reviewer brief fields: exact base and owned diff, task outcome/spec, acceptance evidence, review scope and non-goals. Return specification compliance and code quality as separate verdicts. Every finding names the affected path/line, observed evidence, consequence and a focused correction. Reviewers do not expand scope or claim execution they did not perform. Parent resolves conflicts, accepts corrections, integrates changes and owns final verification.

Recovery stays in the same parent checkpoint. For a worker failure or missing report, inspect actual status and partial output before deciding whether to continue inline, provide missing context or retry changed work. For a dependency blockage, preserve the block and advance other ready work. For a model-capability mismatch, use an exposed authorized selection if available or fall back to the host default/inline. For overlapping writes, serialize and reconcile actual bytes before accepting either result. After compaction, reload the same plan/checkpoint and verify worker identities, task status and current output before redispatch; completed valid work is reused.

Parent rechecks actual working diff including new files, accepted public seam tests and separate spec/quality verdicts. Scoped re-review covers addressed findings/new breakage, not unrelated polish. Shared unchanged suite evidence need not be repeated by every child.

Workers and review templates are resources, never an alternate router or model policy. No automatic integration branch, worktree reset, merger agent or ticket closure from upstream defaults.
