# AI-RULES

Reusable skills for AI agents: investigate the right problem, choose methods for
the task, and verify the result before claiming completion.

Andino Workflow coordinates work with proportional investigation and portable
checkpoints. Focus keeps communication clear; Search First checks existing
solutions when research is needed. Add specialists for codebase recovery, thesis
research, consequential decisions, or Three.js development.

## Quick start

You need Python 3.11+, Git, and an installed agent. From your chosen Python
environment:

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup
```

Choose your hosts and the **Minimal** profile, review the installation plan, then
confirm it. Minimal installs Andino Workflow, Focus and Search First. Start a new
agent session or reload its window after installation.

For example, in Codex:

```text
$andino-workflow resume the existing task plan, check repository drift, and finish the next verified step
```

In Claude Code, use `/andino-workflow`. In OpenCode and Antigravity, ask the agent
to use `andino-workflow` through its supported invocation mechanism. Installation
checks files; it does not prove native discovery, automatic selection, or live use.

## Available skills

| Skill | Use it for |
| --- | --- |
| [Andino Workflow](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow) | Coordinating uncertain or multi-step work and resuming checkpoints |
| [Focus](https://github.com/andinoferdi/AI-RULES/tree/focus) | Clear answers, actionable steps, and useful status updates |
| [Search First](https://github.com/andinoferdi/AI-RULES/tree/search-first) | Comparing existing solutions, integrations, and version-sensitive APIs |
| [AI Codebase Rescue](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue) | Stabilizing fragile subsystems with evidence and regression protection |
| [Skripsi Skill](https://github.com/andinoferdi/AI-RULES/tree/skripsi-skill) | Research planning, literature, methodology, revision, and defense preparation |
| [Council](https://github.com/andinoferdi/AI-RULES/tree/council) | Reviewing consequential choices through independent perspectives when supported |
| [Three.js Skills](https://github.com/andinoferdi/AI-RULES/tree/threejs-skills) | Scenes, shaders, animation, interaction, games, and NixieFX |

Andino is one native entrypoint with 59 internal methods adapted from
Addy Osmani Agent Skills, Matt Pocock Skills and Superpowers. Requirements, TDD,
debugging, architecture and review methods are bundled local guides, not dozens
of extra native skills. Those upstream projects do not need a separate runtime
installation. See the [method index](https://github.com/andinoferdi/AI-RULES/blob/andino-workflow/references/internal-method-index.md).

Three.js is likewise one installable family with 45 internal methods and their
supporting resources. Name the family and, when useful, a method such as
`threejs-shaders`. Installing a family does not activate every method on every task.

## Setup

The CLI offers these profiles and a Custom selection:

| Profile | Included capabilities |
| --- | --- |
| Minimal (`minimal`) | Andino Workflow, Focus, Search First |
| Engineering (`engineering`) | Minimal + AI Codebase Rescue |
| Research / Skripsi (`research-skripsi`) | Minimal + Skripsi Skill |
| Three.js Development (`threejs`) | Minimal + the complete Three.js family |
| Everything (`everything`) | All seven first-party skills |

Installer adapters target Codex (`codex`), Claude Code (`claude-code`), OpenCode
(`opencode`), Antigravity CLI (`antigravity-cli`) and Antigravity IDE / 2.0
(`antigravity-ide`). Adapter support and structural checks are distinct from live
host behavior. Each runtime README explains invocation and discovery limits.

For a project-scoped installation, preview the plan before applying it:

```sh
ai-rules setup --host codex --profile engineering --scope project --project-root . --dry-run --non-interactive
ai-rules setup --host codex --profile engineering --scope project --project-root . --yes --non-interactive
```

For a single capability, use `--capability council` or another catalog ID in place
of `--profile engineering`. Andino also installs Focus and Search First; Council
also installs Focus. The Three.js family has no required sibling, while its
profile installs all four directories. Custom does not offer its internal methods
as separate packages.

Setup defaults to global scope. Repeat the same host, scope, profile or capability
selection to update it. Default `--source latest` checks the configured branches;
`--source bundled` uses the CLI's frozen manifest without checking freshness.
Source checkouts acquire pinned content through Git when an embedded bundle is
unavailable. Preserve local edits and review reported conflicts before replacement.

Setup shows the active phase before installed-state inspection, Git fetch, source
bundle preparation, reconciliation and plan generation. On an interactive terminal,
an orange spinner and elapsed time keep updating during blocking work. Counts appear
only for known work units. After approval, `processed / total` counts resolved
targets, including dependencies; all operations belonging to a target finish before
it is counted. Processed includes failed and blocked targets and is not a success
percentage. The final summary separates installed, updated, current, failed, blocked,
skipped, manual and unfinished targets. A final verification failure removes that
target from the successful count.

The default plan groups actions by host. Global scope uses user skill locations for
the selected hosts; project scope shows the project root once. Full source URLs,
target paths, backup flags, commands and operation diagnostics are available with
`--verbose`. Errors and conflict reasons remain visible without it. Installation
records and the backup root, when relevant, are printed at the end.

```sh
ai-rules setup --host codex --profile everything --dry-run --verbose --non-interactive
ai-rules setup --host codex --profile minimal --yes --non-interactive --no-progress
```

`--no-progress` disables animation and keeps plain milestones. Redirected output,
non-TTY, `--non-interactive`, CI and dumb terminals use plain output automatically,
without cursor animation or ANSI escapes. `NO_COLOR` removes color. Narrow terminals
use a per-host action list instead of squeezing table columns. `--dry-run` resolves
and displays the plan without writing installation or state files; latest source
checks still use temporary Git workspaces. `--yes` keeps its existing approval
behavior. Ctrl+C during installer work exits with code 130, stops the live display and retains completed
changes/backups; an interrupted atomic directory replacement restores the previous
tree. Cancelling selection or confirmation keeps the existing no-change behavior.
Rerun the same setup command to inspect remaining work. Refresh the agent
session/window after installation; file verification does not establish native
discovery or live skill use.

To update the CLI itself, from a clean `main` checkout:

```sh
git pull --ff-only
python -m pip install .
```

Then repeat your setup command. Setup does not install optional services, execute
method examples or upstream hooks, or establish that a model followed a skill.

## Skill combinations by task

Choose a combination for the actual task; the full catalog is not a checklist to
activate every time. All seven first-party skills appear below. When Andino is
active, it coordinates the lifecycle, Focus shapes communication, and Search First
handles research when needed. Focus is named explicitly where the requested output
especially benefits from its communication style; it remains Andino's default layer.

Invoke a combination in plain language, for example:

```text
Use andino-workflow, search-first and council to compare these migration paths, then record the accepted decision and verification plan.
```

Methods such as `tdd`, `debugging`, `code-review`, and `documentation-and-adrs`
are bundled Andino guides. They do not require separate upstream installations.

### Engineering and everyday delivery

| Task | Skills to combine | Focus of the request |
| --- | --- | --- |
| Resume a paused implementation | `andino-workflow` + `focus` | Read the checkpoint, check drift and identify the next verified step. |
| Implement a behavior change | `andino-workflow` + `search-first` | Reuse existing code; apply the bundled `tdd` method to the changed behavior. |
| Select an integration | `andino-workflow` + `search-first` + `council` | Compare supported options and review consequential trade-offs before implementation. |
| Design an API contract | `andino-workflow` + `search-first` | Use `api-and-interface-design`; check consumers and version-specific assumptions. |
| Diagnose an unknown bug | `andino-workflow` + `focus` | Use `debugging` before repair; add Search First only for an unresolved research need. |
| Review the current diff | `andino-workflow` + `focus` | Use `code-review`; report actionable findings with evidence and severity. |
| Investigate a performance regression | `andino-workflow` + `search-first` | Measure first; use `performance-optimization` after the bottleneck is established. |
| Plan a database or framework migration | `andino-workflow` + `search-first` + `council` | Check compatibility, reversibility and regression protection. |
| Write technical documentation or an ADR | `andino-workflow` + `focus` | Use `documentation-and-adrs`; explain the accepted contract and its rationale. |

### Codebase recovery and consequential decisions

| Task | Skills to combine | Focus of the request |
| --- | --- | --- |
| Stabilize repeated subsystem regressions | `andino-workflow` + `ai-codebase-rescue` + `search-first` | Establish evidence and regression protection before choosing a repair. |
| Compare refactoring with a bounded remake | `andino-workflow` + `ai-codebase-rescue` + `council` | Preserve verified behavior and review KEEP/REFACTOR/REMAKE options. |
| Explain a technical-debt recovery assessment | `ai-codebase-rescue` + `focus` | Present the bounded findings, dispositions and verification gaps clearly. |
| Assess a fragile prototype before launch | `andino-workflow` + `ai-codebase-rescue` + `council` | Evaluate evidenced fragility and use `shipping-and-launch` for launch readiness. |
| Choose a product or architecture direction | `andino-workflow` + `council` + `search-first` | Ground alternatives, challenge assumptions and record one accepted decision. |

### Thesis and research

| Task | Skills to combine | Focus of the request |
| --- | --- | --- |
| Develop a thesis proposal | `andino-workflow` + `skripsi-skill` + `focus` | Keep the approved topic, current stage and campus requirements explicit. |
| Search and synthesize literature | `andino-workflow` + `skripsi-skill` + `search-first` | Trace claims to sources and document screening and evidence limits. |
| Compare research designs | `skripsi-skill` + `council` + `search-first` | Review methodological fit against available data and institutional constraints. |
| Resolve supervisor revisions or prepare a defense | `andino-workflow` + `skripsi-skill` + `focus` | Track requested revisions and explain supported claims without inventing results. |

### Three.js and interactive graphics

| Task | Skills to combine | Focus of the request |
| --- | --- | --- |
| Build a scene or animation | `andino-workflow` + `threejs-skills` + `search-first` | Select relevant scene/animation methods and verify the actual library version. |
| Develop a shader or NixieFX effect | `andino-workflow` + `threejs-skills` | Name a method such as `threejs-shaders`; inspect the rendered result. |
| Prototype an interactive 3D game | `andino-workflow` + `threejs-skills` + `search-first` | Select gameplay and interaction methods; test the playable behavior. |
| Recover a repeatedly broken graphics subsystem | `andino-workflow` + `threejs-skills` + `ai-codebase-rescue` | Establish the recurring failure and protect rendering/interaction contracts. |
| Build an interactive research visualization | `andino-workflow` + `skripsi-skill` + `threejs-skills` | Keep research claims traceable and verify the graphics against the supplied data. |

### Combinations with optional external skills

Install these external skills separately using the resources below.

| Task | Skills to combine | Focus of the request |
| --- | --- | --- |
| Design and evaluate a new UI | `andino-workflow` + `search-first` + `design-taste-frontend` + `impeccable` | Establish the design direction, then critique and verify the rendered interface. |
| Polish an existing interface | `andino-workflow` + `focus` + `impeccable` | Improve clarity and usability within the accepted design direction. |
| Reproduce a supplied website | `andino-workflow` + `search-first` + `clone-website` | Inspect the reference and verify fidelity and interactions. |
| Investigate a shipped application or binary | `andino-workflow` + `search-first` + `reverse-engineer-anything` | Use the [REA skill](https://github.com/morluto/rea/tree/main/.agents/skills/reverse-engineer-anything) for artifact/runtime evidence; report unavailable analysis tools honestly. |

For ordinary source-repository analysis, use normal repository tools rather than
REA. Installing its skill supplies instructions and references; actual REA analysis
requires available tools and applicable providers. Council discloses a single-agent
perspective review when independent agents are unavailable. Activating any skill
grants no additional tool permissions or authority to publish or change live data.

## Distribution branches

`main` owns the installer and quality plane. Setup acquires each complete runtime
package from its own branch; users do not need to switch branches or copy files.

| Branch | Distributed content |
| --- | --- |
| [`main`](https://github.com/andinoferdi/AI-RULES/tree/main) | CLI, catalog, profiles, tests, validators, release manifest and evidence |
| [`WebBased`](https://github.com/andinoferdi/AI-RULES/tree/WebBased) | Web/chat rules and project templates; separate from CLI skill packages |
| [`andino-workflow`](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow) | Andino entrypoint, internal guides, resources and notices |
| [`ai-codebase-rescue`](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue) | Recovery methodology and focused references |
| [`council`](https://github.com/andinoferdi/AI-RULES/tree/council) | Decision review methodology |
| [`focus`](https://github.com/andinoferdi/AI-RULES/tree/focus) | Communication contract and bundled language references |
| [`search-first`](https://github.com/andinoferdi/AI-RULES/tree/search-first) | Research methodology and online research playbook |
| [`skripsi-skill`](https://github.com/andinoferdi/AI-RULES/tree/skripsi-skill) | Research guidance, references and templates |
| [`threejs-skills`](https://github.com/andinoferdi/AI-RULES/tree/threejs-skills) | One family with internal guides, code, shaders, assets and notices |

## External resources: manual installation

These are optional additions with their own installation, connection and permission
requirements. They are not installed by an AI-RULES profile.

- UI and specialist skills: [Taste Skill](https://www.tasteskill.dev/),
  [Impeccable](https://github.com/pbakaus/impeccable),
  [AI Website Cloner](https://github.com/JCodesMore/ai-website-cloner-template),
  [Anti-Slop](https://github.com/miqdadbadjuber/anti-slop),
  [Ponytail](https://github.com/DietrichGebert/ponytail), and
  [Graphify](https://graphify.net/).
- Shell command proxy: [RTK](https://github.com/rtk-ai/rtk).
- Reverse engineering skill: [REA's `reverse-engineer-anything`](https://github.com/morluto/rea/tree/main/.agents/skills/reverse-engineer-anything)
  from [morluto/rea](https://github.com/morluto/rea). Install only the skill and its
  bundled references with the upstream [skill-only installation](https://github.com/morluto/rea/blob/main/docs/installation.md#skill-only-installation):

  ```sh
  npx skills add morluto/rea --skill reverse-engineer-anything
  ```

  This command does not register the REA MCP server or install analysis engines.
  REA is an optional external skill, not an AI-RULES profile or bundled method.
- Documentation and browser instruments: [Context7](https://github.com/upstash/context7),
  [Playwright MCP](https://github.com/microsoft/playwright-mcp), and
  [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp).
- Task-specific instruments: [Git MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/git),
  [Draw.io MCP](https://www.npmjs.com/package/@drawio/mcp),
  [StarUML MCP](https://www.npmjs.com/package/staruml-mcp-server),
  [Premiere Pro MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP), and
  [Cheat Engine MCP bridge](https://github.com/miscusi-peek/cheatengine-mcp-bridge).

Select only what the task needs. Bundled Addy/Matt/Superpowers methods require none
of their upstream bootstrap plugins; external services still require actual tools
and authorization.

## Architecture and verification

Each runtime package has one root `SKILL.md`. Internal methods use `GUIDE.md` and
on-demand resources. Preserve the entire package, including notices and assets.
The installer resolves dependencies, stages and verifies whole directories, and
preserves modified or unrecognized targets for conflict review.

The unified Andino runtime is published. The [release manifest](src/ai_rules/release/data/release_manifest.json)
records frozen runtime commits; a tagged standalone installer release is a separate
publication step. Historical evaluations remain tied to the revisions they tested.

- [Package and release contract](docs/agent-skill-family-standard.md)
- [Capability evaluation guide](evals/README.md)
- [Unified Andino evidence and live-host limits](docs/validation/andino-unified/README.md)
- [Andino evolution, setup verification and live-host limits](docs/validation/andino-evolution/README.md)
- [Three.js inventory, provenance and verification](docs/threejs/README.md)

From `main`, after fetching the runtime refs, run the package validators and tests
described in the evaluation guide. Deterministic checks prove their stated scope;
native discovery, model behavior and rendering need separate observed evidence.

## Provenance, credits, and licenses

AI-RULES-authored code and documentation on `main` are available under the
[MIT License](LICENSE), copyright 2026 andinoferdi. Third-party material retains
its applicable licenses, copyright notices and attribution. The license on `main`
does not relicense resources distributed on other branches.

Andino adapts reviewed snapshots of [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills),
[Matt Pocock Skills](https://github.com/mattpocock/skills), and
[Superpowers](https://github.com/obra/superpowers). Its
[provenance and retained MIT notices](https://github.com/andinoferdi/AI-RULES/blob/andino-workflow/references/legal/provenance.md)
identify the source revisions and authors.

Focus credits [Ayoub Ghriss's i-have-adhd](https://github.com/ayghri/i-have-adhd);
Search First credits [Affaan Mustafa's ECC Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md).
Their runtime packages retain MIT notices. Council documents its independently
written adaptation and inspiration in its README. Three.js retains resource-specific
MIT, CC0 and GPL notices; family registration does not create a blanket license.
Consult the applicable package and resource notices before redistribution. These
credits do not imply upstream endorsement or replace third-party license terms.
