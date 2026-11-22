# Workspace Cleanup and Safety

After a verified merge, or a confirmed discard, clean only the exact workspace covered by recorded task ownership and authorization. A conventional folder name is insufficient. Push, PR, and keep routes preserve the checkout.

From outside the target, verify the registered absolute path, HEAD, and status including untracked files. Check for local-only ignored files before removal and preserve anything that must survive. If clean and within scope, run `git worktree remove <verified-absolute-path>` without force. Confirm the registry no longer includes the target. Delete a merged feature branch only if authorized and safe with `git branch -d`.

If removal reports modified files, untracked files, a lock, or other ownership uncertainty, preserve the checkout and report the exact obstruction. On Windows, retry a transient lock only after releasing task-owned handles and rechecking state. Keep repository-wide pruning separate from removal of the verified target.
