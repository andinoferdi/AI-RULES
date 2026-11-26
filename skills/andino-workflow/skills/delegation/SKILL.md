---
name: andino-delegation
description: Use when deciding whether to start subagents for any work (implementing plan tasks, investigating failures, research or exploration, review, verification, panel or council seats, a multi-agent workflow tool), or when handling what a started subagent returned. Operates under Andino Workflow governance.
---

# Decide, brief and accept subagent work under parent ownership

Internal method ID: `andino-delegation` (alias: `delegation`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource grants no action authority; current user,
> project and host rules come first.

## Purpose

Decide whether a subagent would do a piece of work better than you doing it yourself; when it
would, give it everything it needs and nothing it does not, and accept its result only on evidence
you observed. You, the parent, keep the plan, the integration and the final say. A subagent starts
with no memory of the session and costs tens of thousands of tokens before it does anything, so
small or coupled work is usually cheaper inline. Where delegation pays (independent domains, a long
plan whose lanes can run side by side, fresh eyes on risky code, a panel the user asked for), this
skill makes the decision, the brief, the prompt and the handling of returns reliable. The words
lane, frontier, envelope, parent acceptance and content identity are defined in
[the rules](resources/contract.md#words).

## Trigger and non-trigger

Use when:

- an accepted plan has tasks that might go to implementer subagents;
- several failures, bugs or questions might be investigated in parallel;
- research, exploration, review, verification or a second opinion might go to a subagent;
- a council, another panel or a multi-agent workflow tool is about to start agents;
- a subagent returned (done, concerns, needs context, blocked, failed, stopped, usage limit), or
  delegated work must be recovered after a context reset.

Do not select for:

- Shaping the plan itself: `planning`. Executing it yourself: `plan-execution`, which comes here
  when a task might be delegated.
- The method a subagent applies (TDD, debugging, review standards, research): that skill owns it;
  this skill owns the handoff around it.
- A panel's own procedure, such as the council's lenses and synthesis: the panel skill owns it;
  this skill adds the approval and the limits.
- Requests to start agents recursively or without the user's approval.

## Select a resource, not a second lifecycle

Load only the resource the current step names. It runs inside this procedure and current authority;
it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Words, the envelope, limits on every agent, evidence, rulings, recovery | [the rules](resources/contract.md) | Never before the first dispatch |
| Brief file, dispatch call, prompts per role, status routing, report format | [briefs and prompts](resources/subagent-brief-and-report-schemas.md) | No subagent will start |
| Pre-flight table, dependencies and frontier, write collisions, lanes, batching | [pre-flight and frontier](resources/frontier-and-dag-protocols.md) | A single task or a single failure |
| Review, fix rounds, items a reviewer cannot verify, the cap, final review | [review and finishing](resources/two-track-review-and-fix-loop.md) | Nothing to review yet |
| Model and effort per role, host map, start-up cost | [host calibration](resources/host-cost-calibration.md) | Every agent's model and effort is already approved |
| Workspace, journal, waiting for agents, Windows file locks, teardown | [workspace and recovery](resources/workspace-and-isolation-guards.md) | Inline work with no journal |
| One run end to end with every artifact | [worked example](resources/worked-example.md) | The procedure is already clear |

## Prerequisites

Read the request, the accepted spec and plan (or the failure output and recent commits), the current
diff and `git status`; attribute changes already present. Know the host's real agent controls:
whether it sets model and effort per agent, runs agents in the background, and lets you message an
agent after it returns. A missing control goes into the envelope as a limitation, never into a
guessed tool argument. Read [the rules](resources/contract.md) before the first dispatch.

## Procedure

1. **Decide inline or delegate.** For each piece of work, weigh the work saved against the start-up
   (about 60k tokens per agent on Claude Code, see [host calibration](resources/host-cost-calibration.md)),
   the brief, the review and the integration. Work inline when the piece is small, coupled to other
   changes, exploratory, dependent on your context, or shares an unresolved cause with other
   failures: investigate that cause once, yourself, first. Delegate when the work splits into
   independent domains with separate files and stable interfaces, when a lane of related tasks is
   long enough to repay its start-up, when fresh eyes on risky code are worth a reviewer, or when the
   user asked for a panel. File, line and task counts are signals, not quotas; never start an agent
   just to measure. Done when every piece of work has a mode (inline, batch, lane, parallel agent,
   reviewer, researcher or panel seat) and its reason.
2. **Pre-flight.** For a plan, write the
   [pre-flight table](resources/frontier-and-dag-protocols.md#pre-flight-table): one row per pair of
   tasks that share a file or an interface, one row per task checked against itself and the spec.
   Rule on conflicts with the spec as the authority and record each ruling. A task without exact
   files, change and acceptance is not ready to brief: complete it from the source or send it back to
   planning. For failures, group them by cause from the failure output and the commits since the
   last green run. Done when every pair and task has a row (or every failure a group) and every
   conflict has a ruling or a question for the user.
3. **Shape lanes and waves.** Reject duplicate IDs, missing dependencies and cycles. Put related
   tasks that share files or context into one lane. Check every pair of units that may run together
   for [write collisions](resources/frontier-and-dag-protocols.md#write-collisions): same file,
   ancestor directory, shared root configuration, shared mutable state. Only frontier tasks start; at
   most 3 agents run at once, reviewers included. Batch small same-shape edits into one unit. Done
   when every delegated unit owns paths no concurrent unit touches and no consumer can start before
   its producer is accepted.
4. **Choose model and effort per agent** from the
   [role table](resources/host-cost-calibration.md#model-and-effort-by-role): the cheapest tier only
   for transcription or single-file mechanical work; a mid tier for implementation from prose,
   investigation, research and review; a stronger tier only for a risk the plan names. Never `max`;
   never every agent on the strongest tier or on `high`. Done when every agent has an explicit model,
   effort and one-line reason.
5. **Ask once: the envelope.** Send one message listing every agent the run may start (role, task or
   lane, model, effort, owned paths), the review seats, the most agents running at once, the
   fix-round cap, why delegating pays, the rulings made for the spec, what stops the run and any
   control the host lacks. Wait for the user's yes. Inside the approved list you may start listed
   agents as their tasks reach the frontier and send fix rounds to a listed idle worker for its own
   task; everything else is a [new ask](resources/contract.md#approval-the-envelope), including
   resuming an agent that failed, stopped or hit a usage limit. Done when the user approved and the
   plan or journal records the envelope.
6. **Brief and dispatch.** Write one [brief file](resources/subagent-brief-and-report-schemas.md#brief-file)
   per task or batch with every field filled; `scripts/task_brief.py` copies the plan section, and
   you complete it. Pin BASE and owned work in progress. The dispatch call carries one line of fit,
   the brief path, cross-task interfaces and rulings, the role section for this agent and the report
   path; never the plan, the conversation or summaries of earlier tasks. Investigators get the exact
   failure, the suspect commit, their edit scope and the ban on papering over failures. Researchers
   write notes to a file that later briefs point to. Reviewers get the requirements and your rulings
   as facts, never a list of things not to flag. Resolve a material unknown before dispatch; never
   send an agent to guess a contract. Done when each brief is complete for a reader with no session
   memory and each call states model and effort.
7. **Wait and route returns.** Keep doing local work while agents run; when idle, wait in bounded
   stretches and then reconcile live agents
   ([waiting](resources/workspace-and-isolation-guards.md#waiting-for-agents)). Route every return
   with the [status table](resources/subagent-brief-and-report-schemas.md#status-routing). DONE is a
   claim. A concern about correctness or scope is settled before review. NEEDS_CONTEXT gets the
   missing fact, not a stronger model. BLOCKED gets a change: context, a split, a ruling, or a
   proposed model change as a new ask. A failed, stopped or usage-limited agent gets inspection,
   attribution and a question before any resume. Done when every agent's state is known and every
   return has a recorded next action.
8. **Review and accept.** Read every task's full owned diff and proof yourself: committed, staged,
   unstaged and owned untracked bytes; a test run that failed on its assertion with tests selected,
   then passed. Risky tasks also get the listed reviewer, spec first and then quality, with the
   change pinned as a package plus a snapshot of uncommitted files. Run
   [fix rounds](resources/two-track-review-and-fix-loop.md#fix-rounds) through the same idle listed
   worker: findings verbatim, covering tests rerun, a scoped re-review, five rounds as a ceiling.
   Resolve every item the reviewer could not verify. Done when every acceptance criterion has an
   observation (UNVERIFIED stays blocked), every Critical and Important finding is fixed or ruled on,
   and the task is accepted against current files. Only then release its consumers.
9. **Integrate and finish.** Run the plan's real checks on the combined files and read the outputs
   for assumptions that disagree, even across disjoint files. Do one whole-change review (yourself,
   disclosed as not independent, or one listed reviewer justified by risk), send all its findings to
   one fixer and re-review once; there is no second wave. Record identities, rulings, deferred
   findings and NEXT ACTION in the plan, and finish only the commit, push or setup steps already
   authorized, verifying each. Done when the final report lists what changed, the evidence, what is
   not verified, deferred findings and "Rulings I made", each with its cost if wrong.

## Rules that never bend

The full text is in [the rules](resources/contract.md); these hold on every step.

- One envelope per run. A new agent, a resume or relaunch of a failed, stopped or usage-limited
  agent, a model or effort change, another review seat, a higher cap or work outside the listed
  tasks is a new ask.
- At most 3 agents running at once, reviewers and panel seats included. Subagents never start
  subagents; a worker that starts its own reviewer has broken its brief.
- Every call states model and effort. Never `max`; never every agent on the strongest tier or on
  `high`; no panel the user did not ask for.
- Two writers never own the same path or mutable state. You take a task over only after its worker
  returned or stopped and you recorded that ownership moved.
- Reports are claims. UNVERIFIED is not PASS. Zero tests, `no tests ran` or all tests `deselected`
  prove nothing.
- The spec beats the plan; record every ruling. No ruling waives required acceptance, security or
  data correctness, and a product decision the spec leaves open goes to the user.
- Five fix rounds is a ceiling. No automatic relaunch, replacement or escalation.

## Shortcuts that break delegation

| Shortcut | What to do instead |
| --- | --- |
| "A fresh agent per task keeps context clean." | Every start-up costs ~60k tokens. Keep related tasks in one lane; start a fresh worker only when the lane's context would mislead it, and list it. |
| "I'll paste the plan so it has full context." | Write a brief file and pass its path. Pasted text stays in your context for the rest of the session and buries the task for the agent. |
| "Six failing tests, six agents." | Group failures by cause first. A shared cause is one investigation. |
| "The reviewer will over-flag; I'll tell it what to skip." | State the requirement and your ruling as facts. Let it raise what it sees; adjudicate afterwards. |
| "The worker says all tests pass." | Read the run: a failing assertion first, then a pass, with tests selected. `7 deselected` proves nothing. |
| "It stopped on a usage limit; I'll just resume it." | Report what happened and ask, or take the task over inline after attributing its partial edits. |
| "The idle worker needs a new approval to fix its own task." | No. A listed worker that returned normally gets its task's fix rounds inside the envelope. |
| "The plan says 600, so 600." | The spec is the authority. Rule, record, and carry the ruling into the brief. |
| "One more round will converge." | Five is the ceiling and rounds without new evidence end earlier. At the cap, rule on each finding. |
| "A slot is free, so I can start another agent." | Only agents the envelope lists. |
| "Close enough on spec compliance." | A spec gap means not done: fix it or rule on it at the cap. |

## Red flags

- An agent call without an explicit model or effort.
- A dispatch longer than its brief, or a pasted plan or conversation.
- "do not flag", "at most Minor" or "the plan chose" in a reviewer prompt.
- A consumer started before its producer was accepted.
- Two running agents owning overlapping paths, the same manifest or the same service.
- A DONE accepted without reading its diff.
- An agent resumed after it failed or stopped, without the user's yes.
- Rulings in the journal that the final report does not list.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from evidence. This
skill owns the delegation decision, briefs, prompts, routing of returns and acceptance; the method a
subagent applies stays with its own skill. Coordinator brevity never truncates these. Loading this
skill grants no authority: create branches or worktrees, reset, commit, push, install or publish
only under authority you already have, never because a reference skill does so. Run the helper scripts from the
installed skill folder, not the project root: `scripts/task_brief.py`, `scripts/review_package.py`,
`scripts/delegation_workspace.py`.

## Output

- For a run: the mode decision, the pre-flight table, the envelope message, brief files, dispatch
  calls, journal lines, acceptance evidence per task and a final report with what is not verified,
  deferred findings and "Rulings I made".
- For an inline decision: one line saying why no agent starts.

## Verification

Before you call delegated work done:

- [ ] every agent call had an explicit model and effort and was inside the approved envelope;
- [ ] no two running agents shared write ownership;
- [ ] you read every task's diff and proof; every criterion has an observation, and UNVERIFIED
      items are named;
- [ ] reviewer prompts stated requirements and rulings and never told the reviewer what to skip;
- [ ] the combined checks ran on the integrated files;
- [ ] the final report lists every ruling with its cost if wrong.

These checks are properties of the run. Structural checks and helper tests prove bounded properties
only; how a model behaves with this skill stays NOT_VERIFIED without a real trial.

## Worked example and anti-pattern

The [worked example](resources/worked-example.md) runs a nine-task plan with two lanes and one
reviewer: cost decision, pre-flight table, envelope, brief and dispatch, a review and fix round, a
concern settled by the spec, integration and the final rulings list, then the small-plan contrast
and recovery after a reset.

Anti-pattern: a fresh implementer and a reviewer for every task of a small plan, each dispatch
pasting the plan, the reviewer told which findings to skip, and a usage-limited worker quietly
resumed.

## Fallback

- The host cannot start agents, or cannot set model and effort per agent: work inline, or say in
  the envelope that agents inherit the session's settings and prefer inline when those are the
  strongest tier.
- A returned agent cannot be messaged: a fresh agent carrying the brief, the report file and the
  open findings replaces it, which is a new agent and a new ask.
- The helper scripts are unavailable: write the brief by hand, and package the change with
  `git log --oneline`, `git diff --stat` and `git diff -U10 BASE..HEAD` into one file.

## Local resources

- [The rules](resources/contract.md)
- [Briefs and prompts](resources/subagent-brief-and-report-schemas.md)
- [Pre-flight and frontier](resources/frontier-and-dag-protocols.md)
- [Review and finishing](resources/two-track-review-and-fix-loop.md)
- [Host calibration](resources/host-cost-calibration.md)
- [Workspace and recovery](resources/workspace-and-isolation-guards.md)
- [Worked example](resources/worked-example.md)

## Operational example (offline)

This retained synthetic fixture checks DAG/path examples, not autonomous model behavior.

```andino-operational-example
{
  "concurrency_limit": 3,
  "max_fix_rounds": 5,
  "tasks": [
    {"id": "t1", "deps": [], "files": ["src/auth/signer.py"]},
    {"id": "t2", "deps": [], "files": ["src/auth/store.py"]},
    {"id": "t3", "deps": ["t1", "t2"], "files": ["src/auth/middleware.py"]}
  ],
  "collision_pairs": [
    {"t_a": ["src/core"], "t_b": ["src/core/utils.py"], "valid": false},
    {"t_a": ["src/api/v1.py"], "t_b": ["src/api/v2.py"], "valid": true}
  ],
  "expected_frontier_step_0": ["t1", "t2"],
  "expected_frontier_step_1": ["t3"]
}
```

## Provenance

Adapted from `mattpocock/skills:skills/engineering/implement-spec` (commit 6f7f783) and
`obra/superpowers:skills/{dispatching-parallel-agents,subagent-driven-development}` (commit
22f0b46). From Matt Pocock: context pointers, the task graph and its frontier, shared exploration
notes. From Obra: independent problem domains and focused prompts, the pre-flight scan, task review
of spec then quality, scoped re-reviews, the single final fix wave, the rulings list, batching,
bounded waiting and model choice by turn count. The cost gate, lanes, the envelope, the limits on
every agent and evidence identity are Andino's. MIT notices: [references/license.md](references/license.md).
