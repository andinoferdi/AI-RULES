# Multi-Ecosystem Constraint Catalog & Tooling Presets

When configuring `CONSTRAINTS.md`, picking a dimension requires naming a real executable command. Never leave an aspiration without a mechanism, and never hand-roll custom linters when de facto ecosystem tools exist.

This catalog provides tested tooling mappings, CLI execution commands, and sane default thresholds across major technology stacks.

---

## 1. Sane Defaults Matrix

When the user or project has no specific numbers in mind, use these industry-tested baselines. Every number has a rationale; a threshold without a reason will be removed by the next developer who hits it.

| Constraint | Default Threshold | Why This Number |
|---|---|---|
| **Coverage on New Code** | `>= 80%` of changed lines | High enough to enforce tests, low enough to accommodate configuration lines. |
| **Project Coverage** | `Today's value (must not fall)` | Prevents build failures on legacy code while forbidding regressions. |
| **Mutation Score (Stryker)** | `>= 60%` on diff | 60% is realistic for new suites; mature suites target 80%. |
| **Dependency Vulnerabilities** | `Zero HIGH or CRITICAL` | Low and medium are often noisy or non-exploitable in context. |
| **Core Web Vitals: LCP** | `<= 2500 ms` | Google's threshold for "Good" Largest Contentful Paint. |
| **Core Web Vitals: CLS** | `<= 0.1` | Google's threshold for "Good" Cumulative Layout Shift. |
| **Accessibility (WCAG AA)** | `Zero CRITICAL or SERIOUS` | Moderate and minor issues are often debatable or false-positives. |
| **Exception Expiry** | `90 days` | Long enough to schedule refactoring, short enough not to be forgotten. |
| **Ratchet Drift Tolerance** | `0.5` percentage points | Absorbs minor floating-point or unrelated line drift. |

---

## 2. TypeScript & JavaScript Ecosystem

### Tooling Mapping
| Dimension | De Facto Tool | Installation | Execution Command | Gate Rule |
|---|---|---|---|---|
| **Types** | `tsc` | Dev dependency | `tsc --noEmit` | Exit code 0 (zero errors) |
| **Lint** | `biome` or `eslint` | Dev dependency | `biome check` or `eslint .` | Exit code 0 |
| **Secrets** | `gitleaks` | System binary | `gitleaks dir . --redact --no-banner` | Exit code 0 |
| **Coverage** | `vitest` or `jest` | Vitest needs its provider: `npm i -D @vitest/coverage-v8@<installed vitest version>`; Jest has it built in | `vitest run --coverage` (writes lcov with `reporter: ['lcov']`) | Changed lines `>= 80%` (section 7) |
| **Architecture** | `dependency-cruiser` | `npm i -D dependency-cruiser`, rules in `.dependency-cruiser.cjs` (`npx depcruise --init`) | `npx depcruise src` | Exit code 0 (error-severity rules fail) |
| **Architecture (ESLint already the linter)** | ESLint `no-restricted-imports` | Rule in `eslint.config.*` scoped to the inner layer's files | the existing lint command | Exit code 0 |
| **Security: Code** | `semgrep` | pipx / brew | `semgrep scan --config p/typescript --json` | Normalized via quality-gate |
| **Security: Deps** | `osv-scanner` | brew / binary | `osv-scanner scan source -r .` | Zero high or critical |
| **Bundle Size** | `size-limit` | Dev dependency | `size-limit --json` | Per-entry byte budget |
| **Mutation** | `stryker` | Dev dependency | `stryker run --mutate <changed-files>` | Mutation score `>= 60%` |

### Ready-to-Use `package.json` Scripts
```json
{
  "scripts": {
    "check:floor": "node scripts/floor-guard.mjs --base origin/main --check-expiry",
    "check:fast": "npm run check:floor && tsc --noEmit && biome check && gitleaks dir . --redact --no-banner",
    "check:task": "npm run check:fast && vitest run --coverage",
    "check:security": "semgrep scan --config p/default --strict --json > semgrep-results.json && node scripts/quality-gate.mjs semgrep semgrep-results.json",
    "check:full": "npm run check:task && npm run check:security && osv-scanner scan source -r ."
  }
}
```

