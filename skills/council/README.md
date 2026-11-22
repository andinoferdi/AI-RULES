# Council

Council reviews consequential choices through five perspectives, anonymized peer critique, and a synthesized recommendation with exactly one actionable next step.

For architectural forks, technology migrations, or strategic trade-offs, **Council** uses independent advisors to examine assumptions and challenge the initial framing. Inspired by Andrej Karpathy and Ole Lehmann's multi-perspective deliberation model, it reviews the choice before you commit.

---

## The 5 Deliberation Lenses

```
   ┌─────────────────────────────────────────────────────────────┐
   │                    DECISION BRIEF                           │
   └────────┬───────────┬───────────┬────────────┬───────────────┘
            ▼           ▼           ▼            ▼               ▼
       Contrarian  FirstPrinc.  Expansionist  Outsider        Executor
       [Downsides] [Root Assump] [Upside/Scale] [Blind Spots]  [Feasibility]
            └───────────┴───────────┼────────────┴───────────────┘
                                    ▼
                        ANONYMOUS PEER CRITIQUE
                                    ▼
                         ACTIONABLE VERDICT & NEXT STEP
```

1. **Contrarian** — Uncovers failure modes, hidden costs, second-order risks, and disconfirming evidence.
2. **First Principles** — Strips away false assumptions and challenges whether the right question is being asked.
3. **Expansionist** — Identifies realistic upside, compound benefits, and scalable opportunities.
4. **Outsider** — Spots comprehension gaps, stakeholder friction, and assumptions insiders take for granted.
5. **Executor** — Evaluates implementation constraints, reversibility, dependency risks, and concrete steps.

---

## When to Use

| Convene Council For | Do NOT Convene For |
|---|---|
| Irreversible architectural forks (e.g., monolith vs. microservices) | Simple factual questions or lookups |
| Technology stack / library selection with material trade-offs | Minor code formatting or cosmetic preferences |
| Subsystem replacement vs. refactoring decisions | Routine bug fixes or everyday drafting |
| Critical thesis/research methodological choices | Tasks already settled with clear requirements |

---

## Quick Start

### 1. Installation

Install via the **AI-RULES CLI** (included in the `everything` profile and custom setup; automatically installs companion `focus`):

```sh
# Install CLI
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Setup Council for your host
ai-rules setup --capability council --host <host>
```

<details>
<summary>Manual Installation</summary>

```sh
git clone --depth 1 --single-branch --branch council https://github.com/andinoferdi/AI-RULES.git "<skills-dir>/council"
```

| Host | Global Skills Directory | Project Skills Directory |
|---|---|---|
| **Codex** | `~/.agents/skills/council` | `.agents/skills/council` |
| **Claude Code** | `~/.claude/skills/council` | `.claude/skills/council` |
| **OpenCode** | `~/.config/opencode/skills/council` | `.agents/skills/council` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/council` | `.agents/skills/council` |

</details>

### 2. Usage

- **Claude Code:** `/council Should we rebuild the billing pipeline in Go or optimize the existing Node service?`
- **Codex:** `$council evaluate trade-offs between PostgreSQL partitioning and sharding for our telemetry data`
- **OpenCode / Antigravity:** Ask your agent to "Council this decision" or run a war room review.

---

## How a Run Works

1. **Context and brief.** Council reads what you named plus the project's instruction files when they matter, then writes one neutral brief with every material fact tagged `[verified]`, `[reported]`, `[assumption]` or `[unknown]`.
2. **Advisors.** Five advisors get the same brief and the same written template. Each argues its lens at full strength, without seeing the others.
3. **Peer review.** Three reviewers see the five answers as Responses A-E. Each names the strongest answer, challenges the weakest claim, says what everyone missed, and ends with a `FINAL RANKING` line.
4. **Chair.** The main agent reveals who wrote what, treats the ranking as a signal rather than proof, checks the decisive claims against their tags, and writes the verdict.

### Run budget

A default run uses 8 sub-agents in three waves of at most 3: three advisors, two advisors, then three reviewers. Advisors use a mid-tier model at medium effort and reviewers a mid or low tier at low effort. Council announces the count, models and effort before dispatching and waits for approval when your rules require it. Five reviewers run only on request. Hosts without sub-agents get a labeled **single-agent perspective review** built from the same templates.

---

## Verdict Output Format

Council answers in chat with one fixed layout:

| English | Bahasa Indonesia | Content |
|---|---|---|
| Recommendation | Rekomendasi | The choice and why it beats the strongest alternative. |
| Where the council agrees | Titik temu | Points the advisors reached independently. |
| Where the council clashes | Perbedaan | Real disagreements and the assumptions behind them. |
| Blind spots from review | Hal terlewat | Risks that surfaced only in peer review. |
| What would change the verdict | Yang bisa mengubah verdict | The observation that would flip the choice. |
| First action | Langkah pertama | Exactly one concrete next step. |
| Run line | Jalannya council | Agents, models and effort actually used, and the context read. |

---

## References

- [`SKILL.md`](SKILL.md) — Runtime contract, run budget, and host fidelity limits.
- [`references/prompts.md`](references/prompts.md) — Advisor, reviewer, and single-agent templates plus the chair checklist.
- [`references/worked-example.md`](references/worked-example.md) — One complete illustrative run.
- [AI-RULES Main](https://github.com/andinoferdi/AI-RULES/tree/main) — Validator suite, release manifest, and test harnesses.

## License

Council is released under the [MIT license](references/license.md). It is inspired by [aiwithremy/claude-skills-llm-council](https://github.com/aiwithremy/claude-skills-llm-council) and [karpathy/llm-council](https://github.com/karpathy/llm-council); neither declares a license, so no text or code from them is included.
