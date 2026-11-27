# Signal recipes

Concrete shapes for gates 2 to 5. The code is TypeScript on Node with `@opentelemetry/api`; the
rules hold in any stack, so translate the shape into the project's own logger, metrics client and
tracer instead of adding a new one. Each section names the gate that uses it.

## Pick the signal (gate 1)

| Signal | Answers | Cost | Example |
| --- | --- | --- | --- |
| Structured log | What happened in this one case? | Per event; grows with traffic | `payment_failed` with the provider error code |
| Metric | How often, how fast, in aggregate? | Fixed per series; cheap to query | p99 latency of provider calls |
| Trace | Where did the time go across services? | Per request; usually sampled | One slow checkout, broken down by hop |

Metrics tell you **that** something is wrong, traces tell you **where**, logs tell you **why**. A
question that needs "which customer" or "which run" is a log or trace question, never a metric
label.

## Structured events (gate 2)

Log events, not prose. One JSON object per line, a stable event name, machine-readable fields:

```typescript
// BAD: interpolated prose. Unqueryable, inconsistent, and it leaks the email.
logger.info(`Payment ${id} failed for user ${email} after ${n} retries`);

// GOOD: stable event name, allowlisted fields, bounded error code.
logger.warn({
  event: 'payment_attempt_failed',
  paymentId: id,
  provider: 'stripe',
  errorCode: err.code,        // bounded set, not err.message
  attempt: n,
  retryable: true,
}, 'payment attempt failed');
```

| Level | Meaning | On-call action |
| --- | --- | --- |
| `error` | An invariant broke or a terminal failure reached a user; someone may need to act | Investigate |
| `warn` | Degraded but handled: a retryable attempt failed, a fallback was used | Watch for trends |
| `info` | A significant outcome: payment paid, job finished | None |
| `debug` | Diagnostic detail | Off in production by default |

Allowlist fields. Never log whole request or response bodies, auth headers, tokens, passwords,
card data or unredacted personal data, at any level and behind any flag: a debug switch left on in
production is how telemetry pipelines leak.

## Correlation ID and entry point (gate 2)

Accept or generate the request ID at the trusted boundary, bind it to a child logger, return it:

```typescript
const REQUEST_ID = /^[A-Za-z0-9_-]{8,64}$/;

app.use((req, res, next) => {
  const incoming = req.header('x-request-id');
  req.id = incoming && REQUEST_ID.test(incoming) ? incoming : crypto.randomUUID();
  req.log = logger.child({ requestId: req.id });
  res.setHeader('x-request-id', req.id);
  next();
});
```

When several entry points write to one sink, a request ID says which run a line belongs to, not
what started it. Stamp the entry point where the run starts, from a fixed set, next to the request
ID, with one helper for every entry point:

```typescript
type EntryPoint = 'scheduler' | 'replay_endpoint' | 'cli';

// `entryPoint`, not `source`: ECS reserves `source.*` for network fields.
export const runLog = (entryPoint: EntryPoint, requestId: string) =>
  logger.child({ entryPoint, requestId });

// scheduler tick        -> runLog('scheduler', crypto.randomUUID())
// POST /jobs/:id/replay -> runLog('replay_endpoint', req.id)
// CLI invocation        -> runLog('cli', process.env.RUN_ID ?? crypto.randomUUID())
```

A field that only correlates with an entry point (the queue name, the time of day, the host) is a
hint, not an attribution: anything that can invoke the job can reproduce it.

## Across a queue or an HTTP hop (gates 2 and 4)

Carry the request ID, the entry point and the trace context in the message metadata. The consumer
reads them; it never re-derives them.

```typescript
import { context, propagation, trace } from '@opentelemetry/api';

const tracer = trace.getTracer('payments');

// Producer: inside the entry point's active span.
function enqueuePayment(invoiceId: string, entryPoint: EntryPoint, requestId: string) {
  const headers: Record<string, string> = { requestId, entryPoint };
  propagation.inject(context.active(), headers);       // adds traceparent / tracestate
  queue.send({ invoiceId, headers });
}

// Consumer: continue the producer's trace and bind its attribution.
function onMessage(msg: { invoiceId: string; headers: Record<string, string> }) {
  const parent = propagation.extract(context.active(), msg.headers);
  return context.with(parent, () =>
    tracer.startActiveSpan('payment.process', async (span) => {
      const log = runLog(msg.headers.entryPoint as EntryPoint, msg.headers.requestId);
      try {
        return await processPayment(msg.invoiceId, log);
      } finally {
        span.end();
      }
    }));
}
```

