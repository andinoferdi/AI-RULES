# DEVELOPER HANDOFF

Historical pre-publication review checkpoint. The current delivery status, published commit, installer proof and subsequent validation are in [publication review](publication-review.md) and [current-runtime review](current-runtime-review.md). Statements below about uncommitted work, unchanged release pins and absent publication describe that earlier checkpoint.

Objective: implement ULTIMATE PROMPT's capability integration layer, retaining the accepted adaptive core and one Andino lifecycle owner.

Status: implementation and structural validation verified; historical live coverage partial. Overall acceptance remains open where invocation/host coverage is NOT_VERIFIED.

Current runtime SHA256: `dc9916a964011c8c7d16c977f614616db949e0643d5b0efa0aa3b47edb7f8447` (55 contracts).
Evaluated runtime SHA256: `75607e6fa1b4bf0b227ad677c5e42219cc62d8d3e68970fdb4dec9107ac2a8c7` (53 contracts).
The final change adds idea-refine/interview-me only: all original 53 complete contracts and every other runtime file compare unchanged. [Revision lineage](capability-runtime-lineage.json) preserves this distinction; historical record audit requires explicit `--allow-historical` and never treats those records as latest-runtime PASS.

## 1. Exact files changed

Runtime is in the attached worktree `C:/Users/Lenovo/.codex/worktrees/andino-capability-integration/AI-RULES`, detached at baseline `0f41b684eac5b990de48e6f54727f7031943f8b7`:

- `SKILL.md`: additive capability-discovery/use principles only.
- `README.md`: registry and host-dependent selective use explanation.
- `references/routing.md`: evidence-driven selection, states, policies and explicit MCP routes.
- New `references/capability-registry.md`: all explicit per-capability contracts.
- New `references/capability-coexistence.md`: provider/collision/overlap decisions.
- New `references/invocation-adapter.md`: actual native host discovery/invocation and observable evidence contract.

`references/ui-coexistence.md` is unchanged. Adaptive core before the new paragraph compares exactly with the baseline. No runtime executable, dependency or second meta-router was added.

Quality plane is `C:/Users/Lenovo/Downloads/AI-RULES`, branch `main`, baseline `1ebc45366975dfab0f873c11c11ede09641b7164`:

- `.github/workflows/validate-skills.yml`: deterministic capability eval-schema step.
- `README.md`, `evals/README.md`: integration/evaluation/coverage documentation.
- `evals/andino-workflow.json`: original 28 objects intact; 32 capability cases appended.
- `scripts/validate_andino_capabilities.py`: contract/case/record checks and exact content hash.
- `scripts/run_andino_capability_eval.py`: isolated oracle-hidden live actor runner.
- `scripts/run_andino_capability_suite.py`: sequential/resumable live runner; stops deterministic setup failures.
- `scripts/audit_andino_capability_live.py`: saved evidence consistency/coverage, no automatic behavioral grading.
- `tests/test_andino_capabilities.py`: nine targeted failure/contract/evidence/CSV hash/lineage/fixture tests.
- `docs/exec-plans/active/andino-capability-integration.md`: current execution state.
- `docs/validation/andino-workflow/integration-review.md`: historical checkpoint points to this revision.
- This handoff, `capability-traceability.json`, `capability-runtime-lineage.json`, `live/*.json`, `smoke/*.json`: requirement ownership, revision scope and actual observed records.

Ignored authoring helpers under `.ai-rules/` are not runtime/distribution files. They do not modify global installed skills. The frozen release pin remains unchanged because this is an uncommitted patch, not a published runtime commit.

## 2. Registry structure

One on-demand Markdown registry has an index and one heading per capability: 10 Superpowers, 24 Agent Skills, 12 other individual skill routes, 8 MCPs and 1 native entry, totaling 55. Each entry has Type, Family/provider, Aliases, Primary purpose, Trigger, Preferred when, Avoid when, Availability check, Invocation method, First-call/preflight, Fallback, Coexistence/conflicts, Mutation/permission boundary, Verification requirement and Activation policy.

