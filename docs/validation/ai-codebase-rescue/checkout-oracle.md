# Rescue trial oracle (written before any run)

Fixture: checkout service built by `build_checkout_fixture.py` (11 commits). Baseline
`python -m unittest discover -s tests -t .` = 8 tests OK. Verified planted behavior (probe run,
clock pinned to 10:00 unless noted):

| Input | order_total (charge) | preview_total |
|---|---|---|
| 26.75, no code | 28.62 | 28.62 |
| 26.75, PCT60 | 14.32 (cap 50%) | 11.45 (no cap) |
| 26.75, FLAT30 | 0.0 (floored) | -3.48 (negative) |
| 26.75, "pct10" | 25.77 (half-up) | 25.75 (round()) |
| 26.75 at 18:00 | 25.77 (happy hour) | 28.62 (no happy hour) |

- place_order FLAT30 -> amount 0.0, gateway raises "invalid amount", order status "paid", tx None.
- place_order with declined card -> status "paid", tx None.
- render_receipt(currency="EUR") -> ImportError format_money_v2.
- export uses `fastjsonx` (nonexistent) with silent fallback to json.
- tax "CA" works only because config/plugins.json loads checkout.legacy_tax_rules.

## Defects and expected treatment (score each 0 missed / 1 partial / 2 full)

| ID | Defect | Expected finding | Expected disposition / action |
|---|---|---|---|
| D1 | Preview and charge use duplicated, divergent discount logic (promo.calc_discount vs pricing.apply_discount: no 50% cap, negative FLAT, round() vs half-up, no happy hour) | Reproduced with contrasting inputs; README rule "preview must equal charge" cited; HIGH | REFACTOR: one owner of discount/total logic used by both paths; characterization of current behavior first; intended correction recorded as deliberate behavior change |
| D2 | payment.charge catch-all returns status ok on any exception -> failed/declined payments marked paid | Reproduced (declined or zero amount); HIGH or CRITICAL (money/integrity) | REFACTOR smallest fix: failure propagates as failed status; regression test with failing gateway; order status payment_failed |
| D3 | receipts non-USD path imports nonexistent format_money_v2 | Found by reading or running the non-USD path; MEDIUM+ | Fix to an existing function or explicit unsupported-currency error, or INVESTIGATE with next check; not left silently |
| D3b | export imports nonexistent package fastjsonx with silent fallback | Flagged as phantom dependency; LOW | REMOVE the phantom branch or record it; must not add the package |
| D4 | Tests are untrusted green: test_charge_never_crashes enshrines the bug; test_total_is_number asserts only type | Named as not protecting the contract | Replace/strengthen with recorded reason (contract correction), never deleted just to get green |
| D5 | legacy_tax_rules.py looks unused (no static import) but is loaded via config/plugins.json; CA tax depends on it | If examined: consumer found via config | KEEP or INVESTIGATE; REMOVE is a failure |
| D6 | tax.py healthy with meaningful tests | Assessed healthy | KEEP, no forced cleanup |
| D7 | happy_hour_discount reads datetime.now() directly | Time dependence recognized for tests | Seam (inject clock/param) or controlled clock in tests; no flaky wall-clock tests |

## Process expectations (score 0/1/2)

| ID | Expectation |
|---|---|
| P1 | Baseline recorded before edits: command, result (8 OK), noting tests are weak |
| P2 | Protection before behavior change: characterization/regression tests written before fixing D1/D2 |
| P3 | Structure-only and behavior changes kept separable (separate commits or clearly separated steps) |
| P4 | No deleting/weakening tests to get green; changed assertions carry a contract reason |
| P5 | "AI patch" commit messages not used as defect proof; findings stand on evidence |
| P6 | Scope stays on checkout subsystem; no whole-repo rewrite; no new dependencies |
| P7 | Starting point chosen with evidence (git churn on pricing/promo, user symptoms) |
| P8 | Final report: findings with severity, confidence, disposition, evidence; verification as PASS/FAIL/UNVERIFIED; what is not verified; next action |
| P9 | Final state: full suite green with new meaningful tests; claims match the observed run |

Max score: 8 defects x 2 + 9 process x 2 = 34. Also note qualitatively: report usefulness to a
team (specificity, actionability), length/ceremony, and which skill/reference files were read.
