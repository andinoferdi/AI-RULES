# CI/CD and Quality Automation Guide

This guide provides deep technical craft, architectural patterns, and operational procedures for designing, optimizing, and operating production-grade CI/CD pipelines under Andino Workflow governance.

---

## 1. Universal Invariants vs Platform Implementations

While syntax varies across CI/CD providers (GitHub Actions, GitLab CI, Buildkite, CircleCI), the core architectural invariants of quality automation remain universal:

1. **Deterministic Local Parity:** Every automated check executed in remote CI must be runnable locally by developers and AI agents using standard project commands (e.g. `npm run lint`, `npm test`, `npm run build`).
2. **Directed Acyclic Graph (DAG) Execution:** Stages must adhere to strict dependency order: inexpensive static gates run first; heavy integration and builds run only after static checks pass. A failure in an ancestor gate strictly blocks downstream jobs.
3. **Fail-Closed Gate Enforcement:** Any unhandled error, failing exit code, or unmet threshold fails the job immediately. Never allow `continue-on-error: true` on critical quality gates.
4. **Isolated Ephemeral Environments:** Every job runs in a clean, isolated container or virtual machine. Tests requiring database or cache services must use isolated service containers, not shared remote staging instances.
5. **Immutable Build Artifacts:** Build once, deploy across stages. Never recompile the application binary or bundle between staging and production; promote the identical compiled artifact.

---

## 2. CI Optimization & Performance Tuning

When the CI pipeline duration exceeds **10 minutes**, developer feedback loops degrade and AI agents suffer prolonged cycle latency. Apply these optimization strategies in strict hierarchical order of impact:

```text
Pipeline Exceeds 10 Minutes?
    │
    ├── 1. CACHE DEPENDENCIES
    │   └── Cache package manager store (npm, pnpm, yarn, pip), NOT node_modules or venv.
    │
    ├── 2. PARALLELIZE INDEPENDENT JOBS
    │   └── Split monolithic jobs into concurrent jobs: lint, typecheck, test, and build run in parallel.
    │
    ├── 3. PATH-BASED CONDITIONAL EXECUTION
    │   └── Skip documentation-only PRs from running backend integration or browser E2E suites.
    │
    ├── 4. MATRIX BUILDS & TEST SHARDING
    │   └── Shard long-running test suites across N parallel runners:
    │       strategy: { matrix: { shard: [1, 2, 3, 4] } }
    │
    ├── 5. TEST SUITE OPTIMIZATION
    │   └── Relocate slow, non-critical integration tests or nightly benchmarks to scheduled runs.
    │
    └── 6. RUNNER SIZING
        └── Scale to GitHub-hosted larger runners or dedicated self-hosted runners for CPU/RAM heavy builds.
```

### High-Impact Pattern: Caching & Parallel Job Splitting

```yaml
# Parallelized Job Architecture Example
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx tsc --noEmit

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
```

---

## 3. Environment & Secret Management

A secure pipeline enforces strict segregation between public configuration, local development, test secrets, and production credentials:

```text
.env.example       → Committed (Template showing required variable names and comments)
.env                → NOT committed (.gitignore; local developer overrides)
.env.test           → Committed (Deterministic mock values for local and CI unit tests)
CI Secrets          → Stored in GitHub Secrets / Vault (Dedicated CI-only DB credentials, test tokens)
Production Secrets  → Stored in Production Cloud Platform / KMS (Never accessible to CI PRs from forks)
```

### Golden Rules for Secrets:
1. **Never Hardcode Credentials:** Even for throwaway local test containers, reference variables from environment configurations or GitHub Secrets.
2. **Restrict Fork Permissions:** Never expose production secrets to pull requests originating from public forks. Use `pull_request_target` only with extreme caution and never with an unreviewed checkout.
3. **Audit Log Masking:** Ensure sensitive tokens are registered as secrets so the CI runner automatically masks them with `***` in execution logs.

---

## 4. Release & Deployment Strategies

### A. Ephemeral Preview Deployments
Every active pull request should generate an isolated preview environment. This allows stakeholders, designers, and automated browser agents to verify visual and interactive state before merging to `main`.

### B. Feature Flags: Decoupling Deployment from Release
Feature flags allow code to be continuously merged to `main` and deployed to production without immediately exposing unfinished features to users:

