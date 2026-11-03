# AI Agent CI Error-Reflection Loop

This resource defines the protocol for AI coding agents (Claude Code, Codex, Antigravity) to process, diagnose, and remediate automated CI/CD pipeline failures with high token efficiency and zero hallucinated passes.

---

## 1. The Reflection Architecture

When an automated CI gate fails, the agent must not blindly retry commands or generate speculative fixes. It must execute this closed-loop cycle:

```
┌────────────────────────────────────────────────────────┐
│                   CI Gate Failure                       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Log Extraction & Distillation (RTK / Pattern Filter)│
│    Strip terminal noise, extract stack trace & context  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Failure Classification                              │
│    Identify failure category: Lint, Type, Test, Build  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Single-Cycle Root Cause Diagnosis                   │
│    Inspect local source files; identify the broken seam │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. Deterministic Local Verification                    │
│    Run exact failing check locally; confirm exit code 0│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 5. Atomic Commit & Push Readiness                      │
│    Stage only touched files; document fix in commit msg│
└────────────────────────────────────────────────────────┘
```

---

## 2. Distilled Log Extraction & Tokenomics

CI logs often span thousands of lines containing environment setup, download progress bars, and dependency extraction trees. Dumping raw logs into an agent's context window wastes working tokens, causes context fragmentation, and degrades reasoning.

### Log Distillation Rules:
1. **Filter Out Noise**: Discard package installation logs, asset download percentages, and compiler informational banners.
2. **Extract the Core Trace**: Isolate:
   - The exact failing command (e.g., `npm run test:unit`)
   - The exit code (e.g., `Process completed with exit code 1`)
   - The file path and line number of the failure (e.g., `src/auth/token.ts:42:15`)
   - The assertion or compiler error message (e.g., `Expected status 200, received 500`)
3. **Use Distillation Tools**:
   - In CLI environments, prefix commands with `rtk` (Rust Token Killer) or pipe output through focused grep/sed patterns.
   - For Jest/Vitest: filter for `FAIL` suites and lines between `●` and stack boundary.
   - For TypeScript: filter for `error TS\d+:`.

---

## 3. Failure Classification & Targeted Remediation Matrix

| Category | Typical Symptoms | Targeted Agent Remediation Procedure | Forbidden Shortcuts |
|---|---|---|---|
| **Lint / Format** | ESLint, Prettier, or Ruff exit code 1; styling/whitespace error. | Run automated formatter/fixer (`npm run lint -- --fix` or `ruff check --fix`). Inspect unfixable rules and correct the syntax. | **NEVER** add `/* eslint-disable */` or suppress rules without explicit user instruction. |
| **Type Check** | `tsc --noEmit` or `mypy` failures; TS2322, TS2339. | Read exact line and symbol definition. Fix the interface mismatch or type narrowing in the source code. | **NEVER** use `@ts-ignore`, `@ts-expect-error`, or cast to `any` as an escape hatch. |
| **Unit / Test** | Jest, Vitest, or Pytest assertion failures; expected vs received mismatch. | Read test code and implementation. If implementation introduced a regression, fix implementation. If test expectations are outdated due to an approved contract change, update the test assertion with documented justification. | **NEVER** comment out failing tests, delete assertions, or mark tests as `.skip`. |
| **Build / Bundle** | Webpack, Vite, Next.js build failure; missing asset, circular import, syntax error. | Inspect the build log around the fatal error. Verify path aliases (`@/...`), environment variable accessibility during build time, and export/import signatures. | **NEVER** delete build flags or remove required output verification steps. |
| **Integration / DB** | Prisma/TypeORM/Flyway migration mismatch; connection refused; 500 status. | Check database service readiness (`pg_isready`), verify schema migration files against database snapshot, and inspect mock vs real environment variables. | **NEVER** bypass migrations or drop tables without an audited migration plan. |
| **E2E / Browser** | Playwright/Cypress timeout, selector not found, assertion failed on element state. | Download or inspect failure artifacts (traces, screenshots, HTML snapshot). Diagnose whether the failure is a timing issue (race condition) or a real UI/DOM regression. Add explicit web-first assertions (`toBeVisible()`). | **NEVER** insert hardcoded sleeps (`sleep(5000)`) instead of locator-based waiting. |
| **Security Audit** | `npm audit` or `pip-audit` reports high/critical vulnerabilities. | Identify affected dependency. Run targeted update (`npm update <pkg>` or `npm audit fix`). If a breaking major version is required, assess risk and record decision. | **NEVER** lower the audit threshold from `--audit-level=high` to pass the gate. |

---

## 4. Single-Cycle Root-Cause Debugging Protocol

AI agents are susceptible to "shotgun debugging" — making random edits across multiple files in hopes that one passes. To prevent this, enforce a single-cycle debugging discipline:

1. **Hypothesis Formation**: State in one sentence: *"The test failed because `X` in file `Y` did not account for state `Z`."*
2. **Minimal Seam Edit**: Modify only the code necessary to address hypothesis `X`.
3. **Local Replay**: Execute ONLY the failing test suite locally first to confirm the fix:
   ```sh
   # Example: replay specific failing test
   npx vitest run src/auth/token.test.ts
   ```
4. **Full Quality Gate Verification**: Only after the isolated test passes, execute the full pipeline locally to ensure no collateral regressions were introduced:
   ```sh
   npm run lint && npx tsc --noEmit && npm test
   ```

---

## 5. Anti-Hallucination & Anti-Flakiness Guardrails

### Flaky Test Detection:

Compare the original failure and a diagnostic pass at the same commit. Capture
the run and attempt IDs, runner and service versions, shard/seed, first failing
step, and available logs. Separate service startup, migration, and test
execution. Use the first divergent signal to test one hypothesis (readiness,
shared state, ordering, resource pressure, or infrastructure). Reproduce under
matching conditions, then repeat the targeted check after the fix and report
the number of attempts and failures. A passing rerun alone leaves the cause open.
If a test passes locally but failed in CI (or vice-versa), do not dismiss it as "just flaky" or re-run until it passes.
- Check for shared state across test suites (e.g. global variables, database records not cleaned in `afterEach`).
- Check for race conditions, unresolved Promises, or timezone/locale dependencies.
- Quarantine genuinely flaky external dependencies with a clear TODO and issue reference, never silently.

### Anti-Hallucination Mandates:
- **No Passing Claims Without Observable Output**: An agent must never declare "CI pipeline passed" unless it has directly observed exit code 0 from the test runner.
- **Evidence Preservation**: Include the passing output summary in the handoff or execution plan checkpoint.
