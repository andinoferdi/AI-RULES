# Prove claims against the current result

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Bind each status claim to actual complete observations and tested state.

## Trigger and non-trigger

Use when: About to claim success, accept delegated work, hand off a completed task, or deliver verified work.

Do not select for: No change/claim needing proof; do not rerun unchanged checks ritualistically.

## Prerequisites

Map claim/current artifact to accepted criteria and existing valid evidence.

## Procedure

**Require current proof for every success claim.** Apply this gate before reporting
success, accepting delegated work, handing off a completed task, or taking an
authorized delivery action. Apply it again to claims about the delivery result.

1. **Choose proof.** Name the claim, its acceptance criterion, and the command
   or observation that could establish it. For task completion, cover each
   required criterion. For delegated work, inspect the actual diff and verify
   the integrated result. For regression sensitivity, confirm the expected
   failure in an isolated faulty copy and the pass with the fix.
2. **Check currency.** Identify the artifact, inputs, environment, and scope
   the evidence covers. Reuse a prior result when those conditions and any
   required freshness window still match. Rerun affected checks when they
   change or cannot be established.
3. **Run and read.** Execute the complete check for the intended scope. Inspect
   the exit status, exercised cases, assertions, failures, and skips. A zero
   exit with no relevant cases leaves the claim unverified. Name any observed
   baseline failures and show the comparison that establishes them.
4. **Decide and report.** If the observation proves the criterion, report the
   supported scope and result. If it fails, report the observed failure. If
   evidence is missing, partial, or unavailable, state the exact unverified
   scope and what would establish it. Withhold completion while any required
   criterion lacks passing evidence.

Record the command or action, working environment, tested identity, outcome,
and relevant exclusions. See the supporting contract for claim-specific checks.

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

MIT attribution/notices are preserved in package legal references ([references/license.md](references/license.md)). No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
