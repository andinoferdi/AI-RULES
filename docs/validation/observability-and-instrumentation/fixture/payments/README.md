# payments-worker

Charges due invoices through the payment provider. Three entry points put a job on the
queue; one worker drains it and calls the provider with up to three attempts per job.

| Entry point | How it runs | What it does |
| --- | --- | --- |
| Scheduler | cron, nightly at 02:00, and with `--requeue-failed` at 02:30 | enqueues every `due` invoice; with `--requeue-failed`, enqueues `failed` ones again |
| Replay endpoint | `POST /invoices/{id}/replay`, used by the support team | enqueues one invoice (`payments/api.py`) |
| Manual CLI | `scripts/charge_now.py`, used by operations | enqueues one invoice |

The worker runs right after each enqueue in production. Locally:

```
python scripts/reset_data.py                  # fresh copy of data/ into var/
python scripts/scheduler_tick.py              # or: --requeue-failed
python scripts/replay.py inv-103 --request-id req-1
python scripts/charge_now.py inv-101
python scripts/run_worker.py                  # drains the queue
python -m unittest discover -s tests
```

The fake provider follows `data/provider_script.json` (per invoice, the outcome of each
attempt), so every run is repeatable after `reset_data.py`.

## Telemetry

`payments/telemetry/` is our in-house package: a JSON-lines logger (`log.py`), counters,
gauges and histograms flushed to `var/telemetry/metrics.json` (`metrics.py`, cumulative across
processes, like our metrics backend) and spans written to `var/telemetry/spans.jsonl` with W3C
`traceparent` inject/extract (`tracing.py`). Production ships these files to the log, metrics
and tracing backends; the shipping itself is not in this repository. No new dependencies may be
added before the partner launch.

Alert rules live in `ops/alerts.yaml`. Production settings are in `deploy/prod.env`, which only
the platform team deploys.

## Log retention

The worker log is kept 30 days. The scheduler's cron history and the API access log are kept
3 days.
