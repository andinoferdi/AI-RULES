# Bounded remake

Use when evidence suggests replacing an existing implementation within a known
boundary. Preserve verified product and behavioral contracts; do not mechanically
port accidental internal structure into the replacement.

REFACTOR keeps the existing implementation as its foundation. REMAKE builds a new
implementation behind a preserved contract. Compare both against the observed
failure, change risk, verification cost and maintenance burden. A preference for
cleaner code or AI provenance is not a replacement rationale.

## Entry gates

Record PASS, FAIL or UNKNOWN and the supporting evidence for each gate in the
active task record. All material gates must PASS before replacement implementation.
An unknown or failed material gate means INVESTIGATE with a specific next evidence
action. Do not average gate scores or treat urgency as permission to skip safety.

| Gate | Required evidence |
| --- | --- |
| Boundary | Named modules/files/service/interface, principal consumers, dependencies and integration seams; bounded blast radius. |
| Contract | Verified behavior, public interfaces, data/permission invariants, side effects and relevant error/UX behavior; intentional corrections distinguished from preserved behavior. |
| Baseline | Relevant reproducible test, trace, fixture or repeatable manual proof, including current failures and limitations of test trust. |
| Risk | Evidence that internal structure materially causes fragility or defects, plus a concrete explanation of why incremental repair would preserve the problem or incur worse risk/cost. |
| Safety | Regression/characterization protection for critical contracts and a viable controlled swap/recovery path; data recovery where persistence is affected. |
| Scope | Existing authorization covers the bounded change; no silent product decision, unrelated subsystem change or unauthorized migration. |

Passing gates does not authorize separate destructive Git, live-data or external
operations. Escalate only the actual missing decision or permission. Continue
independent safe work where useful; do not widen the boundary to make gates pass.

## Replacement sequence

1. Capture preserved contracts and known defects. Do not canonize an existing bug
   merely because a characterization test reproduces it; document the intended fix.
2. Identify consumers and seams, then establish meaningful regression protection
   before replacing critical behavior. If safe protection cannot be established,
   return INVESTIGATE instead of pretending the baseline is adequate.
3. Design the smallest replacement boundary from the verified contracts. Follow
   repository conventions; avoid carrying over the diagnosed accidental complexity.
4. Build within that boundary and integrate through a controlled seam. Use an
   adapter, flag, parallel path or branch-by-abstraction only when consumer count,
   comparison needs or cutover/recovery risk justifies its cost. A self-contained
   target can use a direct swap with equivalent protection.
5. Compare old/new behavior with fixtures or safe dual runs where practical.
   Never duplicate payments, writes or other irreversible effects to obtain a
   comparison. Use isolated fixtures or read-only observations instead.
6. Switch consumers, verify target contracts and checks proportional to integration
   risk, and apply the defined recovery action if acceptance fails. Do not claim
   success from compilation alone or from an unmeasured performance impression.
7. Prove the old path obsolete before authorized removal: inspect static consumers,
   dynamic registration/configuration, public extension points and operational use
   where relevant. A no-hit text search alone may miss a runtime consumer.
8. Remove proven obsolete paths and temporary migration machinery when no longer
   required. If coexistence must remain, record why, its risk and removal condition.
   Verify again after cleanup, then return evidence, deviations and residual risks
   to the active task's existing checkpoint or host context.

Choose the smallest sufficient sequence; these are evidence obligations, not a
new mandatory phase system. Stop affected mutation if the boundary expands,
contracts conflict, user edits collide, or replacement requires an unapproved
product decision. Reassess the disposition with the new evidence.

## Full repository rewrite is a separate program

Do not recommend "rewrite the repository" unless all of the following hold:

- The owner explicitly authorizes evaluation of full rewrite.
- Evidence shows system-wide problems, not merely several bounded defects.
- Incremental and seam-based alternatives were evaluated and shown inadequate
  with concrete reasons.
- Critical product contracts and business invariants are mapped.
- Data and integration migration strategy is understood.
- Coexistence, cutover and rollback/recovery strategy is available.
- Operational and deployment risks are understood.
- Cost, time and maintenance tradeoffs are compared with incremental remediation.
- Cross-system verification and acceptance strategy is available.

Authorization to evaluate is not authorization to execute. Return bounded options
or INVESTIGATE when this threshold is unmet; the user and active lifecycle owner
govern any separate modernization program. Severity, frustration and code authorship do not
lower the threshold.
