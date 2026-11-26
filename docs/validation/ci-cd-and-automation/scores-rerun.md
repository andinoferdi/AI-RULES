# Scores (re-run)

Blind grading of the re-run, 2026-11-26. Letters: A candidate with the Q3 fix (r4, skill at b6f4b2f), B Addy (r1), C current skill (r2); the grader saw letters only. Grader: a fresh Sonnet 5.5 subagent at medium effort with the rubric, the fixture and the three output folders. The B and C outputs are the same files graded in [scores.md](scores.md).


Method note: Python `yaml` is not installed, so no YAML parse was run. Workflow files were read in full by eye (events, needs, if:, expressions). `bash -n` was not run by me. Scripts were read.

## Task 1

| ID | A | B | C |
| --- | --- | --- | --- |
| C1 | 2 - ci.yml job `build` kept; "Name unchanged: the ruleset and the status dashboard read `build`" | 2 - job `build` kept; DESIGN: ruleset requires it and dashboard reads it, no change needed | 2 - `name: build` kept; DESIGN names ruleset and dashboard as readers |
| C2 | 2 - `merge_group` trigger; classifier uses merge_group base/head SHAs, errors run everything | 2 - `merge_group` added; `changes` sets code=true for any non-pull_request event (full run) | 2 - `merge_group` added; classifier handles merge_group SHAs, unknown means run all |
| C3 | 2 - no paths filter; `build` `if: always()`, fails on changes failure or any non-success unless skipped and docs_only=true | 2 - same pattern, skip accepted only when code=="false"; changes must be success | 2 - same pattern, skip accepted only when docs_only=="true" |
| C4 | 2 - continue-on-error removed; fixed 2 visible errors, says remaining 12 must be fixed in same PR before merge, no rule disabling | 2 - removed; fixed 2, "land a lint-fix PR first (run lint locally), then this workflow" | 2 - removed; fixed 2, "remaining 12 must be fixed before this lands" (fix first or same PR) |
| C5 | 2 - lint/typecheck/test/test:integration/db:migrate/build/e2e all exist; `npm ci`; `node-version-file: .nvmrc` | 2 - same, real scripts, npm ci, .nvmrc | 2 - same |
| C6 | 2 - `cache: npm`, six parallel jobs, e2e skipped on docs-only, concurrency cancels only on pull_request | 2 - same three | 2 - same three (group includes event name) |
| C7 | 2 - postgres:16 with pg_isready health options, db:migrate before tests, `ci-only` password scoped to job | 2 - health check, migrate, password `postgres` for service container | 2 - health check, migrate, throwaway password stated in a comment |
| C8 | 2 - top `contents: read`, timeouts on all jobs, first-party actions on major tags, follow-up says pin non-actions to SHAs | 1 - top `contents: read` (widened for `changes`), timeouts, but DESIGN states no pinning policy ("Actions moved from v3 to v4" only) | 2 - top `contents: read`, timeouts, "Actions are pinned to major tags @v4; SHA pinning is a follow-up" |
| C9 | 2 - label.yml: base checkout, no npm ci, `github.token`, LABELER_PAT dropped and to be revoked, 2026-12-02 noted | 2 - sparse checkout of base script only, `github.token`, PAT revoke, 2026-12-02 noted | 2 - base checkout, no PR code, GITHUB_TOKEN, PAT revoke, 2026-12-02 noted |
| C10 | 2 - upload-artifact `if: failure()`, `retention-days: 7` | 2 - same | 2 - same |
| C11 | 2 - names failing lint, docs-only, mixed, merge_group and push-to-main `build`; "none of the workflow executed", NOT VERIFIED list | 2 - lists code PR, lint break blocks, docs-only, merge queue, fork PR; "Not run" | 2 - lists code PR, lint break, docs-only, mixed, merge queue, fork; "Not run here" |

Task 1 totals: A 22, B 21, C 22

## Task 2

| ID | A | B | C |
| --- | --- | --- | --- |
| F1 | 2 - table of 5121/1 (9f3c2e1), 5133/1 (4ab81d0), 5121/2 with assertions; "same commit fails and passes with no code change" (first failing step only implicit) | 1 - runs and assertions and re-run point cited, but no commits and first failing step not named | 2 - runs, commits, "First failing step: npm run test:integration", assertions, "a plain re-run" |
| F2 | 2 - w1 seed in beforeAll vs w2 TRUNCATE in beforeEach with timestamps; passing attempt shows no overlap | 2 - same mechanism, timestamps per run, passing attempt 11:09:41.900-42.034 | 2 - same, timestamps, passing attempt shows no overlap |
| F3 | 2 - wait-for-db retries also in passing attempt and in all runs, ruled out | 2 - names "no response"/"rejecting connections" as pre-migration, always ends accepting; not startup (does not say it appears in the passing attempt) | 1 - says DB not starting and wait-for-db succeeded, earlier steps identical in the passing attempt, but does not name the retry lines |
| F4 | 2 - loop of 30 before/after plus a negative control | 2 - loop 30-50 before, 50 after, expected counts | 2 - loop of 30 before, 30 of 30 after |
| F5 | 2 - rejects retry: beforeAll does not re-run, hides regressions | 2 - rejects retry with reason (fixture in beforeAll not re-run) | 2 - rejects retry as a quarantine with no exit condition, with reasons |
| F6 | 2 - each file owns its rows, TRUNCATE removed, parallelism kept (in tests) | 2 - `fileParallelism: false` for integration config, trade-off (a few hundred ms) stated | 2 - `fileParallelism: false`, cost about 4.5 s run stated |

