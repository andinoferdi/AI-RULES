# Evidence and findings

Use when assessing a candidate finding, choosing a disposition or returning
verification evidence to Andino. Keep findings in the existing shared plan or its
already-established evidence artifacts, not a second rescue state store.

## Evidence quality and claim discipline

Prefer evidence in this order, while checking that it applies to the current target:

1. Reproducible behavior or a deterministic failing test.
2. Runtime trace, measured baseline or a safe security proof.
3. A source/config path tied to a known contract and reachable consumer.
4. Corroborating static signals.
5. Historical user/agent summaries.
6. Intuition or style smells, which are investigation leads only.

Record the path/symbol or artifact, relevant environment/input, method and actual
result. Separate observation, expected invariant and causal hypothesis. A passing
test that never exercises the affected contract is not regression proof. Lack of
reproduction does not erase strong source-path proof, but constrain the impact claim
to what that proof supports. Mark conflicting or missing evidence explicitly.

Do not delete, skip or weaken failing tests to obtain green results. Change an
expectation only when a verified contract correction justifies it, with the reason
recorded. Do not hide errors behind catch-all handlers, fabricated output or
unmeasured fallback paths. Separate pre-existing failures from new failures.
Unexecuted checks are unverified, not passing. Claims of faster, safer or fixed
behavior require corresponding measurements, boundary evidence or regression proof.
Redact secrets and sensitive data from evidence; use safe fixtures where possible.

## Severity is impact, not strategy

| Severity | Evidence-supported impact | Effect within authorized scope |
| --- | --- | --- |
| CRITICAL | Sensitive access bypass, meaningful secret exposure, irreversible/widespread data loss, unsafe destruction or broad severe production impact. | Stop lower-priority cleanup; prioritize safe containment and remediation. |
| HIGH | Important flow materially wrong, significant security weakness, repeatable reliability failure, major critical-path degradation or serious outage risk. | Resolve before rescue completion/release or record explicit owner risk acceptance. |
| MEDIUM | Bounded defect, meaningful architectural regression risk, important coverage gap or divergent duplicated behavior. | Repair in scope or record deliberate deferral and residual risk. |
| LOW | Concrete limited-impact defect, proven minor dead code or clarity problem with actual maintenance consequences. | Do not expand scope merely to clear it. |

Severity cannot be inferred from line count, aesthetics, authorship, or how much
code a proposed fix replaces. Healthy KEEP areas need no fabricated defect severity;
record them as assessed areas rather than forcing them into a defect report.

## Confidence is strength of proof

- **HIGH:** reproduced, directly demonstrated by test/trace/runtime evidence, or
  strong source-path proof tied to a known contract.
- **MEDIUM:** strong code/config evidence with incomplete reproduction or impact proof.
- **LOW:** heuristic, smell or incomplete hypothesis.

LOW confidence alone never justifies destructive removal or replacement. Choose
INVESTIGATE where the uncertainty prevents safe mutation, and name the exact next
check. A plausible severe risk can merit urgent investigation without pretending
its cause or full impact is confirmed.

## Finding contract

For each material finding, provide these fields; use an explicit unknown rather
than inventing facts. Aggregate findings only when their evidence and scope align.

```text
ID: RSC-001 (unique within the ticket)
Category:
Severity: CRITICAL | HIGH | MEDIUM | LOW
Confidence: HIGH | MEDIUM | LOW
Affected Area:
Evidence:
Observed Behavior:
Expected Behavior / Invariant:
Impact:
Recommended Disposition: KEEP | REFACTOR | REMAKE | REMOVE | INVESTIGATE
Remediation Scope:
Verification Method:
Dependencies / Blockers: optional
Provenance Context: optional, never defect proof
```

Scope names the files/modules and relevant integrations plus excluded boundaries.
Verification names the observable outcome and how it will be checked, not just
"run tests". After action, append actual changes, check results, deviations and
residual risk; do not silently rewrite the original observation as a success.
For INVESTIGATE, identify the artifact or question to inspect, the concrete action,
and the evidence needed to choose a disposition. Return that recommendation to
Andino rather than assigning a competing authoritative NEXT ACTION.

## AI provenance stays separate

When relevant, provenance may be CONFIRMED (direct user/session/generated-origin
evidence), INDICATED (credible but inconclusive history), UNKNOWN or IRRELEVANT.
Record the basis; generic Git metadata or code style alone does not prove AI origin.
Do not invent AI-detection percentages or infer author competence.

Provenance may guide inspection of a recent change cluster, session artifacts,
out-of-scope edits or suspected invented dependencies/APIs. It cannot determine
correctness, severity, security, maintainability, REMOVE or REMAKE. Verify the
engineering concern independently. Apply the same standard to human-written code.

**Deletion test:** remove the provenance field mentally. If the remediation finding
no longer stands on its evidence, reject it. Verified healthy AI-assisted code can
remain KEEP; missing verification calls for bounded investigation, not a rewrite.

## Compact return packet

Return only decision-relevant evidence: eligibility and scope, baseline and trust,
findings/dispositions, preserved contracts, protection and gate results, actual
implementation and verification, deferred risks and the next evidence action.
Link existing artifacts instead of copying full logs. This packet is a projection
for the Andino plan, not a new plan, lifecycle or independent completion verdict.
