# Unified Andino integration — local delivery

This report belongs to the single active [execution plan](../../exec-plans/active/andino-capability-integration.md). The user-supplied `ULTIMATE-PROMPT.md` is the execution/permission authority; `GRAND-PLAN.md` defines Phase A–G and the quality gates. Earlier delivery history is not current acceptance evidence.

## 1. Status

**IMPLEMENTED — local acceptance verified; host verification remains explicitly incomplete.** All 65 eligible source capabilities are mapped and operationally represented, the package/install/regression gates pass, and the final oracle-hidden selection run passes 114/114. No published-release or universal host claim is made.

**Publication continuation, 2026-10-18:** the user authorized commit/push of both existing branches. Runtime commit `efd9c508d55ed94ab2a1229e3324a008e7db71f0` is confirmed on remote `andino-workflow`. The runtime publication hash is `b94423e2409edcac5616ce097aa2741c0bc3a26dfda8690563a68bb540c1d657`. `publication-lineage.json` proves that all differences from the v3 candidate below are trailing EOF newlines only; non-EOF text is identical. All 57 procedures were rerun against publication bytes; original reports remain in `pre-publication/`. Branch publication and a tagged/binary installer release are separate outcomes.

The final candidate is `build/andino-unified-candidate-v3`, content SHA256 `628e3d35c153e463924dbb17212523568e9b759e4d6fd3367a30dad70d6424cd`. Hashing sorts relative paths, then hashes each path + NUL + UTF-8 Markdown with CRLF normalized to LF + NUL. This is a package identity, not a Git commit.

## 2. Branches and changes

- Runtime: existing `andino-workflow`, base `f531269775aafa8b162b4ec65dd919b37a208ffe`, checkout `C:/Users/Lenovo/Downloads/AI-RULES`. Changes are in root documentation, selected routing/coexistence references, the internal-method index, 57 guides, supporting Markdown and three MIT notices/provenance.
- Quality/installer: existing `main`, base `80f54467188a76ad95af3943221fd2a4b59d2181`, worktree `C:/Users/Lenovo/Downloads/AI-RULES-main`. Changes cover scoped package/registry validators, source reconciliation, operational/behavior/installation checks, regression tests, evals, family documentation, this evidence directory and the existing plan.
- The worktree was created for the **existing** `main` branch. No branch creation, staging, commit, push, merge, rebase, stash, destructive cleanup or real global installation is part of this delivery. User untracked prompts, sources and other directories were preserved.
- See `preflight.json`, `preflight-upstreams.json` and final preservation evidence for exact refs/status. Frozen release manifest and sibling pins remain unchanged.

Those bullets describe the original local handoff. The later explicit user authorization permits scoped staging, commit and normal push for `andino-workflow` and `main`. MAIN now pins the published Andino commit at global/Andino sequence **13**; all six sibling entries remain identical to the previous manifest. No new branch, force push, merge, tag, global setup or installer binary release is authorized or performed by this continuation. `publication-preflight.json` and `staged-runtime.json` identify the reviewed publication scope.

`changed-files.json` lists the exact local change surface, including files Git's tracked diff omits: runtime has 7 modified tracked files and 115 new owned package files; MAIN has 7 modified tracked files plus its new quality/evidence files. Disposable `build/` candidates are generated artifacts and are not release refs.

## 3. Upstream snapshots

