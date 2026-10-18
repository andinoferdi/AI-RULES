# AI-RULES

## Distribution branches

| Branch | Purpose |
| --- | --- |
| [`main`](https://github.com/andinoferdi/AI-RULES/tree/main) | Installer source, tests, release tooling, and validation evidence |
| [`WebBased`](https://github.com/andinoferdi/AI-RULES/tree/WebBased) | Web/chat rules and project templates |
| [`search-first`](https://github.com/andinoferdi/AI-RULES/tree/search-first) | Existing-solution research before implementation |
| [`focus`](https://github.com/andinoferdi/AI-RULES/tree/focus) | Clear, concise, actionable communication |
| [`council`](https://github.com/andinoferdi/AI-RULES/tree/council) | Five-perspective decision review and verdict |
| [`andino-workflow`](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow) | Adaptive workflow, capability routing, and portable checkpoints |
| [`ai-codebase-rescue`](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue) | Evidence-based stabilization of fragile codebases |
| [`skripsi-skill`](https://github.com/andinoferdi/AI-RULES/tree/skripsi-skill) | Thesis and research guidance |
| [`threejs-skills`](https://github.com/andinoferdi/AI-RULES/tree/threejs-skills) | One installable family containing all 45 Three.js/NixieFX methods and supporting files |

The `threejs` profile installs one complete `threejs-skills` family plus Andino,
Focus and Search First (four directories). Custom offers only **Three.js Skills**
for this collection. Its 45 internal methods are selected automatically by need or
explicitly named in a prompt, e.g. "threejs-skills, specifically threejs-shaders".
Use "andino-workflow and threejs-skills" for selective domain help in Andino's task.
Minimal/Engineering are unchanged. See [the package contract](docs/threejs/README.md).

Install the CLI from `main`. Setup downloads each skill from its own distribution branch, so you never switch branches or copy skill files by hand.

## Setup

Requirements: Python 3.11+, Git, and the AI agent you plan to use, already installed.

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
| Three.js Development | Complete Three.js family + Andino Workflow + Focus + Search First |
| Everything | All seven first-party capabilities, including the complete Three.js family |

Open a new agent session or reload its window after setup. Installing skills does not activate every method for every task. Third-party skills, plugins, and MCP servers need their own installation or connection.

Run `ai-rules setup` again to update the selected skills from their latest configured branches. To update the CLI itself, run these commands from a clean `main` checkout:

```sh
git pull --ff-only
python -m pip install .
ai-rules setup
```

Setup verifies files and entry points. It does not confirm that a running agent has used a skill. Review any reported conflict or unsupported installation layout before you replace files. See the [validation guide](evals/README.md) for testing details.

Council is optional in Custom setup selection and included in Everything. For standalone installation, use `ai-rules setup --capability council --host codex` (replace the host as needed). Council uses Focus for natural language and can assist Andino Workflow with consequential decisions; it does not replace Andino's lifecycle or guarantee independent sub-agents on every host.

## Skill combinations by task

`andino-workflow` is the single entry point. Its unified package contains 57
reviewed internal methods adapted from Addy Osmani Agent Skills, Matt Pocock Skills
and Superpowers. Name Andino and the task, or an explicit internal method such as
`tdd`, `decision-interview` or `domain-modeling`. Original source names in the
table are compatibility aliases for local guides; they need no upstream skill/plugin
installation. Andino reads only the methods needed for the current phase. Focus
remains its communication sibling; consequential acceptance uses bundled `verification`.
The unified working-tree candidate is tested locally; publication and pin advancement
remain separate authorized release actions. See [current evidence](docs/validation/andino-unified/README.md).

| Task | Suggested combination | Notes |
| --- | --- | --- |
| New frontend (landing page, portfolio, company profile) | `andino-workflow` + `search-first` → `design-taste-frontend` → `impeccable` | Taste produces the visual direction; Impeccable evaluates and refines it. Check rendered screenshots before calling it done. |
| Polish an existing UI | `andino-workflow` + `search-first` → `impeccable` | Add Taste only when the design direction should change. |
| Dashboard, admin panel, multi-page app | `andino-workflow` + `search-first` → `impeccable` + `frontend-ui-engineering` | Taste is not needed for every dashboard. |
| Website cloning | `andino-workflow` + `search-first` → `clone-website` | Fidelity first. For a redesign afterwards, continue with Taste and Impeccable. |
| New backend feature | `andino-workflow` + `search-first` + `test-driven-development` | Add `api-and-interface-design` for API contracts. |
| Bug with unknown cause | `andino-workflow` → `systematic-debugging` → `search-first` → `test-driven-development` | Diagnose first. Use `search-first` only if the fix needs an existing library or solution. Use TDD for the regression test. |
| Fragile codebase, repeated patches, regressions | `andino-workflow` + `search-first` → `ai-codebase-rescue` | Use after there is evidence of a structural problem, not just ugly code. |
| Overly complex code | `andino-workflow` + `search-first` → `code-simplification` | For existing code. `ponytail` fits better for preventing over-engineering before implementation. |
| Code review | `andino-workflow` + `search-first` → `code-review-and-quality` | Add `security-and-hardening` or `performance-optimization` only when a relevant need is found. |
| Thesis / research | `andino-workflow` + `search-first` → `skripsi-skill` | Add coding skills only when the task involves software implementation. |
| Consequential decision, strategy, or competing options | `andino-workflow` → `council` | Use for a meaningful trade-off that benefits from independent perspectives and peer review. Focus handles communication; Council does not replace Andino's lifecycle. Actual independent sub-agents depend on host support. |
| API, authentication, authorization | `andino-workflow` + `search-first` + `api-and-interface-design` + `security-and-hardening` | Use for systems that handle user data or access rights. |
| Slow website | `andino-workflow` + `search-first` → `performance-optimization` | Measure first. If the root cause is unknown, use `systematic-debugging` to investigate. |
| Database or framework migration | `andino-workflow` + `search-first` + `deprecation-and-migration` | `search-first` checks unclear version compatibility. Add TDD for regression protection. |
| UI / browser testing | `andino-workflow` + `search-first` + `browser-testing-with-devtools` | Use a real browser with Playwright or DevTools to verify interaction and rendering. |
| CI/CD and deployment | `andino-workflow` + `search-first` + `ci-cd-and-automation` or `shipping-and-launch` | Pick by phase: building the pipeline or preparing a release. |
| Technical documentation and architecture decisions | `andino-workflow` + `search-first` + `documentation-and-adrs` | Add `council` when a consequential architecture choice needs competing perspectives before recording the decision; skip it for routine documentation. |

## External resources: manual installation

Third-party skills/plugins and MCP servers must be installed or connected separately using their own setup instructions. Select only the capabilities relevant to your task.

Skills and plugin families: [Ponytail](https://github.com/DietrichGebert/ponytail),
[Impeccable](https://github.com/pbakaus/impeccable), [Taste Skill](https://www.tasteskill.dev/),
[AI Website Cloner](https://github.com/JCodesMore/ai-website-cloner-template),
[Graphify](https://graphify.net/) and [Anti-Slop](https://github.com/miqdadbadjuber/anti-slop).

Addy/Matt/Superpowers repositories are reviewed build/audit provenance for bundled
Andino methods, not runtime prerequisites. Preserve the complete Andino directory,
including `skills/`, local resources and legal notices. Installation runs no upstream
hooks, method examples, package managers or automatic fetch/update. Optional external
services are invoked only when actually available, relevant and authorized.

MCP servers: [Context7](https://github.com/upstash/context7),
[Playwright MCP](https://github.com/microsoft/playwright-mcp),
[Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp),
[Git MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/git),
[Draw.io MCP](https://www.npmjs.com/package/@drawio/mcp),
[StarUML MCP](https://www.npmjs.com/package/staruml-mcp-server), and specialized/on-demand
[Premiere Pro MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) and
[Cheat Engine MCP bridge](https://github.com/miscusi-peek/cheatengine-mcp-bridge).