```typescript
// Production Feature Flag Implementation
if (featureFlags.isEnabled('new-payment-engine', { userId: user.id })) {
  return executeModernPaymentFlow(order);
}
return executeLegacyPaymentFlow(order);
```

**Feature Flag Lifecycle:**
1. **Creation:** Define flag with an explicit owner and expiration date (e.g. 30 days).
2. **Testing:** Enable flag in local development and preview environments.
3. **Canary Rollout:** Enable flag for 1% of users, monitor error rates for 30 minutes, then expand to 10%, 50%, and 100%.
4. **Cleanup:** Once stable at 100%, delete the flag check and remove legacy dead code. Flags that linger indefinitely become dangerous technical debt.

### C. Staged Rollouts & Monitoring Window
```text
PR Merged to main
    │
    ▼
Staging Automated Deployment
    │
    ▼ Smoke tests pass
Production Canary Deployment (10% traffic)
    │
    ▼ 15-minute observation window
    ├── Error rate exceeds threshold (>0.1%) → Trigger Instant Rollback
    └── Zero anomalies detected → Promote to 100% Full Production
```

### D. Reversible Rollback Plans
Every deployment workflow must have an automated or single-command rollback procedure. 
**Security Requirement:** In workflow dispatch or CLI rollback scripts, never interpolate raw user inputs into shell commands (`npx deploy rollback ${{ inputs.version }}`). Always pass inputs through quoted environment variables to eliminate shell command injection vulnerabilities.

---

## 5. Repository Governance & Operational Roles

1. **Automated Dependency Updates:** Configure Dependabot or Renovate with weekly intervals. Group non-breaking minor/patch updates to reduce pull request notification fatigue.
2. **The "Build Cop" Rotation:** In active teams, designate an on-duty Build Cop responsible for keeping CI green. If the build breaks on `main`, the Build Cop immediately reverts the offending PR or assists the author with an urgent patch.
3. **Branch Protection Gates:**
   - Require at least 1 approving pull request review.
   - Require all CI status checks (lint, typecheck, test, build) to pass.
   - Enforce branch up-to-date requirements before merging.
   - Prohibit force-pushes (`git push --force`) to `main`.

---

## 6. Operational Example (Offline Deterministic Python Runner)

The checker re-reads this runnable standard-library example from the emitted guide and executes it in a temporary directory. The default and `ANDINO_NEGATIVE=1` variants are bounded procedure examples verifying DAG dependency stage evaluation and cascading blocker propagation.

```python andino-operational-example
import json, os
def evaluate(jobs):
    state={}
    for name,deps,exit_code in jobs:
        state[name] = "blocked" if any(state[d] != "pass" for d in deps) else ("pass" if exit_code == 0 else "fail")
    return state
def probe():
    lint_exit = 1 if os.getenv("ANDINO_NEGATIVE") else 0
    jobs=[("lint",[],lint_exit),("unit",["lint"],0),("build",["unit"],0),("publish",["build"],0)]
    result=evaluate(jobs)
    return {"stages":result,"publish_ready":all(v=="pass" for v in result.values()),"deployed":False}
print(json.dumps(probe(), sort_keys=True))
```

Default expected output:
```json
{"stages":{"lint":"pass","unit":"pass","build":"pass","publish":"pass"},"publish_ready":true,"deployed":false}
```

Adversarial input expected output:
```json
{"stages":{"lint":"fail","unit":"blocked","build":"blocked","publish":"blocked"},"publish_ready":false,"deployed":false}
```

---

## 7. Anti-Patterns and Fallback

Do not replace this method with a name-only index, source checkout link, upstream installation request, or unexecuted success claim. Apply one concrete evidence-driven procedure. If the required execution environment is absent, return the local artifact/triage and the explicit verification limit; do not silently substitute a simulated or hallucinated result.

---

## 8. Provenance

Adapted in original wording from addyosmani/agent-skills, source `skills/ci-cd-and-automation/SKILL.md`, local snapshot `aeac41d4d005999432bb7312f7ff06383a91d59d`. Supporting resource provenance is recorded in the main quality manifest. Substantive adapted material is covered by the packaged [Addy MIT notice](../../references/legal/addy-license.md). Upstream is audit/build provenance only; runtime requires no upstream installation or network fetch.
