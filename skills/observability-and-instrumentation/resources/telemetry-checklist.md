# Worked example and telemetry proof checklist

## Payment retries from a scheduler and replay endpoint

Start from the worker's existing logger, metrics and tracer. The scheduler and
replay endpoint each create a run with an allowlisted origin and a validated or
generated request ID. Put both in queue metadata with the injected trace
context. The worker extracts the context and binds the same origin and request
ID to its logger before calling the provider. A worker retry keeps the original
origin. A separately initiated replay starts its own run.

| On-call question | Evidence to query | Decision |
| --- | --- | --- |
| Are payment operations succeeding after retries? | Rate of terminal failures divided by all completed operations over the same window. Group success by bounded first-attempt or after-retry outcome when needed. | Decide whether customers are affected. |
| Which attempt failed and where did the run originate? | Filter structured events by request ID and inspect entry point, attempt number, bounded error code and terminal outcome. | Distinguish scheduler traffic from replay and confirm retry exhaustion. |
| Is time spent waiting in the queue or calling the provider? | Compare queue age with provider attempt duration histograms. Follow a trace across enqueue, consume and provider call. | Route investigation to the queue or provider owner. |

Example event at the worker after a retryable timeout:

```json
{"event":"payment_attempt_failed","level":"warn","requestId":"r7","entryPoint":"scheduler","attempt":1,"errorCode":"provider_timeout","retryable":true}
```

Count the provider attempt as a dependency error. If the second attempt succeeds,
count one terminal payment success and zero terminal failures for the run. Count
at the existing terminal state boundary so redelivery does not inflate completed
operations. Keep request IDs in allowlisted diagnostic events. Provider metrics
can use bounded provider and outcome dimensions. Record duration in a histogram
with units and buckets suitable for the latency objective.

Page on the terminal failure ratio using the team's approved objective and
window. Until those values are available, record the alert as a proposal.
The runbook identifies the payment on-call owner, starts with terminal outcome
counts and provider attempt latency for the affected window, then directs the
operator to the queue or provider escalation path based on those results.

## Exercise and audit the same case

- Force one scheduler attempt to time out and the next to succeed. Expect one
  failed dependency attempt and one successful operation. Replay a separate run
  that exhausts retries. Expect one terminal failure, with replay attribution.
- For each run, inspect emitted events by request ID, query before/after metric
  counts, and follow the enqueue-to-provider trace in the configured backend.
  Evaluate the alert rule against controlled success and breach inputs. Verify
  notification delivery separately when authorized.
- When auditing, a worker log that reconstructs origin from queue name leaves
  attribution unresolved. A terminal failure counter that moves on each attempt
  overstates user impact. A standalone worker span leaves propagation unproven.
  Identify the first failing boundary and the smallest change to fix it, then
  rerun the affected check.
- Report the expected and observed result for each check, the query or artifact
  used, and any missing evidence with its next action. Local JSON output can
  demonstrate event shape without proving export, cross-service traces or routing.

## Quick checklist
Start with 2–4 on-call questions. Every field/signal answers one. Logs use JSON/stable event/level/correlation; entryPoint comes from originating scheduler/CLI/replay path, not downstream inference. Propagate both across queue/HTTP. Allowlist identifiers/metadata; never full bodies/tokens/passwords/PII.
RED on endpoint/dependency, USE on pool/queue/resource. Route templates/status classes/provider names are bounded labels; user/tenant/request IDs and raw URLs/errors belong only in appropriately redacted logs/traces. Histograms permit p50/p95/p99; means alone hide tails. Budget cardinality and retention.
Initialize tracing before clients; W3C context travels each async boundary. Manual spans name meaningful work, not every function. Low head sampling/default and error-retaining tail sampling when supported; no sensitive attributes.
Alert symptom + threshold/duration/SLO rationale + owner/runbook. Page for immediate user impact, ticket for slower degradation. Causes feed dashboards. Runbook minimum: what it means, first discriminating query, escalation. Correct stale steps when closing incident.
In authorized test environment emit a real failure; find by requestId and entryPoint, verify structured output and expected series, follow an unbroken trace and test alert delivery/runbook. Offline artifact inspection does not prove exporter or channel works. Recording external notification needs explicit authority.
Output signal/question map, actual artifact identifiers, observed gaps and deployment limitations.

Provenance: independently worded adaptation of the Addy snapshot identified in the owning GUIDE.md; full MIT notice at [../references/license.md](../references/license.md). No upstream installation or hook is required.
