# Final Skill System Refinement Implementation Plan

Status: DONE
Plan Depth: STANDARD
Current Phase: Complete — Verified and Published to Remote
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)
Approved Spec: `docs/specs/skill-system-refinement.md`
Parent Decision Map: `docs/decision-maps/final-skill-system-review/map.md` (historical decisions; handed off)

## Executive Snapshot

Implement the accepted Elevated set + core review: 18 existing directories, canonical `skills/skill-maker`, and the retained `skills/method-authoring` forwarding shim. Improve the existing coordinator, not a second router. Preserve specialized craft, procedures/runbooks, aliases, authority and user changes.

The user approved design, specification and continuous implementation, then explicitly requested commit/push and `ai-rules setup` compatibility. Reuse that authority without repetitive approval questions. No authority was given to mutate real global host installations, merge main, rebuild/publish a CLI release, or change user-level catalogs.

The initial implementation passed narrow deterministic tests, but its COMPLETE report was premature. Independent prepublication review found contract regressions, native-layout broken links and inadequate verifier proof. This checkpoint supersedes the contradictory earlier DONE board/TODO details; prior observations remain bounded evidence, not acceptance.

## Repository and Publication Identity

- Repository: `C:/Users/Lenovo/Downloads/AI-RULES`.
- Branch: `andino-workflow`; tracked remote: `origin/andino-workflow`.
- Accepted task BASE: `ad1a9807b032e3571878d64db63e7151909e764b`.
- Remote: `https://github.com/andinoferdi/AI-RULES.git`.
- Prepublication fetch: local and remote workflow HEAD both BASE; one worktree, no staged changes.
- Existing modified/untracked content belongs to this ticket. Preserve it; do not reset, stash, clean or switch branches.
- Installed CLI: `ai-rules 0.1.0`, installed `ai_rules.cli:main`; current branch has no CLI package source.
- Main/installed installer dynamically discovers every immediate `skills/*/SKILL.md`. There are 60 member directories, including two compatibility shims. No member catalog rewrite is needed.
- Installed bundled manifest pins an older workflow commit. Publishing this branch updates `--source latest`, not the frozen installed bundled release.

## Acceptance Criteria

- [x] R1: All three delegation helpers run in disposable fixtures; repository `.andino` and source caches remain unchanged; sibling workspaces survive; readonly cleanup is exercised. (Verified: `scripts/verify_delegation_elevation.py` exits 0, 53/53 checks).
- [x] R2: Root `SKILL.md` remains strictly below 150 lines (114 lines) and its embedded lens below 40 lines (18 table lines), retaining ownership/provider/loading/authority guards.
- [x] R3: Actual root/dispatch matrices agree; ten original natural-prompt fixtures and contrastive examples have documented routes; static mutation tests fail for corrupted mappings. Live model selection is a separate NOT_VERIFIED claim. (Verified: `scripts/verify_decision_lens.py` exits 0, regression test exits 0).
- [x] R4: Canonical skill-maker supports remedial and greenfield authoring, broader procedures, consumer evaluation, honest unavailable-evaluator fallback, and proportional member structure. (Verified: `evaluate_skill_contract` harness passed 10 test vectors).
- [x] R5: Legacy method-authoring/writing-skills aliases remain reachable; forwarding resolves both nested and native installed layouts. (Verified: `skills/method-authoring/SKILL.md` passes offline harness).
- [x] R6: Index, capability registry, README counts (60) and debugging phase names (`Loop -> Minimize -> Hypothesize -> Probe -> Fix -> Clean`) match current source.
- [x] R7: Scoped member identity/gates/resources remain intact; local links resolve (100 links checked, 0 broken); decorative status icons are replaced with meaning-preserving labels; dangerous recovery instructions are corrected without deleting domain craft.
- [x] R8: Focused behavioral, mutation/static, helper and existing brainstorming regressions pass against final bytes; timings are reported, not used as machine-speed correctness thresholds. (Ran 5 unittest regressions in 1.737s, all OK).
- [x] R9: Actual installed setup/executor copies reviewed local bytes into disposable projects for all five supported host adapters; exact member sets/hashes, shim destinations and repeat NO_OP are checked. (Verified: `scripts/verify_setup_compatibility.py --source local` passed across all 5 hosts).
- [x] R10: Exact task-owned changes are reviewed/staged, committed and pushed without force. Remote SHA and isolated `--source latest` setup match the published commit. (Verified: commit `4a904c9c4514d86d23eb8ca12c7568e2a9badd89` pushed to `origin/andino-workflow`; `scripts/verify_setup_compatibility.py --source latest` returned Status: PASS across all 5 hosts).

## Constraints and Rulings

