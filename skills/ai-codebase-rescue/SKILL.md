---
name: ai-codebase-rescue
description: Use when a fragile, patch-heavy codebase or bounded subsystem keeps regressing, when a team is afraid to change code that lacks trustworthy tests, when rushed or AI-assisted patches left duplicated logic, swallowed errors, silent fallbacks or phantom imports, when a prototype must be hardened for production, when contracts or ownership drifted across layers, or when someone asks to rescue, remake or rewrite a subsystem, including a read-only rescue assessment. Do not use for routine local bugs, formatting, cosmetic cleanup, ordinary features or reviews, dependency bumps, or AI authorship alone.
---

# AI Codebase Rescue

Judge engineering condition, not suspected authorship. Preserve verified product
and behavioral contracts; do not preserve accidental implementation complexity.

## Lifecycle boundary

This is a standalone specialist methodology. Use the active host's task context
and repository conventions for scope, acceptance, evidence and completion. Reuse
an existing plan or checkpoint; without one, record the objective, boundary, mode,
findings, verification and next action in the host's normal task context. Missing
`andino-workflow` does not block authorized investigation or remediation.

When Andino is active or the repository requires it, bind to its existing plan
and normal plan contract. Andino owns classification, phase state, checkpoint,
authoritative `NEXT ACTION` and completion; return evidence to that owner. Merely
installing Andino does not activate it or replace another active lifecycle.
Do not create a rescue plan format, router, checkpoint store, state file, tag or
competing DONE. Honor native invocation controls; do not install or activate
another skill just to run this one. Tool or memory availability never establishes truth.

## Eligibility gate

Proceed when evidence or the explicit request identifies a bounded rescue need:
repeated regressions, unreliable verification around risky changes, patch-on-patch
fragility, material architecture/ownership/contract inconsistency, or replacement
of an existing subsystem while preserving behavior.

Vague requests such as "clean this up", "technical debt", or "AI wrote this"
require a small targeted inspection. They do not establish defects or authorize
replacement. Ordinary local fixes, renames, dependency updates, style preferences,
normal reviews and greenfield features return to the ordinary workflow. Healthy
code may receive KEEP; do not manufacture remediation to justify activation.

## Choose the mode

| Mode | Use when | Produces |
| --- | --- | --- |
| Assess | The request asks for a diagnosis, audit or plan, or edit authority is absent or unclear | Read-only report: findings, dispositions, ranked targets and proposed steps with their protection |
| Stabilize | Edits are authorized and dispositions are KEEP, REFACTOR or REMOVE | Pinned behavior, small verified steps, report |
| Remake | An area's REMAKE disposition passed every bounded remake gate | Replacement behind preserved contracts, run through the Stabilize loop |

Record the mode in the existing task record. Dispositions stay per finding; one
request can hold KEEP, REFACTOR and INVESTIGATE areas.

## Establish the scoped evidence

1. Inspect applicable rules and current Git status, diff, branch and target.
   Protect user changes. An overlapping unknown change, wrong base or conflicting
   instruction stops mutation of the affected area; report it in the active task.
   Do not reset, stash or move user changes to make inspection convenient.
2. Identify intended behavior using requirements, trusted tests, consumers and
   runtime evidence. Record public interfaces, data and permission invariants,
   side effects, error behavior and relevant user experience. Existing behavior
   is evidence, not automatic proof of correctness; identify intentional fixes.
3. Capture a reproducible baseline and assess test trust before editing. Record
   command, environment, observed result and pre-existing failures. Name which
   existing tests exercise the contract and which only look green. If tests are
   missing, use meaningful characterization, fixtures or repeatable manual proof
   appropriate to risk. Material uncertainty remains INVESTIGATE.
4. Map only the target's consumers, integration points, dependencies and state/data
   ownership, including code reached through configuration, plugins or strings.
   Inspect risks supported by signals: correctness, data loss, access control,
   resource lifecycle, concurrency, dependency facts or measured runtime behavior.
   Do not scan the whole repository or run a universal audit by habit.
