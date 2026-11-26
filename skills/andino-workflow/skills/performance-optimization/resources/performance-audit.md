# Web performance audit

Open this when a browser-rendered page is slow: a Lighthouse or PageSpeed report, a trace, field
data, or a complaint about load, layout shift or responsiveness.

## Core Web Vitals

| Metric | Good | Needs improvement | Poor |
| --- | --- | --- | --- |
| LCP (Largest Contentful Paint) | ≤ 2.5 s | ≤ 4.0 s | > 4.0 s |
| INP (Interaction to Next Paint) | ≤ 200 ms | ≤ 500 ms | > 500 ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

Assessed at the 75th percentile of real page loads (field data). Source: web.dev "Web Vitals",
read 2026-11-26; thresholds can change, so check the current page when a decision depends on
them. Project budgets, when they exist, govern.

## Lab versus field

- **Lab** (Lighthouse, PageSpeed lab section, a DevTools trace, a local headless run): one device
  and network profile, reproducible, good for finding causes and for CI budgets. Lighthouse
  cannot measure INP; Total Blocking Time is its proxy.
- **Field** (Chrome UX Report, PageSpeed field section, a RUM library such as `web-vitals`): real
  users at p75 over a window (CrUX: rolling 28 days). It confirms an improvement; it does not
  react within a day.
- A page with little traffic has no CrUX data. Say so instead of quoting a lab number as user
  experience.

## LCP by subpart

Split the LCP time into four subparts (web.dev "Optimize LCP"; Chrome "LCP breakdown") and work on
the largest:

| Subpart | Spans | Usual causes | Fixes |
| --- | --- | --- | --- |
| Time to first byte | Navigation start to first HTML byte | Slow server, no caching, redirects, distant origin | Cache the HTML or its data, serve from an edge, remove redirects; profile the backend route |
| Resource load delay | First byte to the start of the LCP resource download | Image not in the initial HTML (set by script, CSS background, client rendering); `loading="lazy"` on the LCP image; low priority | Put the URL in the HTML as a real `src`, never lazy-load the LCP image, add `fetchpriority="high"`, or `<link rel="preload">` when the URL is only known to CSS or script |
| Resource load duration | Download time of the resource | Large file, old format, no responsive sizes, slow host | Serve sized variants with `srcset`/`sizes`, AVIF or WebP, compress, use a CDN |
| Element render delay | Resource loaded to element painted | Render-blocking CSS or synchronous scripts in `<head>`, long main-thread tasks, content hidden by A/B or consent scripts, element inserted late by script | Defer or async non-critical scripts, inline only small critical CSS, break long tasks, render the element in HTML |

web.dev's guide: the two delay subparts should be near zero, and most of the time should go to
TTFB and load duration. Shrinking the download alone can move the time into render delay when
rendering is still blocked; remeasure the split, not only the total.

**Deferring scripts safely.** `defer` runs a script after parsing, in order; `async` runs it
whenever it arrives. Before deferring a script, find every inline script or attribute handler
that calls what it defines. Move those calls into a deferred script after it, or into a
`DOMContentLoaded` listener, or the page breaks while the score improves.

## Layout shift (CLS)

- Give every image, video and iframe `width` and `height` attributes, or a CSS `aspect-ratio`.
- Reserve space for ads, embeds and late content; insert new content below the viewport or in
  response to a user action.
- Fonts: preload the critical font, use `font-display` deliberately, and match fallback metrics
  (`size-adjust`) to reduce the swap shift.
- Animate `transform` and `opacity`, not properties that move layout.

## Responsiveness (INP)

Trace the slow interaction and split it: input delay (main thread busy when the user acted),
processing (event handlers), presentation delay (rendering after the handlers). Break long
tasks, yield to the main thread, debounce expensive handlers, avoid forced synchronous layout,
and keep DOM size moderate. Field INP attribution (the `web-vitals` attribution build) names the
element and phase.

## Honest scorecard

| Metric | Value | Unit | Source | Target | Status |
| --- | --- | --- | --- | --- | --- |
| LCP | 3,900 | ms | Lighthouse 12, mobile, simulated throttling, 2026-11-02 | ≤ 2,500 | Poor |
| LCP after change | NOT MEASURED | | | ≤ 2,500 | Pending: rerun the same Lighthouse config 5 times, compare medians |
| CLS | 0.04 | | same run | ≤ 0.1 | Good |
| INP field | NOT MEASURED | | no CrUX data for this page | ≤ 200 ms | Unknown |

Static source review produces potential findings only: name the location, the expected effect
and the capture that would confirm it. Source cannot produce LCP, INP or CLS values.

## Budgets and regression guards

Lighthouse CI asserts lab metrics on every change (a proposal until it runs here):

```json
{
  "ci": {
    "collect": { "numberOfRuns": 5 },
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500, "aggregationMethod": "median" }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1, "aggregationMethod": "median" }],
        "total-blocking-time": ["warn", { "maxNumericValue": 200, "aggregationMethod": "median" }]
      }
    }
  }
}
```

Save as `lighthouserc.json` and run `npx --package=@lhci/cli lhci autorun` in CI; it uses
Lighthouse's default mobile emulation, matching a mobile report. The CLI package is `@lhci/cli`; the unscoped `lhci` on npm is a different package. Pair lab budgets
with a byte budget for JavaScript and images, and, where real-user monitoring exists, an alert on
a meaningful p75 movement.

Browser APIs such as speculation rules, view transitions, `scheduler.yield` and the Long
Animation Frames API need a current support check before use.

Provenance: independently worded adaptation of Addy Osmani's `performance-optimization`
(addyosmani/agent-skills 783c41e, MIT) plus web.dev and Chrome documentation; notice in
[../references/license.md](../references/license.md).
