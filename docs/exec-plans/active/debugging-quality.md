# Debugging skill quality

Branch: andino-workflow. Status: IN_PROGRESS. Phase: execution.

## Decisions and acceptance

- Keep the six-phase investigation, exact-symptom red gate, seam regression, redaction, cleanup and ownership-safe three-fix stop. Use the member entrypoint for the full decision flow and GUIDE for how to apply it. Preserve the executable example and member identity.
- At intake distinguish confirmed causes from unknown causes. In phases 1–2 classify setup errors, use a working comparison and keep the original trigger. For slow and flaky cases record a measurement or failure rate instead of imposing a five-second deadline.
- In phases 3–4 rank plausible causes with predictions that can refute them. Distinguish reversible probes from failed fix attempts. In phases 5–6 report missing seams explicitly and verify the original trigger, regression and affected checks. When exact reproduction remains inaccessible, report the evidence gap and request the smallest missing artifact.
- Align supporting resources and correct the Matt Pocock source URL. The three upstream root LICENSE files identify MIT and match the existing notices.
- Review against three cases: wrong-tenant result versus setup error, slow CI-only repro, and flaky failure with several disproved probes. Check local content and perform latest-source setup into a temporary Codex home after push. Verify installed member and nested guide/resources against the pushed bytes.

## NEXT ACTION

Implement the entrypoint, guide and resource alignment, then verify and publish.

## Result / evidence

- Self-reviewed the three scenarios against the revised phase gates. An import failure cannot satisfy exact symptom RED. Slow CI can retain the original signal. Disproved flaky probes do not consume the three-fix budget. This was a contract walkthrough, not a live model comparison.
- Ran the operational example with default and negative input. Observed exit 0 and 2 respectively.
- Routing test exposed a missing explicit guide-first requirement in the coordinator body. Restored the direct link and ordering there.
- Portfolio validator reported an unexpected file in the existing search-first source. Debugging files are checked separately and latest setup will verify the installed artifact.
