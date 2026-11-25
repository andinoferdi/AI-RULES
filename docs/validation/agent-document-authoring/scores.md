# Scores

## Task 1 (AGENTS.md)

| ID | A | B | C |
|---|---|---|---|
| D1 | 2 - A/task1/AGENTS.md: layout and command list gone, "Commands are in the `Makefile`" | 2 - B: "The `Makefile` is the live command list"; one intro line | 1 - C: kept "`make lint`, `make fmt`, `make test`." and a layout line |
| D2 | 2 - once: "Run `make lint` and `make test` before pushing" | 2 - once under "Before you push" | 2 - once in the intro paragraph |
| D3 | 2 - docs/backfill.md, pointer "Backfills: `docs/backfill.md`" | 2 - docs/backfill.md, "Read docs/backfill.md before running or changing a backfill" | 2 - docs/backfill.md, "Running or planning a backfill: read" |
| D4 | 2 - "Point jobs at the dev or staging warehouse... production runs only from the scheduler" | 2 - "Run jobs from a laptop against the dev or staging warehouse only"; `.env` untracked | 2 - "Laptops point at dev or staging; the production warehouse is off limits"; `.env` stays uncommitted |
| D5 | 2 - "done when both exit 0" (lint, test) | 2 - "Done when make lint and make test both exit 0", plus dbt-build exit 0 for model work | 0 - no completion criterion in AGENTS.md; "Run lint and test before pushing" only (audit says the sentence was removed, nothing put in place) |
| D6 | 2 - opening deleted | 2 - deleted | 2 - deleted |
| D7 | 1 - front-loaded but "Schema, model, table, migration or DDL changes" synonyms remain | 1 - heading "Models, schemas, tables, migrations, DDL" synonyms remain | 1 - "Touching a schema, model, table, migration or DDL" synonyms remain |
| D8 | 2 - AUDIT row 2: flake8 stale, Makefile runs ruff; now `make lint` | 2 - AUDIT: "prose said flake8; Makefile uses ruff" | 2 - AUDIT: "Makefile uses ruff. Replaced by make lint" |
| D9 | 2 - timeout removed, "the job timeout are in config/jobs.yaml" | 2 - "that file is the single source" | 2 - "The job timeout lives in config/jobs.yaml" |
| D10 | 2 - rule in Gotchas and docs/backfill.md; misc pointer dropped | 2 - rule in AGENTS.md Backfills section and backfill.md; misc pointer dropped | 2 - rule in AGENTS.md and backfill.md; misc pointer dropped |
| D11 | 2 - Gotchas: "staging warehouse is wiped Sundays 00:00 UTC" | 2 - "Staging" section | 2 - "Staging" section |

Task 1 totals: A 21, B 21, C 18.

## Task 2 (release-notes skill)

| ID | A | B | C |
|---|---|---|---|
| S1 | 2 - `disable-model-invocation: true` with reason in DECISIONS | 2 - same flag, reason in DECISIONS | 2 - same flag, reason in DECISIONS |
| S2 | 2 - "Draft release notes from git history since the last tag. Run by the release manager at release time." | 2 - "Use when cutting a release and drafting its release notes or changelog..." (one mild pair) | 2 - "Draft RELEASE_NOTES.md from git history since the last tag." |
| S3 | 2 - changesets.md, "If `.changeset/` exists, follow [changesets]" | 2 - resources/changesets.md with conditional pointer | 2 - CHANGESETS.md with conditional pointer |
| S4 | 2 - "every commit since the tag appears in exactly one group" | 2 - same, plus highlights appear in groups | 2 - same |
| S5 | 2 - 6 short steps, no padding | 2 - 6 steps, one intro line | 2 - 5 steps |

Task 2 totals: A 10, B 10, C 10.

## Output quality (both tasks)

| ID | A | B | C |
|---|---|---|---|
| Q1 | 2 - AUDIT table with Location, Finding, Fix | 2 - findings name file/section and fix | 2 - findings name source, problem and fix |
| Q2 | 2 - "no-op claims are hypotheses" | 2 - "Not verified" section, hedged | 2 - no behavioural overclaims made |
| Q3 | 2 - plain rewritten files | 2 - plain | 2 - plain |
| Q4 | 2 - 27 vs 78 lines | 2 - 31 vs 78 lines | 2 - 24 vs 78 lines |
| Q5 | 2 - ledger accounts for every rule | 2 - rules kept, removals justified | 2 - rules kept (announce start/end, dry-run, rate, pool) |

Quality totals: A 10, B 10, C 10.

## Overall: A 41, B 41, C 38

## Most decisive differences
1. D5: C's AGENTS.md has no checkable completion criterion (A and B state "exit 0" conditions; B also for dbt-build).
2. D1: C kept the Makefile command list and layout line; A and B reduced to a Makefile pointer.
3. Everything else ties; Task 2 and quality were identical, and D7 is 1 for all (synonym triggers remain).
