# Environment and Worktree Detection

Run these read-only checks in the candidate checkout before changing directories:

```sh
git rev-parse --show-toplevel
git rev-parse --absolute-git-dir
git rev-parse --path-format=absolute --git-common-dir
git rev-parse --show-superproject-working-tree
git rev-parse HEAD
git branch --show-current
git worktree list --porcelain
git status --porcelain=v1 --untracked-files=all
```

Normalize paths using the host's path semantics. A nonempty superproject identifies submodule context. Match the checkout root against the worktree registry before concluding it is linked. An empty branch name identifies detached HEAD independently of workspace type. Record the lifecycle owner from task or host evidence.

Resolve a merge or PR base from the accepted plan or user instruction. Treat a guessed fork point or tracking branch as a clue. Ask when the destination still has competing interpretations. Find the actual base checkout in the worktree registry and verify it before mutation.
