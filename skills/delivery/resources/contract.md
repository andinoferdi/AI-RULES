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
| `VERIFYING` | Test suite exit code != 0 | `HARD_STOP` | Halt immediately; report failure log; no menu offered. |
| `VERIFYING` | Uncommitted functional changes | `DIRTY_TREE_STOP` | Require commit or stash before presenting options. |
| `VERIFYING` | Test suite exit code == 0 | `ENVIRONMENT_DETECTED` | Inspect `GIT_DIR` vs `GIT_COMMON`; confirm base branch. |
| `ENVIRONMENT_DETECTED` | Base branch confirmed | `MENU_PRESENTED` | Present locked 3-option menu (or 2-option for detached HEAD). |
| `MENU_PRESENTED` | Option 1 selected (Merge Locally) | `MERGING_LOCAL` | Checkout base, merge, run post-merge test. Abort on failure. |
| `MENU_PRESENTED` | Option 2 selected (Push & PR) | `PUSHING_PR` | Push upstream; create PR via forge CLI or report URL. |
| `MENU_PRESENTED` | Option 3 selected (Keep As-Is) | `COMPLETED_PRESERVED` | Record path, preserve branch and worktree untouched. |
| `MENU_PRESENTED` | Explicit word `discard` typed | `DISCARDING` | Confirm commit list, force-delete branch, prune worktree. |

## 4. Rollback and Invariant Preservation

- If post-merge verification fails during Option 1, execute `git merge --abort` immediately to return the repository to its clean pre-merge state.
- If worktree cleanup is refused due to untracked or modified files, never supply `--force`. Disclose files and require human resolution.
