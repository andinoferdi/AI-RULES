# Andino reliability repair

Status: DONE
Depth: STANDARD
Current Phase: Publication

## Executive Snapshot

Completed2026-10-29: internal-first dispatch/handoffs across59 methods/53 aliases published as runtime65df26d. Main delivery37a8712 publishes the quality tooling and release19 pin; both remote SHAs verified. Full final339-test suite passes (one optional skip); real remote and actual repaired ai-rules.exe fresh/repeat/upgrade/backup/repeat pass.244 manual AI cases remain available; no model testing was performed. Details: docs/validation/andino-reliability/verification.json.

## Objective

Make internal method selection, loading, handoffs and acceptance explicit, observable and complete without forcing every task through all methods or adding a competing lifecycle/runtime router.

## Acceptance Criteria

- All59 canonical methods and source aliases remain available and accounted for.
- Explicit and implicit selection share one internal dispatch contract; quoted mentions are not instructions.
- Internal work methods load before Focus; style support does not replace or block task work.
- Accepted multi-step planning/execution transitions are explicit; locked decisions and simple-task shortcuts remain valid.
- Native siblings retain invocation/permission controls, explicit user choice, required research/domain ownership and existing UI policy.
- Existing evaluation infrastructure is reused; offline coverage includes explicit, implicit, negative and handoff cases.
- Offline checks distinguish structural success from unexecuted model behavior; manual test bundle is ready for the user.
- Relevant tests and package checks pass on candidate working bytes. No AI actor/evaluation CLI is launched.

## Scope and baseline

- Runtime checkout: C:/Users/Lenovo/Downloads/AI-RULES, andino-workflow at17ce784ad0aff4b6e299ff0f3ae7b4baa012a3a9. Existing untracked docs/ and src/ must remain intact.
- Quality checkout: C:/Users/Lenovo/.codex/worktrees/andino-reliability-quality/AI-RULES, detached at1a3b645336f5aa9edc065d9e5be863af5cda8584, initially clean.
- Prior audit/inventory remains in runtime checkout docs/. No commit, push, global installation or release-manifest update is authorized.
- Existing old readiness tests freeze Focus-first paragraphs. User now explicitly changes this policy; replace those byte-identity assertions with protected-contract checks rather than preserving the obsolete order.
- Search First reuse: current index, registry, aliases, evals/andino-unified.json, capability validators and actor record format already provide the needed foundation. No external dependency or new live harness needed.
- Rescue disposition: KEEP canonical guides and lifecycle; REFACTOR bounded dispatch/transition policy; INVESTIGATE future model reliability through user-run cases. No repository REMAKE.

## Execution Board

| Phase | Status | Result / Evidence |
| --- | --- | --- |
| Contract and regression | DONE | Baseline88 tests pass; new dispatch contracts fail4/5 on old runtime and pass5/5 on working bytes. Missing-alias and registry-heading regressions also observed RED then GREEN. |
| Runtime dispatch and handoffs | DONE | Internal-first entry/index/routing/adapter; explicit accepted-plan execution; planning-to-execution and review/verification handoffs. Permission/domain/UI contracts retained. |
| Coverage and manual evaluation | DONE |59 methods,53 aliases/57 target pairs,19 sibling declarations,9 instrument/native entries and244 manual cases pass offline catalog/fixture/package checks. Two fixture applications plus routing/priority/handoff controls exported. Model behavior NOT_VERIFIED. |
| Verification and review | DONE |336 general tests pass (one optional skip);108 affected Andino tests pass after review fixes;7 package/74 capability schemas pass;41 offline installer scenarios pass. Independent review findings fixed and rechecked. Source/export/install hashes match. |
| Publication | DONE | Runtime65df26d and main delivery37a8712 pushed normally and exact remote SHAs verified. Release19 pins runtime with sibling pins unchanged. Remote default-latest and actual installed CLI fresh/repeat/upgrade/backup/repeat PASS. Full final339-test suite PASS (one optional skip). |

## Publication continuation — 2026-10-29

The user's new request supersedes the prior no-commit/push/release-pin scope. Publish the ten reviewed runtime files to origin/andino-workflow, preserve unrelated untracked docs/src, then publish the matching main quality/release metadata needed for setup availability. Existing model-testing exclusion remains. Do not change global skill installations or publish a binary/tagged release unless needed by the actual default-latest path. Reuse unchanged verification evidence and verify real remote acquisition in disposable projects.

The actual installed ai-rules.exe failed with ModuleNotFoundError because its editable source points at the runtime checkout. Repairing the CLI installation is necessary to satisfy the user's request that the command works. Build a local non-editable wheel with the eight manifest-pinned bundles, install it without dependencies/network, then test the actual executable from a non-repository disposable directory without PYTHONPATH/home/source overrides. Global skill installations remain untouched; no tagged binary release is needed for default latest.

## Final evidence and decisions

- Runtime hash: af63474a8966cc8186ddf50882989c57c792b0a1bccb5e07b2eadc3b6f2bcfd9.
- Source and exported candidate are identical. Runtime remains at the original branch with uncommitted changes; quality remains the managed detached worktree. No commit, push, release-pin update or global install.
- Full suite initially failed imports because the global editable package pointed to the old runtime namespace. Process-local sys.path/PYTHONPATH selecting quality src/ resolved imports without changing installed state.
- Final review fixed relative export paths, evidence-template compatibility, multi-target alias coverage and missing protected Focus assertions. Three new manual/export regressions were observed failing before repair, then all108 Andino tests passed.
- No actor CLI was launched. Council/independent source review is distinct from model behavior testing; three-advisor/five-lens adaptation and capacity retry are recorded in council.md.
- Existing runtime untracked docs/ and src/ preserved. New runtime file references/method-dispatch.md is part of the candidate, not excluded as an untracked artifact.

## Neutral Council brief

The user authorizes full implementation and identifies three requirements: explicit requests are sometimes not followed across all internal methods; implicit requests must discover appropriate methods; Focus/external siblings must not displace internal work methods. They explicitly exclude running AI models as tests and will test their agents themselves. Existing runtime has59 GUIDE.md methods, source aliases, a native sibling registry and one lifecycle; main has validators and eval fixtures. Options: load every method upfront, internal intent/phase dispatch with guide activation before communication support, or split methods into native skills/new executable orchestration. Assess the smallest safe implementation under these requirements. Preserve required domain/research siblings, explicit native provider choice, permission limits and accepted UI policy. Existing Focus-first text-freeze tests need intentional replacement because user changes priority. Offline checks can prove catalog/fixture/contracts, not actual model selection/quality. Return <=180 words: recommendation, material risk, concrete invariant and evidence needed; no edits, actors or nested delegation.

## NEXT ACTION

None — requested commit/push and ai-rules setup availability complete. User may run ai-rules setup and reload the agent session. Manual AI behavior testing remains the user's separate follow-up.
