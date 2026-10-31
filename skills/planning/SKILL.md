---
name: andino-planning
description: Turn accepted requirements into implementation-ready tasks with exact code/artifact changes, decision-bearing snippets, interfaces, dependencies and concrete checks a fresh executor can follow without chat history.
---

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
Before drafting implementation task detail, read
[the worked examples](resources/worked-example.md), including the change blocks.
They show the required output shape, not optional inspiration.

## Ready tasks carry the change

A milestone such as "build the API", "restore the scene" or "add validation"
is a roadmap item, even with an acceptance paragraph. For every implementation
task offered as ready, the saved plan must answer **where, what changes into what,
and how will we know?** Write a task-local **Change Specification**:

- Inspected starting state: exact file and symbol/section anchor, with relevant
  existing behavior. Mark new files/interfaces as proposed. Lines are optional
  navigation aids; use an anchor that survives nearby edits.
- Operation and result for each owned file: add/replace/remove which code, config
  or text; exact names, signatures, imports, literals and error/side-effect rules
  that constrain the change. "Follow the existing pattern" names the reference
  file/symbol and the differences, not an instruction to redesign the task.
- Decision-bearing change blocks: small before/after snippets, a diff, replacement
  text or a code skeleton with the non-obvious logic filled in. Include them for
  algorithms, formulas, schema/enums, exact copy/config and other choices that
  prose plus signatures leaves open. Include concrete test assertions/fixtures
  as code for executable checks. Routine bodies need no transcription.
- Ordered actions and runnable proof: working directory, prerequisites, exact
  commands/manual operations, inputs and observable expected results.

Plan density never relaxes these essentials. A task is not ready while a material
behavior, interface or change is still "appropriate", "as needed" or UNKNOWN.
State that readiness separately from TODO/IN_PROGRESS work status. For unresolved
work keep a roadmap/discovery item, its missing decision and a bounded exit check;
populate dependent Change Specifications with the resolved contract before calling
them ready. Known decisions must not be postponed to the executor merely to keep
the plan short. Proportional detail means removing repeated context, not decisions.

## Procedure

1. **Ground the next executor.** Inspect the relevant files, callers, test setup
   and repository commands. Record accepted outcomes with exact values and a short
   approach explaining boundaries and tradeoffs. Distinguish existing inspected
   interfaces from proposed ones. Keep unverified facts `UNKNOWN` with a bounded
   discovery action; dependent work waits for its exit criterion. During planning,
   edit the plan rather than application source; code snippets inside the plan are
   encouraged when they specify the change. Never report planned checks as run.
2. **Choose deliverables.** Prefer thin paths through the real entrypoint to the
   observable result. Include setup, configuration and documentation in the slice
   they enable. A necessary foundation or discovery task is valid when it has its
   own acceptance and explicitly unblocks a named consumer. Split a task when its
   outcomes can be reviewed independently or its uncertainty prevents one focused
   implementation/test cycle. File count is a warning, not a mandatory split.
3. **Make each task executable.** Record its requirement, dependencies, owned files,
   consumed/produced interfaces where relevant, concrete acceptance, Change
   Specification and action sequence. For behavior changes, include named tests
   with decisive assertion/fixture code, then expected RED, the specified change
   and focused GREEN. Align with
   the canonical TDD guide: a meaningful failing assertion distinguishes missing
   behavior from broken setup. For static documents/configuration, use an
   appropriate artifact check. Name working directory, prerequisites, exact command
   and expected signal. A missing test suite calls for a concrete supported check
   or justified test-setup task, never invented scripts or silently omitted proof.
   Commit steps appear only under existing authorization.
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
   Run a **fresh-executor check**: using only the saved plan and its reachable
   repository/spec references, can someone locate each ready edit, write it without
   choosing material behavior, and verify it? Fix missing changes/assertions inline.
   A detailed snippet must still agree with current source and accepted requirements;
   detail alone is not correctness. Label remaining roadmap items honestly.
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
tasks containing concrete change instructions and code/text where decisions need
it, verified or explicitly proposed interfaces, risks, current state and a
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