Initialize the tracing SDK before any instrumented client is imported. Auto-instrumentation covers
HTTP, gRPC and common database clients; add manual spans only around meaningful units of work
(`chargeProvider`, `applyDiscounts`) with the attributes on-call filters by, never personal data.

## Attempt and outcome (gate 3)

Count every provider call as an attempt, and count each job once when it reaches its terminal state.
A job that succeeds on the second attempt adds one failed attempt and zero terminal failures.

```typescript
import { metrics } from '@opentelemetry/api';

const meter = metrics.getMeter('payments');
const attempts = meter.createCounter('payment.provider.attempts');          // per call
const outcomes = meter.createCounter('payment.outcomes');                   // once per job
const duration = meter.createHistogram('payment.provider.duration', { unit: 's' });

attempts.add(1, { provider: 'stripe', outcome: 'timeout' });                // retryable
outcomes.add(1, { outcome: 'paid', path: 'after_retry' });                  // terminal
duration.record(elapsedSeconds, { provider: 'stripe', outcome: 'ok' });
```

Bucket boundaries are set in the SDK, not at the call site: in `@opentelemetry/sdk-metrics` 2.x pass
a view `{ instrumentName: 'payment.provider.duration', aggregation: { type:
AggregationType.EXPLICIT_BUCKET_HISTOGRAM, options: { boundaries: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5,
10, 30] } } }`. Choose boundaries that resolve the objective: a 30 s provider timeout needs a bucket
at or above 30. With Prometheus clients the same rules hold for `Histogram` and `labelNames`.

Use RED (rate, errors, duration) on every endpoint and external dependency, USE (utilization,
saturation, errors) on queues, pools and hosts: queue depth and the age of the oldest job for every
worker.

## Labels and cardinality (gate 3)

Every unique label combination is its own time series. Labels come from small fixed sets:

```text
OK as label:    route="/api/tasks/:id"   status_class="5xx"   provider="stripe"   outcome="timeout"
NEVER a label:  user_id, email, tenant_id, request_id, full URL, error message text
```

Estimate before adding a dimension and write the number down: `3 routes x 5 status classes x 2
providers x 3 outcomes = 90 series`. Track percentiles, never averages: an average hides the 1 % of
users having a terrible time. Read p50, p95 and p99 from the histogram.

## Alerts (gate 5)

Page on symptoms users feel; put causes on dashboards.

| Symptom (page when the owner approves the threshold) | Cause (dashboard, or a ticket) |
| --- | --- |
| Terminal failure ratio above the objective for the window | CPU high on one host |
| p99 latency above the objective | One pod restarted |
| Oldest queued job older than the objective | Disk filling slowly |

Two severities only: **page** (users hurt now) and **ticket** (degradation, act this week). Every
threshold and window comes from an SLO or a measured baseline. Without one, the rule ships as a
proposal that cannot wake anyone:

```yaml
- alert: PaymentsFailedAfterRetries
  expr: <terminal failure ratio over 30m> > <PROPOSED: payments lead to approve>
  labels:
    severity: ticket        # becomes page once the owner approves the threshold
    owner: payments-oncall
  annotations:
    runbook: docs/runbooks/payments-failed-after-retries.md
```

Delete an alert whose answer is "ignore it, it self-heals". Fire a rule against controlled input in
a test environment when the project has one; send a real notification only with explicit
authorization.

## Runbook (gate 5)

Store it next to the alerts (for example `docs/runbooks/<alert>.md`), named after the alert:

```markdown
# Runbook: PaymentsFailedAfterRetries
**Means:** customers ended unpaid after every retry; provider outage or a bad deploy are likely.
**First check:** terminal outcomes by reason and provider attempt p99 for the alert window;
  timeouts with high p99 point at the provider, declines at card data, neither at the worker.
**Escalate to:** #payments-oncall; provider status page and account manager for timeouts.
```

Add steps only when the first check alone cannot decide; a five-step runbook covering the three
common causes beats twenty steps that get skimmed. Fix a wrong or missing step before closing the
incident that exposed it.

## Sampling (gate 4)

Head-sample at a low default rate and keep every error trace with tail sampling when the backend
supports it. A tail sampler keeps only the spans that reach it, so check the sampling decision on
every hop of the path: one service sampling at 1 % breaks the trace for the rest.

Provenance: recipes adapted from Addy Osmani's `observability-and-instrumentation`
(addyosmani/agent-skills, path last changed in c4efec8, MIT); OpenTelemetry API calls checked
against the opentelemetry-js documentation. Notice: [../references/license.md](../references/license.md).
