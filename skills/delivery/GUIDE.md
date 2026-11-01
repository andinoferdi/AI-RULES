# Factual Integration and Branch Delivery Guide

Internal Andino resource. Operates under Andino Workflow governance.

## 1. Overview and Core Principle

The delivery phase transitions validated implementation into repository integration. Its core invariant is simple:

```
Verify tests ──▶ Detect environment ──▶ Confirm base ──▶ Present locked menu ──▶ Execute & verify ──▶ Clean up
```

Announce clearly at initiation:
*"I am using the delivery skill to complete this branch integration."*

---

## 2. Step 1: Pre-Integration Test Verification

Run the project's full test suite on the active working tree before doing anything else.

- **Node / TypeScript:** `npm test` or `pnpm test`
- **Python:** `pytest` or `python -m unittest`
- **Rust:** `cargo test`
- **Go:** `go test ./...`
- **Make:** `make test`

### Stop Condition: Failing Tests
If any test fails, do not present the integration menu. The menu is gated behind a green suite. Report failures and stop:

```
Tests failing (<N> failures). Must fix before completing:

[Failure output]
```

---

## 3. Step 2: Detect Environment

Capture Git workspace metadata before changing directories:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
BRANCH_NAME=$(git symbolic-ref --short -q HEAD 2>/dev/null || echo "")
```

### Environment Classification Matrix

| State | Detection | Menu Presented | Cleanup Behavior |
| :--- | :--- | :--- | :--- |
| **Normal Repo** | `GIT_DIR == GIT_COMMON` | Standard 3 options | No worktree to clean up. |
| **Named Worktree** | `GIT_DIR != GIT_COMMON`, named branch | Standard 3 options | Provenance-based cleanup if under `.worktrees/`. |
| **Detached HEAD** | `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 2 options (no merge) | Externally managed; preserve worktree. |

---

## 4. Step 3: Determine and Confirm Base Branch

Identify the fork point of the feature branch from durable execution plans or upstream tracking. If not already proven, confirm explicitly with the human partner:

```
This branch split from <candidate-base-branch> - is that correct?
```

Never assume the base is `main`. Merging into an incorrect base branch causes severe repository drift.

---

## 5. Step 4: Present Options via Dual-Mode Menu

### A. Host UI Mode (Claude Code with `AskUserQuestion`)
When running in an interactive session supporting structured question dialogs, invoke `AskUserQuestion` with the fixed choices matching the environment.

### B. Headless / CLI Terminal Mode (Codex, OpenCode, Shell)
Render the locked text menu and await user response:

#### Standard 3-Option Menu
```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

#### Reduced 2-Option Menu (Detached HEAD)
```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)

Which option?
```

---

## 6. Step 5: Execute Choice

### Option 1: Merge Locally

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

git checkout <base-branch>
git pull
git merge <feature-branch>

# Run full test suite on merged tree
<project test command>
```

#### Post-Merge Failure Rollback
If the test suite fails on the merged tree:
1. Halt immediately.
2. Roll back the merge:
   - For an uncommitted merge: `git merge --abort`
   - For a fast-forward merge: `git reset --hard ORIG_HEAD`
3. Leave the feature branch and worktree untouched.
4. Report the failure and investigate.

#### Post-Merge Success
When tests pass:
1. Clean up workspace (Step 6).
2. Delete the local branch: `git branch -d <feature-branch>`.

---

### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>
```

1. If GitHub CLI (`gh`) or GitLab CLI (`glab`) is installed, create the PR with structured title and description:
   - Integrate with sibling skill `andino-pr-description` (summary, blast radius, verification evidence, rollback).
2. If forge CLI is absent, surface the remote comparison URL printed by Git.
3. Keep the worktree intact so review feedback can be addressed directly.

---

### Option 3: Keep As-Is

Report:
*"Keeping branch <feature-branch>. Worktree preserved at <worktree-path>."*

---

### Discard Procedure (Explicit Request Only)

Discarding is never shown in the menu. If the user explicitly asks to throw work away, confirm first:

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for the exact word `discard`. When confirmed:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
# Clean worktree
git branch -D <feature-branch>
```

---

## 7. Step 6: Workspace Cleanup

Runs for Option 1 and confirmed discards. Options 2 and 3 always preserve the worktree.

1. **If `GIT_DIR == GIT_COMMON`:** Normal repo, nothing to remove. Done.
2. **If `WORKTREE_PATH` is under `.worktrees/` or `worktrees/`:**
   ```bash
   git worktree remove "$WORKTREE_PATH"
   git worktree prune
   ```
3. **If Removal is Refused (`contains modified or untracked files`):**
   Never use `--force`. Inspect files:
   ```bash
   git -C "$WORKTREE_PATH" status --porcelain -uall
   ```
   Show files to user and offer:
   1. Commit them to `<branch>` before cleanup
   2. Move them into `<main repo root>`
   3. Delete them (unrecoverable)
4. **Otherwise:** The workspace belongs to the host; leave it in place.

---

## 8. Quick Reference Matrix

| Option | Merge Locally | Push Remote | Keep Worktree | Delete Branch |
| :--- | :--- | :--- | :--- | :--- |
| **1. Merge Locally** | Yes | No | No (cleaned if under `.worktrees/`) | Yes (`-d`) |
| **2. Create PR** | No | Yes | Yes | No |
| **3. Keep As-Is** | No | No | Yes | No |
| **Discard (Explicit)** | No | No | No | Yes (`-D`) |

---

## 9. Modular Resources Index

- Handoff Ledger and Status Schema: [resources/contract.md](resources/contract.md)
- Environment and Worktree Detection: [resources/environment-and-worktree-detection.md](resources/environment-and-worktree-detection.md)
- Pre-Integration Verification: [resources/pre-integration-verification.md](resources/pre-integration-verification.md)
- Integration Menu and Execution: [resources/integration-menu-and-execution.md](resources/integration-menu-and-execution.md)
- Workspace Cleanup and Safety: [resources/workspace-cleanup-and-safety.md](resources/workspace-cleanup-and-safety.md)
- Anti-Rationalization and Failure Modes: [resources/anti-rationalization-and-failure-modes.md](resources/anti-rationalization-and-failure-modes.md)
