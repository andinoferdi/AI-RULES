# Ledgerline

Invoicing backend for small accounting firms. Two deployables live in this repository:

- `api/`: Node 22, TypeScript 5.7, Fastify 5, Vitest 3, ESLint 9 with typescript-eslint. Code is
  split into `src/domain/` (business rules) and `src/http/` (routes and error shapes). The domain
  layer is meant to know nothing about HTTP.
- `worker/`: Python 3.12 job that builds monthly revenue reports. pytest 8, pytest-cov, ruff and
  mypy are dev dependencies (mypy is installed but not run anywhere).

There is no web UI in this repository. The customer dashboard is a separate Next.js repository,
`ledgerline-dashboard`, which gets a preview deploy for every pull request.

## People

- @maya-lead, tech lead. Owns merges to `main` and any change to quality policy.
- @dani, backend engineer.
- @rina-pm, product manager.

## How work is done

- Most changes are written by coding agents (Claude Code and Codex). A nightly scheduled agent run
  is planned for dependency bumps.
- `.claude/settings.json` runs ESLint after every agent edit.
- CI is GitHub Actions (`.github/workflows/ci.yml`). The `api` and `worker` jobs are required
  checks on `main`. Pull requests target `main`.
- Laptops run macOS and Windows. Machine-wide tools such as gitleaks, osv-scanner or semgrep are
  not installed on laptops; CI runners can install anything.

## Measurements on record

- `api/coverage/lcov.info`: produced by @dani on 2026-11-02 at commit 3f1c2aa with a coverage
  provider installed only on his laptop (`npx vitest run --coverage`). CI does not produce
  coverage.
- `worker/reports/coverage-2026-11-02.txt`: `pytest --cov=report_worker` followed by
  `coverage report --precision=1`, same day and commit.
