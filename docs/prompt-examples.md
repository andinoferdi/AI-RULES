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
- `Skills`, `Tools/MCP` and `Mode` sit together on one line each. A blank line separates every
  slot from `Task` on.
- A slot with one item stays on one line. A slot with two or more items puts each on its own
  `- ` line: one check, file or limit per bullet. No line is wrapped by hand.
- `[brackets]` mark what you fill in.

The **Workflow picks** line under a heading names the Andino members the wording usually
triggers. It sits outside the prompt block, so you never copy or type it. If the agent does not
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

### New API endpoint with a regression guard

Workflow picks: `andino-api-and-interface-design`, `andino-tdd`, `andino-verification`.

```text
Task: add POST /api/orders/{id}/refund that refunds a paid order once.

Context/evidence:
- Handlers live in [src/api/orders.ts]
- Existing tests in [tests/orders.test.ts]
- Payment client: [src/payments/client.ts]

Done when:
- A second refund for the same order returns 409.
- A refund of an unpaid order returns 422.
- The new tests fail before the change and pass after it.

Constraints: keep the existing error response shape.
```

### Turn an accepted spec into a plan, no code yet

Workflow picks: `andino-planning`.

```text
Mode: plan only

Task: plan the CSV export feature described in the spec.

Context/evidence:
- Spec: [docs/specs/csv-export.md]
- Current export code: [src/export/]

Done when: the plan lists each task with its files, the tests that prove it and its order, saved at docs/exec-plans/active/csv-export.md.
```

### Execute an approved plan, or resume one that stopped

Workflow picks: `andino-plan-execution`.

```text
Task: execute the approved plan, starting from its NEXT ACTION.

Context/evidence: plan: [docs/exec-plans/active/csv-export.md].

Done when: every task in the plan is DONE with its recorded test result, or the first blocker is written into the plan with the exact next step.

Constraints: no commit or push.
```

### Large feature split into independent lanes

Workflow picks: `andino-delegation`.

```text
Task: implement tasks T3, T4 and T5 of the plan in parallel where they are independent.

Context/evidence:
- Plan: [docs/exec-plans/active/billing.md]
- The three tasks touch [src/invoices/], [src/tax/] and [src/emails/]

Done when: each task passes its own tests and the full suite passes after integration.

Constraints: show me the agent count, models and effort before starting any subagent.
```

### Database schema change with live consumers

Workflow picks: `andino-deprecation-and-migration`.

```text
Task: rename column users.fullname to users.display_name without downtime.

Context/evidence:
- ORM models in [src/db/models.py]
- Services reading the column: [list or "find them"]
- Database: PostgreSQL [version]

Done when:
- The migration runs forward and backward on a copy of the schema.
- Every reader uses the new name, with the old one still readable until the final step.

Constraints: no destructive step without asking me first.
```

## 2. Frontend and design

### New landing page with its own visual direction

```text
Skills: design-taste-frontend, impeccable, copywriting
Tools/MCP: playwright for screenshots
Mode: brainstorm first

Task:
- Build a landing page for [product].
- The visual direction is still open: decide it with me.

Context/evidence:
- Audience: [who].
- Offer: [one sentence].
- References I like: [links].

Done when: the page renders without console errors and you showed me screenshots at 360, 768 and 1440 px.

Constraints: use the project's existing stack: [Next.js/Tailwind/...].
```

### Polish an existing screen that looks generic

```text
Skills: impeccable, antislop-ui
Tools/MCP: playwright for screenshots

Task: critique and polish the dashboard so it stops looking AI-generated.

Context/evidence:
- Page: [/dashboard]
- Component folder: [src/components/dashboard/]

Done when: you list the issues found, fix them, and show before/after screenshots at 1440 px.

Constraints: keep the current color palette and data.
```

### Mobile layout breaks

Workflow picks: `andino-browser-testing-with-devtools`.

```text
Skills: antislop-layoutmobile
Tools/MCP: playwright for screenshots

Task: fix the pricing table that overflows horizontally on phones.

Context/evidence:
- Page: [/pricing]
- Screenshot: [attach]
- Component: [src/components/PricingTable.tsx]

Done when:
- No horizontal scroll at 360 px.
- Tap targets are at least 44 px.
- 768 and 1440 px look unchanged.
```

### Accessibility pass

```text
Skills: antislop-human, impeccable
Tools/MCP: playwright for keyboard checks

Task: make the signup form fully usable by keyboard and screen readers.

Context/evidence: form: [src/components/SignupForm.tsx].

Done when:
- Every field is reachable by Tab in order.
- Focus is always visible.
- Errors are announced.
- Text contrast is at least 4.5:1.
```

