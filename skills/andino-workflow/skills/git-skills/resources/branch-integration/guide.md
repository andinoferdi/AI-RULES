# Finish a branch: merge, push, open a PR, keep or discard

Internal Andino resource under `andino-git-skills`. Loading it changes neither tools nor
permissions.

## Purpose

Take finished work on a branch to the place the user wants it, prove the result works there, and
leave nothing behind that the user still needs. The order is fixed: verify the candidate, find its
base, settle the action, carry it out and test the result, clean up only what a green result
allows, report. Most damage in this area comes from skipping a test or cleaning up after a red
one, not from not knowing the commands.

## Trigger and non-trigger

Use when the work on a branch is done and it must be merged, pushed, opened as a PR, kept or
thrown away, or when a merge, push or cleanup went wrong.

Do not use for: writing the commits themselves ([change-hygiene](../change-hygiene/guide.md)),
the PR text ([pr-draft](../pr-draft/guide.md)), or setting up a worktree
([workspace](../workspace/guide.md)).

## Procedure

Work through the gates in order and keep the output each **Done when** line names; the report
quotes it.

1. **Verify the candidate on its own tree.** In the candidate's checkout run
   `git status --porcelain=v1 -uall`, check for an operation in progress
   (`git rev-parse -q --verify MERGE_HEAD`, `.git/rebase-merge`, `.git/rebase-apply`), and record
   `git rev-parse HEAD`. Uncommitted changes that belong to the work go through change-hygiene
   first; other people's files stay where they are. Then run the project's own test command, the
   one in its README, CONTRIBUTING, Makefile, `package.json` or CI config. A "command not found",
   "no tests ran" or a different runner than the project uses is not a result: find the right
   command. Done when: you have the candidate SHA and the test output on that SHA. If any test
   fails that did not fail on the base, stop here and report the failures; do not offer
   integration options.
2. **Find the base from evidence.** In this order: the user's words or the accepted plan, spec or
   ticket; branch notes in the repository (a plan file naming the base, `branch.<name>.description`);
   the fork point (`git merge-base <candidate> <base>` for each plausible base, and
   `git log --oneline <base>..<candidate>` to see which base gives only the candidate's own
   commits). A tracking branch or the repository's default branch is a clue, not proof. When two
   bases stay plausible, ask and keep everything as it is meanwhile. Done when: you can write
   "Base: `<branch>` at `<sha>`, because `<evidence>`".
3. **Settle the action.** Use the user's words: "merge it" is a local merge, "push" is a push only,
   "open a PR" is a push plus a PR, "clean up" covers the worktree and branch of this candidate
   only. When the choice is open, show exactly this menu and wait:

   ```text
   The work on <branch> is verified (<test command>: <result>). What should happen to it?
   1. Merge it into <base> locally
   2. Push it and open a pull request against <base>
   3. Keep the branch as it is
   ```

   For a detached HEAD (a worktree the host created), offer only: 1. push it as a new branch and
   open a pull request, 2. keep it as it is. Discarding is never on the menu; it happens only when
   the user asks for it. Done when: the action, its destination and the user's authorizing words
   are written down.
