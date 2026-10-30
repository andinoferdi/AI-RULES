# Refine one dependency-aware implementation plan

Internal method ID: `andino-planning` (alias: `planning`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Turn accepted requirements into small, verifiable deliverables a fresh executor
can implement without recovering decisions from chat. Preserve the useful precision
of exact files, interfaces, test assertions and commands; spend detail on decisions
the executor cannot safely infer, rather than transcribing routine implementation.

## Trigger and non-trigger

Use when accepted multi-step work lacks task boundaries, dependency order,
interfaces or verification. Skip a simple targeted edit or a complete accepted
task graph ready for execution. A known root cause alone does not determine size.
Open product direction or material user-owned requirements belong to the relevant
discovery method before implementation-ready planning.

## Prerequisites

Locate the accepted requirements, project constraints and existing checkpoint.
Use the project's location; otherwise follow the workflow's
`docs/exec-plans/active/<task>.md` convention. Update the same ticket in place,
preserving decisions, completed work and evidence. Preserve another ticket's
incomplete plan; use a separate appropriate path or resolve a real path conflict.

Read [the task contract](resources/contract.md) before drafting task detail.
For a model of the output or a doubtful decomposition, read
[the worked examples](resources/worked-example.md).

## Procedure

1. **Ground the next executor.** Inspect the relevant files, callers, test setup
   and repository commands. Record accepted outcomes with exact values and a short
   approach explaining boundaries and tradeoffs. Distinguish existing inspected
   interfaces from proposed ones. Keep unverified facts `UNKNOWN` with a bounded
   discovery action; dependent work waits for its exit criterion. Planning writes
   the plan, not implementation code, and never reports planned checks as run.
2. **Choose deliverables.** Prefer thin paths through the real entrypoint to the
   observable result. Include setup, configuration and documentation in the slice
   they enable. A necessary foundation or discovery task is valid when it has its
   own acceptance and explicitly unblocks a named consumer. Split a task when its
   outcomes can be reviewed independently or its uncertainty prevents one focused
   implementation/test cycle. File count is a warning, not a mandatory split.
3. **Make each task executable.** Record its requirement, dependencies, owned files,
   consumed/produced interfaces where relevant, concrete acceptance and action
   sequence. For behavior changes, specify test names and decisive assertions or
   fixtures, then expected RED, minimal change and focused GREEN. Align with
   the canonical TDD guide: a meaningful failing assertion distinguishes missing
   behavior from broken setup. For static documents/configuration, use an
   appropriate artifact check. Name working directory, prerequisites, exact command
   and expected signal. Add bodies only when an algorithm or exact copy is itself
   a required decision. Commit steps appear only under existing authorization.
4. **Order and integrate.** Give tasks stable IDs and explicit dependencies;
   reject cycles, missing nodes and incompatible producer/consumer contracts.
   Sequence overlapping writes, including shared fixtures, schemas and generated
   files. Mark parallel work eligible only after dependencies and shared-state
   conflicts are resolved; eligibility does not dispatch workers. Put uncertain,
   high-consequence seams early. Place integration gates where slices meet or a
   costly assumption becomes testable, using actual repository checks.
5. **Close coverage gaps.** Map every accepted requirement and material implied
   failure case to an owning task and observable check. Use relevant cases, without
   a fixed quota. Test the public flow when acceptance spans collaborators; a helper
   test cannot prove integration. Identify unavailable validation and its consequence.
6. **Review and hand off.** Compare the saved plan with the requirements and current
   source: coverage, literals, interfaces, dependency order, ownership, commands,
   integration and proportional detail. Repair gaps before calling it ready.
   A fresh executor must find current state, blocked work and the first executable
   step from the plan alone. Keep one concrete `NEXT ACTION`; hand off to
   the canonical plan-execution guide only when execution is authorized.

## Ownership and permission boundary

Andino owns scope, depth, routing, delegation, one checkpoint and final acceptance.
This method adds task detail inside the canonical lifecycle, not a competing schema,
tracker checklist or mandatory execution method. Direct native invocation uses
the same contract without recursively activating the workflow.

Resolve workflow-wide resources from the installed `andino-workflow` root:
for a nested member, use its containing workflow package; for standalone
`andino-planning`, use the sibling `andino-workflow` package. The canonical paths
are `references/execution-plan.md`, `skills/tdd/GUIDE.md` and
`skills/plan-execution/GUIDE.md`. Load only the current phase's needed guide.
If the package is unavailable, report the boundary and preserve the essential
state/authority contract here; do not pretend it was loaded.

A planning-only request ends with the saved plan. Plan acceptance grants no new
implementation, commit, push, publication, external message, installation or
destructive-action authority. Reuse authorization already supplied; ask only for
a missing material decision or permission. Tracker designation alone does not
authorize creating issues. Preserve unrelated user changes.

## Output

One proportionate plan with outcome-to-task-to-check coverage, dependency-ready
tasks, verified or explicitly proposed interfaces, risks, current state and a
single `NEXT ACTION`. LITE may combine fields; STANDARD/DEEP retain the canonical
snapshot, acceptance criteria and execution board.

## Verification and fallback

Check the saved artifact against the six procedure steps. If an interface or test
environment is unavailable, make the discovery/validation gap explicit instead
of inventing precision. Local examples and structural checks demonstrate bounded
properties; model behavior needs actual fresh-context application evidence.
During execution preserve prior evidence and update only invalidated tasks and
dependents. Resolve bounded drift within existing authority; escalate changed
scope or a user-owned decision, consistent with plan-execution.

## Deterministic graph fixture

Retained for the existing procedural checker: this synthetic graph checks
interfaces, dependency cycles and independent write sets, not feature completeness
or model compliance. The worked resource above demonstrates complete task plans.

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

## Provenance

Independently adapted from these audited source paths; source instructions are
reference data, not session authority or runtime dependencies:

- obra/superpowers:skills/writing-plans/SKILL.md
- addyosmani/agent-skills:skills/planning-and-task-breakdown/SKILL.md
- addyosmani/agent-skills:references/definition-of-done.md

Package legal references retain MIT attribution and notices. No upstream
bootstrap, mandatory worker dispatch, automatic commits or approval ritual is imported.