5. Choose the starting point from evidence: symptom, violated contract, change
   point and test point, ranked by churn, complexity and consumers. Read
   [triage and hotspots](references/triage-and-hotspots.md).
6. Sweep the target for signals common in rushed or agent-made patches: phantom
   imports, APIs or packages, swallowed errors and fake success, silent fallbacks,
   diverged duplicate rules, test doubles in production paths. Read
   [AI failure signals](references/ai-failure-signals.md). A signal is a lead;
   only its evidence check makes it a finding.

Read [evidence and findings](references/evidence-and-findings.md) when classifying
findings or preparing the report. Tie each finding to verifiable behavior
or a source/config path and known contract. Historical summaries are leads, not
proof when current artifacts are available. Every remediation finding must remain
valid with its provenance field removed.

## Choose a disposition per finding or area

| Disposition | Operational decision |
| --- | --- |
| KEEP | Verified behavior and proportionate structure have no material in-scope risk requiring change. Record evidence; make no forced cleanup. |
| REFACTOR | Keep the existing foundation; incrementally repair or restructure a bounded area with regression protection. Preserve external contracts except an explicitly intended defect correction. |
| REMAKE | Replace internal implementation behind verified contracts because evidence implicates the structure itself and explains why incremental repair is worse. Pass the gates below first. |
| REMOVE | Delete a proven obsolete path or dependency only after consumer, configuration and integration checks appropriate to risk. A quick search with no hits is insufficient proof. |
| INVESTIGATE | Contracts, boundary, baseline, permissions or evidence are materially uncertain. Name the next evidence action and what result would permit a decision. |

Severity determines urgency and impact; confidence expresses strength of proof;
neither automatically selects disposition. A severe defect may need a small repair.
Ugly or AI-authored code may need none. Prefer the smallest justified surface,
not the smallest patch when that patch would preserve the demonstrated failure.

## Bounded remake gate

Before choosing or implementing REMAKE, read
[bounded remake](references/bounded-remake.md). Record evidence for **Boundary,
Contract, Baseline, Risk, Safety and Scope** gates in the active task record. All material
gates must PASS before replacement begins. Failure or unknown evidence produces
INVESTIGATE and a concrete next check, never speculative replacement.

Full repository rewrite is a separate modernization/migration program. Do not
expand a bounded request into it; its evaluation requires explicit authorization
and the additional evidence threshold in the reference.

## Stabilize loop

Within existing authorization, repeat for each target in ranked order:

1. **Pin before change.** Add characterization tests, or a failing test for the
   defect, at the test point, and run them on the unmodified code. Pins pass on
   unmodified code; a failing pin is a wrong observation. A defect found while
   pinning is pinned as a known bug with its finding ID and recorded, never fixed
   in the pinning step. When code resists tests, read
   [safety-net techniques](references/safety-net-techniques.md).
2. **One concern per step.** A step is structure-only or behavior-only. When
   commits are authorized, stage only that concern's files and read the staged
   list before committing. Read [refactoring moves](references/refactoring-moves.md)
   for named moves, migration patterns and blast-radius checks.
3. **Check.** Run the pins and focused tests after every step. A structure step
   that turns a pin red is reverted and retried smaller; do not debug forward.
4. **Correct behavior deliberately.** A behavior step flips exactly the known-bug
   pins it fixes, in the same step, with the contract reason. Any other red pin
   is an unintended change.
5. **Trace downstream.** For each changed contract, list its consumers and any data
   already written under the defect that needs reconciliation.

Implement only the justified boundary using repository conventions, preserving
verified behavior while correcting the documented defect. Do not add dependencies,
abstractions, fallback paths or migration machinery without a demonstrated need.
Stop affected work if new evidence requires a material product decision, unsafe
mutation or expansion beyond scope.

