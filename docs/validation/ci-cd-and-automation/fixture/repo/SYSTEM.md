# Orders platform

Node 22 (`.nvmrc`), TypeScript 5, Express 4, Postgres 16, npm with `package-lock.json`,
Vitest 3 and Playwright. The API ships as a Docker image to AWS ECS (Fargate). The web app in
`web/` is a Vite single-page app hosted on Vercel.

## Repository and contributors

- Public repository `acme/orders-platform` on GitHub. About 30% of pull requests come from
  forks opened by community contributors.
- The repository's default `GITHUB_TOKEN` permission is "Read and write" (the old default;
  nobody changed it).
- Repository secrets: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (an IAM user with
  administrator rights in the AWS account), `VERCEL_TOKEN`, and `LABELER_PAT` (a personal
  access token with `repo` scope used by the labeling workflow). Repository variables:
  `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.
- A notice in the repository's Actions tab says GitHub will enforce, on 2026-12-02, the default
  policy that blocks `pull_request_target` workflows in public repositories.

## Merge rules on `main`

- A ruleset requires one approving review and the status check `build` from GitHub Actions.
- The merge queue is enabled for `main`.
- The team's status dashboard reads the check run named `build` on each `main` commit through
  the GitHub API to show whether `main` is green.

## CI today

- `.github/workflows/ci.yml` has one job and takes about 22 minutes. `npm install` takes about
  6 minutes of that (nothing is cached) and the end-to-end tests about 9 minutes.
- Lint does not block: the step has `continue-on-error: true`. `main` has 14 lint errors today.
- About 35% of pull requests change only files under `docs/` or `*.md` files.
- The integration tests failed in 6 of the last 40 runs on `main`. A re-run usually passes.
  `DEBUG_SQL=1` was added to the integration step last week to help investigate. The logs of
  the latest runs are in `ci-logs/`.

## Tests

- `npm test`: unit tests, no services needed.
- `npm run test:integration`: needs Postgres 16 and `DATABASE_URL`; run `npm run db:migrate`
  first. All integration test files use the same database.
- `npm run e2e`: Playwright against `npm run preview` of the built web app, so it needs
  `npm run build` first. The tests stub the API.

## Deploys today

- `scripts/deploy.sh <staging|prod> [tag]` is run by hand from a developer's laptop with the
  long-lived AWS keys above. It builds the image on the laptop, pushes it to ECR, registers a
  task definition, updates the ECS service and then runs the migrations.
- AWS account `123456789012`, region `eu-west-1`. ECR repository `orders-api` (tags are
  mutable). ECS clusters `orders-staging` and `orders-prod`, each with service `orders-api`.
  The deployment circuit breaker is off on both services.
- GitHub OIDC is already set up in the account: the identity provider for
  `token.actions.githubusercontent.com` exists, and so do two roles:
  `arn:aws:iam::123456789012:role/gha-deploy-staging` (trusts
  `repo:acme/orders-platform:environment:staging`) and
  `arn:aws:iam::123456789012:role/gha-deploy-prod` (trusts
  `repo:acme/orders-platform:environment:production`). Both may push to ECR, register task
  definitions, update their cluster's service and read their environment's database secret.
- The migration runner needs `DATABASE_URL`. It is stored in AWS Secrets Manager as
  `orders/staging/database-url` and `orders/prod/database-url`.
- Migration policy: every migration works with the previous release's code (add first; drop a
  column only in a later release, once no running code reads it).
- Incident 2026-11-03: release `2026.11.3` added `orders.notes`, and the code reading it
  shipped in the same deploy. Because `deploy.sh` runs migrations after updating the service,
  the new tasks returned `column "notes" does not exist` for about 4 minutes.
- `GET /healthz` returns 200 and the deployed git SHA. The CloudWatch alarm
  `orders-api-prod-5xx-rate` fires when more than 1% of production responses are 5xx over 5
  minutes.
- Rollback today: `scripts/deploy.sh prod <old-tag>` on a laptop, which rebuilds the old tag
  from that laptop's checkout.

## Web previews

Designers want a preview URL of `web/` for every pull request. The Vercel project exists and
the token and ids above are in place.
