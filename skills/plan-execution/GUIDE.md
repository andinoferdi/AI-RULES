# Execute the accepted graph and preserve recovery evidence

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Carry accepted tasks to evidenced outcomes without repeating verified work, stalling
on unneeded check-ins, or losing state.

## Trigger and non-trigger

Use when: Accepted plan ready or interrupted execution resumes.

Do not select for: Unresolved product intent or unapproved redesign.

## Prerequisites

Locate plan identity/checkpoint (`docs/exec-plans/active/<task>.md` or project convention);
inspect branch/worktree/diff/spec/task graph and compare evidence with current bytes.

Read [the contract](resources/contract.md) before execution. For an end-to-end trace,
read [the worked example](resources/worked-example.md).

## Core principles

- **The plan already did the thinking**: Execute it exactly, prove each step with
  verified observations, and update the durable checkpoint in-place.
- **Continuous execution**: Do not pause between tasks to ask "should I continue?".
  Execute dependency-ready tasks without stopping unless encountering one of the
  Four Hard Stops.
- **Rulings, not stalls**: Resolve ambiguities, plan defects, and bounded conflicts
  immediately. Record `Ruling: <decision> — <reason> — <cost if wrong>`.
- **Narration discipline**: Keep commentary between tool calls concise (1-2 lines);
  state the action and comparison against expected signals.
- **Single durable checkpoint**: Mutate the canonical plan in-place. No dual-ledger
  or external bash script dependencies.
- **Two-Phase Signal Gate**:
  - Behavioral code: Canonical TDD (`skills/tdd/GUIDE.md`) (watch RED fail -> minimal
    change -> watch GREEN pass).
  - Static content/config: Targeted Verification Contract (linter, schema, visual
    diff, or artifact check).
- **Blast radius hard-gating**: Continuous execution applies strictly to authorized
  local reversible work.
- **Four Hard Stops**:
  1. Irreversible or destructive operations (e.g. deleting branches, dropping tables).
  2. Security-sensitive perimeters (credentials, auth secrets).
  3. Crossing worktree/session boundaries without explicit prior authorization
     (git push, remote publish, external messaging).
  4. Rencana fundamentally broken where every path forward is guesswork.

## Procedure

1. **Establish task and checkpoint identity**:
   Locate the authoritative plan file (`docs/exec-plans/active/<task>.md`). Inspect
   the current branch/worktree, `git status --short`, and baseline commit (`HEAD`).
   Ensure working tree is clean or uncommitted changes are strictly accounted for.

2. **Audit drift and invalidate affected dependents**:
   Compare completed-task evidence with current outputs, dependencies, test identity,
   and freshness. Reuse work only when its evidence still supports the same acceptance;
   invalidate drifted evidence and affected dependents, not unrelated completed work.
   A checkbox or old commit alone is insufficient.

3. **Select task and claim in-place**:
   Select a dependency-ready task. Read its exact contract, verified interfaces, and
   recorded rulings from the plan. Mutate the plan in-place: set task status to
   `IN_PROGRESS` and update the Execution Board before editing code.

4. **Execute through the Two-Phase Signal Gate**:
   - **For behavioral code (canonical TDD, `skills/tdd/GUIDE.md`)**:
     1. *Phase 1 (RED)*: Add or locate the test case. Run the test command. Observe
        and verify the failing signal (discriminating assertion failure, not syntax error).
     2. *Phase 2 (GREEN)*: Write the minimal implementation satisfying the test.
        Rerun test command. Observe and verify passing signal (exit 0).
     3. *Regression pass*: Run the module test suite to verify no collateral breakage.
   - **For static artifacts (Documentation, Configuration, Schemas)**:
     1. Run targeted validator (linter, schema validator, build command).
     2. Compare actual output against `Expected:` signal.
     3. Confirm exit 0 and matching output.

5. **Apply Rulings, not stalls**:
   If a plan defect, interface ambiguity, or bounded conflict arises:
   - Decide the smallest change satisfying the specification.
   - Record the ruling directly in the owning task within the plan:
     `Ruling: <what was decided> — <why this satisfies spec> — <cost if wrong>`
   - Continue execution immediately. Do not pause to ask permission for decisions
     within session authority.
   - Only halt on the Four Hard Stops.

