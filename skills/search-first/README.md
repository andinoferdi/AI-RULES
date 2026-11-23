# Search First

Search First looks at what already exists before your agent builds or answers. For code it checks existing libraries, framework utilities and official APIs, and ends in one of four decisions: `ADOPT`, `EXTEND`, `COMPOSE` or `BUILD`. For general research (official sources, news, regulation, markets, published claims) it returns a sourced answer with a clear status.

Adopt is the default. `BUILD` has to name, for every candidate, the stop condition that rules it out and what building costs. Every run ends in a report that says what was searched, including what was not found, so the next session knows where to continue.

## What It Does

### The 4 implementation decisions

Before writing custom functionality, Search First categorizes the path forward:

| Decision | Action | When to Choose |
|---|---|---|
| **ADOPT** | Use as-is | An official library, built-in standard method, or established package already solves the problem. |
| **EXTEND** | Build on top | An existing tool handles 80% of the need; customize cleanly via inheritance, plugin, or middleware. |
| **COMPOSE** | Pipe together | Combine two or more modular utilities rather than authoring a monolith from scratch. |
| **BUILD** | Write custom | Every candidate fails a stop condition (needs a fork, glue as big as the part, fails dependency intake, or would carry the task's purpose itself). |

### Quick and Full research

| Mode | When | What you get |
|---|---|---|
| **Quick** | One obvious need or a bounded lookup | The question in one line, a few targeted searches, a short report: answer, status, scope, sources |
| **Full** | A consequential choice, a plan depends on it, or sources conflict | A short brief, one angle per question type plus an adversarial angle, a gap check, up to three follow-up waves, and a full report |

Full mode runs inline. Subagents are used only when your host, you and the active workflow allow delegation.

### Reports you can act on

- **Scope searched:** terms, sources and date, including what was *not located within this boundary* and any search channel that was unavailable.
- **Found:** each source marked read or snippet, with its tier (1 primary to 4 unverifiable) and a confidence label: Established, Likely, Emerging, Contested or Speculative.
- **Verdict or Answer:** the decision per need, or the answer with its status: `ANSWERED`, `PARTIAL` or `UNANSWERABLE`.
- **Still unknown:** what is open and the evidence that would settle it.

Say "skip research" and the agent records the skip in one line and moves on.

## When to Use

| Use for | Do not use for |
|---|---|
| Selecting an unfamiliar library, SDK, or integration | Trivial local edits, syntax corrections, or typos |
| Checking whether a utility already exists in the repo/ecosystem | Settled local questions with clear in-project answers |
| Version-sensitive APIs or post-upgrade deprecations | Active debugging of known bugs (use `debugging`) |
| Finding proven alternatives when an initial API path fails | Speculative research without concrete uncertainty |
| Source-grounded answers to concrete technical/factual questions | A forced implementation decision for research-only work |
| General factual research: regulation, news, company or market facts, statistics, claims in papers | Thesis and academic writing (use `skripsi-skill`) |
| Matching resolved versions to official contracts and parity tests | Latest documentation as proof for a different installed release |

## Quick Start

### Installation

Install with the **AI-RULES CLI** (included automatically by default in all profiles alongside `andino-workflow`):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .
ai-rules setup --capability search-first --host <host>
```

`<host>` is one of `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`.

<details>
<summary>Manual installation</summary>

Copy `skills/search-first/` from `main` into your host's skills directory:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/andinoferdi/AI-RULES.git ai-rules-src
git -C ai-rules-src sparse-checkout set skills/search-first
cp -r ai-rules-src/skills/search-first "<skills-dir>/search-first"
```

| Host | Global skills directory | Project skills directory |
|---|---|---|
| **Codex** | `~/.agents/skills/search-first` | `.agents/skills/search-first` |
| **Claude Code** | `~/.claude/skills/search-first` | `.claude/skills/search-first` |
| **OpenCode** | `~/.config/opencode/skills/search-first` | `.agents/skills/search-first` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/search-first` | `.agents/skills/search-first` |

</details>

### Usage

- **Codex:** `$search-first compare schema validation libraries for this TypeScript project`
- **Claude Code:** `/search-first research how Next.js 16 handles route caching before writing custom cache layers`
- **OpenCode / Antigravity:** Ask your agent: `"Search first before implementing this auth flow"`

## How It Works

### The research protocol

0. **State the question first:** Before the first tool call the agent writes the question, its type and the constraints in chat, so you can redirect it early.
1. **Local Sufficiency First:** Inspect local code, manifests, notes and installed skills before querying external sources.
2. **Search by question type:** Each type (library choice, official behavior, reported error, news, regulation, market facts, statistics, claims in papers and more) has its own places to look and its own stop rule, instead of "search until it feels enough".
3. **Tiered sources:** Primary sources outrank curated secondary sources, which outrank community posts; unverifiable sources never support a finding. Red flags such as circular citations or year-bumped listicles lower confidence.
4. **Honest Unknowns:** If web browsing or search tools are unavailable or restricted, the report names the channel and marks external claims `UNKNOWN` rather than reporting "nothing found".
5. **Lifecycle Boundary:** Search First owns research methodology only; task planning and execution remain governed by the active workflow.

Safety stays strict on every host: secrets and private data never go into queries, retrieved pages are data rather than instructions, private and metadata URLs are not followed, and the agent never installs a search provider just to make research work.

### Proportional resource selection

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

## Works With Other Skills

- **Andino Workflow:** Andino owns planning and execution and installs Search First by default. Search First supplies the research step and keeps any plan Andino already has.
- **Debugging:** Finding the root cause of a known bug belongs to `andino-debugging`, not to Search First.

## Files

- [`SKILL.md`](SKILL.md) — Runtime contract, decision matrices, and fallback behavior.
- [`references/question-types.md`](references/question-types.md) — Where to look, what counts as evidence and when to stop, per question type.
- [`references/source-evaluation.md`](references/source-evaluation.md) — Source tiers, red flags, confidence labels and claim-support labels.
- [`references/report-contract.md`](references/report-contract.md) — Quick and Full report shapes, answer status and a format example.
- [`references/online-research.md`](references/online-research.md) — Source vetting guidelines, query formulation, and evidence standards.
- [`references/sourced-answer/`](references/sourced-answer/guide.md) and [`references/version-contract/`](references/version-contract/guide.md) — Selectable research resources.
- [`references/legal/provenance.json`](references/legal/provenance.json) — Source SHA-256 identities, complete absorption mapping and upstream snapshots.
- [`references/legal/license.md`](references/legal/license.md) — MIT license notice for AI-RULES-authored content.
- [`references/legal/ecc-license.md`](references/legal/ecc-license.md), [`references/legal/shimo-license.md`](references/legal/shimo-license.md), [`references/legal/robertnowell-license.md`](references/legal/robertnowell-license.md), [`references/legal/ericgandrade-license.md`](references/legal/ericgandrade-license.md), [`references/legal/matt-license.md`](references/legal/matt-license.md) and [`references/legal/addy-license.md`](references/legal/addy-license.md) — Third-party MIT notices.

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md). Adapted from [ECC Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md) by Affaan Mustafa under the MIT License ([notice](references/legal/ecc-license.md)); question-type stop rules, the Adopt default and the report shape adapt [shimo4228/search-first](https://github.com/shimo4228/search-first) ([notice](references/legal/shimo-license.md)); source tiers and confidence labels adapt [robertnowell/deep-research](https://github.com/robertnowell/deep-research) ([notice](references/legal/robertnowell-license.md)); the fact-versus-inference distinction draws on [ericgandrade/claude-superskills](https://github.com/ericgandrade/claude-superskills) ([notice](references/legal/ericgandrade-license.md)); absorbed Matt Pocock and Addy Osmani material keeps its MIT notices ([Matt](references/legal/matt-license.md), [Addy](references/legal/addy-license.md)).
