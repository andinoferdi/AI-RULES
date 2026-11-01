# Environment and Worktree Detection Protocol

Internal Andino resource. Operates under Andino Workflow governance.

## 1. Mechanical Workspace Detection

Execute the following shell commands to capture the exact Git workspace topology before any directory changes:

```bash
# Capture directory paths while inside the active workspace
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)

# Determine branch name and HEAD state
BRANCH_NAME=$(git symbolic-ref --short -q HEAD 2>/dev/null || echo "")
```

Capture these variables immediately upon entering the delivery phase. Later steps (such as local merge) will change directories to the main repository root before cleanup runs, making relative lookups inaccurate.

## 2. Environment Classification Matrix

Compare `GIT_DIR` and `GIT_COMMON` to classify the current execution environment:

| State | Condition | Menu Type | Worktree Cleanup Behavior |
| :--- | :--- | :--- | :--- |
| **Normal Repository** | `GIT_DIR == GIT_COMMON` | Standard 3 options | No worktree to clean up. Workspace is the primary clone. |
| **Named-Branch Worktree** | `GIT_DIR != GIT_COMMON` and `BRANCH_NAME != ""` | Standard 3 options | Worktree cleanup applies if under `.worktrees/` or `worktrees/`. |
| **Detached HEAD Worktree** | `GIT_DIR != GIT_COMMON` and `BRANCH_NAME == ""` | Reduced 2 options (no local merge) | Externally managed workspace. Leave in place; no local merge. |

## 3. Base Branch Identification Protocol

The base branch is the integration target that the current branch was originally forked from.

1. **Inspect Provenance:** Check the execution plan (`docs/exec-plans/active/*.md`), the upstream tracking branch (`git rev-parse --abbrev-ref --symbolic-full-name @{u}`), or the conversation context.
2. **Never Assume Main:** Even if `main` or `master` is the repository default, the work may have branched from `develop`, `release/v1.0`, or a staging branch.
3. **Explicit Confirmation:** If the base branch cannot be proved from durable metadata, prompt the human partner:
   ```
   This branch split from <candidate-base-branch> - is that correct?
   ```
   Do not proceed to merge until the base branch is explicitly confirmed. Merging into the wrong base branch causes severe repository drift.

## 4. Multi-Host and Windows Path Handling

- On Windows under Git Bash, `pwd -P` returns POSIX-style paths (e.g., `/c/Users/...`). Ensure consistent comparison between `GIT_DIR` and `GIT_COMMON`.
- When switching directories via `cd "$MAIN_ROOT"`, use normalized forward slashes.
- Stale worktree registrations can be pruned safely via `git worktree prune`.
