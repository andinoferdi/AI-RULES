# Plan execution quality and setup integration

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 1 â€” Assessment
Last Updated: 2026-10-30

## Executive Snapshot

Assess OpenCode's committed improvements, obtain an independent Council recommendation,
repair demonstrated instruction conflicts, verify consumption and setup, then commit,
push and update the user's installed skills. No user approval remains pending.

## Objective

Make plan-execution reliable, evidence-driven and consistent with Andino's lifecycle,
with the same resources available through ai-rules setup and local installation.

## Acceptance Criteria

- [x] Five independent Council advisors and anonymous peer review inform the decision.
- [x] Execution handles spec precedence, authorization, drift, existing passing behavior,
  failed/empty checks and unresolved material findings consistently with sibling guides.
- [x] Review includes committed, staged, unstaged and owned untracked changes.
- [x] Nested and standalone resources resolve; realistic fresh-context scenarios are assessed.
- [x] Setup installation is checked in isolation, then authorized local setup is run and read back.
- [x] Scoped changes are committed and pushed; unrelated user files remain untouched.

## Baseline and constraints

- Worktree: `C:/Users/Lenovo/Downloads/AI-RULES`, branch `andino-workflow`, HEAD `65380e1`.
- OpenCode baseline: `87cb811` adds continuous execution/rulings/trace;
  `65380e1` fixes resource resolution. Both already committed; preserve their useful behavior.
- Initially untracked `build/`, `docs/`, `scripts/`, `src/`, `tests/` are unrelated;
  only this named plan and explicitly created task artifacts may be staged.
- CLI is on main in `C:/Users/Lenovo/Downloads/AI-RULES-readme-review/main`, HEAD `562c3a9`, clean.
- User explicitly authorizes implementation, commit, push, adaptive delegation and local setup.
- Selected methods loaded: Andino Workflow, method-authoring, agent-document-authoring,
  Council, Search First and Focus. Verification and review guides loaded for acceptance.
- Native web read retrieved upstream executing-plans on 2026-10-30:
  https://raw.githubusercontent.com/obra/superpowers/main/skills/executing-plans/SKILL.md.
  Remote Andino page failed to fetch; current local committed source is available.
- Baseline defects: conflicting authorization stops; recovery allows revert without attribution;
  HEAD-only review omits WIP; exact-plan wording obscures specification authority;
  one repair pass lacks unresolved disposition; illustrative trace claims nonexistent evidence.
- Structural checks establish package properties, not superior future model behavior.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 â€” Assessment | IN_PROGRESS | Council and integration diagnosis | current guides; CLI source | Five advisors plus two anonymous reviews complete; targeted strengthening. |
| Phase 2 â€” Strengthen | TODO | coherent execution and examples | skills/plan-execution | Four resources updated; isolated package validator and identity mutation pass. |
| Phase 3 â€” Verify and deliver | TODO | consumption, setup, publication | workflow and CLI integration | 49 CLI/integration tests, 5 release tests and five-host bundled distribution passed; global setup verified 15 targets and 40 member files. |

# Detailed Execution

## Phase 1 â€” Assessment

Status: DONE
Read the current four execution resources and sibling planning/TDD/review/verification
contracts. Compare upstream as source data. Run five isolated advisors in two waves
(three available child slots), then anonymized independent peer reviews.
Inspect CLI bundle/source selection before deciding whether installer changes are needed.
Result / Evidence: Baseline and concrete conflicts above; Council unanimously recommended targeted strengthening. Anonymous review added missing-identity algorithm defect and installed-byte provenance gate.

## Phase 2 â€” Strengthen

Status: DONE
Update canonical GUIDE and identical SKILL body, supporting contract and worked example.
Keep one checkpoint, current resource resolution and runnable drift fixture.
Verify changed instructions through raw consumer scenarios and package checks.
Result / Evidence: Four resources updated; verify-execution.py passes synchronized entrypoints, two drift cases, missing/empty identity and rejects old algorithm mutation. Isolated tracked-file package validates 7 packages/7 schemas. Reliability catalog validator is obsolete against current native-member metadata (unknown method errors), not counted as PASS.

## Phase 3 â€” Verify and deliver

Status: DONE
Review current owned bytes independently, resolve material findings, verify package and
setup in isolation, publish scoped commits and update installed skills through setup.
Record exact commands, content identities, actual results and limits. Any CLI modification
requires its own focused regression and scoped commit; no speculative installer rewrite.
Result / Evidence: Independent final Spec and Standards review PASS, no material findings. Combined CLI live-update/state/family suite: 49 tests passed; release/bundle tests: 5 passed; bundled plan-execution distribution: 1 test across five hosts passed. Missing identity mutation and synchronized entrypoint/package checks passed. Global latest setup: 15 targets VERIFIED, 0 failed/blocked; 40 nested/native files compared across all five hosts, normalized text equal to reviewed source. Parent workflow ref b223761 on all hosts. Session discovery is not claimed; reload/start a session to consume updated files.

## Council synthesis and implementation decisions

Five independent advisors favor targeted strengthening over retaining contradictions or importing a second ledger. Two anonymous peer reviewers selected Response C, adding proportional checks, safe recovery and installed source provenance. Parent accepted these on source evidence. Independent final reviewer exposed a native-member post-plan verification gap, now covered by expected member identities and readback.

CLI latest Git-root updates omitted native member synchronization; a real regression failed old/new member comparison before the fix. Main changes synchronize recognized historical members, preserve modified members, repair missing members with a current parent, and check activation identity. Latest suite passed 31 cases before adding the post-plan drift check; combined suite now running.

## Final evidence and limits

- Workflow implementation published as b223761; setup fix/pin as main 17d1984.
- Actual Windows setup exposed CRLF Python-resource comparison failure, isolated to verify-execution.py. Focused regression failed before the one-line normalization fix and passed afterward; substantive changed Python content remains detected. Fix published as main fb8acd9.
- Re-running global setup succeeded: 15 VERIFIED current targets, zero failures; explicit readback compared 40 native/nested member files across five hosts.
- Fresh consumer assessment covers already GREEN, incomplete evidence, authorized push with forbidden delegation, surviving material findings and dirty/untracked scope. This is qualitative evidence, not a controlled benchmark proving superiority over Superpowers.
- The legacy reliability catalog validator remains incompatible with the current native-member catalog; not counted as success. The tracked-source package validator passed. Initial whole-directory validation was contaminated by pre-existing untracked build/cache files; isolated tracked-source validation replaced it.
- Existing unrelated untracked files are preserved. Setup backups are retained under ~/.ai-rules/backups. Profile now selects all five installed hosts for workflow/focus/search-first.
- Main release manifest points to reviewed member bytes for bundled source setup. Existing downloaded frozen executables were not rebuilt or republished.

## NEXT ACTION

None — task complete.
