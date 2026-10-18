# Execute the accepted graph and preserve recovery evidence

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Carry accepted tasks to evidenced outcomes without repeating verified work.

## Trigger and non-trigger

Use when: Accepted plan ready or interrupted execution resumes.

Do not select for: Unresolved product intent or unapproved redesign.

## Prerequisites

Locate plan identity/checkpoint; inspect branch/worktree/diff/spec/task graph and compare evidence with current bytes.

## Procedure

1. Reconcile drift for completed tasks using actual output identities and check scope. Checked boxes, old commits and recollection alone are insufficient; invalidate only affected evidence.
2. Select dependency-ready task and read exact contract, interfaces and rulings. Capture baseline bytes/ownership; task range is not necessarily HEAD~1.
3. Implement one slice using canonical TDD for behavior, targeted verification for static content. Compare each actual command result to expected signal; preserve named failures.
4. Resolve bounded plan/spec/interface conflicts with evidence, reason and cost. Continue independent authorized work; ask only about material missing decisions.
5. Record completion only after current acceptance checks ran. Append commands/results, output hashes, review residuals and next frontier immediately to the same plan.
6. Perform cross-task/final acceptance and prepare delivery. Andino owns DONE; preserve durable evidence instead of deleting it as scratch.

## Ownership

Andino owns selection, depth, scope, the existing durable checkpoint, delegation and DONE. Parent owns shared artifacts/final acceptance. This guide cannot invoke denied/manual siblings or establish another lifecycle.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

Current task states/evidence, deviations, exact checks, unresolved acceptance and one NEXT ACTION.

## Verification

Unchanged completed output is skipped; drift reopens its verification and blocks dependents.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "plan_id": "ticket-17",
  "files": {
    "created.py": "VALUE = 15\n"
  },
  "completed": [
    {
      "id": "create",
      "path": "created.py",
      "content": "VALUE = 15\n"
    }
  ],
  "next_task": {
    "id": "list",
    "deps": [
      "create"
    ]
  },
  "drift_content": "VALUE = 16\n"
}
```

Anti-pattern: Redo completed work after compaction, premature completion or second .superpowers ledger.

## Fallback

Reconstruct missing evidence narrowly from current source/artifacts, label provisional claims; no fallback into wrong branch checkout.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- obra/superpowers:skills/executing-plans/SKILL.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
