# Elevate CI/CD and Automation to Match and Exceed Upstream Agent-Skills

Status: COMPLETED
Plan Depth: STANDARD
Current Phase: Phase 5 — Verification & Delivery Complete
Last Updated: 2026-11-01
Active Agent: Claude Code (Andino Workflow)

## Executive Snapshot

Successfully elevated `skills/ci-cd-and-automation/` on branch `andino-workflow` from an abstract, over-compressed 97-line protocol into a premier, production-grade quality automation and delivery engine. The elevated skill synthesizes the generative craft of Addy Osmani's `ci-cd-and-automation` (unbroken quality gate pipeline, copy-paste ready GitHub Actions workflows, PostgreSQL service container isolation, Playwright E2E artifact capture, feature flag lifecycles, and rationalization busters) with Andino's unique advantages: token-efficient agent error-reflection loops (distilled terminal logs, 1-cycle root-cause debugging, prevention of blind reruns), platform-agnostic quality invariants, multi-stage deployment patterns (Canary, Staged Rollout, Safe Rollback with shell-injection prevention), offline deterministic Python DAG verification, and complete integration with `ai-rules setup`.

## Objective

Deliver an upgraded, self-contained `skills/ci-cd-and-automation` bundle whose AI output quality, syntax reliability, agent reflection rigor, and deployment safety match and surpass upstream benchmarks, verified through deterministic artifact checks and ready for direct deployment via `ai-rules setup`.

## Acceptance Criteria

- [x] `skills/ci-cd-and-automation/SKILL.md` overhauled with high-density operational directives: unbroken ASCII Quality Gate Pipeline, strict fail-closed anti-skip policy, rationalization refutation table (7 common agent shortcuts), 12 diagnostic red flags, and explicit pointers to specialized resources.
- [x] `skills/ci-cd-and-automation/GUIDE.md` overhauled with deep craft chapters: universal CI/CD invariants vs platform implementations, CI optimization decision tree (<10 min threshold), environment & secret segregation matrix (.env.example vs .env.test vs secrets manager), release & deployment strategies (Preview Deployments, Feature Flag lifecycle, Staged Rollouts with 15-minute monitoring window, Safe Rollbacks), and repository governance (Dependabot, Build Cop, branch protection).
- [x] `skills/ci-cd-and-automation/resources/pipeline-templates.md` created with complete, production-ready, security-audited GitHub Actions workflows:
  - Basic CI Pipeline (Node 22, package manager cache, lint, typecheck, coverage, build, security audit)
  - Database Integration Tests (PostgreSQL 16 service container with health checks and migration deployment)
  - Playwright E2E Tests (Chromium installation and failure artifact upload)
  - PR Preview Deployments
  - Safe Parameterized Rollback Workflow (preventing shell injection via environment variable passing)
  - Dependabot / Automated Dependency Update Configuration
- [x] `skills/ci-cd-and-automation/resources/agent-feedback-loop.md` created with structured error-reflection cycles for AI coding agents:
  - Classification of CI failures: Lint, Type, Unit/Coverage, Build, Integration/DB, E2E, Security
  - Distilled log filtering for token efficiency (leveraging RTK or targeted regex to avoid context flooding)
  - Single-cycle root-cause debugging protocol (preventing blind reruns or speculative shotgun fixes)
  - Anti-hallucination guardrails (prohibiting disabling tests, skipping linters, or claiming passing status without evidence)
- [x] `skills/ci-cd-and-automation/resources/worked-example.md` created with a realistic end-to-end CI regression scenario (e.g. schema migration drift causing integration test failure), step-by-step diagnosis, and embedded runnable standard-library Python test script verifying DAG dependency stages, cascading blocker logic, and negative test toggles.
- [x] `references/legal/provenance.md` updated with comprehensive audit details and Addy Osmani MIT attribution.
- [x] Deterministic Python verification script executed and passing in temporary directory.
- [x] Upgraded skill synchronized directly to local host directory `~/.claude/skills/andino-workflow/skills/ci-cd-and-automation/`.
- [x] Git committed and pushed to `origin/andino-workflow`, verified compatible with `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run`.

## Scope

### In Scope
- `skills/ci-cd-and-automation/SKILL.md`
- `skills/ci-cd-and-automation/GUIDE.md`
- `skills/ci-cd-and-automation/resources/pipeline-templates.md`
- `skills/ci-cd-and-automation/resources/agent-feedback-loop.md`
- `skills/ci-cd-and-automation/resources/worked-example.md`
- `references/legal/provenance.md`
- Host synchronization to `~/.claude/skills/andino-workflow/`
- Verification with `ai-rules setup`

