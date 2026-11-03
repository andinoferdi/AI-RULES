---
name: andino-code-review
description: Use when reviewing a pull request, commit range, branch, work in progress, or agent handoff, or when requesting or responding to code review.
---

# Code Review Across Spec and Standards

Internal method ID: `andino-code-review` (alias: `code-review`).

> **Andino Workflow Member Skill**
> Use proportional investigation, evidence-based decisions, and one durable
> checkpoint. Keep the active workflow in control without invoking it again.

## Trigger and non-trigger

Review an identifiable change or evaluate feedback about one. Conceptual advice
and standalone cosmetic cleanup belong outside this procedure. Review mode is
read-only. Use the reception protocol when asked to act on feedback.

## 1. Pin the requested change

| Request | Review boundary |
| --- | --- |
| Commit or explicit endpoint comparison | Resolve the supplied endpoints to SHAs and inspect `git diff <base> <head>`. For one commit, use its requested parent comparison or the corresponding patch. |
| Branch or pull request | Resolve target and head to SHAs and compare their merge base to head. Use the PR target when known. |
| Work in progress | Capture the requested staged and unstaged layers plus in-scope untracked source. Include committed branch changes when the requested scope includes them. |
| Pasted diff or excerpts | Review the supplied bytes and report the unavailable context that affects the verdict. |

For WIP, use `git diff --cached`, `git diff`, and
`git ls-files --others --exclude-standard` to identify the layers. Read the
included untracked files. Inspect the final effective content as well as
layer-specific changes when the request calls for them. Keep local changes
outside a committed-only verdict. Distinguish out-of-scope material from
in-scope bytes you could not inspect. Resolve ambiguous boundaries from the
request and repository; ask when competing boundaries would change the review.
Report an empty diff or unresolved ref before issuing a verdict.

## 2. Establish evidence and review both axes

1. Locate the task, acceptance criteria, existing contracts and applicable
   repository standards. Read the affected tests early. Identify what each
   relevant test actually observes and which bad implementation could pass it.
2. **Spec.** Trace requirements to implementation and tests. Check preserved
   caller behavior, boundaries, failure paths and state transitions. When an
   originating spec is missing, mark feature acceptance unverified and assess
   the behavior supported by existing contracts.
3. **Standards.** Evaluate correctness, readability, architecture, security and
   performance in proportion to the change. Follow affected callers or data
   across boundaries to verify reachability. Use the [checklists](resources/checklists.md)
   for relevant risks and the [guide](GUIDE.md) for structural remedies and
   splitting a review by coherent behavior.
4. Before reporting a candidate issue, check whether a caller, guard, contract
   or test already resolves it. Tie it to a changed behavior or a pre-existing
   issue made reachable or materially worse by the change. Distinguish a
   confirmed defect from missing evidence. Name a focused reproduction or
   regression assertion when it would resolve uncertainty or prevent recurrence.

## 3. Report and reconcile

- **Scope.** State the reviewed snapshot and the applicable requirement sources.
- **Findings.** Order by severity and label each with its primary axis. Report
  one finding per root cause and cross-reference the other axis when affected.
  Use a changed `file:line` or nearest available anchor, concrete trigger,
  consequence, supporting evidence, and the smallest practical remedy.
  Say when there are no actionable findings.
- **Axis verdicts.** Give Spec and Standards each a verdict of `PASS`, `FAIL`,
  or `UNVERIFIED`. A confirmed blocker fails its affected axis. A material
  evidence gap without a confirmed blocker leaves the affected axis unverified.
  Overall, use `CHANGES REQUESTED` for blockers, `UNVERIFIED` for remaining
  material gaps, or `NO BLOCKERS FOUND` for completed coverage without blockers.
- **Verification and limits.** Separate tests inspected, checks actually run,
  and results reported by others. Identify any evidence needed for a verdict.
- **Declined to Judge.** Record material exclusions and why they were excluded,
  or state that there were none.

| Prefix | Impact |
| --- | --- |
| `[CRITICAL]` | Blocker involving severe harm such as an exploitable security break or unrecoverable data loss. |
| `[REQUIRED]` | Blocker involving a concrete regression, unmet requirement, or enforceable project rule. |
| `[SUGGESTION]` | Optional improvement with a specific benefit and proportionate remedy. |
| `[NIT]` | Optional cosmetic correction. Cap at three per review. |

## 4. Request or receive review

Use the [agent protocols](resources/agent-review-protocols.md) to hand over
the pinned snapshot or verify feedback. Independent review is conditional on
the applicable delegation contract and authorization. Verify a finding and its
proposed remedy against current code before editing. Give one evidence-backed
pushback on a disputed item, then escalate a persistent dispute.

## Companion resources

- [Deep craft and structural remedies](GUIDE.md)
- [Technical checklists](resources/checklists.md)
- [Review handoff and reception](resources/agent-review-protocols.md)
- [Worked example and verification](resources/worked-example.md)

## Ownership and Provenance
Andino coordinates selection, progress tracking, and durable checkpoints. This skill owns its execution procedure and verification criteria.
Adapted and consolidated from audited snapshot paths:
- `addyosmani/agent-skills:skills/code-review-and-quality/SKILL.md` (MIT, Addy Osmani 2025)
- `addyosmani/agent-skills:references/security-checklist.md` & `performance-checklist.md`
- `mattpocock/skills:skills/engineering/code-review/SKILL.md` (MIT, Matt Pocock 2026)
- `obra/superpowers:skills/requesting-code-review` & `receiving-code-review` (MIT, Jesse Vincent 2025)
Preserved under MIT license terms in [references/license.md](references/license.md).
