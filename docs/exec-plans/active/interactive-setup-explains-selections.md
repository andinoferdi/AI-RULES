# Interactive setup explains selections

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 3 — Verify and close
Last Updated: 2026-09-22

## Executive Snapshot

Make `ai-rules setup` explain hosts, profiles, and capabilities without changing their stable IDs or installation semantics. The existing catalog/profile membership is authoritative; user-facing descriptions will be metadata driven. Next: add a failing focused test for formatted option values and the setup summary.

## Objective

Let a non-technical user understand what an interactive setup choice means and what it will install before approving mutation.

## Acceptance Criteria

- [ ] Interactive host, profile, and capability choices show human-readable labels and explanatory descriptions while returning current stable IDs.
- [ ] Profile inclusions are derived from profile metadata, not duplicated in Python.
- [ ] Interactive setup renders a concise summary before its existing confirmation.
- [ ] Non-interactive setup and capability resolution retain their current behavior.

## Scope

In scope: interactive presentation, catalog/profile descriptive metadata, focused tests, and the summary.

Out of scope: profile membership, resolver/executor semantics, installation paths, state schemas, and installer architecture.

## Current Technical Context

`interactive.py` currently passes raw IDs to Questionary. The installed Questionary 2.1.1 supports `Choice(title, value, description)` and displays the current choice description portably. `profiles.json` defines membership and `capabilities.json` defines display names.

## File Impact Map

### Create

- `docs/exec-plans/active/interactive-setup-explains-selections.md` — durable ticket state.

### Modify

- `src/ai_rules/interactive.py` — metadata-driven option rendering and summary helper.
- `src/ai_rules/domain/models.py` — optional descriptive metadata fields.
- `src/ai_rules/profiles/data/profiles.json` — profile purposes.
- `src/ai_rules/catalog/data/capabilities.json` — capability purposes.
- `src/ai_rules/cli.py` — pass metadata and render the interactive summary.
- `tests/installer/test_interactive_setup.py` — presentation mapping and summary contracts.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Specify and test presentation contracts | DONE | Capture required visible behavior | interactive tests | Focused tests first failed for missing choice builders, then passed. |
| Phase 2 — Implement metadata-driven prompts | DONE | Render descriptions while preserving IDs | interactive, CLI, metadata | Built-in Questionary descriptions provide selected-item detail; IDs remain values. |
| Phase 3 — Verify and close | DONE | Validate behavior and regression suite | tests and manual dry-run | Full unittest suite, both project validators, and compileall passed. |

## Decisions Log

- D-001 — Use Questionary's built-in choice descriptions instead of a new TUI dependency. Reason: v2.1.1 supports the required selected-item explanation and is already cross-platform in this project. Impact: portable dynamic descriptions with no terminal framework change.
- D-002 — Keep profile membership authoritative in `profiles.json`; add only human-facing description metadata. Reason: avoids parallel capability lists and preserves resolver behavior.

## Verification Matrix

| Requirement | Verification | Status | Evidence |
| --- | --- | --- | --- |
| Stable IDs survive display formatting | focused interactive tests | PASS | 5 interactive tests passed. |
| Descriptions and profile inclusions are shown | focused interactive tests and terminal smoke | PASS | Selected Questionary descriptions and Recommended summary observed. |
| No regression | `python -m unittest discover -s tests` | PASS | 94 tests passed. |
| Package syntax valid | `python -m compileall -q src` | PASS | Exit 0. |

## Progress Log

- 2026-09-22 — Inspected current prompt flow and Questionary API; confirmed built-in selected-choice descriptions.
- 2026-09-22 — Added metadata-derived choices and a pre-plan interactive summary. Manual PowerShell dry-run verified host/profile descriptions and Recommended summary; used ASCII separator in the summary for Windows console code-page readability.
- 2026-09-22 — Final verification: 94 unit tests, both project validators, and `compileall` completed with exit code 0. `git diff --check` was clean.

## NEXT ACTION

None — ticket complete.
