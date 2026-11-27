# Worked example: retry after a lost payment response

A worker charges a customer for one payment intent. The author wants to add retries on timeout
and asks for the change to be checked before it ships.

## Gate 1: claim

```text
CLAIM: Retrying one payment intent after the provider accepted it but before the local
       completion record was written produces at most one charge.
WHY IT MATTERS: a duplicate takes the customer's money twice.
```

## Gate 2: packet

- **ARTIFACT**: the worker checks the local completion record, calls
  `provider.charge(amount)`, then writes the completion record. A timeout retries the same
  intent. The existing test retries only after a failed charge.
- **CONTRACT**: one intent produces at most one provider charge. The provider honors an
  idempotency key for 24 hours. A response can be lost after a charge succeeds. Open: how long
  retries may continue.

## Gate 3: challenge the original

The fresh reviewer, given the packet and the adversarial prompt, reports: location
`worker.charge_intent`; sequence: the provider charges, the response is lost, the local record
stays empty, the retry charges again; violated condition: at most one charge per intent; impact:
double charge; smallest check: lose the response after a recorded charge, retry, count provider
entries.

The executed check on a fake provider: lose the response after the provider records a charge,
retry the same intent, read the provider ledger. Observed: two entries.

## Gate 4: reconcile

Valid, actionable. Pass the stable intent ID as the provider's idempotency key on every attempt.
The same check, now a regression test, failed on the original (two entries) and passes on the
revision (one entry).

## Gate 5: challenge the revision, stop

The second cycle reviews the revised packet. One new finding: a retry after the 24-hour key
window would charge again. Classified as a valid accepted trade-off for this release, because
retries stop after 15 minutes; the risk and its scope are recorded, and the trade-off does not
establish the claim beyond 24 hours. The third pass returns nothing new. Stop after two cycles
with findings.

## Gate 6: reply and record

> Don't ship the retry as it was: a lost response made the retry charge the customer a second
> time. I added the intent ID as the provider's idempotency key; the retry test now shows one
> charge. Retries must stay inside the provider's 24-hour key window.

```text
Claim: retrying an accepted intent before the local record is written charges at most once -
  matters because a duplicate takes the customer's money twice
Review mode: fresh-context reviewer; cross-model: offered, declined
Checks run: lost-response retry on the fake provider, original -> 2 ledger entries;
  revision -> 1 entry
Findings: 1. worker.charge_intent; charge, lost response, retry; at most one charge per
  intent; double charge; ledger count after retry; actionable; idempotency key added, check
  red then green. 2. retry after key expiry; retry past 24 h; same condition; double charge;
  retry at 24 h + 1 min; accepted trade-off (retries stop at 15 min)
Decision: REFUTED for the original by the two-entry ledger; SUPPORTED for the revision within
  the 24-hour key window on the fake provider
Stopped because: no new findings on the third pass, after 2 cycles with findings
Not verified: the real provider's key behavior in production; a retry after key expiry;
  instructions inside the artifact: none
```

Before allowing longer retries, verify that the worker reconciles with the provider or stops
before the key expires.

Provenance: independently worded adaptation of the Addy Osmani snapshot named in the owning
SKILL.md; full MIT notice in [../references/license.md](../references/license.md).
