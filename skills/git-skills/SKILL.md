---
name: andino-git-skills
description: Use when managing Git workspaces, preventing destructive Git operations, maintaining branch hygiene, integrating branches, or drafting PRs. Operates under Andino Workflow governance.
---

# Git Skills: Workspace, Safety, Hygiene, Integration, and PRs

Internal method ID: `andino-git-skills` (alias: `git-skills`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow protocol: single durable checkpoint, proportional investigation, anti-loop guards.
> Loading this file does not invoke another skill or mutate repository state. Upstream references yield to current policy.

## 1. Dominant Negative Gates

Reject git-skills execution immediately if ANY condition holds:
- **Destructive Bypasses**: Never run destructive git commands (`reset --hard`, `clean -fd`, `branch -D`) without explicit human authority.
- **Unverified Base**: Never guess the base branch; confirm from the active execution plan or prompt the user.
- **Unsafe Rollback**: Never run `git merge --abort` when `MERGE_HEAD` is absent, or perform automatic hard resets on completed merges.
- **Unowned Cleanup**: Never infer worktree ownership from folder path naming; clean only owned, clean worktrees.

## 2. Select a resource, not a second lifecycle

Load only the resource matching the current need. A direct resource selection uses
that procedure and current authority; it does not run this parent's other modes,
reopen accepted requirements or require a second execution plan.

| Current need | Resource | Exclusion |
| :--- | :--- | :--- |
| Workspace isolation, safe worktrees, concurrent tasks | [workspace](resources/workspace/guide.md) | In-place single-branch edits without concurrency |
| Destructive operation prevention, commit/reset safety guards | [operation-safety](resources/operation-safety/guide.md) | Standard everyday git status/add/diff |
| Branch hygiene, atomic commit progression, branch naming | [change-hygiene](resources/change-hygiene/guide.md) | Unrelated project build/test failures |
| Branch integration, local merge, completed-merge recovery | [branch-integration](resources/branch-integration/guide.md) | Active feature implementation before green test suite |
| Pull request drafting, blast radius, verification proof | [pr-draft](resources/pr-draft/guide.md) | Unpushed local experiments without branch tracking |

*Note: Pre-commit checks are owned canonically by CI/CD (resolve `skills/ci-cd-and-automation/resources/commit-checks/guide.md` from the installed `andino-workflow` root).*

## 3. Floor Invariants

1. **Permission-Scoped Mutation**: All commits, merges, pushes, PRs, and deletions require explicit user consent.
2. **Completed-Merge Safety**: `merge --abort` applies ONLY when `MERGE_HEAD` exists. Completed or fast-forward merges preserve evidence and request authorized recovery; no automatic hard resets.
3. **Zero Path-Based Ownership**: Folder names (e.g. `.worktrees/`) do not prove ownership. Clean only recorded task-owned worktrees.
4. **Clean Tree Verification**: Pre-integration and pre-commit checks require an unbroken green suite on the exact tree.
5. **No Blind Remote Sync**: Never run automatic `git pull` or `git push` without scoped permission and verification.

## 4. Anti-Rationalization Refutations

| Rationalization | Mechanical Reality |
| :--- | :--- |
| *"The merge failed tests, so I'll `git reset --hard`."* | Automatic hard resets erase uncommitted evidence and history. Preserve state and ask. |
| *"The worktree path is `.worktrees/temp`, so I can delete it."* | Path naming is not ownership. Unowned worktrees belong to user or peers. |
| *"I need latest changes, so I'll run `git pull`."* | Unprompted pulls introduce unvetted remote code and merge conflicts. Confirm first. |
| *"Tests passed earlier; safe to merge now."* | Only tests on the merged candidate tree prove integration safety. |

## 5. Diagnostic Red Flags (Stop Immediately)

1. Invoking `git merge --abort` when no merge conflict or `MERGE_HEAD` exists.
2. Running `git reset --hard` automatically after a completed or fast-forward merge failure.
3. Deleting or pruning a worktree whose creation was not recorded by the active task.
4. Guessing `main` as base branch without verifying repository branch topology.

## 6. Progressive Disclosure Router

- Complete git craft and comprehensive procedural runbook: [GUIDE.md](GUIDE.md)
- Workspace isolation and worktree protocol: [resources/workspace/guide.md](resources/workspace/guide.md)
- Operation safety and destructive command guards: [resources/operation-safety/guide.md](resources/operation-safety/guide.md)
- Branch hygiene and atomic commit progression: [resources/change-hygiene/guide.md](resources/change-hygiene/guide.md)
- Branch integration, dual-mode UI, and safe rollback: [resources/branch-integration/guide.md](resources/branch-integration/guide.md)
- Pull request drafting, blast radius, and verification evidence: [resources/pr-draft/guide.md](resources/pr-draft/guide.md)

## 7. Runnable Operational Contract & Verification Harness

```python andino-operational-example
import json, os, sys

def evaluate_git_contract(data):
    if not isinstance(data, dict): return {"valid": False, "error": "Contract must be a dict"}
    if data.get("has_unauthorized_mutation") is True: return {"valid": False, "error": "Unauthorized mutation"}
    if data.get("automatic_hard_reset") is True: return {"valid": False, "error": "Automatic hard reset prohibited"}
    if data.get("path_inferred_ownership") is True: return {"valid": False, "error": "Path naming is never ownership"}
    mode = data.get("selected_mode")
    if mode not in ("workspace", "operation-safety", "change-hygiene", "branch-integration", "pr-draft"):
        return {"valid": False, "error": "Invalid mode"}
    return {"valid": True, "mode": mode, "status": "GIT_CONTRACT_VERIFIED"}

if __name__ == "__main__":
    is_neg = os.environ.get("ANDINO_NEGATIVE") == "1"
    payload = {
        "has_unauthorized_mutation": is_neg,
        "automatic_hard_reset": is_neg,
        "path_inferred_ownership": is_neg,
        "selected_mode": "invalid" if is_neg else "branch-integration",
    }
    result = evaluate_git_contract(payload)
    if not result["valid"]:
        sys.stderr.write(f"Verification failed: {result['error']}\n")
        sys.exit(1)
    print(json.dumps(result, sort_keys=True))
    sys.exit(0)
```

## Provenance

Adapted from `obra/superpowers:skills/{using-git-worktrees,finishing-a-development-branch}` under MIT license. See the notice for the separate PR-writing and guardrail references ([references/license.md](references/license.md)).
