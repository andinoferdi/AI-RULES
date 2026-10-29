# Refine one dependency-aware implementation plan

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Turn accepted requirements into verifiable vertical slices without competing task state.

Keep the active Andino plan's `LITE`, `STANDARD`, or `DEEP` density proportional to scope and risk. Refine only the decisions needed to execute and verify the accepted work; do not force a deep plan for a small change.

## Trigger and non-trigger

Use when: Accepted multi-step work lacks exact interfaces, dependency order or verification.

Do not select for: Simple targeted edit or already complete accepted graph ready to execute.

## Prerequisites

Locate active Andino plan/checkpoint/spec/constraints, existing evidence and drift.

## Procedure

1. Map each accepted requirement and decision to an observable outcome and owning boundary. Retain current decisions/completed evidence; never overwrite a different incomplete ticket.
2. Choose independently testable vertical slices; fold setup/config/docs into the slice they enable. Split where one deliverable could be rejected while another passes.
3. Inspect the relevant repository and spec before recording exact paths, interfaces or commands. For each task, record owned files, consumed/produced signatures and evidence source when verified; if unknown, state the uncertainty and make dependent work wait for verification. Add dependencies, concrete acceptance cases, focused commands and expected signals.
4. Validate directed acyclic graph and compatible producer/consumer names/types. Missing node/cycle is a defect; shared write files serialize otherwise independent tasks.
5. Put uncertain/high-risk seams early. Checkpoints follow meaningful dependency boundaries; failure conditions and review-focus inputs implied by the spec get an observable check in the owning task.
6. Self-review requirement coverage, accepted decisions, repository constraints, task consistency, verified interfaces, independent oracles, integration gates and proportion. Update the existing plan's single `NEXT ACTION`. Tracker designation does not authorize publishing issues or a duplicate checklist.

## Ownership

When this plan is accepted and execution is authorized, hand off to
[plan-execution](../plan-execution/GUIDE.md) for the next dependency-ready task.
A planning-only request ends with the plan; acceptance of a plan does not by itself
grant implementation or publication authority. Reuse the same Andino checkpoint.

Andino owns selection, depth, scope, the existing durable checkpoint, delegation and DONE. Parent owns shared artifacts/final acceptance. This guide cannot invoke denied/manual siblings or establish another lifecycle.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

One refined plan with requirement→task map, graph/interfaces/ownership, acceptance commands, risks and NEXT ACTION.

## Verification

Topological order satisfies dependencies; reject cycles/dangling tasks. Shared files cannot occupy same write frontier.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "tasks": [
    {
      "id": "create",
      "deps": [],
      "files": [
        "store.py"
      ],
      "produces": [
        "create(name)->id"
      ],
      "consumes": []
    },
    {
      "id": "list",
      "deps": [
        "create"
      ],
      "files": [
        "store.py",
        "test_list.py"
      ],
      "produces": [
        "list()->names"
      ],
      "consumes": [
        "create(name)->id"
      ]
    },
    {
      "id": "audit",
      "deps": [
        "create"
      ],
      "files": [
        "audit.py"
      ],
      "produces": [
        "audit(id)->record"
      ],
      "consumes": [
        "create(name)->id"
      ]
    }
  ],
  "bad_cycle": [
    {
      "id": "a",
      "deps": [
        "b"
      ],
      "files": []
    },
    {
      "id": "b",
      "deps": [
        "a"
      ],
      "files": []
    }
  ],
  "dangling": [
    {
      "id": "a",
      "deps": [
        "missing"
      ],
      "files": []
    }
  ]
}
```

Anti-pattern: All database then all API then all UI then connect; invented bodies where engineer can decide; second task list competing with plan.

## Fallback

Isolate material unresolved interface decision; continue independent work. Without tracker access keep an unpublished draft in the existing plan.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- addyosmani/agent-skills:skills/planning-and-task-breakdown/SKILL.md
- obra/superpowers:skills/writing-plans/SKILL.md

- addyosmani/agent-skills:references/definition-of-done.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
