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

Andino is one native entrypoint with 57 reviewed internal methods adapted from
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

To update the CLI itself, from a clean `main` checkout:

```sh
git pull --ff-only
python -m pip install .
```

Then repeat your setup command. Setup does not install optional services, execute
method examples or upstream hooks, or establish that a model followed a skill.

## Skill combinations by task

Start with the capability the task needs. Andino can coordinate broader work;
its Focus dependency shapes communication, and Search First runs only when there
is a research need. The method names below refer to bundled Andino guides.

| Task | Example request |
| --- | --- |
| Implement a behavior change | `Use andino-workflow and its tdd method for this change.` |
| Diagnose an unknown bug | `Use andino-workflow to diagnose this failure before repair.` |
| Review an implementation | `Use andino-workflow's code-review method on the current diff.` |
| Compare an unfamiliar integration | `Use search-first to compare supported options for this stack.` |
| Recover a fragile subsystem | `Use andino-workflow and ai-codebase-rescue for the repeated checkout regressions.` |
| Develop a thesis proposal | `Use andino-workflow and skripsi-skill; keep my approved topic and campus requirements.` |
| Resolve a consequential trade-off | `Use council to compare these migration paths and their reversibility.` |
| Build a shader effect | `Use andino-workflow and threejs-skills, specifically threejs-shaders.` |
| Design and evaluate a UI | `Use andino-workflow with design-taste-frontend, then impeccable.` |

The last example needs optional external skills. Council discloses a single-agent
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
- [Three.js inventory, provenance and verification](docs/threejs/README.md)

From `main`, after fetching the runtime refs, run the package validators and tests
described in the evaluation guide. Deterministic checks prove their stated scope;
native discovery, model behavior and rendering need separate observed evidence.

## Provenance, credits, and licenses

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
credits do not imply upstream endorsement or a repository-wide license grant.
