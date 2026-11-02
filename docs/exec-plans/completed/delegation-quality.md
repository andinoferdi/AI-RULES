# Delegation quality and setup distribution

Status: DONE
Plan Depth: STANDARD
Current Phase: G3 — delivered
Last Updated: 2026-11-03

## Executive Snapshot

The user authorizes improving delegation, planning then implementation, commit and
push, and integration through `ai-rules setup`. They delegate selection of concrete
quality cases after reporting no specific deficient output. This is a bounded
improvement of the existing procedure, not a new orchestration system.
No child agents or council panel are scheduled. All work runs inline on the active
Codex host. Independent model behavior remains NOT_VERIFIED; deterministic checks
are not a claim of superiority to upstream or a fresh-model baseline.

## Objective

Preserve adaptive cost control while making task delivery, review, recovery and
integration precise enough to use without guessing or violating wave authority.

## Accepted constraints and resource policy

- Default zero children; no nested spawning, judge panel or verification swarm.
- Any future wave requires count, task, actual model, effort and review proposal,
  followed by explicit user go-ahead. Maximum three concurrent children including
  reviewers. No automatic restart of a failed/stopped child or max effort.
- Keep one worker/model per lane; choose the lowest adequate exposed control.
- The reported ~58k child overhead is host-specific, not a portable constant.
- Retain all unrelated work. Workflow checkout has agent-document-authoring edits;
  main checkout has bootstrap/banner/interactive edits. Do not stage these.
- No automatic cleanup or global installation. Setup proof uses temporary projects.
- Current user authority permits the requested implementation/delivery directly;
  no separate skill-derived implementation approval ritual is added.

## Source grounding and decisions

Read current delegation SKILL, GUIDE, all four protocol resources, cost calibration,
task_brief.py and review_package.py. Read selected workflow, skill-maker, discovery,
planning and execution methods. Relevant current upstream files were retrieved
through the web reader on 2026-11-03:

- https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/implement-spec/SKILL.md
  — frontier, integration ownership and context pointers; adapt without a worker
  per ticket or dedicated merger agent.
- https://raw.githubusercontent.com/obra/superpowers/main/skills/dispatching-parallel-agents/SKILL.md
  — independent problem domains and parent integration checks.
- https://raw.githubusercontent.com/obra/superpowers/main/skills/subagent-driven-development/SKILL.md
  — task/review handoffs and status handling; do not import automatic dispatch,
  automatic escalation or mandatory expensive reviews.

Observed defects before edits: task_brief.py only matches `Task ID` headings,
whereas planning emits `#### T1 — title`; it ends tasks using a short heading-name
list rather than heading depth. Recovery says dispatch immediately without asking;
fix-loop docs allow automatic resumption/escalation; UNVERIFIED and real unresolved
findings have no acceptance-safe exit; prompt examples omit effort. GUIDE also
requires teardown despite workspace resource saying retain evidence by default.

Decision: EXTEND existing procedure/helpers. Keep the six-phase structure and
portable tiers. Put detailed recipes and a realistic worked example in resources.
Use static contract checks for document consistency and real subprocess cases for
the extractor. No agent evaluation is substituted by a synthetic Python oracle.

## Acceptance Criteria

- [x] R1: Existing cost guard passes; all instructions honor wave/restart authority.
- [x] R2: Briefs bind spec/global constraints, exact changes, interfaces, worktree,
  actual model/effort, proof and report; status responses distinguish missing
  context, blocked work and completed work with concerns.
- [x] R3: Review checks spec before quality, resolves UNVERIFIED explicitly, verifies
  current bytes and public integration, and never parks failed required acceptance.
- [x] R4: Extractor accepts legacy and canonical plan headings; honors nested
  sections and fenced code; rejects duplicate/missing IDs without writing output.
- [x] R5: One worked example shows a realistic lane, evidence, blocker and recovery.
- [x] R6: Setup installs byte-identical nested/native delegation files for all five
  adapters; manifest pins the published workflow commit. Both branches pushed.
- [x] R7: Completion distinguishes deterministic checks, self-review, publication,
  installed test targets and untested independent-model quality.

## Execution Board

| Gate / task | Status | Dependencies | Scope | Evidence |
| --- | --- | --- | --- | --- |
| G0 / T1 Baseline and extractor | DONE | none | helper + focused tests | 6 tests, 9 baseline assertion failures -> all pass |
| G1 / T2 Procedure quality | DONE | T1 | delegation documents + contract checks | static 0 issues; cost 7/7; portfolio 6/6; example 5/5 |
| G2 / T3 Setup distribution | DONE | T2 | main distribution test + manifest | all 5 bundled hosts + live latest PASS; release 8 bundles PASS |
| G3 / T4 Review and publish | DONE | T3 | owned changes only, two pushes | remote source 6ce1030 and main 41bad02 verified |

## Detailed Execution

