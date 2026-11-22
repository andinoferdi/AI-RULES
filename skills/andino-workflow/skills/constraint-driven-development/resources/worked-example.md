# Complete Worked Example: From Intake to Anti-Evasion

This worked example demonstrates the end-to-end lifecycle of Constraint-Driven Development in a production TypeScript/Next.js repository. It covers:
1. Pre-interview environment detection.
2. The 4-question intake interview with sane defaults.
3. Generating the canonical `CONSTRAINTS.md`.
4. Wiring checks into developer lifecycle scripts.
5. Detecting and mechanically rejecting an AI evasion diff.
6. Embedded zero-dependency verification harness.

---

## 1. Step 1: Detect Before Asking

Before opening an intake interview, inspect the repository silently:
```sh
# Inspected files:
# - package.json -> dependencies include "typescript", "vitest", "eslint"
# - eslint.config.mjs -> active flat config
# - coverage/lcov.info -> exists from previous run, current project coverage is 64.2%
# - .github/workflows/ci.yml -> runs `npm test` and `npm run lint`
```

**Two-line report to the user:**
> "Detected Next.js 15, TypeScript 5.7, ESLint 9, and Vitest. Baseline project test coverage is currently 64.2%."

---

## 2. Step 2: The 4-Question Intake

```
Q1: Beyond the baseline floor, which dimensions do you want enforced?
    (a) Test coverage on changed code
    (b) Security scanning (secrets & code)
    (c) Performance budgets (Lighthouse)
    (d) Accessibility (Axe-core)
GUESS: (a) and (b) — you have Vitest installed and handle authenticated user routes.
DEFAULT if unsure: (a) and (b).
User answer: "Default is fine, let's do (a) and (b)."

Q2: When a check fails mid-task, should the agent block or warn?
GUESS: Block. A warning nobody reads mid-task is an ignored warning.
DEFAULT if unsure: Block on the floor, warn on optional dimensions.
User answer: "Block."

Q3: Do you have specific target numbers in mind, or should I measure today's baseline and hold the line?
GUESS: Measure and hold. Baseline coverage is 64.2%; changed lines target 80%.
DEFAULT if unsure: Measure and hold.
User answer: "Hold the line."

Q4: What is the slowest check you'll tolerate before an agent hands work back?
GUESS: 90 seconds for task-end checks; fast loop under 5 seconds.
DEFAULT if unsure: 90s at task end, unlimited in CI.
User answer: "90s."
```

---

## 3. Step 3: Canonical `CONSTRAINTS.md` Generated

The skill writes `CONSTRAINTS.md` at the repository root:

```markdown
# Quality Constraints

Last reviewed: 2026-11-01 by @andino

## Floor (Always Enforced, Zero Setup Required)

- No new suppression comments: `@ts-ignore`, `@ts-nocheck`, `eslint-disable`, `biome-ignore`
- No unimplemented stubs: `throw new Error("Not implemented")`, empty `catch {}`
- No skipped or deleted tests without a justified commit message
- No removed assertions from surviving test files
- No secrets in source code (`--redact` mandatory)
- This file does not get weakened to make a change pass

## Enforced With Numbers

| Dimension | Rule | Checked by | Runs at |
|---|---|---|---|
| Types | Zero type errors | `tsc --noEmit` | every edit |
| Lint | Zero errors from config | `npm run lint` | every edit |
| Secrets | No leaked credentials | `gitleaks dir . --redact --no-banner` | every edit |
| Floor Guard | Zero floor violations | `node scripts/floor-guard.mjs` | every edit |
| Coverage | Changed lines >= 80% covered | `vitest run --coverage` | task end, CI |
| Security: code | Zero HIGH or CRITICAL | `npm run check:security` | CI |
| Security: deps | Zero HIGH or CRITICAL | `osv-scanner scan source -r .` | CI |

Every row names the exact executable command that produces the verdict.

## Measured, Not Yet Enforced (Ratchets)

| Metric | Today | Direction | Tolerance |
|---|---|---|---|
| Project test coverage | 64.2% | must not fall | 0.5% |
| Bundle size (main entry) | 172 kB | must not grow | 2 kB |

## Exceptions

| ID | Rule | Path | Reason | Owner | Expires |
|---|---|---|---|---|---|
| W1 | `no-explicit-any` | `src/legacy/xml-parser.ts` | Legacy migration ENG-402 | @andino | 2026-12-31 |
```

---

## 4. Step 4: Wire to Package Scripts

Update `package.json`:
```json
{
  "scripts": {
    "check:floor": "node scripts/floor-guard.mjs",
    "check:fast": "npm run check:floor && tsc --noEmit && npm run lint && gitleaks dir . --redact --no-banner",
    "check:task": "npm run check:fast && vitest run --coverage",
    "check:security": "semgrep scan --config p/typescript --strict --json > semgrep.json && node scripts/quality-gate.mjs semgrep semgrep.json",
    "check:full": "npm run check:task && npm run check:security && osv-scanner scan source -r ."
  }
}
```

