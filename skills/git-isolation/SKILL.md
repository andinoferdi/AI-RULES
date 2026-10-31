---
name: andino-git-isolation
description: Implementation needs isolation/branch-specific edits or resumed workspace reconciliation. Operates under Andino Workflow governance.
---

# Preserve user state and authorized isolation

Internal method ID: `andino-git-isolation` (alias: `git-isolation`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Choose correct existing workspace without unauthorized branch or state changes.

## Trigger and non-trigger

Use when: Implementation needs isolation/branch-specific edits or resumed workspace reconciliation.

Do not select for: Read-only explanation or suitable existing authorized checkout.

## Prerequisites

Inspect root/branch/Git-common dirs/superproject/worktrees/dirty paths and session permissions.

## Procedure

1. Different Git/common dirs can mean linked worktree; inspect superproject first to exclude submodule false-positive. Record named/detached state and lifecycle owner.
2. Reuse suitable current/attached worktree and explicit branch/location preference. Inspect actual state before creating anything.
3. Use native workspace tool only if its branch behavior fits authorization. If it forces a new branch under no-new-branch policy, choose authorized existing-branch mechanism or report the gap.
4. Resolve proposed absolute path; prevent collision with snapshots/user files/active worktrees. Never change .gitignore/create branch/commit for an upstream recipe.
5. Preserve dirty/untracked files; establish baseline with existing tooling. Denial does not permit edits in another branch's checkout.
6. Cleanup requires proven ownership/authority and preserved needed content. Path name does not prove ownership; never force dirty-file refusal.

## Ownership

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-git-isolation` and this guide expose one method, without recursive workflow invocation.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

Workspace/branch/submodule/dirty evidence, authorized path, baseline and lifecycle owner.

## Verification

Distinguish ordinary, linked and submodule; reject outside/colliding targets while preserving files.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "cases": [
    {
      "git_dir": "/repo/.git",
      "common": "/repo/.git",
      "superproject": "",
      "expected": "ordinary"
    },
    {
      "git_dir": "/repo/.git/worktrees/a",
      "common": "/repo/.git",
      "superproject": "",
      "expected": "linked"
    },
    {
      "git_dir": "/parent/.git/modules/a",
      "common": "/parent/.git",
      "superproject": "/parent",
      "expected": "submodule"
    }
  ],
  "allowed_root": "workspace",
  "safe": "workspace/isolated",
  "unsafe": "../outside",
  "protected": "workspace/upstream"
}
```

Anti-pattern: Auto -b, install, .gitignore commit, reset/clean or folder-name cleanup.

## Fallback

Block only branch-specific unsafe writes; continue correctly located/read-only independent work.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- obra/superpowers:skills/using-git-worktrees/SKILL.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
