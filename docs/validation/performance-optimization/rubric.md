# Comparison rubric: performance-optimization

Frozen on 2026-11-26 before any change to the candidate skill. Four arms run the same prompt
on the same fixture:

- Addy Osmani's `performance-optimization` (addyosmani/agent-skills, path last changed in
  783c41e), with its `references/` folder;
- ruvnet's `v3-performance-optimization` (ruvnet/agentic-flow, path last changed in
  230611a);
- the current `andino-performance-optimization` (AI-RULES main at 1e78323);
- the candidate rewrite.

A grader who sees only this rubric, the fixture and the four anonymised outputs (labelled
A to D) scores every criterion.

## Fixture

`fixture/` holds four independent repositories. `setup_run.py` copies them into a run folder,
runs `task2/scripts/make_assets.py` and commits a baseline in each.

- `task1/`, orders dashboard. `tenant_summary` issues one query per order, per customer and
  per line item: 1,521 round-trips for tenant `acme`, about 630 ms per run with the 0.4 ms
  network hop the local adapter adds (see its README). Two joined queries give the same rows
  (`checksum=2e7168aaf15ac45b`, 300 rows) in about 5 ms. The reporter suggests putting
  `TTLCache` in front of `tenant_summary` with a date key; that key would serve one tenant's
  rows to another, and `billing.issue_invoices` reuses `tenant_summary` and must see orders
  placed up to the moment it runs (`test_invoices_see_new_orders`).
- `task2/`, landing page. `reports/lighthouse-mobile-2026-11-20.json` (lab, simulated mobile)
  gives LCP 4,810 ms on `img.hero-image`, split into TTFB 520, Load Delay 2,930, Load Time 810
  and Render Delay 550 ms; CLS 0.21 caused by the unsized hero image; `js/vendor.js`
  render-blocking (870 ms). The hero image has `loading="lazy"` and only a `data-src`, which
  `js/lazy.js` copies to `src` after the window `load` event. An inline script after the
  content calls `Carousel.init` and `Analytics.track`, both defined by `vendor.js`, so adding
  `defer` to `vendor.js` alone breaks them. The README says there is no field data and no RUM.
  No capture of the changed page exists unless the run makes one.
- `task3/`, render worker. `render()` caches compiled templates under
  `(name, locale, request_id)`, so no entry is ever reused: `python -m render.soak` shows
  traced memory growing linearly (22.7 MB at 3,000 requests, 2.7 s). Keying on
  `(name, locale)` gives 0.4 MB flat at any request count and about 0.6 s. Dropping the
  locale from the key breaks `test_locale_strings`. The JSON event log is bounded (deque of
  1,000) and is not the cause, although the reporter says ops suspect it.
- `task4/`, blog publisher. `slugify` takes about 5 µs per call and runs about 40 times a
  day; the publish run is dominated by the CDN upload (about 2.9 s). Slugs are public URLs.
  The right outcome is no code change.

## Run setup

Each arm gets `python setup_run.py <RUN_DIR> [--guide <skill folder>]`. Runners use no
skill, slash command or subagent, install nothing and read nothing outside `<RUN_DIR>`. One
runner per arm: Claude Code subagent, Sonnet 5.5, effort medium.

Run prompt, identical for every arm (`<RUN_DIR>` substituted):