Types distinguish skill methodology, MCP instruments and native host facilities. State distinguishes DISCOVERED, AVAILABLE, INVOKABLE, ACTIVE, USED, UNAVAILABLE and NOT_NEEDED. Activation policies are AUTO, CONDITIONAL_AUTO and PERMISSION_GATED. Those are selection/action rules, not a universal host API or automatic dependency installation.

## 3. Complete requested mapping

| Family | Exact registered routes |
| --- | --- |
| Superpowers | systematic-debugging; test-driven-development; verification-before-completion; brainstorming; writing-plans; requesting-code-review; receiving-code-review; dispatching-parallel-agents; using-git-worktrees; finishing-a-development-branch |
| Ponytail | ponytail, conditional actual complexity risk |
| Claude-Mem | claude-mem with actual mem-search/search/timeline/detail discovery |
| UI/UX Pro Max | ui-ux-pro-max |
| Taste | design-taste-frontend, taste-skill alias only when host exposes it |
| AI Website Cloner | clone-website, fidelity only unless redesign requested |
| Graphify | graphify skill; actual version's CLI/MCP query/callers/impact/path/trace schema, no invented tool names |
| Anti-Slop | antislop; antislop-ui; antislop-copywriting; antislop-human; antislop-layoutmobile; antislop-code |
| Agent Skills: requested minimum | api-and-interface-design; browser-testing-with-devtools; ci-cd-and-automation; code-review-and-quality; code-simplification; constraint-driven-development; context-engineering; debugging-and-error-recovery; deprecation-and-migration; documentation-and-adrs; doubt-driven-development; frontend-ui-engineering; git-workflow-and-versioning; incremental-implementation; observability-and-instrumentation; performance-optimization; planning-and-task-breakdown; security-and-hardening; shipping-and-launch; source-driven-development; spec-driven-development; agent-skills-test-driven-development (provider-qualified test-driven-development alias) |
| Agent Skills: installed extras found | idea-refine; interview-me. Installed using-agent-skills is explicitly excluded as competing router. |
| MCP instruments | context7; playwright-mcp; chrome-devtools; git-mcp; drawio-mcp; staruml-mcp; premiere-pro-mcp; cheatengine-mcp |
| Existing facilities | native-capabilities (filesystem/search/shell/Git/browser/tests) |

The installed Agent Skills source catalog has 25 directories: 24 individual skills including the two extras above, plus the excluded meta-router. The installer still manages only its three first-party skill distributions; this registry does not convert third-party recommendations into installer entries.

## 4. Provider collision and coexistence

Explicit user/project provider wins. Otherwise inspect actual provider/path, resolve equivalent copies by project scope/host authoritative root, then use documented defaults: Superpowers for overlapping named disciplines including TDD; Agent Skills for its named categories. Agent Skills renamed TDD remains an alias for its provider, not the Superpowers implementation. Use one identifiable permitted equivalent if preferred provider unavailable; unresolved provider is UNKNOWN, never invented. Do not rely silently on last-loaded or directory order.

Ponytail handles prospective over-build risk; code-simplification handles existing-code refactoring. Anti-Slop is a selected quality concern, subordinate to accepted user direction/function/accessibility. UI/Taste retains the exact existing coexistence policy and explicit single-skill choices. Native simple references precede Graphify; native sufficient Git precedes MCP. Playwright reproduces a flow; DevTools can answer a distinct diagnostic question. Draw.io serves general editable diagrams; StarUML formal models. None creates another plan, full-family pipeline or delegated-agent default.

## 5. Trigger, boundary and fallback for every capability

The runtime registry contains the exact per-entry contracts. [The traceability inventory](capability-traceability.json) carries a complete ID/provider/alias/trigger/boundary/fallback mapping and per-capability evidence status so the reviewer need not infer coverage from prose.

Notable operational contracts: inspect dependency versions before Context7; resolve actual tool names; one default browser surface; Git reads first; editable artifact read-back rather than editor-opening claims; Premiere connection then project/sequence inspection then deferred schema/tool discovery, focused authorized mutation and read-back; Cheat Engine connectivity and target evidence before bounded reads, with no implied write/injection/process/shell authority.

When unavailable, use a safe sufficient local alternative and label it, or preserve the exact material gap/minimum missing access. Do not claim the unavailable worker/tool was used. Readiness-only Premiere test used `launchIfNeeded:false`; no app launch or timeline edit was requested/performed.