### Loading and error states for a component

Workflow picks: `andino-plan-execution` (frontend-engineering resource).

```text
Task: add loading, empty and error states to the orders list.

Context/evidence:
- Component: [src/components/OrdersList.tsx]
- API hook: [src/hooks/useOrders.ts]

Done when:
- Each state renders with mocked data in the existing component tests.
- The list no longer shows a blank screen while loading.
```

### Copy an existing site faithfully

```text
Skills: clone-website
Tools/MCP: playwright for side-by-side screenshots

Task: rebuild [URL] as local code that matches the original.

Context/evidence:
- Target stack: [Next.js + Tailwind]
- Pages: [home, pricing]

Done when:
- Screenshots of the clone and the original match at 360, 768 and 1440 px.
- Links and hover states work.

Constraints: only for a site I own or may copy: [say which].
```

### Three.js scene that runs slowly

Workflow picks: `andino-performance-optimization`.

```text
Skills: threejs-skills
Tools/MCP: chrome-devtools for a performance trace

Task: make the hero 3D scene hold 60 fps on a mid-range laptop.

Context/evidence:
- Scene code: [src/three/Hero.tsx]
- Current fps: [number] on [device]

Done when: a trace shows stable 60 fps on the same device with the same visual result.
```

### Logo for a new product

```text
Skills: logo-design
Mode: brainstorm first

Task: design a logo for [product name].

Context/evidence:
- What the product does: [one sentence]
- Tone: [e.g. calm, technical]
- Colors to avoid: [list]

Done when: I get three distinct SVG directions and the final one in light and dark versions.
```

## 3. Bugs, failures and performance

### Runtime error with a stack trace

Workflow picks: `andino-debugging`, `andino-tdd`.

```text
Task: fix the crash when saving a profile without an avatar.

Context/evidence:
- Repro: [steps]
- Error: [paste the full stack trace]
- Version: [app/framework version]

Done when:
- A test reproduces the crash first and passes after the fix.
- Saving with and without an avatar both work.
```

### Test that fails only in CI

Workflow picks: `andino-ci-cd-and-automation`, `andino-debugging`.

```text
Task: find out why test [name] fails in CI but passes locally, and fix the cause.

Context/evidence:
- Failing run: [CI link or pasted log]
- Workflow file: [.github/workflows/ci.yml]

Done when:
- The cause is named with evidence.
- Five consecutive CI runs pass.

Constraints: no retries or skips to hide the failure.
```

### Slow page in production

Workflow picks: `andino-performance-optimization`.

```text
Tools/MCP: chrome-devtools for a performance trace and network waterfall

Task: cut the load time of [/products].

Context/evidence:
- Current measurement: [LCP/TTFB numbers]
- Environment: [URL or local build command]

Done when: a before/after trace on the same setup shows the improvement and the cause it fixed.
```

### Something broke after a library upgrade

```text
Tools/MCP: context7 for the docs of the installed version

Task: fix the build that fails after upgrading [library] from [old] to [new].

Context/evidence:
- Error: [paste]
- Lockfile: [package-lock.json/pnpm-lock.yaml]

Done when:
- The build and tests pass on the new version.
- You name the documented change that caused the break.
```

### The same area keeps regressing

```text
Skills: ai-codebase-rescue

Task: stabilize the checkout flow; every fix breaks something else.

Context/evidence:
- Area: [src/checkout/]
- Recent regressions: [issue links or descriptions]

Done when:
- Each part of the area is marked KEEP/REFACTOR/REMAKE/REMOVE with evidence.
- Regression tests cover the last three failures.

Constraints: no rewrite before the evidence is in.
```

## 4. Code quality and review

### Review a branch before merging

Workflow picks: `andino-code-review`.

```text
Task: review the branch [feature/refund] against main.

Context/evidence: what it should do: [link to spec or one paragraph].

Done when: findings are ranked by severity with file:line and a concrete fix, split into "does it meet the spec" and "code standards".

Constraints:
- Review only.
- Do not edit files.
```

### Clean up working but messy code

Workflow picks: `andino-code-simplification`.

```text
Task: simplify [src/utils/pricing.ts] without changing behavior.

Context/evidence: tests that cover it: [tests/pricing.test.ts].

Done when:
- The same tests pass.
- Nesting and duplication are reduced.
- The diff changes no output.
```

### Check a proposal for over-engineering

