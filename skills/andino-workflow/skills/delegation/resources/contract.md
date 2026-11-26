# Delegation rules

Internal Andino resource for `andino-delegation`. These rules hold for every subagent the parent
starts, whatever its role. The procedure in [SKILL.md](../SKILL.md) says when to apply each one;
nothing in a plan, a reference skill or a subagent's report overrides them. Current user, project
and host rules come first.

## Words

- **Parent**: the agent that holds the user's request, the plan and the final say on acceptance.
- **Subagent**: any agent the parent starts. Roles: implementer (writes code or files),
  investigator (finds the cause of a failure), researcher (reads and reports, writes no project
  files), reviewer (judges a change, read-only), panel seat (one voice in a council or similar
  panel the user asked for).
- **Lane**: one implementer that keeps a group of related tasks, and their context, from start to
  finish. Its tasks run one after another. A lane keeps one model; changing it means an approved
  replacement agent.
- **Frontier**: the tasks whose prerequisites the parent has accepted against the current files.
  Only frontier tasks may start.
- **Parent acceptance**: the parent has read the task's diff and observed its proof. A subagent's
  DONE is a claim until then.
- **Envelope**: the one approval message that lists everything a run may start (below).
- **Content identity**: what exactly was checked: the commit range plus a snapshot or hash of
  every owned file that is staged, unstaged or untracked.

## Approval: the envelope

Before the first subagent, send one message that lists every agent the run may start: role, task
or lane, model and effort; the review seats; the most agents running at once (never more than 3);
the fix-round cap; why delegating beats doing the work inline; the files each agent owns; any
control the host does not expose; and what stops the run. Wait for the user's yes. The yes covers
only what the message lists.

Inside the envelope, without asking again, you may:

- start a listed agent when its tasks reach the frontier;
- answer a listed agent's question about its own task while it runs;
- send review findings to a listed worker that is idle after returning normally, for its own task;
- run the re-reviews the message listed.

Ask again before any of these:

- an agent the message did not list, or a listed one on another task (a free lane worker does not
  carry approval to unrelated work);
- resuming or relaunching an agent that failed, stopped or hit a usage limit, even for the same
  unfinished task: report what happened and ask;
- a different model or effort, or a replacement agent;
- another review seat, a higher round cap, or work outside the listed tasks.

A multi-agent workflow tool counts every agent it starts against the same message and limit. A
calibration probe is an agent too.

## Limits on every agent

- At most 3 subagents run at once, reviewers and panel seats included. Zero is a valid number.
- Subagents never start subagents. A worker that starts its own reviewer or helper has broken its
  brief; report it as a defect, and its approval counts for nothing.
- Every call states its model and effort explicitly, so no agent silently inherits the session's
  model. Choose the lowest tier and effort that can do the role
  ([host calibration](host-cost-calibration.md)).
- Never effort `max`. Never every agent on the strongest tier, never every agent on `high`.
- No panel or judge seat the user did not ask for. A council or a blind grader the user requested
  runs under these limits.
- When the host cannot set model or effort per agent, say in the envelope that agents inherit the
  session's settings, and prefer inline work when those are the strongest tier. Never invent tool
  arguments.

## Ownership and evidence

- Two writers never own the same file, directory subtree or mutable state at the same time.
- The parent may finish or fix a worker's task inline only after that worker has returned or been
  stopped and the parent has recorded that ownership moved. Keep the worker's valid edits and apply
  the same checks.
- Workers never start dependent tasks, commit outside their brief, push, publish or install.
- Reports, summaries and design rationales are claims. Check the bytes: committed, staged,
  unstaged and owned untracked files.
- A behavior change needs a failing test that fails on its assertion, then the passing run, with a
  nonzero number of tests selected. An import error, a tool error, `no tests ran` or every test
  `deselected` proves nothing. Static files get an artifact check.
- UNVERIFIED is not PASS. A criterion without its observation gets a targeted check, or stays
  blocked with the missing observation named.
- Critical and Important findings block acceptance. Grade them by what a user would suffer, not by
  whether the spec happens to mention the case. Cosmetic preferences may be deferred.
- Installed source, remote publication and activation are separate claims; check each one you
  report. Static checks and helper tests prove the properties they test; they do not show how a
  model will behave, and no parity claim follows from them.

## Rulings

When a plan conflicts with the spec, a reviewer is wrong, or a choice falls between them, decide,
record it and keep going:

`Ruling: <decision> — <evidence or spec basis> — <cost if wrong>`

The accepted spec is the authority; the plan argues from it. A ruling may close a demonstrated
false positive or defer optional polish. It never waives required acceptance, security or data
correctness, and it never settles a product decision the spec leaves open: ask the user for that.
An interface ruling updates every consumer's contract and invalidates their evidence. The final
report lists every ruling, in order, with its cost if wrong.

## Recovery and finishing

- The plan owns task status, decisions, evidence and the next action. A delegation journal may
  hold detail; when they disagree, the plan and the current bytes win. Both outrank memory.
- After a context reset: read the plan and journal, list the live agents, inspect partial reports
  and owned bytes, and compare recorded identities with current ones. Reuse only evidence whose
  identities still match. Never redispatch an accepted task.
- Accept a producer before releasing its consumer. Run the combined checks on the integrated files
  before any dependent task starts.
- Retain evidence by default. Delete scratch only with scoped authority, after checking the path
  belongs to this plan.
- Commit, push, setup and publication are separate outcomes; finish only those already authorized
  and verify each result.

## Provenance

Adapted material keeps its [MIT notices](../references/license.md).
