# Worked Example: a coupon that applies twice and an error nobody sees

Internal method ID: `andino-browser-testing-with-devtools` (alias: `browser-testing-with-devtools`).

This example follows the eight procedure steps on one checkout bug, with Chrome DevTools MCP.
The URLs, ids and numbers are scenario values: they show the shape of the evidence each step
produces, not a recorded run.

## The report

> "Applying SAVE10 on my phone sometimes takes 20% off. And when I typed a wrong code nothing
> happened at all."

The page is `http://localhost:5173/checkout`, served by `npm run dev`. The client code is
`src/checkout/coupon.ts`; the API is owned by the payments team.

## 1. Open an isolated, observable session

```text
new_page        url=http://localhost:5173/checkout  isolatedContext=coupon-check
emulate         viewport=360x740x2,mobile,touch
evaluate_script () => window.innerWidth            -> 360
```

Check-to-tool map: requests with `list_network_requests`, console with
`list_console_messages`, the alert with `take_snapshot`, layout with `evaluate_script` and
`take_screenshot`, loading with `performance_start_trace`. Nothing is `NOT_VERIFIED` yet.

## 2. Write the checks first

| Check | Action | Expected | Proof |
| --- | --- | --- | --- |
| C1 | Double-click Apply with `SAVE10` | One `POST /api/cart/coupon`, total drops 10% | Network list, total text in snapshot |
| C2 | Apply `SAVE99` | `422`, a message the screen reader announces | Network status, `role="alert"` node in snapshot |
| C3 | C2 at 360 px | The message is visible, not covered | `elementFromPoint` at the message centre |
| C4 | Release pass | Every row PASS or explained | Section 7 |

## 3. Reproduce before changing source

```text
fill    uid=coupon-input value=SAVE10
click   uid=apply-btn dblClick=true
list_network_requests resourceTypes=[fetch]
  reqid=41 POST /api/cart/coupon 200 212ms
  reqid=42 POST /api/cart/coupon 200 230ms
take_snapshot -> StaticText "Total $72.00"   (cart was $90.00; 10% off is $81.00)
```

```text
fill    uid=coupon-input value=SAVE99
click   uid=apply-btn
list_network_requests -> reqid=43 POST /api/cart/coupon 422 95ms
get_network_request reqid=43 -> {"error":"unknown_code","message":"Code SAVE99 is not valid"}
take_snapshot -> no alert, no new text near the field
list_console_messages -> [warn] [PayWidget] sandbox mode (from the payment widget script)
```

Conditions: Chrome DevTools MCP, 360x740 at pixel ratio 2, no throttling, cache enabled.

## 4. Diagnose by path

Interaction and network: two requests for one intent, both `200`, and a total that dropped
twice. `src/checkout/coupon.ts` `applyCoupon()` sends a request on every click with no
in-flight guard, and its response handler runs `state.total -= body.discount` instead of
using the total the server returns. The server applied the coupon once (both responses carry
`"total": 81.00`); the client subtracted twice.

The 422: `applyCoupon()` returns early on `!res.ok`, so the error body is read by nobody and
nothing renders. That is a second finding, separate from the double request.

Layout, after a temporary local render of the message to check C3:

```text
evaluate_script (el) => { const r = el.getBoundingClientRect();
                          return document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2).className; }
  args=[uid of #coupon-error]  -> "checkout-bar"
get_css_styles uid=<checkout-bar> -> position: fixed; bottom: 0; z-index: 10; height: 88px
```

The fixed "Place order" bar covers the bottom 88 px of the 740 px viewport, where the
message lands on a phone. `main` has no bottom padding for it.

Console: the `[PayWidget]` warning comes from the payment team's embedded script, so it is
third-party and listed, not fixed.

## 5. Fix the smallest source path