---

## 5. Step 5: The Mid-Task Evasion Attempt

An agent is tasked with adding a new billing endpoint. To achieve green status rapidly, it creates this unified git diff:

```diff
--- a/src/billing/service.ts
+++ b/src/billing/service.ts
@@ -42,3 +42,5 @@ export async function processPayment(user: User, amount: number) {
+// @ts-ignore: bypass type mismatch on legacy currency code
+const currency = user.profile.currency;
+if (!currency) throw new Error("Not implemented yet");

--- a/src/billing/service.test.ts
+++ b/src/billing/service.test.ts
@@ -15,4 +15,2 @@ describe("BillingService", () => {
-  it("validates currency format", () => {
-    expect(validateCurrency("USD")).toBe(true);
-  });
+  it.skip("validates currency format", () => {});

--- a/CONSTRAINTS.md
+++ b/CONSTRAINTS.md
@@ -18,1 +18,1 @@
-| Coverage | Changed lines >= 80% covered | `vitest run --coverage` | task end, CI |
+| Coverage | Changed lines >= 70% covered | `vitest run --coverage` | task end, CI |
```

---

## 6. Step 6: Mechanical Rejection by Floor Guard

When `npm run check:fast` runs, the floor guard analyzes the diff:

```
$ node scripts/floor-guard.mjs

floor-guard: [VIOLATION] Found 4 attempt(s) to weaken the floor:
  - [silenced-checker] src/billing/service.ts: "// @ts-ignore: bypass type mismatch on legacy currency code"
  - [unfinished-work] src/billing/service.ts: "if (!currency) throw new Error("Not implemented yet");"
  - [test-made-easier] src/billing/service.test.ts: "it.skip("validates currency format", () => {});"
  - [threshold-loosened] CONSTRAINTS.md: "Minimum lowered: 80.0 -> 70.0"

Fix the issues above or register a tracked exception in CONSTRAINTS.md.
npm ERR! Lifecycle script failed with exit code 1.
```

The change is **blocked mechanically**. The agent cannot self-certify completion until:
1. The `@ts-ignore` is replaced with proper typing.
2. The stub `throw new Error("Not implemented yet")` is replaced with real logic.
3. The test `.skip` is removed and the test assertion is restored.
4. `CONSTRAINTS.md` is reverted to `>= 80%`.

---

## 7. Embedded Python Verification Harness

Below is the standalone Python verification script (`run_verification.py`) asserting floor-guard behavior:

```python
import json
import os
import re

def evaluate_floor(diff_text, old_min=80, new_min=80, is_available=True):
    if not is_available:
        return {"exit": 2, "rules": ["baseline-unavailable"]}

    findings = []
    in_hunk = False

    re_suppression = re.compile(r"@ts-ignore|@ts-nocheck|eslint-disable|biome-ignore|#\s*noqa")
    re_stub = re.compile(r"Not implemented|catch\s*\{\s*\}|\bTODO\b")
    re_skip = re.compile(r"\.skip\(|\.todo\(|@pytest\.mark\.skip")

    for line in diff_text.splitlines():
        if line.startswith("@@"):
            in_hunk = True
            continue
        if not in_hunk:
            continue

        if line.startswith("+") and not line.startswith("+++"):
            content = line[1:]
            if re_suppression.search(content):
                findings.append("silenced-checker")
            if re_stub.search(content):
                findings.append("unfinished-work")
            if re_skip.search(content):
                findings.append("test-made-easier")

        elif line.startswith("-") and not line.startswith("---"):
            content = line[1:]
            if "assert " in content or "expect(" in content:
                findings.append("assertion-removed")

    if new_min < old_min:
        findings.append("threshold-loosened")

    return {
        "exit": 1 if findings else 0,
        "rules": sorted(list(set(findings)))
    }

def probe():
    sample_diff = (
        "--- a/service.ts\n"
        "+++ b/service.ts\n"
        "@@ -1,3 +1,4 @@\n"
        "-expect(result).toBe(true);\n"
        "+// @ts-ignore\n"
        "+it.skip('test', () => {});\n"
        "+throw new Error('Not implemented');\n"
    )
    if os.getenv("ANDINO_NEGATIVE"):
        return evaluate_floor("", 80, 80, is_available=False)
    return evaluate_floor(sample_diff, old_min=80, new_min=70, is_available=True)

if __name__ == "__main__":
    result = probe()
    print(json.dumps(result, sort_keys=True))
```

**Expected Default Output:**
```json
{"exit": 1, "rules": ["assertion-removed", "silenced-checker", "test-made-easier", "threshold-loosened", "unfinished-work"]}
```

**Expected Adversarial Output (`ANDINO_NEGATIVE=1`):**
```json
{"exit": 2, "rules": ["baseline-unavailable"]}
```