Compare results with the baseline using targeted behavior checks and broader
checks proportional to affected integrations. Include failure paths and relevant
permission/data invariants. Performance claims require comparable measurements.
Do not delete or weaken tests, suppress errors, fake success, or update snapshots
merely to conceal a regression. Remove old implementation only with obsolescence
proof, then verify the resulting integration again.

Repeat a failed action only with changed state or new evidence, following any
active lifecycle's retry limits. Report unavailable verification and remaining uncertainty honestly.
Commit, push, publication, deployment and live-data operations require applicable
user authorization; a rescue request alone does not grant it.

## Read references by risk

Load only what the current evidence requires; domain presence alone is not a reason
to read every reference:

- [Triage and hotspots](references/triage-and-hotspots.md): when choosing the target.
- [AI failure signals](references/ai-failure-signals.md): for the sweep and your own diff.
- [Safety-net techniques](references/safety-net-techniques.md): before the first pin
  in code without trustworthy tests.
- [Refactoring moves](references/refactoring-moves.md): before the first change step.
- [Evidence and findings](references/evidence-and-findings.md): when classifying findings.
- [Regression and verification](references/regression-and-verification.md): when
  assessing test trust, recording the baseline or substantiating claims.
- [Bounded remake](references/bounded-remake.md): before choosing or running REMAKE.
- [Audit taxonomy](references/audit-taxonomy.md): when the risk signals are unclear.
- [Frontend runtime stability](references/frontend-runtime-stability.md): only for
  rendering, scroll/input, layout synchronization or animation/runtime symptoms.
- [Security and production hardening](references/security-and-production-hardening.md):
  when trust, sensitive data, configuration or migration/release risks are implicated.
- [Rescue report](references/rescue-report.md): before writing the report.
- [Worked example](references/worked-example.md): when the loop or report shape is unclear.
- [Validation scenarios](references/validation-scenarios.md): only when developing or
  validating this skill, never during a rescue.

## Report

Deliver the report in the [rescue report](references/rescue-report.md) shape:
Outcome; mode, boundary and eligibility; baseline and test trust; findings with
severity, confidence, disposition and evidence, including KEEP areas; changes, one
concern per row; preserved contracts and intentional changes; downstream impact;
verification as PASS, FAIL or UNVERIFIED per check; decisions for the owner;
deferred and INVESTIGATE items with their next evidence action; next action.
Include remake gate results when relevant, remaining risks and blockers, and keep
implemented, verified, deferred and unverified results distinct. Assess mode lists
proposed steps instead of changes. Never add health scores or percentages; report
measured signals.

In standalone use, the host reports completion only against the agreed scope and
actual verification, or records an actionable checkpoint. With Andino active, return
this packet to its existing plan; Andino decides acceptance and authoritative NEXT
ACTION. This method creates no parallel phase system or competing lifecycle completion claim.

## Done when

- Boundary, mode, baseline and test-trust verdict are recorded.
- Every finding has severity, confidence, disposition and evidence; assessed healthy
  areas are listed as KEEP.
- Every changed contract had protection that ran on unmodified code before the change.
- Every step held one concern, and its staged files matched that concern.
- Final checks are reported as PASS, FAIL or UNVERIFIED with no claim beyond them.
- Downstream consumers, data needing reconciliation and owner decisions are listed.
- The report is delivered, or returned to the active Andino plan.

## Sharp edges

| Failure | Guard |
| --- | --- |
| The fix lands before any test pins current behavior | Pin first and run the pins on unmodified code |
| One commit mixes a refactor with a behavior change, or two concerns | One concern per step; read the staged list |
| A bug found while pinning is fixed silently | Pin it as a known bug; fix it in its own behavior step |
| Debugging forward after a refactor step turns red | Revert the step and retry smaller |
| "Dead" code deleted after one text search | Check configuration, plugins, dynamic loading and external consumers |
| A missing API or package is invented or installed to make an import pass | Use a real API, or an explicit unsupported error and an owner decision |
| A health score or percentage appears in the report | Report measured signals only |
| The report says fixed or safe beyond the checks that ran | PASS, FAIL or UNVERIFIED per executed check |
