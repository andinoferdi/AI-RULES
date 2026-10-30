# Natural Writing

Natural Writing writes, rewrites, and reviews Indonesian and English documents for clarity and natural flow, while preserving exact technical terms, citations, numbers, and conceptual depth.

Formulaic prose can overuse dramatic reveals ("It's not just X, it's Y"), repetitive tripartite lists, bloated adjectives, and artificial transitions. **Natural Writing** addresses these patterns in essays, technical articles, and academic papers through three modes, with edits guided by the document's audience and register.

---

## The 3 Operational Modes

| Mode | Purpose | Preservation Rules |
|---|---|---|
| **Write** | Generates fresh prose from supplied notes or outline | Adheres to genre depth, natural vocabulary, and evidence limits. |
| **Rewrite** | Polishes existing text for clarity and natural flow | **Meaning-preserving:** preserve all numbers, citations, and terminology. |
| **Review** | Evaluates prose quality without changing the file | Delivers prioritized critique on repetition, tone drift, and formulaic phrasing. |

---

## When to Use

| Use For | Do NOT Use For |
|---|---|
| Technical articles, essays, and documentation prose | Conversational chat replies (use `focus`) |
| Academic sections, literature reviews, thesis chapters | Code, JSON, or machine-readable outputs |
| Polishing rough drafts without altering their meaning | Bypassing AI detectors (no gimmicky bypass promises) |
| Reviewing tone, cadence, and register inconsistencies | Task planning or lifecycle management |

---

## Quick Start

### 1. Installation

Install via the **AI-RULES CLI** (included in the `research-skripsi` and `everything` profiles):

```sh
# Install CLI
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Setup Natural Writing for your host
ai-rules setup --capability natural-writing --host <host>
```

<details>
<summary>Manual Installation</summary>

```sh
git clone --depth 1 --single-branch --branch natural-writing https://github.com/andinoferdi/AI-RULES.git "<skills-dir>/natural-writing"
```

| Host | Global Skills Directory | Project Skills Directory |
|---|---|---|
| **Codex** | `~/.agents/skills/natural-writing` | `.agents/skills/natural-writing` |
| **Claude Code** | `~/.claude/skills/natural-writing` | `.claude/skills/natural-writing` |
| **OpenCode** | `~/.config/opencode/skills/natural-writing` | `.agents/skills/natural-writing` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/natural-writing` | `.agents/skills/natural-writing` |

</details>

### 2. Usage Examples

- **Rewrite (English):**
  `/natural-writing rewrite this technical architecture document for flow and conciseness; preserve API names, benchmarks, and citations`
- **Review (Indonesian):**
  `/natural-writing review artikel ini untuk mendeteksi repetisi, gaya bahasa kaku, dan pola formulaik khas AI; jangan ubah filenya`
- **Write (Academic with Companion Skills):**
  `Use andino-workflow, skripsi-skill, and natural-writing to draft Chapter 2 from the verified literature notes in formal Indonesian academic prose`

---

## Protected Content Contract

In **Rewrite** mode, Natural Writing requires meaning-preserving edits:
1. **Facts & Numbers:** Statistical values, sample sizes, and timestamps remain untouched.
2. **Citations & References:** APA/IEEE keys, quotes, and author names are preserved verbatim.
3. **Domain Vocabulary:** Exact framework names, method signatures, and technical terms are never substituted for generic synonyms.

---

## References & Provenance

- [`SKILL.md`](SKILL.md) — Mode selection, protected content rules, and verification checklist.
- [`references/indonesian-writing.md`](references/indonesian-writing.md) — Natural Indonesian patterns and vocabulary guide.
- [`references/english-writing.md`](references/english-writing.md) — Natural English patterns and guidance on formulaic phrasing.
- [`references/academic-writing.md`](references/academic-writing.md) — Claim strength, citation rigor, and academic registers.
- [`references/editing-and-review.md`](references/editing-and-review.md) — Structured editorial procedures.
- Created by Andino Ferdiansah under the [MIT License](references/license.md).
