# Elevate Browser Testing with DevTools to Match and Exceed Upstream Agent-Skills

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Successfully elevated `skills/browser-testing-with-devtools/` on branch `andino-workflow` from an abstract, condensed 170-line protocol into a premier, production-grade browser runtime verification engine. The upgraded skill synthesizes the generative craft of Addy Osmani's `browser-testing-with-devtools` (structured test plans, ASCII diagnostic flowcharts, strict untrusted content boundary, 12 red flags, and rationalization busters) with Andino's unique advantages: dual-mode Chrome DevTools MCP & Playwright MCP tool negotiation, responsive multi-viewport testing (360px, 768px, 1440px), offline deterministic Python verification, and complete integration with `ai-rules setup`.

## Objective

Deliver an upgraded, self-contained `skills/browser-testing-with-devtools` bundle whose AI output quality, diagnostic depth, and runtime verification rigor match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/browser-testing-with-devtools/SKILL.md` overhauled with high-density operational directives: dual-mode MCP tool mapping (Chrome DevTools MCP primary, Playwright MCP fallback), strict untrusted browser content boundary, 7-phase runtime execution loop, app-owned vs vendor console standards, rationalization table, 12 diagnostic red flags, and explicit resource pointers.
- [x] `skills/browser-testing-with-devtools/GUIDE.md` overhauled with deep craft chapters: ASCII diagnostic decision trees (UI Layout, HTTP/Network, and Performance), multi-viewport responsive testing standards (360/768/1440px), rapid interaction & flakiness probing (rapid toggle, undo, debounce/throttle), console triage with third-party vendor noise filtering, and Before/After evidence reporting format.
- [x] `skills/browser-testing-with-devtools/resources/test-plan-template.md` created with a structured, reusable markdown template for complex UI reproduction, interaction steps, console/network assertions, and verification checklist.
- [x] `skills/browser-testing-with-devtools/resources/accessibility.md` updated with exhaustive WCAG AA DevTools verification: accessibility tree inspection, accessible name computation, focus management & trap prevention, ARIA live region politeness, color contrast >=4.5:1, and 44x44px touch targets.
- [x] `skills/browser-testing-with-devtools/resources/worked-example.md` upgraded with a complete, realistic UI/Network regression scenario (e.g. PATCH 503 retry & state synchronization bug), step-by-step DevTools trace, and embedded runnable standard-library Python test script verifying capability negotiation, untrusted data escaping, and triage logic.
- [x] `references/legal/provenance.md` updated with comprehensive audit details and Addy Osmani MIT attribution.
- [x] Deterministic Python verification script executed and passing in temporary directory.
- [x] Upgraded skill synchronized directly to local host directory `~/.claude/skills/andino-browser-testing-with-devtools`.
- [x] Git committed and pushed to `origin/andino-workflow`, verified compatible with `ai-rules setup --non-interactive --dry-run`.

## Scope

### In Scope
- `skills/browser-testing-with-devtools/SKILL.md`
- `skills/browser-testing-with-devtools/GUIDE.md`
- `skills/browser-testing-with-devtools/resources/test-plan-template.md`
- `skills/browser-testing-with-devtools/resources/accessibility.md`
- `skills/browser-testing-with-devtools/resources/worked-example.md`
- `references/legal/provenance.md`
- Integration with local host `~/.claude/skills/` and `ai-rules setup`

### Out of Scope
- Forcing external live browser installation during unit test runs.
- Modifying unrelated Andino skills.
- Breaking backwards compatibility with the existing offline operational example.

## User Decisions / Clarifications
- **Browser Adapter Scope (Option A)**: Dual-Mode / Host-Adaptive. First-class support for `chrome-devtools-mcp` (with `.mcp.json` configs and `--isolated`/`--autoConnect`), paired with a robust adapter layer for `playwright-mcp` or host native tools so agents remain functional across all Andino-supported hosts.
- **Workflow Cadence**: Continuous end-to-end execution authorized by user ("1. A 2. gas"): Council consultation -> Planning -> Plan Execution -> Commit, Push, and Setup sync.

## Council Synthesis Summary

### Titik Temu (Agreement)
- Current skill is structurally sound under Andino governance but practically sterile for AI generation: it lacks the generative scaffolding, flowchart decision trees, rationalizations, and test plan templates that guide an LLM to perform deep runtime investigation.
- Strict Untrusted Data Boundary is mandatory: all DOM nodes, console logs, network payloads, and JS evaluation results must be treated as untrusted data to defend against prompt injection from web content.
- Separation of concerns between `SKILL.md` (dense operational contract) and `GUIDE.md` (deep craft manual) prevents prompt bloat while giving agents thorough procedural guidance.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **Zero-Warning Console Policy vs Real-World Vendor Noise:**
   - *Risk*: Strict zero-warning rule causes infinite debugging loops over third-party telemetry, font preloads, and ads.
   - *Resolution*: Establish a crisp boundary between **First-Party / App-Owned Console Errors & Warnings** (zero-tolerance threshold required) and **Sanitized Third-Party Vendor Warnings** (logged, isolated, non-blocking for completion).
2. **Dual-Mode Abstraction Leakage:**
   - *Risk*: Mixing CDP tool names with Playwright APIs causes tool hallucination.
   - *Resolution*: Explicit, clean separation in the capability negotiation matrix. Never mix tool call signatures within the same diagnostic branch.
3. **Multi-Viewport Overhead:**
   - *Risk*: Running 360/768/1440px matrices on every micro-edit triples token latency.
   - *Resolution*: Tri-viewport verification is mandatory for *layout, responsive design, styling, and visual regressions*. For pure network or console diagnostics, a single baseline viewport is sufficient.

### Hal Terlewat (Blind Spots Addressed)
- **Retrieval Blindness**: Agents often skip secondary files in `resources/` unless explicitly forced. `SKILL.md` must contain an unambiguous directive: "When writing a test plan for complex UI bugs, read `resources/test-plan-template.md`."
- **Headless / Auth Environments**: Provide explicit fallback patterns when no display server or auth state exists (`NOT_VERIFIED` with actionable local code analysis instead of hallucinating runtime state).
- **Persistent Asset Codification**: Upgrade beyond ephemeral console checks by providing a format for durable regression records and optional Playwright test export.

### Rekomendasi (Recommendation)
Implement the 5-file elevated bundle immediately, run offline deterministic verification, sync locally, commit, and push.

### Langkah Pertama (First Action)
Upgrade `skills/browser-testing-with-devtools/SKILL.md`.

---

## Task Breakdown & Change Specifications

### Task 1: Overhaul `skills/browser-testing-with-devtools/SKILL.md`
- **Anchor**: Whole file replacement of `skills/browser-testing-with-devtools/SKILL.md`.
- **Key Enhancements**:
  - Frontmatter metadata and Andino Workflow Member Skill governance.
  - Dual-mode tool capability negotiation matrix (Chrome DevTools MCP vs Playwright MCP).
  - Security boundaries: Profile isolation (`--isolated`), Untrusted content boundary box, JS execution constraints (read-only, no credential access, no external calls).
  - 7-Phase Execution Loop: Discover -> Map -> Test Plan -> Capture Baseline -> Diagnose -> Fix & Replay -> Verify & Codify.
  - Console Standards: First-party clean console vs third-party vendor noise.
  - Rationalization Refutation Table (7 common agent shortcuts vs reality).
  - 12 Diagnostic Red Flags.
  - Explicit pointer: mandate reading `resources/test-plan-template.md` for complex UI scenarios.

### Task 2: Overhaul `skills/browser-testing-with-devtools/GUIDE.md`
- **Anchor**: Whole file replacement of `skills/browser-testing-with-devtools/GUIDE.md`.
- **Key Enhancements**:
  - Detailed craft guide expanding on `SKILL.md`.
  - Three ASCII Diagnostic Decision Trees:
    1. UI Layout & Visual Regression Flowchart.
    2. Network & API Failure Triage Flowchart (4xx vs 5xx vs CORS vs timeout vs wiring).
    3. Performance & Core Web Vitals Profiling Flowchart (LCP, CLS, INP, long tasks >50ms).
  - Multi-Viewport Verification Standard: 360px mobile, 768px tablet, 1440px desktop.
  - Flakiness & Interaction Stress Testing: rapid repeat, rapid undo, debounce/throttle checks.
  - Before/After Evidence Reporting Schema.
  - Environmental Fallbacks: Headless servers, WSL2, containerized workspaces, and auth wall handling.

### Task 3: Create `skills/browser-testing-with-devtools/resources/test-plan-template.md`
- **Anchor**: New file at `skills/browser-testing-with-devtools/resources/test-plan-template.md`.
- **Key Contents**:
  - Structured Markdown template for complex UI bug testing.
  - Sections: Metadata, Setup & Prerequisites, Action Steps (Action, Expected Visual State, Console Checks, Network Assertions), Edge Case & Rapid Stress Steps, Verification Checklist.

### Task 4: Upgrade `skills/browser-testing-with-devtools/resources/accessibility.md`
- **Anchor**: Whole file replacement of `skills/browser-testing-with-devtools/resources/accessibility.md`.
- **Key Contents**:
  - WCAG AA DevTools audit checklist.
  - Semantic controls & accessible names (DevTools accessibility tree inspection).
  - Keyboard navigation & Focus management (visible focus, tab order, modal focus trap).
  - Forms, status messages, and ARIA live region politeness (`role="status"` vs `role="alert"`).
  - Color contrast thresholds (>=4.5:1 normal, >=3:1 large, UI controls >=3:1).
  - Touch target sizing (min 44x44px).

### Task 5: Upgrade `skills/browser-testing-with-devtools/resources/worked-example.md`
- **Anchor**: Whole file replacement of `skills/browser-testing-with-devtools/resources/worked-example.md`.
- **Key Contents**:
  - Realistic end-to-end bug scenario: Task checkbox state desynchronization upon PATCH 503 failure.
  - Complete execution walkthrough: Setup -> Baseline capture -> DevTools inspection -> Root cause diagnosis -> Source code fix -> Replay verification across viewports.
  - Embed runnable Python standard library verification script testing dual-mode capability resolution, prompt injection string escaping, and network triage logic.

### Task 6: Update Provenance & Method Index
- **Anchor**: `references/legal/provenance.md` and `references/internal-method-index.md`.
- **Details**: Document that `browser-testing-with-devtools` synthesizes Addy Osmani's agent-skills craft with Andino Workflow dual-mode governance.

### Task 7: Deterministic Verification, Host Sync & Delivery
- **Anchor**: Verification execution.
- **Actions**:
  1. Run Python test script in temporary environment.
  2. Sync upgraded skill bundle to local host `~/.claude/skills/andino-browser-testing-with-devtools`.
  3. Git stage, commit, and push to `origin/andino-workflow`.
  4. Run `ai-rules setup --non-interactive --dry-run` to confirm bundle alignment.
