# Delegation supporting contract

Internal Andino resource. One parent, one authoritative plan, bounded handoffs.

## Readiness and sparse handoff

A ready brief names outcome, spec/plan anchors and Global Constraints, exact owned
paths/worktree, current inputs, consumed/produced interfaces, settled decisions,
literal acceptance cases, verification commands/signals and report destination.
Pass minimal sufficient facts with pointers; transcripts and a whole plan are not
a substitute. An extraction helper does not infer or validate these fields.

A lane retains one worker/model for related work. Run only dependency-ready tasks;
parent acceptance of a producer precedes its consumer. An unrelated task does not
inherit approval just because a lane has a free worker.

## Authority, controls and recovery

Before each wave declare count, tasks, actual model, effort and review scope; wait
for the user's go-ahead. Maximum three concurrent children including reviewers;
zero nested spawning. Never max effort or every child capable/high. No automatic
relaunch of a failed/stopped/quota-limited child. No automatic calibration child.

Inspect live status and partial work first. NEEDS_CONTEXT receives the precise
missing contract; BLOCKED records evidence and a bounded next check. A worker that
has stopped needs go-ahead to resume even when the same task is unfinished. Reuse
an approval only for its exact still-valid scope; no automatic fresh worker or
tier/effort escalation at a round number.

Parent may continue inline after the worker relinquishes ownership. Attribute and
preserve partial edits; rerun unchanged acceptance gates. Parent and worker never
write the same lane concurrently.

## Review and acceptance

Parent inspects committed, staged, unstaged and owned untracked content. Pin
source, check and environment identities; missing fields do not match. A committed
diff package alone cannot cover dirty/new files.

Spec review maps each required acceptance criterion to observed implementation and
test/artifact proof, including missing/extra/misunderstood behavior. Quality review
then checks real consequences and regression risks. One reviewer can do both.
UNVERIFIED is neither PASS nor an optional concern: obtain targeted evidence or
leave the affected criterion blocked. DONE_WITH_CONCERNS is not parent acceptance.

Critical/Important findings block completion. Classify by real user effect, not
only whether the spec mentions the issue. Cosmetic preferences may be deferred.
Five repair rounds is an upper limit; stop earlier without new evidence. A ruling
cannot turn failed required acceptance into DONE. At the cap, preserve the blocker
and revise the grounded plan or ask for the missing user decision/authority.

## Integration and completion

Parent runs the public integration gate on actual combined bytes before unlocking
dependents. Disjoint paths do not prove compatible interfaces or shared-state
independence. Final whole-change review is required; another agent is conditional
on utility, risk and wave approval. Distinct self-review is disclosed as such.

The plan owns statuses, decisions, evidence and NEXT ACTION. A workspace journal
supports it, never overrides it. Resume checks drift and live workers before any
new dispatch. Retain evidence by default; cleanup requires scoped authority and
ownership/containment checks. Installed source, remote publication and activation
are separate claims.

Static contract checks and deterministic helper/integration cases are bounded
evidence. Independent model quality remains NOT_VERIFIED without actual approved
fresh-context trials; no claim of parity/superiority follows from keyword checks.

## Provenance

Adapted material retains [MIT notices](../references/license.md).
