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

## Verdict Output Format

Council returns a decision artifact:
- **Titik Temu / Agreement:** Where the advisors independently converged.
- **Perbedaan / Disagreement:** Disputed assumptions and real trade-offs.
- **Hal Terlewat / Blind Spots:** Risks uncovered during anonymous peer review.
- **Rekomendasi / Recommendation:** Justified decision and residual uncertainty.
- **Langkah Pertama / First Action:** Exactly one practical, immediate next move.

---

## References

- [`SKILL.md`](SKILL.md) — Runtime contract, advisor prompts, and host fidelity constraints.
- [AI-RULES Main](https://github.com/andinoferdi/AI-RULES/tree/main) — Validator suite, release manifest, and test harnesses.
