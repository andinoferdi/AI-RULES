---
name: andino-constraint-driven-development
description: Establishes a project's quality bar as a written contract and stops agents quietly lowering it. Operates under Andino Workflow governance.
---

# Constraint-Driven Development

Internal method ID: `andino-constraint-driven-development` (alias: `constraint-driven-development`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, single durable checkpoints, and anti-loop guards. Selected skills own their full procedures, resource contracts, and verification checks. Do not re-invoke `andino-workflow` recursively.

Define what "good enough to ship" means in a written, numbered `CONSTRAINTS.md` contract and mechanically prevent coding agents from weakening it mid-task.

## Activation & Negative Gates

- **Use when**:
  - Starting a project or significant feature with no written quality bar.
  - The user requests quality gates, standards enforcement, or stopping agents from shipping regressions.
  - An agent repeatedly adds suppressions, skips tests, or loosens thresholds to pass.
  - Unattended autonomous loops (`/build auto`) need deterministic merge boundaries.
- **Do NOT use when**:
  - `CONSTRAINTS.md` already exists and remains unchanged (read and follow it directly).
  - Throwaway spikes or 1-day exploratory prototypes.
  - User requested immediate code review (`andino-code-review`) or CI setup (`andino-ci-cd-and-automation`).

## The 4-Question Intake Discipline

Never ask what can be inspected from package manifests. Present at most four questions, each with a GUESS and a DEFAULT:
1. **Dimensions**: Enforce coverage (a), security (b), performance (c), accessibility (d), or architecture (e)? *Default: (a) + (b).*
2. **Blocking Policy**: Block or warn on mid-task failure? *Default: Block on floor, warn on optional.*
3. **Threshold Strategy**: Target numbers or measure and hold? *Default: Measure baseline today and ratchet.*
4. **Latency Budget**: Max tolerated check duration? *Default: <=5s edit loop, <=90s task end, uncapped in CI.*

## The Five Floor Invariants (Zero Setup Required)

Diff-scoped against `merge-base -> working-tree + untracked`. Always enforced:
1. **No Silenced Checkers**: Zero added `@ts-ignore`, `@ts-nocheck`, `eslint-disable`, `biome-ignore`, `# noqa`, `istanbul ignore`, `nosemgrep`.
2. **No Tests Made Easier**: Zero added `.skip()`, deleted test files, or assertions stripped from surviving tests.
3. **No Unfinished Stubs**: Zero `throw new Error("Not implemented")`, empty `catch {}`, or `TODO` placeholders in new code.
4. **No Weakened Rules**: Zero lowered minimums, raised maximums, or deleted constraint rows in `CONSTRAINTS.md`.
5. **No Leaked Secrets**: All secret scanning must mandate `--redact`. Never leak credential tokens into agent transcripts.

## Anti-Rationalization Refutations

| Rationalization | Mandated Reality |
|---|---|
| *"We'll add constraints once the code settles."* | **False.** Code settles around whatever was permitted while moving. Enforce the floor on day one. |
| *"Our unit tests are our constraints."* | **False.** Tests prove you agree with yourself. Enforce at least one external constraint (WCAG, CVE, Lighthouse). |
| *"We can't hit 80% coverage on legacy code."* | **False.** Measure today's number (e.g. 52%) and enforce that it must not fall. |
| *"Checks slow down the agent too much."* | **False.** Scope checks to the diff; keep edit checks <5s and task checks <90s. |
| *"I need to bypass a gate for an urgent hotfix."* | **False.** Register an owned Exception row with a 90-day expiry. Never lower the global rule. |

## Diagnostic Red Flags (Stop Immediately)

- [ ] Modifying `CONSTRAINTS.md` in the same commit as a failing feature implementation.
- [ ] Running an intake past 4 questions or asking what was already readable in `package.json`.
- [ ] Writing a constraint number without an executable command in the `Checked by` column.
- [ ] An exception row lacking an individual owner (`@user`) or expiring beyond 90 days.
- [ ] Running secret scanners without `--redact` or letting scanner errors (exit 2) pass as clean (exit 0).

## Progressive Disclosure Resources

- [resources/floor-guard.md](resources/floor-guard.md) — Node.js (`floor-guard.mjs`) and Python (`floor_guard.py`) diff-scoped guards.
- [resources/quality-gate-protocols.md](resources/quality-gate-protocols.md) — Normalizing Semgrep, Axe-core, and Lighthouse exit codes.
- [resources/constraint-catalog.md](resources/constraint-catalog.md) — De facto tool matrices and sane defaults for TS, Python, Go, Rust, Web.
- [resources/worked-example.md](resources/worked-example.md) — Complete intake, `CONSTRAINTS.md` generation, and anti-evasion walkthrough.

## Operational Example (Offline)

```python andino-operational-example
import json, os, re
def floor(diff, old_min, new_min, available=True):
    if not available: return {"exit": 2, "rules": ["baseline-unavailable"]}
    findings = []
    in_hunk = False
    for line in diff.splitlines():
        if line.startswith("@@"): in_hunk = True; continue
        if not in_hunk: continue
        if line.startswith("+") and not line.startswith("+++"):
            if re.search(r"@ts-ignore|eslint-disable|biome-ignore|#\s*noqa|\.skip\(", line[1:]): findings.append("silenced-or-skipped")
            if re.search(r"Not implemented|catch\s*\{\s*\}|\bTODO\b", line[1:]): findings.append("unfinished-work")
        if line.startswith("-") and not line.startswith("---") and re.search(r"\b(assert|expect)\b", line[1:]):
            findings.append("assertion-removed")
    if new_min < old_min: findings.append("threshold-loosened")
    return {"exit": 1 if findings else 0, "rules": sorted(list(set(findings)))}
def probe():
    diff = "--- a/test.py\n+++ b/test.py\n@@ -1 +1,3 @@\n-assert answer == 42\n+// @ts-ignore\n+throw new Error('Not implemented');\n"
    if os.getenv("ANDINO_NEGATIVE"): return floor("", 80, 80, False)
    return floor(diff, 80, 70)
print(json.dumps(probe(), sort_keys=True))
```

Default output: `{"exit": 1, "rules": ["assertion-removed", "silenced-or-skipped", "threshold-loosened", "unfinished-work"]}`  
Adversarial output (`ANDINO_NEGATIVE=1`): `{"exit": 2, "rules": ["baseline-unavailable"]}`

## Output & Verification

Return the concrete `CONSTRAINTS.md`, modified script identifiers, exact check results, and one `NEXT ACTION` in the active Andino ticket. Never claim completion without test evidence.
