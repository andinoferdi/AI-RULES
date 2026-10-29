# Skripsi Skill

> **Structured academic research and thesis guidance for AI agents.** Guides undergraduate and graduate researchers from topic formulation through defense preparation, with strict evidence traceability and campus compliance.

Writing a thesis (*skripsi*) requires systematic academic rigor: grounded literature synthesis, defensible methodology, honest empirical analysis, and responsive revisions. Generic AI assistants frequently hallucinate citations, fabricate survey numbers, or ignore institutional guidelines. **Skripsi Skill** provides a disciplined, stage-aware workflow that keeps all research claims anchored in verified academic evidence.

---

## The 6 Research Stages

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

---

## When to Use

| ✅ Use Skripsi Skill For | ❌ Do NOT Use Skripsi Skill For |
|---|---|
| Refining thesis titles, background, and research gaps | Superficial sentence rephrasing (use `focus`) |
| Systematic literature reviews and citation matrices | Unrelated software engineering or generic coding |
| Structuring chapters according to campus guidelines | Fabricating synthetic research data or fake surveys |
| Preparing formal responses to supervisor review notes | Bypassing institutional ethics or thesis guidelines |

---

## Quick Start

### 1. Installation

Install via the **AI-RULES CLI** (included in the `research-skripsi` and `everything` profiles):

```sh
# Install CLI
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Setup Skripsi Skill for your host
ai-rules setup --capability skripsi-skill --host <host>
```

<details>
<summary>Manual Installation</summary>

```sh
git clone --depth 1 --single-branch --branch skripsi-skill https://github.com/andinoferdi/AI-RULES.git "<skills-dir>/skripsi-skill"
```

| Host | Global Skills Directory | Project Skills Directory |
|---|---|---|
| **Codex** | `~/.agents/skills/skripsi-skill` | `.agents/skills/skripsi-skill` |
| **Claude Code** | `~/.claude/skills/skripsi-skill` | `.claude/skills/skripsi-skill` |
| **OpenCode** | `~/.config/opencode/skills/skripsi-skill` | `.agents/skills/skripsi-skill` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/skripsi-skill` | `.agents/skills/skripsi-skill` |

</details>

### 2. Usage Examples

- **Proposal Outline:**
  `/skripsi-skill Judul saya sudah disetujui: 'Optimasi Routing Algoritma X'. Bantu susun latar belakang dan rumusan masalah Bab 1`
- **Supervisor Revision:**
  `/skripsi-skill Dosen meminta saya memperkuat perbandingan di Bab 2 dengan 5 studi terbaru 2024-2026. Ini catatan revisinya`
- **Defense Preparation:**
  `/skripsi-skill Simulasikan pertanyaan kritis penguji tentang keterbatasan metode pengujian data saya`

---

## Academic Integrity Contract

- **Zero Hallucination:** If literature or empirical data is missing, the agent explicitly flags it as `DATA_REQUIRED` rather than generating plausible references.
- **Traceable Attribution:** Every theoretical assertion must cite verifiable authors, years, and methodological contexts.
- **Campus Precedence:** Your department's official thesis formatting guide (*Buku Panduan Skripsi*) strictly outranks default formatting.

---

## References & Assets

- [`SKILL.md`](SKILL.md) — Runtime contract, stage state machine, and integrity rules.
- [`references/evidence-guidelines-integrity.md`](references/evidence-guidelines-integrity.md) — Source verification standards.
- [`assets/research-core-templates.md`](assets/research-core-templates.md) — Standard proposal and chapter structures.
