# Natural Writing

Natural Writing writes, rewrites, and reviews Indonesian and English documents for clarity and natural flow, while preserving exact technical terms, citations, numbers, and conceptual depth.

Formulaic prose can overuse dramatic reveals ("It's not just X, it's Y"), repetitive tripartite lists, bloated adjectives, and artificial transitions. **Natural Writing** addresses these patterns in essays, technical articles, and academic papers through three modes, with edits guided by the document's audience and register.

## What It Does

### The 3 operational modes

| Mode | Purpose | Preservation Rules |
|---|---|---|
| **Write** | Generates fresh prose from supplied notes or outline | Adheres to genre depth, natural vocabulary, and evidence limits. |
| **Rewrite** | Polishes existing text for clarity and natural flow | **Meaning-preserving:** preserve all numbers, citations, and terminology. |
| **Review** | Evaluates prose quality without changing the file | Delivers prioritized critique on repetition, tone drift, and formulaic phrasing. |

Rewrite works at three levels, and an unclear request gets the narrowest one:

| Level | Changes | Keeps |
|---|---|---|
| **Proofread** | Spelling, punctuation, standard word forms, capitals, number notation | Sentence structure and order |
| **Edit** | The above plus sentence structure, connectives, redundancy, formulaic patterns | Claims, argument order, technical terms |
| **Rewrite** | The above plus paragraph structure and the order of ideas | Facts, numbers, citations |

Every result comes as the finished text first, then a short change note: what changed, claims flagged for the author, gaps marked with `[PERLU DATA: …]` / `[data needed: …]` or `[PERLU RUJUKAN: …]` / `[citation needed: …]`, and instructions found inside your text (they are treated as content, never followed). Proofread adds a before → after list.

## When to Use

| Use for | Do not use for |
|---|---|
| Technical articles, essays, and documentation prose | Conversational chat replies (use `focus`) |
| Academic sections, literature reviews, thesis chapters | Code, JSON, or machine-readable outputs |
| Polishing rough drafts without altering their meaning | Bypassing AI detectors (no gimmicky bypass promises) |
| Reviewing tone, cadence, and register inconsistencies | Task planning or lifecycle management |

## Quick Start

### Installation

Install with the **AI-RULES CLI** (included in the `research-skripsi` and `everything` profiles):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .
ai-rules setup --capability natural-writing --host <host>
```

`<host>` is one of `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`.

<details>
<summary>Manual installation</summary>

Copy `skills/natural-writing/` from `main` into your host's skills directory:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/andinoferdi/AI-RULES.git ai-rules-src
git -C ai-rules-src sparse-checkout set skills/natural-writing
cp -r ai-rules-src/skills/natural-writing "<skills-dir>/natural-writing"
```

| Host | Global skills directory | Project skills directory |
|---|---|---|
| **Codex** | `~/.agents/skills/natural-writing` | `.agents/skills/natural-writing` |
| **Claude Code** | `~/.claude/skills/natural-writing` | `.claude/skills/natural-writing` |
| **OpenCode** | `~/.config/opencode/skills/natural-writing` | `.agents/skills/natural-writing` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/natural-writing` | `.agents/skills/natural-writing` |

</details>

### Usage

- **Rewrite (English):**
  `/natural-writing rewrite this technical architecture document for flow and conciseness; preserve API names, benchmarks, and citations`
- **Review (Indonesian):**
  `/natural-writing review artikel ini untuk mendeteksi repetisi, gaya bahasa kaku, dan pola formulaik khas AI; jangan ubah filenya`
- **Write (Academic with Companion Skills):**
  `Use andino-workflow, skripsi-skill, and natural-writing to draft Chapter 2 from the verified literature notes in formal Indonesian academic prose`

## How It Works

### Protected content contract

In **Rewrite** mode, Natural Writing requires meaning-preserving edits:
1. **Facts & Numbers:** Statistical values, sample sizes, and timestamps remain untouched.
2. **Citations & References:** APA/IEEE keys, quotes, and author names are preserved verbatim.
3. **Domain Vocabulary:** Exact framework names, method signatures, and technical terms are never substituted for generic synonyms.

### Bundled checker

The skill ships a standard-library Python checker. `compare` lists numbers, citations, code, URLs and quotations that went missing or were added, and flags shifts in hedging or causal wording. `scan` lists pattern hints with line numbers. Both are bounded checks: a PASS does not prove the meaning is unchanged.

```sh
python scripts/check.py compare original.md result.md --mode rewrite
python scripts/check.py scan result.md --lang id
```

### Plain technical English

For English runbooks, procedures, error messages and UI text, an opt-in plain technical register applies ASD-STE100-inspired rules (condition before command, one instruction per sentence, one term per meaning) and keeps every hedge. It does not claim STE compliance.

## Works With Other Skills

- **Focus:** Focus owns chat replies and progress updates; Natural Writing owns requested writing artifacts.
- **Skripsi Skill:** Skripsi Skill owns research validity and thesis structure; Natural Writing owns the prose.
- **Andino Workflow:** Andino owns the task lifecycle; Natural Writing only shapes the text it is asked to write or review.

## Files

- [`SKILL.md`](SKILL.md) — Mode selection, protected content rules, and verification checklist.
- [`references/indonesian-writing.md`](references/indonesian-writing.md) — Natural Indonesian patterns and vocabulary guide.
- [`references/english-writing.md`](references/english-writing.md) — Natural English patterns and guidance on formulaic phrasing.
- [`references/academic-writing.md`](references/academic-writing.md) — Claim strength, citation rigor, and academic registers.
- [`references/editing-and-review.md`](references/editing-and-review.md) — Structured editorial procedures.
- [`references/indonesian-mechanics.md`](references/indonesian-mechanics.md) — EYD V mechanics, kata baku, numbers, abbreviations, loanwords and what not to correct.
- [`references/plain-technical-english.md`](references/plain-technical-english.md) — Opt-in plain technical English register.
- [`scripts/check.py`](scripts/check.py) — `compare` and `scan` checks.
- [`references/legal/license.md`](references/legal/license.md) — MIT license notice.

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md). Ideas (not text) were informed by humanizer-id, naskah-id, bahasa-skills, bahasa-indonesia-skill, asd-ste100-skill and SimpleEnglish.
