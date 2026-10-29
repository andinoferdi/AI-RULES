---
name: andino-plan-execution
description: Accepted plan ready or interrupted execution resumes. Operates under Andino Workflow governance.
---

# Execute the accepted graph and preserve recovery evidence

Internal method ID: `andino-plan-execution` (alias: `plan-execution`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Carry accepted tasks to evidenced outcomes without repeating verified work.

## Trigger and non-trigger

Use when: Accepted plan ready or interrupted execution resumes.

Do not select for: Unresolved product intent or unapproved redesign.

## Prerequisites

Locate plan identity/checkpoint; inspect branch/worktree/diff/spec/task graph and compare evidence with current bytes.

## Procedure

1. Establish the task and authoritative plan/checkpoint identity. Map accepted outcomes and specifications to current task IDs; inspect the current branch/worktree, status and relevant diff.
2. Compare completed-task evidence with current outputs, dependencies, test identity/scope, environment and freshness. Reuse work only when its evidence still supports the same acceptance; invalidate drifted evidence and affected dependents, not unrelated completed work. A checkbox, worker report or old commit alone is insufficient.
3. Select a dependency-ready task and read its exact contract, verified interfaces and recorded rulings. Confirm producer prerequisites against current bytes and capture baseline ownership; task range is not necessarily `HEAD~1`.
4. Implement one slice using canonical TDD for behavior and suitable targeted verification for static content. Compare each actual command result to its expected signal; retain failures and material limitations.
5. Resolve bounded plan/spec/interface conflicts from accepted requirements and current evidence, recording the decision and reason in the same checkpoint. Continue independent authorized work; ask only when a material user-owned decision or policy requires it.
6. Inspect worker reports and actual output before integration. Check owned paths, consumed/produced interfaces, review findings and current verification; a worker success message does not establish acceptance.
7. Before accepting implementation, load [code-review](../code-review/GUIDE.md) for Spec/Standards review and [verification](../verification/GUIDE.md) for the consequential completion claim, unless their valid current activation/evidence can be reused. Record completion only after current acceptance checks ran. Append evidence identity, commands/results, review residuals, blockers and the next frontier to the same plan.
8. Perform cross-task/final acceptance and prepare delivery. Andino owns DONE; preserve durable evidence instead of deleting it as scratch.

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

## Evidence reuse example

This example reuses a completed task only when its source and verification identity still match. A changed prerequisite invalidates its dependent evidence; unrelated current evidence remains reusable.

```python evolution-example
import json

def reusable_tasks(tasks, prior, current):
    def evidence_matches(task_id):
        old = prior.get(task_id)
        now = current.get(task_id)
        return bool(old and now
                    and old.get("result") == "PASS"
                    and old.get("source") == now.get("source")
                    and old.get("check") == now.get("check")
                    and old.get("environment") == now.get("environment"))

    invalid = {
        task["id"] for task in tasks if not evidence_matches(task["id"])
    }
    changed = True
    while changed:
        changed = False
        for task in tasks:
            if task["id"] not in invalid and any(dep in invalid for dep in task["deps"]):
                invalid.add(task["id"])
                changed = True
    return {
        "reusable": sorted(task["id"] for task in tasks if task["id"] not in invalid),
        "rerun": sorted(invalid),
    }

tasks = [
    {"id": "base", "deps": []},
    {"id": "ui", "deps": ["base"]},
    {"id": "docs", "deps": ["base"]},
]
prior = {
    name: {"source": name + "-source", "check": name + "-check",
           "environment": "same", "result": "PASS"}
    for name in ("base", "ui", "docs")
}
current = {
    "base": {"source": "base-source", "check": "base-check", "environment": "same"},
    "ui": {"source": "ui-source", "check": "new-ui-check", "environment": "same"},
    "docs": {"source": "docs-source", "check": "docs-check", "environment": "same"},
}
producer_drift = dict(current)
producer_drift["base"] = {"source": "changed-base", "check": "base-check", "environment": "same"}
result = {
    "local_drift": reusable_tasks(tasks, prior, current),
    "producer_drift": reusable_tasks(tasks, prior, producer_drift),
}
print(json.dumps(result, sort_keys=True))
```

Expected output:

```json
{"local_drift": {"rerun": ["ui"], "reusable": ["base", "docs"]}, "producer_drift": {"rerun": ["base", "docs", "ui"], "reusable": []}}
```

## Fallback

Reconstruct missing evidence narrowly from current source/artifacts, label provisional claims; no fallback into wrong branch checkout.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- obra/superpowers:skills/executing-plans/SKILL.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
