
# Factual Integration and Branch Delivery

Resource contract; selected directly under its canonical owner.

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: single durable checkpoint, proportional investigation, anti-loop guards.
> Loading this file does not invoke another skill or mutate repository state. Upstream references yield to current policy.

## 1. Dominant Negative Gates

Reject delivery invocation immediately if ANY condition holds:
- **Failing Tests**: Project test suite fails (<N> failures). Return to active task implementation; the menu comes only after a green suite.
- **Uncommitted Functional Work**: Working tree holds uncommitted or unstaged feature changes. Commit or stash before integration.
- **Unresolved Merge Conflicts**: Repository is in an unfinished conflict or rebase state (`MERGE_HEAD` exists). Resolve inline first.
- **Presumed Integration Authority**: Never execute merge, push, or branch deletion without explicit human confirmation.

## 2. Operational Triage Router

| Environment State | Detection Condition | Menu Type | Worktree Cleanup Behavior |
| :--- | :--- | :--- | :--- |
| **Normal Repo** | `GIT_DIR == GIT_COMMON` | Standard 3 options | No worktree to remove; workspace preserved. |
| **Named Worktree** | `GIT_DIR != GIT_COMMON`, named branch | Standard 3 options | Worktree removed if under `.worktrees/` or `worktrees/`. |
| **Detached HEAD** | `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 2 options (no merge) | Externally managed; leave worktree in place. |

## 3. Gated 6-Phase Lifecycle

```
[Phase 1: Test Suite Verification] ──▶ [Phase 2: Environment & Base Detection] ──▶ [Phase 3: Present Locked Menu]
                                                                                               │
[Phase 6: Ownership Workspace Cleanup] ◀── [Phase 5: Post-Merge Test & Abort] ◀── [Phase 4: Execute Choice]
```

- **Phase 1 (Test Suite Verification)**: Run full project test suite. If non-zero exit, halt and report failures.
- **Phase 2 (Environment & Base Detection)**: Capture `GIT_DIR`, `GIT_COMMON`, `WORKTREE_PATH`. Confirm base branch fork point.
- **Phase 3 (Present Locked Menu)**: Dual-Mode UI: invoke `AskUserQuestion` if interactive host; otherwise render 1/2/3 text menu.
- **Phase 4 (Execute Choice)**: Option 1: checkout base, merge (no automatic pull); Option 2: push -u, create PR via forge CLI; Option 3: keep as-is.
- **Phase 5 (Post-Merge Test & Abort)**: Verify tests on merged tree. On failure, if MERGE_HEAD exists run `git merge --abort`; if merge completed or fast-forwarded, preserve evidence and base HEAD, request permission-scoped recovery (no automatic hard reset).
- **Phase 6 (Workspace Cleanup)**: Clean only task-owned worktrees; path naming is never ownership. On refusal, never `--force`; prompt human resolution.

## 4. Five Floor Invariants

1. **Strict Green Suite Prerequisite**: Delivery menu is locked until full test suite passes on the exact candidate tree.
2. **Human Integration Authority**: Integration choices belong exclusively to the human partner; no silent merges or PR creations.
3. **Non-Negotiable Menu Options**: Present exactly the fixed 3-option (or 2-option) menu; discard exists only on explicit request.
4. **Zero-Force Refusal Guard**: Never apply `--force` to remove worktrees containing uncommitted or untracked files.
5. **Completed-Merge Safety**: `git merge --abort` applies ONLY when `MERGE_HEAD` exists. Completed or fast-forward merges preserve evidence and request authorized recovery; no automatic hard reset (`git reset --hard`), automatic pull, push, or delete.
6. **Path Naming Never Ownership**: Folder paths (e.g. `.worktrees/`) do not establish ownership; clean only recorded task-owned worktrees.

## 5. Anti-Rationalization Refutations

| Rationalization Shortcut | Mechanical Reality & Required Response |
| :--- | :--- |
| *"Tests passed earlier in the session; skip rerunning."* | A green suite only proves the tree it ran on. Run tests on the candidate tree now. |
| *"They obviously want it merged to main."* | Integration is the human partner's decision. Present the menu and await choice. |
| *"Worktree removal refused; `--force` finishes cleanup."* | Refusal means files exist only in that worktree. `--force` destroys them. Show user and ask. |
| *"The post-merge failure is probably flaky."* | Failing merged result stops everything. Preserve state, run `git merge --abort` only if MERGE_HEAD exists, and investigate. |
| *"The base branch is obviously main."* | Confirm fork point from plan or ask. Merging to the wrong base is costly to undo. |
| *"Post-merge tests failed, so I'll `git reset --hard`."* | Automatic hard resets rewrite history and destroy evidence without authority. Preserve state and request recovery. |

## 6. Diagnostic Red Flags (Stop Immediately)

1. Presenting the integration menu while test suite has failing tests.
2. Executing `git merge` or `git push` without human selection from the menu.
3. Running `git worktree remove --force` when untracked files are reported.
4. Guessing the integration base branch without verification.
5. Deleting a feature branch after a failed post-merge test run.
6. Running `git merge --abort` when no MERGE_HEAD exists, or running `git reset --hard` automatically.

## 7. Progressive Disclosure Router

- Complete delivery craft and procedural runbook: [guide.md](guide.md)
- Handoff ledger schema and status transitions: [resources/contract.md](resources/contract.md)
- Mechanical git-dir and worktree detection: [resources/environment-and-worktree-detection.md](resources/environment-and-worktree-detection.md)
- Pre-integration test runner protocols: [resources/pre-integration-verification.md](resources/pre-integration-verification.md)
- Menu specification, merge, PR creation, and discard: [resources/integration-menu-and-execution.md](resources/integration-menu-and-execution.md)
- Workspace removal, untracked protection, and Windows locks: [resources/workspace-cleanup-and-safety.md](resources/workspace-cleanup-and-safety.md)
- Anti-rationalization table and failure case studies: [resources/anti-rationalization-and-failure-modes.md](resources/anti-rationalization-and-failure-modes.md)
- Provenance: Adapted from `obra/superpowers:skills/finishing-a-development-branch`. Preserved under MIT license terms in [../../references/license.md](../../references/license.md).

## 8. Runnable Operational Contract & Verification Harness

```python andino-operational-example
import json, os, sys

