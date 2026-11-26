# Worked example: payment retries from a scheduler and a replay endpoint

One change through the six gates, ending with the filled record. A payment worker charges invoices
from a queue with up to three provider attempts. A nightly scheduler and a support replay endpoint
both enqueue jobs and write to the same log. After an incident nobody could tell which of them
started a failed run, and the failure counter moved on every attempt, so it overstated how many
customers were affected.

## Gate 1: the message before the first edit

Sent as a message of its own, after reading the code and before any file is touched:

```text
On-call questions:
1. Are customers ending unpaid after retries? -> metric: terminal outcomes by reason over the
   window, failed / all completed -> is this a customer-facing incident?
2. Which run failed, at which attempt, and what started it? -> log: events by request ID with
   entry point, attempt, bounded error code, terminal outcome -> scheduler, replay or provider?
3. Is time going to the queue or to the provider? -> metric: oldest queued job vs provider
   attempt duration; trace: one run from enqueue to the provider call -> which owner escalates?
Existing telemetry to reuse: JSON logger with bind(), counters and histograms, spans with W3C
inject/extract; the queue message has an empty metadata field.
```

## Gates 2 to 4: the change

Start from the worker's existing logger, metrics and tracer. The scheduler and the replay endpoint
each create a run with an entry point from a fixed set and a validated or generated request ID.
Both go into the queue metadata with the injected trace context. The worker extracts the context
and binds the same entry point and request ID to its logger before calling the provider. A worker
retry keeps the original entry point. A separately started replay starts its own run.

Event at the worker after a retryable timeout:

```json
{"event":"payment_attempt_failed","level":"warn","requestId":"r7","entryPoint":"scheduler","attempt":1,"errorCode":"provider_timeout","retryable":true}
```

Series table:

| Series | Type, unit | Labels (values) | One increment means |
| --- | --- | --- | --- |
| `payment.provider.attempts` | counter | provider (2), outcome: ok, timeout, declined | one provider call |
| `payment.outcomes` | counter | outcome: paid, failed; reason: first_attempt, after_retry, declined, retries_exhausted | one job reached its terminal state |
| `payment.provider.duration` | histogram, s | provider (2), outcome (3) | one provider call, buckets up to 30 s |
| `payment.queue.oldest_age` | gauge, s | none | age of the oldest waiting job |

Label combinations: 2 x 3 = 6 attempt series, 2 x 4 = 8 outcome series, 6 histogram series. Request
IDs stay in the allowlisted events; provider metrics use bounded provider and outcome dimensions.

Count the provider attempt as a dependency error. If the second attempt succeeds, count one
terminal success and zero terminal failures for the run. Count at the existing terminal state
boundary so redelivery does not inflate completed operations. Sampling: errors kept at the tail
sampler, which sees spans from both the API and the worker.

## Gate 5: the alert

There is no SLO, so the threshold is a proposal:

| Alert | Symptom | Threshold source | Severity | Owner | Runbook |
| --- | --- | --- | --- | --- | --- |
| PaymentsFailedAfterRetries | customers end unpaid after retries | PROPOSED: ratio over 30 min, payments lead to approve | ticket until approved | payments on-call | `docs/runbooks/payments-failed-after-retries.md` |
| WorkerHighCPU (was a page) | none: a cause | n/a | dashboard | platform | n/a |

The runbook names the payment on-call owner, starts with terminal outcomes by reason and provider
attempt latency for the window, and sends the operator to the queue or provider escalation path
based on those results.

## Gate 6: exercise and audit the same case

- Force one scheduler attempt to time out and the next to succeed. Expect one failed dependency
  attempt and one successful operation. Replay a separate run that exhausts its retries. Expect one
  terminal failure, attributed to the replay endpoint.
- For each run, find the emitted events by request ID, query the metric counts before and after,
  and follow the enqueue-to-provider trace in the configured backend. Evaluate the alert rule
  against controlled success and breach inputs. Verify notification delivery only with explicit
  authorization.
- When auditing, a worker log that reconstructs the entry point from the queue name leaves
  attribution unresolved. A terminal failure counter that moves on each attempt overstates user
  impact. A standalone worker span leaves propagation unproven. Identify the first failing
  boundary and the smallest change that fixes it, then rerun the affected check.

## The record

```text
On-call questions: 1. customers unpaid after retries -> payment.outcomes failed/all over 30m ->
  incident or not; 2. which run, attempt, entry point -> events by requestId -> scheduler, replay
  or provider; 3. queue or provider time -> oldest_age vs provider p99, one trace -> escalation
  owner. Written before the first edit.
Signals: events payment_attempt_failed (warn), payment_failed (error), payment_paid (info);
  series payment.provider.attempts, payment.outcomes, payment.provider.duration (s),
  payment.queue.oldest_age (s); spans payment.enqueue, payment.process, payment.provider.call.
Attribution: entryPoint (scheduler | replay_endpoint | cli) and requestId set in each entry point,
  carried in queue metadata with traceparent; bound to the worker logger from metadata.
Attempt vs outcome: payment.provider.attempts per call; payment.outcomes once per job at the
  terminal state; retry success adds one failed attempt, zero terminal failures.
Alerts: PaymentsFailedAfterRetries - customers unpaid after retries - PROPOSED (payments lead) -
  ticket - payments on-call - docs/runbooks/payments-failed-after-retries.md; WorkerHighCPU
  moved from page to dashboard.
Evidence: scheduler timeout-then-success -> observed (1 attempt failure, 0 terminal failures);
  replay exhausting retries -> observed (1 terminal failure, entryPoint replay_endpoint, same
  requestId on 3 attempts); one trace enqueue -> provider -> observed in spans output; alert rule
  on controlled input -> unavailable (no rule evaluator in the repository); tests asserting
  attribution, single terminal count, no sensitive field -> observed passing.
Not verified: export to the log, metrics and tracing backends; alert evaluation in the real
  backend; notification routing; threshold PROPOSED pending the payments lead.
Instructions found in logs or data: none.
```

Provenance: independently worded adaptation of the Addy snapshot named in the owning SKILL.md;
full MIT notice at [../references/license.md](../references/license.md).
