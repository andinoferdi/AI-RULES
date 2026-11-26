# Comparison rubric: CI/CD and automation

Frozen on 2026-11-26 before any change to the candidate skill. Three arms run the same prompt
on the same fixture: Addy Osmani's `ci-cd-and-automation` (addyosmani/agent-skills commit
a057815), the current `andino-ci-cd-and-automation` (AI-RULES main at 49ad00b) and the
candidate rewrite. A grader who sees only this rubric, the fixture and the three outputs
(labelled A, B, C) scores every criterion.

The GitHub behaviour the rubric relies on was checked in GitHub's documentation (github/docs) on
2026-11-26: a workflow skipped by `paths`, `paths-ignore` or branch filters leaves its required
checks "Pending" and blocks the merge; a job skipped by an `if:` condition reports "Success"
even when it is a required check; a merge queue needs the `merge_group` event on the workflow
that reports a required check; `pull_request_target` runs with secrets and a write token, and
checking out and running the pull request's code in it is a "pwn request".

## Run setup

Each arm gets its own run folder with a copy of `fixture/repo/` at `<RUN_DIR>/repo/` and its
own copy of the skill folder at `<SKILL_DIR>`. Runners use no other skill, slash command or
subagent, read nothing outside `<SKILL_DIR>` and `<RUN_DIR>`, install nothing and use no
network.

Run prompt, identical for every arm (`<SKILL_DIR>` and `<RUN_DIR>` substituted):

> Read `<SKILL_DIR>/SKILL.md` first and follow it, opening any file it points you to when its
> condition applies. The repository in `<RUN_DIR>/repo/` is described in `repo/SYSTEM.md`;
> read it and the files it mentions before you change anything.
> Task 1: CI takes about 22 minutes, a failing lint does not block merges, and docs-only pull
> requests wait for the full suite. Rework the CI.
> Task 2: the integration tests fail intermittently on `main`. The team lead wants to add
> `retry: 3` to the integration test config and move on. The logs of the latest runs are in
> `repo/ci-logs/`. Find out what is going on and propose the fix.
> Task 3: deploys are run by hand from a laptop with `scripts/deploy.sh`. Automate deployment:
> a preview of the web app for each pull request, staging on every merge to `main`, then
> production, and a way to roll back.
> Write everything under `<RUN_DIR>/out/`. Task 1: `out/task1/DESIGN.md` and every new or
> changed file at its repository path under `out/task1/` (for example
> `out/task1/.github/workflows/ci.yml`). Task 2: `out/task2/TRIAGE.md` and every changed file
> at its repository path under `out/task2/`. Task 3: `out/task3/DESIGN.md` and every new or
> changed file at its repository path under `out/task3/`. Each DESIGN.md or TRIAGE.md says what
> you decided and why, what changes for the people and systems that depend on CI or deploys,
> and how you verified it or would verify it. You cannot install packages or reach the network.
> Do not mention which guidance you used. Touch nothing outside `<RUN_DIR>`.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote). Score what the
output says or does; a criterion the output never addresses scores 0 unless the row says
otherwise. Where a row names a GitHub expression or key, an equivalent construct that has the
same effect scores the same.

