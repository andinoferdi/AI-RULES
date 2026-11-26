# Scores

Blind grading of the first run, 2026-11-26. Letters: A current skill (r2), B candidate (r3), C Addy (r1); the grader saw letters only. Grader: one Sonnet 5.5 subagent at medium effort with the rubric, the fixture and the three output folders.


Read-only checks run: `bash -n` on every task3 script (all pass). No YAML parser available (`import yaml` fails), so workflows were read by eye.

## Task 1

| ID | A | B | C |
| --- | --- | --- | --- |
| C1 | 2 - aggregate job `name: build`, DESIGN: ruleset, merge queue and dashboard read `build` | 2 - `build` aggregate, comment and DESIGN table name ruleset and dashboard | 2 - `build` aggregate, DESIGN says ruleset requires it and dashboard reads it |
| C2 | 2 - `merge_group` trigger; classifier uses merge_group base/head shas (works for that event) | 2 - `merge_group`; BASE/HEAD fall back to merge_group shas | 2 - `merge_group`; non-PR events always `code=true` (full run) |
| C3 | 2 - no paths filter; `changes`; `build` `if: always()`, fails on failed/cancelled, skip only if docs_only, classifier failure fails build | 2 - same pattern; checks/integration/e2e judged, skipped accepted only if docs_only | 2 - same; `code=false` required to accept skip; changes must succeed |
| C4 | 2 - `continue-on-error` removed; fixed 2 errors, says other 12 must land first or in same PR | 2 - removed; fixed 2, rest "in this PR or a PR merged first" | 2 - removed; fixed 2, explicit rollout order: lint-fix PR first |
| C5 | 2 - real scripts, `npm ci`, `node-version-file: .nvmrc` | 2 - matrix of real scripts (lint, typecheck, test, build), `npm ci`, .nvmrc | 2 - real scripts, `npm ci`, .nvmrc |
| C6 | 2 - `cache: npm`, parallel jobs, e2e skipped docs-only, concurrency cancels only on pull_request | 2 - same, plus Playwright browser cache | 2 - same, plus Playwright cache |
| C7 | 2 - postgres:16, `pg_isready` health options, migrate, disposable creds | 2 - same | 2 - same |
| C8 | 2 - `contents: read`, timeouts, majors with SHA+Dependabot follow-up stated | 2 - read-only, timeouts, current majors, dependabot.yml for actions | 1 - read-only and timeouts, majors used but no pinning policy stated (only "major version tags" in task 3) |
| C9 | 2 - base checkout only, no npm ci, GITHUB_TOKEN, LABELER_PAT dropped, 2026-12-02 noted | 2 - same, permissions narrowed, date noted | 2 - sparse checkout of base script, GITHUB_TOKEN, PAT revoked, date noted |
| C10 | 2 - `if: failure()` upload playwright-report, `retention-days: 7` | 2 - failure() upload report and test-results, 7 days | 2 - failure() upload report, 7 days |
| C11 | 2 - 7 concrete checks (code PR, failing lint, docs-only, merge queue, fork); "Not run" stated | 2 - 6 concrete checks incl. cancelled run; NOT VERIFIED stated, notes none run | 2 - 7 checks; "Not run" stated |

Task 1 totals: A 22, B 22, C 21.

## Task 2

| ID | A | B | C |
| --- | --- | --- | --- |
| F1 | 2 - runs 5121/1, 5133/1, 5121/2 with commits, first failing step `test:integration`, re-run is plain re-run at same commit | 2 - table with runs, commits, failing tests; re-run at same commit passes, "re-run usually passes" because of timing | 1 - cites runs/attempts and assertions and re-run re-rolls timing, but no commits and no named first failing step |
| F2 | 2 - w1/w2, TRUNCATE in beforeEach vs beforeAll, timestamps for all three attempts | 2 - same with timestamps | 2 - same with timestamps |
| F3 | 1 - only says wait-for-db succeeded and earlier steps identical; retries not discussed | 2 - retry counts compared, passing attempt also retried | 2 - retries before migrate end with "accepting connections", ruled out |
| F4 | 2 - loop 30 times before and after (not run), count stated | 2 - 30 before and after, forced sleep to raise rate | 2 - 30-50 before and after, artificial latency |
| F5 | 2 - rejects retry as quarantine without exit condition | 2 - explains retry does not rerun beforeAll | 2 - same reasoning |
| F6 | 2 - `fileParallelism: false` for integration config, cost stated | 2 - same plus orders seeds per test with scoped DELETE | 2 - same plus orders TRUNCATE in beforeEach; per-worker alternative named |

