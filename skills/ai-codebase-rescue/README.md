# AI Codebase Rescue

AI Codebase Rescue stabilizes fragile, patch-heavy subsystems: it finds where to start, pins current behavior before changing it, fixes one concern at a time and reports what changed with honest verification.

When a subsystem breaks repeatedly, guessing or rewriting without a baseline throws away working edge cases. **AI Codebase Rescue** works from evidence: a reproducible baseline, a test-trust verdict, ranked targets, pins that pass on the unmodified code, small verified steps and an explicit decision for every inspected area: `KEEP`, `REFACTOR`, `REMAKE`, `REMOVE` or `INVESTIGATE`.

## What It Does

### Three modes

| Mode | When | Result |
|---|---|---|
| **Assess** | Diagnosis, audit or plan requested, or no edit authority | Read-only report with findings, ranked targets and proposed steps |
| **Stabilize** | Edits authorized; areas are KEEP, REFACTOR or REMOVE | Pinned behavior, one-concern steps, report |
| **Remake** | An area passed all six remake gates | Replacement behind preserved contracts |

### The 5 Dispositions

Every inspected component receives an explicit, evidence-backed disposition:

| Disposition | Meaning | Criteria |
|---|---|---|
| **KEEP** | Leave untouched | Stable, working, verified by tests; cosmetic ugliness does not justify edits. |
| **REFACTOR** | Improve structure | Preserves exact public contracts and behaviors; clears tangled complexity. |
| **REMAKE** | Clean reimplementation | Architectural dead-end; verified against strict regression test harnesses. |
| **REMOVE** | Dead code elimination | Unused paths or dependencies, proven obsolete including config and plugin consumers. |
| **INVESTIGATE** | Gather missing evidence | Root cause or boundary behavior cannot yet be verified with available evidence. |

## When to Use

| Use for | Do not use for |
|---|---|
| Repeated regressions in the same module | Routine single-file bug fixes (use debugging) |
| Code the team is afraid to change because tests cannot be trusted | Cosmetic cleanup, linting, or formatting |
| Rushed or AI-assisted patches with duplicated logic, swallowed errors or phantom imports | Greenfield feature implementation |
| Fragile prototypes being hardened for production | Dependency bumps or ordinary reviews |
| Material contract, ownership, or boundary drift | Rewrites justified merely because "AI wrote it" |

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
- **Codex:** `$ai-codebase-rescue assess the session refresh code and propose steps, do not edit`
- **OpenCode / Antigravity:** Ask the agent to use `ai-codebase-rescue`, or invoke it through the native skill tool.

## How It Works

1. **Scope the evidence.** Git state, intended behavior, baseline run and a test-trust verdict, consumers including config and plugin registrations.
2. **Choose where to start.** Symptom, violated contract, change point and test point, ranked by churn, complexity and consumers. No health scores.
3. **Sweep for AI-typical failure signals.** Phantom imports and packages, swallowed errors and fake success, silent fallbacks, diverged duplicate rules. Signals are leads; each finding needs its own evidence.
4. **Stabilize loop.** Pin current behavior (known bugs pinned, not silently fixed), then one structure-only or behavior-only step at a time, checked after every step. A red refactor step is reverted, not debugged forward.
5. **Report.** Findings with severity, confidence and disposition, changes per concern, downstream impact including data that needs reconciliation, and PASS, FAIL or UNVERIFIED per check.

## Works With Other Skills

- **Andino Workflow:** Andino owns the lifecycle, execution plan, and durable checkpoints. When a bounded codebase recovery need is identified, Andino routes the work to `ai-codebase-rescue`, which returns its report to the existing plan.
- **Standalone:** Works in the host's task context. It creates no state file, tag or second plan in the target project.

## Files

- [`SKILL.md`](SKILL.md) — Runtime contract: modes, evidence, dispositions, Stabilize loop, report, Done when.
- [`references/triage-and-hotspots.md`](references/triage-and-hotspots.md) — Choosing the starting target.
- [`references/ai-failure-signals.md`](references/ai-failure-signals.md) — Signals common in rushed or agent-made patches and their checks.
- [`references/safety-net-techniques.md`](references/safety-net-techniques.md) — Characterization, known-bug pins, seams and dependency breaking.
- [`references/refactoring-moves.md`](references/refactoring-moves.md) — Step discipline, named moves and migration patterns.
- [`references/rescue-report.md`](references/rescue-report.md) — Report skeleton and rules.
- [`references/worked-example.md`](references/worked-example.md) — One complete run.
- [`references/evidence-and-findings.md`](references/evidence-and-findings.md), [`references/regression-and-verification.md`](references/regression-and-verification.md), [`references/bounded-remake.md`](references/bounded-remake.md), [`references/audit-taxonomy.md`](references/audit-taxonomy.md), [`references/security-and-production-hardening.md`](references/security-and-production-hardening.md), [`references/frontend-runtime-stability.md`](references/frontend-runtime-stability.md) — Evidence, verification and risk-specific references.
- [`references/validation-scenarios.md`](references/validation-scenarios.md) — Scenarios A-W for validating the skill.
- [`references/legal/license.md`](references/legal/license.md) — MIT license notice; [`references/legal/provenance.md`](references/legal/provenance.md) — adapted sources and their notices.

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md). Material adapted from Rune and Wondel.ai is used under their MIT licenses; see [provenance](references/legal/provenance.md).
