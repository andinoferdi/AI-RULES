# RESCUE-004 - Managed multi-skill distribution

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 3 - Verification and handoff
Last Updated: 2026-09-19

## Executive Snapshot

Phase 4 implemented: generic explicit two-skill sync, compatible Andino-only wrapper,
seven additional deterministic tests and adapter documentation. All 17 tests PASS
using temporary homes; full validator retains six legacy broken links. Ready for PM
review. No live installation, host policy change or Phase 5 work performed.

## Objective

Distribute the explicit andino-workflow and ai-codebase-rescue canonical trees with
shared mechanics, preserved ownership/drift behavior and backward compatibility.

## Acceptance Criteria

- [x] Inspect source, consumers, host roots and marker/backup semantics.
- [x] Preserve Andino CLI/API behavior through delegation.
- [x] Prove both complete trees, check, source drift, update/backup, unmanaged/local
  refusal, idempotence and single-skill isolation in temporary homes.
- [x] Preserve Phase 1-3 artifacts and report legacy validator failures honestly.
- [x] Stop for PM review before Phase 5 and any live install.

## Baseline and Compatibility Contract

- Branch ai-codebase-rescue; prior Phase 3 modifications remain in routing.md and
  routing-scenarios.md, with completed RESCUE-003 untracked. Preserve these changes.
- Existing consumers: README/adapters instructions and historical plans use CLI;
  validate.py imports sync, hashes, SOURCE and DESTINATIONS and overrides SOURCE
  for isolated fixtures. harden-runtime documents running after sync, no sync import.
- CLI: no positional args; --home defaults to Path.home(), resolved before sync;
  --check checks only. Success exit 0, missing/drift raises RuntimeError (CLI nonzero).
- Four roots: .agents/skills, .claude/skills, .config/opencode/skills,
  .gemini/config/skills. Wrapper appends andino-workflow only.
- Full tree copy; .andino-generated.json has source string and relative-path SHA256
  files map; hashes exclude files named .andino-generated.json.
- Equal content prints OK and does not modify anything, even without a marker.
  Different content in check mode raises Drift; absent destination raises Missing.
  Different content in sync requires marker.files equal to current hashes, otherwise
  refuse unmanaged/local edits. Marker does not cryptographically authenticate ownership.
- Stage full source then replace. Previous tree backed up at selected home's
  .andino/backups/sync/previous-*/andino-workflow. No host config is copied.
- Sequential processing, not an all-host transaction: earlier destinations may
  finish before a later refusal. Retain and document this behavior.
- Extraction is compatible; no additional consumers requiring a product decision.

## Scope / Decisions

New scripts/sync-skills.py, wrapper scripts/sync-workflow.py, deterministic tests
in scripts/validate.py and clean adapters/README.md. Explicit allowlist only; no
folder discovery. Generic backup leaf uses skill name; legacy leaf unchanged.
Preserve SOURCE/DESTINATIONS/hashes/sync wrapper API for current consumers.
No methodology, lifecycle, host policy, credential/config, live install, commit,
push, PR or deployment changes. Six legacy links remain out of scope.

## Execution Board

| Phase | Status | Evidence |
| --- | --- | --- |
| Phase 1 - Contract inspection | DONE | Current implementation and callers read; contract above. |
| Phase 2 - Extract and test | DONE | Shared mechanics, allowlist, wrapper and seven new tests. |
| Phase 3 - Verification and handoff | DONE | 17 tests PASS; six legacy links still fail. |

## Phase 1 - Contract inspection

Status: DONE

### Result / Evidence

Existing metadata supports a second skill without migration: marker source/files
are already tree-specific. All four hosts use the same copy mechanics.

## Phase 2 - Extract and test

Status: DONE

### Result / Evidence

- [Generic sync](../../../scripts/sync-skills.py) owns shared hashes/copy/drift and
  explicit managed names. --skill is repeatable; default selects only the two names.
- [Legacy wrapper](../../../scripts/sync-workflow.py) retains CLI, SOURCE override,
  DESTINATIONS, hashes and sync(home, check=False); delegates shared mechanics.
- [Tests](../../../scripts/validate.py) add ManagedSkills and register it in the
  existing entrypoint without weakening Markdown link checks.
- [Adapter documentation](../../../adapters/README.md) explains selection, check,
  ownership, backup and sequential partial-progress semantics. README unchanged.
- Defensive checks reject missing canonical SKILL.md and resolved destinations
  outside the selected home before copying. Valid existing installations retain
  their format and behavior; no migration is required.

## Phase 3 - Verification and handoff

Status: DONE

### Result / Evidence

`python -B -X utf8 -m unittest discover -s scripts -p validate.py -v`:
17 tests PASS in 2.595s (10 existing + 7 new). All mutation fixtures and CLI
subprocesses explicitly target TemporaryDirectory homes, not actual user homes.

| New test | Evidence |
| --- | --- |
| complete_trees_metadata_links_and_idempotence | Both trees on four hosts; matching bytes/hashes, references, marker source/files, unchanged file mtimes after check/repeat. |
| source_drift_update_backup_and_skill_isolation | Source change fails check; rescue update backs up four prior trees within temp home; Andino bytes unchanged. |
| refuses_unmanaged_and_local_drift_for_each_skill | Both skills reject different unmanaged content and edited generated content; local bytes retained, no backup on refusal. |
| identical_unmanaged_tree_is_not_adopted_or_overwritten | Legacy equal-content exception stays a no-op, without marker adoption. |
| explicit_selection_and_missing_source_do_not_write | Unknown/empty/traversal selections and missing sources rejected without creating home. |
| legacy_cli_and_generic_cli_check_exit_and_selection | Legacy only installs Andino; missing/drift check exits nonzero; rescue selection and both-skill check succeed. |
| legacy_marker_update_and_backup_with_source_override | Manually seeded old-format markers update through wrapper; historical backup leaf remains andino-workflow even with overridden SOURCE. |

`git diff --check` passes. Full `python -B -X utf8 scripts/validate.py` still exits
1 before tests with the same six legacy links: AGENTS.md ->
put-in-your-projects/Agents.md; prompt-awal.md -> put-in-your-projects/1. First-prompt.md;
README.md -> those two missing paths; put-in-your-projects/ai-rules/2.
Send-to-every-prompt.md -> task.md and brd.md. No new broken link was reported.

## Limits / DEVELOPER HANDOFF

This proves deterministic distribution in isolated homes, not live host discovery
or implicit model selection (UNVERIFIED). Existing sequential/non-transactional
replacement and content-based marker trust remain unchanged; failures can leave
earlier hosts updated, as documented. No credential/provider configs copied.

Phase 4 changes only generic sync, legacy wrapper, validator tests, adapter docs
and this new ticket. Prior Phase 3 dirty files/checkpoint were preserved. No rescue
methodology, lifecycle, generated/live install, host policy, commit or remote change.

## NEXT ACTION

PM: review sync-skills.py, sync-workflow.py, ManagedSkills tests, adapter docs and
the compatibility evidence above. Return GO or REVISE before Phase 5; do not run
either sync entrypoint against a live home from this completed ticket.

