# Safe existing-installation lifecycle

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 3 — Verify and close
Last Updated: 2026-09-22

## Executive Snapshot

`setup` blocks unknown existing installations because it lacks a migration path. Implement explicit safe adoption and replacement: content-identical unmanaged first-party skills can be adopted without rewriting; differing skills can be replaced only with explicit approval, unique backup, staged verification, and rollback. Existing external integrations remain conservative unless compatible detection can prove they are already satisfied.

## Objective

Make repeated `ai-rules setup` behave as a safe reconciler/updater rather than an install-only command while preserving unknown user files by default.

## Acceptance Criteria

- [ ] Exact-match unmanaged first-party skills are adoptable without rewriting content.
- [ ] Different unmanaged first-party skills remain protected by default and are replaceable only after an explicit `--replace-existing` decision.
- [ ] Replacement has a unique backup and restores the old target after a post-replacement failure.
- [ ] Managed targets retain current update, repair, and downgrade protections.
- [ ] Explicit `--adopt-existing` and `--replace-existing` flags are wired through the CLI and resolver.
- [ ] State records only successful adoption/replacement outcomes.

## Scope

In scope: resolver actions, CLI flags, first-party content identity, safe directory transaction, state recording, and focused regression tests.

Out of scope: silent overwrite, changing profile membership, automatic marketplace installation, and unverified rewriting of external configuration or credentials.

## Current Technical Context

`ResolveRequest` already defines `allow_adopt` and `allow_replace`, but `_reconcile` ignores them. Existing unknown first-party paths become `UNKNOWN_ORIGIN` and block. `copy_tree_atomic` currently uses a capability-name backup path and removes the target before replacement, which is insufficient for repeatable rollback.

## Architecture / Approach

1. Detect first-party content equality using a deterministic tree digest of the local target and bundled target.
2. Route unknown matching targets to ADOPT only when explicitly enabled; route mismatches to REPLACE only when explicitly enabled; otherwise retain BLOCK protection.
3. Treat ADOPT as a state-only operation. Treat REPLACE/UPDATE/REPAIR as a staged directory transaction with a unique backup and rollback on verification failure.
4. Persist management state only for `APPLIED` operations after executor success.

## File Impact Map

### Create

- `docs/exec-plans/active/safe-existing-installation-lifecycle.md` — durable ticket state.

### Modify

- `src/ai_rules/cli.py` — expose controls and content-aware current state.
- `src/ai_rules/resolver/engine.py` — explicit adoption/replacement reconciliation.
- `src/ai_rules/execution/executor.py` — staged replace, unique backups, rollback, and state-only adoption.
- `tests/installer/*` — regression contracts.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Specify reconciliation and transaction contracts | DONE | Write failing behavior contracts | resolver/executor/CLI tests | Focused tests first failed for missing content identity and adoption behavior. |
| Phase 2 — Implement safe lifecycle | DONE | Wire flags and transactions | CLI, resolver, executor | Added explicit migration controls, deterministic tree identity, staged replace, unique backups, and rollback. |
| Phase 3 — Verify and close | DONE | Prove safety and regressions | focused/full validation | 101 tests, both validators, and compileall passed. |

## Decisions Log

- D-001 — No implicit overwrite. Reason: an existing folder without a verified ownership record may contain user modifications.
- D-002 — Content match is determined by deterministic full-tree identity, not a `SKILL.md` existence check. Reason: preserve ownership integrity.
- D-003 — External capability configs are not rewritten under this ticket because current detection establishes presence, not endpoint/auth equality.

## Verification Matrix

| Requirement | Verification | Status | Evidence |
| --- | --- | --- | --- |
| Adopt does not rewrite matching bundle | focused executor/CLI test | PASS | CLI integration test confirmed identical tree hash before and after ADOPT. |
| Replace creates unique backup and rolls back failure | focused executor test | PASS | Failure-injected transaction restored prior `SKILL.md`; unique backup retained. |
| Unknown targets remain blocked by default | resolver/CLI test | PASS | Resolver test confirms no action without explicit migration flag. |
| Flags enable only their intended action | resolver/CLI test | PASS | CLI test covers `--adopt-existing` and `--replace-existing`. |
| No regression | full unittest and repository validators | PASS | 101 tests, skill and traceability validators, and compileall exit 0. |

## Findings

### CONFIRMED

- `ResolveRequest.allow_adopt` and `allow_replace` are defined but not consumed by resolver reconciliation.
- `copy_tree_atomic` backs up to a reusable fixed target path and deletes the live target before attempting replacement.
- Context7 auto-adoption is limited to Codex when its credential-free `mcp list` output names `context7` and the expected official URL. Other hosts remain protected until their equivalent configuration identity can be verified.

## NEXT ACTION

None — ticket complete.
