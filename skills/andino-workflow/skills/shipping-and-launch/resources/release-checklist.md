# Release decision and rollback record

## Readiness review

Fill in the candidate and previous production artifact, release stage, change summary, affected journeys and cohorts, release owner, observer, recovery executor, authorization and execution status. Use the repository's Definition of Done and release policy. Record evidence for applicable checks.

| Surface | Select checks appropriate to the change |
| --- | --- |
| Build and behavior | Candidate build, unit/integration/end-to-end tests for changed paths, lint/types, review and staging smoke. |
| Security | Native dependency audit, secret and configuration handling, input validation, authorization and abuse controls for exposed endpoints. |
| Performance | Compare critical-path latency, throughput, saturation and affected client budgets to their baselines. |
| Accessibility | For changed UI, exercise keyboard and focus behavior, accessible names, errors and contrast. |
| Infrastructure and data | Verify production config, health, telemetry, dependency and mixed-version compatibility, migration recovery and data reconciliation. |
| Documentation | Review release notes, operator runbook, user instructions and API compatibility notes where affected. |

For each required check record **gate | expected | observed | evidence and time | status | owner and next action**. Use PASS, FAIL, UNAVAILABLE or NOT APPLICABLE with a reason. Keep the record compact for a routine release.

## Stage and recovery handoff

- **Stage** — Cohort and candidate/control query, window and minimum volume, signal thresholds, observer, decision time and next stage. Compare like traffic and verify actual exposure. Distinguish a zero baseline with known volume from a missing baseline.
- **Thresholds** — Use accepted release policy. For illustration, error rise up to 10% and p95 rise up to 20% can pass their individual gates. Error above 2× baseline or p95 above 50% regression can trigger recovery. Intermediate values hold. For zero baseline, use a pre-agreed absolute ceiling and denominator. Set explicit boundaries for user impact, data, security and applicable business or client signals.
- **Error budget** — Use the service's window, remaining budget and burn policy. Example policy permits normal pace above 20%, only low-risk slow rollout above zero through 20%, and freezes feature rollout when exhausted. Excessive canary burn holds expansion even with favorable aggregate metrics.
- **Recovery** — Record trigger, executor, approved runbook/command, target flag or previous artifact, recovery deadline, verification and escalation. Confirm data preservation and recovery separately. Check health, errors, latency, the critical journey and telemetry after each action. Verify data reconciliation if writes were exposed.
- **Decision** — Record READY, HOLD or NO-GO, the scope and reason, evidence and the next action with owner and timing. List completed live actions separately from proposals.

## Worked cases

These are hypothetical operator records. Their figures and policies are fixture inputs.

| Input | Decision and operator handoff |
| --- | --- |
| **Routine flag.** Candidate `r42`, current `r41`. Staging smoke and both flag-state tests pass. Production health and dashboard access verified with the flag OFF. Release policy allows a 5% canary with 30 minutes and at least 1,000 requests per cohort. Owner Ana has an approved flag-off runbook. | **READY for 5% only.** Ana may enable the canary within the approved window. Compare matched request counts, errors, p95 and checkout success before expansion. If the stop rule fires, Ana disables the flag and verifies checkout and error recovery. Ana owns flag removal after stable full rollout. |
| **Mixed canary.** Candidate `r43` at 5%. Over matched windows with sufficient volume, candidate has 24 errors in 2,000 requests (1.2%) versus control's 20 in 10,000 (0.2%). Aggregate health is green. Approved stop rule is over 2× control. | **NO-GO for expansion.** The candidate is at 6× control. The authorized operator reduces exposure per the runbook and checks cohort exposure and user-facing errors afterward. If the window had too few observations and no independently verified stop breach, HOLD at the current stage and record the next decision time and sample requirement. |
| **Destructive migration.** Candidate `r44` drops a column still read by the prior binary. Backup exists, but restore duration and writes after cutover have not been tested. | **NO-GO for the destructive step.** The migration owner stages a compatible transition, rehearses recovery and reconciliation in a representative environment, and submits the evidence before requesting destructive-step authorization. A binary revert alone is unsafe after the drop. |

Provenance: independently worded adaptation of the Addy snapshot identified in the owning GUIDE.md. Full MIT notice at [../references/license.md](../references/license.md). Runtime uses local resources.
