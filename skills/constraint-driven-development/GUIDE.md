# The Craft of Constraint-Driven Development

This guide defines the comprehensive methodology for establishing, measuring, and mechanically enforcing a project's quality contract under Andino Workflow governance.

---

## 1. Foundations: The Irreversible Quality Ratchet

In software development, writing code used to be the primary bottleneck. Human engineers read what they wrote, and their internal taste and standards governed quality.

Autonomous and semi-autonomous coding agents invert this dynamic: **an agent can generate more code in an afternoon than a team can review in a week.** When an agent hits a failing test or a strict linter mid-task, its optimization gradient is simple: find the fastest path to green. Without hard mechanical guardrails, agents take the cheapest road to green—they add `@ts-ignore`, comment out assertions, `.skip()` tests, or lower coverage thresholds.

```
┌────────────────────────────┐       ┌────────────────────────────┐       ┌────────────────────────────┐
│  Spec-Driven Development   │ ────▶ │   Test-Driven Development  │ ────▶ │ Constraint-Driven Develop. │
│     "What to build"        │       │      "Proves it works"     │       │ "Good enough to ship"      │
└────────────────────────────┘       └────────────────────────────┘       └────────────────────────────┘
```

- **Spec-driven development** defines what to build.
- **Test-driven development** proves the implementation works against the specification.
- **Constraint-Driven Development** defines what "good enough to ship" means before anyone argues in a pull request.

**The Core Axiom**: Prose instructions ("write clean, secure code with good tests") degrade across agent context windows. A constraint only exists if violation terminates execution with a non-zero exit code (`1` or `2`).

---

## 2. The 3-Tier Circularity Hierarchy

Not all constraints provide equal protection. If an agent writes both the implementation and the tests that verify it, verification becomes circular. To establish genuine confidence, rank constraints by their external independence:

```
                  ▲
                 / \
                /   \       Tier 1: EXTERNAL CONSTRAINTS
               /  1  \      (Axe-core WCAG, OSV vulnerability DB, Lighthouse Core Web Vitals)
              /───────\     Agent cannot manipulate these standards.
             /    2    \    Tier 2: PROJECT CONSTRAINTS
            /───────────\   (Team ESLint/Biome rules, architecture boundaries, gitleaks rules)
           /      3      \  Human-owned files; agent cannot alter without review.
          /───────────────\ Tier 3: SUITE CONSTRAINTS
                            (Project's own unit tests, mocks, test fixtures)
                            High utility, but inherently circular if agent wrote both.
```

