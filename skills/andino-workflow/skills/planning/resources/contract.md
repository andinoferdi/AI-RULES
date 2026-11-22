# Planning task contract

## One checkpoint, proportional detail

The workflow's `references/execution-plan.md` and
`references/execution-plan-template.md` own document state. Resolve them from the
installed workflow root as described in the planning guide.
Add task contracts to that checkpoint's Detailed Execution section. If a project
already uses a different shape, preserve equivalent state and acceptance fields.
An external tracker can be an ordered index; keep one authoritative task status.

Choose density by uncertainty, consequence, coupling and handoff cost:

| Density | Useful detail |
| --- | --- |
| LITE | Objective, observable acceptance, constraints, current state, short actions, verification and NEXT ACTION; fields may share a paragraph. |
| STANDARD | Canonical header, Executive Snapshot, Objective, Acceptance Criteria, Execution Board, task contracts and NEXT ACTION. |
| DEEP | STANDARD plus the decision evidence, interface/state contracts, risk experiments, migration/rollback or staged gates warranted by the work. |

File counts, a fixed number of failure cases or a fixed checkpoint cadence do not
select a tier. Include architecture/stack only when they constrain the work.
More detail is useful when it removes a consequential choice for the executor.

## Execution readiness

Work status tracks progress; readiness describes whether a task is specified
enough to begin. Keep the canonical statuses unchanged. For implementation tasks,
record `Readiness: READY` only after source grounding, a complete Change
Specification and concrete proof. Otherwise use `Readiness: NEEDS_DETAIL` or
`Readiness: WAITING_ON D1` with the exact gap. Equivalent explicit project fields
are fine. A roadmap can mix ready and unresolved work, but cannot be handed off
as wholly implementation-ready. A discovery task can itself be READY when its
source/experiment, output artifact, exit criterion and blocked consumers are exact.

Discovery completion must replace dependent unknowns with decisions and change
instructions in this same plan. Do not merely mark D1 DONE and let consumers infer
what it discovered. Keep independent ready tasks moving within existing authority.

## Grounded task template

Use this inside the canonical plan, combining fields for simple tasks. Replace
placeholders with inspected facts, explicitly proposed decisions or a bounded
unknown. Existing symbols/commands need evidence; new files/signatures are labeled
proposed, not falsely described as already present.

````markdown
### T1 — Observable deliverable
Status: TODO
Readiness: READY / NEEDS_DETAIL / WAITING_ON D1 [resolve before handoff]
Requirements: R1 (exact accepted outcome/value)
Depends on: none
Owns: Modify `verified/path.py` (`inspected_symbol`); Test `tests/test_path.py`
Interfaces: consumes [inspected name/signature + source]; produces [proposed name/signature]
Acceptance: [literal input/state -> expected output/side effect; relevant failure case]

Change Specification:
- `verified/path.py::inspected_symbol`: currently [observed state];
  [add/replace/remove exact code/behavior, signatures and literal values].
- [Each other owned file: anchor, operation, resulting state; reference concrete
  pattern file/symbol if reused. Include the decisive code/diff/replacement below.]

```python
# Task-specific change, not generic "implement here" or an entire unrelated module.
[replace with the actual decision-bearing snippet before handoff]
```

Actions:
- [ ] Add `test_case_name` using [fixture/setup]; include its decisive assertion code.
- [ ] Run [focused command] from [working directory]; expect [specific missing-behavior assertion].
- [ ] Apply the specified changes at [exact anchors], using the change block above.
- [ ] Rerun [focused command]; expect [assertions pass, exit 0, nonzero test count].

Verification prerequisites: [runtime, fixture/service, environment; or none beyond repo setup]
Integration gate: [real command/public-flow check at the relevant boundary]
Result / Evidence: Not run — planned checks only.
````

Interfaces may be `none — no cross-task interface change`. Point to a producer's
contract instead of copying its implementation. For a new symbol, establish the
import/fixture first when needed so RED exercises the intended behavior; syntax,
missing tooling and broken imports are setup failures, not behavioral proof.
If RED may already pass, investigate existing coverage before inventing new code.
Static artifact tasks substitute inspect/change/validate for TDD.

Each ready task must let an executor locate the change, understand what to write
and run a discriminating check without redesigning a boundary. Write decisive
test assertions as code, using the repository's actual fixtures/imports. Full
test setup is needed only when it is not established by a named local reference.

Choose the smallest change block that fixes the actual decisions: a schema field
and enum values; a branch/formula with its boundary condition; exact old/new copy;
a config key/value; or a signature plus decided data flow. A signature alone cannot
settle an algorithm or failure policy. Use a complete small body when that is the
clearest specification. Avoid duplicate routine bodies and redundant copies of
producer code. Never require a full executable patch before source is known.

"Implement feature", "restore old behavior", "handle edge cases", "write tests"
or "use the existing pattern" without their exact change/test/reference are not
Change Specifications. These phrases can label a milestone, not authorize a ready
task. A fresh executor may choose routine local mechanics; it must not have to
guess product behavior, cross-task contracts, exact values or the changed areas.

## Coverage and integration

Use a compact table or equivalent explicit links:

| Requirement or material failure case | Owner | Observable check |
| --- | --- | --- |
| R1: accepted input -> output | T1 | named test/assertion or artifact observation |

Walk the accepted spec, not just task titles. Every in-scope requirement has an
owner and check; every task serves a requirement, risk or named prerequisite.
Include relevant invalid/empty/boundary inputs, permissions, failure recovery or
concurrency only where the accepted behavior implies them. Record a justified
validation gap when a check cannot run; a heading or exit 0 alone is not coverage.

The dependency graph must have unique IDs, existing dependencies and no cycles.
Consumers must agree with their producers' names, types and error/side-effect
contracts. Serialize shared writes and other shared-state hazards even when
feature outcomes differ. A discovery task states the uncertainty, bounded source
or experiment, expected decision artifact and the dependent work it blocks.

Gates test integration when it becomes meaningful: entrypoint -> real collaborators
-> observable result. Reuse the project's standing quality floor and applicable
commands; do not prescribe unavailable linters/typecheckers or full suites after
every tiny step. Broad claims such as durability or performance need their own
fault/load conditions and expected observations, or a narrower stated scope.

## State, drift and authority

Planned verification stays separate from actual results. After execution, record
the command/action, observed result, tested content identity/environment and limits
in the owning task or phase. DONE requires its acceptance evidence and the
applicable project quality floor, not merely a worker report or checked box.

Keep canonical statuses `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `SKIPPED`; board
and detail must agree. A BLOCKED task names its blocker. Completed evidence survives
replanning unless drift invalidates it. Local corrections update the affected
task; changed interfaces invalidate affected consumers and evidence. Rebaseline
those tasks before execution; independent authorized work can continue. Request a
decision only if the change exceeds authority or changes a user-owned requirement.

Commits, clean-tree requirements, tracker writes and publishing are not implicit
acceptance criteria. Include an authorized commit boundary when useful and stage
only owned paths. Existing unrelated changes may remain. Planning-only ends at
the plan; implementation already authorized can proceed through plan-execution
without a new approval ritual. `NEXT ACTION` names the next artifact, action and
check, or `None — task complete` after verified completion.
