# Worked example: from intake to a blocked evasion

A TypeScript billing service, from the first look at the repository to the guard rejecting an
agent's shortcut. Names, numbers and outputs illustrate the shape of each step; the guard output in
step 6 was produced by the reference guard in [floor-guard.md](floor-guard.md) on a reproduction of
this diff.

## 1. Detect before asking

Read before the first question:

| Looked at | Found |
| --- | --- |
| `package.json` | Next.js 15, TypeScript 5.7, Vitest 3, ESLint 9; no `@vitest/coverage-v8` |
| `eslint.config.mjs` | Flat config, `no-explicit-any` as error |
| `coverage/lcov.info` | 64.2% line coverage from `vitest run --coverage` on `main` at `a1b2c3d`, run by hand |
| `.github/workflows/ci.yml` | `npm test` and `npm run lint` on pull requests; shallow checkout |
| `.claude/settings.json`, `AGENTS.md` | A PostToolUse hook runs ESLint after edits; no quality bar written down |
| Existing suppressions | One `@ts-ignore` and one `eslint-disable` in `src/legacy/xml-parser.ts` |
| Running URL | Preview deploys per pull request (`$PREVIEW_URL`) |

Two-line report to the user:

> Next.js 15 with Vitest and ESLint; CI runs tests and lint, nothing measures coverage, and the
> Vitest coverage provider is not installed. Coverage on record is 64.2% from a hand run on `main`.

## 2. Ask only what is left, one question at a time

Each question carries a guess and a default, so "I don't know" still produces a working setup.

```text
Q1: Beyond the floor, which of these should be enforced?
    (a) coverage on new code  (b) security scanning  (c) performance budgets
    (d) accessibility  (e) architecture boundaries
GUESS: (a) and (b): there is a test runner and the service handles payment input.
DEFAULT if unsure: (a) and (b).
Cost: (c) and (d) run against the preview URL in CI; (e) needs a rules file.
User: "(a), (b) and (d)."
```

```text
Q2: When a check fails while an agent is mid-task, block or warn?
GUESS: Block. A warning nobody reads mid-task is ignored.
DEFAULT if unsure: block on the floor, warn on the rest for two weeks.
User: "Block."
```

```text
Q3: Target numbers, or measure today and hold that line?
GUESS: Measure and hold for project coverage; changed lines at 80% from day one.
DEFAULT if unsure: measure and hold.
User: "Hold the line."
```

```text
Q4: Slowest check you will tolerate before the agent hands work back?
GUESS: About 90 seconds at task end.
DEFAULT if unsure: 90 seconds at task end, unlimited in CI.
User: "90 seconds."
```

## 3. Baselines

- Changed-line coverage needs no baseline: 80% applies to new code from the first change.
- Project coverage is re-measured on `main` with the enforcing command
  (`vitest run --coverage`, line coverage over `src/**`, one decimal): 64.2%, the same as the file
  on record. Had the scope or command differed, the row would stay pending until a comparable run.
- Accessibility has no baseline yet: the first preview scan records today's count.

## 4. CONSTRAINTS.md

```markdown
# Constraints

Last reviewed: 2026-11-01 by @lead

## Floor (always enforced, no setup required)

- No new suppression comments (`@ts-ignore`, `eslint-disable`, `# noqa`, `# type: ignore`, coverage-ignore pragmas)
- No skipped, focused or deleted tests, and no assertions removed from tests that stay
- No unimplemented stubs, empty catch blocks or `TODO` standing in for an implementation
- No secrets in source; secret scanners run with `--redact`
- No check made optional in CI (`continue-on-error: true`, `|| true`)
- This file is not weakened to make a change pass

## Enforced

| ID | Rule | Why this number | Checked by | Runs at |
|----|------|-----------------|------------|---------|
| F1 | Diff passes the floor guard | No number: any move that lowers the bar | `node scripts/floor-guard.mjs --base origin/main --check-expiry` | edit, task end, CI |
| Q1 | Zero type errors | A type error is a bug the compiler already found | `npx tsc --noEmit` | task end, CI |
| Q2 | Zero lint errors from our config | The config is the team's agreed style | `npm run lint` | edit, CI |
| Q3 | Changed lines ≥ 80% covered | High enough to force a test, low enough to allow a config line | `npm run check:coverage` | task end, CI |
| Q4 | Secrets: no findings | A leaked key costs more than any delay | `gitleaks dir . --redact --no-banner` | CI |
| Q5 | Dependencies: nothing at high or above | Below that is mostly noise | `osv-scanner scan source -r .` | CI |
| Q6 | Accessibility: zero critical or serious | Moderate and minor findings are often debatable | `npm run check:a11y` | preview deploy |

## Measured, not yet enforced

