# Search First

> **Research existing solutions before writing custom code.** Prevents reinventing the wheel by systematically evaluating libraries, framework utilities, and official APIs: `ADOPT`, `EXTEND`, `COMPOSE`, or `BUILD`.

AI coding agents habitually jump straight to writing hundreds of lines of custom code for utilities that already exist in standard libraries or battle-tested packages. **Search First** forces an evidence-based research gate before non-trivial implementation decisions, ensuring every approach is grounded in authoritative documentation and current API contracts.

---

## The 4 Implementation Decisions

Before writing custom functionality, Search First categorizes the path forward:

| Decision | Action | When to Choose |
|---|---|---|
| **ADOPT** | Use as-is | An official library, built-in standard method, or established package already solves the problem. |
| **EXTEND** | Build on top | An existing tool handles 80% of the need; customize cleanly via inheritance, plugin, or middleware. |
| **COMPOSE** | Pipe together | Combine two or more modular utilities rather than authoring a monolith from scratch. |
| **BUILD** | Write custom | No safe, maintained, or lightweight solution exists; write tailored, test-guarded code. |

---

## When to Use

| ✅ Run Search First For | ❌ Do NOT Run Search First For |
|---|---|
| Selecting an unfamiliar library, SDK, or integration | Trivial local edits, syntax corrections, or typos |
| Checking whether a utility already exists in the repo/ecosystem | Settled local questions with clear in-project answers |
| Version-sensitive APIs or post-upgrade deprecations | Active debugging of known bugs (use `debugging`) |
| Finding proven alternatives when an initial API path fails | Speculative research without concrete uncertainty |

---

## Quick Start

### 1. Installation

Install via the **AI-RULES CLI** (included automatically by default in all profiles alongside `andino-workflow`):

```sh
# Install CLI
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Setup Search First for your host
ai-rules setup --capability search-first --host <host>
```

<details>
<summary>Manual Installation</summary>

```sh
git clone --depth 1 --single-branch --branch search-first https://github.com/andinoferdi/AI-RULES.git "<skills-dir>/search-first"
```

| Host | Global Skills Directory | Project Skills Directory |
|---|---|---|
| **Codex** | `~/.agents/skills/search-first` | `.agents/skills/search-first` |
| **Claude Code** | `~/.claude/skills/search-first` | `.claude/skills/search-first` |
| **OpenCode** | `~/.config/opencode/skills/search-first` | `.agents/skills/search-first` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/search-first` | `.agents/skills/search-first` |

</details>

### 2. Usage Examples

- **Codex:** `$search-first compare schema validation libraries for this TypeScript project`
- **Claude Code:** `/search-first research how Next.js 16 handles route caching before writing custom cache layers`
- **OpenCode / Antigravity:** Ask your agent: `"Search first before implementing this auth flow"`

---

## The Research Protocol

1. **Local Sufficiency First:** Inspect local package manifests and existing utility directories before querying external sources.
2. **Authoritative Sources Only:** Rely on official documentation, verified release notes, and high-trust repositories over unverified blog snippets.
3. **Honest Unknowns:** If web browsing or search tools are unavailable or restricted, mark external compatibility claims as `UNKNOWN` rather than speculating.
4. **Lifecycle Harmony:** Search First owns research methodology only; task planning and execution remain governed by the active workflow.

---

## References & Provenance

- [`SKILL.md`](SKILL.md) — Runtime contract, decision matrices, and fallback behavior.
- [`references/online-research.md`](references/online-research.md) — Source vetting guidelines, query formulation, and evidence standards.
- Adapted from [ECC Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md) by Affaan Mustafa under the MIT License ([license notice](references/license.md)).
