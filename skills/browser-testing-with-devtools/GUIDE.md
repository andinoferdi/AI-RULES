# Browser runtime verification guide

Internal method ID: `andino-browser-testing-with-devtools` (alias: `browser-testing-with-devtools`).

> **Andino Workflow Member Skill Guide**
> This guide provides the complete craft manual, diagnostic decision trees, responsive viewport protocols, and evidence schemas for browser testing with DevTools.

---

## 1. The DevTools Verification Mindset

Static code review answers the question: *"Does the code look syntactically and logically plausible?"*
Browser runtime verification answers the question: *"Does the rendered interface satisfy user invariants in an actual browser engine?"*

Modern web applications involve complex interactions between DOM generation, CSS cascade resolution, font loading, asynchronous event loops, network latencies, and device viewports. An AI agent that does not verify runtime browser state will regularly suffer from:
- **CSS Specificity Blindness:** Assuming a CSS rule applies when a higher-specificity selector or cascade layer overrides it.
- **Layout Collapses:** Missing flex/grid overflow, hidden scrollbars, or text truncations at narrow viewports.
- **Race Conditions:** Code that works on instant local mocks failing when real network latency delays a response.
- **Silent Failures:** Event listeners failing to fire due to unhandled promise rejections or z-index stacking overlays intercepting pointer clicks.

---

## 2. Diagnostic Decision Trees

### Flowchart 1: UI Layout & Visual Regression

```
┌──────────────────────────────────────────────────────────────┐
│  REPRODUCE: Navigate to page & trigger visual anomaly        │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  INSPECT DOM & COMPUTED STYLES                               │
│  - Inspect element in DOM tree (check tags, classes, attrs)   │
│  - Read computed styles (box model, display, position, flex) │
│  - Check accessibility tree (accessible name, role, state)   │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
                        Is element present
                           in the DOM?
                          /           \
                    YES  /             \  NO
                        /               \
                       ▼                 ▼
          ┌───────────────────────┐  ┌────────────────────────┐
          │ Check display,        │  │ Check component render │
          │ visibility, opacity,  │  │ conditions, data       │
          │ z-index, & overflow   │  │ hydration, & routing   │
          └───────────┬───────────┘  └───────────┬────────────┘
                      │                          │
                      ▼                          ▼
┌──────────────────────────────────────────────────────────────┐
│  DIAGNOSE ROOT CAUSE                                         │
│  - CSS clash / specificity override?                         │
│  - Flex/Grid container wrapping issue?                       │
│  - State variable missing or formatted incorrectly?          │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  FIX SOURCE & REPLAY                                         │
│  - Apply minimal source code edit in project                 │
│  - Reload page & wait for font / layout observers to settle  │
│  - Verify at 360px (mobile), 768px (tablet), 1440px (desktop)│
└──────────────────────────────────────────────────────────────┘
```

---

### Flowchart 2: HTTP & Network Failure Triage

```
┌──────────────────────────────────────────────────────────────┐
│  CAPTURE: Trigger user action while monitoring network       │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
                      Did the network request
                             fire?
                            /     \
                      YES  /       \  NO
                          /         \
                         ▼           ▼
┌────────────────────────────────┐  ┌──────────────────────────┐
│  ANALYZE HTTP STATUS CODE      │  │ EVENT WIRING DEFECT      │
│  - URL, Method (GET/POST/etc.) │  │ - Event listener missing │
│  - Request payload & headers   │  │ - Pointer event blocked  │
│  - Response status & payload   │  │ - Form preventDefault()  │
└───────────────┬────────────────┘  └──────────────────────────┘
                │
    ┌───────────┼───────────┬───────────┬───────────┐
    ▼           ▼           ▼           ▼           ▼
  2xx OK      4xx Client   5xx Server  CORS Block  Timeout
┌───────────┐┌───────────┐┌───────────┐┌───────────┐┌───────────┐
│State parse││Payload or ││Server log ││Origin /   ││Latency or │
│or UI render││URL path  ││or backend ││Preflight  ││oversized  │
│defect     ││mismatch   ││failure    ││headers    ││payload    │
└───────────┘└───────────┘└───────────┘└───────────┘└───────────┘
```

---

