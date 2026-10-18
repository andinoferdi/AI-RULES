# Delegate disjoint work under parent ownership

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Use actual children only when independence, authority and benefit justify their cost.

## Trigger and non-trigger

Use when: Bounded independent tasks or materially useful independent review.

Do not select for: Related unknown failures, shared write state, missing authority/tool or cheaper inline work.

## Prerequisites

Read accepted graph/checkpoint; verify authorized exposed tool and benefit. Maximum three children, no nested spawning; pin workspace and ownership.

## Procedure

1. Compute ready frontier using verified producer evidence. Group related failures before splitting; normalize write paths and reject exact/ancestor overlap.
2. Choose at most three disjoint ready tasks. Brief each with outcome/spec pointer, exact scope, interfaces, constraints, commands, report path, no nested agents and no unapproved Git/environment mutation.
3. Track child identity/status in the same parent ledger. Return contract: DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED plus changed files, actual commands/results and residuals. Avoid whole-history prompts.
4. Keep useful independent work while children run; use bounded waits, no short repeated polling. Denial/missing tool means honest inline fallback, not fabricated dispatch or another-host bypass.
5. Inspect report and actual changed bytes, ownership, both review axes and integration. A worker success statement is insufficient; run meaningful cross-task checks when results join.
6. Fix/re-review only affected findings with changed evidence. At most two transient retries; three unsuccessful fixes require architecture reassessment. A loop cap never fulfills failed material acceptance.

## Ownership

Andino owns selection, depth, scope, the existing durable checkpoint, delegation and DONE. Parent owns shared artifacts/final acceptance. This guide cannot invoke denied/manual siblings or establish another lifecycle.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

Dispatch/no-dispatch rationale, graph/ownership, identities, reports, parent verification and residuals.

## Verification

Safe pair can run; dependency-not-ready, ancestor path collision, missing authority/tool cannot. No nested agents.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "tasks": [
    {
      "id": "api",
      "deps": [],
      "files": [
        "src/api.py"
      ]
    },
    {
      "id": "docs",
      "deps": [],
      "files": [
        "docs/api.md"
      ]
    },
    {
      "id": "ui",
      "deps": [
        "api"
      ],
      "files": [
        "src/ui.py"
      ]
    }
  ],
  "overlap": [
    {
      "id": "a",
      "deps": [],
      "files": [
        "src/shared"
      ]
    },
    {
      "id": "b",
      "deps": [],
      "files": [
        "src/shared/config.py"
      ]
    }
  ],
  "max_children": 3,
  "capability": true,
  "authorized": true
}
```

Anti-pattern: One child per failure count, shared-manifest concurrent writes, inherited permission escalation or automatic source implement-spec branches/merges.

## Fallback

Do work inline with same contract when benefit/tool/authority is absent. Supply missing evidence to blocked child; never redispatch unchanged repeatedly.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- mattpocock/skills:skills/engineering/implement-spec/SKILL.md
- obra/superpowers:skills/dispatching-parallel-agents/SKILL.md
- obra/superpowers:skills/subagent-driven-development/SKILL.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
