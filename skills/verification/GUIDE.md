# Prove claims against the current result

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Bind each status claim to actual complete observations and tested state.

## Trigger and non-trigger

Use when: About to report fixed/passing/complete or accept worker output.

Do not select for: No change/claim needing proof; do not rerun unchanged checks ritualistically.

## Prerequisites

Map claim/current artifact to accepted criteria and existing valid evidence.

## Procedure

1. Map claims to proving observation: regression, suite, build, lint, security, interaction or review. Lint cannot prove build/user flow.
2. Pin relevant bytes/state and run missing/stale checks with native commands. Capture command/environment/exit/result and safe log location.
3. Read relevant output and named baseline failures. Zero exit with no cases or skipped scope is not success; distinguish failed/passed/not checked.
4. Test regression sensitivity using isolated faulty copy/mutation. Inspect actual delegated changes and integration evidence, not only self-report.
5. Invalidate affected evidence after bytes/state change. Reuse unaffected evidence; broaden checks only for new risk/failure.
6. Report exact scope/results/limits. Lists of test names or requirements are indexes, not proof.

## Ownership

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-verification` and this guide expose one method, without recursive workflow invocation.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

Claim→criterion→command/action→result→tested identity with gaps.

## Verification

Evidence must match current state/scope; unit pass cannot prove live host or authorize deployment.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "source": "def answer():\n    return 15\n",
  "test": "import unittest\nfrom subject import answer\nclass Contract(unittest.TestCase):\n    def test_answer(self):\n        self.assertEqual(answer(),15)\n",
  "changed_source": "def answer():\n    return 16\n",
  "criterion": "public answer returns 15"
}
```

Anti-pattern: Should pass, worker said done, old-tree green, headings as model-behavior proof.

## Fallback

Unavailable required capability remains exact not-verified criterion; continue possible checks without unauthorized installation.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- obra/superpowers:skills/verification-before-completion/SKILL.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
