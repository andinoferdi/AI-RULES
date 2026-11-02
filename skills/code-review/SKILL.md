---
name: andino-code-review
description: Comprehensive bidirectional 2-axis code review evaluating Spec requirements and Standards quality independently. Operates under Andino Workflow governance.
---

# Code Review: Dual-Axis Quality Engine

Internal method ID: `andino-code-review` (alias: `code-review`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, and single durable checkpoints.
> Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

```
                    ┌───────────────────────────────┐
                    │  PIN SCOPE: BASE..HEAD + W.T. │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │      INSPECT TESTS FIRST      │
                    └───────┬───────────────┬───────┘
                            │               │
       ┌────────────────────▼─────┐   ┌─────▼────────────────────┐
       │     AXIS 1: SPEC TRACK   │   │  AXIS 2: STANDARDS TRACK │
       │ Requirements, Edges,     │   │ Security, Fowler Smells, │
       │ Boundary Oracles, State  │   │ Perf, Architecture, Style│
       └────────────────────┬─────┘   └─────┬────────────────────┘
                            │               │
                            └───────┬───────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │ GRADE: [CRITICAL] [REQUIRED]  │
                    │        [SUGGESTION] [NIT]     │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │ 1-CYCLE VERIFY / ANTI-DEADLOCK│
                    └───────────────────────────────┘
```

## Trigger and Non-Trigger
- **Use when:** Reviewing pull requests, feature branches, WIP diffs, uncommitted working tree changes, or verifying subagent task handoffs.
- **Do not select for:** Conceptual questions with no code diff, or unrequested cosmetic nit hunts on unedited code.

## Prerequisites & Scope Pinning
Resolve baseline commit (`BASE_SHA=$(git merge-base origin/main HEAD)`) and head commit (`HEAD_SHA=$(git rev-parse HEAD)`). Capture staged, unstaged, and owned untracked files. A review of `HEAD~1..HEAD` alone that omits working tree bytes is invalid.

## Operational Procedure
1. **Pin Scope & State:** Record immutable byte boundary (`BASE..HEAD` + untracked files). Log out-of-scope files in the mandatory "Declined to Judge" ledger.
2. **Read Tests First:** Examine existing and added tests. Identify the behavioral contract, independent oracle, and plausible mutation points.
3. **Execute Spec Axis:** Map every acceptance requirement to implementation logic. Report missing, partial, or inverted behaviors citing exact `file:line` locations and failure inputs. Spec silence does not waive user invariants.
4. **Execute Standards Axis:** Inspect code against local standards and the 5 quality dimensions (Correctness, Readability, Architecture, Security, Performance). Audit against `resources/checklists.md` and map design smells to named structural remedies.
5. **Grade Findings & Formulate Remedies:** Categorize comments using explicit prefixes: `[CRITICAL]` and `[REQUIRED]` (blockers), `[SUGGESTION]` and `[NIT]` (non-blocking, max 3 nits/pass). Pair every defect with an explicit structural remedy.
6. **Enforce 1-Cycle Reception Guard:** The author must verify findings before implementing. If a finding is inaccurate, the author issues exactly one technical pushback with evidence. If disputes persist, escalate to user/coordinator—never loop in multi-turn debate.

## Rationalization Refutation Table
| Common Agent Excuse | Reality & Operating Invariant |
|---|---|
| *"The diff is small, so I can skip the Spec Axis."* | Small diffs often introduce critical boundary regressions. Run both axes without exception. |
| *"I'll review HEAD~1 instead of checking untracked files."* | New features often contain uncommitted files. Pinning working tree and untracked files is mandatory. |
| *"The code is clean, so the requirements must be met."* | Clean, elegant code frequently implements the wrong requirement. Keep the two axes strictly isolated. |
| *"I will implement all reviewer suggestions immediately."* | Performative sycophancy. Verify every comment against codebase reality before touching code. |
| *"I'll debate the reviewer until they agree with me."* | Reception deadlock. Limit technical pushbacks to 1 cycle backed by test evidence, then escalate. |
| *"I will add a generic plugin registry just in case."* | YAGNI violation. Reject speculative generality unless three distinct consumers already exist. |
| *"I'll leave dead code in case we need it later."* | Dead code degrades context. Flag orphaned functions and obsolete compatibility shims for deletion. |

## Diagnostic Red Flags
1. Review approved without inspecting tests or formulating mutation oracles.
2. Spec and Standards verdicts conflated into a single unstructured comment block.
3. Critical security or correctness findings softened into optional suggestions.
4. Reviewer mutating files or switching git branches during review (violating read-only boundary).
5. Untracked files omitted from review scope snapshot.
6. Reviewer providing vague critique ("this is messy") without a Named Structural Remedy.
7. Author submitting performative sycophantic praise ("You're absolutely right!").
8. Author and reviewer looping across multiple cycles debating aesthetic preferences.
9. Cosmetic nits exceeding 3 items, overwhelming author attention.
10. Large diff ($>400$ lines) reviewed without suggesting decomposition strategies.

## Companion Resources
- **Deep Craft Manual:** Read [GUIDE.md](GUIDE.md) for change sizing, splitting strategies, the 12 Fowler smells catalog, and dispute hierarchies.
- **Technical Checklists:** Read [resources/checklists.md](resources/checklists.md) for STRIDE threat modeling, path containment, SQL injection, and database indexing.
- **Agent Protocols:** Read [resources/agent-review-protocols.md](resources/agent-review-protocols.md) for subagent dispatch templates, "Spec is a vision document", and anti-sycophantic receiving rules.
- **Worked Example & Verification:** Read [resources/worked-example.md](resources/worked-example.md) for end-to-end pull request walkthroughs and zero-dependency Python verification suite.

## Ownership and Provenance
Andino coordinates selection, progress tracking, and durable checkpoints. This skill owns its execution procedure and verification criteria.
Adapted and consolidated from audited snapshot paths:
- `addyosmani/agent-skills:skills/code-review-and-quality/SKILL.md` (MIT, Addy Osmani 2025)
- `addyosmani/agent-skills:references/security-checklist.md` & `performance-checklist.md`
- `mattpocock/skills:skills/engineering/code-review/SKILL.md` (MIT, Matt Pocock 2026)
- `obra/superpowers:skills/requesting-code-review` & `receiving-code-review` (MIT, Jesse Vincent 2025)
Preserved under MIT license terms in [references/license.md](references/license.md).