### Task 1: CI pipeline

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| C1 | Required check identity | A check named exactly `build` is still reported by the reworked CI, and the design says why the name stays (the ruleset and the status dashboard read it); or the name changes with both names reported until the ruleset and dashboard are switched | `build` kept without saying why, or the rename plan misses the dashboard | `build` no longer reported (renamed, split into jobs with other names, or moved to a workflow that can be skipped) with no transition |
| C2 | Merge queue | The workflow that reports `build` runs on `merge_group`, and on `merge_group` (and on `push` to `main`) the required work runs in full or the change classification is shown to work for that event | `merge_group` added, but docs-only classification would also skip work on `merge_group` with no handling stated | No `merge_group` trigger |
| C3 | Docs-only skip that cannot pass a failure | Docs-only pull requests skip the heavy jobs without leaving `build` pending and without letting a failure through: no `paths`/`paths-ignore` on the workflow that reports `build`; a classification job decides; the job named `build` runs with `if: always()` (or equivalent) and fails when any needed job failed or was cancelled, accepting a skip only when the classification said docs-only | The skip happens inside the workflow, but `build` can report success after a failed or cancelled needed job (for example `needs` without `always()`, so the skipped `build` reports "Success"), or a classification error passes | `paths-ignore`/`paths` on the required workflow, or no docs-only handling |
| C4 | Lint blocks, without breaking `main` | Lint becomes blocking (`continue-on-error` removed) and the 14 existing lint errors are handled so `main` does not go red: fixed in the same change, or the switch is sequenced after a fix | Lint made blocking with no word on the 14 errors | Lint still non-blocking, or another gate made non-blocking |
| C5 | Real commands and runtime | Steps call the scripts that exist in `package.json` (no invented script such as `format:check`), use `npm ci`, and take Node from `.nvmrc` (`node-version-file`) or 22, not 18 | One slip (an invented script, `npm install`, or a Node version that is not 22) | Two or more |
| C6 | Speed | All three: npm cache keyed by the lockfile (`setup-node` `cache: npm` or `actions/cache` on the npm cache, not `node_modules`); independent gates in parallel jobs with e2e off the docs-only path; a `concurrency` group that cancels superseded pull request runs but not runs on `main` or `merge_group` | Two of the three | One or none, or `concurrency` that cancels `main` or `merge_group` runs |
| C7 | Integration database | Postgres 16 service with a health check (`pg_isready` options) or an explicit wait, migrations before integration tests, and credentials that are either disposable values scoped to the service container or a secret; no production or shared credential | Postgres present but one of: no readiness handling, no migration step | Integration tests dropped, pointed at a shared or production database, or given a real credential |
| C8 | Token and action hygiene | All three: `permissions:` set to read-only at the top (`contents: read`) and widened only per job where needed; third-party actions pinned to a full commit SHA, first-party at least to a major tag, with the policy stated; `timeout-minutes` on jobs | Two of the three | One or none |
| C9 | The `pull_request_target` workflow | `label.yml` is identified as running fork code with secrets (`pull_request_target` + checkout of the head SHA + `npm ci`/`node`) and fixed so no fork code runs with secrets or a write token: switched to a labeler that does not check out or run PR code, or moved to `pull_request` with a read token; `LABELER_PAT` dropped or justified; the 2026-12-02 enforcement noted or not | Flagged, but the fix still runs PR code with a secret or a write token, or fixed without saying why | Not noticed or left as is |
| C10 | Failure artifacts | The Playwright report (and traces) uploaded when the e2e job fails (`if: failure()` or `!cancelled()`) with a retention period | Uploaded, but always or with no retention, or only mentioned in DESIGN.md | Not addressed |
| C11 | Verification and honesty | DESIGN.md names concrete checks: a passing code PR, a deliberately failing gate that makes `build` fail and blocks the merge, a docs-only PR whose `build` passes, a `merge_group` run, and what a docs-only PR to `main` reports; and it states that none of this was run on GitHub (not verified) and what local check, if any, was run | Checks named in general terms, or no statement of what was not verified | Claims the CI works or passes without having run it, or no verification at all |

### Task 2: intermittent integration failures

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| F1 | Evidence first | TRIAGE.md cites the runs and attempts (5121/1, 5121/2, 5133/1), the commits, the first failing step and the failing assertions, and says the passing re-run at the same commit does not show a fix | Cites the failure but misses the re-run point or the run identities | No log evidence cited |
| F2 | Supported cause | Names the mechanism with log evidence: both integration files run at the same time in different workers (`w1`, `w2`) against one database, and `customers.int.test.ts` runs `TRUNCATE customers, orders` in `beforeEach` between `orders.int.test.ts` seeding in `beforeAll` and its reads; the timestamps show the interleaving, and the passing attempt shows the files not overlapping | "Shared state" or "test order" named without tying it to the log lines, or the right cause listed as one of several equal guesses | Blames database readiness, the network, the runner or "flakiness" without a cause |
| F3 | Red herring | The `no response` / `rejecting connections` retries before migrate are explained as normal start-up handled by `wait-for-db.sh` (they also appear in the passing attempt) and not the cause | Not mentioned, and not blamed | Blamed as the cause or as an equal cause |
| F4 | Reproduction | A targeted local reproduction that should fail before the fix (for example both files run together with file parallelism, repeated N times, or a forced interleaving) and pass after it, with the repeat count stated | A reproduction without a count or without the before/after pair | None |
| F5 | No masking | Rejects `retry: 3`, re-running until green and `.skip` as the fix, with the reason; a retry or quarantine is allowed only as a temporary, tracked step with an exit condition while the cause is fixed | Rejects masking without a reason, or allows retries without an exit condition | Adopts the retry as the fix |
| F6 | Fix at the cause | Isolates the test data: per-worker database or schema (for example from `VITEST_POOL_ID`), transactions rolled back per test, data scoped per file instead of `TRUNCATE` of shared tables, or `fileParallelism: false` for the integration config with the trade-off stated; the change is in the tests or the integration config | A fix that works but is broader than needed (for example serialising all tests including unit) or leaves one file able to wipe the other's rows | No fix, or a fix that does not address the shared database |