```text
Skills: ponytail-review
Mode: plan only

Task: tell me if this design is more than the problem needs.

Context/evidence:
- Proposal: [paste or link]
- Actual requirement: [one paragraph]

Done when: you list each part you would cut, keep or simplify, with the reason.
```

### Security audit of a trust boundary

Workflow picks: `andino-security-and-hardening`.

```text
Task: audit the login and password-reset flow.

Context/evidence:
- Code: [src/auth/]
- Deployment: [how secrets and sessions are stored]

Done when:
- Each finding has severity, a reproducible scenario and a fix.
- Nothing found is stated per area, not skipped.

Constraints: no live attacks against production.
```

### Set and enforce a quality bar

Workflow picks: `andino-constraint-driven-development`.

```text
Task: write down the quality rules for this repo and make the checks enforce them.

Context/evidence: current tooling: [linters, test commands, CI file].

Done when: the rules are in [docs/quality.md] and CI fails when one is broken.
```

### Pressure-test a risky assumption before building on it

Workflow picks: `andino-doubt-driven-development`.

```text
Task: before we migrate, check the assumption that every order has exactly one customer.

Context/evidence:
- Schema: [file]
- Read-only data access: [how]

Done when: the assumption is confirmed or disproved with queries and counts.

Constraints: read-only.
```

### Remove AI-style filler from comments

```text
Skills: antislop-code

Task: clean the comments in [src/services/] so they explain intent, not restate code.

Context/evidence: folder: [src/services/].

Done when: the diff touches only comments and the tests still pass.
```

## 5. Architecture, diagrams and docs

### Find architectural friction in a large codebase

Workflow picks: `andino-architecture-survey`.

```text
Tools/MCP: graphify for callers and dependencies

Task: show where the payments module is hardest to change and why.

Context/evidence:
- Module: [src/payments/]
- Recent pain: [examples]

Done when: I get the top problem areas with evidence from the code and a before/after sketch for each.

Constraints:
- Report only.
- No refactor.
```

### Design a module boundary or API contract

Workflow picks: `andino-api-and-interface-design`.

```text
Mode: brainstorm first

Task: design the public interface of the new notifications module.

Context/evidence:
- Callers that need it: [list]
- Channels: email, push, in-app.

Done when: we agree on function signatures, error shapes and what stays private.
```

### Editable architecture diagram

```text
Tools/MCP: drawio

Task: draw the current request flow from browser to database.

Context/evidence: services: [list or "read docker-compose.yml"].

Done when: a .drawio file opens in draw.io and every box matches a real service in the repo.
```

### UML class diagram from code

```text
Tools/MCP: staruml

Task: generate a class diagram of the domain models.

Context/evidence: models: [src/domain/].

Done when: the StarUML model shows every class with its fields and relations, matching the code.
```

### Record a decision

Workflow picks: `andino-documentation-and-adrs`.

```text
Task: write an ADR for choosing [queue technology].

Context/evidence:
- Options compared: [list]
- Decision: [chosen option and why]

Done when: docs/adr/[number]-[slug].md states context, decision, consequences and rejected options.
```

### Agent instructions for a repo

Workflow picks: `andino-agent-document-authoring`.

```text
Task: write the AGENTS.md for this repo.

Context/evidence:
- Build/test commands: [list]
- Rules agents keep breaking: [list]

Done when: AGENTS.md has the commands, the rules and nothing an agent can read from the code itself.
```

## 6. Git, CI/CD and shipping

### Integrate a branch safely

Workflow picks: `andino-git-skills`.

```text
Tools/MCP: git (if native git is unavailable)

Task: merge [feature/x] into main.

Context/evidence: conflicts expected in: [files or "unknown"].

Done when:
- main contains the branch.
- The test suite passes after the merge.
- The branch is kept.

Constraints:
- No force push.
- No push without asking me.
```

### Draft a pull request description

Workflow picks: `andino-git-skills`.

```text
Task: write the PR description for the current branch.

Context/evidence:
- Issue: [link]
- Screenshots: [attach if UI]

Done when: the description lists what changed, why, how it was tested and any risk.
```

### Set up a CI pipeline

Workflow picks: `andino-ci-cd-and-automation`.

```text
Task: add a GitHub Actions workflow that runs lint, type check and tests on every PR.

Context/evidence:
- Commands: [npm run lint, npm run typecheck, npm test]
- Node version: [x]

Done when: a test PR shows all three jobs running and a deliberately broken test failing the run.
```

### Add production logging and metrics