| Source | Commit | Tree | Actual inventory | State / notice |
| --- | --- | --- | --- | --- |
| [Addy](https://github.com/addyosmani/agent-skills) | `aeac41d4d005999432bb7312f7ff06383a91d59d` | `8483a004722df18e33800e00da9880f328db5e7c` | 217 tracked files, 25 skills | clean, MIT 2025 Addy Osmani |
| [Matt](https://github.com/mattpocock/skills) | `49dd158d1076134a641b33efb035946536778336` | `3ce485319972aae46dec0c2ac34cf4a7f28f7414` | 190 tracked files, 38 skills + 1 archived record | clean, MIT 2026 Matt Pocock |
| [Superpowers](https://github.com/obra/superpowers) | `bb92a77741419a4ab5f06e711a283343f1ada0c3` | `4ac675daa3415bc836f707c7e60237ac7b66c7d5` | 238 tracked files, 15 skills | clean, MIT 2025 Jesse Vincent |

The three `*-audit.json` files contain source-path/byte manifests and resource/provenance decisions; corresponding Markdown files explain them. These are complete inventories of the actual local snapshots, not assertions about future upstream versions.

## 4. Coverage

`coverage.json` accounts for 79 source records: **61 stable, 4 misc, 5 meta, 1 setup, 7 in-progress, 1 deprecated**. All 65 stable/misc records map to substantive bundled procedures. Meta/setup functionality goes to the root contract or a relevant internal method. Seven immature records are conditional, with bounded procedures and explicit limits. The archived deprecated record is excluded with a rationale. No eligible record is silently deferred.

There are **57 canonical guides plus the root-contract destination**, and **116 source-resource dispositions** in `resource-map.json`. Per-row `verification_evidence` resolves fixture IDs, procedural report/record and separately graded selection evidence. Mapping, bounded operation and live selection are distinct claims.

## 5. Conflict resolution

`ownership.json` has 19 concerns, each with one owner, precedence, trigger/non-trigger, effects, permission boundary, fallback and negative-test references. `canonical-decisions.md` records the source comparison and rulings:

- TDD: accepted public seam and independent literal oracle; one RED→minimal GREEN behavior at a time; optional refactoring is a separate GREEN-only review gate.
- Diagnosis: one discriminating investigation before repair; environment prevention follows established causes.
- Requirements and planning: resolve only material open decisions; refine the one Andino plan/graph rather than create another lifecycle.
- Review: current owned diff/untracked inputs, spec axis then relevant quality/security/standards; completion requires parent inspection and current observations.
- Delegation: actual authority/tool/benefit, at most three direct children, disjoint writes, no nested spawning; inline fallback otherwise.
- Focus, Search First, UI, academic, Rescue/Council and Three.js keep their existing ownership and native invocation controls. A bundled method cannot bypass a denied/manual-only sibling.

## 6. Runtime architecture

One native `SKILL.md` remains. `references/internal-method-index.md` selects progressively from `skills/<id>/GUIDE.md`; local `resources/`, `references/`, `templates/` or `examples/` hold supporting Markdown. The frozen candidate has **127 Markdown files** and no bundled executable, upstream bootstrap, hook, server or fetch dependency.

Explicit relevant internal IDs resolve to local guides. Source aliases converge on canonical methods; `ask-matt`, `using-agent-skills` and `using-superpowers` are not callable bootstrap aliases. Actual permitted guide reading establishes ACTIVE; relevant observed action establishes USED. Discovery, availability, invokability and use remain distinct. Missing/denied resources stay unavailable; no alternate-copy bypass or invented native invocation is permitted.

## 7. Multi-agent evidence

Three source audits/implementation scopes ran independently; shared root/index/registry changes were integrated serially by the parent. Separate oracle-hidden Codex actors performed selection and actual implementation, diagnosis and review fixtures. Actors could write only their own output directories and could not spawn children. Two independent reviews examined runtime and MAIN; the parent reproduced findings, added failing regression checks and integrated fixes.

The original `actors/`, `actors-v2/`, raw inputs and oracle/grade files are retained. Actor success alone was not accepted. Parent grading checks exact guide paths/hashes and expected inclusion/exclusion; actual small fixture code is inspected and checked independently. Codex actor evidence proves the recorded resource workflow, not ordinary native picker discovery or another host's delegation behavior.

## 8. Installer

The scoped Andino validator accepts safe internal Markdown paths, rejects nested native identities (including Windows case variants), unsafe/reserved paths, collisions, non-regular files and broken local links/images. Other package families retain their policies. The existing atomic whole-directory installer/backup/idempotency implementation was reused.

`installation.json` records actual disposable offline CLI scenarios: 30 profile/custom × host fresh/repeat pairs, five modified-managed blocks with edits preserved, five unmanaged conflicts with content preserved, and clean update + original backup + repeat NO_OP. Actual sibling branch exports are used. Upstream directories are not supplied to the fixture/installer; this is not an OS-level filesystem denial claim. No network source or real global installation is used.

## 9. Verification

Run commands from the MAIN worktree; use the native commands below (the local host wrapper used during execution is not a project dependency):

```text
python -m unittest discover -s tests -v
python scripts/validate_skills.py --andino-dir build/andino-unified-publication --webbased-ref origin/WebBased --threejs-ref origin/threejs-skills
python scripts/validate_andino_capabilities.py --runtime build/andino-unified-publication
python scripts/validate_andino_unified.py --runtime build/andino-unified-publication --check-sources
python scripts/check_andino_addy_methods.py
python scripts/check_andino_matt_methods.py
python scripts/check_andino_superpowers_methods.py
python scripts/check_andino_installation.py --runtime build/andino-unified-candidate-v3
python scripts/check_andino_publication.py
python scripts/build_release.py --stage-only --output build/andino-unified-release-13
python scripts/grade_andino_behavior.py --runtime build/andino-unified-candidate-v3 --oracle docs/validation/andino-unified/routing-oracle-v2.json --actors docs/validation/andino-unified/actors-v3 --catalog docs/validation/andino-unified/native-catalog.json --output docs/validation/andino-unified/behavior-grade.json
python scripts/run_andino_capability_eval.py --runtime build/andino-unified-candidate-v3 --catalog docs/validation/andino-unified/native-catalog.json --case debugging-superpowers-route --host claude-code --timeout 60 --output docs/validation/andino-unified/claude-debugging-v3.json
git diff --check
```

The baseline had 195 tests and one pre-existing opt-in skip. **Final unittest: 223 run, zero failures/errors, one unchanged opt-in skip** (`final-tests-v3.log`). The 28 focused corruption/evidence/containment gates pass. All **57 bounded method procedures**, **41 installer scenarios**, **114/114 v3 selections**, source reconciliation and package/registry/sibling validators pass. `parent-work-grade.json` independently confirms eight implementation cases, four review cases, both review axes and two faulty-before copies. Each `*-operational.json` binds exact guide/resource bytes, method metadata, checker and manifest identities. The Addy checker also runs 18 adversarial cases and kills 18 load-bearing mutations. These examples prove bounded operations; they do not prove future model compliance or actual browser/production operations.

Evidence history is deliberately visible: v1 strict selection was **109/114**; five mismatches exposed phase/authority ambiguity in fixtures. The original requests/oracles are retained and five clarified raw fixtures are separately identified. v2 was **113/114**: the unchanged invoice request revealed premature API design before TDD; root phase guidance was clarified. The initial Claude trace also loaded diagnostic evidence too early; sequencing was corrected, with later traces retained separately. `final-tests-v2-failed.log` records an intermediate schema mismatch, corrected by preserving adaptive-case field presence and recognizing canonical method IDs. None of those earlier results is relabeled PASS.

`native-grade.json` reviews actual traces: initial Claude ordering FAIL; v2 scoped PASS on hash `9973fa8c41fc09768126d00aadb2b95cd1d5c93ca16cc9a704492b5afbc8b9cf`; final v3 NOT VERIFIED because the account returned its weekly-limit message. No unchanged retry or alternate-account bypass was attempted. The only v2→v3 runtime change is root guidance for settled-phase TDD selection; all 57 guides/resources and index are unchanged, but this lineage does not relabel v2 as a live v3 run. `review-resolution.json` and the independent `actors/batch-2/final-resolution.json` close all reproduced runtime/MAIN findings; the latter independently rejects all six checker/manifest omissions and validates all 57 current records.

| Host surface | Actual observed scope | Remaining limit |
| --- | --- | --- |
| Codex | Delegated resource selection and three disposable work fixtures; CLI inventory 0.154.0 | Actor model/version not exposed; ordinary native picker and Codex CLI run not claimed |
| Claude Code 2.1.300 | v2 restricted native Skill invocation, Focus, local guide/resource reads and fixture diagnosis; model `claude-opus-5-5` | v3 account weekly limit: NOT VERIFIED. Explicit temporary plugin registration; ordinary auto-discovery, mutations, MCP and delegation not proved |
| OpenCode 2.0.29 | Installed path/package and version discovery | Live behavior NOT VERIFIED: no controlled read-only evaluation adapter used |
| Antigravity CLI | Installer path/registration contract | Live behavior/version NOT VERIFIED: no controlled CLI conversation adapter identified |
| Antigravity IDE | Installer path/registration contract | Live behavior/version NOT VERIFIED: no controlled IDE conversation adapter |

## 10. Legal and security

Three complete MIT notices and runtime provenance are distributed. Superpowers' CC BY-SA community code of conduct is excluded; Anthropic-adapted reference expression with unresolved separate provenance is excluded, with independently worded concepts retained. Branding, servers, automatic bootstrap/install/commit hooks and dangerous source helpers are not imported as authority.

Operational Python is explicitly maintained QA code, extracted from reviewed bundled examples and executed in disposable fixtures; it is never auto-executed by installation. The Addy import/process/network/file guards are defense-in-depth for trusted reviewed examples, not a general sandbox for hostile Python. Outside-scope chmod/truncate are now regression-protected. Stale guide/resource/metadata/checker evidence, duplicate source accounting, missing notices and unsafe package structure are rejected. No credentials or live customer/production data are used.

## 11. Risks and open items

Live host parity remains unproven and is not a local implementation blocker under the user's explicit contract. A manual smoke on each untested surface must use a disposable project/account context: install only the candidate locally, start a fresh session, discover exactly one Andino, invoke its actual host mechanism, finish Focus/guide loading before work, then run the supplied invoice/diagnosis/review fixtures. Save raw tool traces, host/model/version, exact candidate hash, file hashes, assertions and negative permission tests. Do not assume a read counts as native invocation where a native tool exists.

Resume the final Claude smoke after the account's normal weekly reset. Preserve the failed attempt and its message; the actor reported a reset time but this delivery does not infer an absolute reset date or promise one.

For ordinary auto-discovery on Claude, repeat without explicit temporary plugin registration. For OpenCode/Antigravity, establish a restricted supported adapter before unattended execution; never reuse another host to bypass a denied action. Optional external instruments and production remediation require their own actual scope and evidence. Full semantic equivalence for all future tasks is not claimed by the bounded examples.

## 12. Release readiness and authorized branch publication

The original unpublished proposal is retained in `pre-publication/release-proposal.json`. The current `release-proposal.json` records actual runtime publication and the user's authorization. MAIN's manifest pins `efd9c508d55ed94ab2a1229e3324a008e7db71f0`, with only Andino/global sequence advanced to 13 and the verification date updated. Sibling pins are unchanged. The MAIN commit containing this report carries the quality-plane implementation and release pin; its actual identity is available from Git history and the executing agent's push confirmation.

`published-setup.json` records actual default-latest acquisition from the remote and disposable fresh/repeat plus official upgrade/backup/repeat checks. No source/catalog/network implementation is mocked; only `Path.home` points to the disposable home. `publication-tests.log` records the suite after the real pin update. A standalone installer binary/tagged release and remaining live host smoke are outside this authorized branch-publication delivery.

`publication-verification.json` is the current publication gate: all three runtime/package/source validators PASS, seven source bundles export successfully with the exact published Andino hash, remote setup PASS and the post-pin suite has 223 tests/zero failures/one unchanged skip. `main-eof-lineage.json` records five MAIN terminal-newline cleanups after that suite; all four affected Python ASTs are identical, and 28 focused tests plus all 57 procedures were rerun afterward. Original v3-only evidence stays revision-scoped.

`acceptance.json` reconciles the 32 task IDs actually present in GRAND-PLAN, 14 requirements and six quality gates. Q1–Q5 pass within the documented local scope; Q6 was approved by the user's later commit/push instruction for both existing branches. The evidence ledger is not another execution plan.