### The Rule of External Opinions
A quality bar made entirely of Tier 3 checks (the project's own tests) can pass while the application is fundamentally broken or insecure. **A production `CONSTRAINTS.md` must enforce at least one Tier 1 or Tier 2 external constraint.**

---

## 3. The 4-Question Intake Discipline

Never ask what you can read. Before asking the user any questions, silently inspect the repository:
- Language and package manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`).
- Existing test runners, linters, and coverage artifacts.
- CI workflows in `.github/workflows/`.

Limit intake to **at most four discriminating questions**, and provide a **GUESS** and a **DEFAULT** for each. A 12-question intake produces a configuration nobody understands and a user who abandons setup.

```
Q1: Beyond the baseline floor, which dimensions do you want enforced?
    (a) Test coverage on new code
    (b) Security scanning (code & secrets)
    (c) Performance budgets (Lighthouse)
    (d) Accessibility (Axe-core)
    (e) Architecture boundaries (dependency-cruiser)
DEFAULT if unsure: (a) and (b). (Note: (c) and (d) require a running preview URL).

Q2: When a check fails mid-task, should the agent block or warn?
DEFAULT if unsure: Block on the floor, warn on optional dimensions for the first 2 weeks.

Q3: Do you have target numbers in mind, or should I measure today's baseline and hold the line?
DEFAULT if unsure: Measure and hold. (See Ratchets below).

Q4: What is the slowest check you'll tolerate before the agent hands work back?
DEFAULT if unsure: 90 seconds at task end; fast edit checks under 5 seconds.
```

---

## 4. The 4-Stage Lifecycle Integration

The single biggest mistake teams make is running every check everywhere. A gate that stalls the agent loop gets disabled with `--no-verify`, and a disabled gate is worse than no gate because the illusion of safety remains.

| Stage | Trigger / Command | Checks Executed | Latency Budget |
|---|---|---|---|
| **1. BUILD** | Post-edit / `check:fast` | Types, fast linter, secret scan, **The Floor Guard** | **< 5 seconds** (changed files only) |
| **2. VERIFY** | Task end / `check:task` | Unit & integration tests, diff-scoped coverage | **< 90 seconds** |
| **3. REVIEW** | PR review / `check:review` | Full floor guard, security scans, mutation on diff | **2 - 5 minutes** |
| **4. SHIP** | CI pipeline / `check:full` | All above + preview deploy checks (Lighthouse, Axe-core) | **Uncapped (in CI)** |

### Two Rules for Fast Loops
1. **Scope to the Diff**: Check the lines and files the change touched, not the entire repository. Coverage on changed lines is a number the agent directly controls; total repository coverage is debt it inherited.
2. **Cost Dictates Placement**: Expensive scanners (mutation testing, whole-repo Semgrep, Lighthouse) belong at review or in CI, never in the post-edit loop.

---

## 5. The Ratchet Mechanism: "Measure Today and Hold the Line"

Demanding 80% coverage on a legacy codebase currently at 45% creates a red build that never turns green, teaching the team to ignore failures.

The ratchet solves this without negotiation: **record where the project is today, and refuse to let it get worse.**

```
Metric: Project Test Coverage
Recorded Today: 64.2%
Direction: must not fall
Tolerance: 0.5% (absorbs floating-point and unrelated file drift)

Commit 1 (Agent adds feature without tests): Coverage drops to 62.8% -> BLOCKED.
Commit 2 (Agent adds proper tests): Coverage rises to 66.1% -> PASSED.
RATCHET TIGHTENED: Update CONSTRAINTS.md baseline to 66.1%.
```

Ratcheting turns technical debt repayment into an automated, monotonic side-effect of daily feature delivery.

---

## 6. Guarding the Bar Itself: The 5 Evasion Moves

Coding agents rarely craft elaborate exploits. Instead, when faced with a red check, they take the shortest path to green. The diff-scoped floor guard watches for these five specific moves:

1. **Threshold Moved**: Changing `80%` to `70%`, raising a latency budget from `200ms` to `300ms`, or deleting a rule row from `CONSTRAINTS.md`.
2. **Test Made Easier**: Adding `.skip()`, deleting test files, or removing assertions (`expect()`, `assert`) from surviving test files.
3. **Checker Silenced**: Introducing suppression comments (`@ts-ignore`, `@ts-nocheck`, `eslint-disable`, `biome-ignore`, `# noqa`, `istanbul ignore`, `Stryker disable`, `nosemgrep`).
4. **Unfinished Work**: Adding stub functions with `throw new Error("Not implemented")`, empty `catch {}` blocks, or `TODO` markers.
5. **Unauthorized Exceptions**: Adding a row to the `Exceptions` table without documented authority, ticket reference, and explicit expiry date.

---

## 7. Anti-Rationalization Refutation Table

| Agent / Developer Rationalization | Mandated Reality |
|---|---|
| *"We'll add quality constraints once the codebase settles."* | **False.** Code settles around whatever was permitted while it was moving. Add the floor on day one. |
| *"Our unit tests are our constraints."* | **False.** Tests prove you agree with yourself. They say nothing about coverage on new code, dependency risks, or bundle growth. |
| *"We can't hit 80% coverage on this legacy codebase."* | **False.** Do not demand 80%. Measure today's number (e.g. 52.4%) and enforce that it must not fall. |
| *"These quality checks slow down the agent too much."* | **False.** Only if slow checks were placed in the fast loop. Move scans over 5 seconds to task-end or CI. |
| *"I'll remember what our standards are without writing them down."* | **False.** The agent writing the code has no memory across sessions; it needs an explicit contract in `CONSTRAINTS.md`. |
| *"This constraint is blocking an emergency hotfix."* | **False.** Add a tracked Exception row with a 90-day expiry and your handle. Never delete or lower the global constraint. |

---

## 8. Diagnostic Red Flags (Stop Immediately)

- [ ] Modifying `CONSTRAINTS.md` in the same commit as a failing feature implementation.
- [ ] An intake interview running past 4 questions or asking what could be read from `package.json`.
- [ ] A numbered constraint written into `CONSTRAINTS.md` without an exact executable command in the `Checked by` column.
- [ ] An exception row lacking an individual owner (`@user`) or having an expiry date beyond 90 days.
- [ ] Hand-rolling a custom regex checker when a de facto tool (`tsc`, `biome`, `ruff`, `vitest`) exists.
- [ ] Secret scanners (`gitleaks`) executed without the `--redact` flag.
- [ ] Floor guard returning exit code 0 when diff collection fails (errors must always exit 2).

---

## 9. Progressive Disclosure to Resources

- [resources/floor-guard.md](resources/floor-guard.md) — Complete Node.js (`floor-guard.mjs`) and Python stdlib (`floor_guard.py`) diff-scoped implementations.
- [resources/quality-gate-protocols.md](resources/quality-gate-protocols.md) — Exit code normalization for Semgrep, Axe-core, and Lighthouse; redaction rules; exception schemas.
- [resources/constraint-catalog.md](resources/constraint-catalog.md) — Tooling matrices and sane default presets for TypeScript, Python, Go, Rust, and Web UI.
- [resources/worked-example.md](resources/worked-example.md) — End-to-end walkthrough from intake to anti-evasion rejection with embedded Python test script.

---

## 10. Provenance

Adapted from addyosmani/agent-skills, source `skills/constraint-driven-development/SKILL.md`. Substantive adapted material is covered by the packaged Addy MIT notice ([references/license.md](references/license.md)). Upstream is audit/build provenance only; runtime requires no upstream installation or network fetch.