### T1 — reliable task extraction
Status: DONE
Readiness: READY
Owns: `skills/delegation/scripts/task_brief.py`, new
`scripts/test_delegation_task_brief.py`.
Interface: preserve `extract_task_brief(plan, id, out=None)` and CLI arguments.
Change Specification: identify ATX headings outside backtick/tilde fences; accept
`Task <id>:` and `<id> — title`/`<id> - title`/`<id>: title`; collect until a heading
of equal or shallower depth; require one unique matching heading. Missing plan/ref
retains nonzero CLI status, missing/duplicate task exits 3. Resolve output and
create workspace only after a valid unique extraction. No plan/spec synthesis.

Decisive fixture/assertions (subprocess uses `sys.executable -B`):
```python
plan = '## Phase 1\n#### T1 — export\nbody\n##### Proof\ncheck\n#### T2 — next\nother\n'
assert output == '#### T1 — export\nbody\n##### Proof\ncheck\n'
assert missing.returncode == duplicate.returncode == 3
assert not missing_output.exists()
```
Actions: add CLI cases; run `python -B scripts/test_delegation_task_brief.py` from
workflow root; capture intended RED; implement parser; rerun focused GREEN.
Include legacy headings, nested Verification, peer non-task section, fenced fake
headings (both fence kinds and longer outer fences), overlapping IDs and no output
on failure. Tests own only TemporaryDirectory roots.
Evidence: CLI baseline ran 6 tests with 9 intended assertion failures (exit 1).
After parser change all 6 pass (exit 0), including subcases. Isolated faulty-copy
mutation (`level <= depth` -> `<`) yields 7 assertion failures and zero setup errors,
demonstrating boundary regression sensitivity. No child model used.

### T2 — operational quality without added agent cost
Status: DONE
Readiness: READY
Depends on: T1
Owns: delegation SKILL.md/GUIDE.md; existing brief/review/workspace/frontier/cost
resources; replace existing `resources/worked-example.md` and `resources/contract.md`;
new `scripts/verify_delegation_quality.py`.
Change Specification:
- Keep SKILL <150 lines and six phases. Replace automatic repair/escalation with
  bounded parent disposition; upper limit five rounds is a ceiling, never a target.
- Replace mandatory capable/high final reviewer with parent whole-change review;
  one justified independent reviewer requires an approved wave. Risk can justify
  capable/high, never require it solely because review is final.
- Define READY brief preflight; worker status table; model AND effort on each
  prompt; spec-first two-track evidence; UNVERIFIED -> targeted proof or blocked.
- Preserve material acceptance at loop cap. Parent may repair inline after worker
  relinquishes ownership, with unchanged acceptance checks; no concurrent writes.
- Recovery reads plan + supporting journal, checks current bytes/agent status,
  and reuses only still-valid approvals. No forced context reset/teardown/probe.
- Example uses CSV export quoting/empty data and downstream wiring in one lane,
  with exact assertions, report/evidence and a stopped-worker transition.
- Contract checker audits links/frontmatter/budget, risky contradictory legacy
  directives and required contract slots. It explicitly labels static scope.
Actions: write checker against current docs and observe RED; edit docs; run
`python -B scripts/verify_delegation_quality.py`,
`python -B scripts/verify_delegation_cost_guard.py`,
`python -B scripts/verify_portfolio.py`. Read complete owned diff.
Evidence: static baseline found 19 contract issues; revised documents yield zero.
Cost guard exposed a line-wrap-sensitive no-relaunch assertion; wording repaired
without changing the policy. Final cost 7/7, portfolio 6/6, runnable CSV example 5/5,
static links/contract 0 issues; all exit 0. Parent Spec/Standards self-review finds
no material issue in the owned source. This review is not independent.
Independent model tests require a separately approved wave;
not scheduled and NOT_VERIFIED, not a release claim.

