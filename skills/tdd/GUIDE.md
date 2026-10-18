# Test one public behavior before implementing it

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Implement a behavior with a regression guard that demonstrably fails without the change.

## Trigger and non-trigger

Use when: A feature, bug fix or behavior change needs a regression guard, including pasted code.

Do not select for: Pure prose/static content or reversible configuration without behavioral impact.

## Prerequisites

Discover manifests, CI, wrappers and neighboring tests; read glossary/ADRs. Record accepted seam, literal behavior, focused/suite commands. Reuse accepted seams; ask only about an unresolved material interface choice.

## Procedure

1. Choose one public seam and observable behavior. Name a plausible production mutation the test must catch; derive expectations independently from a literal worked case.
2. Write one readable arrange/act/assert test. Run existing code and inspect RED: expected assertion failure, not broken import, syntax or test setup. Repair setup before trusting the failure.
3. Implement only enough to pass this behavior. Run the focused check and inspect GREEN, then take the next vertical slice. Avoid writing all imagined tests before any implementation.
4. Exercise real internal collaborators. Double only slow/external/unsafe/nondeterministic boundaries; understand their side effects and complete response shape. Assert public state, not mock presence or private call sequences.
5. After implementation is GREEN, optional refactoring is a separate review gate. Name observed complexity, inspect callers, preserve seam/outputs/errors/side-effect order and rerun checks after each small change. Stop if behavior or architecture would change.
6. Run project suite and applicable integration/build checks. Report all failures including baseline ones. Reuse unchanged valid evidence instead of ceremonial repeats.

## Ownership

Andino owns selection, depth, scope, the existing durable checkpoint, delegation and DONE. Parent owns shared artifacts/final acceptance. This guide cannot invoke denied/manual siblings or establish another lifecycle.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

Accepted seam, literal contract, intended RED output, minimal GREEN change, mutation sensitivity, suite result and separate refactor decision.

## Verification

Observe intended assertion fail then pass; faulty-copy mutation must fail again. Refactor passes unchanged behavioral tests.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "red_source": "def total(values):\n    return 0\n",
  "green_source": "def total(values):\n    result = 0\n    for value in values:\n        result += value\n    return result\n",
  "refactor_source": "def total(values):\n    return sum(values)\n",
  "test_source": "import unittest\nfrom subject import total\nclass Contract(unittest.TestCase):\n    def test_known_invoice(self):\n        self.assertEqual(total([10, 5]), 15)\n",
  "expected_failure": "0 != 15",
  "oracle": 15,
  "refactor_reason": "Review removes accumulator bookkeeping while preserving the public list-of-integers contract"
}
```

Anti-pattern: Computing expected via the implementation, matching source tokens as behavior proof, deleting user code for process violations or redesigning architecture inside a fix.

## Fallback

If no suitable seam reaches the real bug pattern, document the architecture gap and bounded repro; do not claim a shallow test provides protection.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- addyosmani/agent-skills:skills/test-driven-development/SKILL.md
- mattpocock/skills:skills/engineering/tdd/SKILL.md
- mattpocock/skills:skills/engineering/tdd/tests.md
- mattpocock/skills:skills/engineering/tdd/mocking.md
- obra/superpowers:skills/test-driven-development/SKILL.md
- obra/superpowers:skills/test-driven-development/writing-good-tests.md

- addyosmani/agent-skills:references/testing-patterns.md

- addyosmani/agent-skills:agents/test-engineer.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