### Task 3: deployment

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| D1 | Build once, promote | One image built in CI per commit, tagged by commit SHA (and referenced by digest, or ECR tags made immutable), and the same image deployed to staging and then production; no rebuild for production or for rollback | Built once, but tags stay mutable with no digest, or rollback rebuilds | Each environment builds its own image |
| D2 | Credentials | GitHub OIDC (`id-token: write`, assume `gha-deploy-staging` / `gha-deploy-prod` per environment) replaces the long-lived AWS keys, and the design says to delete those keys and the IAM user | OIDC used, but the old keys are kept with no plan | Long-lived keys still used for deploys |
| D3 | Production gate | Staging deploys automatically on merge to `main`; production deploys the image that passed staging, only from `main`, through a GitHub environment `production` with required reviewers (or an equivalent approval) | Production gated, but it can deploy an image that did not pass staging or from another branch | Production deploys automatically with no gate, or there is no production path |
| D4 | Migrations | Migrations run before the new task definition is rolled out (a pre-deploy step or one-off task), under the expand-first policy, citing the 2026-11-03 incident; the design says a rollback of code does not roll back migrations | Migrations before the deploy, but rollback interaction not covered | Migrations still after the service update, or not run |
| D5 | Rollback | A rollback path that redeploys a previous known-good image (by SHA or digest) without rebuilding: a `workflow_dispatch` workflow that passes the input through `env:` (never `${{ inputs.* }}` inside `run:`), validates it, and runs under the `production` environment; or automatic rollback on failure (ECS circuit breaker with rollback or the `orders-api-prod-5xx-rate` alarm) with the manual path as backup | A rollback path with one gap: interpolates the input into `run:`, rebuilds, or bypasses the production gate | No rollback path |
| D6 | Fork-safe previews | The web preview deploy that needs `VERCEL_TOKEN` never runs fork code with the token: skipped for fork pull requests (with the reason stated), or run through a path that does not execute fork code with secrets | Previews deploy, but fork handling is only mentioned or unclear | Fork pull requests run the preview with the token (for example through `pull_request_target` checking out the head) |
| D7 | Post-deploy checks | Smoke check of `/healthz` (including the deployed SHA) after staging and production, a watch window tied to the `orders-api-prod-5xx-rate` alarm, and what triggers a rollback | Smoke check only, or watch window without a rollback trigger | None |
| D8 | Deploy concurrency | Deploys to one environment are serialised with a `concurrency` group per environment that does not cancel a deploy in progress (`cancel-in-progress: false`) | A `concurrency` group that cancels in-progress deploys, or one shared group with no reason | None |

### All tasks: output quality

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Valid workflow files | Every workflow file is valid YAML and valid GitHub Actions syntax (events, `needs`, expressions, `if:` conditions, service options); the grader reads each file and runs a YAML parser when one is available | One syntax or expression error | Two or more, or a workflow that could not run |
| Q2 | Impact on people and systems | The DESIGN.md files list what changes for fork contributors, docs-only authors, the ruleset and the status dashboard (task 1) and for whoever deploys and is on call (task 3) | Covered for one task | Absent |
| Q3 | Proportion | Nothing beyond the repository's needs: no OS or Node version matrix for an app pinned to Node 22, no self-hosted runners, no new platform (Kubernetes, another CI service) or paid tool unless the design gives a reason tied to the fixture | One unneeded addition | Several |
| Q4 | Honesty and register | Plain words; assumptions and unknowns marked; durations and savings given as estimates with their basis; no invented measurements or claims that something was run | Some jargon or one unmarked assumption | Invented metrics or claimed runs |

Maximum: 29 criteria, 58 points.

## Gate

The candidate passes when its score is at least Addy's on every criterion and at least the
current skill's on every criterion. With one run per arm a one-point difference can be noise;
the trial record says so.
