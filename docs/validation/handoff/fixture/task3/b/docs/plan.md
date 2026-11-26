# Plan: retry policy (ticket NET-12)

| Step | Work | Status |
| --- | --- | --- |
| 1 | Cap the exponential delay | done |
| 2 | Default attempts from `retrykit/config.py` | done |
| 3 | Full jitter with an injectable random source | todo |
| 4 | Document the policy in README | todo |

## Checkpoint

Updated by Sari 2026-11-25. Steps 1 and 2 done, all tests pass. NEXT ACTION: step 3.
