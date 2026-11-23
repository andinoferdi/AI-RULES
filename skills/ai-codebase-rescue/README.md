# AI Codebase Rescue

AI Codebase Rescue stabilizes fragile, patch-heavy subsystems through regression protection and explicit engineering decisions: `KEEP`, `REFACTOR`, `REMAKE`, `REMOVE`, or `INVESTIGATE`.

When a subsystem breaks repeatedly, guessing or rewriting without a baseline risks discarding working edge-case behaviors. **AI Codebase Rescue** uses a triage loop to investigate accumulated patches and regressions: establish baseline behavior $\rightarrow$ isolate regression tests $\rightarrow$ audit contract drift $\rightarrow$ apply targeted remediation.

## What It Does

### The 5 Dispositions

Every inspected component receives an explicit, evidence-backed disposition:

| Disposition | Meaning | Criteria |
|---|---|---|
| **KEEP** | Leave untouched | Stable, working, verified by tests; cosmetic ugliness does not justify edits. |
| **REFACTOR** | Improve structure | Preserves exact public contracts and behaviors; clears tangled complexity. |
| **REMAKE** | Clean reimplementation | Architectural dead-end; verified against strict regression test harnesses. |
| **REMOVE** | Dead code elimination | Unused endpoints, zombie abstractions, or redundant helper drift. |
| **INVESTIGATE** | Gather missing telemetry | Root cause or boundary behavior cannot yet be verified with available evidence. |

## When to Use

| Use for | Do not use for |
|---|---|
| Repeated regressions in the same module | Routine single-file bug fixes (use debugging) |
| Fragile prototypes being hardened for production | Cosmetic cleanup, linting, or formatting |
| Material contract, ownership, or boundary drift | Greenfield feature implementation |
| Legacy technical-debt recovery with active consumers | Rewrites justified merely because "AI wrote it" |

## Quick Start

### Installation

Install with the **AI-RULES CLI** (included in the `engineering` and `everything` profiles):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .
ai-rules setup --capability ai-codebase-rescue --host <host>
```

`<host>` is one of `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`.

<details>
<summary>Manual installation</summary>

Copy `skills/ai-codebase-rescue/` from `main` into your host's skills directory:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/andinoferdi/AI-RULES.git ai-rules-src
git -C ai-rules-src sparse-checkout set skills/ai-codebase-rescue
cp -r ai-rules-src/skills/ai-codebase-rescue "<skills-dir>/ai-codebase-rescue"
```

| Host | Global skills directory | Project skills directory |
|---|---|---|
| **Codex** | `~/.agents/skills/ai-codebase-rescue` | `.agents/skills/ai-codebase-rescue` |
| **Claude Code** | `~/.claude/skills/ai-codebase-rescue` | `.claude/skills/ai-codebase-rescue` |
| **OpenCode** | `~/.config/opencode/skills/ai-codebase-rescue` | `.agents/skills/ai-codebase-rescue` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/ai-codebase-rescue` | `.agents/skills/ai-codebase-rescue` |

</details>

### Usage

- **Claude Code:** `/ai-codebase-rescue investigate repeated payment timeout regressions in the checkout module`
- **Codex:** `$ai-codebase-rescue audit authentication session drift and protect token refresh`
- **OpenCode / Antigravity:** Ask the agent to use `ai-codebase-rescue`, or invoke it through the native skill tool.

## Works With Other Skills

- **Andino Workflow:** Andino owns the lifecycle, execution plan, and durable checkpoints. When a bounded codebase recovery need is identified, Andino delegates to `ai-codebase-rescue` for stabilization within the existing plan.
- **Standalone:** Operates within the host's active session, creating bounded evidence and regression test suites.

## Files

- [`SKILL.md`](SKILL.md) — Runtime contract and activation rules.
- [`references/audit-taxonomy.md`](references/audit-taxonomy.md) — Defect classification and disposition criteria.
- [`references/regression-and-verification.md`](references/regression-and-verification.md) — Baseline capture and test verification protocols.
- [`references/validation-scenarios.md`](references/validation-scenarios.md) — Representative triage scenarios.
- [`references/legal/license.md`](references/legal/license.md) — MIT license notice.

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md).