def evaluate_delivery_contract(data):
    if not isinstance(data, dict): return {"valid": False, "error": "Contract must be a dict"}
    if data.get("test_suite_passed") is not True: return {"valid": False, "error": "Green test suite required"}
    if not str(data.get("base_branch", "")).strip(): return {"valid": False, "error": "Base branch must be confirmed"}
    if data.get("has_uncommitted_changes") is True: return {"valid": False, "error": "Working tree must be clean"}
    options = data.get("presented_options", [])
    if len(options) not in (2, 3): return {"valid": False, "error": "Menu must present exactly 2 or 3 options"}
    if data.get("force_removal_used") is True: return {"valid": False, "error": "Zero-force invariant violated"}
    if data.get("automatic_hard_reset_used") is True: return {"valid": False, "error": "Automatic hard reset prohibited"}
    if data.get("automatic_pull_used") is True: return {"valid": False, "error": "Automatic pull prohibited"}
    if data.get("merge_abort_without_merge_head") is True: return {"valid": False, "error": "merge --abort only valid when MERGE_HEAD exists"}
    if data.get("unowned_cleanup_attempted") is True: return {"valid": False, "error": "Path naming is never ownership; clean only owned worktrees"}
    return {"valid": True, "status": "DELIVERY_CONTRACT_VERIFIED"}

if __name__ == "__main__":
    is_neg = os.environ.get("ANDINO_NEGATIVE") == "1"
    payload = {
        "test_suite_passed": not is_neg,
        "base_branch": "" if is_neg else "main",
        "has_uncommitted_changes": is_neg,
        "presented_options": ["merge", "pr", "keep"],
        "force_removal_used": is_neg,
        "automatic_hard_reset_used": is_neg,
        "automatic_pull_used": is_neg,
        "merge_abort_without_merge_head": is_neg,
        "unowned_cleanup_attempted": is_neg,
    }
    result = evaluate_delivery_contract(payload)
    if not result["valid"]:
        sys.stderr.write(f"Verification failed: {result['error']}\n")
        sys.exit(1)
    print(json.dumps(result, sort_keys=True))
    sys.exit(0)
```
