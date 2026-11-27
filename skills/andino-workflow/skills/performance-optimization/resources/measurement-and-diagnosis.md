# Measurement and diagnosis

Open this for gates 1 and 2: choosing the capture that splits a symptom, taking samples that can
be compared, and reading the result. Every snippet uses the language's standard tooling; when a
tool is missing, name it and use the closest installed one.

## Symptom to first capture

```
What is slow or heavy?
├── First page load (LCP, FCP, TTFB)
│   └── Trace or Lighthouse report -> LCP element and its four subparts
│       (see performance-audit.md); server time -> profile the backend route
├── Interaction feels sluggish (INP, jank)
│   └── Trace the interaction -> input delay vs handler time vs presentation delay;
│       long tasks over 50 ms on the main thread
├── One endpoint or job is slow
│   └── Per-request timing split: queue/pool wait, application CPU, query count and time,
│       downstream calls; query count at two input sizes
├── Every endpoint is slow at once
│   └── Pool wait vs execution time, CPU and memory saturation, GC pauses, a shared dependency
├── Slow only sometimes (tail latency)
│   └── Sample slow requests separately (p95/p99); lock waits, GC, cold caches, noisy neighbours
├── Memory grows with time or traffic
│   └── Traced memory at 2-3 request counts; allocation snapshot diff by line; object counts
├── CPU-bound code
│   └── Profile top frames by cumulative time; work at two input sizes (does it grow faster
│       than the input?)
└── Startup is slow
    └── Import or module-load timing; cold start measured from process start, cold and warm apart
```

## Sampling and statistics

- Take at least three samples; five or more when one run is under 50 ms or the spread is wide.
  Discard nothing silently; if a first run is a cold start, report it apart.
- Use the statistic that matches the complaint: median for typical cost, p95 or p99 for a tail,
  p75 for Core Web Vitals field data. Report the spread as min-max (or interquartile range for
  large samples).
- The noise rule: a delta smaller than the larger of the two spreads is not a gain.
- Keep conditions fixed: revision, input and its size, cache state, machine, background load,
  device and network profile for browsers, concurrency for services. Write them down; the
  remeasure copies them.
- Growth questions need two or three input sizes, not one: work that doubles when the input
  doubles is linear, work that quadruples is quadratic.
- Synthetic (benchmark, lab) and field (real users) numbers answer different questions. A lab
  improvement predicts a field improvement; only field data confirms it.

```python
import statistics, timeit

def sample(stmt, setup="pass", repeat=5, number=1, globals=None):
    runs = timeit.repeat(stmt, setup, repeat=repeat, number=number, globals=globals)
    ms = sorted(r * 1000 / number for r in runs)
    return {"median_ms": round(statistics.median(ms), 2), "min_ms": round(ms[0], 2),
            "max_ms": round(ms[-1], 2), "n": len(ms)}
```

For a CLI or service command, time the command itself several times with the shell's `time`, a
loop around `perf_counter`, or the project's benchmark; keep its printed output to compare
results before and after.

## Attribution captures

### CPU profile (Python)

```python
import cProfile, pstats

profiler = cProfile.Profile()
profiler.enable()
run_the_slow_path()
profiler.disable()
pstats.Stats(profiler).sort_stats("cumulative").print_stats(12)
```

Read the cumulative column top-down: the first frame owned by the project with a large share is
the suspect. Node: `node --cpu-prof script.js` and open the `.cpuprofile` in DevTools; browsers:
the Performance panel.

### Query count and time per operation

Wrap the connection or cursor, count calls and time them, then run the operation at two sizes:

```python
import time

class CountingConnection:
    def __init__(self, conn):
        self.conn, self.calls, self.seconds = conn, 0, 0.0

    def execute(self, sql, params=()):
        start = time.perf_counter()
        try:
            return self.conn.execute(sql, params)
        finally:
            self.calls += 1
            self.seconds += time.perf_counter() - start
```

A call count that grows with the number of rows returned is repeated work (N+1). Many ORMs log
queries with a setting (Django `connection.queries`, SQLAlchemy `echo=True`); prefer the built-in
when it exists.

### Allocation snapshot diff (Python)

```python
import tracemalloc

tracemalloc.start(10)
run_workload(1_000)
before = tracemalloc.take_snapshot()
run_workload(1_000)
after = tracemalloc.take_snapshot()
for stat in after.compare_to(before, "lineno")[:10]:
    print(stat)
```

Lines whose size keeps growing between equal workloads hold the leak; a flat diff rules a
suspect out. Other runtimes: heap snapshots in DevTools or `node --inspect`, `jmap`/JFR, `dotnet-gcdump`.

### Ruling out a suggested cause

Measure the suspect directly and quote the output: its share in the profile, its allocation
growth, its time in the trace. "The PDF library is the slow part" is a reason to look; the
profile showing its frames at 4% of the total is the evidence that rules it out.

### Pool wait versus execution

Time acquiring a connection separately from running the query. High wait with stable execution
means capacity or connections held too long (long transactions, missing release, work done while
holding the connection); rising execution means the database itself.

### Query plan

Capture the estimated plan first (`EXPLAIN`); run `EXPLAIN ANALYZE`, which executes the
statement, only where its effects and load are safe. Compare estimated and actual rows, look for
scans and sorts, and keep the plan text for the before/after comparison.

## Reading a Lighthouse JSON report

Lighthouse reports are lab data from one run under the settings in `configSettings` (form factor,
throttling). Useful audits by id:

| Audit id | What it gives |
| --- | --- |
| `largest-contentful-paint` | LCP value (`numericValue`, ms) |
| `largest-contentful-paint-element` | The LCP element and a phase table: TTFB, load delay, load time, render delay |
| `cumulative-layout-shift`, `layout-shifts` | CLS and the elements that moved, with causes |
| `total-blocking-time` | Lab proxy for responsiveness (Lighthouse cannot measure INP) |
| `render-blocking-resources` | Scripts and styles delaying first render, with estimated savings |
| `lcp-lazy-loaded`, `prioritize-lcp-image` | LCP image discovered late or deprioritized |
| `unsized-images`, `uses-responsive-images`, `modern-image-formats` | Image sizing and bytes |

Audit ids and phase names change between Lighthouse versions; read `lighthouseVersion` and use
what the report contains. A field section (`loadingExperience` in PageSpeed Insights) appears only
when the page has enough Chrome UX Report traffic.

## Recording

Write the command, samples, statistic, spread and conditions into the record as you take them.
The capture's output quoted in Attribution is what lets someone else check the decision without
rerunning it.
