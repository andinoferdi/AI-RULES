# Focus

Focus guides AI agents to answer the question first, give concrete steps, and state uncertainty while preserving evidence and necessary depth.

Conversational filler and generic disclaimers can bury the answer. **Focus** applies **Priority A (A. PRIORITAS)** to communication: answer the core question first, outline immediate steps, and match the natural register of Indonesian or English.

---

## Core Communication Rules (Priority A)

| Rule | What It Means |
|---|---|
| **Result First** | State the direct answer or solution immediately before giving reasons or background. |
| **Active & Natural Voice** | Use simple, natural sentences; avoid formulaic phrasing and corporate jargon. |
| **Length Budget** | Each request type has a word or step budget (for example, a how-to gets at most 6 one-line steps). Background, side topics and caveats are cut unless they change what the reader does. |
| **Zero Conversational Fluff** | No pleasantries ("Certainly! I'd be happy to help"), no throat-clearing preambles, no trailing caveats. |
| **Preserve Facts & Limits** | Never invent numbers, sources, or certainty; distinguish verified facts from assumptions. |
| **Actionable Next Steps** | For practical queries, provide concrete steps that can be run or tested immediately. |
| **Restated Progress** | On multi-step work every update says which step is done and which comes next, so the reader never has to remember where things stand. |
| **Small Visible Lists** | Long lists are grouped and ranked, with at most five items shown per group. Nothing is dropped when the user asks for everything. |
| **Plain Error Reports** | An error report gives the symptom, the confirmed cause or "cause unknown", and the next check, without alarm words. |
| **Shape Breaks Only for a Reason** | The shape yields only in listed cases: an explicit request for detail, a destructive action, a debug spiral, real ambiguity, or a conflict with the task or the host. |

---

## When to Use

| Use Focus For | Do NOT Use Focus For |
|---|---|
| Direct answers without conversational filler | Truncating long-form essays or reports (use `natural-writing`) |
| Clear technical steps and immediate commands | Bypassing verification or reducing investigation depth |
| Specific status updates (done, pending, blocked) | Replacing domain workflows or task execution logic |
| Adaptive bilingual responses (Indonesian & English) | Overriding explicit user requests for a formal style |
| Repairing a confusing previous explanation with missing context and a concrete example | Starting research, a curriculum or file edits from explanation repair |

---

## Quick Start

### 1. Installation

Install via the **AI-RULES CLI** (included automatically by default in all profiles through `andino-workflow`):

```sh
# Install CLI
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Setup Focus for your host
ai-rules setup --capability focus --host <host>
```

<details>
<summary>Manual Installation</summary>

```sh
git clone --depth 1 --single-branch --branch focus https://github.com/andinoferdi/AI-RULES.git "<skills-dir>/focus"
```

| Host | Global Skills Directory | Project Skills Directory |
|---|---|---|
| **Codex** | `~/.agents/skills/focus` | `.agents/skills/focus` |
| **Claude Code** | `~/.claude/skills/focus` | `.claude/skills/focus` |
| **OpenCode** | `~/.config/opencode/skills/focus` | `.agents/skills/focus` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/focus` | `.agents/skills/focus` |

</details>

### 2. Usage

Focus triggers automatically when installed alongside Andino Workflow, or you can invoke it directly:

- **Claude Code:** `/focus explain how to roll back the latest database migration`
- **Codex:** `$focus outline the steps to configure HTTPS on Caddy`
- **OpenCode / Antigravity:** Ask your agent to "use focus" or write using the focus style.
- **Deactivate:** Simply say `stop focus` or request another style.

---

## Relationship to Other Skills

- **Andino Workflow:** Focus serves as the default presentation layer for Andino; it shapes communication while Andino owns the task lifecycle and execution plan.
- **Natural Writing:** Focus controls conversational and progress communication; long-form writing artifacts (essays, academic chapters, documentation) are governed by `natural-writing`.
- **Web Chatbots:** For copy-pasting into ChatGPT Web or Claude Web, refer to the [WebBased branch](https://github.com/andinoferdi/AI-RULES/tree/WebBased).

---

## References & Provenance

- [`SKILL.md`](SKILL.md) — Activation, length budgets, cut rules, shape rules with Bad/Good examples, when to break the shape, and style precedence. On first use it reads Priority A plus the language file for the reply language; a mixed-language reply reads both.
- [`references/priority-a.md`](references/priority-a.md) — Canonical Priority A communication principles.
- [`references/human-language-indonesia.md`](references/human-language-indonesia.md) — Indonesian conversational patterns.
- [`references/human-language-english.md`](references/human-language-english.md) — English conversational patterns.
- [`references/explanation-repair.md`](references/explanation-repair.md) — Load only for a confusing prior explanation; preserves meaning without a curriculum, research, file edits or a parent lifecycle.
- [`references/consolidation-provenance.json`](references/consolidation-provenance.json) — Absorbed-source SHA-256 identities and mapping; [Matt Pocock MIT notice](references/matt-license.md).
- Adapted from [i-have-adhd](https://github.com/ayghri/i-have-adhd) by Ayoub Ghriss under the MIT License ([license notice](references/license.md)).
