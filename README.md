# AI-RULES

Install Andino's skills for Codex, Claude Code, OpenCode, and Antigravity. Start with one Andino Workflow invocation; it selects relevant supporting skills and tools within the host's permissions.

## Distribution branches

| Branch | Purpose |
| --- | --- |
| [`main`](https://github.com/andinoferdi/AI-RULES/tree/main) | Installer source, tests, release tooling, and validation evidence |
| [`WebBased`](https://github.com/andinoferdi/AI-RULES/tree/WebBased) | Web/chat rules and project templates |
| [`search-first`](https://github.com/andinoferdi/AI-RULES/tree/search-first) | Existing-solution research before implementation |
| [`focus`](https://github.com/andinoferdi/AI-RULES/tree/focus) | Clear, concise, actionable communication |
| [`andino-workflow`](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow) | Adaptive workflow, capability routing, and portable checkpoints |
| [`ai-codebase-rescue`](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue) | Evidence-based stabilization of fragile codebases |
| [`skripsi-skill`](https://github.com/andinoferdi/AI-RULES/tree/skripsi-skill) | Thesis and research guidance |

Install the CLI from `main`. Setup downloads each skill from its own distribution branch; no manual branch switching or skill copying is needed.

## Setup

Requirements: **Python 3.11+**, **Git**, and your chosen AI agent already installed.

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup
```

Select your agents and a profile, then confirm the installation plan:

| Profile | Skills installed |
| --- | --- |
| Minimal | Andino Workflow + Focus + Search First |
| Engineering | Andino Workflow + Focus + Search First + AI Codebase Rescue |
| Research / Skripsi | Andino Workflow + Focus + Search First + Skripsi Skill |
| Everything | All five |

Open a new agent session or reload its window after setup. Installing all five skills does **not** activate all of them for every task. Third-party skills, plugins, and MCP servers require their own installation or connection.

Run `ai-rules setup` again to update selected skills from their latest configured branches. To update the CLI itself, run these commands from a clean `main` checkout:

```sh
git pull --ff-only
python -m pip install .
ai-rules setup
```

Setup verifies files and entry points, not successful skill use in a running agent. Review any reported conflict or unsupported installation layout before replacing files. See the [validation guide](evals/README.md) for testing details.

## Search First

`ai-rules setup --capability search-first` installs it independently. Selecting
Andino automatically installs Focus and Search First through the dependency
resolver. Focus stays independent; Search First is activated only when meaningful
existing-solution research is needed, not for every coding request.

Use `$search-first [task]` in Codex. Other hosts use their supported native skill
or setup-generated command/workflow (such as `/search-first`). Andino loads the
real installed skill when permitted, uses its findings, and retains lifecycle
ownership. Unknown-cause bugs keep the debugging route. Search First adds no
permission to install dependencies or perform external writes.

The proactive online upgrade adds actual native search and
source reading when local evidence leaves material external technical uncertainty,
with version checks, query redaction, untrusted-source protection and honest
offline/denied limits. See [upgrade validation](docs/validation/search-first/online/README.md)
for tested revisions and availability boundaries. Search First and Andino runtime
commits are published on their existing branches; release sequence 9 pins those
verified commits for bundled setup.

This is an AI-RULES adaptation of [ECC Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md),
by Affaan Mustafa, under MIT. See the distribution's `references/license.md`.

## Example prompt

Use one entry point. Replace `[prompt]` with your task; include the project path only when it differs from the agent's current project.

**Codex** — select the skill through the `$` picker:

```text
$andino-workflow [prompt]
```

**Claude Code, OpenCode, and Antigravity**:

```text
/andino-workflow [prompt]
```

Examples below use Codex syntax. For the other agents, replace `$andino-workflow` with `/andino-workflow`.

```text
$andino-workflow Skripsi saya sampai mana dan apa next steps berdasarkan dokumen terbaru?
```

```text
$andino-workflow Telusuri penyebab tombol login tidak merespons, perbaiki secara minimal, lalu verifikasi.
```

```text
$andino-workflow Redesign landing page agar lebih mudah dibaca di mobile. Pertahankan identitas visual dan konten utama.
```

State the outcome and important constraints directly. No list of every installed skill/MCP or multiple slash commands is needed. Andino selects and activates relevant supporting skills when the host allows it, and reports unavailable capabilities. Trivial tasks outside required routes may use no specialist.

When checking compliance, look for routing-reference loading (unless already in context), actual supporting-skill activation when required, and task evidence. Not every reference needs to be read; a claimed skill name alone is not proof of use.

## Skill combinations by task

`andino-workflow` is the single entry point and routes required skills by itself, so a prompt only needs to name it plus the skills that are not activated automatically. Do not list every skill: Superpowers and Agent Skills are individual skills, not a bundle to load together. `focus` and `verification-before-completion` are activated by Andino when needed. Use `anti-slop` only when a concrete UI, copy, or code quality defect appears.

| Task | Suggested combination | Notes |
| --- | --- | --- |
| New frontend (landing page, portfolio, company profile) | `andino-workflow` → `design-taste-frontend` → `impeccable` | Taste produces the visual direction; Impeccable evaluates and refines it. Check rendered screenshots before calling it done. |
| Polish an existing UI | `andino-workflow` → `impeccable` | Add Taste only when the design direction should change. |
| Dashboard, admin panel, multi-page app | `andino-workflow` → `impeccable` + `frontend-ui-engineering` | Taste is not needed for every dashboard. |
| Website cloning | `andino-workflow` → `clone-website` | Fidelity first. For a redesign afterwards, continue with Taste and Impeccable. |
| New backend feature | `andino-workflow` + `test-driven-development` | Add `search-first` when researching solutions or libraries, and `api-and-interface-design` for API contracts. |
| Bug with unknown cause | `andino-workflow` → `systematic-debugging` → `test-driven-development` | Use TDD for the regression test or behavior fix. |
| Fragile codebase, repeated patches, regressions | `andino-workflow` → `ai-codebase-rescue` | Use after there is evidence of a structural problem, not just ugly code. |
| Overly complex code | `andino-workflow` → `code-simplification` | For existing code. `ponytail` fits better for preventing over-engineering before implementation. |
| Code review | `andino-workflow` → `code-review-and-quality` | Add `security-and-hardening` or `performance-optimization` only when a relevant need is found. |
| Thesis / research | `andino-workflow` → `skripsi-skill` | Add coding skills only when the task involves software implementation. |
| API, authentication, authorization | `andino-workflow` + `api-and-interface-design` + `security-and-hardening` | Important for systems handling data and access rights. |
| Slow website | `andino-workflow` → `performance-optimization` | Measure first. If the root cause is unknown, use `systematic-debugging` to investigate. |
| Database or framework migration | `andino-workflow` + `deprecation-and-migration` | Add `search-first` for unclear version compatibility and TDD for regression protection. |
| UI / browser testing | `andino-workflow` + `browser-testing-with-devtools` | Use a real browser with Playwright or DevTools to verify interaction and rendering. |
| CI/CD and deployment | `andino-workflow` + `ci-cd-and-automation` or `shipping-and-launch` | Pick by phase: building the pipeline or preparing a release. |
| Technical documentation and architecture decisions | `andino-workflow` + `documentation-and-adrs` | For important technical decisions, not every small change. |

## External resources — manual installation

Third-party skills/plugins and MCP servers must be installed or connected separately using their own setup instructions. Select only the capabilities relevant to your task.

Skills and plugin families: [Superpowers](https://github.com/obra/superpowers),
[Ponytail](https://github.com/DietrichGebert/ponytail),
[Impeccable](https://github.com/pbakaus/impeccable), [Taste Skill](https://www.tasteskill.dev/),
[AI Website Cloner](https://github.com/JCodesMore/ai-website-cloner-template),
[Graphify](https://graphify.net/), [Anti-Slop](https://github.com/miqdadbadjuber/anti-slop), and [Agent Skills](https://github.com/addyosmani/agent-skills).

MCP servers: [Context7](https://github.com/upstash/context7),
[Playwright MCP](https://github.com/microsoft/playwright-mcp),
[Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp),
[Git MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/git),
[Draw.io MCP](https://www.npmjs.com/package/@drawio/mcp),
[StarUML MCP](https://www.npmjs.com/package/staruml-mcp-server), and specialized/on-demand
[Premiere Pro MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) and
[Cheat Engine MCP bridge](https://github.com/miscusi-peek/cheatengine-mcp-bridge).

## Focus

Andino loads `focus` as its default communication skill, including direct answers.
Setup resolves the dependency automatically; repeat activation reuses valid context.
It changes communication, not task scope, investigation or verification. Higher
instructions, explicit style requests and `A. PRIORITAS` retain priority.

To select Focus alone, choose it in custom setup or run:

```sh
ai-rules setup --capability focus
```

After reloading the host, use `$focus [request]` in Codex or `/focus [request]` in
Claude Code, OpenCode and Antigravity. It stays active in the conversation until
you change the preference (for example, `stop focus`). Rerun setup to update it.

For ChatGPT and other web chatbots, copy `A. PRIORITAS` and `X. Focus` from the
[WebBased README](https://github.com/andinoferdi/AI-RULES/tree/WebBased#x-focus).
No skill loader is required. Focus adapts the MIT-licensed i-have-adhd; the runtime
and WebBased distribution each retain its attribution and full license notice.

Validation details: [Focus integration](docs/exec-plans/completed/focus.md).
The [Focus contract evaluation](docs/validation/focus-contract/report.md) records
paired model outputs, observed improvements and remaining behavioral limits.
Setup downloads Focus from its own distribution branch. The release manifest also
pins Focus and Andino for `--source bundled` installations. File and entry-point
checks do not prove that a running agent has loaded the skill.
