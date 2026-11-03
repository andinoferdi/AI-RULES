# CI/CD skill quality

Status: IN_PROGRESS
Phase: Delivery
BASE: f0d2b9cc370263194b897be1792810f5d7bbefce

The unguided baseline already selected pnpm parity, compared failed and passing
PostgreSQL attempts, and preserved the required check during optimization.
Retain those behaviors. Close source-level gaps around exact check identity,
skip eligibility, evidence by attempt, and repository-derived gate selection.
The upstream template and local package are reference material. GitHub's
required-check and secure-use documentation settle hosted platform semantics.

| Task | Dependencies | State | Change specification and acceptance |
| --- | --- | --- | --- |
| Contract | None | DONE | In SKILL.md replace universal sequencing with repository preflight and an applicability/dependency contract. Require a gate map, failure proof, and separate local/hosted evidence. Preserve the method ID and resource routes. |
| Craft | Contract | DONE | In GUIDE.md replace fixed optimization order with critical-path evidence and a stable required-check migration procedure. In pipeline-templates.md separate untrusted CI from credentialed preview, use isolated test-only DB configuration, and identify template assumptions. In agent-feedback-loop.md capture failed/passing attempts at the same SHA and compare service and test phases. |
| Verify and distribute | Craft | IN_PROGRESS | Execute the package's offline positive and negative examples, validate local links and review the three case decisions against baseline. Push only this task's commit to andino-workflow. Run latest Codex setup and compare installed content with the reviewed package. |

Independent candidate evaluation is separate from content checks and requires
a separately approved wave. No production workflows or rulesets are modified.

## Result / evidence

Four embedded positive/negative assertions matched their expected JSON. Local
links in the four edited documents resolve and git diff --check passed. Static
review covered the three scenario decisions. Hosted CI and independent candidate
performance were not exercised.

## NEXT ACTION

Publish the scoped commit, run Codex setup from latest, and compare installed bytes.