## 6. Eval cases added/changed

All 28 prior eval objects are preserved. Added 32 exact requested IDs, from `debugging-superpowers-route` through `simple-task-zero-capability`. The new case schema has raw fixture setup and evaluator-only capability IDs; prompt construction excludes expected, forbidden and those capability IDs. Actual metadata/catalog facts do not create tools or permission in the actor.

The optional runner copies real installed skill resources, creates bounded raw fixtures and executes an authenticated ephemeral read-only Codex CLI context. It captures actual commands/results and runtime/catalog hashes. It does not fabricate skill stubs or mock MCP invocations. Model identity is UNKNOWN because observed CLI events did not expose it. No model override was made.

## 7. Actual validation commands/results

| Check actually executed | Result |
| --- | --- |
| `python scripts/validate_andino_capabilities.py --runtime <edited-runtime>` | PASS for the inspected registry and all 32 new schemas; exact SHA256 printed. |
| `python scripts/validate_andino_capabilities.py --cases-only` | PASS; also wired into CI without model execution. |
| `python -m unittest discover -s tests -p test_andino_capabilities.py` | Nine tests PASS. Initial missing-module failure was observed before implementing the checker. CSV hash regression added after actual runner error. |
| `python -m unittest discover -s tests` | Final complete run: 117 tests PASS, 42.807 seconds. |
| `python scripts/validate_skills.py` | PASS: 3 existing published skill packages, metadata/links and all 3 eval schemas. Separate directory check validates the uncommitted edited Andino runtime. |
| `python scripts/validate_skripsi_traceability.py` | PASS: 335 requirement/acceptance owners, 32 capabilities, 110 initial eval owners, 75 task records. |
| `python scripts/audit_skripsi_live.py` | Existing evidence consistency: 58 PASS, 0 FAIL, 60 NOT_VERIFIED; no new Skripsi actor run. |
| Compare previous Andino JSON objects | PASS: all original 28 unchanged. |
| Compare runtime core and UI coexistence | PASS: core identical after removing requested additive paragraph; UI coexistence exact baseline match. |
| `git diff --check` in both checkouts | PASS. |
| `python scripts/audit_andino_capability_live.py --runtime <edited-runtime> --allow-historical` | PASS record consistency: 32 records, 9 PASS / 23 NOT_VERIFIED, no missing case IDs; all explicitly tied to evaluated 53-contract hash. |
| Capability validator with `--records <live-or-smoke-folder> --allow-historical` | Checks record structure and known lineage; historical evidence is explicitly counted separately. |
| Python compilation of the four new quality scripts and final main-document link check | PASS. |

Test scope is explicit: schema, contract and record consistency are not live behavioral PASS. Unit tests do not prove service readiness. No unchanged broad suite is repeated solely for documentation edits.

## 8. Live invocation tests actually run

The oracle-hidden CLI suite attempted all 32 requested scenarios sequentially: 31 actor completions and one UI/UX timeout. Explicit review produced 9 PASS / 23 NOT_VERIFIED, no FAIL verdict inferred from a missing instrument or blocked setup. PASS IDs: debugging-superpowers-route, agent-skills-no-double-router, ponytail-needed, ponytail-not-needed, ui-taste-coexistence, clone-fidelity, diagram-tool-choice, premiere-howto-no-mutation and simple-task-zero-capability.

Its records retain actual selection/load actions, output, failures/timeouts and reviewer verdict. A normal runner exit initially records NOT_VERIFIED; explicit review is required before assigning PASS/FAIL. A successful selected-skill load plus applied reasoning proves selection/loading for that case, while feature implementation, browser outcome or external operation remains unverified if not performed. Six individual skills have actual observed revision-scoped use: systematic-debugging, code-review-and-quality, ponytail, design-taste-frontend, ui-ux-pro-max and clone-website. This is not whole-family coverage or latest-55-contract/cross-host PASS.

Separately, nine actual Codex desktop read/preflight smoke calls were executed. Five succeeded: Context7 resolve-library lookup (followed by actual documentation query), Git status read, Draw.io disposable page-list read, Playwright blank-tab list, and DevTools blank-page list. Four did not supply usable service evidence: Claude-Mem search timeout, StarUML service unavailable, Premiere readiness false, Cheat Engine pipe unreachable. These are `scope: smoke`; none proves an independent actor autonomously selected the instrument.