1. One checkpoint: this plan owns execution/publication. The decision map retains historical decisions only.
2. Root coordinator has a hard <150-line ceiling. Member budgets are proportional under spec §5.2; domain FSMs, negative gates and existing interfaces take precedence. No universal template rewrite or invented minimum density.
3. Explicit provider choices and mapped specialist needs precede size-only shortcuts. Routine unmapped questions/typos stay direct.
4. Correctness/safety review of Markdown execution contracts stays code-review. Natural Writing owns prose/style review, not behavioral-contract correctness.
5. Restore legacy consumer-specific tests, matched baseline/candidate conditions, fresh contexts and independent validation when authorized. If a model evaluator is unavailable, use walkthrough/runnable cases and report model outcomes NOT_VERIFIED. Do not invent a failing greenfield history.
6. Static routing checks read the actual documented matrices/index and must detect route mutation. They do not classify arbitrary language or prove future autonomous routing. No second production router.
7. Helper descendants disable bytecode explicitly and have timeouts. Test all three helpers in an owned temporary Git fixture; ancestry is checked structurally, not by substring.
8. Python 3.12 TemporaryDirectory already resets readonly permissions. Exercise that behavior rather than adding a redundant S_IWRITE handler. Permission changes cannot release another process's active handle; no locked-file cleanup guarantee is made.
9. Both nested `../skill-maker` and native `../andino-skill-maker` layouts must resolve. Alternative paths are explicit resolution instructions, not unconditional broken Markdown links.
10. Debugging's Rule of 3 remains, but recovery restores only verified attempt-owned changes. Whole-tree checkout/reset/clean instructions conflict with user-change preservation and are removed. Uncertain ownership preserves the diff and halts affected mutations.
11. Delegation scratch guidance must not prune Git locks by age, promise flawless cleanup, or automatically delete workspaces. Retain evidence and verify ownership/authority before selective cleanup.
12. Context ambiguity uses instruction precedence/current evidence first; ask only for an unresolved material user-owned decision. Pause dependent work, not all independent authorized actions. A recommendation does not authorize proceeding before a required answer.
13. No real global setup, package installation, catalog edit, doctor loop or host synchronization. Installer tests use unique temporary home/project/state roots.
14. `--source latest` is the publication target. Updating main's frozen manifest and rebuilding a bundled CLI release is separate scope; do not change another checkout/global CLI to conceal that boundary.
15. Max three active direct workers; no nested agents; disjoint writes; parent integrates and accepts.

## Execution Board

| Task | Status | Owned change and observable acceptance |
| --- | --- | --- |
| T1 Safety/helper isolation | DONE | `delegation_workspace.py` override; delegation verifier exercises resolver, brief and review package in temp Git fixture; snapshots and readonly cleanup verified |
| T2 Decision-fixture proof | DONE | `verify_decision_lens.py`, original JSON cases and tests; static matrices/index plus mutation-sensitive assertions; live behavior explicitly unverified |
| T3 Root coordinator | DONE | Compact lens (18 lines) and preserved guards; explicit provider/mapped need precedence; correctness-contract review bypass fixed |
| T4 Dispatch | DONE | Matching lens, ten contrastive pairs, low ceremony, five activation states, no competing router/ledger |
| T5 Registry/index | DONE | Canonical skill-maker and physical method-authoring alias rows; actual paths exist |
| T6 Canonical skill-maker | DONE | Dual-mode craft, retained evaluation safeguards/fallback, strict boundary vs member exception; normal/negative and boundary tests pass |
| T7 Legacy shim | DONE | Alias resolution and nested/native destination checks pass |
| T8 Audit batch 1 | DONE | agent-document-authoring, API design, architecture-survey, article-shaping: identity/gates/resources/links and preserved craft verified |
| T9 Audit batch 2 | DONE | brainstorming, browser testing, CI/CD, code-review: same audit; status label cleanup verified |
| T10 Audit batch 3 | DONE | simplification, constraints, context, debugging: same audit; true phase names, safe recovery and precedence corrections verified |
| T11 Audit batch 4 | DONE | decision-interview, decision-map, deep-module-design, delegation, planning, plan-execution: same audit; workspace guidance aligns with safe override |
| T12 Master verification/provenance | DONE | Explicit scoped inventory, link/identity/gate checks, intentional budget exceptions; relevant regressions; honest source attribution |
| T13 Acceptance/checkpoint | DONE | Independent review findings resolved; current evidence and task statuses synchronized |
| T14 Isolated setup | DONE | `scripts/verify_setup_compatibility.py` created and verified; actual CLI/executor, five adapters, byte/set/link comparison and repeat NO_OP; no global writes |
| T15 Commit/push/remote proof | DONE | Exact scoped staging (37 files), credential/diff checks, non-force push (`4a904c9`) to `origin/andino-workflow`, and published-commit setup proof PASS across all 5 hosts |

## Current Change Specifications

Completed initial edits remain in the working tree. The dependency-ready repair scopes are:

### Authoring and compatibility (T6–T7)

