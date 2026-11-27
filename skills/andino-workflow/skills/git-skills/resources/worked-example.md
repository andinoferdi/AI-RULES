# Worked example: finishing a branch whose merged tree fails

Synthetic scenario; paths, SHAs and output are illustrative. A weather-station data pipeline
(Node, `npm test` per its README). CONTRIBUTING says feature branches start from `develop` and
merge back into it. Lina writes: "The gust smoothing in `../stations-gusts` is done. Merge it
locally and clean up the worktree and branch. Don't push."

## Gate 1: snapshot

```text
$ git -C ../stations-gusts rev-parse --absolute-git-dir
/work/stations/.git/worktrees/stations-gusts      <- differs from the common dir: linked worktree
$ git -C ../stations-gusts branch --show-current
feature/gust-smoothing
$ git -C ../stations-gusts status --porcelain=v1 -uall
?? notes/units-question.md                         <- Lina's note, exists only here
$ git worktree list --porcelain                    <- main checkout /work/stations on main, clean
$ git rev-parse -q --verify MERGE_HEAD             <- nothing in progress
```

Done when: linked worktree on `feature/gust-smoothing` at `7c1e0a4`; one untracked file owned by
Lina; main checkout clean on `main`; no operation in progress.

## Gate 2: the project's check, on the candidate

```text
$ cd ../stations-gusts && npm test
Tests: 58 passed, 58 total
```

## Gate 3: classify and authorize

| Command | Effect | Authorized by |
| --- | --- | --- |
| `git switch develop` in the clean main checkout | local reversible | "merge it locally" |
| `git merge --no-ff --no-commit feature/gust-smoothing` | records history (only if committed) | "merge it locally" |
| `git commit --no-edit` | records history | "merge it locally", only if green |
| `git worktree remove ../stations-gusts` | discards a checkout | "clean up the worktree", only if green |
| `git branch -d feature/gust-smoothing` | deletes a merged branch | "clean up ... branch", only if green |
| `git pull` | would bring in unasked remote commits | nobody: not run |

Base: `develop`, because CONTRIBUTING says feature branches start from it and
`git log --oneline develop..feature/gust-smoothing` lists only the three gust commits, while
`main..feature/gust-smoothing` also lists eleven develop commits.

## Gate 4: branch-integration

```text
$ git rev-parse develop
4f02b9d
$ git switch develop
$ git merge --no-ff --no-commit feature/gust-smoothing
Automatic merge went well; stopped before committing as requested
$ npm test
FAIL test/gusts.test.js > smooths a 3-sample window: expected 12.4, received 12
Tests: 1 failed, 61 passed, 62 total
$ git merge --abort                    <- MERGE_HEAD exists and the merge is ours
$ git rev-parse develop
4f02b9d                                <- base unchanged
```

`develop` gained "Round wind speeds to whole km/h (OPS-19)" after the branch started; the gust test
expects one decimal. That is a product decision, not something to fix silently.

## Gate 5: observe; cleanup is skipped

Red stops cleanup: the worktree, the branch and `notes/units-question.md` stay.
`git worktree list` still shows `/work/stations-gusts [feature/gust-smoothing]`.

## Gate 6: the reply

> The merge into `develop` is not done: with OPS-19's rounding on `develop`, the gust smoothing test
> fails (expected 12.4, got 12). I undid my unfinished merge, so `develop` is still at `4f02b9d`,
> and I kept the worktree, the branch and your note. Should gusts keep one decimal, or should the
> test follow the new rounding?

```text
Request: "Merge it locally and clean up the worktree and branch. Don't push."
State before: /work/stations-gusts, linked worktree on feature/gust-smoothing at 7c1e0a4; untracked notes/units-question.md (Lina's)
Check: npm test on 7c1e0a4 -> 58 passed
Actions: git switch develop; git merge --no-ff --no-commit (authorized by "merge it locally"); git merge --abort after red
Observed: npm test on the merged tree -> 1 failed (smooths a 3-sample window: expected 12.4, received 12), 61 passed; develop still 4f02b9d
Kept: worktree /work/stations-gusts, branch feature/gust-smoothing, notes/units-question.md, because the merged tree is red
Not done or not verified: merge commit, worktree removal and branch deletion, pending the rounding decision (keep one decimal, or update the test to OPS-19)
```

## What the anti-pattern would have done

Merged and committed, called the failure flaky, removed the worktree with `--force` (deleting
Lina's only copy of her note) and deleted the branch with `-D` because "the user asked for
cleanup", leaving a red `develop` and nothing to recover the work from but the reflog.
