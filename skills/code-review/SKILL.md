---
name: andino-code-review
description: Review PR, branch, WIP/untracked changes, pasted diff or completed feature. Operates under Andino Workflow governance.
---

# Review the current diff on two independent axes

Internal method ID: `andino-code-review` (alias: `code-review`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Assess spec behavior and documented standards separately, with risk-sensitive quality review.

## Trigger and non-trigger

Use when: Review PR, branch, WIP/untracked changes, pasted diff or completed feature.

Do not select for: Conceptual question with no change or unrequested cosmetic nit hunt.

## Prerequisites

Resolve requested baseline/accepted task BASE. Capture staged/unstaged/owned untracked bytes; read spec, standards and tests.

## Procedure

1. Pin immutable review scope including relevant committed range plus actual working diff and owned new files. Record exact bytes/line locations. HEAD-only or HEAD~1 can omit the work.
2. Read tests first; name behavior, independent oracle and plausible mutation. Mutate a disposable copy and observe regression failure; restore the copy, preserving user files.
3. Spec axis maps each requirement to behavior and reports missing/partial/wrong behavior or scope additions with requirement and file:line evidence. Missing spec means not verified.
4. Standards axis checks local documented rules and distinguishes hard violations from heuristic smells. Inspect correctness, naming/locality/concept count, boundary types, security and measured performance as relevant.
5. Preserve both verdicts. Grade findings by user effect; name exact trigger, consequence, location, evidence and concrete remedy. Repo rules override generic tastes; do not repeat tooling's formatter output.
6. Verify feedback against current code/usages/compatibility before changing it. Fix material issues with covering tests and scoped re-review; record reasoned disagreement. Andino owns acceptance; review grants no merge/publish authority.

## Ownership

Andino owns selection, depth, scope, the existing durable checkpoint, delegation and DONE. Parent owns shared artifacts/final acceptance. This guide cannot invoke denied/manual siblings or establish another lifecycle.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

Scope snapshot, tested identity, separate Spec/Standards verdicts, prioritized findings, mutation result, actual checks and limitations.

## Verification

Planted boundary bug fails Spec while an independent explicit security rule fails Standards. Byte drift invalidates affected verdicts.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "base_source": "def spend(balance, amount):\n    return balance - amount\n",
  "candidate_source": "def spend(balance, amount):\n    amount = eval(str(amount))\n    if amount >= balance:\n        return None\n    return balance - amount\n",
  "fixed_source": "def spend(balance, amount):\n    if amount > balance:\n        return None\n    return balance - amount\n",
  "test_source": "import unittest\nfrom subject import spend\nclass Contract(unittest.TestCase):\n    def test_exact_balance_allowed(self):\n        self.assertEqual(spend(10, 10), 0)\n",
  "spec": "Spending the entire balance is permitted and returns zero.",
  "standards": "Dynamic eval of input is prohibited.",
  "expected_spec_line": 3,
  "expected_standards_line": 2,
  "untracked": {
    "helper.py": "VALUE = 7\n"
  }
}
```

Anti-pattern: Mandatory praise, arbitrary tastes as hard standards, hiding untracked files, merging away a failed axis or nested duplicate reviewers.

## Fallback

Without a reviewer tool make a separate self-review pass and disclose limits. Missing spec or live environment stays explicitly not verified.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- addyosmani/agent-skills:skills/code-review-and-quality/SKILL.md
- addyosmani/agent-skills:references/security-checklist.md
- addyosmani/agent-skills:references/performance-checklist.md
- mattpocock/skills:skills/engineering/code-review/SKILL.md
- obra/superpowers:skills/requesting-code-review/SKILL.md
- obra/superpowers:skills/receiving-code-review/SKILL.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
