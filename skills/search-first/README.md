# Search First

Search First evaluates existing libraries, framework utilities, and official APIs before custom code, leading to one of four implementation decisions: `ADOPT`, `EXTEND`, `COMPOSE`, or `BUILD`.

Before writing custom utilities, check whether standard libraries or maintained packages already meet the need. **Search First** uses a research gate for non-trivial implementation decisions, checking approaches against authoritative documentation and current API contracts.

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

| Run Search First For | Do NOT Run Search First For |
|---|---|
| Selecting an unfamiliar library, SDK, or integration | Trivial local edits, syntax corrections, or typos |
| Checking whether a utility already exists in the repo/ecosystem | Settled local questions with clear in-project answers |
| Version-sensitive APIs or post-upgrade deprecations | Active debugging of known bugs (use `debugging`) |
| Finding proven alternatives when an initial API path fails | Speculative research without concrete uncertainty |
| Source-grounded answers to concrete technical/factual questions | A forced implementation decision for research-only work |
| Matching resolved versions to official contracts and parity tests | Latest documentation as proof for a different installed release |

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
4. **Lifecycle Boundary:** Search First owns research methodology only; task planning and execution remain governed by the active workflow.

---

## Proportional Resource Selection

Select the resource for the actual unresolved need, not a mandatory full lifecycle:

- **Sourced answer:** Read the [contract](references/sourced-answer/contract.md)
  and [full guide](references/sourced-answer/guide.md) for a concrete question,
  primary-source findings, near-claim citations, contradictions and explicit gaps.
  Its [worked example](references/sourced-answer/resources/worked-example.md)
  checks a bounded findings artifact; it is not live research proof.
- **Version-sensitive implementation:** Read the
  [contract](references/version-contract/contract.md) and
  [full guide](references/version-contract/guide.md). Preserve the chain
  **manifest constraint + resolved lockfile/environment version → matching primary
  source with deep URL/version/section → change → parity test**. Record actual
  source-to-test evidence; a fixture cannot prove application integration.
- **Cache/revalidation:** Read [documentation freshness](references/version-contract/resources/documentation-freshness.md)
  when relevant. Reuse requires an actual matching-validator 304 for the same
  representation and purpose. Cached content remains untrusted; missing validators,
  failed retrieval or a different prompt do not establish current proof.
- **Online work:** The existing [online preflight](references/online-research.md)
  still governs real search/reading, sanitized queries, permission boundaries,
  source vetting, bounded retries and truthful unavailable/denied/insufficient states.

These are nonnative resources, not aliases or separately installed skills. A
bounded sourced answer need not compare packages, choose ADOPT/EXTEND/COMPOSE/BUILD,
edit code or activate Andino. Use the current task's evidence convention; with
Andino already active, keep its existing plan. Resolve any separate workflow-owned
method from the actual installed workflow root selected by the host, never through
a sibling-relative link. No parent installation or full workflow activation is
required just to use these resources.

## References & Provenance

- [`SKILL.md`](SKILL.md) — Runtime contract, decision matrices, and fallback behavior.
- [`references/online-research.md`](references/online-research.md) — Source vetting guidelines, query formulation, and evidence standards.
- [`references/consolidation-provenance.json`](references/consolidation-provenance.json) — Source SHA-256 identities, complete absorption mapping and upstream snapshots; accompanying [Matt Pocock](references/matt-license.md) and [Addy Osmani](references/addy-license.md) MIT notices.
- Adapted from [ECC Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md) by Affaan Mustafa under the MIT License ([license notice](references/license.md)).
