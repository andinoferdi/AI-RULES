# Skripsi Skill

Skripsi Skill guides undergraduate and graduate researchers from topic formulation through defense preparation, with evidence traceability and attention to campus requirements.

Writing a thesis (*skripsi*) requires grounded literature synthesis, defensible methodology, honest empirical analysis, and revisions that address feedback. **Skripsi Skill** provides guidance for the current research stage, requiring verified academic evidence for research claims and adherence to institutional guidelines. Its integrity rules prohibit fabricated citations and survey numbers.

## What It Does

### The 6 research stages

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 1. Proposal  │ ──▶ │2. Literature │ ──▶ │3. Methodology│
│ Title & Gaps │     │ Synthesis    │     │ Research Des.│
└──────────────┘     └──────────────┘     └──────────────┘
       │                                         │
       ▼                                         ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  6. Defense  │ ◀── │ 5. Revisions │ ◀── │ 4. Analysis  │
│ Q&A Prep     │     │ Supv. Feedback     │ Real Data    │
└──────────────┘     └──────────────┘     └──────────────┘
```

1. **Proposal & Topic Formulation:** Formulates research questions, problem statements, and novelty gaps without reopening settled approvals.
2. **Literature Review & Synthesis:** Structures thematic matrices and critical synthesis from verified papers (APA/IEEE/institutional standards).
3. **Methodology Design:** Establishes rigorous quantitative, qualitative, or engineering design artifacts and validation protocols.
4. **Data Analysis & Findings:** Interprets actual experimental data; never invents statistics, survey samples, or evaluation benchmarks.
5. **Supervisor Revision Tracking:** Resolves feedback point-by-point, documenting exact thesis modifications for supervisor review.
6. **Defense & Trial Preparation:** Prepares anticipated defense questions, slide talk tracks, and limitation rebuttals.

## When to Use

| Use for | Do not use for |
|---|---|
| Refining thesis titles, background, and research gaps | Superficial sentence rephrasing (use `natural-writing`) |
| Systematic literature reviews and citation matrices | Unrelated software engineering or generic coding |
| Structuring chapters according to campus guidelines | Fabricating synthetic research data or fake surveys |
| Preparing formal responses to supervisor review notes | Bypassing institutional ethics or thesis guidelines |

## Quick Start

### Installation

Install with the **AI-RULES CLI** (included in the `research-skripsi` and `everything` profiles):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .
ai-rules setup --capability skripsi-skill --host <host>
```

`<host>` is one of `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`.

<details>
<summary>Manual installation</summary>

Copy `skills/skripsi-skill/` from `main` into your host's skills directory:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/andinoferdi/AI-RULES.git ai-rules-src
git -C ai-rules-src sparse-checkout set skills/skripsi-skill
cp -r ai-rules-src/skills/skripsi-skill "<skills-dir>/skripsi-skill"
```

| Host | Global skills directory | Project skills directory |
|---|---|---|
| **Codex** | `~/.agents/skills/skripsi-skill` | `.agents/skills/skripsi-skill` |
| **Claude Code** | `~/.claude/skills/skripsi-skill` | `.claude/skills/skripsi-skill` |
| **OpenCode** | `~/.config/opencode/skills/skripsi-skill` | `.agents/skills/skripsi-skill` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/skripsi-skill` | `.agents/skills/skripsi-skill` |

</details>

### Usage

- **Proposal Outline:**
  `/skripsi-skill Judul saya sudah disetujui: 'Optimasi Routing Algoritma X'. Bantu susun latar belakang dan rumusan masalah Bab 1`
- **Supervisor Revision:**
  `/skripsi-skill Dosen meminta saya memperkuat perbandingan di Bab 2 dengan 5 studi terbaru 2024-2026. Ini catatan revisinya`
- **Defense Preparation:**
  `/skripsi-skill Simulasikan pertanyaan kritis penguji tentang keterbatasan metode pengujian data saya`

## How It Works

### Academic integrity contract

- **Missing Evidence:** If literature or empirical data is missing, the agent explicitly flags it as `DATA_REQUIRED` rather than generating plausible references.
- **Traceable Attribution:** Every theoretical assertion must cite verifiable authors, years, and methodological contexts.
- **Campus Precedence:** Your department's official thesis formatting guide (*Buku Panduan Skripsi*) strictly outranks default formatting.

## Works With Other Skills

- **Andino Workflow:** When Andino owns the project lifecycle, Skripsi Skill acts as its research specialist and returns research state, evidence, limits and the next research action without a competing plan.
- **Natural Writing:** Optional companion for the prose of supported academic text; Skripsi Skill keeps research validity.

## Files

- [`SKILL.md`](SKILL.md) — Runtime contract, stage routing, and integrity rules.
- [`references/research-state-and-routing.md`](references/research-state-and-routing.md) — Entering, resuming and changing research state.
- [`references/evidence-guidelines-integrity.md`](references/evidence-guidelines-integrity.md) — Source verification standards.
- [`references/andino-integration.md`](references/andino-integration.md) — Lifecycle integration and companion skills.
- [`assets/research-core-templates.md`](assets/research-core-templates.md) — Standard proposal and chapter structures.
- [`references/legal/license.md`](references/legal/license.md) — MIT license notice.

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md).
