# Delegate Disjoint Work Under Parent Ownership — Deep Craft Guide

Internal Andino resource for `andino-delegation`. The user/project/host govern
authority and resources; this guide owns delegation craft. The existing plan
owns status. Supporting scratch artifacts do not create a second lifecycle.

## 1. Choose the useful mode

Start inline. Compare work saved with child start-up, briefing, integration and
review cost. A small change can require careful thought without benefiting from a
new agent. A large coupled change can also be cheaper inline. Do not treat task
count, file count or line count as a dispatch trigger.

Parallel dispatch fits distinct domains with stable interfaces, disjoint writes
and no shared mutable fixtures/services. Shared root causes need inline diagnosis.
Subagent-driven implementation fits ready tasks whose isolated context adds enough
value to justify the handoff. One worker and one model own a lane of related tasks.
Only dependency-ready tasks run; lane membership does not bypass parent acceptance.

Read [the contract](resources/contract.md) and the relevant recipes. The selected
domain method still owns implementation/testing; delegation does not replace it.

## 2. Preflight before spending

Read accepted spec/plan, current worktree and existing changes. Identify exact
acceptance values, global constraints, produced/consumed interfaces and test setup.
Verify that each ready task has an actual change specification, not a milestone.

Pin the worktree, BASE and owned paths. Stable shared reads are permitted; mutable
shared state must be isolated or serialized. Do not create branches, reset worktrees
or commit merely because an upstream reference does so. Reuse session authority.

For delegated work needing durable handoffs, run
`python scripts/delegation_workspace.py PLAN` from this skill directory, then
inspect its ownership marker. Scripts are relative to the installed skill directory,
not the project root. An inline task does not need scratch setup. The plan records
current state; a journal may retain detailed worker history and file pointers.
See [workspace and recovery](resources/workspace-and-isolation-guards.md).

Exit: current plan/spec, attribution, ready contract and real ownership are known.

## 3. Frontier, wave and brief

Use [frontier rules](resources/frontier-and-dag-protocols.md). A prerequisite is
satisfied only after parent acceptance against still-current source/check inputs.
Maximum three concurrently active direct children, including reviewers; no nested
spawning. Eligibility alone does not authorize dispatch.

Before each wave state:
- count, lanes/tasks and why delegation is cheaper/usefully independent;
- real host model and effort for each child, plus role and owned worktree/paths;
- planned reviews, proof, stopping condition and any unavailable controls.

Wait for the user's go-ahead. Record the approved scope in the plan.
No automatic relaunch of failed, stopped or quota-limited workers. A changed role, replacement,
model/effort or additional review needs applicable wave approval.

Run `python scripts/task_brief.py PLAN TASK_ID` to extract one task. It recognizes
legacy `Task ID:` and canonical `ID — title` headings, preserves nested sections
and ignores fenced headings. Duplicate/missing IDs fail. It does not copy global
requirements or decide readiness. Complete the [brief recipe](resources/subagent-brief-and-report-schemas.md)
with spec/global pointers, exact interfaces, prior accepted decisions and expected
proof. Read the result before dispatch. Never substitute pointers for missing facts.

Exit: approved wave, complete brief, exact controls and pinned input identity.

## 4. Worker status is a decision point

Read the short reply and full report; reconcile actual worker state and partial
bytes before acting. DONE is unaccepted work. DONE_WITH_CONCERNS needs each concern
graded by actual consequence. NEEDS_CONTEXT needs the missing interface/decision,
not a stronger model by default. BLOCKED needs the exact failed operation and
bounded next check. A missing report, stopped child or quota failure calls for
inspection and a recovery choice, never blind redispatch.

If ownership is transferred inline, stop/reconcile the child first, record that it
relinquishes ownership and preserve its valid work. Apply the same implementation
and acceptance checks. Workers cannot start dependents or publish by themselves.

Exit: known output identity, report and a grounded review/recovery action.

## 5. Review and bounded repair

Parent reads the complete owned diff and proof for every task. Meaningful behavior
changes need intended RED then GREEN; static documents need suitable artifact checks.
Missing imports/tooling or zero discovered tests do not demonstrate behavior.

For risky changes add one approved reviewer covering both tracks: spec first,
then quality. Risk includes security, state machines, races, renderer/3D, money,
migrations and data integrity. Require criterion-to-code/test evidence and concrete
findings. A reported passing test is still unverified testimony until observed.

`python scripts/review_package.py PLAN BASE HEAD` packages committed changes only.
Record dirty/new owned files separately with current content identity; never claim
an empty/old commit range covers WIP. Give a reviewer the actual complete change.
UNVERIFIED requires a focused observation or remains a blocked criterion.
Follow [review and repair](resources/two-track-review-and-fix-loop.md).

Five rounds is a maximum, not a target. Stop earlier when no new evidence appears.
A stopped worker needs go-ahead to resume. Replacement or escalation is proposed,
not automatic at a round number. A ruling can reject a demonstrated false positive
or defer optional polish; required acceptance remains open until satisfied.

Exit: current acceptance observed, material findings resolved, review identities known.

## 6. Integrate, checkpoint and finish

Parent reconciles concurrent changes and reruns the wave's real public integration
gate. Review worker outputs for incompatible assumptions even with disjoint files.
Only parent-accepted tasks unlock consumers. Reuse unchanged valid evidence rather
than rerunning every suite per worker.

Review the whole owned change for cross-task behavior and completeness. Choose
one independent final reviewer only when its value/risk and approved wave justify
the cost. The parent can perform a distinct two-track self-review; disclose the
lack of independence. Never automatically select capable/high because review is final.

Record accepted source/check/environment identity, rulings, remaining risks and one
NEXT ACTION in the authoritative plan. Retain handoff evidence by default. Scoped
teardown requires authority and containment/ownership checks. Commit, push, setup
and publication are distinct outcomes; finish those already authorized and verify
their resulting state. Checkpoint/context compaction does not itself authorize
another wave or require a context-clearing feature the host cannot provide.

## 7. Select real model and effort controls

Map portable tiers through [host calibration](resources/host-cost-calibration.md).
Declare actual model AND effort on every implementer/reviewer dispatch.

| Work | Starting tier / effort | Escalation evidence |
| --- | --- | --- |
| Mechanical work with exact changes/tests | Fast / low | Repeated substantive mistakes despite a complete brief |
| Ordinary modules, UI, integration, scoped review | Standard / medium | Concrete unresolved complexity |
| State machines, races, renderer/3D, cross-section threads | Capable / medium | Plan-identified risk can justify high |
| Final review | Lowest adequate tier / low or medium | Broad consequential risk can justify capable/high |

Never max; never every child capable or high. Fixes do not change a lane's model in
place: propose an approved replacement when needed. If explicit selection is not
exposed, state the host limitation and prefer inline; do not invent tool arguments.

## 8. Evidence and provenance

[Worked example](resources/worked-example.md) demonstrates handoff quality and
resource decisions. Static checks and helper tests prove bounded properties;
independent model behavior stays NOT_VERIFIED without real approved evaluation.
Upstream mechanisms are adapted to these guards, not imported as authority:
context pointers/frontiers from Matt Pocock and independent domains/spec-quality
review from Obra. [MIT notices](references/license.md).
