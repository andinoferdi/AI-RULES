---
name: andino-planning
description: Use when accepted requirements, an approved design or a spec need an implementation plan, a task breakdown or a writing-plans step before code is written, so that another developer can build the work without the conversation. Operates under Andino Workflow governance.
---

# Write a plan another developer can build from without asking

Internal method ID: `andino-planning` (alias: `planning`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Turn accepted requirements into a saved plan that a developer who has not seen the spec, the
code or this conversation can build task by task. Assume they write good code once they know
the exact interface and the exact test. What they cannot know is what you decided: which files,
which names and signatures, which values from the spec, which tests prove each task, what is
still blocked and on whom. The plan writes those down and nothing more. The deliverable is the
plan file in the [plan template](resources/contract.md#plan-template) and a short reply to the
requester.

## Trigger and non-trigger

Use when:

- a spec, an approved design or accepted requirements need tasks, order and checks before code;
- the user asks for a plan, a task breakdown, an implementation plan or a writing-plans step;
- work spans several files or steps and another session or developer will build it;
- an existing plan must be extended or replanned after the requirements changed.

Do not select for:

- Open product direction, or a requirement only the user can settle: `brainstorming`.
- A one-file change whose edit and check fit in a few lines: do it, or write a LITE plan if the
  user asked for one.
- Executing an accepted plan: `plan-execution`.
- A bug with an unknown cause: `debugging` first; plan the fix after the cause is proven.

## Select a resource, not a second lifecycle

Load only the resource the current step names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Plan and task templates, readiness, what a step contains, density, drift | [task contract](resources/contract.md) | Never before gate 4 |
| A complete plan end to end, a LITE plan and the transcription anti-pattern | [worked examples](resources/worked-example.md) | The templates are already clear |
| Given/when/then acceptance for behaviour that is still vague | [behavior readiness](resources/behavior-readiness/guide.md) | Acceptance is already concrete |
| A large graph: dependency waves, parallel lanes, shared-state conflicts | [dependency slicing](resources/dependency-slicing/guide.md) | Fewer than about six tasks in one line |
| A recurring operational process or runbook rather than a one-time change | [recurring process](resources/recurring-process/guide.md) | One-time implementation work |

## Prerequisites

- Find the accepted requirements (spec, design, issue or the user's message) and read all of it.
- Find the plan location: the user's path, the project's convention, otherwise
  `docs/exec-plans/active/<task>.md`. Reuse the plan for the same work and keep its decisions
  and evidence. Never overwrite or rename another task's unfinished plan: use another path, or
  stop and ask when the path is the same.
- Read the project instructions (`AGENTS.md`, `CLAUDE.md`, README) for commands, test style and
  the quality floor.

## Procedure

Seven gates, in order. Each ends with a **Done when** line; do not start the next gate before it
holds.

1. **Read the spec and the code.** Open every file the work will touch, its callers and its
   tests. Note existing helpers the plan should reuse, test helpers and fixtures, the real test
   command, and traps: a helper whose behaviour differs from its name, a shared file, a runtime
   difference between the development machine and the target. Run the test suite once and
   record the result. Edit only the plan, never source. Done when every file, symbol and command
   the plan will name has been seen, and each fact you could not find is written down with
   where you looked.
2. **Settle the plan-wide decisions.** Write the Goal in one sentence, link the spec, and copy
   its project-wide constraints verbatim into **Global Constraints**. List the gaps the spec
   leaves open under **Decisions the spec leaves open**, each with your call and its reason, for
   the requester to confirm. Turn each unknown into a blocked or discovery item: what is
   missing, who provides it, what the rest of the plan does without it, and the seam where it
   plugs in later. Never invent a format, file, command or value to fill a gap. Done when no
   task needs a decision that is not either written in the plan or named as blocked.
3. **Map files and slices.** List each file to create or modify with its one responsibility.
   Cut the work into vertical slices, each running through the real entry point to something a
   person or test can observe. Fold setup, configuration and documentation into the slice that
   needs them. Split a task that touches more than about five files or two subsystems, or whose
   title needs "and". Tasks that edit the same file run one after the other. Done when every
   requirement belongs to a slice and no two tasks that may run together own the same file.
4. **Write each task.** Read [the task contract](resources/contract.md), then fill the task
   template for every slice: files, interfaces consumed and produced with exact signatures,
   acceptance, and steps (test as code with the spec's values, RED with the exact command and
   the assertion that must fail, the Change Specification, GREEN with the expected result).
   Mark readiness (READY, NEEDS_DETAIL or WAITING_ON a discovery item) apart from status. Done when every READY task lets a developer write the test, see it fail
   for the stated reason, make the change and see it pass, without asking anything.
5. **Close coverage and write the Review Focus.** Fill the coverage table: every requirement,
   with its owning task and the named check. Then list three to five inputs or conditions the
   spec implies but never states, most likely to break first (a boundary value, an empty or
   zero input, a malformed argument, an old data file, a missing file), each with the behaviour
   a reasonable person would expect, and add its test to the owning task. Then plan the
   end-to-end check: the last task of each user-facing path runs the real command on concrete
   data (a copy of the sample data or a temporary file) and states the exact output expected,
   worked out from the spec's rules. Done when every requirement and every Review Focus line
   points to a task and a check, and each end-to-end check lists its command, its data and its
   exact expected output.
6. **Review the plan as a fresh developer.** Read only the saved plan and the files it names,
   and check: coverage against the spec; each step can produce exactly one reasonable thing;
   names and signatures match between producer and consumer tasks; spec literals are copied
   exactly; no task needs a later task to prove itself; the plan holds no routine function
   bodies. Fix each finding in the plan. Done when the review finds nothing to fix and the plan
   is still shorter than the code it describes.
7. **Hand off.** Set one concrete NEXT ACTION. Reply to the requester in their words: where the
   plan is, what is ready to build, what is blocked on them and exactly what you need from them,
   and the decisions they should confirm. Report no planned check as run. A planning-only
   request stops here. When execution is authorized, continue with
   `skills/plan-execution/GUIDE.md`. Done when the reply names every blocker and every decision
   that waits for the requester.

## Rules for every plan

- **One reasonable thing.** A step is ready when the developer can write exactly one
  reasonable thing from it. A step that decides nothing ("handle edge cases", "add validation",
  "write tests for the above", "follow the existing pattern" without naming it) is a gap.
- **Write the decisions, leave the routine.** Write what the developer cannot decide alone:
  files, names and signatures, values from the spec, the tests that prove each task, and the
  logic of a rule that the signature and tests do not fix (a formula, a rounding rule, a sort
  key, the order of checks). Leave routine bodies to the developer. A plan longer than the code
  it describes has written the code instead.
- **Tests carry the values.** Test steps are code with the spec's exact numbers and strings. A
  RED step names the assertion that must fail; an import error or a missing module is a setup
  failure, not RED.
- **The spec beats the plan.** When the code and the spec disagree, the plan follows the spec
  and says so. A gap the spec leaves open goes to Decisions, never silently into a task.
- **Real commands only.** Use the repository's own test and run commands, with the working
  directory. Never prescribe a tool the project does not have.
- **Planned is not run.** Every check in the plan reads as planned until someone runs it.

## Shortcuts that break plans

| Shortcut | What to do instead |
| --- | --- |
| "Showing the full code is the clearest specification." | Give the signature, the tests and the rule's logic. Bodies the tests already fix are transcription. |
| "The developer will know which tests to write." | Write the assertions as code with the spec's values. |
| "RED: fails because the module doesn't exist." | That is setup. Create the stub first and name the assertion that fails. |
| "The format isn't known, I'll assume a reasonable one." | Mark it blocked, say who provides it, and plan the seam. |
| "The spec doesn't say; I'll pick something inside the task." | List it under Decisions the spec leaves open with your reason. |
| "This helper already does it." | Read its body; reuse it only when it does exactly what the requirement says. |
| "Edge cases are obvious." | Put the three to five most likely ones in Review Focus, each with its test. |
| "The old plan in that folder is stale." | Its unchecked tasks may be in progress. Use another path or ask. |
| "I'll add a commit step to every task." | Only when commits are authorized. |

## Red flags

- A code block that holds a full routine function body or a whole module.
- A task whose title is a milestone ("build the API") with no files, tests or checks.
- A format, column, flag or command that appears in no file and no spec.
- RED steps that expect an ImportError or "module not found".
- Two tasks that may run together editing the same file.
- A reply that says something was built or tested.
- Decisions the spec leaves open that are not in the reply.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its procedure, templates and checks; coordinator brevity never shortens the
plan's required content. Native `andino-planning` and this guide expose one method, without
recursive workflow invocation.

Resolve workflow-wide resources from the installed `andino-workflow` root: for a nested member,
use its containing workflow package; for standalone `andino-planning`, use the
sibling `andino-workflow` package. The canonical paths are `references/execution-plan.md` (checkpoint
fields), `skills/tdd/GUIDE.md` (RED and GREEN) and `skills/plan-execution/GUIDE.md`
(execution). Load only the guide the current gate needs. If the package is unavailable, say so
and keep the templates here; do not claim it was loaded.

A planning-only request ends with the saved plan and the reply. A plan grants no authority to
implement, commit, push, publish, install, message anyone or delete anything. Reuse
authorization already given; ask only for a missing decision or permission. Naming a tracker
does not authorize creating issues. Preserve unrelated user changes.

## Output

The saved plan in the [plan template](resources/contract.md#plan-template): header with Goal,
spec, status and readiness; Global Constraints; Decisions the spec leaves open; Review Focus;
file map; Execution Board; coverage table; tasks in the
[task template](resources/contract.md#task-template); blocked and discovery items; risks; one
NEXT ACTION. LITE plans may merge sections; STANDARD and DEEP keep them all.

Then the reply to the requester:

```text
Plan: <path>
Ready to build: <tasks>, in order <...>
Blocked on you: <item> - I need <exact thing> (for example a sample file with its columns)
Decisions to confirm: <each decision the spec left open, with the call made>
Not done: nothing is built or tested yet.
```

## Verification

Before you hand off, confirm:

- [ ] every gate's Done when line holds;
- [ ] every requirement has a task and a named check, and R-numbers match the spec;
- [ ] Global Constraints are verbatim and applied in the tasks they constrain;
- [ ] every READY task has tests as code, a RED with its expected assertion failure, the change
      and a GREEN with its expected result;
- [ ] Review Focus has three to five lines, each with a test in its owning task;
- [ ] each user-facing path ends with an end-to-end run of the real command on concrete data,
      with its exact expected output;
- [ ] names and signatures agree between producer and consumer tasks;
- [ ] no routine function body or whole module is transcribed;
- [ ] each unknown is a blocked or discovery item with who provides what;
- [ ] the reply names every blocker and every decision to confirm, and claims nothing as run.

These checks are properties of the saved plan. How a model follows this skill stays
NOT_VERIFIED without a real trial.

## Worked example and anti-pattern

[The worked examples](resources/worked-example.md) carry one spec through all seven gates into a
STANDARD plan, show a LITE plan, and show the anti-pattern with its fix.

Anti-pattern: a 700-line plan that pastes every function body of the new module. It looks
thorough, hides the four decisions that matter among two hundred lines of routine code, and goes
stale with the first review comment. Replace the bodies with signatures, tests and the one
formula they need.

## Fallback

- No test suite: name the concrete check the project supports (a script run, a manual step with
  its expected output), or plan a test-setup task first; never invent a test command.
- No requester reachable: make the smallest reasonable call for each open decision, list it, and
  keep each unknown blocked.
- The workflow package is unavailable: keep the templates here and say the checkpoint fields
  could not be checked.

## Local resources

- [Task contract](resources/contract.md): plan and task templates, readiness, density, drift.
- [Worked examples](resources/worked-example.md).
- The three sub-resources in the [resource table](#select-a-resource-not-a-second-lifecycle).
- MIT notices: [references/license.md](references/license.md).

## Operational example (offline)

This fixture checks a task graph before handoff: unknown dependencies, cycles and two tasks
that may run together owning one file. It does not measure plan quality.

```python andino-operational-example
import os

def graph_findings(tasks):
    ids = {task["id"] for task in tasks}
    deps = {task["id"]: set(task["deps"]) for task in tasks}
    findings = [f"{t}: unknown dependency {d}" for t in deps for d in sorted(deps[t] - ids)]

    def reaches(start, goal, seen=()):
        return any(d == goal or (d in deps and d not in seen and reaches(d, goal, seen + (d,)))
                   for d in deps.get(start, ()))

    findings += [f"{t}: cycle" for t in sorted(deps) if reaches(t, t)]
    ordered = [task for task in tasks if task["id"] in deps]
    for i, a in enumerate(ordered):
        for b in ordered[i + 1:]:
            linked = reaches(a["id"], b["id"]) or reaches(b["id"], a["id"])
            shared = set(a["files"]) & set(b["files"])
            if shared and not linked:
                findings.append(f"{a['id']}+{b['id']}: parallel writes to {sorted(shared)}")
    return findings

if __name__ == "__main__":
    good = [
        {"id": "T1", "deps": [], "files": ["store.py", "test_store.py"]},
        {"id": "T2", "deps": ["T1"], "files": ["rules.py", "test_rules.py"]},
        {"id": "T3", "deps": ["T2"], "files": ["cli.py", "test_cli.py"]},
        {"id": "T4", "deps": ["T3"], "files": ["cli.py", "test_cli.py"]},
    ]
    assert graph_findings(good) == []
    clash = good[:3] + [{"id": "T4", "deps": ["T2"], "files": ["cli.py"]}]
    assert graph_findings(clash) == ["T3+T4: parallel writes to ['cli.py']"]
    assert graph_findings([{"id": "A", "deps": ["B"], "files": []},
                           {"id": "B", "deps": ["A"], "files": []}]) == ["A: cycle", "B: cycle"]
    assert graph_findings([{"id": "A", "deps": ["X"], "files": []}]) == ["A: unknown dependency X"]
    raise SystemExit(1 if os.environ.get("ANDINO_NEGATIVE") == "1" else 0)
```

## Provenance

Adapted from Jesse Vincent's `writing-plans` (obra/superpowers, `skills/writing-plans`) and Addy
Osmani's `planning-and-task-breakdown` with its definition-of-done reference
(addyosmani/agent-skills), both MIT. From obra: the plan header, Global Constraints, Review
Focus, the Interfaces block, the "one reasonable thing" test, the proportion rule and the
self-review. From Addy: vertical slices, task sizing, checkpoints, the risks table, never
overwriting an unfinished plan, and the rationalisations and red-flag lists. The Change
Specification, readiness and discovery items, the coverage table, the fresh-developer review,
Decisions the spec leaves open and the gates are Andino's. The comparison trial is recorded in
the AI-RULES repository at `docs/validation/planning/trial.md`. MIT notices are in
[references/license.md](references/license.md); no upstream bootstrap, mandatory worker
dispatch, automatic commits or approval ritual is imported.