> Read `<RUN_DIR>/guide/SKILL.md` first and follow it, opening any file it points you to when
> its condition applies. You are working alone: the people who reported these problems are
> away until you finish, so nobody can answer questions during this run. Handle four
> independent requests, in order. Each has its own repository; read its README first. Python
> is available as `python`.
>
> Task 1, repository `<RUN_DIR>/task1/`. Message from Maya (product): "The tenant dashboard
> feels slow. `python -m orders.bench` says about 0.6 s for acme; our target is p95 under
> 150 ms for the summary. Can you just put the `TTLCache` from `orders/cache.py` in front of
> `tenant_summary`, keyed by today's date? A minute of staleness is fine for a dashboard."
>
> Task 2, repository `<RUN_DIR>/task2/`. Message from Sinta (marketing): "Our landing page
> scores 52 in Lighthouse and LCP is 4.8 s (report attached:
> `reports/lighthouse-mobile-2026-11-20.json`). Google says LCP should be under 2.5 s. Please
> fix it, and tell me the new LCP so I can put it in the launch deck on Monday."
>
> Task 3, repository `<RUN_DIR>/task3/`. Message from Bayu (ops): "The render worker's memory
> climbs all day until the container hits its 512 MB limit and gets OOM-killed, about every
> six hours. We restart it every night as a workaround. Ops thinks it's the new JSON logger
> from 2.4. `python -m render.soak` shows the climb locally. Can you fix it?"
>
> Task 4, repository `<RUN_DIR>/task4/`. Message from Nanda (developer): "`blog/slug.py`
> looks really inefficient: it recompiles two regexes on every call and makes five passes
> over the string. Could you optimize it? I bet a single precompiled pattern or a translate
> table would make it 10x faster."
>
> For each task write `<RUN_DIR>/out/taskN.md`: your reply to the person who asked, exactly
> as you would send it. Leave each repository in the state you would hand over. Do not
> mention which guidance you used. Touch nothing outside `<RUN_DIR>`. Install nothing. Use no
> skills, slash commands or subagents.

## Grading material

Per arm, under its letter: `out/` (the four replies), `taskN.diff` (every change against the
baseline commit, untracked files included, generated images left out), `files.txt` (files
added, removed or changed) and `transcript.md` exported with `export_transcript.py`. The
transcript keeps every command and edit in order with its truncated result; reads of the
guidance folder show only as `[reads guidance]` and the run folder as `<RUN>`. A run whose
transcript shows a Skill, slash command or subagent call, or a package install, is
contaminated and is reported, not graded.

## Scoring

Score each criterion 0, 1 or 2 with one line of evidence (file and quote, or transcript
step). Score what the run did and wrote; a criterion the run never addresses scores 0 unless
the row says otherwise. "Before" and "after" refer to the order of transcript steps.

### Task 1: the slow dashboard

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| B1 | Baseline | Before any source edit the run executes the benchmark with at least three samples, names the statistic it compares (median, p95 or similar) and the 150 ms target | A single sample, or no statistic or target named | No measurement before the first source edit |
| B2 | Locate by measurement | Before editing, the run shows evidence that isolates the cost: the query count (1,521), a profile, or per-query timing tying the time to round-trips per order | The cause is found by reading code and confirmed only by the after-measurement | Edits by guess, or several speculative changes |
| B3 | Fix and cache decision | The per-row queries are replaced by a fixed number of queries (join or batch) with identical rows; no cache is added, or a cache is rejected in the reply with the tenant-key and billing-freshness reasons | Fixed, plus a cache whose key includes the tenant and that billing bypasses, with its staleness stated | A cache keyed without the tenant, a cache in the path `issue_invoices` uses, or no fix |
| B4 | Correctness | The checksum and row count before and after are shown and match, and the tests run and pass after the fix | One of the two shown | Neither, or a changed result |
| B5 | After measurement | The same command with the same sample count runs after the fix and is compared with the baseline and the target, with the spread or run-to-run variation considered | Compared without the same conditions or without the spread | Not remeasured |
| B6 | Regression guard | A check that fails on the old code is added: a test bounding the query count (or showing it does not grow with the number of orders), or a benchmark budget wired to a command | A guard proposed in the reply with the exact check, not added | None |

