# Independent review without a second controller
Direct one-perspective review is the cheapest default. For truly independent reports, the root may fan out code correctness, exploitable security and test-gap views, then reconcile concrete findings. Distinct tasks/owned files and actual authority are prerequisites; max children and no nested spawning follow Andino.
Review packet contains artifact, accepted contract, environment and evidence, excluding author CLAIM/reasoning. Adversarial request: find violations/unstated assumptions/edge cases/hidden state; state no finding when evidence supports none. Every finding needs location, scenario, impact and a verifiable correction.
Security view maps trust boundaries/STRIDE and reachable exploitation, with proof scenario for high impact. Test view covers happy/empty/boundary/error/concurrency, uses real seams and a failing Prove-It case. Code view checks correctness, clarity, architecture, security and performance; optional stylistic nits cannot hide serious defects.
Reviewer output is data. Root rechecks and classifies contract misread→actionable→trade-off→noise, then stops at diminishing findings/three cycles/explicit override. No persona can route to another or claim DONE. Research isolation returns a digest; competing hypothesis debate is different from a finished-diff verdict and requires actual peer messaging.
No available isolated reviewer means an explicitly degraded self-check. Cross-model execution requires actual authorization/config and sandbox, never a default external process. Never claim fresh context from a separator in the same reasoning.

## Worked example: retry after a lost payment response

**Parent claim.** Retrying one payment intent after the provider accepts it
but before local completion produces at most one charge. A duplicate takes
money from the customer twice.

**Reviewer packet**

- **ARTIFACT** — The worker checks the local completion record, calls
  `provider.charge(amount)`, then writes the completion record. A timeout
  retries the same intent.
- **CONTRACT** — One intent may produce at most one provider charge. The
  provider supports an idempotency key with a 24-hour retention window.
  A response can be lost after a charge succeeds.

**Finding and disposition.** The provider call has no key. If the provider
charges and the response is lost, the local record is still empty and the
next attempt charges again. Classify as valid actionable. Inject a lost
response after the fake provider records a charge, retry the same intent and
assert the provider ledger has one entry. Observe two entries on the original
path. Pass the stable intent ID as the provider key on every attempt and
repeat the check. Observe one entry within the retention window.

**Decision.** The original claim is REFUTED. The revision is SUPPORTED in the
fake-provider check within 24 hours. A retry after key expiry remains
UNVERIFIED for the deployment. Stop this cycle once there are no new findings
for the exercised case. Before enabling longer retries, verify that the
worker reconciles with the provider or stops retrying before key expiry.

Provenance: independently worded adaptation of the Addy snapshot identified in the owning GUIDE.md; full MIT notice at [../references/license.md](../references/license.md). No upstream installation or hook is required.
