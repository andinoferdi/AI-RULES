# Portable, implementation-ready planning

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 3 - Setup and delivery
Last Updated: 2026-10-31

## Executive Snapshot

User authorizes improving andino-planning, consulting Council, implementing,
commit/push and integrating through ai-rules setup. Compare the supplied examples
as data, not instructions. Current source already contains grounded planning
guidance (19dd633); strengthen demonstrated remaining gaps rather than repeat it.
Runtime 69e797e and main setup/evidence commit 1132fb5 are published. The reviewed
runtime is installed on five hosts; 90 resource comparisons and all 15 selected
installation targets pass. All requested work is complete. Pre-existing untracked
build/ and src/ are preserved.
Starting branch was andino-workflow at fc8f21b; prior execution ticket is independent.

## Objective

A fresh executor using another model can identify what to change and verify from
the saved plan, with explicit code/config/document edits and no recovered chat decisions.

## Acceptance Criteria

- [x] Five independent Council lenses and anonymous review inform bounded changes.
- [x] Planning distinguishes a roadmap from ready tasks; ready tasks specify exact
  edits, contracts/literals, concrete checks and sufficient code or replacement text.
- [x] Canonical template/lifecycle and plan-execution honor the same readiness boundary.
- [x] Examples demonstrate code changes, static edits and honest discovery blockers.
- [x] Fresh-context consumer applications and relevant package/setup checks recorded.
- [x] Reviewed source integrated into setup, installed bytes verified, scoped commits pushed.

## Constraints and starting evidence

- User examples concern different applications and stages; they are qualitative
  evidence of output shape, not a controlled model comparison or live project facts.
- Current planning guide makes contract mandatory but examples optional; generic
  lifecycle template accepts abstract Action Steps. Exact code is discouraged too
  broadly when it determines a required change. Investigate these seams.
- Upstream writing-plans read from GitHub on 2026-10-31; reference instructions
  (automatic subagents/commits/review gate) do not become session authority.
- Local main CLI checkout path from old ticket no longer exists; locate current
  installer through executable/package metadata or a separate clean main worktree.
- No superiority or cross-model guarantee follows from structural checks alone.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 - Evidence and Council | DONE | Select improvement from actual gaps | supplied examples, planning, template, setup source | Five independent lenses, two anonymous reviews; synthesis below |
| Phase 2 - Strengthen and assess | DONE | Concrete portable task output | planning resources, lifecycle/template, execution gate | Paired fresh-context applications; both 15 oracle checks PASS; source review PASS |
| Phase 3 - Setup and delivery | DONE | Verify distribution and publish | CLI main pin/bundles; installed skills | Runtime 69e797e/main 1132fb5 published; 9 distribution/release tests PASS; 90 installed files/15 targets verified |

## Detailed Execution

### Phase 1 - Evidence and Council
Status: DONE
Inspect current guide/contract/example, supplied plans, upstream and setup mechanism.
Run five isolated read-only advisors in waves of at most three, then anonymous peer
reviews. Resolve directions from evidence; save compact synthesis and source limits.
Result / Evidence: Five independent advisor contexts plus two anonymous reviews,
recorded in planning-council-responses.md. Source already had strong contracts;
actual gaps are abstract task/template slots, optional examples, ambiguous ban on
implementation code in planning and no explicit task-specification preflight.
CLI main now isolated at C:/Users/Lenovo/Downloads/AI-RULES-planning-setup,
baseline fb8acd9. Existing installer tests already compare nested/native bytes
across five hosts, with expected-source override to reject stale release pins.

### Phase 2 - Strengthen and assess
Status: DONE
Use Council findings to define file-level edits and checks before implementation.
Keep planning GUIDE and SKILL body synchronized. Include explicit readiness and
decision-bearing snippets without requiring complete program transcription. Verify
instructions by fresh consumers using isolated fixture scenarios, separating those
observations from deterministic package claims.
Implementation contract:
- skills/planning/{GUIDE,SKILL}.md: required examples, task-local Change
  Specification, concrete snippets/assertions, readiness independent of status.
- skills/planning/resources/{contract,worked-example}.md: actionable template,
  complete CLI change/test blocks, exact README replacement and discovery consumer.