## 9. PASS / FAIL / NOT_VERIFIED per capability

See every registered ID in [capability-traceability.json](capability-traceability.json). Policy/schema coverage, revision-scoped behavioral use and service smoke are separate columns. Never infer a whole-family PASS from one successful individual skill. Negative selection cases prove only the absence of unnecessary use in that actor/context. Latest-runtime and cross-host coverage require their actual own evidence.

## 10. Unavailable host integrations

- The isolated CLI adapter exposes no MCP servers. Positive instrument routing/application cases remain NOT_VERIFIED there even though desktop tool discovery succeeds.
- Some isolated CLI contexts rejected local file reads under native host policy; one UI/UX evaluation timed out. No permission bypass was used.
- Graphify MCP is not exposed in this desktop session; installed Graphify skill/CLI is not a connected graph service. No new graph was generated.
- Claude-Mem retrieval timed out after 45000ms; observer separately reports `Failed to parse JSON`. No worker restart/config/credential change was made.
- StarUML `localhost:58321` inspection failed. Cheat Engine bridge pipe not reachable.
- Premiere preflight returned `premiere_not_running`, `retry:false`, `userActionRequired:true`. Its requested next step was communicated verbatim and no further Premiere call was made: “Adobe Premiere Pro is installed but could not be launched from this environment. Open Premiere yourself. The MCP Bridge panel auto-starts. Then run verify_premiere_connection once.”
- Claude Code, Antigravity and OpenCode live behavior/parity have not been executed. Registry contracts respect their native controls without claiming invocation.

## 11. Decisions and deviations

Use a Markdown host contract instead of a runtime executable adapter because this distribution is a portable instruction package and permits Markdown runtime resources. Real invocation remains the host's native interface; optional Python scripts are quality-plane evaluation tooling only.

Installed aliases/provider differences are explicit, including Agent Skills TDD rename. Upstream Ponytail broad coding/persistence defaults and Graphify broad scan defaults yield to the accepted user/project current-need boundaries. The actual installed Agent Skills catalog, rather than the minimum list alone, prompted the two additional individual routes.

An initial external-resource hashing bug applied Andino's Markdown-only package restriction to UI/UX CSV resources. It was fixed with separate byte-based skill-resource hashing and a meaningful regression test. Four previously executed records were preserved. Failed setup repetitions were not counted as live invocations; suite now stops deterministic setup failures. No acceptance is weakened to hide missing evidence.

Review also identified fixture inadequacies: initial native-Git case did not materialize a Git repository, memory-proposal case omitted its file, and rerouting reused the database log rather than a library error. Those records remain NOT_VERIFIED. The adapter now creates a disposable no-commit Git/index fixture, a proposal file and a distinct API-error log, and saves exact actor input for future reproduction. The fixture correction is tested locally; its revised live scenarios were not claimed as rerun. Permission denials were not retried unchanged. Latest added metadata does not justify pretending earlier denied reads succeeded.

## 12. Diff summary / stop conditions

Runtime: three existing files updated and three new references. Quality plane: 32 specs appended, targeted validators/live tooling/tests, portable plan/evidence/handoff. No unrelated installer/catalog/profile behavior or accepted core was rewritten. No global installed skill was replaced, no package dependency installed, no commit/push/merge/publish occurred, and no user application project/process memory was mutated. Requested implementation exists as reviewable local changes; a release pin cannot refer to an unpublished uncommitted patch.

## 13. Recommended next validation / review requested

Senior PM should review integration contracts and explicit evidence gaps in one pass. Accept structure separately from full live coverage. Next consequential validation: run the positive instrument cases in an isolated host exposing the actual selected MCPs and disposable browser/diagram/application fixtures; restore unavailable bridges through their normal user/native mechanisms, then test exact preflight/read-back. Execute provider-collision/selection cases with native permitted copies and repeat on other hosts only before claiming parity. Ask for a concrete publication/global-update action only if the user chooses that next stage; PM GO is not that authorization.
