# Andino capability integration

Status: DONE — authorized branch delivery, 2026-10-18; implementation verified and live-host limits retained
Owner: Andino Workflow / active Codex host
Date: 2026-10-02
Density: STANDARD

## Executive snapshot

CURRENT STATE (2026-10-18): Runtime checkout C:/Users/Lenovo/Downloads/AI-RULES on existing andino-workflow at f531269775aafa8b162b4ec65dd919b37a208ffe. Existing main branch 80f54467188a76ad95af3943221fd2a4b59d2181 is isolated at C:/Users/Lenovo/Downloads/AI-RULES-main. Runtime tracked files initially clean; user untracked prompts, upstream checkouts, build/, scripts/, src/, tests/ and threejs-skills/ preserved. No new branch, stash, staging or publication authorized.
CURRENT PHASE: G — authorized branch delivery; runtime published and MAIN release pin/setup/regressions verified. This checkpoint travels with the MAIN delivery commit.
EVIDENCE: docs/validation/andino-unified/README.md and verification.json reconcile current acceptance. Final candidate SHA256 628e3d35c153e463924dbb17212523568e9b759e4d6fd3367a30dad70d6424cd: 65/65 eligible rows mapped, 57 procedures PASS, 114/114 oracle-hidden v3 selections PASS, 41 installer scenarios PASS, full unittest 223 run/zero failures/one unchanged opt-in skip, 28 focused gates PASS, sibling/packaging/source checks and both diff checks PASS. Parent independently checked fixture outcomes and closed independent review findings. Native Claude v2 scoped PASS; final v3 blocked by weekly account limit, explicitly NOT VERIFIED. OpenCode/Antigravity live surfaces remain NOT VERIFIED with smoke procedures. Refs/prompts/upstream snapshots and protected UI/Three.js/plan/handoff contracts preserved.
NEXT ACTION: No implementation work remains. Confirm remote MAIN equals the delivery commit when executing its authorized normal push. Remaining live-host smoke stays explicitly NOT VERIFIED; resume Claude after its normal weekly reset or use a controlled authorized adapter for the other hosts. No new branch/tag/global installation is authorized.

### Unified integration execution board (current authority)

| Phase | Status | Evidence / exit |
| --- | --- | --- |
| A — Baseline and inventory | DONE | 195 baseline tests PASS, one opt-in skip; package/Focus/Three.js validators PASS; 217 Addy + 190 Matt + 238 Superpowers files byte-inventoried; 78 actual skills plus one archived doc; clean snapshots. |
| B — Canonical model | DONE | coverage.json derives 79 rows, 57 guide destinations plus root; ownership.json has 19 resolved concerns; canonical-decisions.md records comparative TDD, all-source requirements/debug/review and legal rulings. Source set/hash reconciliation and nine corruption/ownership gate tests PASS. |
| C — Internal methods | DONE | Parent independently reran all three procedural checkers: 18 Addy +28 Matt +11 canonical scenarios PASS. Addy includes 18 adversarial +18 killed mutations; canonical checks correct-reason RED/GREEN, planted review defect and policy failures. 126 runtime Markdown files initially link/metadata clean; 57 unique guides. Essential method assets mapped; bootstrap compatibility resources integrated in D. No model-routing or optional live tool claim from these checks. |
| D — Runtime integration | DONE | Single root entry, 57-method index, 34 canonical alias contracts, host-resource loading and max-three/no-nesting policy integrated. 127 runtime Markdown files have zero metadata/link errors. 116 asset mappings include explicit bootstrap/unsupported-host exclusions. UI/Three.js/plan contracts preserved. |
| E — Packaging | DONE | 28 focused gate tests PASS. Package validator accepts only scoped Markdown guide/resources; other families unchanged. Final candidate has 127 Markdown files/one native identity. 41 offline installer scenarios PASS: five profiles + custom across five host paths, repeat NO_OP, five managed-edit blocks, five unmanaged conflict blocks, clean update/backup/repeat. Real sibling branch exports, no upstream directories supplied to installer, network source or new fixture Git history. Frozen manifest/sibling pins unchanged; release-proposal.json identifies unpublished 628e3d35… content hash. |
| F — Verification | DONE | verification.json, behavior-grade.json, parent-work-grade.json, installation.json, native-grade.json and preservation.json; all local material gates PASS, host limits explicit. Original v1/v2 failures retained. Independent final-resolution.json closes all five MAIN findings; parent corrected runtime alias/branch/ordering/phase findings. |
| G — Handoff | DONE | Local report plus authorized branch delivery: runtime efd9c508 pushed/remote-confirmed; MAIN sequence13 pinned, real remote fresh/repeat and official upgrade/backup/repeat PASS,223 post-pin tests OK/one unchanged skip,7 source bundles staged. MAIN normal push is the final executing action of the delivery commit. No fabricated pin,new branch or tag. |

Acceptance for this continuation is ULTIMATE-PROMPT.md sections 5–12 and GRAND-PLAN.md R01–R14 / Q1–Q6. Historical publication permissions below apply only to their prior ticket; current work forbids commit/push/merge/rebase/new branches/global installation. Exactly one current plan is used. Prior verification remains revision-scoped and is not current PASS.

