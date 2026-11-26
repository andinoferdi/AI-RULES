# Planning task contract

The plan and task templates, what each kind of step contains, readiness, density, and how plan
state changes during execution. The workflow's `references/execution-plan.md` owns the
checkpoint lifecycle (resolve it from the installed workflow root as the planning guide says);
this file gives the planning content that goes into it. If the project already uses another
plan shape, keep equivalent fields.

## Plan template

One file, saved where the planning guide's Prerequisites say. Replace every placeholder with an
inspected fact, a decision with its reason, or a named blocked item. Delete a section only when
the density table below allows it.

````markdown
# <Feature> implementation plan

Status: TODO | IN_PROGRESS | BLOCKED | DONE
Plan Depth: LITE | STANDARD | DEEP
Spec: <path to the accepted spec or design; the developer reads it with this plan>
Last Updated: <YYYY-MM-DD>

## Executive Snapshot
<Two or three lines: what is ready, what is blocked and on whom, where to start.>

## Goal
<One sentence: what this builds and for whom.>

## Global Constraints
<Every project-wide requirement from the spec, copied verbatim, one line each: runtime and
version floors, dependency limits, money or unit rules, data compatibility, wording rules.
Every task implicitly includes this section.>

## Decisions the spec leaves open
<One line each: the gap, the call made, the reason. The requester confirms these; the reply
lists them.>

## Review Focus
<Three to five inputs or conditions the spec implies but does not state, most likely to break
first, each with the behaviour a reasonable person expects and the task whose tests cover it.>

## File map
<Each file to create or modify, with its one responsibility.>

## Execution Board
| Task | Status | Readiness | Depends on | Files |
| --- | --- | --- | --- | --- |

## Coverage
| Requirement | Task | Check |
| --- | --- | --- |

## Tasks
<One block per task in the task template.>

## Blocked and discovery items
<Each unknown: what is missing, who provides it, what proceeds without it, the seam where it
plugs in, and the exit check that ends the block.>

## Risks
| Risk | Effect | Covered by |
| --- | --- | --- |

## NEXT ACTION
<One concrete action: the task, its first step and its first check.>
````

## Task template

````markdown
### T1 - <observable deliverable>
Status: TODO
Readiness: READY | NEEDS_DETAIL (<missing decision>) | WAITING_ON D1
Requirements: R1, R2
Depends on: none | T0
Files: Create `path/new.py`; Modify `path/existing.py` (`symbol`); Test `tests/test_x.py`
Interfaces:
- Consumes: <exact name and signature from an earlier task or existing code, with its file>
- Produces: <exact name, parameters and return type later tasks rely on>
Acceptance: <literal input or state -> expected output or side effect; the failure cases>

Change Specification:
- `path/existing.py::symbol`: today <inspected behaviour>; change to <result, with the exact
  names, literals and error rules>.
- `path/new.py` (proposed): <what it holds; signatures; the rule's logic when the signature and
  tests do not fix it>.

Steps:
- [ ] 1. Write the tests in `tests/test_x.py`:

```python
def test_specific_behaviour(self):
    self.assertEqual(function(spec_input), spec_value)
```

- [ ] 2. RED: run `<test command>` from `<directory>`. Expect `test_specific_behaviour` to fail
      with `<the assertion message>` (not an import or setup error).
- [ ] 3. Make the change in the Change Specification.
- [ ] 4. GREEN: rerun the same command; expect `<N tests, OK>`. Then run the full suite.
- [ ] 5. Commit `<owned files>` (only when commits are authorized).

Result / Evidence: Not run - planned checks only.
````

Fields may share a line in a LITE plan. "Interfaces: none" is fine when a task changes no
cross-task interface.

## What a step contains

A step is ready when the developer can write exactly one reasonable thing from it. Each kind of
step carries what makes it unambiguous and nothing more:

