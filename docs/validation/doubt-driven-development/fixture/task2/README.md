# Events

Webhook events for the analytics pipeline. The provider may deliver the same event more than
once; a repeat carries the same `id` and may carry a later `received_at`.

- Every event has an `id`, a string. Ids are case-sensitive: `EV-1` and `ev-1` are different
  events.
- `data/sample-day.json` is one day of real deliveries, anonymised.
- Runs on Python 3.11 or later.

Tests: `python -m unittest discover -s tests -t .`
