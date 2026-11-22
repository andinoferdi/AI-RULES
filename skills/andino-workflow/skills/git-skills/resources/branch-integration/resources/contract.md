# Delivery Contract and Handoff Ledger Specification

Internal Andino resource. Operates under Andino Workflow governance.

## 1. Purpose and Authority Boundaries

The delivery contract formalizes the verification state, integration decisions, and handoff ledger before any repository or branch mutation occurs.

- **Verification does not grant mutation authority:** Passing tests and green verification prove candidate readiness; they do not authorize automatic branch creation, local merge, remote push, PR creation, publication, or worktree deletion.
- **Explicit human integration mandate:** The choice of integration path belongs exclusively to the human partner.
- **Independent task continuity:** Denied, deferred, or unavailable integration actions must not erase verified candidate evidence. The branch and worktree remain intact.

## 2. Handoff Ledger Schema

Every delivery evaluation produces or updates a structured handoff ledger:

```json
{
  "delivery_contract_version": 1,
  "timestamp": "2026-11-01T00:00:00Z",
  "workspace": {
    "git_dir": ".git/worktrees/feature-auth",
    "git_common_dir": ".git",
    "worktree_path": "/repo/.worktrees/feature-auth",
    "is_worktree": true,
    "is_detached": false,
    "environment_type": "named_worktree"
  },
  "branch_state": {
    "current_branch": "feature/token-refresh",
    "base_branch": "main",
    "head_sha": "a1b2c3d4e5f6...",
    "clean_working_tree": true
  },
  "verification": {
    "suite_command": "pytest -v",
    "suite_exit_code": 0,
    "status": "passed",
    "unverified_criteria": []
  },
  "permissions": {
    "local_merge": false,
    "remote_push": false,
    "create_pr": false,
    "discard": false
  },
  "decision": {
    "selected_option": null,
    "rationale": null,
    "confirmed_by_human": false
  },
  "residuals": {
    "untracked_files": [],
    "deferred_items": [],
    "durable_plan_ref": "docs/exec-plans/active/token-refresh.md"
  },
  "next_action": "Present integration options to human partner"
}
```

## 3. State Transition Matrix

| Initial State | Event / Signal | Target State | Permitted Action |
| :--- | :--- | :--- | :--- |
| `VERIFYING` | Candidate fails readiness checks | `HARD_STOP` | Preserve state and report missing evidence. |
| `VERIFYING` | Exact candidate is verified | `READY` | Resolve only missing choice or destination. |
| `READY` | Scoped push or PR is authorized | `PUBLISHING` | Verify remote ref and record PR separately. |
| `READY` | Scoped merge and base are authorized | `MERGING_LOCAL` | Merge in safe base checkout and verify merged HEAD. |
| `READY` | Keep is selected | `COMPLETED_PRESERVED` | Record the preserved checkout. |
| `READY` | Explicit discard is confirmed | `DISCARDING` | Recheck scope before owned cleanup. |

## 4. Rollback and Invariant Preservation

- Abort only an authorized, task-owned merge while `MERGE_HEAD` exists in the base checkout. If the merge already completed (merge commit created or fast-forward), preserve test failure logs, base HEAD, and candidate branch intact; request permission-scoped recovery options (no automatic hard reset).
- Worktree cleanup requires recorded task session ownership and clean state; path naming never establishes ownership.
- If worktree cleanup is refused due to untracked or modified files, never supply `--force`. Disclose files and require human resolution.
