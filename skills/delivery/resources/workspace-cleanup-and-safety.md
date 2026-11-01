# Workspace Cleanup and Safety Protocol

Internal Andino resource. Operates under Andino Workflow governance.

## 1. Ownership-Based Worktree Removal

Workspace cleanup applies only to **Option 1 (Local Merge)** after a green post-merge test run, and to **Confirmed Discards**. Options 2 (Push & PR) and 3 (Keep As-Is) always preserve the worktree.

### Execution Context
Worktree removal commands must run from outside the target worktree. Use the `MAIN_ROOT` directory and the `WORKTREE_PATH` captured during initial environment detection.

### Classification Rules

1. **Normal Repository (`GIT_DIR == GIT_COMMON`):**
   No worktree exists. Cleanup is complete without filesystem mutations.
2. **Workflow-Managed Worktree (`WORKTREE_PATH` is under `.worktrees/` or `worktrees/`):**
   The workflow owns this worktree. Proceed to removal:
   ```bash
   git worktree remove "$WORKTREE_PATH"
   git worktree prune
   ```
3. **Host-Managed or External Worktree:**
   The workspace is managed by the host environment or external tooling. Leave it in place. If the host platform provides an explicit exit tool, invoke it cleanly.

---

## 2. Uncommitted Files and Refusal Protection

If `git worktree remove` fails with the message `contains modified or untracked files`:

### The Zero-Force Floor Invariant
**Never append `--force` on your own initiative.** The refusal indicates that files exist in this worktree that exist nowhere else in Git history: scratch notes, draft plans, or uncommitted code. Forcing removal permanently destroys them.

### Safe Resolution Protocol

1. Enumerate all uncommitted and untracked files:
   ```bash
   git -C "$WORKTREE_PATH" status --porcelain -uall
   ```
2. Present the exact file list and prompt the human partner:
   ```
   Worktree removal refused — these files were never committed:

   <file list>

   1. Commit them to <branch> before cleanup
   2. Move them into <main repo root>
   3. Delete them (unrecoverable)

   Which?
   ```
3. Execute the chosen action, verify the working tree is clean, and re-attempt `git worktree remove`.

---

## 3. Windows File Lock Handling

On Windows systems, background processes (such as language servers, terminal sessions, or antivirus indexers) can briefly lock directory handles, causing `git worktree remove` to fail with access denied errors.

### Safe Retry Procedure
1. Retry the removal command once after a brief interval.
2. If the lock persists, run `git worktree prune` to ensure Git metadata is consistent.
3. Report the locked path to the human partner with manual deletion guidance rather than issuing destructive shell overrides.