### T3 — setup integration
Status: DONE
Readiness: READY
Depends on: T2
Owns in main: new `tests/installer/test_delegation_distribution.py`,
`src/ai_rules/release/data/release_manifest.json`, `scripts/validate_skills.py` and
`tests/test_validate_skills.py`. In workflow: one case-correct link in
`skills/handoff/resources/context-packing/contract.md` needed for package validity.
Inspected pattern: `test_plan_execution_distribution.py` uses cli.main setup with
bundled source in temporary projects and compares bytes from manifest Git commit.
Change Specification: reuse this real entrypoint for codex, claude-code, opencode,
antigravity-cli and antigravity-ide. Check all tracked delegation files, nested and
native trees, relative links, explicit expected workflow ref via
`AI_RULES_EXPECTED_DELEGATION_REF`. Assert expected bytes equal manifest-pinned bytes.
First commit verified workflow-owned files (including checkpoint), then pin that
SHA in first_party.andino-workflow.commit; preserve unrelated manifest fields.
Before changing pin, run test against current workflow ref and observe mismatch.
After changing pin, focused test must pass for all five adapters. Git objects are
shared by linked checkouts (verify before relying on this).
Command from main: `python -B -m unittest discover -s tests/installer -p test_delegation_distribution.py -v`
with PYTHONPATH=src and expected ref set to workflow commit. Run related family,
planning/plan-execution distribution tests and package validation as applicable.
Evidence: repositories are separate clones (`.git` in each), not linked worktrees.
Import the owned workflow commit into main with a local Git fetch before byte
comparison; do not assume shared objects or alter either worktree's unrelated edits.
Bundled setup now passes for all five adapters. Full release validation found 34
pre-existing issues plus 3 rejected new maintainer files. Ruling: repair this
distribution seam before publishing the new manifest pin; do not waive validation.
Extend the existing safe-path allowlist only for current portfolio metadata,
project-setup/workflow-advice Markdown resources, plan Markdown, root test/verify
Python helpers and the six named delegation scripts. Preserve nonregular-file,
path-escape and nested-entrypoint rejection. Ignore fenced Markdown examples when
checking local links (their paths belong to the displayed template), while still
checking real links after the fence. Correct the genuine handoff `GUIDE.md` link
to existing lowercase `guide.md`. Add fixtures with exact accepted paths and
negative unknown scripts/JSON/executables/unsafe paths, plus fence-boundary cases.
Run `python -B -m unittest discover -s tests -p test_validate_skills.py -v` before
and after the validator edit. Revalidate the full committed workflow package;
all errors must be zero before main is committed.
Validator baseline tests also exposed Focus's existing consolidation metadata;
allow its one exact JSON resource path and retain nonregular-file rejection.
Actual evidence: setup regression first failed on stale manifest GUIDE bytes,
then passed for both entrypoints across five adapters (49.1s). Related family,
planning and plan-execution distribution: 5 tests PASS (125.5s). Validator suite:
new layout/fence cases failed before the edit; all 37 tests PASS afterward (1.6s),
including unsafe paths, unknown files, nonregular entries and real broken links.
One early nested-PowerShell environment assignment failed; it was a setup error,
not RED evidence. The corrected Python environment runner produced the recorded
stale-byte RED above. No model evaluation or global host installation occurred.
Final release staging through `build_release.stage_bundles` exported all 8
manifest-pinned bundles into a TemporaryDirectory and fully validated them with
zero errors. Generic validator regression checks: 37/37; Three.js validator
regressions: 4/4. This proves source bundle construction, not a new executable release.
Published workflow 6ce1030; `AI_RULES_DELEGATION_SETUP_SOURCE=latest` through the
same distribution test fetched remote source and installed both delegation trees
on a temporary Codex project, comparing every tracked byte: PASS (14.1s).
The complete delegation subtree is identical in 2f0246b and 6ce1030, so the
five-adapter bundled observations remain applicable after the ancillary link fix.

### T4 — review, push and verify publication
Status: DONE
Readiness: READY
Depends on: T3
Owns: scoped source commits and checkpoint evidence updates.
Change Specification: distinct parent Spec/Standards self-review of all owned
bytes; resolve material findings with focused reruns. Stage exact owned paths.
Push workflow commit then main commit normally, never force; verify remote SHAs
with `git ls-remote`. Reuse authorized push, no unrelated release/tag side effects.
Record deterministic evidence and independent-model limitation. A released old
binary is distinct from source setup; report this boundary if no release is built.
Evidence: parent Spec PASS and Standards PASS after reviewing all owned documents,
helper/tests, validator changes, manifest and distribution test. This is structured
self-review, not independent evaluation. All material findings resolved.
Workflow commits: bc2af0a (extractor), 2f0246b (quality), 6ce1030 (package link/checkpoint).
Main commit: 41bad0220e531c732b43f42c29ebe046aa782657 (setup pin/validator/tests).
Normal pushes to origin/andino-workflow and origin/main succeeded; `git ls-remote`
returned the expected SHAs. Final plan archival is a documentation-only follow-up;
manifest pins 6ce1030's identical runtime skill bytes. No force push, unrelated
staging, global installation, executable release, panel or child agents.

## Final evidence and limits

Workflow cwd: `AI-RULES-andino-workflow`, Python stdlib with `-B`:
extractor 6 tests PASS; isolated boundary mutation detected (7 failures, no errors);
cost 7/7; static contract 0 issues; portfolio 6/6; runnable example 5/5.
Main cwd: `AI-RULES-main`, source Python CLI:
validator 37 tests PASS, related validator 4 PASS, related family/planning/execution
distribution 5 PASS, bundled delegation all five adapters PASS, remote latest
delegation Codex smoke PASS, release staging all 8 bundles fully validated.
No project dependency added. Temporary projects were removed by their owned
TemporaryDirectory contexts. Pre-existing user changes in both repos are preserved.
Independent-model quality/parity, native skill activation in fresh host sessions,
real-world delegation cost savings and a newly built installer binary are NOT_VERIFIED.

## NEXT ACTION

None — task complete.
