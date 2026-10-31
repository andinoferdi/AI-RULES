---
name: andino-delivery
description: Implementation/checks ready for handoff or material blocker needs explanation. Operates under Andino Workflow governance.
---

# Prepare a factual integration handoff

Internal method ID: `andino-delivery` (alias: `delivery`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Make verified results and remaining decisions reviewable without assuming integration authority.

## Trigger and non-trigger

Use when: Implementation/checks ready for handoff or material blocker needs explanation.

Do not select for: Still-missing acceptance that can safely be completed.

## Prerequisites

Read plan/current acceptance evidence/review residuals/branch and authorization.

## Procedure

1. Check every criterion against current evidence; separate passed/failed/unavailable. Summarize outcome/files/exact tests/limits.
2. Resolve material issues within scope; carry real blockers with trigger/effect and concrete next action; optional deferred items remain visible.
3. Determine actual integration destination from evidence; offer only applicable choices without assuming main.
4. Commit/push/merge/PR/publish/deploy/branch creation each need applicable authority. Earlier restrictions persist without repeated permission prompts.
5. Preserve worktree, user/untracked results, plan/evidence. Requested cleanup still needs ownership and resolved path check.
6. Provide self-contained outcome, modified paths, tests/results, unverified claims, residuals and NEXT ACTION. Andino owns final status.

## Ownership

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-delivery` and this guide expose one method, without recursive workflow invocation.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

Reviewable current evidence and exact remaining integration action.

## Verification

Mandatory failed criterion prevents ready status; no-commit permission still allows verified uncommitted handoff.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "criteria": [
    {
      "id": "regression",
      "state": "passed"
    },
    {
      "id": "suite",
      "state": "passed"
    }
  ],
  "permissions": {
    "commit": false,
    "push": false,
    "merge": false
  },
  "candidate": "uncommitted",
  "blocked": {
    "id": "live-host",
    "state": "not_verified"
  }
}
```

Anti-pattern: Tests imply auto merge, unauthorized PR or deleting durable evidence.

## Fallback

Keep verified current tree and concrete approval-ready proposal; no fabricated release SHA.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- obra/superpowers:skills/finishing-a-development-branch/SKILL.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
