# Set up an isolated worktree

Internal Andino resource under `andino-git-skills`. Loading it changes neither tools nor
permissions.

## Purpose

Give new work its own checkout so the user's current branch, unfinished edits and other
worktrees stay exactly as they were, and hand over a workspace whose test baseline is known.
Detect existing isolation first, prefer the host's own worktree tool, fall back to
`git worktree`, and never fight the harness.

## Trigger and non-trigger

Use when work needs its own branch and checkout, when the user asks for an isolated workspace,
or when a session resumes in a worktree and must find out where it is.

Do not use for: read-only questions, or work the user wants done in the current checkout.
Finishing and removing worktrees belongs to [branch-integration](../branch-integration/guide.md).

## Procedure

1. **Find out where you are.** Run, in the current checkout:

   ```bash
   git rev-parse --show-toplevel
   git rev-parse --absolute-git-dir
   git rev-parse --path-format=absolute --git-common-dir
   git rev-parse --show-superproject-working-tree
   git branch --show-current
   git worktree list --porcelain
   git status --porcelain=v1 -uall
   ```

   | Observation | Workspace |
   | --- | --- |
   | git dir equals common dir | ordinary checkout |
   | git dir differs, superproject empty | linked worktree |
   | superproject printed | submodule: treat as an ordinary checkout of that repository |
   | branch name empty | detached HEAD (often a host-created worktree) |

   Done when: you can state the workspace type, the branch or detached SHA, every dirty and
   untracked path with its owner (the user's, yours, generated), and the other worktrees.
2. **Reuse before creating.** Already in a linked worktree on the branch the work needs, or the
   user named an existing one: use it and go to step 5. Creating a branch or worktree needs the
   user's request or a project rule that asks for isolation; otherwise offer it in one line and
   work where you are if they decline. Done when: you are reusing a named worktree, or you have
   the words that authorize a new one.
3. **Choose the place.** Take the first that applies:
   1. a path the user gave;
   2. a location the project's own instructions name (README, CONTRIBUTING, `AGENTS.md`,
      `CLAUDE.md`);
   3. an existing `.worktrees/` at the repository root, then `worktrees/`;
   4. the host's own worktree tool, when it has one (`EnterWorktree`, a `/worktree` command, a
      `--worktree` flag) and its branch behaviour fits what the user allowed: it places, tracks and
      cleans up the worktree itself, and a manual `git worktree add` beside it creates state the
      host cannot see;
   5. `.worktrees/<branch-name>` at the repository root.

   For a folder inside the repository, check it is ignored: `git check-ignore -q <folder>`. Exit 1
   means it would show up as untracked: add one line with the folder to `.git/info/exclude`
   (local to this clone, never committed) and check again. Do not edit and commit `.gitignore` on
   the user's branch unless they ask. Make sure the target path does not exist and is not in
   `git worktree list`. Done when: you have an absolute path, `git check-ignore -q` exits 0 for it
   (or it lies outside the repository), and nothing occupies it.
4. **Create it from the right base.** The base is the commit the user named, or the current tip
   of the branch they named; record `git rev-parse <base>`.

   ```bash
   git worktree add <absolute-path> -b <new-branch> <base>
   ```

   `git worktree add` starts from committed content only: the user's uncommitted edits stay in
   their checkout and are not copied. Never stash, commit or move them to make room. Check
   `git -C <path> status --porcelain` is empty and the original checkout's `git status
   --porcelain=v1 -uall` is identical to the snapshot from step 1. If creation is refused
   (permission or sandbox), say so and work in the current checkout only when it is suitable and
   allowed. Done when: `git worktree list` shows the path on the new branch at the recorded base,
   and the user's checkout is unchanged.
5. **Set up and take the baseline inside the worktree.** Run only the setup the project documents
   (its README or CONTRIBUTING install step, within what the user allowed), then the project's own
   test command from inside the worktree. Name every failure and check the project's notes for
   known issues; do not fix them here. A runner error ("command not found", "no tests ran") is not
   a baseline: find the documented command. Done when: you have the command, the counts, and each
   failing test named as known (with its issue reference) or unexplained.
6. **Report it ready** with the block below. When the baseline has unexplained failures, say so
   and ask whether to start anyway. Done when: every line of the block is filled from output you
   observed in steps 1 to 5.

```text
Worktree ready: <absolute path>
Branch: <name>, from <base branch> at <short sha>
Ignored by: <.git/info/exclude line | existing rule | outside the repository> (git check-ignore exit 0)
Baseline: <command> -> <N passed, M failed>; failures: <test names and known-issue ids>
Left as they were: <the user's dirty and untracked paths; other worktrees>
```

## Quick reference

| Situation | Action |
| --- | --- |
| Already in a linked worktree on the right branch | Reuse it (step 2) |
| In a submodule | Treat it as an ordinary checkout |
| The user or project names a location | Use it |
| `.worktrees/` and `worktrees/` both exist | Use `.worktrees/` |
| The host has a worktree tool | Use it |
| The folder is not ignored | Add it to `.git/info/exclude`, never commit `.gitignore` unasked |
| The user has uncommitted edits | Leave them; `git worktree add` does not copy them |
| Creation refused by the sandbox | Report it; work in place only when suitable |
| Baseline tests fail | Name each failure, known or not; ask before building on unexplained ones |

## Shortcuts that break isolation

| Shortcut | What happens instead |
| --- | --- |
| "I'm obviously not in a worktree." | Run step 1. Host-created worktrees and submodules both fool a glance. |
| "`git worktree add` is quicker than finding the host's tool." | The host loses track of a worktree it did not make. Use its tool when it has one. |
| "The folder is surely ignored." | `git check-ignore -q` decides. An unignored worktree shows up as untracked in the main checkout. |
| "I'll commit a `.gitignore` line on main first." | That is a commit the user did not ask for on their branch. Use `.git/info/exclude`. |
| "I'll stash the user's edits so the tree is clean." | Their edits never block `git worktree add`. Leave them alone. |
| "That old worktree under `.worktrees/` looks abandoned." | It is not yours unless this task created it or the user said so. Leave it. |
| "The baseline can wait." | A failure found later cannot be told apart from one you caused. |

## Permission boundary

Creating a branch or a worktree needs the user's request or a project rule; this guide grants
neither. No commit, push, install beyond the documented setup, or cleanup of other worktrees
happens here.

## Provenance

Adapted from Jesse Vincent's `using-git-worktrees` (obra/superpowers bc86802, MIT): detecting
existing isolation, the submodule guard, preferring the host's tool, the location order, the
`git check-ignore` check, the baseline and the ready report. Ignoring through `.git/info/exclude`
instead of a `.gitignore` commit, leaving the user's edits untouched and ownership by record are
Andino's. Notices: [license](../../references/license.md).
