# Three.js family integration

Status: DONE (authorized local implementation; remote publication remains a separate authorized action)
Depth: STANDARD
CURRENT PHASE: Verification (DONE)

## Executive Snapshot / CURRENT STATE

Local implementation is verified on main, threejs-skills and andino-workflow.
Runtime a41a0a1 and Andino 06aca9e are committed; main commit follows final review.
All 714 source files remain unchanged. 45 members + family index install as 46
standalone packages; the threejs profile installs 49 targets. Actual CLI and Windows
executable smoke pass, including Git-free bundled install in isolated scopes.
Codex live discovery finds all 46; one shader and one unrelated HTML scenario were
observed. Other host behavior, remaining review-only scenarios, rendering and
remote publication remain NOT_VERIFIED. See docs/threejs/README.md and evidence.json.


## Objective

Deliver a runtime family on threejs-skills, selective routing on andino-workflow,
and backward-compatible individual/subpath installation plus threejs profile on main.

## Acceptance Criteria

- Inventory every source skill and supporting file; record provenance gaps.
- Preserve standalone packages and domain methods; Andino owns lifecycle.
- Latest and bundled sources install subpackages safely through existing transactions.
- Cover dependency closure, path safety, binary resources, updates and conflicts.
- Validate runtime, routing, release staging and existing regression suite.
- Distinguish structural tests, host discovery and observed behavioral use.

## Execution Board

| Phase | Status | Result / Evidence |
| --- | --- | --- |
| Audit | DONE | 45 skills / 714 original files inventoried with SHA256; provenance gaps retained |
| Runtime | DONE | Isolated orphan branch; 46 standalone packages pass validator; original source unchanged |
| Installer | DONE | Subpaths, transitives, binary export, conflict protection, legacy fingerprints; 192 total tests, 191 pass and 1 optional skip |
| Routing | DONE | 06aca9e committed; registry and invocation validated; Codex positive and negative smoke observed |
| Verification | DONE | 52 bundles staged; executable installs 49 targets with no Git, project/global and repeated NO_OP; package/source hashes validated |

## DECISIONS

- EXTEND existing source/export mechanisms; no new dependency or router.
- Reuse one plan; no subagents needed.
- Specialist dependencies remain optional unless technically required.
- Do not advance stable release revisions silently to unpublished commits.

## EVIDENCE

- LatestSources already fetches selections in one fetch per repository.
- `git ls-tree -rz` includes the recursive `-r` flag: no recursion defect established.
- Resolver expands only one dependency level: transitive closure needs a regression.
- Validator currently decodes every resource as UTF-8; source has binary assets.
- Game Director owns a competing progress file and suggests delegation/all-phase loading;
  adapt its lifecycle boundaries while preserving its game-production methods.

## NEXT ACTION

Review docs/threejs/README.md and the inventory's source-rights gaps, then authorize
publication separately. Publish threejs-skills, andino-workflow, main, then the
installer release in that order; verify remote SHAs before clearing local-only
manifest markers. No push, merge, PR, tag or publication is authorized or performed.

## Progress / decisions

- Runtime worktree: C:/Users/Lenovo/.codex/worktrees/threejs-runtime/AI-RULES.
- Andino worktree: C:/Users/Lenovo/.codex/worktrees/threejs-andino/AI-RULES,
  local branch fast-forwarded with fetch from already fetched origin ref (no merge).
- Entry index installs from entrypoint/ to avoid nested specialist discovery.
- Preserve original examples; copy five cross-package reference targets with local
  imports into standalone consumers. Metadata quoted descriptions normalized to
  supported plain scalars, no technical methods removed.
- Existing validator: 33 tests pass; Three.js package validation: 46 packages pass.
- First full suite: 179 tests, 3 failures, 1 skipped. Two assertions assumed target
  order and the Everything fixture lacked the unpublished family branch; repaired
  fixtures/assertions, not production behavior. Re-run required.
- New integration test reproduced bundled update overwriting personal additions;
  record file fingerprints for bundled installs and block modified update/remove.
- No potential credential signatures detected by bounded full-text scan. This is
  not an exhaustive security audit. Missing blanket rights and two supplied GPL
  notices must remain explicit before publication.

- Real-package smoke found and reproduced Windows git archive CRLF conversion for code resources; export now disables conversion per command (global config unchanged).
- Real-package state serialization rejected a harmless filename containing credentials; fingerprint records now use path/blob lists and read older dict records. Secret-field rejection was not weakened.
- CLI Codex 0.154.0 smoke failed before model execution: configured gpt-6.1-sol is unsupported for its ChatGPT-account transport (400). No activation/use claim. Investigating a model-free skills/list discovery surface.
- Local actual collection setup now exits 0 for latest and bundled; 49 targets verified and repeated setup NO_OP.

- Final automated suite: 192 total, 191 passed, 1 optional Search First candidate
  fixture skipped. Existing family validation and Skripsi traceability pass.
- Codex app-server skills/list: 46 enabled family packages, zero family errors.
  Fresh actor loaded threejs-shaders and returned a smooth one-second GLSL pulse;
  fresh unrelated HTML correction loaded no Three.js/NixieFX specialist.
  Model override used the default returned by live model/list for this test process
  only after the configured alias was rejected; no global model/config changes.
- Windows PyInstaller executable built (98,933,164 bytes); both project and fake-home
  global bundled setup verified 49 targets with Git absent from PATH; repeats NO_OP.
- Runtime and Andino worktrees clean and retained. Main commit is the final delivery
  commit. Original untracked source remains outside main's index.

- Final review added a regression and guard for legacy bundled records without fingerprints: never infer unmodified content from ownership alone. Final suite/build rerun follows this change.

- Final legacy-guard suite: 192 total, 191 passed, one optional fixture skipped. Authoring helper reproduces all committed runtime resource hashes from the untouched original collection.

- Final executable after legacy guard: SHA256 1cd3aa2264d50ef1d136a9e89614c74871efb695f19a9145af7e53d79af0cf21. Fresh project/global installs each 49 VERIFIED targets without Git; repeats NO_OP. Main original source remains untracked and unchanged.