Task 2 totals: A 12, B 11, C 11

## Task 3

| ID | A | B | C |
| --- | --- | --- | --- |
| D1 | 2 - built once in staging job tagged `$GITHUB_SHA`, digest passed to prod, rollback looks up digest, no rebuild; ECR immutability follow-up | 2 - `sha-<sha>` image once, digest resolved, same image to prod, rollback no rebuild; immutability recommended | 2 - tag = SHA, digest passed from staging to prod; immutability recommended |
| D2 | 2 - OIDC per environment; delete secrets and IAM user after a clean release | 2 - OIDC roles per environment; delete secrets and deactivate IAM keys | 2 - OIDC; delete two secrets and IAM admin user |
| D3 | 2 - staging on push main; production `needs: staging`, environment `production`, main only, digest from staging | 2 - workflow_run after CI success on main; production needs staging, environment production | 2 - workflow_run after CI on main; production needs staging (skipped with it on docs-only), environment production |
| D4 | 2 - migrate.sh before deploy.sh, cites 2026-11-03, "rollback redeploys code and never reverts the schema" | 2 - migrations before update-service, cites incident, "Migrations are never reversed" | 2 - migrate before service update, cites incident, never reverted |
| D5 | 2 - rollback.yml dispatch, SHA via env, 40-hex check, environment input (production gated), plus circuit breaker and auto restore | 2 - dispatch via reusable workflow, SHA via env and validated, production environment, circuit breaker, auto restore | 2 - dispatch, inputs via env, validated, production environment, auto restore in script |
| D6 | 2 - `if: head.repo.full_name == github.repository`, reason stated, no pull_request_target | 2 - same condition, reason stated | 2 - same condition plus dependabot skip, reason stated |
| D7 | 2 - smoke.sh /healthz with SHA after both, watch.sh on `orders-api-prod-5xx-rate` 10 min, failure restores previous task def | 2 - /healthz SHA check (skipped with warning if API_URL unset), 10 min bake on alarm, failure restores previous | 2 - /healthz SHA check, 6 min alarm bake in prod, failure restores previous |
| D8 | 2 - `deploy-staging`/`deploy-production`, cancel-in-progress false | 2 - same groups, false | 2 - same groups, false |

Task 3 totals: A 16, B 16, C 16

## Quality

| ID | A | B | C |
| --- | --- | --- | --- |
| Q1 | 2 - no syntax or expression error found by eye (action major versions v6/v7 unverifiable) | 2 - none found; reusable workflow, `vars` in step if, concurrency on uses-job all valid | 2 - none found |
| Q2 | 2 - "What changes for people and systems" in task 1 and 3 (fork, docs-only, ruleset, dashboard; devs, approvers, designers) | 2 - both sections incl. on-call rollback | 2 - both sections |
| Q3 | 2 - nothing extra | 2 - nothing extra | 2 - nothing extra |
| Q4 | 1 - estimates marked; but "checked 2026-11-26 in the guidance I follow" and "from the guidance I follow" refer to guidance and imply a check | 2 - estimates marked "not yet measured", unverified Vercel pin admitted | 2 - estimates marked, placeholders flagged |

Quality totals: A 7, B 8, C 8

## Totals

| Group | A | B | C |
| --- | --- | --- | --- |
| Task 1 (of 22) | 22 | 21 | 22 |
| Task 2 (of 12) | 12 | 11 | 11 |
| Task 3 (of 16) | 16 | 16 | 16 |
| Quality (of 8) | 7 | 8 | 8 |
| Total (of 58) | 57 | 56 | 57 |

## Unsure

- C4: all three fixed 2 of 14 errors and made fixing the other 12 a precondition; I scored 2 for all because the sequencing is stated. A stricter reader could give 1.
- F1 (B): scored 1 for missing commits and first failing step; leniently could be 2.
- F3 (C, B): C does not name the retry lines (1); B does not say they appear in the passing attempt (2, lenient).
- C8 (B): 1 only because no pinning policy is stated; the workflow itself is equal to the others.
- Q1: no YAML parser available; action versions (checkout v7, cache v6) in A could not be checked.
- Q4 (A): 1 for the mention of "guidance" with an implied check; the content is otherwise honest.