### Flowchart 3: Performance & Core Web Vitals Profiling

```
┌──────────────────────────────────────────────────────────────┐
│  BASELINE: Record DevTools Performance Trace during action   │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  INSPECT CORE WEB VITALS & METRICS                           │
│  - LCP (Largest Contentful Paint)   Target: <= 2.5s          │
│  - CLS (Cumulative Layout Shift)    Target: <= 0.1           │
│  - INP (Interaction to Next Paint)  Target: <= 200ms         │
│  - Long Tasks (> 50ms blocking main thread)                  │
└──────────────────────────────┬───────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
  High LCP (>2.5s)       High CLS (>0.1)        High INP (>200ms)
┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
│- Unoptimized image │ │- Images lack       │ │- Heavy JS on main  │
│- Render-blocking CSS││  width/height attrs│ │  thread (>50ms)    │
│- Slow server TTFB  │ │- Dynamic ad/banner │ │- Un-memoized list  │
│- Client hydration  │ │  injected late     │ │  re-renders        │
└────────────────────┘ └────────────────────┘ └────────────────────┘
```

---

## 3. Tri-Viewport Responsive Verification Standard

Web applications cannot be verified on desktop viewports alone. All visual and layout tasks must verify across three standard viewports:

| Viewport | Target Device | Key Inspection Focus |
|---|---|---|
| **360px** | Mobile Portrait | - Minimum 44x44px touch target sizes for buttons/links.<br>- No horizontal scrollbar (`document.body.scrollWidth === window.innerWidth`).<br>- Form inputs legible without pinch-zooming.<br>- Text wraps naturally without awkward word truncation. |
| **768px** | Tablet Portrait | - Multi-column layouts cleanly transition from single-column.<br>- Navigation drawer / mobile menu correctly toggles or adapts.<br>- Cards and grid items maintain proportional gutters. |
| **1440px** | Desktop Wide | - Maximum content container width constraint prevents over-stretching.<br>- Sticky headers / sidebars stay correctly pinned without content overlap.<br>- Typography maintains optimal reading line-length (45-75 characters). |

---

## 4. Rapid Interaction & Flakiness Probing

Bugs in real applications frequently stem from rapid user interactions that trigger race conditions or unhandled state transitions. When debugging interactive components, apply these three stress probes:

1. **Rapid Toggle Probe:**
   - Click the interactive element (checkbox, accordion, dropdown toggle) 5 times rapidly (<300ms intervals).
   - *Expected:* Component state remains completely consistent with final toggle; no animation stuck mid-flight; no DOM node duplication.
2. **In-Flight Rollback / Undo Probe:**
   - Trigger a mutating action that sends an HTTP request, then immediately trigger undo or cancel before the response returns.
   - *Expected:* Application handles optimistic rollback cleanly without crashing, double-rendering, or reverting to stale server state.
3. **Network Debounce / Throttle Probe:**
   - Type rapidly into a search or auto-complete input field.
   - *Expected:* Network monitor confirms requests are properly debounced; only the final search query fires; previous obsolete requests are aborted or ignored.

---

## 5. Console Health & Third-Party Noise Filtering

### Clean Console Rule
When testing local application code, any error or warning produced by the application under test indicates a defect. A task is **not verified** if first-party console errors remain.

### Categorizing Console Output

```
Console Message
  ├── First-Party / Application-Owned (MUST BE FIXED)
  │     ├── Uncaught Error / TypeError / ReferenceError
  │     ├── React "Each child in a list should have a unique key"
  │     ├── React "Warning: Can't perform a React state update on an unmounted component"
  │     ├── Failed fetch/XHR to application API endpoints
  │     └── CSP violation caused by project script or stylesheet
  │
  └── Third-Party / Vendor Telemetry (CATALOG & ISOLATE)
        ├── Sentry / Datadog / PostHog beacon blocked by ad-blocker
        ├── Google Analytics / Tag Manager script preload notice
        └── External CDN font preflight CORS notice
```

---

## 6. Dual-Mode Host Capability Negotiation

When executing browser verification, negotiate host tools using this precedence:

1. **Chrome DevTools MCP (Preferred):**
   - Full Chrome DevTools Protocol access.
   - Complete support for live DOM snapshots, computed CSS rules, network event streaming, performance traces, and isolated profiles.