2026-10-18 C checkpoint: Three MIT notices and runtime provenance added. Scoped package/registry tests demonstrate expected RED failures against the old validator (valid internal guide rejected; canonical method type rejected); implementation changes wait for E dependency gate. Baseline remains revision-scoped. Available CLI inventory: Codex executable, Claude executable and OpenCode launcher; no Gemini command. This is discovery only, not authentication/readiness or live behavior proof. Source audit manifests include a resolved wait-what metadata gap; no source bytes changed.

2026-10-18 F/G checkpoint: Preserve original actor raw inputs, oracles, traces, reviews and failed intermediate tests. v1 109/114 exposed five fixture phase/authority ambiguities; five revised requests are recorded separately. v2 113/114 exposed premature API design before TDD; v3 uses those same revised raw requests and passes 114/114 after a root-only phase correction. Candidate lineage is ec364b5f… → 9973fa8c… → 628e3d35…. Initial native Claude ordering FAIL; v2 scoped PASS; v3 weekly account limit NOT VERIFIED, with no retry/bypass. Runtime review removed ticket-specific branch restrictions from generic guidance. MAIN review regression-protected Windows aliases/image links, duplicate source paths, outside-scope chmod/truncate and current metadata/checker/manifest evidence, including all six missing-input cases. No original source or sibling contract was rewritten. Current delivery is IMPLEMENTED with incomplete live-host verification, not universal parity or a published release.

2026-10-18 publication continuation: Human authorized commit and push of both existing branches. Scoped staged validation found excess EOF blank lines in 113 new runtime files; normalize only terminal newlines, preserve v3 snapshot and record exact per-file lineage. All non-EOF text is identical; 57 procedures rerun against publication bytes. Runtime efd9c508d55ed94ab2a1229e3324a008e7db71f0 normal-pushed and remote-confirmed; package hash b94423e2409edcac5616ce097aa2741c0bc3a26dfda8690563a68bb540c1d657. MAIN advances only Andino/global sequence to 13 and its actual commit pin; all six siblings unchanged. Actual remote fresh/repeat and old-official upgrade/backup/repeat PASS. Post-pin full suite223 OK/one unchanged opt-in skip;7 release source bundles export with exact published Andino hash. Five MAIN EOF-only cleanups preserve Python ASTs;28 focused tests and57 procedures rerun afterward. publication-verification.json binds current evidence. Earlier no-publication statements describe their historical authorization scope, now superseded for these two branch commits/pushes only. MAIN is committed/pushed as the final authorized execution action; its containing commit identifies the quality-plane delivery without a self-referential fake SHA.

### Historical executive snapshot (2026-10-02, retained)

CURRENT STATE: Published runtime effc3b8d7326d121317da86aff205de7c0bb0e80, 55 contracts; main preserves 28 adaptive specs plus 32 required and two supplemental specs. Six exact-current-runtime samples: 4 scoped PASS / 2 NOT_VERIFIED. Historical 32-case batch: 9 PASS / 23 NOT_VERIFIED; nine historical service smoke records: 5 PASS / 4 NOT_VERIFIED. Default remote setup upgrade, backup, SHA/hash lock and repeat NO_OP verified in disposable project. Overall live acceptance remains open.
CURRENT PHASE: delivered implementation/publication; remaining live acceptance requires adequate host fixtures.
EVIDENCE: current runtime SHA256 dc9916a964011c8c7d16c977f614616db949e0643d5b0efa0aa3b47edb7f8447; prior evaluated SHA256 75607e6fa1b4bf0b227ad677c5e42219cc62d8d3e68970fdb4dec9107ac2a8c7. Lineage proves final registry change adds only two installed Agent Skills routes; 53 previous contracts and all other files unchanged. Final full suite 117 PASS; nine targeted tests, runtime/contracts/schemas, record audit, script compilation, final document links and both diff checks PASS.

## Objective

Implement the integration-layer revision in ULTIMATE PROMPT.txt, preserving the accepted adaptive core. Andino selects minimum useful capabilities from evidence and actual need, resolves provenance, invokes through real host interfaces, reroutes and stops.

## Scope and decisions

- Runtime: attached worktree C:/Users/Lenovo/.codex/worktrees/andino-capability-integration/AI-RULES (baseline 0f41b684eac5b990de48e6f54727f7031943f8b7).
- Quality plane: main checkout C:/Users/Lenovo/Downloads/AI-RULES.
- Preserve ui-coexistence and adaptive reasoning/persistence rules; do not add another router or installer support for external dependencies.
- Initial authorization covered implementation and validation. Latest human instruction explicitly authorizes cleanup, commit and normal push. Global skill replacement and live application mutation remain outside this delivery.
- File is a transcript plus final PM handoff. Earlier AI diagnoses are claims; current repository and host evidence determine actual implementation state.
- Published runtime has both a real commit and the evaluated content hash. Stable manifest advances Andino/global sequence to 3 with siblings unchanged.
- No delegated development agents. Isolated live model evaluations are validation fixtures, not independent implementation owners.
- 2026-10-02 PM review: implementation GO, no blocking runtime revision; accepted contracts LOCKED. User now explicitly authorizes commit/push and final cleanup, and requires setup to reconcile the latest Andino safely. Publication does not imply full live or cross-host PASS.

