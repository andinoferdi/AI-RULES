---
name: andino-plan-execution
description: Execute accepted plans with continuous authorized progress, current acceptance evidence and one durable checkpoint under Andino Workflow.
---

# Execute accepted tasks against current evidence

Internal method ID: `andino-plan-execution` (alias: `plan-execution`).

> **Andino Workflow Member Skill**
> Apply proportional investigation, evidence-based decisions and one durable checkpoint.
> Hand off to the next relevant phase without recursively invoking the workflow.

## Purpose

Carry accepted tasks to observable outcomes without repeating verified work, stalling
on unnecessary check-ins, or losing the evidence needed to resume.

## Trigger and non-trigger

Use when: An accepted plan is ready for authorized execution, or interrupted execution resumes.

Do not select for: Unresolved product intent, planning-only requests or unapproved redesign.

## Prerequisites

Locate the authoritative plan, accepted requirements and current worktree. Read
[the execution contract](resources/contract.md) before executing. Consult
[the worked example](resources/worked-example.md) for a concrete trace and pressure cases.
Reuse the plan's LITE/STANDARD/DEEP shape and equivalent project fields.

## Execution principles

- **Specification before steps**: Session instructions and accepted requirements
  govern the outcome; the plan supplies the route. Follow valid steps and correct
  demonstrated defects with recorded rulings while preserving locked decisions.
- **Continuous execution**: Carry dependency-ready work through acceptance without
  repeated permission check-ins. Reuse existing scoped authorization, including
  authorized commit, push or setup; the skill itself grants none.
- **One checkpoint**: Keep actual progress, decisions and evidence in the existing
  plan. No second ledger, mandatory workspace script or conversation-memory dependency.
- **Observed signals**: Compare expected results with actual output and exercised
  scope. Exit 0, checklist marks and worker reports cannot substitute for acceptance.
- **Bounded context**: Read the current task and relevant rulings; filter long logs
  to the useful result. Give concise progress updates and material decisions.

Pause the affected action for missing authority, an unresolved material user-owned
decision, inaccessible required evidence, or a broken plan with no grounded route.
Check the exact scope of prior authorization for destructive, security-sensitive or
external actions. Ask only for what remains missing, checkpoint the blocker and next
check, and continue independent authorized work. Available tools do not grant authority.

## Procedure

1. **Establish identity and preflight**. Read plan, reachable specification and
   constraints. Inspect branch/worktree, `git status --short` and accepted task BASE.
   Attribute existing changes without requiring a clean tree. If a referenced spec
   is unavailable, record whether current accepted requirements suffice; block only
   decisions that need missing evidence. Inspect shared producer/consumer interfaces
   and dependency readiness. Check **specification readiness**, too: each next
   implementation task needs exact file/symbol anchors, its Change Specification
   (what changes into what, including decision-bearing code/text and literals),
   and concrete acceptance checks. A milestone or a detailed but stale/conflicting
   snippet is not sufficient. Within existing authority, resolve discoverable gaps
   from current source and write the smallest correction into the task before
   editing; use canonical planning when task decomposition/detail is missing.
   Unknown material contracts block only their consumers until bounded discovery
   populates them. Preserve locked decisions and completed valid evidence; ask
   only for a genuinely missing user-owned decision or authority.
   Record mismatches and disposition in the same plan,
   or one short note when there are no shared interfaces.

2. **Audit drift and recover**. Compare completed-task evidence with current inputs,
   outputs, checks, environment and dependencies. Reuse evidence only when required
   identities are present and still match; invalidate affected tasks and dependents,
   preserving unrelated verified work. For partial work, inspect and attribute current
   bytes, preserve user changes and run missing checks. Never revert unknown work as
   a recovery shortcut.

3. **Take a ready task**. Re-read its exact acceptance, commands, interfaces and relevant
   rulings rather than a remembered summary. Set `IN_PROGRESS` and synchronize the
   board when present before editing owned artifacts. Use parallel work only when
   useful, authorized and independently owned; serialize shared writes. Andino retains
   delegation and integration ownership.

4. **Execute and compare each signal**.
   - **Behavior changes**: Load canonical TDD before implementation. Observe one
     discriminating RED assertion, make the minimal change, then observe focused
     GREEN. Syntax/import/tooling/fixture errors are setup failures. If already GREEN,
     inspect the assertion and real behavior: reuse adequate existing coverage or
     strengthen an inadequate test. Preserve correct code; do not manufacture RED
     or reimplement already-satisfied behavior.
   - **Static artifacts**: Inspect/change/validate against observable acceptance.
     Configuration/schema changes affecting runtime behavior need behavioral checks.
     Content checks prove content properties, not future model compliance.
   - **Each required check**: Run with its recorded directory and prerequisites,
     read output and compare expected values, exercised cases and scope. Empty or
     wholly skipped test discovery is a gap. Select regression/integration checks
     by affected behavior, risk and the standing project quality floor; reuse
     unaffected evidence instead of rerunning broad suites after every small step.
   - **Mismatch**: Diagnose code failures with canonical debugging before patching;
     correct defective plan steps through bounded rulings. Unavailable checks leave
     their criterion `NOT_VERIFIED`, not silently waived.