---

## 3. Python Ecosystem

### Tooling Mapping
| Dimension | De Facto Tool | Installation | Execution Command | Gate Rule |
|---|---|---|---|---|
| **Types** | `mypy` or `pyright` | `pip install mypy` | `mypy .` | Exit code 0 |
| **Lint & Format** | `ruff` | `pip install ruff` | `ruff check . && ruff format --check .` | Exit code 0 |
| **Secrets** | `gitleaks` | System binary | `gitleaks dir . --redact --no-banner` | Exit code 0 |
| **Coverage** | `pytest-cov` | `pip install pytest-cov` | `pytest --cov --cov-report=lcov` (or `--cov-report=xml`) | Changed lines `>= 80%` (section 7) |
| **Changed-line coverage** | `diff-cover` | `pip install diff-cover` | `diff-cover coverage.xml --compare-branch=origin/main --fail-under=80` (reads Cobertura XML or LCov) | Exit code 0 |
| **Architecture** | `import-linter` | `pip install import-linter`, `forbidden` or `layers` contract in `.importlinter` | `lint-imports` | Exit code 0 |
| **Security: Code** | `semgrep` | `pipx install semgrep` | `semgrep scan --config p/python --json` | Normalized via quality-gate |
| **Security: Deps** | `pip-audit` | `pip install pip-audit` | `pip-audit --strict` | Zero known vulnerabilities |

### Ready-to-Use `Makefile` / `pyproject.toml`
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
strict = true
warn_unreachable = true

[tool.pytest.ini_options]
# Project floor: --cov-fail-under is today's measured value (a ratchet), not an invented 80.
addopts = "--cov=src --cov-report=term-missing --cov-report=xml"
```

```makefile
# Makefile
.PHONY: check-floor check-fast check-task check-security

check-floor:
	python scripts/floor_guard.py --base origin/main --check-expiry

check-fast: check-floor
	ruff check .
	ruff format --check .
	mypy src

check-task: check-fast
	pytest --cov=src --cov-report=xml
	diff-cover coverage.xml --compare-branch=origin/main --fail-under=80

check-security:
	pip-audit
	semgrep scan --config p/python --strict --json > semgrep.json && python scripts/quality_gate.py semgrep semgrep.json
```

---

## 4. Go Ecosystem

### Tooling Mapping
| Dimension | De Facto Tool | Installation | Execution Command | Gate Rule |
|---|---|---|---|---|
| **Types & Vet** | `go vet` | Built-in | `go vet ./...` | Exit code 0 |
| **Lint** | `golangci-lint` | `go install ...` | `golangci-lint run` | Exit code 0 |
| **Secrets** | `gitleaks` | System binary | `gitleaks dir . --redact --no-banner` | Exit code 0 |
| **Coverage** | `go test` | Built-in | `go test -race -coverprofile=coverage.out ./...` | Changed lines `>= 80%` |
| **Architecture** | `golangci-lint` `depguard` | `depguard` rules in `.golangci.yml` | `golangci-lint run` | Exit code 0 |
| **Security: Deps** | `govulncheck` | `go install golang.org/x/vuln/cmd/govulncheck@latest` | `govulncheck ./...` | Exit code 0 |

### Ready-to-Use `Makefile`
```makefile
.PHONY: check-floor check-fast check-task

check-floor:
	python scripts/floor_guard.py --base origin/main --check-expiry

check-fast: check-floor
	go vet ./...
	golangci-lint run

check-task: check-fast
	go test -race -coverprofile=coverage.out ./...
	govulncheck ./...
