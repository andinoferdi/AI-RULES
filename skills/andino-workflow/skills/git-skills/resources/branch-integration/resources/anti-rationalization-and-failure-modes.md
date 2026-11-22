# Anti-Rationalization and Failure Modes Matrix

Internal Andino resource. Operates under Andino Workflow governance.

## 1. Anti-Rationalization Refutations Table

| Agent Excuse / Rationalization | Mechanical Reality and Required Response |
| :--- | :--- |
| *"Tests passed earlier in the session, so we can skip running them now."* | A green test suite only proves the tree it was executed on. Any subsequent edits or rebases invalidate previous proof. Run the full suite on the active candidate tree now. |
| *"The user obviously wants this merged to main."* | Integration authority belongs exclusively to the human partner. Use an existing scoped decision or ask for the missing choice. |
| *"The user seems done with this feature, so I will offer to discard it."* | The menu is complete as written. Discard exists only when explicitly initiated by the human partner in conversation. |
| *"The user said 'yeah, clean it up', which counts as confirmation to discard."* | Only the explicitly typed word `discard` authorizes permanent branch or commit deletion. |
| *"The PR is created, so the worktree is just clutter now."* | Pull request feedback, CI fixes, and review iterations are performed directly in that worktree. It must be preserved until the PR is merged or closed. |
| *"Worktree removal was refused, but `--force` is just finishing the requested cleanup."* | Removal refusal means uncommitted or untracked files exist only in that worktree. `--force` destroys them irrevocably. Enumerate the files and request human direction. |
| *"The test failure on the merged result is probably a flaky test."* | A failing merged result halts everything. Leave the feature branch and worktree intact, abort the merge, and investigate. |
| *"The base branch is obviously main."* | Never guess. Confirm the fork point from execution plans, upstream configuration, or ask the user. Undoing a merge to the wrong base is costly. |
| *"The push was rejected, so a force-push (`git push -f`) will fix it."* | A rejected push means the remote has diverged. Force-pushing risks destroying upstream commits. Investigate the divergence; force-push only under explicit human mandate. |
| *"This other worktree looks abandoned, so I will clean it up too."* | Path naming is never ownership. Clean only worktrees explicitly created and recorded as owned by the current delivery task. Never touch foreign workspaces. |
| *"Post-merge tests failed, so I'll run `git reset --hard`."* | Automatic hard resets rewrite history and destroy evidence without authority. Run `git merge --abort` only if `MERGE_HEAD` exists; on completed or fast-forward merges, preserve state and request recovery. |

---

## 2. Diagnostic Red Flags (Stop Immediately)

1. Presenting the integration menu while the test suite has failing tests.
2. Executing `git merge` or `git push` without scoped authorization.
3. Guessing the base branch is `main` without checking plan metadata or confirming with the user.
4. Using `git worktree remove --force` when untracked or uncommitted files are present.
5. Deleting a feature branch when post-merge verification failed.
6. Force-pushing (`-f` or `--force`) to a remote branch without explicit human instructions.
7. Omitting the post-merge test run after a local merge.
8. Running `git merge --abort` when no `MERGE_HEAD` exists, or running `git reset --hard` automatically on merge failure.