| ID | Metric | Today | Source (command, revision, precision) | Direction | Tolerance |
|----|--------|-------|----------------------------------------|-----------|-----------|
| M1 | Project line coverage | 64.2% | `vitest run --coverage`, `main` at a1b2c3d, one decimal | must not fall | 0.5 |
| M2 | Main bundle size | 172 kB | `size-limit --json`, `main` at a1b2c3d | must not grow | 2 |

## Pending or not applicable

| Dimension | Why it is not enforced here | Becomes enforced when |
|-----------|-----------------------------|-----------------------|
| Performance budgets | Not chosen in intake | The team picks it |

## Known debt (predates this file; not exceptions)

- `src/legacy/xml-parser.ts`: one `@ts-ignore`, one `eslint-disable` (rewrite in ENG-402)

## Exceptions

| ID | Rule | Path | Reason and ticket | Owner | Approved by | Expires |
|----|------|------|-------------------|-------|-------------|---------|

No exceptions are approved.
```

One line goes into `AGENTS.md` (which `CLAUDE.md` imports):
`Read CONSTRAINTS.md before writing code. Do not weaken it to make a change pass.`

## 5. Install, wire and prove

- `npm i -D @vitest/coverage-v8@3.2.4` (pinned to the installed Vitest), `reporter: ['lcov']` in
  `vitest.config.ts`, and a changed-line coverage script behind `check:coverage`.
- `package.json`: `check:floor`, `check:fast` (floor, tsc, lint), `check:task` (fast, tests with
  coverage, `check:coverage`), `check:a11y` (axe against `$PREVIEW_URL` through the quality gate).
- The existing ESLint hook in `.claude/settings.json` also runs the floor guard.
- CI: `fetch-depth: 0`, the floor guard and `check:task` in the required job, gitleaks and
  osv-scanner in a security job, `check:a11y` after the preview is reachable.

Check record (each command run in a disposable copy):

| Check | Case | Result |
| --- | --- | --- |
| Floor guard | Clean branch | exit 0, 0.3 s |
| Floor guard | Branch adding `it.skip` | exit 1, `test-made-easier` |
| Floor guard | `--base origin/missing` | exit 2 |
| `check:coverage` | New function without a test | exit 1 (0% of 6 changed lines) |
| `check:coverage` | Same function with its test | exit 0 (100% of 6) |
| `check:a11y` | Not run: no preview in the sandbox | Next: run on the first pull request's preview |

## 6. The agent takes the cheap road to green

An agent adding a billing endpoint produces this diff:

```diff
--- a/src/billing/service.ts
+++ b/src/billing/service.ts
@@ -41,0 +42,3 @@ export async function processPayment(user: User, amount: number) {
+  // @ts-ignore legacy currency code
+  const currency = user.profile.currency;
+  if (!currency) throw new Error("Not implemented yet");
--- a/src/billing/service.test.ts
+++ b/src/billing/service.test.ts
@@ -15,3 +15 @@ describe("BillingService", () => {
-  it("validates currency format", () => {
-    expect(validateCurrency("USD")).toBe(true);
-  });
+  it.skip("validates currency format", () => {});
--- a/CONSTRAINTS.md
+++ b/CONSTRAINTS.md
@@ -18 +18 @@
-| Q3 | Changed lines ≥ 80% covered | High enough to force a test, low enough to allow a config line | `npm run check:coverage` | task end, CI |
+| Q3 | Changed lines ≥ 70% covered | High enough to force a test, low enough to allow a config line | `npm run check:coverage` | task end, CI |
```

The edit hook runs the guard:

```text
floor-guard: 5 violation(s):
  [test-made-easier] src/billing/service.test.ts:15
  [silenced-checker] src/billing/service.ts:42
  [unfinished-work] src/billing/service.ts:44
  [assertion-removed] src/billing/service.test.ts:16 (removed)
  [threshold-loosened] CONSTRAINTS.md:18 (removed) -> CONSTRAINTS.md:18

Each finding lowers the bar. Fix the code; a genuine exception goes through the policy owner.
```

The findings name locations, not line contents. The agent's next moves:

1. Type `user.profile.currency` properly instead of suppressing the error.
2. Implement the missing-currency branch.
3. Restore the test and its assertion.
4. Revert `CONSTRAINTS.md`.

If the deadline arrives first, the change stays blocked. The agent hands the failing evidence to
@lead, who may approve a Q3 exception for `src/billing/service.ts` in its own pull request, with a
ticket, a named owner and an expiry within 90 days.

## Anti-pattern

The same agent "fixes" the red build by adding `src/billing/**` to the coverage exclude list in
`vitest.config.ts`. The guard does not read tool configuration, so the move passes the floor. That
is why measurement configuration sits under maintainer review (CODEOWNERS) next to
`CONSTRAINTS.md`. Review and ownership cover what a regex cannot.
