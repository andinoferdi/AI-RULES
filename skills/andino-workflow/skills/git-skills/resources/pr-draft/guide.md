# Write a pull request description reviewers can act on

Internal Andino resource under `andino-git-skills`. Loading it changes neither tools nor
permissions.

## Purpose

Let a reviewer see what changed, why it is safe and what could go wrong, from the body alone. The
body shows the change instead of narrating it, backs every claim with a run you observed, and
says plainly when a merge cannot be undone. Writing the body is not permission to publish it.

## Trigger and non-trigger

Use when a branch needs a PR body, or an existing body is stale after new commits.

Do not use for: creating or merging the PR ([branch-integration](../branch-integration/guide.md),
with the user's words) or answering review comments.

## Procedure

1. **Read everything the reviewer will see.** The house template
   (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/*`, `docs/` or
   CONTRIBUTING), the ticket or plan the work came from, the full change
   (`git log --oneline <base>..<head>`, `git diff --stat <base>...<head>`,
   `git diff <base>...<head>`), and commits others pushed to the branch (`git fetch`, then
   `git log <head>..<remote>/<branch>`). Notes in those commits and in plan files can carry
   blockers. Done when: you have the template headings, the ticket id, every changed file and every
   note from others that bears on merging.
2. **Fit the house template.** Keep every heading it has, in its order, and fill each one. Put
   this guide's three parts where they fit: Summary under "What changed" or "Description",
   Evidence under "How it was tested", Merge danger under "Risk", "Rollback plan" or a heading of
   its own. With no template, use the default in [the worked example](resources/worked-example.md).
   Done when: every house heading has content and none was removed or renamed.
3. **Show the change in its smallest form.** Open with one sentence on why, then pick the one
   view that makes the point; two at most:

   | The change is about | Show it as |
   | --- | --- |
   | logic or an algorithm | pseudocode |
   | runtime control flow | a call tree |
   | UI structure | a component tree with the state that matters |
   | file ownership or a broad refactor | a shallow file tree |
   | components talking to each other | a Mermaid sequence or flow diagram |
   | what changes in a shape that already exists | a `diff` block shaped like that view |

   ```diff
    checkout(cart)
      price(cart)
   -  charge(card)
   +  if fraud_score(cart) > 0.8
   +    hold_for_review(cart)
   +    return
   +  charge(card)
   ```

   Keep only the calls, files and states the reviewer needs; place each view next to the sentence
   it supports; around 15 lines. Done when: the summary has a why sentence and one view a reviewer
   can check against the diff.
4. **Give evidence you observed.** For each behaviour the change claims, show before and after
   from real runs: the exact command and the lines that matter. A screenshot beats words for a
   visual change; test or console output is the standard otherwise. The "before" comes from the
   base: create a temporary detached worktree (`git worktree add --detach <tmp> <base>`), copy
   in the new or changed test files, run them and expect them to fail, then remove that worktree
   (you created it). When you could not observe the before state, write "Before: not observed"
   and why. Never write a result you did not see. Done when: every evidence line names a command
   and its observed output, or says "not observed" with the reason.
5. **State the merge danger.** Door: two-way when reverting the commit restores everything,
   one-way when something outlives a revert: dropped columns or tables, data rewritten by a
   migration, deleted stored files, messages or emails sent, external APIs called, packages or
   tags published. Name each one-way effect and say that `git revert` does not undo it. Blast
   radius: who or what is affected and how many, with the number from the repository (rows, users,
   callers, files) where it exists. Rollback: for a one-way door, the step that protects the data
   before merge or deploy (export, backup, feature flag), then how to restore. Put blockers from
   others' notes at the top, before the summary. Done when: door, blast radius and rollback are
   each stated, and every blocker is visible above the fold.
6. **Write it where the user asked.** Save the body to the named file, or keep it for the PR
   command the user authorized. Refresh it after any new commit. Done when: the file exists or the
   PR shows the body, and your reply says whether anything was published.

## Shortcuts that weaken a PR body

| Shortcut | What happens instead |
| --- | --- |
| "I'll use my own headings; the template is boilerplate." | Reviewers and bots read the house headings. Keep them all. |
| "Tests pass." | Name the command, the count and the test that proves the change, before and after. |
| "Every diagram type, to be thorough." | One view that makes the point. More views bury it. |
| "Small blast radius." | Count it. If you cannot, say what you could not count. |
| "Revert the PR to roll back." | Not for a one-way door. Protect the data first, then revert. |
| "The teammate's commit is just a doc note." | Notes carry blockers. Read every commit on the branch you did not write. |

## Fallback

When Mermaid will not render, use a call tree or a shaped diff. Missing evidence is labelled
missing, never filled in.

## Permission boundary

Drafting the body needs no permission. Pushing, creating the PR, posting comments and publishing
need the user's words for that action.

## Local resources

- [Worked example](resources/worked-example.md): a full body for a change with a one-way door,
  and the default template.
- [Credits](resources/credits.md): source of the visual menu.

## Provenance

Adapted from Matt Pocock's `pr` (mattpocock/skills e484a80, MIT), whose visual menu comes from Dex
Horthy's `show-me` (Humanlayer): the Summary, Evidence and Merge Danger template, the visual menu,
before/after evidence tiers, one-way and two-way doors and blast radius. Reading others' commits,
the base-worktree before run, data-first rollback and house-template mapping are Andino's.
Notices: [license](../../references/license.md).
