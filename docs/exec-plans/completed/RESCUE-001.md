# RESCUE-001 - Canonical rescue contract, first slice

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 3 - Verification and handoff
Last Updated: 2026-09-19

## Executive Snapshot

First slice implemented: canonical skill and two core references, with metadata
validation and 10 existing isolated adapter/plan tests passing. Existing feature
branch matches the verified skills baseline; four unrelated user edits remain.
Repository-wide validation still fails on the same six pre-existing Markdown links.
No routing/distribution/live changes. Next action belongs to PM review before any
later slice; first-slice completion does not mean the entire GRAND-PLAN is complete.

## Objective

Provide an evidence-first, framework-independent rescue methodology with five
dispositions and bounded replacement gates, without a second lifecycle owner.

## Acceptance Criteria

- [x] Record local/remote baseline and protect existing changes.
- [x] Create a dedicated plan; do not repurpose ANDINO-002.
- [x] Create SKILL.md, evidence-and-findings.md and bounded-remake.md only.
- [x] Narrow eligibility; distinct dispositions; independent severity/confidence;
  provenance never proves a defect; all replacement gates operational.
- [x] Preserve Andino lifecycle and return evidence to its shared plan.
- [x] Validate metadata, references, plan and relevant repository behavior;
  disclose baseline failures and limits of semantic validation.
- [x] Prepare DEVELOPER HANDOFF and stop before later slices.

## Scope

Create `skills/ai-codebase-rescue/SKILL.md` and its two references:
`references/evidence-and-findings.md`, `references/bounded-remake.md`.
Maintain this plan. No routing, additional domain references, distribution,
generated installs, live installation, dependencies, plugins, commits, push, PR,
merge or deployment. The supplied GRAND-PLAN is specification; its broader roadmap
does not expand the bounded first-slice handoff selected by the user's START.

## Baseline / Starting Evidence

- Working directory: C:/Users/Lenovo/Downloads/AI-RULES.
- Branch: ai-codebase-rescue; HEAD f3210ca5d85c95306e2e7601519e1946752ac07f.
- Local skills and origin/skills match HEAD; `git ls-remote origin refs/heads/skills`
  confirms the remote also matches. No local-only commits against skills.
- origin: https://github.com/andinoferdi/AI-RULES.git.
- One worktree, this directory. Feature branch has no upstream.
- Existing modified files: README.md, adapters/README.md,
  put-in-your-projects/ai-rules/2. Send-to-every-prompt.md,
  put-in-your-projects/ai-rules/code-rules.md. All are RTK documentation edits;
  none overlaps the new paths. No initial untracked files.
- Canonical rescue directory absent; ANDINO-002 stays untouched.
- Root AGENTS.md's template link is stale. Located and read the actual contract
  at put-in-your-projects/ai-rules/AGENTS.md; no conflict with approved paths.
- Pre-edit `python -X utf8 scripts/validate.py` exits 1: six broken links:
  AGENTS.md -> put-in-your-projects/Agents.md;
  prompt-awal.md -> put-in-your-projects/1. First-prompt.md;
  README.md -> those same two missing template paths;
  put-in-your-projects/ai-rules/2. Send-to-every-prompt.md -> task.md and brd.md.

## Decisions / Deviations

- Reuse the already-existing dedicated ai-codebase-rescue branch. The proposed
  feat/ai-codebase-rescue name was a candidate; creating another branch adds no
  isolation value. Its base is verified and user edits need no relocation.
- Use andino-workflow for durable state and skill-creator for skill authoring.
- Keep baseline link repairs outside this slice; do not alter user-edited files.
- Source specification: C:/Users/Lenovo/Downloads/GRAND-PLAN ai-codebase-rescue.md,
  especially sections 12-16, 18-19 and 22; supplied PM handoff narrows scope.

## Execution Board

| Phase | Status | Evidence |
| --- | --- | --- |
| Phase 1 - Baseline | DONE | Git, remote and overlap inspected; baseline failure captured. |
| Phase 2 - Canonical contract | DONE | Three permitted files authored; no other skill resources. |
| Phase 3 - Verification and handoff | DONE | Metadata valid; 10 tests pass; baseline link failures disclosed. |

## Phase 1 - Baseline

Status: DONE

### Result / Evidence