Workflow picks: `andino-observability-and-instrumentation`.

```text
Task: make failed payments diagnosable from logs.

Context/evidence:
- Code: [src/payments/]
- Logging library: [name]
- Where logs go: [service]

Done when: one failed payment produces a log entry with order id, error code and duration, and no card data.
```

### Release readiness check

Workflow picks: `andino-shipping-and-launch`.

```text
Mode: plan only

Task: tell me if version [x.y] is ready to release and how to roll it back.

Context/evidence:
- Changelog: [file]
- Deploy method: [how]

Done when: I get a go/no-go list with evidence and the exact rollback steps.
```

### A step only I can do

Workflow picks: `andino-human-procedure`.

```text
Task: set up the production environment variables for the new service.

Context/evidence:
- Variables needed: [names only]
- Platform: [Vercel/Railway/...]

Done when: you give me exact click-by-click steps, I confirm, and you verify the app reads them.

Constraints: never ask me to paste secret values into the chat.
```

### Triage incoming issues

Workflow picks: `andino-issue-triage`.

```text
Task: triage the open issues labeled "new".

Context/evidence:
- Repo: [owner/name]
- Labels we use: [list]

Done when: each issue gets a proposed label, priority and next step in a table.

Constraints: do not comment on or change issues.
```

## 7. Research and decisions

### Choose a library

```text
Task: pick the best library for [PDF generation] in this project.

Context/evidence:
- Stack: [framework and version]
- Needs: [list]
- Must run on: [server/edge]

Done when: I get adopt/extend/build options with sources, versions checked, and one recommendation.
```

### Use an API you have not used before

```text
Tools/MCP: context7 for the docs of the installed version

Task: integrate [library] webhooks into the order service.

Context/evidence:
- Installed version: [from lockfile]
- Service: [src/orders/]

Done when:
- A test sends a signed sample webhook and the handler accepts it.
- A bad signature is rejected.
```

### A decision that is expensive to undo

```text
Skills: council

Task: decide whether to move from REST to GraphQL for the mobile app.

Context/evidence:
- Current pain: [list]
- Team size: [n]
- Timeline: [months]

Done when: I get a recommendation, the strongest counter-argument and one cheap test to run first.
```

### Explore an idea before anything is decided

```text
Mode: brainstorm first

Task: I want users to share their dashboards; help me work out what that should mean.

Context/evidence:
- Current dashboard feature: [short description]
- Who asked for it: [users]

Done when: we agree on the scope, the main options and what we will not build.
```

## 8. Writing, learning and thesis

### Learn something over several sessions

Workflow picks: `andino-learning-workspace`.

```text
Task: teach me Rust ownership step by step while I build a small CLI.

Context/evidence:
- What I know: [languages]
- Time per session: [minutes]

Done when:
- Each session ends with an exercise I solved.
- Progress is saved for the next session.
```

### Article from rough notes

Workflow picks: `andino-article-shaping`.

```text
Skills: natural-writing

Task: turn my notes into a blog post about [topic].

Context/evidence:
- Notes: [paste or file]
- Readers: [who]

Done when:
- The post uses only my material and examples.
- You mark any gap you could not fill.
```

### Polish a document or email

```text
Skills: natural-writing

Task: rewrite this email to the client so it is clear and polite but firm.

Context/evidence:
- Draft: [paste]
- What I need from them: [one sentence]

Done when: the meaning and facts are unchanged and it reads like a person wrote it.
```

### Thesis literature review

```text
Skills: skripsi-skill, natural-writing

Task: help me draft Chapter 2 from the papers I collected.

Context/evidence:
- Papers: [folder or list]
- Campus and program: [name]
- Citation style: [APA/IEEE]

Done when: every claim in the draft cites one of my papers and the draft follows the campus format.

Constraints: no invented sources.
```

### Thesis defense preparation

```text
Skills: skripsi-skill, council

Task: prepare me for the defense of my thesis.

Context/evidence:
- Thesis file: [path]
- Examiners' focus areas if known: [list]

Done when: I get the likely questions with short answers grounded in my thesis, and the weakest points to fix first.
```

## 9. Marketing, content and branding

### SEO audit of a site

```text
Skills: seo-audit
Tools/MCP: playwright to load the pages

Task: audit [URL] for technical and on-page SEO problems.

Context/evidence:
- Target keywords: [list]
- Pages that matter: [list]

Done when: issues are ranked by impact with the page and the fix for each.
```

### Get cited by AI search