Task 2 totals: A 11, B 12, C 11.

## Task 3

| ID | A | B | C |
| --- | --- | --- | --- |
| D1 | 2 - build once in staging, tag = full SHA, deploy by digest, production reuses digest, rollback resolves digest; immutability recommended | 2 - same | 2 - `sha-<sha>` tag built once, resolved to digest in deploy, immutability recommended, no rebuild |
| D2 | 2 - OIDC both roles, delete keys and IAM user | 2 - OIDC, delete admin key and secrets | 2 - OIDC, delete secrets and deactivate keys |
| D3 | 2 - staging auto, production `needs: staging`, `environment: production`, workflow_run on main only | 2 - same | 2 - same |
| D4 | 2 - migrate before update in ecs-deploy.sh, cites 2026-11-03, not reverted on rollback | 2 - migrate.sh before deploy.sh, incident cited, schema not reverted | 2 - migrations step before update, incident cited, not reversed |
| D5 | 2 - dispatch, inputs via env, 40-hex validation, environment production, no rebuild; auto restore too | 2 - same, `if: github.ref == main`, circuit breaker plus alarm-driven rollback | 2 - dispatch inputs only passed as `with` to reusable workflow and validated in env, production env, no rebuild |
| D6 | 2 - fork PRs skipped with reason | 2 - same | 2 - same |
| D7 | 2 - /healthz SHA, 6 min alarm bake, restore on failure | 2 - smoke.sh, 10 min watch.sh, rollback on alarm | 2 - /healthz SHA (skipped with warning if API_URL unset), 10 min bake, rollback on failure |
| D8 | 2 - per-environment groups, cancel false | 2 - same | 2 - same |

Task 3 totals: A 16, B 16, C 16.

## Quality

| ID | A | B | C |
| --- | --- | --- | --- |
| Q1 | 2 - no syntax/expression errors found by reading; `bash -n` on scripts passes | 2 - none found; action majors (v7, v6) and vercel@44 unverifiable but flagged by the output | 2 - none found; reusable workflow wiring looks valid |
| Q2 | 2 - both DESIGN files list impact on forks, docs-only, ruleset, dashboard, deployers, on-call | 2 - same | 2 - same |
| Q3 | 2 - nothing extra | 1 - adds `dependabot.yml` and web staging/promote flow beyond ask | 2 - nothing extra |
| Q4 | 2 - estimates marked "needs measuring", unknowns marked | 2 - UNKNOWN and NOT VERIFIED marked; only `bash -n` claimed (true) | 2 - "not run", estimates marked; "well under a minute" is lightly unmarked |

Quality totals: A 8, B 7, C 8.

## Totals

| Group | A | B | C |
| --- | --- | --- | --- |
| Task 1 of 22 | 22 | 22 | 21 |
| Task 2 of 12 | 11 | 12 | 11 |
| Task 3 of 16 | 16 | 16 | 16 |
| Quality of 8 | 8 | 7 | 8 |
| Total of 58 | 57 | 57 | 56 |

## Unsure

- C4 (all three): each fixed only 2 of 14 errors and states the rest must land first; scored 2 as "sequenced after a fix", but the delivered change alone would turn `main` red.
- C8 C: scored 1 because no pinning policy is stated in task 1; arguably 2 since no third-party actions exist.
- F3 A: 1 because retries are not discussed; it only says the DB wait succeeded.
- F1 C: 1 for missing commits and first failing step; cited otherwise well.
- Q1 B: action versions (checkout@v7, setup-node@v7, cache@v6, upload-artifact@v7) could not be checked; no YAML parser available.
- Q3 B: dependabot and web promote could be read as in scope.
- D5 C: rollback has no explicit main-branch guard in the workflow (relies on environment branch rule in DESIGN).
