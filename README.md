# AI-RULES

> **Engineering skills and adaptive workflows for AI coding agents.** Investigate problems, apply test-driven development, protect against regressions, and check evidence before declaring completion.

AI coding agents can propose speculative rewrites, invent APIs or use deprecated ones, skip tests, and repeat failed approaches. **AI-RULES** provides engineering practices, specialist workflows, and deterministic quality checks for Claude Code, Codex, OpenCode, and Antigravity.

---

## Quick Start

Requirements: Python 3.11+, Git, and any supported AI coding agent.

```sh
# 1. Clone & install the AI-RULES CLI orchestrator
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# 2. Run interactive setup (choose host & profile)
ai-rules setup
```

Select your host (`codex`, `claude-code`, `opencode`, `antigravity-cli`, `antigravity-ide`) and your profile (**Minimal** is recommended for first-time setup). Start a fresh agent session, and all installed skills are immediately available via slash commands (`/`) or dollar commands (`$`).

---

## First-Party Capabilities

AI-RULES distributes 8 core capabilities and 59 native member skills across dedicated branches:

| Capability | Branch | Purpose | Example Command |
|---|---|---|---|
| **[Andino Workflow](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow)** | `andino-workflow` | Adaptive workflow protocol + **59 composable member skills** (`andino-*`). | `/andino-workflow`<br>`/andino-tdd`<br>`/andino-brainstorming` |
| **[Focus](https://github.com/andinoferdi/AI-RULES/tree/focus)** | `focus` | Direct, result-first communication style (Indonesian & English). | `/focus`<br>`$focus` |
| **[Search First](https://github.com/andinoferdi/AI-RULES/tree/search-first)** | `search-first` | Evidence-based solution research (`ADOPT`, `EXTEND`, `COMPOSE`, `BUILD`). | `/search-first`<br>`$search-first` |
| **[AI Codebase Rescue](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue)** | `ai-codebase-rescue` | Stabilize fragile subsystems (`KEEP`, `REFACTOR`, `REMAKE`, `REMOVE`). | `/ai-codebase-rescue`<br>`$ai-codebase-rescue` |
| **[Council](https://github.com/andinoferdi/AI-RULES/tree/council)** | `council` | High-stakes decision analysis via 5 independent lenses and anonymous review. | `/council`<br>`$council` |
| **[Natural Writing](https://github.com/andinoferdi/AI-RULES/tree/natural-writing)** | `natural-writing` | Prose writing, rewriting, and review without formulaic AI tells. | `/natural-writing`<br>`$natural-writing` |
| **[Skripsi Skill](https://github.com/andinoferdi/AI-RULES/tree/skripsi-skill)** | `skripsi-skill` | Academic thesis, literature matrix, and research defense guidance. | `/skripsi-skill`<br>`$skripsi-skill` |
| **[Three.js Skills](https://github.com/andinoferdi/AI-RULES/tree/threejs-skills)** | `threejs-skills` | 3D graphics family with 45 WebGL/WebGPU and shader methods. | `/threejs-skills`<br>`$threejs-skills` |
| **[WebBased](https://github.com/andinoferdi/AI-RULES/tree/WebBased)** | `WebBased` | 47 ready-to-use prompt templates for web chatbots (Claude/ChatGPT Web). | *Copy-paste directly* |

---

## Setup Profiles

The `ai-rules setup` CLI offers these installation bundles:

| Profile | Target Needs | Included Capabilities |
|---|---|---|
| **Minimal** (`minimal`) | Core adaptive development & research | `andino-workflow` (+ 59 member skills), `focus`, `search-first` |
| **Engineering** (`engineering`) | Full-stack coding & codebase recovery | Minimal + `ai-codebase-rescue` |
| **Research / Skripsi** (`research-skripsi`) | Academic writing & thesis preparation | Minimal + `skripsi-skill` + `natural-writing` |
| **Three.js Development** (`threejs`) | 3D graphics, shaders, and animations | Minimal + `threejs-skills` (45 3D methods) |
| **Everything** (`everything`) | Full installation | All 8 first-party capabilities |

### Non-Interactive / Scripted Usage

```sh
# Install engineering profile for Claude Code in project scope
ai-rules setup --host claude-code --profile engineering --scope project --project-root . --yes --non-interactive

# Install Everything profile for Codex globally
ai-rules setup --host codex --profile everything --scope global --yes --non-interactive

# Update installed capabilities to latest verified release
ai-rules update --host claude-code --profile engineering --scope project --project-root . --yes --non-interactive

# Verify installed integrity with health check
ai-rules doctor --host claude-code --scope project --project-root .
```

---

## How AI-RULES Compares

| Feature | Superpowers | Agent Skills | **AI-RULES** |
|---|---|---|---|
| **Invocation Model** | Monolithic global bootstrap | Individual commands | **Bidirectional routing** (Main orchestrator $\leftrightarrow$ 59 atomic member skills) |
| **Namespace Isolation** | Unprefixed (risk of collisions) | Command wrappers | **Namespaced** (`andino-*` prefix across all hosts) |
| **Context Window Overhead** | High (loads entire methodology) | Variable | **On-demand loading** (Compact frontmatter) |
| **Anti-Looping & Checkpoints** | Custom session state | Manual stop-conditions | **Deterministic Portable Checkpoints** with Git drift detection |
| **Multi-Host CLI Installer** | Per-harness scripts | `npx skills` | **Shared native installer** (`ai-rules setup` with atomic rollback) |

---

## Practical Task Recipes

Name the skills relevant to your task in the prompt:

```text
# 1. Feature implementation with failing tests first
Use andino-workflow and andino-tdd to implement the JWT refresh endpoint with red-green-refactor loop.

# 2. Investigating an unknown bug
Use andino-workflow and andino-debugging to isolate why database connection pools leak under load.

# 3. High-stakes architectural decision
Use andino-workflow, search-first, and council to evaluate migrating from REST to gRPC.

# 4. Stabilizing legacy code
Use andino-workflow and ai-codebase-rescue to audit repeated checkout failures and establish regression tests.

# 5. Academic thesis writing
Use andino-workflow, skripsi-skill, and natural-writing to draft Chapter 2 literature review from verified papers.
```

---

## Supported AI Hosts

| Host Agent | Discovery Path (Global) | Discovery Path (Project) | Command Syntax |
|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` | `/andino-workflow`, `/andino-tdd` |
| **Codex** | `~/.agents/skills/` | `.agents/skills/` | `$andino-workflow`, `$andino-tdd` |
| **OpenCode** | `~/.config/opencode/skills/` | `.agents/skills/` | `/andino-workflow`, `/andino-tdd` |
| **Antigravity CLI** | `~/.gemini/antigravity-cli/skills/` | `.agents/skills/` | Slash commands & native `skill` tool |
| **Antigravity IDE** | `~/.gemini/config/skills/` | `.agents/skills/` | Slash commands & native `skill` tool |

---

## External resources: manual installation

These optional skills and MCP tools are installed separately from AI-RULES profiles.
Follow each project's setup instructions and connection requirements.

- **UI and specialist skills:** [Taste Skill](https://www.tasteskill.dev/),
  [Impeccable](https://github.com/pbakaus/impeccable),
  [AI Website Cloner](https://github.com/JCodesMore/ai-website-cloner-template),
  [Anti-Slop](https://github.com/miqdadbadjuber/anti-slop),
  [Ponytail](https://github.com/DietrichGebert/ponytail), and
  [Graphify](https://graphify.net/).
- **Marketing and branding:** [LinkedIn Skills](https://github.com/sergebulaev/linkedin-skills)
  and [Logo Design Skill](https://github.com/kaankiziltug/logo-design-skill).
- **Web and social content:** [Agent-Reach](https://github.com/Panniantong/Agent-Reach).
- **Shell command proxy:** [RTK](https://github.com/rtk-ai/rtk).
- **Reverse Engineer Anything:** [REA](https://github.com/morluto/rea).
- **Documentation and browser MCP tools:** [Context7](https://github.com/upstash/context7),
  [Playwright MCP](https://github.com/microsoft/playwright-mcp), and
  [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp).
- **Task-specific MCP tools:** [Git MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/git),
  [Draw.io MCP](https://www.npmjs.com/package/@drawio/mcp),
  [StarUML MCP](https://www.npmjs.com/package/staruml-mcp-server),
  [Premiere Pro MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP), and
  [Cheat Engine MCP bridge](https://github.com/miscusi-peek/cheatengine-mcp-bridge).

Install only what your task needs. Bundled Addy/Matt/Superpowers methods do not
require their upstream bootstrap plugins. External services require their own tools
and permissions.

---

## Provenance & Licenses

- AI-RULES-authored code, installer engines, and documentation on `main` are licensed under the **[MIT License](LICENSE)**, copyright 2026 andinoferdi.
- Third-party methods and inspirations retain their original licenses and attributions:
  - `andino-workflow` adapts techniques from [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills), [Matt Pocock Skills](https://github.com/mattpocock/skills), and [Superpowers](https://github.com/obra/superpowers) ([provenance records](https://github.com/andinoferdi/AI-RULES/blob/andino-workflow/references/legal/provenance.md)).
  - `focus` credits [Ayoub Ghriss's i-have-adhd](https://github.com/ayghri/i-have-adhd).
  - `search-first` credits [Affaan Mustafa's ECC Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md).
  - `council` draws inspiration from [Ole Lehmann & Andrej Karpathy's LLM Council](https://github.com/aiwithremy/claude-skills-llm-council).
  - `threejs-skills` retains upstream resource-specific MIT, CC0, and GPL notices.