5. **Record grounded rulings**. Resolve routine implementation choices within authority.
   For a plan defect or conflict, record in its owning task:
   `Ruling: <decision> — <evidence/spec basis> — <cost and scope if wrong>`.
   Propagate changed interfaces to consumers and invalidate affected evidence. A ruling
   cannot waive acceptance or silently change a material user-owned requirement.
   Rebaseline dependent work when needed and continue independent ready tasks.

6. **Complete and checkpoint the task**. Load canonical verification before acceptance.
   Confirm every required action/check has its observed result and every deviation its
   disposition. Record acceptance-to-check mapping, command/action, working directory,
   exit/result, relevant environment, tested identity and limits in `Result / Evidence`.
   A commit range identifies committed content only; include hashes or a scoped diff
   snapshot for WIP and owned new files. Mark `DONE` only with current acceptance
   evidence, synchronize actual board/detail state and set concrete `NEXT ACTION`
   before proceeding. Use `BLOCKED` with its dependency, or `SKIPPED` with an accepted
   replacement, when appropriate; preserve equivalent project representations.

7. **Review the complete owned change**. Load canonical code-review and verification.
   Pin accepted BASE plus committed, staged, unstaged and task-owned untracked bytes.
   Supply spec, acceptance map, check results, rulings and untested failure cases.
   Diff statistics are an index, not substantive review. Use a fresh reviewer when
   useful, authorized and available; otherwise perform a distinct structured self-review
   and disclose its limitation. Preserve separate Spec and Standards verdicts.
   Re-grade findings, including issues a reviewer declined to judge, by user effect.
   Resolve material findings with behavioral or static checks as appropriate, rerun
   affected integration and scope re-review to changed risk. Bound loops by new
   evidence using canonical anti-loop rules. A pass limit never makes unresolved
   material findings DONE; retain failed acceptance, blocker and NEXT ACTION.
   Defer optional polish with a reason instead of expanding scope automatically.

8. **Deliver and hand off**. Account for every in-scope acceptance criterion and
   material review finding. Finish authorized commit/push/setup steps and check
   their resulting state. Distinguish local verification, remote publication and
   installed activation; compare installed content with the reviewed source when
   distribution is in scope. Report results, material rulings, deferred findings
   and verification limits. Andino owns DONE. Preserve the checkpoint and set
   `NEXT ACTION: None — task complete` only when no required work remains.

## Ownership and resource resolution

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-plan-execution` and this guide expose one method, without recursive workflow invocation.

Resolve workflow-wide resources from the installed `andino-workflow` root: a nested
member uses its containing workflow; standalone `andino-plan-execution` uses the
sibling `andino-workflow` package. Canonical workflow-root paths are:

- `references/execution-plan.md` and `references/anti-loop.md` for lifecycle/recovery.
- `skills/tdd/GUIDE.md` for behavior changes.
- `skills/debugging/GUIDE.md` for code failures with unknown cause.
- `skills/code-review/GUIDE.md` and `skills/verification/GUIDE.md` for acceptance.

These are workflow-root paths, not member-relative Markdown links. Load only the
current phase's needed guides through the host's permitted mechanism. Missing
resources remain unavailable; record the gap and use an honest bounded fallback.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push,
merge, publication, external message, installation or destructive cleanup is authorized
by this guide. Reuse earlier permission without repeated confirmation; disclose denied
or unavailable actions and continue independent safe work. Preserve user changes/secrets.

## Output and verification

Current task states, acceptance evidence, rulings, unresolved findings and one NEXT ACTION.
Unchanged verified work is reused; changed or incomplete identity reopens affected
verification. Record actual command/action and result, never inferred success.

## Common rationalizations

| Shortcut | Required response |
| --- | --- |
| "I remember Task N" | Re-read exact acceptance, commands, interfaces and rulings. |
| "It already passes, so break code to get RED" | Inspect coverage and preserve satisfied behavior. |
| "The command exited 0" | Check actual cases, expected values and exercised scope. |
| "The plan is wrong; quietly fix it" | Record the smallest spec-grounded ruling and affected consumers. |
| "HEAD contains the work" | Include staged, unstaged and owned untracked bytes in review identity. |
| "The reviewer said Minor" | Grade real user effect, not silence in the spec. |
| "One repair pass ended" | Remaining material acceptance is still incomplete. |
| "Recovery means reverting the diff" | Attribute and preserve changes, then verify current bytes. |
| "Push/setup always needs another question" | Reuse exact existing authority; verify the result. |

## Fallback

Reconstruct missing evidence narrowly from current artifacts; keep provisional claims
and unavailable checks explicit. Do not change worktrees, erase work or fabricate
dispatch/results to satisfy the procedure.

## Worked example and anti-pattern


The synthetic offline example is applied in temporary isolation. Its independent expected
values describe the contract; its execution is procedural evidence, not a benchmark of
future model behavior.

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

This example reuses a completed task only when its source and verification identity
still match. A changed prerequisite invalidates its dependent evidence; unrelated
current evidence remains reusable.

```python evolution-example
import json

def reusable_tasks(tasks, prior, current):
    def evidence_matches(task_id):
        old = prior.get(task_id)
        now = current.get(task_id)
        return bool(old and now
                    and old.get("result") == "PASS"
                    and all(isinstance(record.get(key), str) and record[key].strip()
                            for record in (old, now)
                            for key in ("source", "check", "environment"))
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
