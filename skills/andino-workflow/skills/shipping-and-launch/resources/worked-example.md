# Four releases from request to record

Hypothetical services, people and numbers; they illustrate the procedure, not a real system.

## 1. Routine flag: READY for 5% only

Request from Ana (release owner): "Can `r42` with the new invoice filters go out this week?"

- Size: Standard. New behaviour behind `invoice_filters`; no schema or data change.
- Authority: review and prepare. Ana enables flags; nobody asked the agent to deploy.
- Evidence: the agent ran the suite (212 passed, 0 skipped) and read CI: the filter end-to-end
  test ran on staging with `r42`. Release checklist rows for build, security (no new
  dependencies, the filter endpoint validates its query), performance (p95 of `/invoices` 180 ms
  on staging against 175 ms for `r41`) and accessibility (filter controls reachable by keyboard,
  labelled) all PASS. Production health and the cohort dashboard were checked with the flag off.
- Recovery: the flag is evaluated per request; turning it off takes under a minute. `r41` reads
  the same schema.

```text
Decision: READY for stage 2 (5%) for r42 -> production
Size: Standard because new behaviour behind a flag, no schema change
Candidate: r42 (commit 9b2e771); production: r41; changes: invoice filters UI and endpoint
Authority: Ana enables flags and deploys; found in files and not followed: none
Evidence: build PASS; tests 212/0 skipped (run by me); staging e2e PASS on r42;
  security PASS; p95 /invoices 180 ms vs 175 ms PASS; keyboard and labels PASS
Blockers and what makes it ready: none
Stages:
  | Stage | Cohort | Min window | Min volume | Signals vs control and thresholds | Observer | Decision at end |
  | 0 Dark | flag off | 1 h | normal | health r42, 5xx/p95 = r41 | Ana | Ana opens 1 |
  | 1 Internal | staff | 1 working day | 50 filter uses | no failures, no new client errors | Ana | Ana |
  | 2 Canary | 5% | 24 h incl. Tue peak | 1,000 requests | 5xx <=1.1x; p95 <=+20%; new client error <=0.1%; invoice views down <1% | Ana | Ana |
  | 3-5 | 25/50/100% | 24 h each, 1 week at 100% | 1,000 | same | Ana | Ana |
Rollback: triggers stop thresholds or user reports; actions flag off (Ana, <1 min), redeploy
  r41 (Ana, 6 min, schema unchanged); data none written; verification 5xx and p95 back to
  control, filters gone for the cohort; escalation Ana's lead
Monitoring: cohort dashboard "invoices-r42"; first hour: health r42, no new error types,
  filter journey by hand, logs flowing
Flag: invoice_filters, default off, owner Ana, removal by 2026-12-18, under 1 min to turn off
Done by me: test run, staging and dashboard checks
NOT EXECUTED: enabling stages -> Ana -> open stage 1 Monday 09:00
Not verified: client error rates on the real cohort (no traffic yet)
Next action: open stage 0 - Ana - Monday 09:00
```

## 2. A canary whose dashboard is green: STOP

Request from Bayu: "Checkout v7 has been at 5% for an hour, the dashboard is green. Go to 25%?"
The agent is on call; the release policy lets on-call set a flag to 0% without asking and
reserves redeploys for the release owner.

- Size: Live decision.
- Evidence over the same hour: candidate 24 errors in 2,000 requests (1.2%), control 20 in
  10,000 (0.2%): 6x, above the 2x stop line. p95 +9% (advance band). Checkout completion 71.0%
  against 72.1% (down 1.5%, hold band). The all-traffic dashboard shows 0.37%, under its alert.
- Decision: STOP, the error ratio decides. Expanding is out of the question.
- Action: the agent sets `checkout_v7` to 0%, then re-observes: candidate traffic 0, errors at
  0.2%, checkout by hand works. 41 orders were placed through the new flow; they stay as they
  are. 18 failed checkouts are listed for support.
- NOT EXECUTED: redeploying v6, owner Bayu, not needed while the flag is at 0%.
- Next action: the payments team finds the error source; the canary restarts at 5% with a full
  window and volume after a fix, not at 25%.

If the hour had produced only 300 candidate requests and no stop breach, the decision would be
HOLD at 5% with the time of the next look and the volume needed.

## 3. A destructive migration: NO-GO for the drop

Candidate `r44` drops `users.legacy_plan`, which `r43` still reads. A nightly backup exists;
restoring it has never been tried and nobody knows how long it takes.

- Size: High risk.
- Problem: once the drop runs, redeploying `r43` fails, and a code revert cannot bring the
  column back. Writes after the drop would be lost by a restore.
- Decision: NO-GO for the drop. READY for an expand release once its gates pass.
- Plan: `r44` stops reading `legacy_plan` and ships without the drop (expand and migrate).
  After `r44` runs everywhere for a week and a restore test has run and been timed, `r45`
  drops the column (contract), with the restore time in its rollback plan.

## 4. A two-line text fix: short form

Request from Rina: "I corrected the support phone number on the contact page and a broken
footer link; what do we need before production?"

- Size: Small. The diff touches two lines of content and nothing else.
- The agent ran the build and the tests (all pass, link check included) and checked the built
  contact page shows the new number and the footer link resolves.

Reply:

> You can publish it. I checked that the commit only changes those two lines, the build and the
> tests pass, and the built contact page shows the new number with a working footer link.
> Publish with `npm run publish`, then open the contact page to check. If anything looks wrong,
> `npm run publish -- --rollback` restores the previous build. I did not publish it.

No flag, stages or watch windows: they would cost more than the change risks.

Provenance: cases 1 to 3 extend the worked cases of the earlier Andino skill; the structure
follows Addy Osmani's `shipping-and-launch` (addyosmani/agent-skills 3d78ead, MIT). Full notice in
[../references/license.md](../references/license.md).
