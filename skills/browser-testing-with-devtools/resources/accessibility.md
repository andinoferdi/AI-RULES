# Accessibility Runtime Verification Checklist

Internal method ID: `andino-browser-testing-with-devtools` (alias: `browser-testing-with-devtools`).

Use Chrome DevTools MCP or Playwright MCP to inspect the live accessibility tree and audit rendered components against WCAG 2.1 AA standards.

---

## 1. Inspecting the DevTools Accessibility Tree

Automated DOM linters only catch a fraction of accessibility defects. Use browser DevTools to inspect how the browser engine computes the accessibility tree:

1. **Accessible Name Computation:**
   - Every interactive control must have an accessible name calculated by the browser.
   - Verify `<button>` elements contain text or an `aria-label`.
   - Verify `<input>` fields are explicitly associated with `<label for="id">` or `aria-labelledby`.
   - Icon-only buttons (e.g. search icons, hamburger menus) MUST have an accessible name (`aria-label="Search"`).
2. **Accessible Role Verification:**
   - Use native HTML elements whenever possible: `<button>` for actions, `<a href>` for navigation.
   - Avoid clickable `<div>` or `<span>` elements. If custom components are unavoidable, verify `role="button"`, `tabindex="0"`, and keyboard event handlers are present.

---

## 2. Keyboard Navigation & Focus Management

Test keyboard interactions purely using keyboard events in the browser:

- [ ] **Sequential Focus Navigation:**
  - Pressing `Tab` navigates through all interactive controls in a logical reading order.
  - No interactive control is skipped or unreachable via keyboard.
- [ ] **Visible Focus Indicator:**
  - Every focused element has a visible, high-contrast focus ring (never use `outline: none` without providing an accessible custom focus style).
- [ ] **Modal & Overlay Focus Trapping:**
  - When a dialog/modal opens, focus immediately moves inside the dialog.
  - Tabbing cycles exclusively within the modal while it remains open (no focus leak to background page).
  - Pressing `Escape` closes the dismissible overlay.
  - Upon closing, focus restores cleanly to the element that triggered the modal.
- [ ] **Skip Links:**
  - For pages with lengthy navigation headers, verify a "Skip to main content" link appears when the user first tabs into the page.

---

## 3. Forms & Dynamic Error States

- [ ] **Explicit Label Association:**
  - Every `<input>`, `<select>`, and `<textarea>` has a programmatic label matching its `id`.
  - Placeholder text is NOT a replacement for a visible label.
- [ ] **Error Announcement & Described-By:**
  - Validation error messages must be linked to their input via `aria-describedby="error-id"`.
  - Never convey error state using color alone (e.g. a red border without descriptive error text fails WCAG).
  - Invalid inputs must expose `aria-invalid="true"`.
- [ ] **Form Submission Error Summary:**
  - On failed submission, focus moves to a top-level error summary or the first invalid field.

---

## 4. Visual Contrast & Target Sizing

- [ ] **Color Contrast Ratios:**
  - Normal text (< 18pt / < 14pt bold): minimum **4.5:1** contrast against background.
  - Large text (>= 18pt / >= 14pt bold): minimum **3.0:1** contrast against background.
  - User interface components & graphical objects (borders, icons): minimum **3.0:1** contrast.
- [ ] **Touch Target Sizing:**
  - On mobile viewports (360px), all tap targets (buttons, links, form controls) must measure at least **44 x 44px** (including padding).
- [ ] **Zoom & Text Resizing:**
  - Page layout remains functional and legible when browser text is zoomed to 200% without clipping or horizontal overflow.
- [ ] **Flashing & Motion:**
  - No elements flash more than 3 times per second. Respect `prefers-reduced-motion` media queries.

---

## 5. Dynamic Content & ARIA Live Regions

- [ ] **Polite Status Announcements:**
  - Non-urgent dynamic updates (e.g., "Saved to draft", "Search results updated", "Item added to cart") use `role="status"` or `aria-live="polite"`.
- [ ] **Urgent Alert Announcements:**
  - Time-sensitive critical errors (e.g., "Session expiring in 1 minute", "Network disconnected") use `role="alert"` or `aria-live="assertive"`.
- [ ] **Loading & Busy States:**
  - During asynchronous loading, containers expose `aria-busy="true"`. Avoid continuously announcing incremental loading frames.

---

## 6. Provenance & Attribution

Adapted from Addy Osmani's `agent-skills`, source `skills/browser-testing-with-devtools/resources/accessibility.md` (Addy Osmani MIT Notice: `references/legal/addy-license.md`), with independent Andino Workflow WCAG 2.1 AA criteria and DevTools tree inspection rules.