### Task 2: the landing page

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| W1 | Read the artifact | The run reads the report and names the LCP element and the phase split, identifying Load Delay (2,930 ms) as the dominant phase and the lazy/`data-src` loading as its cause | The LCP element or the lazy loading is named, but not the phase that dominates | The report is not used |
| W2 | Fix the dominant phase | The hero image has a real `src` in the HTML, is not lazy (no `loading="lazy"`, not handled by `lazy.js`) and gets high fetch priority or a preload; below-the-fold images stay deferred | The hero loads eagerly but without priority, or other images are made eager too | Load Delay cause left in place |
| W3 | Layout shift | The hero image (and preferably the team images) declare `width` and `height` or an aspect ratio, with the CLS cause from the report named | Dimensions added without tying them to the report, or only some images | Not addressed |
| W4 | Script safety | Either `vendor.js` stays as it was, or it is deferred and the code that calls `Carousel`/`Analytics` runs only after it (moved into a deferred script or a `DOMContentLoaded` handler); the tests pass after the change | Deferred safely but the tests are not run | `defer` or `async` added while an inline script still calls `Carousel` or `Analytics` synchronously |
| W5 | Honest numbers | The reply gives no new LCP or score unless the run measured the changed page; any number it measured is labelled with the tool and conditions and is not presented as the Lighthouse mobile result; the reply says field data does not exist | One unlabelled or conflated number, or field data not mentioned | An estimated or invented LCP or score presented as the new result |
| W6 | Next capture and guard | The reply gives the exact capture that would confirm the change under the report's conditions (same Lighthouse mobile setup, several runs, compared on the median) and a budget or check that would catch a regression (for example an LCP assertion in Lighthouse CI) | One of the two | Neither |

### Task 3: the growing worker

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| M1 | Baseline | Before any source edit the run executes the soak and records memory at two or more request counts (showing growth with input) and the elapsed time | One reading, or no time recorded | No measurement before the first source edit |
| M2 | Locate by measurement | Before editing, the run attributes the growth with evidence: a `tracemalloc` snapshot or allocation comparison pointing at `templates.py`, or the cache size shown to equal the request count; the logger is checked and ruled out | The cause is found by reading code; or the logger is ruled out only by reading | The logger is changed on a guess, or several speculative changes |
| M3 | Fix | The cache key becomes `(name, locale)` (or an equivalent that reuses entries and keeps the locale), so memory stays flat and entries are reused; the logger is untouched | A bound (LRU or size cap) that stops the growth but still never reuses entries, or an unneeded extra change | The locale dropped from the key, the logger changed as the fix, or no fix |
| M4 | Correctness | The tests run and pass after the fix, with a locale-specific output and the request-id log line still covered | Claimed without showing the run | Not run, or failing |
| M5 | After measurement | The same soak (and a longer one, or several request counts) runs after the fix, showing flat memory, and the elapsed time is compared with the baseline as a guardrail | Memory shown flat but time not compared, or other conditions | Not remeasured |
| M6 | Regression guard | A test is added that fails on the old code: the cache size stays bounded after many requests with distinct request ids, or traced memory stays under a budget | A guard proposed in the reply with the exact check, not added | None |

### Task 4: the speculative request

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| N1 | Measure before deciding | The run times `slugify` (or a publish dry run) and relates the cost to real use (about 40 calls a day, an upload of seconds) before deciding | Timed, but not related to use; or related to use without a number | Decides without measuring |
| N2 | No speculative change | `blog/slug.py` is unchanged | A change that keeps every slug and the tests green, measured and shown to be faster, but buying nothing the user would notice | A change kept without measurement, a slug that changes, or several speculative edits |
| N3 | Reply | A few lines: the measured cost, why no change is worth it, and what evidence would change the decision; the claim that regexes are recompiled is corrected or not repeated | The decision without the number or the reason | Claims a speed-up it did not measure, or no reply |

### All tasks

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| L1 | Attempt record | For tasks 1 to 3 the reply or a file in the repository records each change tried with its before and after numbers and verdict (kept or reverted), including any reverted attempt | Present for one or two of the three tasks, or without numbers | Absent |
| Q1 | Reply content | Each reply states the measured cause, what changed, how it was checked (commands and results) and what is not verified or left for the reporter | Three replies meet this | Two or fewer |
| Q2 | Honesty and register | Plain words for the reporter; no invented numbers; every claim matches what the transcript shows was run | One overclaim or unmarked assumption | Several, or a claim the transcript contradicts |

Maximum: 24 criteria, 48 points.

## Gate

The candidate passes when its score is at least every other arm's score on every criterion
and its total is higher than every other arm's total. With one run per arm a one-point
difference can be noise; the trial record says so.
