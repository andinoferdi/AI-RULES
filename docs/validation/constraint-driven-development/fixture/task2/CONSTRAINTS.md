# Constraints

Last reviewed: 2026-11-20 by @maya-lead

## Floor (always enforced)

- No new suppression comments
- No skipped, deleted or weakened tests
- No unimplemented stubs or empty catch blocks
- No secrets in source
- This file is not weakened to make a change pass

## Enforced

| ID | Rule | Checked by | Runs at |
|----|------|------------|---------|
| F1 | Diff passes the floor guard | `node scripts/floor-guard.mjs --base origin/main` | edit, task end, CI |
| Q1 | api lint: zero errors, at most 20 warnings | `cd api && npx eslint src --max-warnings 20` | edit, CI |
| Q2 | api changed lines ≥ 80% covered | `node scripts/changed-coverage.mjs api/coverage/lcov.info` | task end, CI |
| Q3 | worker lint: zero errors | `cd worker && ruff check .` | edit, CI |
| Q4 | Secrets: no findings | `gitleaks dir . --redact --no-banner` | CI |

## Measured, not yet enforced

| Metric | Today | Direction | Tolerance |
|--------|-------|-----------|-----------|
| api project coverage | 61.7% | must not fall | 0.5 |
| worker project coverage | 74.2% | must not fall | 0.5 |

## Exceptions

| ID | Rule | Path | Reason | Owner | Expires |
|----|------|------|--------|-------|---------|
| W1 | Q2 | `api/src/legacy/csv.ts` | Rewrite tracked in LED-112 | @dani | 2026-12-15 |
