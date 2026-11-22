# Production Templates, Case Studies, and Refactoring Runbooks

Internal method ID: `andino-agent-document-authoring` resource: `agent-document-templates-and-runbooks.md`.

---

## 1. Production Templates

### Template 1: Passive Root Guidance (`CLAUDE.md` / `AGENTS.md`)
*Ceiling: Strictly under 60 lines. Loaded on every single conversation turn. Contains zero cached environment data.*

```markdown
# Project Operational Invariants

## 1. Floor Invariants
- Code architecture: Flat module structure under `src/`; max file length 250 lines.
- Testing standard: Vitest with strict TDD. Tests must go red before green.
- Git workflow: Clean porcelain status required before commit; zero uncommitted artifacts.

## 2. Context Pointers
- Database migrations: [`docs/db.md`](docs/db.md). Read only when modifying Prisma/SQL schemas.
- Deployment runbook: [`docs/deploy.md`](docs/deploy.md). Read only during release or staging setup.
- API contract definitions: [`docs/api-specs.md`](docs/api-specs.md). Read only when modifying public endpoints.

## 3. Tool Invariants
- Prefix all shell executions with `rtk` where applicable.
- Inspect `package.json` for live command definitions; do not assume default script names.
```

---

### Template 2: Disclosed Context Pointer Resource (`resources/*.md`)
*Ceiling: Under 120 lines. Loaded only when pointer fires. Contains flat peer reference or deep operational matrices.*

```markdown
# [Domain Name] Operational Reference

Internal resource pointer target for `[parent-skill]`.

## 1. Domain Constraints & Invariants
- Invariant 1: [Specific, non-debatable constraint with observable criterion].
- Invariant 2: [Specific, non-debatable constraint with observable criterion].

## 2. Operational Matrix / Decision Table

| Input Condition | Operational Action | Expected Observable Signal |
| :--- | :--- | :--- |
| Condition A | Action A | Exit code 0, specific JSON schema valid |
| Condition B | Action B | Exact error code thrown with payload |

## 3. Demanding Verification Bounds
- Done only when: [Observable binary predicate 1].
- Done only when: [Observable binary predicate 2].
```

---

### Template 3: Router Skill (Cognitive Load Index)
*Purpose: Dispatches multiple tools or runbooks without loading their bodies into active context.*

```markdown
---
name: project-workflow-router
description: Use when determining which specialized operational guide or skill to invoke for a project task.
---

# Workflow Routing Matrix

Inspect the active task objective against this routing table. Load only the specific target required; do not load sibling documents.

| Task Need | Dispatch Target | Exclusion / Do Not Load If |
| :--- | :--- | :--- |
| Database schema modification or rollback | `docs/db-migrations.md` | Purely frontend or in-memory changes |
| API endpoint modification or contract audit | `docs/api-contracts.md` | Internal unit tests with no route changes |
| Production release or container build | `docs/production-release.md` | Local development or test runner debugging |
```

---

## 2. Worked Case Study: Monolithic vs. Stratified Guide

### The Failure Mode: Monolithic, Negated, and Cached (Before)

```markdown
<!-- BEFORE: Sprawl, environment caching, negation trap, fuzzy bounds, no-ops -->
# Deployment Guide
Please be thorough and do a great job deploying the app.
DO NOT deploy if tests are failing. DO NOT deploy on Fridays unless authorized.
Never forget to check environment variables.
To run tests, type `npm test`. To check git status, type `git status`.
Steps:
1. Understand the code and make sure everything looks good.
2. Run the tests.
3. If this is a Docker build, install Alpine Linux, configure multi-stage builds, expose port 3000, copy package.json... (40 lines of inlined Docker config).
4. Deploy the build to production.
5. Make sure the deployment works properly and check logs.
```

### Flaws Diagnosed:
1. **No-ops:** *"Please be thorough"* and *"do a great job"* spend tokens with zero behavioral leverage.
2. **Negation trap:** Multiple bans (*"DO NOT deploy"*, *"Never forget"*) drag failure states into context.
3. **Environment caching:** Explaining `npm test` and `git status` repeats what the environment already tells the model.
4. **Sprawl & Hierarchy collapse:** 40 lines of Docker instructions buried the main deployment flow for standard releases.
5. **Fuzzy bounds:** *"Make sure everything looks good"* and *"check if deployment works properly"* trigger premature completion.

---

### The Elevated Artifact: Stratified, Demanding, and Pruned (After)

```markdown
<!-- AFTER: Positive steering, demanding bounds, progressive disclosure, zero no-ops -->
# Production Release Procedure

Ordered execution sequence for application deployment.

## Procedure

1. Verify test suite: run `npm test`. Done when test runner exits code 0 with 0 failing assertions.
2. Inspect working tree: ensure working directory is clean. Done when `git status --porcelain` emits 0 output lines.
3. Build release artifact:
   - For standard Node targets: execute `npm run build`. Done when `dist/server.js` exists.
   - For containerized targets: consult [`docker-build.md`](resources/docker-build.md). Read only when building container targets.
4. Execute deployment: trigger production pipeline via `npm run deploy:prod`. Done when stdout confirms deployment ID and HTTP health probe `curl -f http://localhost:8080/health` returns 200 OK.
```

---

## 3. The 5-Minute Refactoring Runbook

Follow these 5 sequential passes when refactoring any legacy agent document:

1. **Pass 1 — Strip Environment Caching:** Grep for command explanations, directory layouts, and CLI flag documentation easily discovered via `--help` or `package.json`. Delete them.
2. **Pass 2 — Sentence-by-Sentence No-Op Purge:** Audit every sentence against the model-relative default test. Delete generic pleasantries (*"be thorough"*, *"think carefully"*, *"write clean code"*).
3. **Pass 3 — Positive Target Steering:** Identify every prohibition (*"do not"*, *"never"*). Rewrite it into the required positive target action.
4. **Pass 4 — Disclose Branch References:** Extract multi-line edge-case branches and platform-specific variations into separate files under `resources/`. Replace them with precision context pointers.
5. **Pass 5 — Attach Demanding Observable Bounds:** Replace every subjective termination phrase (*"ensure it works"*) with an observable binary predicate (exit code 0, file existence, schema assertion).
