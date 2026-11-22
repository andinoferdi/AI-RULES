# Doubt-driven development quality

Status: DONE
Depth: STANDARD
Current phase: Delivery

## Executive snapshot

Baseline workflow revision `8ecb810`. The upstream skill separates claim,
packet, adversarial review, reconciliation and stop into explicit steps. The
Andino member preserves those concepts in six dense bullets, with an offline
example that exercises fixed classifications but never challenges an artifact.

## Objective and acceptance

- Preserve the installed ID, Andino ownership, authorization, degraded mode,
  classification precedence, three-cycle limit and unchanged-input guard.
- Make the counterexample, verification and resulting readiness visible for
  material claims. Mechanical work should exit without a review.
- Publish the workflow and bundled pin. Compare native and nested copies from
  both real setup sources to the workflow source in disposable Codex projects.

## Execution board

| Task | Status | Readiness |
| --- | --- | --- |
| Audit and scenario walkthrough | DONE | Baseline and upstream inspected |
| T1 Member procedure and example | DONE | Both entrypoints, relative links, fixture variants and retry outcomes verified |
| T2 Workflow publication and setup | DONE | Workflow `8ba73c4`, bundled pin `1af1734`, 16 exact installed-file comparisons |

## Baseline and decision

No historical failure was supplied. In a manual unguided retry walkthrough, a
payment can succeed before the completion record is written. A timeout or crash
at that point makes a retry charge twice. Reporting only that risk omits the
test seam, the scope of any passing check and whether the decision may stand.
The current skill asks for dispositions and exact commands but supplies no
finding template or worked claim-to-verification example. Upstream gives a
review prompt and stronger step boundaries but leaves the report shape open.
A mechanical rename bypasses both procedures. In a lease-based design,
acquisition alone cannot prove a stale owner cannot write after expiry.
These are manual walkthroughs, with no isolated model samples.

Keep the member layout and borrow the upstream step boundaries. Prefer a
compact reviewer and output contract plus one grounded worked example over
copying the upstream cross-model solicitation or adding review layers.

## Detailed execution

### T1 — Member procedure and example

Owns `skills/doubt-driven-development/{SKILL,GUIDE}.md` and the existing
`resources/review-perspectives.md`. Replace the six Procedure bullets with
five ordered stages named Claim, Extract, Challenge, Reconcile and Stop.
Require a falsifiable predicate and consequence, a packet with artifact and
contract plus relevant counterevidence, and a finding with location, trigger,
violated condition, impact and a disproof check. Choose the cheapest adequate
authorized evidence. Record one of SUPPORTED, REFUTED or UNVERIFIED and bound
it to exercised cases. Keep the optional CLI safeguards. Add a retry example
in the existing resource and retain the manifest-backed executable block.
Verify both member bodies match, links resolve, whitespace passes and both
existing fixture variants produce their documented outputs. Exercise the
worked example with a fake provider and test the uncovered failure boundary.

### T2 — Workflow publication and setup

Push the owned workflow changes to `andino-workflow`. In an isolated checkout
of `origin/main`, advance the workflow SHA and release metadata in
`src/ai_rules/release/data/release_manifest.json` following `d6aa6fa`.
Leave the existing main checkout edits intact. Run actual project-scope
`ai-rules setup --host codex --capability andino-workflow --source latest`
and the bundled equivalent from the updated main source. Compare the four
skill files in both installed copies for both sources. Push the verified pin.

## NEXT ACTION

None. Delivery complete.

## Verification evidence

Local Python checks compared both member bodies, resolved Markdown links and
ran both manifest-backed example variants against their exact expected JSON.
A fake provider produced 2, 1 and 2 charges for an unkeyed retry, a keyed
retry within the window and a keyed retry at expiry. The scoped self-review
found the installation ID, delegation boundary and stop policies preserved.
`git diff --check` passed. This verifies the example and authored contract.
Comparative model-output quality was not measured.

Both project-scope setup sources installed all three planned Codex
capabilities with zero failed, blocked or unfinished targets. The four skill
files matched the published Git objects byte for byte in the native and
nested copies for both sources. Native discovery in a new session was not
tested. The separate main checkout's existing edits were excluded.