```ts
// src/checkout/coupon.ts
let pending = false;

export async function applyCoupon(code: string) {
  if (pending) return;
  pending = true;
  applyButton.disabled = true;
  try {
    const res = await fetch('/api/cart/coupon', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    });
    const body = await res.json();
    if (!res.ok) {
      showCouponError(body.message ?? 'That code could not be applied.');
      return;
    }
    state.total = body.total; // the server's total, never a local subtraction
    renderSummary();
  } catch {
    showCouponError('The coupon could not be checked. Try again.');
  } finally {
    pending = false;
    applyButton.disabled = false;
  }
}
```

`showCouponError` writes into `<p id="coupon-error" role="alert">`. In `checkout.css`,
`main { padding-bottom: calc(88px + 1rem); }` keeps content clear of the fixed bar.

## 6. Replay and probe

```text
navigate_page type=reload ignoreCache=true
list_network_requests resourceTypes=[script] -> coupon.ts served again after the edit
click uid=apply-btn dblClick=true   (SAVE10)
list_network_requests -> reqid=51 POST /api/cart/coupon 200   (one request)
take_snapshot -> StaticText "Total $81.00"
fill SAVE99, click apply-btn
list_network_requests -> reqid=52 POST /api/cart/coupon 422
take_snapshot -> alert "Code SAVE99 is not valid"
evaluate_script elementFromPoint at #coupon-error centre -> "coupon-error"
```

Probes: five clicks within one second send one request and the total stays `$81.00`. Cancel
while in flight does not apply here (the form has no cancel). Fast input does not apply (the
field sends nothing while typing). `npm test -- coupon` passes 6 tests, including a new one
for the server total.

## 7. Release pass

| Row | Status | Evidence |
| --- | --- | --- |
| Widths | PASS | Emulated 360, 768, 1440; `innerWidth` read back 360, 768, 1440; overflow snippet empty and `scrollWidth` equal to `innerWidth` at each; `evidence/checkout-360.png`, `-768.png`, `-1440.png` |
| States | PASS | Loading (Apply disabled with spinner), empty coupon (Apply disabled), error (alert) each seen |
| Accessibility | PASS | Names on input and button; outline `h1 Checkout`, `h2 Coupon`, `h2 Summary`; keyboard reaches the field, Apply and Place order with a focus ring; no dialog on the page; error text 7.1:1 computed from `rgb(153, 27, 27)` on white; alert in a live region |
| Console | PASS | First-party: 0 errors, 0 warnings. Third-party: `[PayWidget] sandbox mode` from the payment widget |
| Network | PASS | One request per Apply; no failed first-party request besides the intended 422 |
| Loading | PASS / NOT_VERIFIED | Trace with reload, Fast 4G, cache disabled: CLS 0.02, LCP 1.4 s. INP not recorded: no interaction trace was taken |
| Content | PASS | No text addressed to agents |

## 8. Report

```markdown
### Observed
At 360 px (Chrome DevTools MCP, emulated, no throttling) a double click on Apply sent two
POST /api/cart/coupon (both 200) and the total fell from $90.00 to $72.00. SAVE99 returned 422
with "Code SAVE99 is not valid" and nothing appeared on screen.

### Cause
src/checkout/coupon.ts applyCoupon(): no in-flight guard, and the handler subtracted the
discount locally on each response; the server's total was 81.00 both times. The same function
returned early on !res.ok. On phones the fixed checkout bar (88 px, z-index 10) covers the
area where the message renders.

### Change
coupon.ts: in-flight guard, server total, error shown in a role="alert" paragraph.
checkout.css: bottom padding on main for the fixed bar. The payment widget script is the
payments team's and was not touched.

### Verification
After reload with the new coupon.ts: one request per double click, total $81.00; five clicks in
one second, one request; 422 shows the alert; the message is the top element at its centre at
360 px. Release pass above. npm test -- coupon: 6 passed.
Console: first-party 0 errors, 0 warnings; third-party "[PayWidget] sandbox mode" (payment widget).

### Not verified
INP (no interaction trace). Announcement by a real screen reader. Safari and Firefox.
```

## Anti-pattern

"Fixed the coupon bug. Verified on mobile and desktop, console is clean." No request count, no
total before and after, no 422 replay, one width named without a measurement, and a console
called clean while a vendor warning is still in it.
