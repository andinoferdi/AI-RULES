# Rollout and rollback in practice

Filled templates for steps 4, 5 and 7, the monitoring tree, flag and error-reporting code for
common stacks, and what to do with data after a recovery. Numbers marked "default" come from the
skill's defaults table; a project policy replaces them.

## A filled stage plan

Release `v3.2.0` (commit `4f1c9e2`), feature `bulk_export` behind a percentage flag that changes
within one minute. Observer: Lina (on call Mon-Thu 08:00-18:00). Recovery executor: Lina; release
owner: Dimas.

| Stage | Cohort | Min window | Min volume | Signals vs control and thresholds | Observer | Decision at end |
| --- | --- | --- | --- | --- | --- | --- |
| 0 Dark | Flag off, all traffic on v3.2.0 | 1 h after deploy | Normal traffic | Health reports 3.2.0; 5xx and p95 equal to v3.1 baseline; no new error types | Lina | Dimas: open stage 1 |
| 1 Internal | Staff accounts | 1 working day (default) | 50 exports | No failed export; no new client errors | Lina | Lina: advance or hold |
| 2 Canary | 5% of users | 24 h incl. Tuesday peak (default) | 1,000 candidate requests (default) | 5xx <= 1.1x control; p95 <= +20%; new client error <= 0.1% of sessions; export success down < 1% | Lina | Lina: advance, hold or stop |
| 3 | 25% | 24 h (default) | same | same | Lina | Lina |
| 4 | 50% | 24 h (default) | same | same | Lina | Lina |
| 5 Full | 100% | 1 week before flag removal (default) | same | same, plus error budget burn <= 1x | Lina | Dimas: remove flag by 2026-12-18 |

Stage 2 opens Monday 09:00 so its 24 hours end inside Lina's hours on Tuesday. No stage opens on
Friday, before a holiday, or after 14:00 on a day the observer leaves at 18:00 when the stage
cannot reach its first decision point by then.

The comparison query, run per stage over the same window for both cohorts:

```sql
SELECT cohort,
       COUNT(*)                                              AS requests,
       SUM(CASE WHEN status >= 500 THEN 1 ELSE 0 END)        AS errors_5xx,
       ROUND(100.0 * SUM(CASE WHEN status >= 500 THEN 1 ELSE 0 END) / COUNT(*), 2) AS error_pct
FROM   request_log
WHERE  ts >= :stage_start AND ts < :now AND route LIKE '/api/%'
GROUP  BY cohort;  -- cohort = 'candidate' (flag on) or 'control' (flag off)
```

## Rollback plan template

```markdown
## Rollback plan for <release> (<candidate identity>)

Triggers
- Stop thresholds from the stage table (5xx > 2x control, p95 > +50%, new client error > 0.1%
  of sessions, user outcome down > 5%), any data-integrity or security finding, or a spike in
  user reports about <journey>.

Actions, in order (stop after the first one that restores users)
1. Flag `<name>` to 0% - <executor> - takes <1 min | ~15 min if it needs a redeploy> -
   command: <exact command or console path>.
2. Redeploy <previous artifact/digest> - <executor> - takes <n min> - valid only while the
   schema still serves it: <yes, contract step not yet run | no, see data>.
3. Data: <restore from snapshot taken <when>, restore last tested <date> | forward fix <script> |
   none needed> - <executor> - takes <n min>.

Data written during exposure
- <table/records> created by the feature: <kept | migrated | reconciled by <script/owner>>.
- Operations that failed for users: <how to find them>, follow-up by <owner>.

Verification after each action
- Health reports <expected version>; 5xx and p95 back to control; <journey> works by hand;
  new error types at zero; logs and metrics still arriving; data checks: <query>.

Escalation
- <name> decides when the plan does not fit; <channel>.

Time to recover (stated or measured)
- Flag: <n>; redeploy: <n>; data: <n>.
```

## What to monitor

```text
Application
  error rate, total and by endpoint
  latency p50 / p95 / p99
  request volume per cohort
  the user outcome the feature serves (exports completed, saves, checkouts)
Infrastructure
  CPU and memory
  database connection pool use, slow queries
  queue depth and age
  disk and network
Client
  Core Web Vitals (LCP, INP, CLS) at p75
  JavaScript errors, new error types by share of sessions
  API errors seen by the client
Release
  deployed version per instance
  flag state and actual cohort exposure
  error budget remaining and burn rate
```

Alert rules and SLOs are built with `observability-and-instrumentation`.

## Flag checks for common stacks

TypeScript (server-rendered React):

```typescript
const flags = await getFeatureFlags(user.id);      // evaluated per request, not at start-up

if (flags.bulkExport) {
  return <BulkExportPanel tasks={tasks} />;        // new path, only for the cohort
}
return <ExportButton tasks={tasks} />;             // existing behaviour stays the default
```

Python:

```python
def export_view(request):
    if flags.is_enabled("bulk_export", user_id=request.user.id):  # percentage rollout by user
        return bulk_export(request)
    return single_export(request)
```

Evaluate the flag per request (or with a short cache) so turning it off takes effect without a
redeploy. Hash the user id for percentage rollouts so a user stays in the same cohort.

## Error reporting for common stacks

React error boundary that reports and recovers:

```typescript
class ErrorBoundary extends React.Component<React.PropsWithChildren> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    reportError(error, {
      componentStack: info.componentStack,
      release: APP_VERSION,                 // lets the dashboard split by version
      flags: activeFlagNames(),             // and by cohort
      page: window.location.pathname,
    });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}
```

Express error handler that reports without leaking internals:

```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  reportError(err, { method: req.method, route: req.route?.path, release: APP_VERSION });
  res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' } });
});
```

## After a recovery

1. Re-observe: version, cohort exposure (0% means no candidate traffic), error rate and latency
   against the pre-release baseline, the journey by hand, telemetry still arriving.
2. Data: count what the feature wrote during exposure; keep it unless a reviewed decision says
   otherwise. A down-migration that drops it needs the release owner and a backup.
3. Users: list operations that failed during exposure (failed saves, payments, exports) and hand
   the list to whoever follows up.
4. Record: the trigger and its numbers, the actions with times, the re-observation, and the
   conditions for a new attempt (fix, test, a fresh first stage with full window and volume).
5. Hand the cause to `debugging`.

Provenance: flag, rollout, monitoring, error-reporting and rollback-template material adapted
from Addy Osmani's `shipping-and-launch` (addyosmani/agent-skills 3d78ead, MIT). Full notice in
[../references/license.md](../references/license.md).