### Out of Scope
- Forcing external hosted CI runs or live deployment mutations during unit tests.
- Modifying unrelated Andino skills.
- Breaking backwards compatibility with the existing offline operational example schema.

## User Decisions / Clarifications
- **CI Platform & Ecosystem Focus (Option 1)**: GitHub Actions as first-class primary implementation with modern runtimes (Node 22, pnpm/npm, Python, PostgreSQL service containers, Playwright), paired with explicit platform-agnostic invariants so non-JS/non-GHA stacks remain fully supported.
- **Agent Error-Reflection Loop (Option 2)**: Specialized reflection protocol for CLI coding agents (Claude Code, Codex, Antigravity) with distilled log filtering (RTK) to prevent token waste and blind reruns.
- **Workflow Cadence (Option 3)**: Autonomous continuous execution authorized by user ("1. A 2. gas"): Council consultation -> Planning -> Plan Execution -> Verification -> Commit, Push, and Setup sync.

## Council Synthesis Summary

### Titik Temu (Agreement)
- Current skill is structurally sound under Andino governance but practically sterile for AI generation: it lacks the generative scaffolding, flowchart decision trees, rationalizations, and production templates that guide an LLM to generate robust pipelines.
- External deterministic verification is an anti-hallucination guardrail: fail-closed gates (Lint -> Type -> Unit -> Build -> Integration -> E2E -> Security -> Bundle) must never be bypassed.
- Separation of concerns between `SKILL.md` (dense operational contract) and `GUIDE.md` / `resources/` prevents prompt bloat while providing comprehensive guidance when invoked.

### Perbedaan & Resolusi Kritis (Disagreements & Resolutions)
1. **GitHub Actions Lock-in vs Platform Invariants:**
   - *Risk*: Hardcoding GitHub Actions syntax traps agents working on GitLab CI, Bitbucket, or Docker.
   - *Resolution*: Establish platform-agnostic quality gate invariants in `SKILL.md` and `GUIDE.md`, while providing GitHub Actions as the primary reference implementation in `resources/pipeline-templates.md` with explicit placeholder markers.
2. **Context Window Bloat vs Retrieval Blindness:**
   - *Risk*: Putting massive YAMLs in `SKILL.md` exhausts working memory; putting them in `resources/` leads to agents ignoring them.
   - *Resolution*: Keep `SKILL.md` dense and concise with high-contrast ASCII diagrams and imperative discovery directives pointing agents directly to specific `resources/` files.
3. **Flaky Test Blind Reruns vs Self-Healing:**
   - *Risk*: Agents blindly re-running failing tests or disabling them to get green status.
   - *Resolution*: Enforce a strict anti-skip policy and a 1-cycle root-cause debugging protocol in `resources/agent-feedback-loop.md`.

## Task Breakdown & Change Specifications

### Task 1: Create `skills/ci-cd-and-automation/resources/pipeline-templates.md`
- **File**: `skills/ci-cd-and-automation/resources/pipeline-templates.md`
- **Content**:
  - Production-ready GitHub Actions YAMLs:
    1. Basic CI Pipeline (checkout, setup-node 22 with npm cache, npm ci, lint, typecheck, test coverage, build, audit).
    2. Service Container Pipeline (PostgreSQL 16 with healthcheck cmd `pg_isready`, isolated DB credentials via secrets, migration execution, integration tests).
    3. Playwright E2E Pipeline (Playwright installation with chromium deps, build, test run, artifact upload `if: failure()`).
    4. PR Preview Deployment Workflow (Vercel/Netlify preview deployment via secrets token).
    5. Safe Parameterized Rollback Workflow (`workflow_dispatch`, passing inputs through environment variables to prevent shell injection, `npx vercel rollback "$VERSION"`).
    6. Automated Dependency Updates (`.github/dependabot.yml` configuration).
  - Explicit placeholder markers `<REPO_OWNER>`, `<NODE_VERSION>`, `<SECRETS_TOKEN>` to avoid hallucinated secrets.

### Task 2: Create `skills/ci-cd-and-automation/resources/agent-feedback-loop.md`
- **File**: `skills/ci-cd-and-automation/resources/agent-feedback-loop.md`
- **Content**:
  - The Agent Reflection Architecture: CI failure -> Log extraction -> Distillation (RTK / error regex) -> Targeted fix -> Local verification -> Commit.
  - Failure Classification Matrix:
    - Lint errors -> `npm run lint -- --fix`, verify remaining issues.
    - Type errors -> Read exact file and line, inspect types, resolve type contracts.
    - Unit test failures -> Invoke root-cause debugging, never change assertions without spec approval.
    - Build errors -> Inspect dependencies, bundler configurations, asset imports.
    - Integration/DB failures -> Check migration sync, service readiness, seed data.
    - E2E failures -> Download failure artifacts/traces, inspect DOM state.
    - Security audit failures -> Audit dependency vulnerabilities, upgrade specific packages or add override.
  - Strict Anti-Patterns:
    - Never blindly rerun flaky tests hoping for a lucky green.
    - Never disable a test or comment out an assertion to make CI pass.
    - Never bypass a lint rule without explicit documented project consensus.
    - Never claim CI is passing without running the command locally or receiving remote status evidence.

