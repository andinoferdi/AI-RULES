# Production CI/CD Pipeline Templates

This resource provides production-ready, security-audited workflow configurations for modern software delivery. Use these templates as foundational scaffolding, adapting runtime versions, package managers, and secret names to match your repository.

---

## 1. Universal CI Pipeline (Node.js / Modern Web)

This workflow runs on every pull request and push to the primary branch. It enforces the full unbroken quality gate: checkout, dependency caching, linting, typechecking, test coverage, production build, and security auditing.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

jobs:
  quality:
    name: Quality Gates
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js runtime
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies (frozen lockfile)
        run: npm ci

      - name: Gate 1 - Lint & Code Style
        run: npm run lint

      - name: Gate 2 - Static Type Validation
        run: npx tsc --noEmit

      - name: Gate 3 - Unit & Focused Tests (with Coverage)
        run: npm test -- --coverage

      - name: Gate 4 - Application Production Build
        run: npm run build

      - name: Gate 5 - Dependency Vulnerability Audit
        run: npm audit --audit-level=high
```

---

## 2. Database Integration Testing (PostgreSQL Service Container)

For applications requiring real database interactions during automated testing, use isolated service containers. Never hardcode credentials; always use GitHub Secrets or workflow environment variables.

```yaml
# .github/workflows/integration.yml
name: Integration Tests

on:
  pull_request:
    branches: [main]

jobs:
  integration:
    name: Database & Service Tests
    runs-on: ubuntu-latest
    timeout-minutes: 20

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD || 'ci_secure_test_password' }}
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js runtime
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Database Migrations
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD || 'ci_secure_test_password' }}@localhost:5432/testdb
        run: npx prisma migrate deploy

      - name: Execute Integration Test Suite
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD || 'ci_secure_test_password' }}@localhost:5432/testdb
        run: npm run test:integration
```

---

## 3. End-to-End Testing (Playwright with Artifact Retention)

E2E tests run against a built application. When E2E tests fail, retaining traces, screenshots, and logs is mandatory for AI and human diagnosis.

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  pull_request:
    branches: [main]

jobs:
  e2e:
    name: Browser E2E Suite
    runs-on: ubuntu-latest
    timeout-minutes: 25

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js runtime
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers & OS Dependencies
        run: npx playwright install --with-deps chromium

      - name: Build Application Artifacts
        run: npm run build

      - name: Execute Playwright E2E Tests
        run: npx playwright test

      - name: Upload Test Report & Failure Artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-failure-report
          path: playwright-report/
          retention-days: 7
```

---

## 4. PR Preview Deployments (Vercel / Cloud Platforms)

Deploy ephemeral preview instances for every active pull request to enable manual visual inspection and stakeholder review before merging to production.

```yaml
# .github/workflows/preview.yml
name: Preview Deployment

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  deploy-preview:
    name: Deploy Ephemeral Preview
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js runtime
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Deploy to Vercel Preview
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
        run: |
          npx vercel pull --yes --environment=preview --token=$VERCEL_TOKEN
          npx vercel build --token=$VERCEL_TOKEN
          PREVIEW_URL=$(npx vercel deploy --prebuilt --token=$VERCEL_TOKEN)
          echo "Preview deployed to: $PREVIEW_URL" >> $GITHUB_STEP_SUMMARY
```

---

## 5. Parameterized Rollback Workflow (Shell-Injection Immune)

Every deployment pipeline must have an immediate, reversible rollback mechanism. Inputs must always be passed via environment variables to defend against shell command injection.

```yaml
# .github/workflows/rollback.yml
name: Emergency Rollback

on:
  workflow_dispatch:
    inputs:
      target_deployment_id:
        description: 'Target Deployment ID or Git Commit SHA to rollback to'
        required: true
        type: string
      reason:
        description: 'Incident reason for emergency rollback'
        required: true
        type: string

jobs:
  rollback:
    name: Execute Instant Rollback
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Announce Rollback Initiation
        env:
          TARGET: ${{ inputs.target_deployment_id }}
          REASON: ${{ inputs.reason }}
          ACTOR: ${{ github.actor }}
        run: |
          echo "Initiating emergency rollback to: $TARGET"
          echo "Reason: $REASON"
          echo "Authorized by: $ACTOR"

      - name: Execute Platform Rollback
        env:
          TARGET: ${{ inputs.target_deployment_id }}
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: |
          # Safe execution: TARGET is evaluated as a quoted shell variable,
          # preventing shell command injection vulnerability.
          npx vercel rollback "$TARGET" --token="$VERCEL_TOKEN" --yes
```

---

## 6. Automated Dependency Updates (Dependabot)

Keep dependencies and GitHub Actions securely updated on an automated cadence.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "04:00"
      timezone: "Etc/UTC"
    open-pull-requests-limit: 5
    reviewers:
      - "<REPO_OWNER>"
    commit-message:
      prefix: "chore(deps)"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 3
    commit-message:
      prefix: "ci(actions)"
```