6. **In-place checkpoint update**:
   Before taking the next task, update the plan in-place:
   - Mark task actions complete `[x]`.
   - Update task status to `DONE`.
   - Append to `Result / Evidence`: exact command, exit status, terminal output summary,
     and commit hash range (`base..head`).
   - Update the Execution Board and update `NEXT ACTION`.

7. **Whole-branch final review gate**:
   Before declaring completion of the plan:
   - If a subagent tool is available, dispatch a fresh reviewer on the diff against
     merge base using code-review (`skills/code-review/GUIDE.md`) and verification (`skills/verification/GUIDE.md`).
   - If no subagent tool is available, perform a structured self-review against the
     specification, acceptance criteria, and full test suite.
   - Re-grade findings by impact:
     - *Critical and Important*: Enter ONE TDD fix pass. Each fix must be verified
       RED -> GREEN with tests before advancing.
     - *Minor*: Record as deferred in the final summary. Minors never trigger an
       extra fix pass.

8. **Final delivery and handoff**:
   - Confirm all Acceptance Criteria boxes are checked with supporting evidence.
   - Record final review summary, list of rulings made, and deferred minors.
   - Set overall plan status to `DONE` and `NEXT ACTION: None — task complete`.
   - Andino owns DONE; preserve durable evidence in the plan instead of deleting it.

## Ownership

Andino owns selection, depth, scope, the existing durable checkpoint, delegation and DONE.
Parent owns shared artifacts/final acceptance. This guide cannot invoke denied/manual
siblings or establish another lifecycle.

Resolve workflow-wide resources from the installed `andino-workflow` root: for a nested
member, use its containing workflow package; for standalone `andino-plan-execution`,
use the sibling `andino-workflow` package. The canonical paths are
`references/execution-plan.md`, `skills/tdd/GUIDE.md`, `skills/code-review/GUIDE.md`
and `skills/verification/GUIDE.md`. Load only the current phase's needed guide.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push,
merge, publication, external message, environment installation or destructive cleanup
is authorized by this guide. Reuse earlier permission without repeated confirmation;
disclose denied/unavailable actions and continue independent safe work.

## Output

Current task states/evidence, deviations, exact checks, unresolved acceptance and one NEXT ACTION.

## Verification

Unchanged completed output is skipped; drift reopens its verification and blocks dependents.

## Common rationalizations

| Excuse | Reality |
| --- | --- |
| "I remember what Task N says without reading" | You remember a vague summary. The plan has exact values, paths, and assertions. Read it. |
| "The plan's code looks right, skip watching RED fail" | A test you never saw fail proves nothing. It could pass unconditionally or test nothing. Run it. |
| "I'll run the full suite at the end instead of per step" | Per-step checks pinpoint what broke. End-of-task runs verify integration, they don't replace step gates. |
| "The plan is wrong here, I'll just quietly do the right thing" | Do the right thing AND record the ruling in the plan. Unrecorded deviation is secret drift. |
| "I'll update the plan checkpoint after finishing several tasks" | Context compaction can happen anytime. Update the plan in-place immediately after each task. |
| "Let me check in with the user before starting the next task" | The user authorized plan execution. Continuous execution is required. Only the Four Hard Stops stop you. |
| "I read my own diff carefully; final review is redundant" | Same author, same blind spots. Fresh reviewer or structured self-review against the spec is mandatory. |
| "Tests should pass, the change was trivial" | "Should" is an unverified assumption. Real commands and terminal output are the only acceptable evidence. |
| "The reviewer labeled it Minor, so I'll leave it as Minor" | Reviewers often grade spec silence rather than user impact. Re-grade by real effect on users, then gate. |
| "The fix is obvious, no need for a failing test first" | A failing test is the only proof the defect existed and is now resolved. Without it you have a guess. |
| "I'll fix all minor suggestions while I'm editing" | Fixing minors unprompted wastes tokens and risks regressing stable code. Defer minors to the report. |
| "I'll create a second ledger file to track progress" | Prohibited. The plan file is the single durable checkpoint. Never maintain dual ledgers. |

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

Reconstruct missing evidence narrowly from current source/artifacts, label provisional
claims; no fallback into wrong branch checkout.