### Task 3: Create `skills/ci-cd-and-automation/resources/worked-example.md`
- **File**: `skills/ci-cd-and-automation/resources/worked-example.md`
- **Content**:
  - Realistic end-to-end bug scenario: A database migration alters a column name, causing backend unit tests to pass but integration tests to fail on query execution.
  - Detailed step-by-step agent troubleshooting walkthrough:
    - Phase 1: Local quality gate failure detection.
    - Phase 2: Distilling failure logs and identifying the failing DAG stage.
    - Phase 3: Root-cause remediation (updating repository query layer and migration snapshot).
    - Phase 4: Local verification replay across all quality gates.
  - Embedded runnable standard-library Python test script verifying:
    - DAG dependency resolution (lint -> unit -> build -> publish).
    - Blocker cascading when an ancestor fails.
    - Negative test support via `ANDINO_NEGATIVE=1`.
    - Deterministic JSON output sorting.

### Task 4: Overhaul `skills/ci-cd-and-automation/SKILL.md`
- **File**: `skills/ci-cd-and-automation/SKILL.md`
- **Content**:
  - Frontmatter metadata and Andino Workflow Member Skill governance.
  - Core Principles: Shift Left (early detection saves hours) and Faster is Safer (smaller batches reduce blast radius).
  - Unbroken ASCII Quality Gate Pipeline:
    `PR Opened -> LINT -> TYPE -> UNIT -> BUILD -> INTEGRATION -> E2E -> SECURITY AUDIT -> BUNDLE SIZE -> Ready for Review`.
  - Strict Rule: Zero Bypass Policy (No gate can be skipped; fix the code, don't disable the gate).
  - Explicit Resource Pointers:
    - Pipeline syntax templates: `resources/pipeline-templates.md`
    - Agent debugging reflection loop: `resources/agent-feedback-loop.md`
    - Worked scenario and deterministic test: `resources/worked-example.md`
  - Rationalization Refutation Table (7 common agent excuses vs reality).
  - 12 Diagnostic Red Flags (silent failures, hardcoded secrets, flaky reruns, missing rollbacks, etc.).
  - Embedded offline runnable Python operational example matching the test harness contract.

### Task 5: Overhaul `skills/ci-cd-and-automation/GUIDE.md`
- **File**: `skills/ci-cd-and-automation/GUIDE.md`
- **Content**:
  - Detailed craft chapters expanding on `SKILL.md`.
  - Universal Invariants vs Platform Implementations (DAG dependency execution, fail-closed boundaries, ephemeral service isolation, immutable artifacts).
  - CI Optimization Decision Tree (hierarchical steps when CI exceeds 10 minutes: cache dependencies -> parallelize -> path filter -> matrix/shard -> schedule slow tests -> runner sizing).
  - Environment & Secret Management Matrix (`.env.example` vs `.env` vs `.env.test` vs CI secrets vs production vaults).
  - Release & Deployment Strategies:
    - Preview Deployments (isolated ephemeral URLs per pull request).
    - Feature Flags Lifecycle (Create -> Test -> Canary -> Full Rollout -> Dead Code Cleanup).
    - Staged Rollouts (Staging auto-deploy -> Manual/automated smoke test -> Production deploy -> 15-minute error monitoring window).
    - Parameterized Rollbacks (Reversible releases, safe env var passing).
  - Repository Governance: Dependabot weekly updates, Build Cop rotation, branch protection rules (required reviews, required status checks, no force push).

### Task 6: Update Provenance & Legal Documentation
- **File**: `references/legal/provenance.md`
- **Action**: Add entry documenting the 2026-11-01 elevation of `ci-cd-and-automation` synthesizing Addy Osmani's agent-skills craft with Andino Workflow governance, agent feedback loops, and offline DAG dependency verification.

### Task 7: Deterministic Verification, Host Sync & Delivery
- **Actions**:
  1. Execute runnable Python operational example in temporary directory to verify default and adversarial outputs match expected JSON.
  2. Synchronize all modified files to `~/.claude/skills/andino-workflow/skills/ci-cd-and-automation/`.
  3. Run `ai-rules setup --capability andino-workflow --host claude-code --non-interactive --dry-run` to confirm 100% clean reconciliation.
  4. Git add, commit with conventional commit format, and push to `origin/andino-workflow`.
