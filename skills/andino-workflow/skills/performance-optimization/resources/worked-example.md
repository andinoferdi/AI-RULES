# Worked example: search suggestions p95

A synthetic case that shows every gate and the record. Commands and numbers are the example's
own; real runs produce their own.

## The request

> "Search suggestions feel laggy on mobile. Our SLO is p95 under 200 ms for
> `/api/suggest`; the dashboard shows about 640 ms. Can you speed it up? Maybe switch to a faster
> JSON library?"

Prerequisites: goal written down (p95 of `/api/suggest` under 200 ms); the repo has
`bench/suggest_bench.py`, which replays 500 recorded queries against a local server and prints
p50/p95; the suite runs with `pytest -q` (212 passed, 0 failed before any change).

## Gate 1: baseline

```
$ for i in 1 2 3 4 5; do python bench/suggest_bench.py --queries bench/queries.txt; done
p50=410ms p95=652ms   p50=402ms p95=640ms   p50=415ms p95=661ms
p50=398ms p95=633ms   p50=408ms p95=647ms
```

Median p95 647 ms, spread 633-661 ms; warm server, revision `a1b2c3d`, 500 queries, local
PostgreSQL, one client. Target 200 ms.

## Gate 2: attribution

```
$ python -m cProfile -s cumulative bench/suggest_once.py | head -12
   ncalls  cumtime  filename:lineno(function)
      500   18.900  views.py:41(suggest)
      500   13.210  serializers.py:12(to_payload)
      500   12.950  json/encoder.py:200(encode)
      500    3.840  search.py:77(top_matches)
```

Serialization takes 13.2 of 18.9 s (70%). The payload is the cause, not the encoder itself:
`to_payload` attaches the user's full `settings` blob (about 180 KB) to every response. The
requester's suspect, the JSON library, is the encoder's speed; the next attempt tests it directly.

## Gate 3: decide one change, then the next

Attempt 1 tests the requester's idea first, since it is cheap and reversible: compact separators
in the encoder. Expected: p95 down by more than the 28 ms spread. Disproved if the delta stays
inside the spread. Must keep: the response body's fields and values.

Attempt 2: stop sending `settings`; the client already fetches it once at login from
`/api/settings`. Expected: p95 under 200 ms. Disproved if p95 stays above 200 ms. Must keep:
every field the suggestion widget reads (checked in `web/suggest.ts`: `id`, `label`, `kind`).

## Gate 4: change and remeasure

| Idea | Baseline -> result | Verdict | Why |
| --- | --- | --- | --- |
| Compact JSON separators | p95 647 -> 631 ms | revert | 16 ms is inside the 28 ms spread |
| Drop `settings` from the payload | p95 647 -> 118 ms (spread 112-125) | keep | Payload 182 KB -> 2.1 KB; widget fields unchanged; 212 tests pass |

## Gate 5: guard

```python
def test_suggest_payload_stays_small(client):
    response = client.get("/api/suggest?q=inv")
    assert len(response.content) < 16_000
```

On the old code: `AssertionError: assert 186311 < 16000`. On the new: passed.

## Gate 6: reply and record

> The suggestions endpoint now meets the SLO in our local benchmark: p95 went from 647 ms to
> 118 ms over 500 recorded queries. Each response carried your full settings (about 180 KB);
> it no longer does, and the widget gets the same fields. Switching JSON settings made no
> measurable difference, so I left it out. Production p95 is not measured yet: after the
> deploy, compare the dashboard's p95 for a day with the 640 ms you saw.

```text
Goal: p95 of /api/suggest under 200 ms (dashboard shows ~640 ms)
Baseline: bench/suggest_bench.py, 500 queries; 5 runs; p95 median 647 ms (spread 633-661); warm, a1b2c3d, local PostgreSQL
Attribution: cProfile -> to_payload/json encode 13.2 of 18.9 s (70%); settings blob ~180 KB per response; ruled out: search.py top_matches 3.8 s (20%)
Change: drop settings from the suggest payload; expected p95 < 200 ms; disproved if p95 stays above 200 ms
Attempts:
| Idea | Baseline -> result | Verdict | Why |
| Compact JSON separators | 647 -> 631 ms | revert | inside 28 ms spread |
| Drop settings from payload | 647 -> 118 ms | keep | 182 KB -> 2.1 KB, fields unchanged |
Correctness: pytest 212 passed before and after; widget fields id/label/kind compared on 20 queries
Guard: test_suggest_payload_stays_small -> fails on old (186311 < 16000), passes on new
Not measured or not verified: production p95, mobile network; next capture: dashboard p95 for 24 h after deploy
```

## Anti-pattern in this case

Switching JSON libraries because the request suggested it, measuring once, and reporting the
16 ms difference as a 2.5% gain. The spread was 28 ms; the gain was noise, and the 180 KB payload
would still be there.