Baseline above confirms the planned development line, non-overlapping dirty files,
and no worktree collision. No Git mutation was needed.

## Phase 2 - Canonical contract

Status: DONE

### Result / Evidence

- [Core skill](../../../skills/ai-codebase-rescue/SKILL.md): eligibility, lifecycle,
  scoped evidence, five dispositions, gates, verification and evidence return.
- [Evidence contract](../../../skills/ai-codebase-rescue/references/evidence-and-findings.md):
  impact/confidence, full finding schema, claim discipline and provenance separation.
- [Replacement contract](../../../skills/ai-codebase-rescue/references/bounded-remake.md):
  six gates, protected replacement/swap/removal and full-rewrite threshold.
- No framework dependencies, new scripts, assets, host metadata or speculative links.

## Phase 3 - Verification and handoff

Status: DONE

### Result / Evidence

`quick_validate.py skills/ai-codebase-rescue` from the installed skill-creator
reports "Skill is valid!". `python -X utf8 -m unittest discover -s scripts
-p validate.py -v` passes all 10 existing tests. Their sync/hardening operations
run against temporary homes, not live installs. `git diff --check` passes.
The repository entrypoint still exits 1 on the exact six baseline links listed
above; no new broken link is reported. This is not a claim of a fully green repo.

Manual semantic review (document review, not agent/model execution):

| Scenario | Contract outcome and evidence |
| --- | --- |
| Healthy AI-authored module | Authorship alone is non-trigger; assessed healthy area KEEP; provenance deletion rule. |
| Typo or one known local bug | Ordinary workflow; eligibility rejects rescue escalation. |
| Repeated regressions but unclear behavior | INVESTIGATE; contract/baseline cannot PASS; concrete evidence action required. |
| Severe localized permission defect | Severity is urgency, not REMAKE; bounded repair with permission regression proof. |
| Structure repeatedly causes bounded instability | Compare incremental repair; REMAKE only with six evidenced PASS gates. |
| Apparently unused dynamically registered path | No-hit search insufficient; inspect registration/consumers before REMOVE. |
| Request to replace whole repository | Separate evaluation authorization and system-wide threshold; no automatic rewrite. |
| Dirty target with unknown user changes | Stop affected mutation; preserve edits and return conflict to Andino. |
| Claimed speedup without measurements | Unverified claim; comparable baseline evidence required. |
| Direct invocation without lifecycle context | Bind to Andino; if unavailable return findings/context gap, no second lifecycle. |

These checks assess the written contract only. Live trigger/non-trigger behavior,
cross-host discovery and scenario execution remain future validation work; this
slice does not install or route the skill.

## Verification Matrix

| Check | Actual result |
| --- | --- |
| Repository entrypoint before edits | FAIL: six existing links; behavior tests not reached. |
| Skill metadata | PASS: skill-creator quick_validate.py. |
| New local references / whitespace | PASS: all five links in the four new files resolve; no trailing whitespace. |
| Completed ticket plan | PASS: validate.validate_plan returns STANDARD with all three phases DONE. |
| Existing isolated adapter/plan tests | PASS: 10/10 via unittest discovery. |
| Manual disposition/eligibility scenarios | Reviewed above; no live invocation claim. |
| Repository entrypoint after edits | FAIL: exact same six baseline links. |

## DEVELOPER HANDOFF

Objective: canonical first slice only. Result: implemented and locally checked;
ready for PM review with the pre-existing repository-link caveat. Branch reused:
ai-codebase-rescue at f3210ca. Changed scope: three canonical files plus this new
plan. ANDINO-002 and the four existing user edits were not edited by this ticket.
No commit, remote mutation, PR, routing, distribution or live installation.

Decision/deviation: reuse the already-correct feature branch instead of creating
the proposed candidate; locate the moved project contract without repairing its
stale caller. No product decisions changed. Later roadmap phases remain unapproved.

## Progress Log

- 2026-09-19: Verified baseline; created dedicated plan before implementation.
- 2026-09-19: Authored canonical slice; validated and prepared bounded handoff;
  moved completed ticket into the completed-plan directory.

## NEXT ACTION

PM: review the three linked canonical files and the evidence/limitations above;
return GO or REVISE with the next bounded scope. Do not begin routing, additional
references or distribution from this completed first-slice ticket.
