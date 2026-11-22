# Open questions

- Skipped stale tests (found 2026-11-22). `tests/test_andino_routing_readiness.py`
  and a few installer tests read the local branch names `andino-workflow` or
  `search-first`. Those branches never exist on CI runners, so the tests always
  skip. When the branches exist, four routing-readiness assertions fail against the
  current andino-workflow pin (for example they still expect
  `skills/decision-interview/GUIDE.md` and the phrase `before Focus`). Decide per
  assertion whether the contract is still wanted, then either update the test to
  the current pin and read `origin/<skill>`, or delete it.
