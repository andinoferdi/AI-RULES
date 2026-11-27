# Rollout policy (tasks-api)

Stages: 5% -> 25% -> 50% -> 100%. Each stage runs at least 30 minutes and needs at least 1,000
candidate requests before a decision. Compare the flag cohort with the control cohort over the
same window.

| Signal | Advance | Hold | Stop |
| --- | --- | --- | --- |
| 5xx rate, candidate vs control | up to 1.1x | 1.1x to 2x | above 2x |
| p95 latency, candidate vs control | up to +20% | +20% to +50% | above +50% |
| New client error type, share of candidate sessions | none | up to 0.1% | above 0.1% |
| Task save completion, candidate vs control | down less than 1% | down 1% to 5% | down more than 5% |

Stop means: set the flag to 0% at once. The on-call engineer may do this without asking anyone.
Redeploying the previous release or running down-migrations needs the release owner (Bima).
