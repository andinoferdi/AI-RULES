---
name: ai-codebase-rescue
description: Stabilize fragile, patch-heavy codebases and bounded subsystems through evidence-first diagnosis, regression protection, and KEEP/REFACTOR/REMAKE/REMOVE/INVESTIGATE decisions. Use for repeated regressions, material ownership or contract drift, technical-debt recovery, production hardening of fragile prototypes, or bounded remake requests. Do not use for routine local bugs, formatting, cosmetic cleanup, ordinary features or reviews, or AI authorship alone.
---

# AI Codebase Rescue

Judge engineering condition, not suspected authorship. Preserve verified product
and behavioral contracts; do not preserve accidental implementation complexity.

## Lifecycle boundary

This is a specialist methodology inside `andino-workflow`. Andino owns task
classification, the execution plan, phase state, checkpoint, authoritative
`NEXT ACTION`, and completion. Consume its objective, approved scope, acceptance
criteria, current phase, evidence and stop condition. Reuse current evidence.
Do not create a rescue plan format, router, checkpoint store or independent DONE.

On direct invocation, first bind to the existing Andino plan; if none exists,
use Andino's normal plan contract for non-trivial work. If Andino is unavailable,
return scoped findings and the missing lifecycle context without inventing a
replacement lifecycle. Tool or memory availability never establishes truth.

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

## Establish the scoped evidence

1. Inspect applicable rules and current Git status, diff, branch and target.
   Protect user changes. An overlapping unknown change, wrong base or conflicting
   instruction stops mutation of the affected area; report the conflict to Andino.
   Do not reset, stash or move user changes to make inspection convenient.
2. Identify intended behavior using requirements, trusted tests, consumers and
   runtime evidence. Record public interfaces, data and permission invariants,
   side effects, error behavior and relevant user experience. Existing behavior
   is evidence, not automatic proof of correctness; identify intentional fixes.
3. Capture a reproducible baseline and assess test trust before editing. Record
   command, environment, observed result and pre-existing failures. If tests are
   missing, use meaningful characterization, fixtures or repeatable manual proof
   appropriate to risk. Material uncertainty remains INVESTIGATE.
4. Map only the target's consumers, integration points, dependencies and state/data
   ownership. Inspect risks supported by signals: correctness, data loss, access
   control, resource lifecycle, concurrency, dependency facts or measured runtime
   behavior. Do not scan the whole repository or run a universal audit by habit.

Read [evidence and findings](references/evidence-and-findings.md) when classifying
findings or preparing the return packet. Tie each finding to verifiable behavior
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
Contract, Baseline, Risk, Safety and Scope** gates in the shared plan. All material
gates must PASS before replacement begins. Failure or unknown evidence produces
INVESTIGATE and a concrete next check, never speculative replacement.

Full repository rewrite is a separate modernization/migration program. Do not
expand a bounded request into it; its evaluation requires explicit authorization
and the additional evidence threshold in the reference.

## Remediate and compare

Within existing authorization, establish regression protection for critical
contracts, then implement only the justified boundary using repository conventions.
Preserve verified behavior while correcting the documented defect. Do not add
dependencies, abstractions, fallback paths or migration machinery without a
demonstrated need. Stop affected work if new evidence requires a material product
decision, unsafe mutation or expansion beyond scope.

Compare results with the baseline using targeted behavior checks and broader
checks proportional to affected integrations. Include failure paths and relevant
permission/data invariants. Performance claims require comparable measurements.
Do not delete or weaken tests, suppress errors, fake success, or update snapshots
merely to conceal a regression. Remove old implementation only with obsolescence
proof, then verify the resulting integration again.

Follow Andino's anti-loop rules: repeat a failed action only with changed state or
new evidence. Report unavailable verification and remaining uncertainty honestly.
Commit, push, publication, deployment and live-data operations require applicable
user authorization; a rescue request alone does not grant it.

## Read references by risk

Load only what the current evidence requires; domain presence alone is not a reason
to read every reference. Each operational reference is available directly here:

- [Audit taxonomy](references/audit-taxonomy.md): when selecting which risk signals
  warrant deeper inspection; use relevant domain extensions only.
- [Regression and verification](references/regression-and-verification.md): when
  establishing baseline/protection, assessing test trust or substantiating claims.
- [Frontend runtime stability](references/frontend-runtime-stability.md): only for
  rendering, scroll/input, layout synchronization or animation/runtime symptoms.
- [Security and production hardening](references/security-and-production-hardening.md):
  when trust, sensitive data, configuration or migration/release risks are implicated.
- [Validation scenarios](references/validation-scenarios.md): only when developing,
  reviewing or validating this skill; not automatically during rescue execution.

## Return evidence to Andino

Return eligibility, boundary and baseline; structured findings with severity,
confidence and disposition; preserved contracts and intentional changes; proposed
versus actual remediation scope; regression protection; remake gate evidence when
relevant; changed files and actual verification outcomes; remaining risks, blockers
and a concrete recommended next action. Distinguish implemented, verified, deferred
and unverified results. Andino incorporates this packet into its existing plan and
decides acceptance and authoritative NEXT ACTION. This method creates no parallel
phase system and makes no independent lifecycle completion claim.
