# AI-RULES

Install Andino's skills for Codex, Claude Code, OpenCode, and Antigravity. Start with one Andino Workflow invocation; it selects relevant supporting skills and tools within the host's permissions.

## Distribution branches

| Branch | Purpose |
| --- | --- |
| [`main`](https://github.com/andinoferdi/AI-RULES/tree/main) | Installer source, tests, release tooling, and validation evidence |
| [`WebBased`](https://github.com/andinoferdi/AI-RULES/tree/WebBased) | Web/chat rules and project templates |
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
| Minimal | Andino Workflow |
| Engineering | Andino Workflow + AI Codebase Rescue |
| Research / Skripsi | Andino Workflow + Skripsi Skill |
| Everything | All three |

Open a new agent session or reload its window after setup. Installing all three skills does **not** activate all of them for every task. Third-party skills, plugins, and MCP servers require their own installation or connection.

Run `ai-rules setup` again to update selected skills from their latest configured branches. To update the CLI itself, run these commands from a clean `main` checkout:

```sh
git pull --ff-only
python -m pip install .
ai-rules setup
```

Setup verifies files and entry points, not successful skill use in a running agent. Review any reported conflict or unsupported installation layout before replacing files. See the [validation guide](evals/README.md) for testing details.

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