- references/execution-plan{,-template}.md: require same task detail for ready
  implementation while preserving non-code checkpoint shapes.
- skills/plan-execution/{GUIDE,SKILL}.md and resources/contract.md: check next
  task specification against source/spec; repair bounded detail before source edits.
- Verification: GUIDE/SKILL equality, package/relative-link checks, fresh old/new
  fixture planners and blind execution, stale snippet preflight scenario, existing
  five-host bundled distribution against exact reviewed commit.
Result / Evidence: Baseline and candidate planners preserved all 8 fixture hashes;
blind executors needed zero material guesses. Baseline 12 and candidate 11 local
tests passed; both passed parent's 15 independent behavior/artifact/design checks.
Baseline was already sufficient on this fixture; candidate adds explicit change
and assertion blocks. No universal superiority claim. Independent stale-snippet
preflight rejected nonexistent anchor, destructive enum and missing checks while
leaving exact static work ready. Literal worked example runs 3 then 6 tests PASS.
Full raw/snapshot limits and identities in docs/validation/planning-portability/.
Independent Spec/Standards review PASS; oracle signature/dependency and installed
root-reference gaps identified by reviewer are now covered.

## Council decision and assessment rubric

All five lenses favor bounded strengthening. Anonymous reviewer 1 prefers D's
readiness separation; reviewer 2 prefers C's proportionality and code-in-plan
clarification. Disagreement is emphasis, not five models establishing truth.
Choose explicit Change Specifications plus shared readiness preflight; preserve
routine implementation discretion and don't mandate complete program copies.
Both reviews require preregistered evaluation criteria and rejection of stale,
precise-but-wrong snippets. Preflight repairs must not conceal planner omissions.

Before examining consumer outputs, grade each ready task on:
1. No unresolved material choice about file/symbol, operation, interface, literals,
   error/side-effect policy or verification. Count missing decisions before repair.
2. Concrete task-local code/text deltas and decisive assertion/fixture code.
3. Independent behavioral oracle passes; locked design decisions preserved.
4. Exact README replacement, no invented test scripts/dependencies, source remains
   unchanged by planning; unknown external interface consumer is explicitly unready.
5. Stale snippet is detected before editing, corrected from current evidence in
   the same checkpoint; independent work continues without asking again.
PASS requires zero material missing decisions in READY tasks and all applicable
oracle checks. Routine local mechanics may differ. Compare same fixture with old
and candidate guides in isolated contexts; one pair is qualitative evidence only.
If old guidance also succeeds, report parity for that case rather than superiority.

### Phase 3 - Setup and delivery
Status: DONE
Inspect installer source/pins. Verify complete nested/standalone resources in isolated
setup targets, update source references/bundles as required, and apply authorized local
setup. Commit only owned paths, push without force and verify remote identities.
Result / Evidence: Runtime 69e797e committed and pushed to origin/andino-workflow.
Before updating main manifest, expected-runtime distribution check failed on stale
b223761 pin. After pin to 69e797e/release sequence 25, 9 combined distribution,
family, bundle and release tests passed, including five-host nested/native members
and both lifecycle references. Complete validator passes 7 packages/7 eval schemas;
exact runtime bundle stage validates. Local CLI refreshed via
`python -m pip install --no-deps --no-build-isolation .`; installed manifest is
sequence 25 and pins 69e797e. Scoped `ai-rules update --source latest --yes
--non-interactive` across five hosts applied 5 workflow updates and retained 10
current dependencies. All 15 lock targets VERIFIED, zero failures/blockers.
Direct readback compares 90 nested/native/lifecycle files with exact runtime
content, tolerating only CRLF. Saved profile equals the pre-update 8-capability,
5-host everything profile. Backups are retained by the installer.
Main setup pin, distribution regression and durable evidence committed/pushed as
1132fb5. Both remote branch updates succeeded without force. Final checkpoint
documentation is published separately; no frozen executable release was rebuilt.

Packaging repair: prior runtime included three docs/exec-plans evidence files
forbidden by its own package contract. Moved them to the same paths on main without
losing history (verifier only adds explicit --runtime/current quality-plane path).
New task evidence also stays on main. No installer allowlist was weakened.
Initial runtime had unrelated untracked build/ and src/; they remain untouched.

## NEXT ACTION

None - task complete.