```text
Skills: ai-seo

Task: make our docs more likely to be quoted by AI assistants.

Context/evidence:
- Docs site: [URL]
- Competitor that gets cited: [URL]

Done when: I get the specific page changes, in order, with the reason for each.
```

### Pricing page that converts

```text
Skills: pricing, copywriting, cro
Mode: brainstorm first

Task: redesign the pricing page and its tiers.

Context/evidence:
- Current page: [URL]
- Plans and prices: [list]
- Conversion today: [number if known]

Done when:
- We agree on the tiers.
- The new copy and layout are implemented with screenshots.
```

### Cold email sequence

```text
Skills: cold-email

Task: write a three-email outbound sequence for [audience].

Context/evidence:
- Offer: [one sentence]
- Proof: [customer results]
- Sender: [role]

Done when: each email has a subject line, under 120 words, one clear ask and a follow-up timing.
```

### Turn an article into LinkedIn posts

```text
Skills: linkedin-repurposer

Task: turn my latest article into three LinkedIn posts.

Context/evidence:
- Article: [link or paste]
- My audience: [who]

Done when: each post has its own hook and stands alone, in my voice.
```

### Read what competitors post

```text
Skills: agent-reach, competitors

Task: summarize what [competitor] announced on YouTube and X this month.

Context/evidence: channels: [links].

Done when: I get a dated list of announcements with links and what each means for us.
```

### Launch plan

```text
Skills: launch
Mode: plan only

Task: plan the launch of [feature] for the next four weeks.

Context/evidence:
- Channels we have: [list]
- Audience size: [numbers]

Done when: I get a week-by-week plan with owners, channels and the metric for each step.
```

## 10. Reverse engineering, media and local tools

### Understand an app you only have as a binary

```text
Tools/MCP: rea

Task: find out how [app] stores its settings and which server it calls on startup.

Context/evidence:
- File: [path to APK/EXE/app bundle]
- I own it or may analyze it: [say which]

Done when: I get the file locations and endpoints with the evidence REA found.

Constraints:
- Analysis only.
- No patching.
```

### Edit a video project

```text
Tools/MCP: premiere

Task: cut the silences longer than one second from the interview sequence.

Context/evidence:
- Project: [path to .prproj]
- Sequence: [name]

Done when: you show me the list of cuts first, and after I approve, the sequence has them applied.

Constraints: work on a duplicate of the sequence.
```

### Inspect a value in a single-player game

```text
Tools/MCP: cheatengine

Task: find the memory address of the player's gold in [game], offline single-player.

Context/evidence:
- Game process: [name.exe]
- Current gold: [number]

Done when: you show the address and its value matching the in-game number.

Constraints:
- Read-only until I say otherwise.
- Never on online or anti-cheat games.
```

## 11. Working with agents and sessions

### Write a new skill

Workflow picks: `andino-skill-maker`.

```text
Task: create a skill that prepares our weekly release notes.

Context/evidence:
- Last three release notes: [links]
- Where the data comes from: [git log, issues]

Done when: the skill runs on last week's changes and its output matches the format of the examples.
```

### Turn a rough prompt into the seven slots

Workflow picks: `andino-optimize-prompt` (only when you ask for it).

```text
Task: turn my rough prompt into a seven-slot prompt for this host.

Context/evidence: rough prompt: [paste it as you would have sent it]

Done when:
- Every skill and MCP server in the result is installed on this host.
- All my facts are unchanged.
- Removed phase skills, conflicts and proposed checks are listed under it.
```

### A session went wrong

Workflow picks: `andino-session-diagnostics`.

```text
Task: find out why the last session ignored the plan and reran the same tests five times.

Context/evidence:
- Transcript or summary: [path]
- Plan: [file]

Done when: I get the causes with the exact moments they happened and one change to prevent each.
```

### Continue on another machine or with another person

Workflow picks: `andino-handoff`.

```text
Task: prepare a handoff so I can continue this work on my laptop tomorrow.

Context/evidence: current task and plan: [file].

Done when: the handoff lists the state, what is verified, what is not, and the first command to run.
```

### End-to-end check in a real browser

Workflow picks: `andino-browser-testing-with-devtools`.

```text
Tools/MCP: playwright, chrome-devtools for console and network

Task: verify the checkout flow works end to end in the browser.

Context/evidence:
- Local URL: [http://localhost:3000]
- Test account: [from seed file]

Done when:
- A test order completes.
- The console has no errors.
- Every API call returns 2xx.
- You show screenshots of each step.
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
| `andino-optimize-prompt` | Turn a rough prompt into the seven slots |
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