## Acceptance criteria

1. All nine requested skill families, all 22 Agent Skills categories and eight MCP instruments have explicit trigger, boundary, discovery, invocation, fallback, permission and verification contracts.
2. Deterministic provider collision resolution; no meta-router bootstrap; preserve explicit single UI skill choices and accepted UI coexistence.
3. Installed, active and used remain distinct; seven conceptual states, three activation policies, honest unavailable fallback, evidence-driven rerouting and release.
4. At least 32 requested capability scenarios added, original 28 preserved; oracle-hidden live harness records exact runtime hash, host/model, provider, actions, evidence and verdict.
5. Structural/schema/unit validation and diff review pass. Live and cross-host results are reported separately without inferring PASS from prose, mocks or transport smoke tests.
6. Developer handoff covers the 13 requested reporting fields and maps every requirement to an artifact/evidence or an explicit limitation.

## Execution board

| Phase | Status | Result / evidence |
| --- | --- | --- |
| Inspect requirements and repository drift | DONE | Entire supplied transcript read; branch layout, installed skill IDs and actual MCP tools inspected. |
| Runtime integration | DONE | Six runtime files changed/added; 55 explicit contracts, deterministic coexistence and seven invocation states; core and ui-coexistence preserved. |
| Quality plane and feasible live validation | DONE | 32 specs, validators, isolated runner/suite, 32 reviewed actor records and nine smoke records; missing behavior explicitly NOT_VERIFIED. |
| Review and handoff | DONE | 34 requirement groups, 55 per-capability mappings, 13-field PM handoff and all feasible final checks completed. |
| Full live/cross-host acceptance | BLOCKED | Isolated adapter has no MCP exposure, native host rejects some reads, four desktop services not ready; no permission bypass or application mutation authorized. |
| User-authorized cleanup/publication and setup proof | DONE | Runtime normal push succeeded; frozen pin aligned; actual remote default setup upgraded prior official copy, backed up and repeated NO_OP. Quality-plane delivery includes portable evidence and preserves/ignores local review packet. |

## Findings

- CONFIRMED: runtime package permits Markdown references only; registry stays Markdown, no runtime executable/meta-router.
- CONFIRMED: host exposes Context7, Playwright, DevTools, Git, Draw.io, StarUML, Premiere and Cheat Engine tools. This proves discovery, not connected service readiness or behavioral routing.
- CONFIRMED: installed Agent Skills TDD is renamed agent-skills-test-driven-development; Superpowers TDD remains test-driven-development. Registry must support both identity and provider, including future same-name collisions.
- CONFIRMED: Graphify skill exists, but no Graphify MCP tool is exposed in this session. Use actual installed interface, no invented universal MCP names.
- CONFIRMED: claude-mem observer reports Failed to parse JSON; retrieval availability must be tested separately if needed.
- CONFIRMED: actual retrieval request timed out after 45000ms; no historical retrieval result is claimed. StarUML localhost service and Cheat Engine pipe unreachable. Premiere readiness false with launchIfNeeded:false; no subsequent Premiere call/mutation.
- CONFIRMED: Context7 resolved public library metadata, Git MCP read runtime status, Draw.io read disposable XML page list, browser MCPs read blank page/tab lists. These are scope:smoke, not routing proof.
- CONFIRMED: runner hashing initially reused Markdown-only runtime restriction for external CSV resources. Fixed with a separate byte-based external-resource hash; regression test proves CSV changes affect hash and remain rejected for Andino runtime. Initial four actual behavioral records preserved; deterministic failed setup attempts never counted as live invocation.
- CONFIRMED: installed Agent Skills plugin has 25 folders: 24 individual disciplines and one excluded using-agent-skills router. idea-refine/interview-me added after 53-contract evaluations. Current samples observe interview-me actual load and focused question; idea-refine reads are blocked and remain NOT_VERIFIED. Historical and current evidence are separate.
- CONFIRMED: initial native-Git/proposal/rerouting fixture inadequacies preserved as NOT_VERIFIED; adapter corrected for future execution and exact actor input capture added. No claim of rerun or repaired host permissions.

## Verification

Validate edited runtime directory, registry completeness, all eval schemas, meaningful rejection tests and full existing unit suite. Live fixtures hide expected/forbidden fields. Read-only service smoke tests do not prove autonomous routing. No global installation or dependency installation is necessary.

## NEXT ACTION

Check published repository/runtime drift, then run idea-refine and the individual Agent review route on a host permitting supplied local reads. Continue remaining instrument-routing cases only with actually exposed MCPs and disposable fixtures. See current-runtime-review.md and publication-review.md under docs/validation/andino-workflow. Do not modify accepted runtime contracts due to host limitations or infer cross-host acceptance from publication.
