# Git Skills: Workspace, Safety, Hygiene, Integration, and PRs — Comprehensive Guide

Internal method ID: `andino-git-skills` (alias: `git-skills`).

## 1. Purpose and Architectural Overview

`andino-git-skills` unifies the repository and version control craft across the Andino Workflow ecosystem. It coordinates workspace isolation, destructive operation prevention, commit hygiene, branch integration, and pull request generation without forcing a rigid, monolithic lifecycle.

### Core Philosophy: Permission-Scoped Operation

Git operations are divided strictly into non-mutating inspections and permission-gated mutations:
- **Inspections (Permitted without ceremony)**: `git status`, `git log`, `git diff`, `git branch --list`, `git rev-parse`.
- **Mutations (Explicit human authorization required)**: `git checkout -b`, `git commit`, `git merge`, `git push`, `git worktree add`, `git worktree remove`, `git branch -d`.
- **Prohibited Automatic Actions**: Automatic hard resets (`git reset --hard`), blind remote synchronizations (`git pull`), unconfirmed branch deletions (`git branch -D`), and forced worktree removals (`--force`).

---

## 2. Select a resource, not a second lifecycle

Load only the resource matching the current need. A direct resource selection uses
that procedure and current authority; it does not run this parent's other modes,
reopen accepted requirements or require a second execution plan.

| Current need | Resource | Exclusion |
| :--- | :--- | :--- |
| Workspace isolation, safe worktrees, concurrent tasks | [workspace](resources/workspace/guide.md) | In-place single-branch edits without concurrency |
| Destructive operation prevention, commit/reset safety guards | [operation-safety](resources/operation-safety/guide.md) | Standard everyday git status/add/diff |
| Branch hygiene, atomic commit progression, branch naming | [change-hygiene](resources/change-hygiene/guide.md) | Unrelated project build/test failures |
| Branch integration, local merge, completed-merge recovery | [branch-integration](resources/branch-integration/guide.md) | Active feature implementation before green test suite |
| Pull request drafting, blast radius, verification proof | [pr-draft](resources/pr-draft/guide.md) | Unpushed local experiments without branch tracking |

*Pre-commit verification scripts, lint/type checks, and git pre-commit hook recipes are owned canonically by CI/CD (resolve `skills/ci-cd-and-automation/resources/commit-checks/guide.md` from the installed `andino-workflow` root).*

---

## 3. The Five Core Operational Modes

### Mode 1: Workspace Isolation (`workspace`)
Use when concurrent tasks, exploratory spikes, or isolated reviews require separate working directories.
- Inspects repository topology (`git rev-parse --git-dir` vs `--git-common-dir`).
- Allocates named worktrees outside dirty paths.
- Records explicit worktree ownership in task session metadata.
- Preserves external or unowned worktrees without modification.

### Mode 2: Operation Safety (`operation-safety`)
Use before running sensitive git commands or recovering from git errors.
- Enforces dominant negative guards against unrecorded hard resets, destructive cleanups, and detached HEAD operations.
- Inspects staging state before index mutations.
- Provides non-destructive alternatives for index recovery and diff isolation.

### Mode 3: Change Hygiene (`change-hygiene`)
Use during implementation to maintain atomic, well-factored commit sequences.
- Establishes conventional commit prefixes (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
- Requires verifiable single-concern slices per commit.
- Prevents mega-commits containing mixed functional and formatting changes.

### Mode 4: Branch Integration (`branch-integration`)
Use when implementation and verification are complete, and candidate changes need integration.
- Gated behind a 100% green test suite on the candidate tree.
- Detects environment state and confirms base branch fork point with human partner.
- Presents locked dual-mode menu (interactive host dialog or locked 1/2/3 text menu).
- **Completed-Merge Safety**:
  - `git merge --abort` applies ONLY when `MERGE_HEAD` exists (uncommitted conflict state).
  - If the merge completed (merge commit created) or was a fast-forward, and post-merge tests fail:
    - Never execute automatic `git reset --hard` or history rewrites.
    - Preserve failure logs, candidate branch, and base HEAD.
    - Propose permission-scoped recovery options to the human partner.
- **Ownership-Based Cleanup**:
  - Clean only worktrees whose ownership was explicitly recorded by the active task.
  - Path naming (e.g. `.worktrees/`) never infers ownership. Unowned worktrees are preserved.
  - Refused removals with untracked files are never forced; surface files to the user.

### Mode 5: Pull Request Drafting (`pr-draft`)
Use when publishing a branch to a remote forge (GitHub, GitLab) for peer review.
- Generates structured PR summaries: context, blast radius, verification evidence, rollback instructions.
- Integrates with installed forge CLIs (`gh`, `glab`) or surfaces comparison URLs.
- Preserves the local worktree intact for addressing review feedback.

---

## 4. Modular Resources Index

- Workspace Isolation Guide: [resources/workspace/guide.md](resources/workspace/guide.md)
- Operation Safety Guide: [resources/operation-safety/guide.md](resources/operation-safety/guide.md)
- Change Hygiene Guide: [resources/change-hygiene/guide.md](resources/change-hygiene/guide.md)
- Branch Integration Guide: [resources/branch-integration/guide.md](resources/branch-integration/guide.md)
- Pull Request Drafting Guide: [resources/pr-draft/guide.md](resources/pr-draft/guide.md)

---

## 5. Provenance & Attribution

Adapted from:
- `obra/superpowers:skills/using-git-worktrees` and `finishing-a-development-branch` (MIT, Jesse Vincent 2025)
- `mattpocock/skills:skills/engineering/git-interactive` and `create-pr` (MIT, Matt Pocock 2026)

Substantive adapted material is covered under the MIT license terms in [references/license.md](references/license.md).
