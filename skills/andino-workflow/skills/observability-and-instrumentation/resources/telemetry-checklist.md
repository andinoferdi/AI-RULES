# Telemetry checklist

The at-a-glance version of the gates, for a final pass or a review of someone else's change. Each
line is checked against emitted output or the diff, never against intent. Mark a line that cannot
be checked here as unavailable, with the reason.

## On-call questions (gate 1)

- [ ] Two to four questions were written before the first edit, in the agent's message.
- [ ] Each question names its signal (log, metric or trace), the query that answers it and the
      decision the answer supports.
- [ ] Every signal added or changed serves one of the questions.

## Structured logging (gate 2)

- [ ] Every line is one JSON object with a stable event name; no prose built by interpolation.
- [ ] Levels are consistent: `error` for a broken invariant or a terminal failure, `warn` for a
      handled degradation such as a retryable attempt, `info` for significant outcomes, `debug`
      off in production.
- [ ] Fields are allowlisted: no bodies, auth headers, tokens, passwords, card data or unredacted
      personal data, at any level or flag setting.
- [ ] Calls to external services log metadata only: endpoint, status, latency, attempt, bounded
      error code.
- [ ] Actual output was spot-checked: structured fields, not `[object Object]`.

## Attribution and correlation (gate 2)

- [ ] A request ID is accepted (validated) or generated at the trusted boundary and appears on
      every line, span and outbound call of the run.
- [ ] Every sink written by more than one entry point carries an entry-point field from a fixed
      set, set where the run starts.
- [ ] Both travel in HTTP headers and queue metadata; no consumer derives them from a queue name,
      a host or the time.

## Metrics (gate 3)

- [ ] **RED** on every endpoint and external dependency: rate, errors, duration.
- [ ] **USE** on every queue, pool and host: utilization, saturation, errors; queue depth and the
      age of the oldest job for every worker.
- [ ] Attempt series and terminal-outcome series are separate; the terminal series moves once per
      job, at the existing terminal state, so retries and redelivery do not inflate it.
- [ ] Each series declares its unit, what one increment means and its denominator.
- [ ] Labels come from fixed sets (route template, status class, provider, outcome); the label
      combinations were estimated and written down.
- [ ] No unbounded label: user, tenant or request IDs, emails, raw URLs, error text.
- [ ] Latency is a histogram with buckets that resolve the objective; p50, p95 and p99 are
      queryable; no average stands alone.

## Tracing (gate 4)

- [ ] The tracing SDK starts before instrumented clients load; auto-instrumentation covers HTTP,
      gRPC and database clients.
- [ ] W3C `traceparent`/`tracestate` is injected on every outbound call and queue message and
      extracted on every inbound one.
- [ ] Manual spans wrap meaningful units of work only, with the attributes on-call filters by and
      no secrets or personal data.
- [ ] Head sampling is low by default; errors are kept with tail sampling where supported; the
      sampling decision holds on every hop of the path.

## Alerting and runbooks (gate 5)

- [ ] Every page is a symptom users feel (terminal failures, latency, queue age); causes (CPU,
      disk, restarts) go to dashboards or tickets.
- [ ] Two severities only: **page** and **ticket**.
- [ ] Every threshold and window cites an SLO or a measured baseline; one without a basis is marked
      PROPOSED with the owner who approves it, and ships as a ticket or a disabled page.
- [ ] Every alert is actionable, has an owner and links a runbook with what it means, the first
      check and the escalation path.
- [ ] Rules were evaluated against controlled input where the project can; a real notification
      was sent only with explicit authorization.
- [ ] No alert fires daily and gets acknowledged without action.

## Dashboards

- [ ] A service health view shows error rate, p99 latency, traffic and saturation.
- [ ] A dependency panel shows each dependency's error rate and latency.
- [ ] The dashboard answers the on-call questions, not "everything except the answer".
- [ ] The default time range is short (1 h to 6 h), not 30 days.

## Verify the telemetry (gate 6)

- [ ] A normal run and a controlled failure went through each entry point.
- [ ] The failed run was found by request ID alone, with its entry point, attempts and terminal
      outcome.
- [ ] Metric deltas match the expected counts for the controlled runs.
- [ ] One trace runs unbroken from the entry point through the queue to the dependency call.
- [ ] Tests assert telemetry properties: attribution reaches the consumer, the terminal outcome is
      counted once, no sensitive field is emitted.
- [ ] Each check is recorded as observed, failed, unavailable or not applicable, with its command
      or artifact. Local output proves event shape, not export, cross-service delivery or routing.

## Pre-launch gate

Before a feature ships to production, all of these hold, or the gap is named with its owner:

- [ ] Structured logs reach the log backend.
- [ ] RED metrics are visible for every new endpoint and dependency.
- [ ] At least one symptom alert exists with a runbook, its threshold approved or marked PROPOSED.
- [ ] A request can be traced across every service it touches.
- [ ] On-call knows where the runbooks are.

Launch-day monitoring and rollback triggers belong to `shipping-and-launch`.

Provenance: adapted from Addy Osmani's `references/shared/observability-checklist.md`
(addyosmani/agent-skills, path last changed in c4efec8, MIT), with the Andino attempt-versus-outcome,
attribution, label-estimate, proposed-threshold and evidence-status items. Notice:
[../references/license.md](../references/license.md).
