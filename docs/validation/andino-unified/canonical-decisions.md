# Canonical design decision — 2026-10-18 (B-T02)

This is technical evidence within the existing execution plan, not a second plan.
Sources: the three snapshot audit manifests and their byte-identified source paths.

## Comparative TDD and refactoring ruling

Addy's skills/test-driven-development/SKILL.md requires repository command discovery,
RED for the correct behavior, minimal GREEN, real public-state tests, DAMP fixtures,
size-aware pyramid and no repeated unchanged tests. Superpowers' corresponding skill
and writing-good-tests.md add independently known expected values, mutation-sensitive
checks and GREEN-only behavior-preserving refactoring. Matt's engineering/tdd and
tests.md/mocking.md require public agreed seams, vertical tracer bullets, no tautologies,
and explicitly put refactoring in review, outside the RED→GREEN implementation loop.
Matt codebase-design adds the deletion test, small interface/deep implementation,
actual variation before adapters, and locality rather than speculative abstraction.

DECIDED: one canonical `tdd` method. Establish the accepted public seam and literal
behavioral contract from current project/spec evidence; ask only when an unresolved
material interface decision remains. Work one RED→GREEN slice at a time. Verify RED
fails for the specified behavior (not setup/import failure), then make the smallest
valid implementation pass. Refactoring is a separate optional review gate after GREEN:
justify an observed complexity problem, preserve behavior and seam, keep the baseline
green after each step, and stop if redesign or scope would change. Architectural
replacement requires its own accepted scope; it cannot hide inside a failing-test fix.
Existing human authorization/accepted seams do not require repeated approval.

## Ownership and retained techniques

- Andino owns discovery, depth, persistence, one checkpoint, delegation and acceptance.
  Upstream bootstrap injection, recursive routers, auto-installs and session hooks are excluded.
- `decision-interview` unifies Matt grilling, Addy interviewing and Superpowers requirements
  discovery: existing evidence first, concrete moments, goals/non-goals/anti-goals,
  only discriminating questions, builder-readiness check, optional safe visual/spike support.
- `planning` refines the single Andino plan; `decision-map` preserves live decision trees;
  `task-decomposition` produces dependent vertical slices/tracker drafts; `plan-execution`
  consumes the same accepted task graph. None owns a second plan or DONE.
- `debugging` unifies reproduction/environment checks, working-pattern comparison,
  evidence across boundaries, one hypothesis, minimal root-cause fix and failing regression.
  Three unsuccessful fixes cause an architecture reassessment, not a fourth blind patch.
  Transient retries remain at most two; permission/schema/auth failures are not retried unchanged.
- `code-review` combines spec then quality/security/performance as relevant, explicit diff
  scope including uncommitted/untracked owned files, evidence-backed feedback, mutation
  sensitivity and green-only refactoring. No mandatory praise, merge or nested reviewers.
- `verification` validates current bytes/actions; `delivery` prepares integration choices.
  Neither grants commit/push/merge/deploy/release authority or trusts worker self-report.
- `delegation` accepts independent disjoint tasks only with actual tools and authority,
  maximum three children, no nested spawning, shared files serialized, parent rechecks evidence.
- Git discipline/isolation preserve existing worktrees/user changes; this ticket permits
  only the existing main/andino-workflow branches. Raw upstream destructive/autocommit defaults yield.
- Focus owns communication, Search First owns required solution/external research,
  Rescue/Council/Skripsi/Three.js retain their current domain boundaries. UI coexistence
  and native manual-only/denied controls remain authoritative. Internal guides are resources,
  never alternate invocation routes for denied siblings.

## Resource/legal decisions

Preserve MIT notices for adapted expression from each local snapshot. Do not redistribute
Superpowers CODE_OF_CONDUCT.md (CC BY-SA 4.0 community policy), upstream branding/servers,
or anthropic-best-practices.md expression with unresolved independent notice. Its general
authoring ideas can be independently expressed. No loss of required runtime functionality.
Replace hazardous source-masking hooks with non-mutating protected-region guidance;
replace unsafe wizard/guardrail shell helpers with scoped procedures and honest fallbacks.
No hooks, process servers, telemetry, network fetch or setup tools run during installation.

Publication pins remain unchanged until authorized runtime publication. A candidate content
hash and release proposal identify uncommitted work; they are not invented Git releases.
