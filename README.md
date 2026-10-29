# AI-RULES

> **Production-grade engineering skills & adaptive workflows for AI coding agents.** Investigate the right problem, enforce test-driven development, protect against regressions, and verify evidence before declaring completion.

AI coding agents are fast, but left unguided they jump to speculative rewrites, hallucinate deprecated APIs, skip tests, and get trapped in repetitive loops. **AI-RULES** equips your agents (Claude Code, Codex, OpenCode, Antigravity) with structured engineering disciplines, composable specialist workflows, and deterministic quality gates.

---

## ⚡ Quick Start (30-Second Setup)

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

## 🧭 First-Party Capabilities

AI-RULES distributes 8 core capabilities and 59 native member skills across dedicated branches:

| Capability | Branch | Purpose | Example Command |
|---|---|---|---|
| **[Andino Workflow](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow)** | `andino-workflow` | Master adaptive workflow protocol + **59 composable member skills** (`andino-*`). | `/andino-workflow`<br>`/andino-tdd`<br>`/andino-brainstorming` |
| **[Focus](https://github.com/andinoferdi/AI-RULES/tree/focus)** | `focus` | Zero-filler, result-first communication style (Indonesian & English). | `/focus`<br>`$focus` |
| **[Search First](https://github.com/andinoferdi/AI-RULES/tree/search-first)** | `search-first` | Evidence-based solution research (`ADOPT`, `EXTEND`, `COMPOSE`, `BUILD`). | `/search-first`<br>`$search-first` |
| **[AI Codebase Rescue](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue)** | `ai-codebase-rescue` | Stabilize fragile subsystems (`KEEP`, `REFACTOR`, `REMAKE`, `REMOVE`). | `/ai-codebase-rescue`<br>`$ai-codebase-rescue` |
| **[Council](https://github.com/andinoferdi/AI-RULES/tree/council)** | `council` | High-stakes decision analysis via 5 independent lenses and anonymous review. | `/council`<br>`$council` |
| **[Natural Writing](https://github.com/andinoferdi/AI-RULES/tree/natural-writing)** | `natural-writing` | Prose writing, rewriting, and review without formulaic AI tells. | `/natural-writing`<br>`$natural-writing` |
| **[Skripsi Skill](https://github.com/andinoferdi/AI-RULES/tree/skripsi-skill)** | `skripsi-skill` | Academic thesis, literature matrix, and research defense guidance. | `/skripsi-skill`<br>`$skripsi-skill` |
| **[Three.js Skills](https://github.com/andinoferdi/AI-RULES/tree/threejs-skills)** | `threejs-skills` | Complete 3D graphics family with 45 WebGL/WebGPU and shader methods. | `/threejs-skills`<br>`$threejs-skills` |
| **[WebBased](https://github.com/andinoferdi/AI-RULES/tree/WebBased)** | `WebBased` | 47 ready-to-use prompt templates for web chatbots (Claude/ChatGPT Web). | *Copy-paste directly* |

---

## 📦 Setup Profiles

The `ai-rules setup` CLI provides tuned installation bundles:

| Profile | Target Needs | Included Capabilities |
|---|---|---|
| **Minimal** (`minimal`) | Core adaptive development & research | `andino-workflow` (+ 59 member skills), `focus`, `search-first` |
| **Engineering** (`engineering`) | Full-stack coding & codebase recovery | Minimal + `ai-codebase-rescue` |
| **Research / Skripsi** (`research-skripsi`) | Academic writing & thesis preparation | Minimal + `skripsi-skill` + `natural-writing` |
| **Three.js Development** (`threejs`) | 3D graphics, shaders, and animations | Minimal + `threejs-skills` (45 3D methods) |
| **Everything** (`everything`) | The complete autonomous agent power rig | All 8 first-party capabilities |

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

## 🏆 How AI-RULES Compares

| Feature | Superpowers | Agent Skills | **AI-RULES** |
|---|---|---|---|
| **Invocation Model** | Monolithic global bootstrap | Disjointed individual commands | **True Bidirectional Mesh** (Master orchestrator $\leftrightarrow$ 59 atomic member skills) |
| **Namespace Isolation** | Unprefixed (risk of collisions) | Command wrappers | **Collision-Proof** (`andino-*` prefix across all hosts) |
| **Context Window Overhead** | High (loads entire methodology) | Variable | **Token-Optimized** (Compact frontmatter, loads on demand) |
| **Anti-Looping & Checkpoints** | Custom session state | Manual stop-conditions | **Deterministic Portable Checkpoints** with Git drift detection |
| **Multi-Host CLI Installer** | Per-harness scripts | `npx skills` | **Unified Native Installer** (`ai-rules setup` with atomic rollback) |

---

## 💡 Practical Task Recipes

Combine skills naturally in your prompt for maximum leverage:

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

## 💻 Supported AI Hosts

| Host Agent | Discovery Path (Global) | Discovery Path (Project) | Command Syntax |
|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` | `/andino-workflow`, `/andino-tdd` |
| **Codex** | `~/.agents/skills/` | `.agents/skills/` | `$andino-workflow`, `$andino-tdd` |
| **OpenCode** | `~/.config/opencode/skills/` | `.agents/skills/` | `/andino-workflow`, `/andino-tdd` |
| **Antigravity CLI** | `~/.gemini/antigravity-cli/skills/` | `.agents/skills/` | Slash commands & native `skill` tool |
| **Antigravity IDE** | `~/.gemini/config/skills/` | `.agents/skills/` | Slash commands & native `skill` tool |

---

## 📜 Provenance & Licenses

- AI-RULES-authored code, installer engines, and documentation on `main` are licensed under the **[MIT License](LICENSE)**, copyright 2026 andinoferdi.
- Third-party methods and inspirations retain their original licenses and attributions:
  - `andino-workflow` adapts techniques from [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills), [Matt Pocock Skills](https://github.com/mattpocock/skills), and [Superpowers](https://github.com/obra/superpowers) ([provenance records](https://github.com/andinoferdi/AI-RULES/blob/andino-workflow/references/legal/provenance.md)).
  - `focus` credits [Ayoub Ghriss's i-have-adhd](https://github.com/ayghri/i-have-adhd).
  - `search-first` credits [Affaan Mustafa's ECC Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md).
  - `council` draws inspiration from [Ole Lehmann & Andrej Karpathy's LLM Council](https://github.com/aiwithremy/claude-skills-llm-council).
  - `threejs-skills` retains upstream resource-specific MIT, CC0, and GPL notices.
