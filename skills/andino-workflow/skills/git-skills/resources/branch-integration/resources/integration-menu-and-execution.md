# Integration Selection and Execution

## Choose the action

Reuse a choice already given in the request or accepted plan. If no choice exists after candidate verification, ask once with the applicable options:

- Named branch: merge locally into the verified base, push and open a PR, or keep the branch.
- Detached HEAD: push the verified commit to a named remote branch and open a PR, or keep the checkout. Use a fully qualified destination ref. Creating a local branch is a separate action.

Ask about the base only for a merge or PR with unresolved target. A tracking branch may identify a push destination, but it does not prove the integration base.

## Execute and check

| Action | Procedure and evidence |
| --- | --- |
| Push only | Verify remote and destination branch. Push the tested SHA with `git push <remote> <sha>:refs/heads/<branch>`. Compare the remote ref with the candidate using `git ls-remote --heads <remote> refs/heads/<branch>`. |
| Push and open PR | Verify push first, then use the repo template and PR drafting route. Record the forge URL when created. If creation fails, report the successful push separately and retain the checkout. |
| Merge locally | Find the base checkout using `git worktree list --porcelain`. If base is not checked out, select an authorized clean checkout for it. Recheck its branch, clean state, and operation state. Merge the verified candidate there without an implicit pull. Run required checks on the resulting HEAD. Verify candidate ancestry before considering cleanup. |
| Keep | Record the exact SHA and location. |
| Discard | Only when explicitly requested. Show worktree, branch, unique commits, and local-only files at risk. Require exact `discard` confirmation. Recheck scope and use the cleanup protocol before deleting the branch. |

On a merge conflict, preserve the checkout unless aborting the task's own in-progress merge is authorized and safe. Check that `MERGE_HEAD` exists in the base checkout before aborting. After a completed merge with failed checks, preserve the base HEAD and candidate, report the failure, and resolve recovery separately. Never force a rejected push.