```

---

## 5. Rust Ecosystem

### Tooling Mapping
| Dimension | De Facto Tool | Installation | Execution Command | Gate Rule |
|---|---|---|---|---|
| **Compilation** | `cargo check` | Built-in | `cargo check --all-targets` | Exit code 0 |
| **Lint** | `cargo clippy` | `rustup component add clippy` | `cargo clippy --all-targets -- -D warnings` | Exit code 0 |
| **Formatting** | `cargo fmt` | `rustup component add rustfmt` | `cargo fmt -- --check` | Exit code 0 |
| **Secrets** | `gitleaks` | System binary | `gitleaks dir . --redact --no-banner` | Exit code 0 |
| **Coverage** | `cargo tarpaulin` | `cargo install cargo-tarpaulin` | `cargo tarpaulin --out Lcov` | Changed lines `>= 80%` |
| **Security: Deps** | `cargo audit` | `cargo install cargo-audit` | `cargo audit` | Zero vulnerabilities |

---

## 6. Web Frontend & Runtime Checks

Web applications require browser-grounded verification. Because Lighthouse and Axe-core require a running URL, they belong in the **runtime / preview stage** (`check:a11y` and `check:perf`), never in the fast edit loop.

### Tooling Mapping
| Dimension | De Facto Tool | Execution Command | Blocking Gate |
|---|---|---|---|
| **Accessibility** | `axe-core` | `axe "$PREVIEW_URL" --tags wcag2a,wcag2aa --stdout > axe.json && node scripts/quality-gate.mjs axe axe.json` | Zero CRITICAL or SERIOUS |
| **Performance (LCP)** | `lighthouse` | `lighthouse $PREVIEW_URL --output=json --quiet > lh.json` | LCP `<= 2500 ms` |
| **Performance (CLS)** | `lighthouse` | `lighthouse $PREVIEW_URL --output=json --quiet > lh.json` | CLS `<= 0.1` |

### Quality Gate Script Wrapper for Lighthouse
```js
// scripts/check-lighthouse.mjs
import { readFileSync } from 'node:fs';
let report;
try {
  report = JSON.parse(readFileSync('lh.json', 'utf8'));
} catch {
  console.error('Lighthouse report missing or unreadable');
  process.exit(2);
}
const lcp = report?.audits?.['largest-contentful-paint']?.numericValue;
const cls = report?.audits?.['cumulative-layout-shift']?.numericValue;
// A missing metric means the run failed (error page, unreachable URL); it must not pass.
if (typeof lcp !== 'number' || typeof cls !== 'number') {
  console.error('Lighthouse report has no LCP or CLS value');
  process.exit(2);
}

if (lcp > 2500) {
  console.error(`LCP failed: ${lcp}ms > 2500ms`);
  process.exit(1);
}
if (cls > 0.1) {
  console.error(`CLS failed: ${cls} > 0.1`);
  process.exit(1);
}
console.log(`Lighthouse passed: LCP ${Math.round(lcp)}ms, CLS ${cls}`);
process.exit(0);
```

These checks need a running URL. When the project has none (a CLI, a library, an API with no UI),
say so and record the dimension as not applicable here, with the repository or deploy where it
belongs, instead of wiring a check that cannot run.

---

## 7. Changed-Line Coverage Without a Second Run

Coverage of the lines a change touched is the number an agent can move, and it needs no baseline:
it applies to new code from day one. Compute it from the report the test run already writes.
Running the suite twice to get one number is the fastest way to make people skip the check.

1. Make the existing test command write a machine-readable report: lcov (Vitest with
   `reporter: ['lcov']` and its coverage provider, Jest, c8, `coverage lcov` for coverage.py,
   `cargo llvm-cov --lcov`) or Cobertura XML (`pytest --cov --cov-report=xml`).
2. Collect the added line numbers per file from `git diff --unified=0 <merge-base>` plus untracked
   files, the same input the floor guard reads.
3. For each changed source file, take the added lines the report lists as executable. Covered
   lines have a hit count above zero. Lines the report does not list (comments, blank lines) do not
   count.
4. Changed-line coverage is covered over executable changed lines. A changed source file missing
   from the report counts as uncovered rather than skipped, so a new untested file cannot pass.
5. Exit 0 at or above the threshold, 1 below it, 2 when the report or the merge base is missing.

`diff-cover` does exactly this for Cobertura XML and LCov reports
(`diff-cover coverage.xml --compare-branch=origin/main --fail-under=80`); prefer it where Python is
available. Otherwise a small script over the lcov file is enough. Prove either one on a change that
adds an untested function (expect exit 1) and on the same change with its test (expect exit 0).
