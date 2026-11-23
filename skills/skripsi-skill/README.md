# Skripsi Skill

Skripsi Skill helps undergraduate and graduate researchers write and defend a thesis
(*skripsi*, *tesis*, *disertasi*), from topic to sidang and on to a journal article, with
thesis-ready drafts and no invented evidence.

A thesis needs grounded literature synthesis, defensible methods, honest analysis and
revisions that answer the supervisor. **Skripsi Skill** delivers the requested chapter or
review first, written as connected academic prose at the requested depth, built only from
the evidence you supply or that was verified. Where evidence is missing it keeps the
sentence and marks the gap (`[PERLU RUJUKAN: …]`, `[PERLU DATA: …]`) instead of inventing
sources, numbers or approvals. Your campus guide always outranks its defaults.

## What It Does

### Six working modes

| Mode | What you get |
| --- | --- |
| Draft (default) | BAB I–V sections, abstracts or article parts in thesis prose, with placeholders for missing evidence and a short note on what to fill |
| Review and revise | Prioritized review with severity and location, supervisor/examiner simulation, a revision tracker (lembar revisi) and tracked revisions |
| Verify | A per-reference check: two-way citation match, existence by DOI or search, claim support, and a clear verdict for each entry |
| Guided | Questions that help you write the chapter yourself, for learning or when campus rules forbid AI-written chapters |
| Defense | Sempro and sidang preparation from your actual thesis: high-risk questions, answer cards and mock rounds |
| Plan and state | Direction, feasibility, problem and research questions, design, sampling, measurement and analysis plans |

### Thesis research stages

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

The skill enters at your current stage and keeps approved decisions; it never restarts
settled work. After the thesis, it helps turn it into a journal article.

## When to Use

| Use for | Do not use for |
|---|---|
| Drafting or reviewing BAB I–V, proposals and abstracts | Polishing one sentence (use `natural-writing`) |
| Literature search, reading and thematic synthesis | Unrelated software engineering or generic coding |
| Supervisor or examiner revisions, sempro and sidang preparation | Producing data, results or approvals that do not exist |
| Citation and claim checks; Indonesian campus and journal conventions | General factual research (use `search-first`) |

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

- **Draft a chapter:**
  `/skripsi-skill Judul saya sudah disetujui. Ini catatan bacaan dan pedoman kampus. Buatkan draf BAB I, latar belakang sekitar 1.000 kata.`
- **Supervisor revision:**
  `/skripsi-skill Ini catatan dosen untuk BAB II saya. Tolong bantu revisi dan buatkan lembar revisinya.`
- **Check references:**
  `/skripsi-skill Cek apakah sitasi dan daftar pustaka BAB II saya sudah cocok dan rujukannya asli.`
- **Defense preparation:**
  `/skripsi-skill Sidang saya minggu depan. Siapkan pertanyaan penguji yang paling berisiko dan cara menjawabnya.`
- **Thesis to article:**
  `/skripsi-skill Bantu ubah skripsi saya jadi artikel untuk jurnal SINTA 4.`

## How It Works

### Output contract

Every reply that produces an artifact follows the same contract (in `SKILL.md`):
artifact first; every supported part written in full; visible placeholders where evidence
is missing; thesis prose rather than bullet lists; requested length met within ±10% or the
shortfall explained; internal status labels kept out of your text; one short note at the
end with what to fill and the next step.

### Academic integrity contract

- **Missing evidence:** placeholders mark what is missing; plausible-looking references,
  data, quotes or results are never generated.
- **Traceable attribution:** every claim keeps its source and the strength its design
  supports (no causal wording for correlational evidence).
- **Campus precedence:** your department's guide (*Buku Panduan Skripsi*) and your
  supervisor's decisions outrank the skill's defaults.
- **Student ownership:** drafts are working drafts for you to verify, understand and
  revise; campus AI-use rules are followed, including switching to guided mode.

### Writing craft

Chapter contracts give each BAB its reader's question, moves in order, common mistakes
with fixes, weak-to-stronger sentence examples and a checklist. Drafting goes from an
evidence map to a paragraph blueprint to prose, and literature paragraphs must
synthesize, not summarize. A worked example shows the whole path on an illustrative topic.

## Works With Other Skills

- **Andino Workflow:** when Andino owns the project lifecycle, Skripsi Skill acts as its
  research specialist and returns the artifact, research state, evidence and limits
  without a competing plan.
- **Natural Writing:** optional companion for register and naturalness of supported text;
  Skripsi Skill keeps research validity and thesis craft.
- **Search First:** runs the lookups behind citation and claim verification when installed.
- **Focus:** shapes the conversation around the artifact, never the artifact itself.

## Files

- [`SKILL.md`](SKILL.md) — runtime contract: output contract, modes, authority, routing.
- [`references/writing-craft.md`](references/writing-craft.md) — evidence map, paragraph blueprint, length control, manuscript firewall.
- [`references/writing-bab-1-3.md`](references/writing-bab-1-3.md) and [`references/writing-bab-4-5.md`](references/writing-bab-4-5.md) — chapter contracts.
- [`references/literature-synthesis-writing.md`](references/literature-synthesis-writing.md) — synthesis versus summary, with paired examples.
- [`references/review-and-revision-craft.md`](references/review-and-revision-craft.md) — reviews, supervisor/examiner simulation, revision tracker.
- [`references/citation-verification.md`](references/citation-verification.md) — reference and claim verification procedure.
- [`references/indonesian-academic-conventions.md`](references/indonesian-academic-conventions.md) — campus guide, EYD V, citations, SINTA, AI use, ethics.
- [`references/thesis-to-article.md`](references/thesis-to-article.md) — turning a thesis into a journal article.
- [`references/research-state-and-routing.md`](references/research-state-and-routing.md) and the other method references — state, evidence, design, literature, results and defense methods.
- [`assets/worked-example-bab-ii.md`](assets/worked-example-bab-ii.md) — one complete worked example.
- [`assets/research-core-templates.md`](assets/research-core-templates.md) — optional output helpers.
- [`references/legal/license.md`](references/legal/license.md) and [`references/legal/third-party-notices.md`](references/legal/third-party-notices.md) — licenses and adapted sources.

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md).
Adapted third-party material keeps its notices in
[third-party notices](references/legal/third-party-notices.md).
