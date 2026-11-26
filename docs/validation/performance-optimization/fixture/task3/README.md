# render-worker

Long-running worker that renders notification e-mails. Each request names a template, a locale
(`en`, `id` or `nl`) and a context, and carries a `request_id` for tracing.

- `render/templates.py`: compiles templates and renders them.
- `render/catalog.py`: template sources and translated strings.
- `render/log.py`: structured JSON event log (keeps the last 1,000 events for the debug page).
- `python -m render.soak [--requests 3000]` replays a production-like mix of requests and
  prints progress with the memory traced by `tracemalloc`.
- `python -m unittest` runs the tests.

The worker runs in a container with a 512 MB memory limit and serves about 40 requests per
second at peak.
