# Integration Menu and Execution Protocol

Internal Andino resource. Operates under Andino Workflow governance.

## 1. Dual-Mode Menu Specification

Present the integration choices using the appropriate channel for the active host environment.

### A. Host UI Mode (Claude Code with `AskUserQuestion`)
When running inside an interactive host with structured dialog capability, invoke `AskUserQuestion` with single-select choices matching the classified environment.

### B. Headless / CLI Terminal Mode (Codex, OpenCode, Antigravity, Shell)
When running in a standard terminal or non-interactive context, render the exact text menu and accept typed input (`1`, `2`, `3` or keywords `merge`, `pr`, `keep`):

#### Standard 3-Option Menu (Normal Repo & Named-Branch Worktree)
```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

#### Reduced 2-Option Menu (Detached HEAD Worktree)
```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)

Which option?
```

Wait for the human partner's response before proceeding. Integration authority belongs strictly to the user.

---

## 2. Option Execution Procedures

### Option 1: Merge Locally

```bash
# 1. Navigate to main repo root for safe context
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# 2. Update base branch and merge
git checkout <base-branch>
git pull
git merge <feature-branch>

# 3. Verify tests on the merged tree
<project test command>
```

#### Post-Merge Failure Rollback Protocol
If tests fail on the merged tree:
1. Stop immediately.
2. If the merge created an uncommitted merge commit or merge conflict, run:
   ```bash
   git merge --abort
   ```
   If the merge was a fast-forward, reset back to the pre-merge state:
   ```bash
   git reset --hard ORIG_HEAD
   ```
3. Leave the feature branch and worktree completely intact.
4. Report the failure output and investigate in isolation.

#### Post-Merge Success
When the merged tree passes tests:
1. Proceed to workspace cleanup (see `workspace-cleanup-and-safety.md`).
2. Delete the local feature branch:
   ```bash
   git branch -d <feature-branch>
   ```

---

### Option 2: Push and Create PR

```bash
# Push branch to remote
git push -u origin <feature-branch>

# From detached HEAD:
# git push origin HEAD:refs/heads/<new-branch-name>
```

#### Forge CLI and PR Generation
1. Check for installed forge tooling (`gh` for GitHub, `glab` for GitLab).
2. If available, invoke `gh pr create` with structured title, body, and base branch.
3. Integrate with sibling skill `andino-pr-description`:
   - Summary of change
   - Blast radius and affected modules
   - Verification evidence and test commands
   - Reversibility and rollback plan
4. If forge CLI is not available, surface the remote comparison URL printed by the Git push command.
5. **Preserve the worktree:** Review comments and PR revisions will be addressed in this workspace.

---

### Option 3: Keep As-Is

1. Announce preservation clearly:
   ```
   Keeping branch <feature-branch>. Worktree preserved at <worktree-path>.
   ```
2. No branches are merged or deleted; no remote calls are made.

---

### Discard Procedure (Explicit Request Only)

Discarding work is never presented as an option in the menu. It is executed only when the human partner explicitly requests it in conversation.

#### Mandatory Confirmation Step
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for the exact word `discard`. If confirmed:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
# Remove worktree (see workspace-cleanup-and-safety.md)
git branch -D <feature-branch>
```
