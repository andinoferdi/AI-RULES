# AI Codebase Rescue

> **Evidence-first codebase stabilization.** Rescue fragile, patch-heavy subsystems with proven regression protection and disciplined engineering dispositions: `KEEP`, `REFACTOR`, `REMAKE`, `REMOVE`, or `INVESTIGATE`.

AI-generated code and rapid patching accelerate software entropy. When a subsystem breaks repeatedly, agents often guess or attempt blind rewrites that discard working edge-case behaviors. **AI Codebase Rescue** enforces an engineering-grade triage loop: establish baseline behavior $\rightarrow$ isolate regression tests $\rightarrow$ audit contract drift $\rightarrow$ apply targeted remediation.

---

## The 5 Dispositions

Every inspected component receives an explicit, evidence-backed disposition:

| Disposition | Meaning | Criteria |
|---|---|---|
| **KEEP** | Leave untouched | Stable, working, verified by tests; cosmetic ugliness does not justify edits. |
| **REFACTOR** | Improve structure | Preserves exact public contracts and behaviors; clears tangled complexity. |
| **REMAKE** | Clean reimplementation | Architectural dead-end; verified against strict regression test harnesses. |
| **REMOVE** | Dead code elimination | Unused endpoints, zombie abstractions, or redundant helper drift. |
| **INVESTIGATE** | Gather missing telemetry | Root cause or boundary behavior cannot yet be verified with available evidence. |

---

## When to Use

| ✅ Use For | ❌ Do NOT Use For |
|---|---|
| Repeated regressions in the same module | Routine single-file bug fixes (use debugging) |
| Fragile prototypes being hardened for production | Cosmetic cleanup, linting, or formatting |
| Material contract, ownership, or boundary drift | Greenfield feature implementation |
| Legacy technical-debt recovery with active consumers | Rewrites justified merely because "AI wrote it" |

---

## Quick Start

### 1. Installation

Install via the **AI-RULES CLI** (included in the `engineering` and `everything` profiles):

```sh
# Install CLI
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Setup for your agent (codex, claude-code, opencode, antigravity-cli, antigravity-ide)
ai-rules setup --capability ai-codebase-rescue --host <host>
```

<details>
<summary>Manual Installation</summary>

Clone directly into your harness's global skills directory:

```sh
git clone --depth 1 --single-branch --branch ai-codebase-rescue https://github.com/andinoferdi/AI-RULES.git "<skills-dir>/ai-codebase-rescue"
```

| Host | Global Skills Directory | Project Skills Directory |
|---|---|---|
| **Codex** | `~/.agents/skills/ai-codebase-rescue` | `.agents/skills/ai-codebase-rescue` |
| **Claude Code** | `~/.claude/skills/ai-codebase-rescue` | `.claude/skills/ai-codebase-rescue` |
| **OpenCode** | `~/.config/opencode/skills/ai-codebase-rescue` | `.agents/skills/ai-codebase-rescue` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/ai-codebase-rescue` | `.agents/skills/ai-codebase-rescue` |

</details>

### 2. Usage

Invoke directly in your coding agent:

- **Claude Code:** `/ai-codebase-rescue investigate repeated payment timeout regressions in the checkout module`
- **Codex:** `$ai-codebase-rescue audit authentication session drift and protect token refresh`
- **OpenCode / Antigravity:** Ask the agent to use `ai-codebase-rescue` or invoke via native skill tool.

---

## Integration with Andino Workflow

AI Codebase Rescue works standalone or seamlessly alongside **Andino Workflow**:
- **With Andino Workflow:** Andino owns the overarching lifecycle, execution plan, and durable checkpoints. When a bounded codebase recovery need is identified, Andino delegates to `ai-codebase-rescue` for stabilization without spawning conflicting plans.
- **Standalone:** Operates within the host's active session, creating bounded evidence and regression test suites.

---

## References & Verification

- [`SKILL.md`](SKILL.md) — Runtime contract and activation rules.
- [`references/audit-taxonomy.md`](references/audit-taxonomy.md) — Defect classification and disposition criteria.
- [`references/regression-and-verification.md`](references/regression-and-verification.md) — Baseline capture and test verification protocols.
- [`references/validation-scenarios.md`](references/validation-scenarios.md) — Representative triage scenarios.