2. **Playwright MCP (Fallback):**
   - High-level browser automation.
   - Use `browser_snapshot` for DOM, `browser_take_screenshot` for visual layout, `browser_console_messages` for logs, and `browser_network_requests` for traffic.
3. **Host-Native Browser (Fallback):**
   - Integrated IDE or platform browser tools. Use available inspection panels.
4. **Restricted / Headless / Unavailable Environment:**
   - If no browser tool is configured, authorized, or functional in the current environment (e.g. headless CI container without Xvfb), do **not** simulate or fabricate browser results.
   - Perform thorough local source code analysis, write unit/component tests, and explicitly mark runtime browser verification as:
     `Runtime Browser Verification: NOT_VERIFIED (No active browser MCP connection)`

---

## 7. Standard Before/After Evidence Reporting Format

When completing browser testing, document the findings in this structured schema for task plans, pull requests, or handoffs:

```markdown
### Browser Runtime Verification Report

**Target URL:** `http://localhost:3000/tasks`
**Active Browser Tool:** Chrome DevTools MCP (`--isolated` temporary profile)

#### 1. Baseline Observations (Before Fix)
- **Visual State:** Checkbox checked, but strikethrough animation missing.
- **Console:** 1 Uncaught Exception: `TypeError: Cannot read properties of undefined (reading 'status')`
- **Network:** `PATCH /api/tasks/42` returned `503 Service Unavailable` (Duration: 820ms).
- **Screenshot:** Captured at 360px and 1440px showing desynchronized checkbox state.

#### 2. Root Cause Analysis
- Component failed to handle 5xx server rejection in optimistic UI update; state was never reverted when PATCH failed.

#### 3. Applied Remediation
- Added `.catch()` block in `src/components/TaskItem.tsx:48` to roll back local task status and dispatch an accessible toast notification via `aria-live="polite"`.

#### 4. Verification & Stress Testing (After Fix)
- **Replay:** Checkbox correctly rolls back to unchecked when PATCH fails with 503.
- **Rapid Toggle:** 5x rapid toggle executed; state remains strictly consistent with zero duplicate requests.
- **Console Health:** 0 Errors, 0 Warnings (Clean Console Standard satisfied).
- **Viewports Verified:**
  - 360px: Pass (touch targets 48x48px, no horizontal scroll).
  - 768px: Pass (grid adapts correctly).
  - 1440px: Pass (container bounded at 1200px max-width).
- **Accessibility:** Retry button has accessible name; error announced to screen readers.
```

---

## 8. Offline Operational Verification Example

The script below demonstrates standard-library triage and capability negotiation logic used for offline self-tests and CI pipelines:

```python andino-operational-example
import json, os

def triage_network(capture):
    if not capture.get("requests"):
        return "event-wiring"
    req = capture["requests"][0]
    if capture.get("cors"):
        return "origin-policy"
    status = req.get("status", 0)
    if status >= 500:
        return "server-failure"
    if status >= 400:
        return "client-contract"
    if req.get("duration_ms", 0) > 3000:
        return "network-timeout"
    return "render-state"

def test_triage():
    sample = {
        "requests": [{"method": "PATCH", "status": 503, "duration_ms": 820}],
        "console": ["Uncaught (in promise) Error: Server 503"]
    }
    if os.getenv("ANDINO_NEGATIVE"):
        sample["requests"] = []
    return {
        "layer": triage_network(sample),
        "requests": len(sample["requests"]),
        "has_console_errors": len(sample["console"]) > 0,
        "offline_verified": True
    }

if __name__ == "__main__":
    print(json.dumps(test_triage(), sort_keys=True))
```

Expected default output:
```json
{"has_console_errors": true, "layer": "server-failure", "offline_verified": true, "requests": 1}
```

---

## 9. Provenance

Adapted and elevated from Addy Osmani's `agent-skills`, source `skills/browser-testing-with-devtools/SKILL.md` (Addy Osmani MIT Notice: [references/license.md](references/license.md)). Enhancements include triple ASCII diagnostic flowcharts, 360/768/1440px multi-viewport standards, rapid interaction flakiness probing, and offline standard library validation.