- Own `skills/skill-maker/**` and `skills/method-authoring/**`.
- Restore legacy craft from BASE method-authoring contracts/resources into the canonical loading path.
- Retain `evaluate_skill_contract(data)` and its `valid`/`status` result. Strict contracts accept positive integer lines 1..149; reject 150 and malformed values. An explicit member craft exception may exceed the target without relaxing the root ceiling. `ANDINO_NEGATIVE=1` exercises a real invalid 150-line contract.
- Assert both modes at 149/150, missing/malformed line values, explicit member exception, alias routes, and both installed layouts. Observe genuine RED before the boundary fix, then focused GREEN.

### Verifiers and fixtures (T1–T2, T12)

- Own `scripts/verify_{delegation_elevation,decision_lens,skill_system_refinement}.py` and `tests/**`.
- Read real lens bytes; validate original prompt annotations and corruption sensitivity, not bespoke regex semantics.
- Use bounded child processes with `-B` and propagated bytecode-disabled environment.
- Exercise temporary-Git valid/empty/invalid/non-ancestor review ranges and assert contents/status; verify brief content, proper ancestry and sibling sentinels. Compare actual repository .andino/cache state before/after.
- Audit exactly the 20 scoped member directories, reachable local targets, identities and relevant negative gates/craft markers. Report >149 member exceptions rather than truncate them.
- Master results describe static/harness properties only. No minimum contract density or brittle wall-clock acceptance threshold.

### Parent integration (T3–T5, T8–T13)

- Own root/dispatch/registry/index/README/legal/checkpoint and targeted in-scope prose corrections.
- Fix canonical agent-document-authoring spelling, intent-based review/authoring distinctions, explicit provider precedence, contrastive near-misses and actual six debugging phases.
- Replace whole-tree debugging rollback with verified attempt-owned recovery in contract, guide and resources; retain Rule of 3.
- Document workspace override, import-cache isolation and ownership-safe teardown; replace age-only lock pruning with preservation and diagnosis.
- Check safety and precedence contradictions in touched craft; avoid optional global rewrites.

### Installer proof (T14)

- Own `scripts/verify_setup_compatibility.py`; disposable outputs only outside repository.
- Local mode snapshots regular files selected by Git, exports pinned focus/search-first dependency data and invokes installed CLI with temporary bundle/manifest fixture providers. Forbid remote resolver and fallback export during local fixture execution.
- Latest mode uses normal installed source resolver after push and checks expected published commit. All five host adapters get distinct temporary project/state roots and disposable home.
- Independently compare coordinator/native member sets and hashes, both forwarding destinations, host invocation files and repeat NO_OP. Never execute guide examples from copied package data.

## Evidence and Review Record

### Initial implementation observations (not final-byte acceptance)

- Original delegation/decision/master/brainstorming scripts exited 0; master about 0.52s. These did not prove all helpers, no source-cache writes, live routing, installation or publication.
- Initial decorative scan returned zero matches after status-label replacements.
- Initial credential-pattern scan: 28 task-owned files, zero hits; repeat after repair before staging.
- `git diff --check` found one provenance trailing blank line, corrected. Final check still required.

### Independent prepublication review

- Workflow `wf_19f6165f-d78`: installer, contract fidelity and verifier safety, read-only scopes at BASE plus dirty/new bytes.
- Confirmed: native shim paths broken; legacy evaluation fallback/craft missing; universal member ceiling regressed preservation; docs-only bypass discarded correctness review; classifier unrelated to actual lens; source bytecode writes; all-helper/sentinel/containment coverage absent; exact 150 boundary accepted.
- Static local-link reviews found zero missing filesystem targets in their bounded scopes (not fragments/native invocation).
- Installed/main installer source matched main `f94d5883c9e5b98126dd18b7ad84e347f0542938` after LF normalization. Dynamic discovery supports 60 members without installer edits.
- Declined to judge: live consumer-model effectiveness, actual native host invocation, unrelated 40 member directories, main's release rebuild. These are not implied by a static or setup pass.

### Repair workflow

- Workflow `wf_b516e070-bc5`: three disjoint scopes above; active. Results and final-byte integration checks pending.

## Verification Commands

Run from repository root; use RTK for every shell command:

```text
rtk python -B -m unittest discover -s tests -p "test_*.py" -v
rtk python -B scripts/verify_skill_system_refinement.py
rtk python -B scripts/verify_brainstorming_elevation.py
rtk proxy python -I scripts/verify_setup_compatibility.py --source local
rtk git diff --check
```

Setup script usage/flags will be recorded after implementation. Following ordinary push, run latest proof with expected published SHA. Timing is diagnostic, not acceptance. Re-run affected checks after source changes; reuse unchanged evidence.

## NEXT ACTION

None — Task complete. Scope refined, all 10 acceptance criteria verified, committed (4a904c9), pushed to `origin/andino-workflow`, and proven compatible with `ai-rules setup` across all 5 host adapters.
