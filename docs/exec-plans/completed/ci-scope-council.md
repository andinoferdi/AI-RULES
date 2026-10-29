# CI scope council

Status: DONE
Depth: LITE
Date: 2026-10-29

## Objective and acceptance

Recommend an evidence-based audit scope for AI-RULES CI/CD using Council.
Return the scope, material disagreement, limitations, and one next action.
This is decision support, not authorization to implement workflow changes.

## Constraints and decisions

- No automated live-model evaluations in CI; user prefers human behavioral testing
  to avoid rate-limit and token consumption.
- User explicitly requested Council delegation for this decision.
- Andino limits delegation to three direct children and prohibits nested spawning.
  Adapt Council to three independent advisors covering five lenses, followed by
  anonymous cross-review; do not claim the full five-independent-advisor procedure.
- Workers are read-only, use the same brief, and have disjoint response ownership.
- No commits, pushes, publication, or workflow/configuration changes.

## Current state and phase

CURRENT PHASE: Decision delivered

| Phase | Status | Evidence |
| --- | --- | --- |
| Frame decision | DONE | Current workflows, pyproject, eval README and installer test files inspected. |
| Independent advice | DONE | ci_scope_principles, ci_scope_challenge, ci_scope_execution returned independent judgments from identical evidence briefs. |
| Anonymous review and decision | DONE | Three independent reviews of anonymized response summaries A-C returned; chair synthesized recommendation and stop conditions. |

## Shared neutral decision brief

AI-RULES distributes skills on branch refs and ships a Python installer/CLI.
The user sees a short green validation job and asks whether CI coverage suits the
project, which contains many skills. Decide the most useful audit scope:
(A) whole repository and all skill families in depth now; (B) Andino only;
(C) a bounded repository-wide risk map with focused investigation where evidence
warrants it; other justified options may be proposed. No implementation is requested.

Verified local evidence: validate-skills.yml runs on main pushes/PRs, manual dispatch
and a daily schedule. It fetches nine named branch refs, installs the package,
executes package validation, Three.js schema/inventory validation, capability
schema validation, unittest discovery from tests, and skripsi traceability audit.
tests/installer/__init__.py exists; installer tests exist, so their absence from CI
cannot be inferred from the job name. release.yml separately builds on Windows,
macOS and Ubuntu using Python 3.12, smokes the artifact with --help, and publishes
on version tags after build succeeds. It does not explicitly depend on the other
workflow's validation; hosted protection and other policy gates are UNKNOWN.
Validation runs on Ubuntu without an explicit setup-python step. pyproject requires
Python >=3.11 and uses setuptools, questionary and rich. evals/README.md explicitly
states schema/structure checks do not prove live model behavior; CI never calls a
model. User rules out automated live-model testing in CI and prefers human testing
for behavior. Do not argue to add it or estimate unmeasured savings. Distinguish
configuration evidence from executed checks. No tests have been run in this review.
Existing CI test breadth, release integration, pinned bundle/ref alignment, and
cross-platform install behavior require targeted evidence before asserting gaps.

Requested output: recommendation with rationale, strongest objection, concrete
inexpensive first action, evidence limits. Keep response within 220 words.

## Method evidence

- Andino, its CI guide and delegation guide read from the installed package.
- Native ci-cd-and-automation SKILL.md read in the preceding turn.
- Native council SKILL.md read this turn; adapted procedure declared above.
- Shared evidence is reused from unchanged inspected local files.
- Verification guide read before accepting worker reports. Parent compared each
  factual basis with the inspected configurations; no workflow or behavioral test
  pass is claimed. No implementation or suite execution was required for this decision.

## Result and chair decision

All three advisors selected C: bounded repository-wide coverage map, followed by
focused investigation of concrete risks. First Principles and Outsider lenses were
assigned to ci_scope_principles, Contrarian and Expansionist to ci_scope_challenge,
and Executor to ci_scope_execution. This is an adapted three-advisor Council,
not five independent advisors or five distinct model providers. Host model defaults
were used; model identities were not independently established.

Anonymized summaries were ordered A=execution, B=principles, C=challenge, without
author or lens names. All three reviews preferred C's claim-to-command-to-artifact
traceability and explicit evidence status. Reviews independently flagged the lack
of acceptance/stop criteria, and warned that release/ref checks were candidates,
not proven highest-priority risks. No substantive disagreement about scope emerged.

Chair recommendation: cover skill package integrity, installer/CLI regressions,
source/ref-to-bundle alignment, and release gates at map level. Deep investigation
requires a concrete unprotected failure or material unknown affecting users.
Map each distributed component to source/ref, actual check, failure consequence,
evidence status, and any human-only behavioral acceptance. Stop the mapping once
these links and relevant unknowns are explicit; do not demand prose review of every
internal guide or add jobs merely to make CI look complex. Rank unknowns by user
impact before choosing one focused follow-up. An observed failing regression,
missing guard for a concrete failure, or unverifiable high-impact release path
justifies deeper work; a job's short duration does not.

Human behavioral testing remains manual and targeted to changed high-impact
instructions/routing, recording prompt, runtime revision, observed behavior and
pass/fail. This does not prove deterministic package/installer correctness, which
belongs in model-free CI. No automated model evaluation is proposed.

The decision task is complete. CI adequacy, hosted protection, and cross-platform
functional correctness remain unverified; the recommendation does not assert gaps.
Only this decision checkpoint was added; workflow/configuration files are unchanged.

## NEXT ACTION

Proposed follow-up: build one bounded coverage matrix for AI-RULES linking each
distributed component to current checks and evidence, then rank concrete risks.
Audit execution and workflow changes are outside this completed decision task.
