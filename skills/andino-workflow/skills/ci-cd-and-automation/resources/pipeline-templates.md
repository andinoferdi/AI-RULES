# Production CI/CD Pipeline Templates

These GitHub Actions examples assume npm, Node and the named scripts. Start from the
repository's lockfile, runtime pin, script names and required check names, and apply the
[rules for every pipeline](../SKILL.md#rules-for-every-pipeline). Action versions were checked
on 2026-11-26 (`actions/checkout@v7`, `actions/setup-node@v7`, `actions/upload-artifact@v7`);
actions outside the `actions/` organisation are pinned to a full commit SHA, and Dependabot
(section 6) keeps both current. Scope permissions to what each job needs; see the
[GitHub secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use).

---

## 1. Universal CI Pipeline (Node.js / Modern Web)

Runs on every pull request, on pushes to the primary branch and in the merge queue. It
enforces the full gate: dependency caching, lint, type check, tests with coverage, build and
a dependency audit. `setup-node` with `cache: npm` caches the npm cache keyed by the
lockfile, not `node_modules`. When the job is split into parallel jobs, keep the required
check name on an aggregate job ([required checks](../SKILL.md#required-checks-keep-their-name-and-cannot-pass-a-failure)).

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  merge_group:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  quality:
    name: Quality Gates
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
        with:
          persist-credentials: false

      - name: Setup Node.js runtime
        uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc   # or node-version: '22' when there is no pin file
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

Use an isolated, disposable PostgreSQL service for integration tests. The literal below is a
public test fixture value scoped to that service. It lets fork PRs exercise the same gate
without secrets. Use secret storage for actual credentials to external systems. Test files
that share the database must own their data (per-worker database or schema, rolled-back
transactions, unique ids) or run serially.

```yaml
# .github/workflows/integration.yml
name: Integration Tests

on:
  pull_request:
    branches: [main]
  merge_group:

permissions:
  contents: read

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
          POSTGRES_PASSWORD: ci_fixture_only
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
        with:
          persist-credentials: false

      - name: Setup Node.js runtime
        uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Database Migrations
        env:
          DATABASE_URL: postgresql://ci_user:ci_fixture_only@localhost:5432/testdb
        run: npx prisma migrate deploy

      - name: Execute Integration Test Suite
        env:
          DATABASE_URL: postgresql://ci_user:ci_fixture_only@localhost:5432/testdb
        run: npm run test:integration
```

---

## 3. End-to-End Testing (Playwright with Artifact Retention)

E2E tests run against a built application. When E2E tests fail, retaining traces,
screenshots and logs is mandatory for AI and human diagnosis.

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  pull_request:
    branches: [main]
  merge_group:

permissions:
  contents: read

jobs:
  e2e:
    name: Browser E2E Suite
    runs-on: ubuntu-latest
    timeout-minutes: 25

    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
        with:
          persist-credentials: false

      - name: Setup Node.js runtime
        uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
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
        uses: actions/upload-artifact@v7
        with:
          name: playwright-failure-report
          path: playwright-report/
          retention-days: 7
```

---

## 4. PR Preview Deployments (Vercel / Cloud Platforms)

This credentialed example assumes same-repository PR authors are trusted to run repository
code with preview credentials. Fork PRs are skipped here and keep the ordinary unprivileged
CI workflow. Reassess this boundary if your repository grants branch creation to
contributors who lack deployment trust. Never move this job to `pull_request_target` to give
forks a preview.

```yaml
# .github/workflows/preview.yml
name: Preview Deployment

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read

jobs:
  deploy-preview:
    if: github.event.pull_request.head.repo.full_name == github.repository
    name: Deploy Ephemeral Preview
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: preview

    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
        with:
          persist-credentials: false

      - name: Setup Node.js runtime
        uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Deploy to Vercel Preview
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ vars.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ vars.VERCEL_PROJECT_ID }}
        run: |
          npx vercel pull --yes --environment=preview --token="$VERCEL_TOKEN"
          npx vercel build --token="$VERCEL_TOKEN"
          PREVIEW_URL=$(npx vercel deploy --prebuilt --token="$VERCEL_TOKEN")
          echo "Preview deployed to: $PREVIEW_URL" >> "$GITHUB_STEP_SUMMARY"
```

---

## 5. Parameterized Rollback Workflow (Quoted Input)

Every deployment pipeline must have an immediate, reversible rollback that redeploys an
earlier artifact without rebuilding it. Inputs must always be passed via environment
variables to defend against shell command injection, and validated before use. The runner
has no platform login, so the CLI gets its token explicitly.

```yaml
# .github/workflows/rollback.yml
name: Emergency Rollback

on:
  workflow_dispatch:
    inputs:
      target_deployment_id:
        description: 'Deployment URL or ID to roll back to'
        required: true
        type: string
      reason:
        description: 'Incident reason for emergency rollback'
        required: true
        type: string

permissions:
  contents: read

jobs:
  rollback:
    name: Execute Instant Rollback
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: production
    concurrency:
      group: deploy-production
      cancel-in-progress: false

    steps:
      - name: Validate and announce the rollback
        env:
          TARGET: ${{ inputs.target_deployment_id }}
          REASON: ${{ inputs.reason }}
          ACTOR: ${{ github.actor }}
        run: |
          [[ "$TARGET" =~ ^[A-Za-z0-9._:/-]+$ ]] || { echo "::error::unexpected characters in target"; exit 1; }
          echo "Initiating emergency rollback to: $TARGET"
          echo "Reason: $REASON"
          echo "Authorized by: $ACTOR"

      - name: Execute Platform Rollback
        env:
          TARGET: ${{ inputs.target_deployment_id }}
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: |
          # TARGET is a quoted shell variable, never ${{ }} inside run: (no shell injection).
          npx vercel rollback "$TARGET" --token "$VERCEL_TOKEN" --yes
```

---

## 6. Automated Dependency Updates (Dependabot)

Keep dependencies and GitHub Actions updated on an automated cadence. Group minor and patch
updates to reduce pull request noise.

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
    groups:
      minor-and-patch:
        update-types: ["minor", "patch"]
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

---

## 7. Promote One Image with OIDC (Container Service)

Build one image per commit, deploy it to staging, then promote the same digest to production
behind the `production` environment's required reviewers. Credentials come from OIDC roles
trusted per environment, not stored keys. Migrations run before the service update and stay
compatible with the previous release; a rollback (section 5) redeploys a stored digest.
The example targets AWS ECR and ECS; the shape is the same on other platforms.

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  staging:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    environment: staging
    permissions:
      contents: read
      id-token: write
    concurrency:
      group: deploy-staging
      cancel-in-progress: false
    outputs:
      image: ${{ steps.push.outputs.image }}
    steps:
      - uses: actions/checkout@v7
        with:
          persist-credentials: false
      - uses: aws-actions/configure-aws-credentials@45666896f5d8e0f10ae255413f3a4cdd03bdc8f5 # v6.3.1
        with:
          role-to-assume: ${{ vars.DEPLOY_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      - id: push
        env:
          REGISTRY: ${{ vars.REGISTRY }}   # <account>.dkr.ecr.<region>.amazonaws.com
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin "$REGISTRY"
          docker build -t "$REGISTRY/app:$GITHUB_SHA" --build-arg GIT_SHA="$GITHUB_SHA" .
          docker push "$REGISTRY/app:$GITHUB_SHA"
          digest=$(aws ecr describe-images --repository-name app --image-ids imageTag="$GITHUB_SHA" \
            --query 'imageDetails[0].imageDigest' --output text)
          echo "image=$REGISTRY/app@$digest" >> "$GITHUB_OUTPUT"
      - env:
          IMAGE: ${{ steps.push.outputs.image }}
        run: |
          ./scripts/migrate.sh staging              # before the new code starts
          ./scripts/deploy.sh staging "$IMAGE"      # update the service, wait until stable
          ./scripts/smoke.sh staging "$GITHUB_SHA"  # /healthz must report this SHA

  production:
    needs: staging
    runs-on: ubuntu-latest
    timeout-minutes: 30
    environment: production                       # required reviewers approve here
    permissions:
      contents: read
      id-token: write
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@v7
        with:
          persist-credentials: false
      - uses: aws-actions/configure-aws-credentials@45666896f5d8e0f10ae255413f3a4cdd03bdc8f5 # v6.3.1
        with:
          role-to-assume: ${{ vars.DEPLOY_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      - env:
          IMAGE: ${{ needs.staging.outputs.image }}  # the digest staging verified
        run: |
          ./scripts/migrate.sh production
          ./scripts/deploy.sh production "$IMAGE"
          ./scripts/smoke.sh production "$GITHUB_SHA"
          ./scripts/watch.sh production 10m         # fail, and roll back, if the error alarm fires
```

Turn on the platform's automatic rollback as well (for ECS, the deployment circuit breaker
with `rollback=true`) so tasks that never become healthy are reverted without a person.