| Step | Carries |
| --- | --- |
| Test | The test's name and its assertions as code, with the spec's exact values, using the project's real fixtures and helpers. |
| RED | The command, the working directory and the assertion that must fail. For a new module, a stub with the signature comes first so RED fails on behaviour. |
| Change | The file and symbol, the exact signature, the literals the spec pins, and code only for logic the signature and tests do not fix. |
| GREEN | The same command and the expected result (test count, OK, exit code or exact output). |
| Reference to another task | That task's Interfaces line; never a copy of its code. |
| Static artifact | The exact text or setting to add or replace, and the check that shows it (a grep, a parse, a rendered page). |

Code that belongs in a plan: test code; a formula or rounding rule; a sort key; the order of
checks with their messages and exit codes; a schema, enum or config key; exact user-facing text.
Code that does not: bodies the signature and the tests already determine, imports, argument
parser boilerplate, loops that only apply a stated rule, whole modules.

Lines that decide nothing are gaps: "TBD", "as appropriate", "handle edge cases", "add
validation", "write tests for the above", "follow the existing pattern" without the file and
symbol, a type or function no task defines.

## Proportion

Compare the plan with the code it describes. When code blocks are most of the plan, replace
bodies with signatures, tests and the rule's logic, then check each step still yields one
reasonable thing. When a step needs the developer to guess a value, a name or an order, add it.
Detail is spent on decisions, not on volume.

## Readiness and discovery

Readiness says whether a task is specified enough to start; status says how far it got. Keep
the canonical statuses `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `SKIPPED`.

- `Readiness: READY`: the files were inspected, the Change Specification is complete, and the
  tests and checks are concrete.
- `Readiness: NEEDS_DETAIL (<gap>)`: a decision or fact is still missing; the gap is named.
- `Readiness: WAITING_ON D1`: the task needs a discovery item's answer.

A discovery item (D1, D2, ...) states the uncertainty, the source or person that answers it,
the questions to answer, the decision it produces and the tasks it unblocks. When it completes,
write the answer into the waiting tasks' Change Specifications in the same plan; marking D1
DONE alone leaves the consumers guessing. A plan may mix READY and waiting tasks; hand it off as
ready only for the READY ones. Independent ready tasks keep moving.

## Density

| Density | Use when | Keep |
| --- | --- | --- |
| LITE | One or two tasks, one subsystem | Goal, spec, constraints, decisions, tasks, checks, NEXT ACTION; sections may merge |
| STANDARD | Several dependent tasks or material decisions | Every section of the plan template |
| DEEP | Migrations, cross-system work, costly mistakes | STANDARD plus decision evidence, rollback or staged gates, and fault or load checks for broad claims |

File counts alone do not set density. Density never removes a READY task's tests, RED, GREEN or
Change Specification.

## Coverage and integration

Walk the spec, not the task titles. Every requirement has an owning task and a named check; every
task serves a requirement, a Review Focus line or a named prerequisite. A helper test cannot
prove behaviour that spans collaborators: test the public entry point where acceptance crosses
modules. Place an integration check where slices meet, using the project's real commands. The
last task of each user-facing path runs the real command on concrete data and states its exact
expected output, worked out from the spec's rules; "check the output by hand" is not a check. Broad
claims (durability, performance, concurrency) need their own fault or load condition and
expected observation, or a narrower stated scope.

The graph has unique IDs, existing dependencies and no cycles. Consumers use the producer's
exact names, types and error rules. Tasks that share a file, fixture, schema or generated file
run in sequence; parallel eligibility does not start workers.

## State, drift and authority

Planned checks stay separate from results. After execution, record in the owning task the
command or action, the observed result, the tested content and environment, and limits. `DONE`
needs that evidence and the project's quality floor, not a checked box or a worker's report. A
`BLOCKED` task names its blocker. The board and the task blocks agree.

Completed evidence survives replanning unless drift invalidates it. A local correction updates
the affected task; a changed interface invalidates its consumers and their evidence, which are
rebaselined before execution. Ask the user only when a change exceeds authority or alters a
requirement they own.

Commits, a clean tree, tracker writes and publishing are not implicit acceptance criteria.
Include a commit step only under existing authorization and stage only owned paths. A
planning-only request ends at the saved plan; execution already authorized continues through
plan-execution without a new approval ritual. `NEXT ACTION` names the next task, step and check,
or `None - task complete` after verified completion.
