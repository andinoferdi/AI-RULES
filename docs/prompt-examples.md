# Prompt examples

Copy-ready Layer 2 prompts for the tasks developers hand to coding agents most often, such as new
features, bug fixes, tests, reviews, docs and questions, plus the specialist work AI-RULES and
its companion skills and MCP servers cover. Every example follows the rules in
[How to Prompt](../README.md#how-to-prompt):

- Slots appear in a fixed order: `Skills`, `Tools/MCP`, `Mode`, `Task`, `Context/evidence`,
  `Done when`, `Constraints`. **Task**, **Context/evidence** and **Done when** are always there;
  the rest appear only when they change the result.
- `Skills` lists only skills the workflow cannot infer. It never lists an `andino-*` member.
- `Mode` is `brainstorm first`, `plan only` or `just do it`. Omitting it means "just do it".
- `[brackets]` mark what you fill in.

The comment under each heading (`# workflow picks:`) names the Andino members the wording usually
triggers. It is there so you can see the mapping. You never type it. If the agent does not
pick them, name the member in the prompt. Layer 1 already covers `andino-workflow`, `focus`,
`search-first` and the subagent rules, so no example repeats them.

Companion skills and MCP servers are installed separately (see
[External resources](../README.md#external-resources-manual-installation)). An example that
names one assumes it is installed and connected on your host. MCP names such as `drawio`,
`staruml`, `premiere`, `cheatengine` and `git` stand for whatever name that server has in your
host's MCP config.

## Contents

1. [Build features](#1-build-features)
2. [Frontend and design](#2-frontend-and-design)
3. [Bugs, failures and performance](#3-bugs-failures-and-performance)
4. [Code quality and review](#4-code-quality-and-review)
5. [Architecture, diagrams and docs](#5-architecture-diagrams-and-docs)
6. [Git, CI/CD and shipping](#6-git-cicd-and-shipping)
7. [Research and decisions](#7-research-and-decisions)
8. [Writing, learning and thesis](#8-writing-learning-and-thesis)
9. [Marketing, content and branding](#9-marketing-content-and-branding)
10. [Reverse engineering, media and local tools](#10-reverse-engineering-media-and-local-tools)
11. [Working with agents and sessions](#11-working-with-agents-and-sessions)
12. [Coverage map](#coverage-map)

## 1. Build features

```text
# New API endpoint with a regression guard
# workflow picks: andino-api-and-interface-design, andino-tdd, andino-verification
Task: add POST /api/orders/{id}/refund that refunds a paid order once.
Context/evidence: handlers live in [src/api/orders.ts]; existing tests in [tests/orders.test.ts];
  payment client: [src/payments/client.ts].
Done when: a second refund for the same order returns 409, a refund of an unpaid order returns 422,
  and the new tests fail before the change and pass after it.
Constraints: keep the existing error response shape.

# Turn an accepted spec into a plan, no code yet
# workflow picks: andino-planning
Mode: plan only
Task: plan the CSV export feature described in the spec.
Context/evidence: spec: [docs/specs/csv-export.md]; current export code: [src/export/].
Done when: the plan lists each task with its files, the tests that prove it and its order,
  saved at docs/exec-plans/active/csv-export.md.

# Execute an approved plan, or resume one that stopped
# workflow picks: andino-plan-execution
Task: execute the approved plan, starting from its NEXT ACTION.
Context/evidence: plan: [docs/exec-plans/active/csv-export.md].
Done when: every task in the plan is DONE with its recorded test result, or the first blocker
  is written into the plan with the exact next step.
Constraints: no commit or push.

# Large feature split into independent lanes
# workflow picks: andino-delegation
Task: implement tasks T3, T4 and T5 of the plan in parallel where they are independent.
Context/evidence: plan: [docs/exec-plans/active/billing.md]; the three tasks touch
  [src/invoices/], [src/tax/] and [src/emails/].
Done when: each task passes its own tests and the full suite passes after integration.
Constraints: show me the agent count, models and effort before starting any subagent.

# Database schema change with live consumers
# workflow picks: andino-deprecation-and-migration
Task: rename column users.fullname to users.display_name without downtime.
Context/evidence: ORM models in [src/db/models.py]; services reading the column: [list or "find them"];
  database: PostgreSQL [version].
Done when: the migration runs forward and backward on a copy of the schema, and every reader uses
  the new name with the old one still readable until the final step.
Constraints: no destructive step without asking me first.
```

## 2. Frontend and design

```text
# New landing page with its own visual direction
Skills: design-taste-frontend, impeccable, copywriting
Tools/MCP: playwright for screenshots
Mode: brainstorm first
Task: build a landing page for [product]. The visual direction is still open: decide it with me.
Context/evidence: audience: [who]; offer: [one sentence]; references I like: [links].
Done when: the page renders without console errors and you showed me screenshots at 360, 768
  and 1440 px.
Constraints: use the project's existing stack: [Next.js/Tailwind/...].

# Polish an existing screen that looks generic
Skills: impeccable, antislop-ui
Tools/MCP: playwright for screenshots
Task: critique and polish the dashboard so it stops looking AI-generated.
Context/evidence: page: [/dashboard]; component folder: [src/components/dashboard/].
Done when: you list the issues found, fix them, and show before/after screenshots at 1440 px.
Constraints: keep the current color palette and data.

# Mobile layout breaks
# workflow picks: andino-browser-testing-with-devtools
Skills: antislop-layoutmobile
Tools/MCP: playwright for screenshots
Task: fix the pricing table that overflows horizontally on phones.
Context/evidence: page: [/pricing]; screenshot: [attach]; component: [src/components/PricingTable.tsx].
Done when: no horizontal scroll at 360 px, tap targets are at least 44 px, and 768/1440 px look unchanged.

# Accessibility pass
Skills: antislop-human, impeccable
Tools/MCP: playwright for keyboard checks
Task: make the signup form fully usable by keyboard and screen readers.
Context/evidence: form: [src/components/SignupForm.tsx].
Done when: every field is reachable by Tab in order, focus is always visible, errors are announced,
  and text contrast is at least 4.5:1.

# Loading and error states for a component
# workflow picks: andino-plan-execution (frontend-engineering resource)
Task: add loading, empty and error states to the orders list.
Context/evidence: component: [src/components/OrdersList.tsx]; API hook: [src/hooks/useOrders.ts].
Done when: each state renders with mocked data in the existing component tests, and the list no
  longer shows a blank screen while loading.

# Copy an existing site faithfully
Skills: clone-website
Tools/MCP: playwright for side-by-side screenshots
Task: rebuild [URL] as local code that matches the original.
Context/evidence: target stack: [Next.js + Tailwind]; pages: [home, pricing].
Done when: screenshots of the clone and the original match at 360, 768 and 1440 px, and links
  and hover states work.
Constraints: only for a site I own or may copy: [say which].

# Three.js scene that runs slowly
# workflow picks: andino-performance-optimization
Skills: threejs-skills
Tools/MCP: chrome-devtools for a performance trace
Task: make the hero 3D scene hold 60 fps on a mid-range laptop.
Context/evidence: scene code: [src/three/Hero.tsx]; current fps: [number] on [device].
Done when: a trace shows stable 60 fps on the same device with the same visual result.

# Logo for a new product
Skills: logo-design
Mode: brainstorm first
Task: design a logo for [product name].
Context/evidence: what the product does: [one sentence]; tone: [e.g. calm, technical];
  colors to avoid: [list].
Done when: I get three distinct SVG directions and the final one in light and dark versions.
```

## 3. Bugs, failures and performance

```text
# Runtime error with a stack trace
# workflow picks: andino-debugging, andino-tdd
Task: fix the crash when saving a profile without an avatar.
Context/evidence: repro: [steps]. Error: [paste the full stack trace]. Version: [app/framework version].
Done when: a test reproduces the crash first and passes after the fix; saving with and without
  an avatar both work.

# Test that fails only in CI
# workflow picks: andino-ci-cd-and-automation, andino-debugging
Task: find out why test [name] fails in CI but passes locally, and fix the cause.
Context/evidence: failing run: [CI link or pasted log]; workflow file: [.github/workflows/ci.yml].
Done when: the cause is named with evidence, and five consecutive CI runs pass.
Constraints: no retries or skips to hide the failure.

# Slow page in production
# workflow picks: andino-performance-optimization
Tools/MCP: chrome-devtools for a performance trace and network waterfall
Task: cut the load time of [/products].
Context/evidence: current measurement: [LCP/TTFB numbers]; environment: [URL or local build command].
Done when: a before/after trace on the same setup shows the improvement and the cause it fixed.

# Something broke after a library upgrade
Tools/MCP: context7 for the docs of the installed version
Task: fix the build that fails after upgrading [library] from [old] to [new].
Context/evidence: error: [paste]; lockfile: [package-lock.json/pnpm-lock.yaml].
Done when: the build and tests pass on the new version, and you name the documented change
  that caused the break.

# The same area keeps regressing
Skills: ai-codebase-rescue
Task: stabilize the checkout flow; every fix breaks something else.
Context/evidence: area: [src/checkout/]; recent regressions: [issue links or descriptions].
Done when: each part of the area is marked KEEP/REFACTOR/REMAKE/REMOVE with evidence, and
  regression tests cover the last three failures.
Constraints: no rewrite before the evidence is in.
```

## 4. Code quality and review

```text
# Review a branch before merging
# workflow picks: andino-code-review
Task: review the branch [feature/refund] against main.
Context/evidence: what it should do: [link to spec or one paragraph].
Done when: findings are ranked by severity with file:line and a concrete fix, split into
  "does it meet the spec" and "code standards".
Constraints: review only; do not edit files.

# Clean up working but messy code
# workflow picks: andino-code-simplification
Task: simplify [src/utils/pricing.ts] without changing behavior.
Context/evidence: tests that cover it: [tests/pricing.test.ts].
Done when: the same tests pass, nesting and duplication are reduced, and the diff changes no output.

# Check a proposal for over-engineering
Skills: ponytail-review
Mode: plan only
Task: tell me if this design is more than the problem needs.
Context/evidence: proposal: [paste or link]; actual requirement: [one paragraph].
Done when: you list each part you would cut, keep or simplify, with the reason.

# Security audit of a trust boundary
# workflow picks: andino-security-and-hardening
Task: audit the login and password-reset flow.
Context/evidence: code: [src/auth/]; deployment: [how secrets and sessions are stored].
Done when: each finding has severity, a reproducible scenario and a fix; nothing found is
  stated per area, not skipped.
Constraints: no live attacks against production.

# Set and enforce a quality bar
# workflow picks: andino-constraint-driven-development
Task: write down the quality rules for this repo and make the checks enforce them.
Context/evidence: current tooling: [linters, test commands, CI file].
Done when: the rules are in [docs/quality.md] and CI fails when one is broken.

# Pressure-test a risky assumption before building on it
# workflow picks: andino-doubt-driven-development
Task: before we migrate, check the assumption that every order has exactly one customer.
Context/evidence: schema: [file]; read-only data access: [how].
Done when: the assumption is confirmed or disproved with queries and counts.
Constraints: read-only.

# Remove AI-style filler from comments
Skills: antislop-code
Task: clean the comments in [src/services/] so they explain intent, not restate code.
Context/evidence: folder: [src/services/].
Done when: the diff touches only comments and the tests still pass.
```

## 5. Architecture, diagrams and docs

```text
# Find architectural friction in a large codebase
# workflow picks: andino-architecture-survey
Tools/MCP: graphify for callers and dependencies
Task: show where the payments module is hardest to change and why.
Context/evidence: module: [src/payments/]; recent pain: [examples].
Done when: I get the top problem areas with evidence from the code and a before/after sketch for each.
Constraints: report only; no refactor.

# Design a module boundary or API contract
# workflow picks: andino-api-and-interface-design
Mode: brainstorm first
Task: design the public interface of the new notifications module.
Context/evidence: callers that need it: [list]; channels: email, push, in-app.
Done when: we agree on function signatures, error shapes and what stays private.

# Editable architecture diagram
Tools/MCP: drawio
Task: draw the current request flow from browser to database.
Context/evidence: services: [list or "read docker-compose.yml"].
Done when: a .drawio file opens in draw.io and every box matches a real service in the repo.

# UML class diagram from code
Tools/MCP: staruml
Task: generate a class diagram of the domain models.
Context/evidence: models: [src/domain/].
Done when: the StarUML model shows every class with its fields and relations, matching the code.

# Record a decision
# workflow picks: andino-documentation-and-adrs
Task: write an ADR for choosing [queue technology].
Context/evidence: options compared: [list]; decision: [chosen option and why].
Done when: docs/adr/[number]-[slug].md states context, decision, consequences and rejected options.

# Agent instructions for a repo
# workflow picks: andino-agent-document-authoring
Task: write the AGENTS.md for this repo.
Context/evidence: build/test commands: [list]; rules agents keep breaking: [list].
Done when: AGENTS.md has the commands, the rules and nothing an agent can read from the code itself.
```

## 6. Git, CI/CD and shipping

```text
# Integrate a branch safely
# workflow picks: andino-git-skills
Tools/MCP: git (if native git is unavailable)
Task: merge [feature/x] into main.
Context/evidence: conflicts expected in: [files or "unknown"].
Done when: main contains the branch, the test suite passes after the merge, and the branch is kept.
Constraints: no force push; no push without asking me.

# Draft a pull request description
# workflow picks: andino-git-skills
Task: write the PR description for the current branch.
Context/evidence: issue: [link]; screenshots: [attach if UI].
Done when: the description lists what changed, why, how it was tested and any risk.

# Set up a CI pipeline
# workflow picks: andino-ci-cd-and-automation
Task: add a GitHub Actions workflow that runs lint, type check and tests on every PR.
Context/evidence: commands: [npm run lint, npm run typecheck, npm test]; Node version: [x].
Done when: a test PR shows all three jobs running and a deliberately broken test failing the run.

# Add production logging and metrics
# workflow picks: andino-observability-and-instrumentation
Task: make failed payments diagnosable from logs.
Context/evidence: code: [src/payments/]; logging library: [name]; where logs go: [service].
Done when: one failed payment produces a log entry with order id, error code and duration,
  and no card data.

# Release readiness check
# workflow picks: andino-shipping-and-launch
Mode: plan only
Task: tell me if version [x.y] is ready to release and how to roll it back.
Context/evidence: changelog: [file]; deploy method: [how].
Done when: I get a go/no-go list with evidence and the exact rollback steps.

# A step only I can do
# workflow picks: andino-human-procedure
Task: set up the production environment variables for the new service.
Context/evidence: variables needed: [names only]; platform: [Vercel/Railway/...].
Done when: you give me exact click-by-click steps, I confirm, and you verify the app reads them.
Constraints: never ask me to paste secret values into the chat.

# Triage incoming issues
# workflow picks: andino-issue-triage
Task: triage the open issues labeled "new".
Context/evidence: repo: [owner/name]; labels we use: [list].
Done when: each issue gets a proposed label, priority and next step in a table.
Constraints: do not comment on or change issues.
```

## 7. Research and decisions

```text
# Choose a library
Task: pick the best library for [PDF generation] in this project.
Context/evidence: stack: [framework and version]; needs: [list]; must run on: [server/edge].
Done when: I get adopt/extend/build options with sources, versions checked, and one recommendation.

# Use an API you have not used before
Tools/MCP: context7 for the docs of the installed version
Task: integrate [library] webhooks into the order service.
Context/evidence: installed version: [from lockfile]; service: [src/orders/].
Done when: a test sends a signed sample webhook and the handler accepts it, and a bad signature is rejected.

# A decision that is expensive to undo
Skills: council
Task: decide whether to move from REST to GraphQL for the mobile app.
Context/evidence: current pain: [list]; team size: [n]; timeline: [months].
Done when: I get a recommendation, the strongest counter-argument and one cheap test to run first.

# Explore an idea before anything is decided
Mode: brainstorm first
Task: I want users to share their dashboards; help me work out what that should mean.
Context/evidence: current dashboard feature: [short description]; who asked for it: [users].
Done when: we agree on the scope, the main options and what we will not build.
```

## 8. Writing, learning and thesis

```text
# Learn something over several sessions
# workflow picks: andino-learning-workspace
Task: teach me Rust ownership step by step while I build a small CLI.
Context/evidence: what I know: [languages]; time per session: [minutes].
Done when: each session ends with an exercise I solved, and progress is saved for the next session.

# Article from rough notes
# workflow picks: andino-article-shaping
Skills: natural-writing
Task: turn my notes into a blog post about [topic].
Context/evidence: notes: [paste or file]; readers: [who].
Done when: the post uses only my material and examples, and you mark any gap you could not fill.

# Polish a document or email
Skills: natural-writing
Task: rewrite this email to the client so it is clear and polite but firm.
Context/evidence: draft: [paste]; what I need from them: [one sentence].
Done when: the meaning and facts are unchanged and it reads like a person wrote it.

# Thesis literature review
Skills: skripsi-skill, natural-writing
Task: help me draft Chapter 2 from the papers I collected.
Context/evidence: papers: [folder or list]; campus and program: [name]; citation style: [APA/IEEE].
Done when: every claim in the draft cites one of my papers and the draft follows the campus format.
Constraints: no invented sources.

# Thesis defense preparation
Skills: skripsi-skill, council
Task: prepare me for the defense of my thesis.
Context/evidence: thesis file: [path]; examiners' focus areas if known: [list].
Done when: I get the likely questions with short answers grounded in my thesis, and the weakest
  points to fix first.
```

## 9. Marketing, content and branding

```text
# SEO audit of a site
Skills: seo-audit
Tools/MCP: playwright to load the pages
Task: audit [URL] for technical and on-page SEO problems.
Context/evidence: target keywords: [list]; pages that matter: [list].
Done when: issues are ranked by impact with the page and the fix for each.

# Get cited by AI search
Skills: ai-seo
Task: make our docs more likely to be quoted by AI assistants.
Context/evidence: docs site: [URL]; competitor that gets cited: [URL].
Done when: I get the specific page changes, in order, with the reason for each.

# Pricing page that converts
Skills: pricing, copywriting, cro
Mode: brainstorm first
Task: redesign the pricing page and its tiers.
Context/evidence: current page: [URL]; plans and prices: [list]; conversion today: [number if known].
Done when: we agree on the tiers, and the new copy and layout are implemented with screenshots.

# Cold email sequence
Skills: cold-email
Task: write a three-email outbound sequence for [audience].
Context/evidence: offer: [one sentence]; proof: [customer results]; sender: [role].
Done when: each email has a subject line, under 120 words, one clear ask and a follow-up timing.

# Turn an article into LinkedIn posts
Skills: linkedin-repurposer
Task: turn my latest article into three LinkedIn posts.
Context/evidence: article: [link or paste]; my audience: [who].
Done when: each post has its own hook and stands alone, in my voice.

# Read what competitors post
Skills: agent-reach, competitors
Task: summarize what [competitor] announced on YouTube and X this month.
Context/evidence: channels: [links].
Done when: I get a dated list of announcements with links and what each means for us.

# Launch plan
Skills: launch
Mode: plan only
Task: plan the launch of [feature] for the next four weeks.
Context/evidence: channels we have: [list]; audience size: [numbers].
Done when: I get a week-by-week plan with owners, channels and the metric for each step.
```

## 10. Reverse engineering, media and local tools

```text
# Understand an app you only have as a binary
Tools/MCP: rea
Task: find out how [app] stores its settings and which server it calls on startup.
Context/evidence: file: [path to APK/EXE/app bundle]; I own it or may analyze it: [say which].
Done when: I get the file locations and endpoints with the evidence REA found.
Constraints: analysis only; no patching.

# Edit a video project
Tools/MCP: premiere
Task: cut the silences longer than one second from the interview sequence.
Context/evidence: project: [path to .prproj]; sequence: [name].
Done when: you show me the list of cuts first, and after I approve, the sequence has them applied.
Constraints: work on a duplicate of the sequence.

# Inspect a value in a single-player game
Tools/MCP: cheatengine
Task: find the memory address of the player's gold in [game], offline single-player.
Context/evidence: game process: [name.exe]; current gold: [number].
Done when: you show the address and its value matching the in-game number.
Constraints: read-only until I say otherwise; never on online or anti-cheat games.
```

## 11. Working with agents and sessions

```text
# Write a new skill
# workflow picks: andino-skill-maker
Task: create a skill that prepares our weekly release notes.
Context/evidence: last three release notes: [links]; where the data comes from: [git log, issues].
Done when: the skill runs on last week's changes and its output matches the format of the examples.

# A session went wrong
# workflow picks: andino-session-diagnostics
Task: find out why the last session ignored the plan and reran the same tests five times.
Context/evidence: transcript or summary: [path]; plan: [file].
Done when: I get the causes with the exact moments they happened and one change to prevent each.

# Continue on another machine or with another person
# workflow picks: andino-handoff
Task: prepare a handoff so I can continue this work on my laptop tomorrow.
Context/evidence: current task and plan: [file].
Done when: the handoff lists the state, what is verified, what is not, and the first command to run.

# End-to-end check in a real browser
# workflow picks: andino-browser-testing-with-devtools
Tools/MCP: playwright, chrome-devtools for console and network
Task: verify the checkout flow works end to end in the browser.
Context/evidence: local URL: [http://localhost:3000]; test account: [from seed file].
Done when: a test order completes, the console has no errors, every API call returns 2xx,
  and you show screenshots of each step.
```

## Coverage map

Which example shows each skill or tool. Phase members such as `andino-tdd`, `andino-debugging`
and `andino-verification` also run inside many other examples.

| Skill or tool | Example |
| --- | --- |
| `andino-agent-document-authoring` | Agent instructions for a repo |
| `andino-api-and-interface-design` | New API endpoint; Design a module boundary |
| `andino-architecture-survey` | Find architectural friction |
| `andino-article-shaping` | Article from rough notes |
| `andino-brainstorming` | Every `Mode: brainstorm first` example |
| `andino-browser-testing-with-devtools` | End-to-end check in a real browser; Mobile layout breaks |
| `andino-ci-cd-and-automation` | Test that fails only in CI; Set up a CI pipeline |
| `andino-code-review` | Review a branch before merging |
| `andino-code-simplification` | Clean up working but messy code |
| `andino-constraint-driven-development` | Set and enforce a quality bar |
| `andino-debugging` | Runtime error with a stack trace |
| `andino-delegation` | Large feature split into independent lanes |
| `andino-deprecation-and-migration` | Database schema change |
| `andino-documentation-and-adrs` | Record a decision |
| `andino-doubt-driven-development` | Pressure-test a risky assumption |
| `andino-git-skills` | Integrate a branch; Draft a pull request |
| `andino-handoff` | Continue on another machine |
| `andino-human-procedure` | A step only I can do |
| `andino-issue-triage` | Triage incoming issues |
| `andino-learning-workspace` | Learn something over several sessions |
| `andino-observability-and-instrumentation` | Add production logging and metrics |
| `andino-performance-optimization` | Slow page in production; Three.js scene that runs slowly |
| `andino-plan-execution` | Execute an approved plan; Loading and error states |
| `andino-planning` | Turn an accepted spec into a plan |
| `andino-security-and-hardening` | Security audit of a trust boundary |
| `andino-session-diagnostics` | A session went wrong |
| `andino-shipping-and-launch` | Release readiness check |
| `andino-skill-maker` | Write a new skill |
| `andino-tdd`, `andino-verification` | New API endpoint; Runtime error |
| `ai-codebase-rescue` | The same area keeps regressing |
| `council` | A decision that is expensive to undo; Thesis defense |
| `natural-writing` | Polish a document; Article; Thesis literature review |
| `skripsi-skill` | Thesis literature review; Thesis defense |
| `threejs-skills` | Three.js scene that runs slowly |
| `search-first` (from Layer 1) | Choose a library |
| `design-taste-frontend`, `impeccable` | New landing page; Polish an existing screen; Accessibility pass |
| `clone-website` | Copy an existing site faithfully |
| `antislop-*` | Polish an existing screen; Mobile layout; Accessibility; Remove AI-style filler |
| `ponytail-review` | Check a proposal for over-engineering |
| `logo-design` | Logo for a new product |
| Marketing Skills (`seo-audit`, `ai-seo`, `pricing`, `copywriting`, `cro`, `cold-email`, `competitors`, `launch`) | Section 9 |
| LinkedIn Skills (`linkedin-repurposer`) | Turn an article into LinkedIn posts |
| `agent-reach` | Read what competitors post |
| `context7` | Library upgrade; Use an API you have not used before |
| `playwright` | Most UI examples; End-to-end check |
| `chrome-devtools` | Slow page; Three.js performance; End-to-end check |
| `graphify` | Find architectural friction |
| `rea` | Understand an app you only have as a binary |
| `git` MCP | Integrate a branch safely |
| `drawio` | Editable architecture diagram |
| `staruml` | UML class diagram from code |
| `premiere` | Edit a video project |
| `cheatengine` | Inspect a value in a single-player game |
| `focus`, `andino-workflow`, RTK | Always on through Layer 1 and the shell; no prompt needed |
