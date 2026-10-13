# Search First integration

Status: DONE
Plan depth: STANDARD

## Executive Snapshot
Adapt ECC Search First as an independent first-party distribution and a conditional
Andino specialist. Reuse the installer dependency resolver, host invocation and
release packaging. Preserve the original checkout's user-modified README.

## Objective and acceptance
Dedicated search-first branch with MIT provenance; independent setup; Andino
requires Focus and Search First without unconditional research. Verify latest and
pinned installation, all five host layouts, updates, idempotence and preservation.
Evaluate A-J behavioral scenarios separately from structural checks and record
actual loading/actions or explicit limitations.

## CURRENT STATE
Main base 201134d; workflow base f47eac4; Focus 9eb6081. Remote heads matched local
tracking refs on 2026-10-13. No pre-existing search-first branch. Main work is in
C:/Users/Lenovo/.codex/worktrees/search-first-integration/AI-RULES.

## CURRENT PHASE
Complete — implementation and verification finished locally.

## Execution Board
| Phase | Status | Result / evidence |
| --- | --- | --- |
| P1 Research and contract | DONE | Complete upstream source read; license exact-match checked at b92f181b3b748d1abbc2afd94af6aa7d8c8fca29; resolver tests failed for missing capability/dependency before implementation. |
| P2 Runtime and setup integration | DONE | search-first b5596b4d47f498adeef24b689f0d44a153cf4f0d; andino-workflow 59529af060a516ac197ff17481e3a8f7134c4ba8; immutable manifest pins; catalog/profiles/docs/CI updated. |
| P3 Verification | DONE | 147 tests passed; structural validators passed; ten current-runtime Claude actor records reviewed against A-J with 10/10 scenario-contract passes. |

## Decisions
- EXTEND existing installer and routing contracts; no new resolver or orchestrator.
- Focus remains independent; Search First owns research only. Local reuse may end
  research without external calls. Unknown bugs retain systematic-debugging.
- Local runtime commits are necessary to supply the explicitly requested real
  distribution branch and immutable release pins. No remote publication inferred.
- Native invocation controls win. No automatic researcher subagent fan-out; ECC's
  deeper research can be performed inline within Andino's existing lifecycle.
- Existing profiles use dependency expansion; expose supporting skill in profile
  descriptions/selection consistently with Focus.

## EVIDENCE
- https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md
- https://github.com/affaan-m/ECC/blob/main/LICENSE (2026 Affaan Mustafa, MIT).
- Existing FocusSelectionTests/FocusSetupTests and generic release bundle exporter.
- Activated installed Andino/Focus and test-driven-development; no Search First
  activation claimed from source inspection.

## NEXT ACTION
Review the local diff and, if publication is desired, obtain explicit authorization
before pushing the three branches. Remote installation and CI remain unverified
until those branches are published.

## Verification progress
- Targeted latest/pinned installs used actual committed runtime snapshots on all
  five adapters. Repeat setup kept file mtimes; standalone update and preservation
  of edited/unrelated/alternate-root installs passed. Embedded bundle avoided Git.
- Extended the existing evaluation runner for standalone entry and opt-in public
  read-only web research; new regression checks failed before implementation and
  passed afterwards. No new evaluation framework or production routing engine.
- Local runtime commits exist solely to provide real package pins. Remotes remain
  unchanged; remote installation of search-first is not yet claimed.
- The final full suite passed 147 tests. The complete output is preserved in
  docs/validation/search-first/unittest.log.
- Codex 0.154.0 read-only actor could not read supplied fixtures (host policy).
  Kept NOT_VERIFIED; did not relax its sandbox or repeat denied operations.
- Claude Code 2.1.294 restricted native reads work, but implicit project-skill
  discovery returned Unknown skill. Official CLI documentation supports explicit
  session plugin registration. A bounded smoke test confirmed native Skill loading
  with --plugin-dir while retaining restricted mode and read-only tool allowlist.
- Extended the existing evaluator, not runtime distribution, with that temporary
  namespace. Standalone and Andino actors now show successful actual Skill calls,
  local reads and (Andino) public metadata/docs retrieval. Review is in progress.
- Initial ten-case review found 5 scoped passes and 5 failures: D/E omitted the
  method, G treated offline research as NOT_NEEDED, H used file reads instead of
  native Skill, and F loaded debugging after artifact reads. All initial traces
  and reasons are preserved under prior-9ab45df, not replaced by later successes.
- Changed only Andino's research route and native-loading clarification. The
  previous version-docs boundary said no mandatory extra skill, conflicting with
  unfamiliar-solution routing. Current route requires Search First when an open
  research need remains, including offline work; settled local reuse still skips.
- Final structural validation passed for five skill packages, 44 capability
  schemas, 57 contracts, and all ten Search First evaluation records at the pinned
  Andino runtime hash. Skripsi traceability also passed unchanged.

## Delivery verification (2026-10-13)

- Reviewed the concurrent Focus communication-reference task before delivery.
  Its detached runtime and validation worktrees remain untouched and uncommitted.
- Three overlapping main files were identified: the skill validation workflow,
  `scripts/validate_skills.py`, and `tests/installer/test_focus.py`. Search First
  changes remain isolated so the Focus delivery can reconcile them after its
  bundled immutable references are separately authorized for publication.
- The final repository-source test run used `src` first on `sys.path`: 147 tests,
  104.912 seconds, OK. A preceding plain interpreter run loaded the globally
  installed older package and failed because its catalog predates Search First;
  that environment mismatch did not cause source changes.
- Staged diff checking and targeted secret-pattern inspection passed. The test log
  was normalized from UTF-16 to UTF-8; prior behavioral traces remain as useful
  audit evidence.