4. **Carry it out and test the result.** Follow the matching row of
   [Carrying out each action](#carrying-out-each-action). Done when: the resulting state is
   observed (merge commit and test output on the merged tree, remote SHA equal to the local one,
   PR URL or body file) or the action stopped with the state preserved and the reason recorded.
5. **Clean up only after a green result.** Cleanup runs only after a merge whose merged tree
   passed the tests, or after a confirmed discard, and only for the candidate's own worktree and
   branch. Follow [Cleanup](#cleanup). A push, a PR or "keep" leaves the worktree in place: review
   fixes happen there. Done when: `git worktree list` and `git branch --list <branch>` show what
   was removed and what was kept, each with its reason.
6. **Report** with the template in [Output](#output). Done when: every line is filled, and every
   step that did not happen says why and what the user needs to decide.

## Carrying out each action

### Merge locally

1. Find where the base is checked out: `git worktree list --porcelain`. Merge in that checkout. If
   the base is not checked out anywhere, use a checkout whose `git status` is clean and switch it
   with `git switch <base>`; never switch a checkout that holds someone's uncommitted work.
2. Record the base before touching it: `git rev-parse <base>`. Do not run `git pull`: remote
   changes the user did not ask for stay out. A `git fetch` to look is fine.
3. Merge without committing, so the result can be tested before it exists as history:

   ```bash
   git merge --no-ff --no-commit <candidate>
   <project test command>
   ```

4. Green: `git commit --no-edit`, then record `git rev-parse HEAD` and confirm
   `git merge-base --is-ancestor <candidate> <base>` exits 0.
   Red, or conflicts you were not asked to resolve: `git merge --abort` (it is valid because
   MERGE_HEAD exists and the merge is your own), confirm `git rev-parse <base>` equals the recorded
   SHA, and report the failing tests with their output. The base is unchanged and nothing needs
   recovery. Keep the worktree and the branch.
5. If a merge commit already exists (someone committed it, or the project requires a plain
   `git merge`) and the merged tree is red: leave it and report. Offer the user, with SHAs:
   revert it (`git revert -m 1 <merge-sha>`, safe once shared), fix forward on the base, or move
   the base back to `<recorded sha>`. Moving a branch back (`git reset --hard`, `git update-ref`)
   rewrites history and runs only on the user's words. Never `git merge --abort` without
   MERGE_HEAD.

When the project requires fast-forward merges, test the candidate rebased on the current base in
its own worktree first, then `git merge --ff-only <candidate>`; say so in the report.

### Push

1. Check the remote and the destination: `git remote -v`, `git ls-remote <remote>
   refs/heads/<branch>`.
2. Push the verified SHA by name: `git push <remote> <sha>:refs/heads/<branch>` (add `-u` when the
   local branch should track it).
3. Verify: `git ls-remote <remote> refs/heads/<branch>` prints the same SHA. Report that line.
4. Rejected as non-fast-forward: someone pushed first. `git fetch <remote>`, then read what arrived:
   `git log --oneline <branch>..<remote>/<branch>` and `git diff <branch>...<remote>/<branch>`.
   Notes in those commits can change the work (a blocker, a request); carry them into the report
   and the PR. Then either integrate (rebase your unpublished commits onto the remote branch, or
   merge it), rerun the tests, and push again; or stop and report what the remote has. Never force
   a push to get past a rejection. A force push runs only on the user's explicit words, and then as
   `git push --force-with-lease=<branch>:<expected-sha>`.

### Push and open a pull request

Push as above, then write the body with [pr-draft](../pr-draft/guide.md). Create the PR with the
forge's CLI (`gh pr create`, `glab mr create`) only when the user authorized creating it;
otherwise save the body where they asked and give the compare URL the push printed. A failed PR
creation does not undo the verified push: report both. Keep the worktree.

### Keep

Report the branch, its SHA and the worktree path. Change nothing.

### Discard (only when the user asks)

List what will be lost, then wait for the user to type `discard`:

```text
This permanently deletes:
- branch <name> and its commits not on <base>: <git log --oneline <base>..<branch>>
- the worktree at <path>, including files that exist only there: <git status --porcelain -uall>
Type 'discard' to confirm.
```

"Yes", "clean it up" or "get rid of it" is not the typed word. After it arrives: Cleanup below,
then `git branch -D <branch>`.

## Cleanup

1. Capture the worktree path before you leave it (`git rev-parse --show-toplevel`), then run
   cleanup from another checkout.
2. Own it: clean only the candidate's worktree that this task created or the user named. A folder
   name such as `.worktrees/x` is not proof that a worktree is yours.
3. Look first: `git -C <path> status --porcelain -uall`. Modified or untracked files exist only
   there. List them and ask whether to commit them to the branch, move them into another checkout,
   or delete them. When nobody can answer, keep the worktree and say why.
4. `git worktree remove <path>` without `--force`. A refusal means files are at stake: go back to
   step 3; never add `--force`. Confirm with `git worktree list`.
5. `git branch -d <branch>`. If git refuses because the branch is not fully merged, stop and report;
   `-D` belongs to a confirmed discard only.
6. Leave other worktrees, stale or not, alone. `git worktree prune` touches every stale entry in the
   repository and needs its own request.

## Quick reference

| Action | Tests on result | Pushes | Keeps worktree | Deletes branch |
| --- | --- | --- | --- | --- |
| Merge locally | yes, before the merge commit | no | only if red | `-d`, only if green |
| Push | candidate already green | yes | yes | no |
| Push and open a PR | candidate already green | yes | yes | no |
| Keep | candidate already green | no | yes | no |
| Discard (asked for) | no | no | no | `-D` after typed `discard` |

## Shortcuts that break finishing

| Shortcut | What happens instead |
| --- | --- |
| "pytest isn't installed, so I can't run the tests." | The project names its own command. Find it; a missing runner is not a test result. |
| "Tests passed earlier in the session." | Only the tree they ran on is proven. Test the candidate now and the merged tree after. |
| "The tests fail after the merge, but the user asked for cleanup." | Red stops cleanup. Keep the worktree, the branch and its files; report the failure. |
| "`-d` refused, so `-D`." | The refusal says the branch is not merged where git can see it. Stop and report. |
| "The base is obviously main." | Check the plan, the notes and the fork point. A wrong base can look green. |
| "Pull first so the merge is current." | Remote commits nobody asked for enter the base untested. Fetch to look, never pull. |
| "The push was rejected; force it." | The remote has work you have not read. Fetch, read it, integrate or stop. |
| "The worktree is under `.worktrees/`, so it is ours to delete." | Ownership is recorded, not read from a path. |
| "The PR is open, so the worktree is clutter." | Review fixes happen there. It stays until the work lands. |
| "I'll undo my merge with `reset --hard`." | Test with `--no-commit` and `git merge --abort`; a completed merge is the user's call. |

## Output

```text
Candidate: <branch> at <sha> in <path>; tests: <command> -> <result>
Base: <branch> at <sha before> (evidence: <plan line, note or fork point>)
Action: <merge | push | push and PR | keep | discard>, authorized by "<user words>"
Result: <merge commit <sha> | merge aborted, base still at <sha> | remote <ref> = <sha> | PR <url or body path>>
Tests on the result: <command> -> <result, failing tests named>
Cleanup: worktree <removed | kept: reason>; branch <deleted with -d | kept: reason>
Remote notes read: <commits from others and what they say, or none>
Needs you: <each open decision with its options and SHAs, or nothing>
```

## Permission boundary

Each of merge, push, PR creation, worktree removal and branch deletion is a separate action that
needs the user's words for it; earlier words for the same scope count. Verification grants no
authority. Nothing here authorizes `git pull`, a force push, `reset --hard`, `--force` removal or
`-D` without the user's words for that exact action.

## Provenance

Adapted from Jesse Vincent's `finishing-a-development-branch` (obra/superpowers b36e082, MIT):
the verify, detect, choose, execute, clean up order, the option menus, the typed `discard`
confirmation, refusing `--force` on removal and the rationalization table. The test-before-commit
merge, the evidence order for the base, the no-pull rule, ownership by record and the rejected-push
procedure are Andino's. Notices: [license](../../references/license.md).
