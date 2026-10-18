# Local Superpowers audit

Source data only. Andino owns execution, permissions and lifecycle.

Snapshot: bb92a77741419a4ab5f06e711a283343f1ada0c3; tree 4ac675daa3415bc836f707c7e60237ac7b66c7d5; branch main; clean.
Tracked files: 238; skill entries: 15; bytes fingerprint: 6cfc2c2707ee5f933ba14a40ad7336b72a2b7a84b4bda690975e6d6fc5ad791c.

## Skill decisions

| Original source | Status | Disposition | Proposed internal method |
|---|---|---|---|
| brainstorming | stable | ADAPT | requirements-discovery |
| diagnosing-superpowers | stable | ADAPT | session-diagnostics |
| dispatching-parallel-agents | stable | MERGE | delegation |
| executing-plans | stable | MERGE | plan-execution |
| finishing-a-development-branch | stable | ADAPT | delivery |
| receiving-code-review | stable | MERGE | code-review |
| requesting-code-review | stable | MERGE | code-review |
| subagent-driven-development | stable | MERGE | delegation |
| systematic-debugging | stable | ADAPT | debugging |
| test-driven-development | stable | ADAPT | tdd |
| using-git-worktrees | stable | ADAPT | git-isolation |
| using-superpowers | meta | INTERNALIZE | root-contract |
| verification-before-completion | stable | MERGE | verification |
| writing-plans | stable | MERGE | planning |
| writing-skills | meta | ADAPT | method-authoring |

## Preserved techniques and conflicts

### brainstorming

Source: skills/brainstorming/SKILL.md.

- Concrete-moment open questions; goals/non-goals/anti-goals; assumptions attributed to agent vs agreed requirements
- Proportional sizing: clear request executes; small change agreed in chat; project written design
- Builder-readiness review sorts already-answered/minor/human-only questions into one pass
- Optional visual comparison and throwaway spike, with explicit persistence decision

Adaptation:
- Mandatory first-message shape and approval/restart cycle cannot replace accepted Andino plan
- No auto commit of design, no unconditional builder subagent, no upstream web server/telemetry

Resources: skills/brainstorming/builder-check-prompt.md; skills/brainstorming/scripts/frame-template.html; skills/brainstorming/scripts/helper.js; skills/brainstorming/scripts/server.cjs; skills/brainstorming/scripts/start-server.sh; skills/brainstorming/scripts/stop-server.sh; skills/brainstorming/visual-companion.md.

### diagnosing-superpowers

Source: skills/diagnosing-superpowers/SKILL.md.

- Verify transcript identity, lineage, event meanings and source provenance before accounting
- Path:line findings with confidence; request/plan/repetition/stumble/verification/token/time dimensions
- Bound transcript records before extracting fields; unknown usage is not zero
- Redact copies with stable placeholders; independent privacy and evidence-support outcomes; reconcile export after scrub

Adaptation:
- Seven unconditional analyst subagents replaced with scoped evidence-driven selection
- No blanket inability to diagnose/fix Andino; retain request-scoped investigation
- Export/archive/issue publishing retain explicit authorization; no automatic history sweep

Resources: skills/diagnosing-superpowers/prompts/analyst-common.md; skills/diagnosing-superpowers/prompts/cost-and-time.md; skills/diagnosing-superpowers/prompts/plan-adherence.md; skills/diagnosing-superpowers/prompts/quality-evidence.md; skills/diagnosing-superpowers/prompts/repeated-work.md; skills/diagnosing-superpowers/prompts/request-conflicts.md; skills/diagnosing-superpowers/prompts/scrub-audit.md; skills/diagnosing-superpowers/prompts/scrub.md; skills/diagnosing-superpowers/prompts/similar-session.md; skills/diagnosing-superpowers/prompts/skill-timeline.md; skills/diagnosing-superpowers/prompts/stumbles.md; skills/diagnosing-superpowers/references/context-safety.md; skills/diagnosing-superpowers/references/github-issues.md; skills/diagnosing-superpowers/references/redaction-policy.md; skills/diagnosing-superpowers/references/session-discovery.md; skills/diagnosing-superpowers/templates/bundle-README.md; skills/diagnosing-superpowers/templates/case.md; skills/diagnosing-superpowers/templates/issue.md; skills/diagnosing-superpowers/templates/report.md.

### dispatching-parallel-agents

Source: skills/dispatching-parallel-agents/SKILL.md.

- Partition independent problem domains; focused self-contained brief with constraints and expected return
- No concurrency for related failures/shared state; parent checks summaries, overlap and integrated suite

Adaptation:
- No automatic fan-out from failure count; Andino owns authorization, benefit, write ownership and budget

Resources: none.

### executing-plans

Source: skills/executing-plans/SKILL.md.

- Plan identity + durable evidence ledger prevents redoing completed work after compaction
- Task briefs preserve exact values/interfaces; compare every Expected line to actual command output
- Record deviation ruling with reason and cost; task completion only after named verification
- Final whole-change review and effect-based severity grading; report residual decisions

Adaptation:
- Do not establish second .superpowers ledger/router or delete durable ticket state
- No plan-implied commit, model override, cleanup, finish-branch cascade
- Source only supports committed-range review; uncommitted approved work needs actual working diff evidence

Resources: skills/executing-plans/scripts/task-done; skills/executing-plans/scripts/task-start.

### finishing-a-development-branch

Source: skills/finishing-a-development-branch/SKILL.md.

- Fresh full-suite verification; detect linked worktree vs normal/detached workspace
- Base branch evidence and preserve externally owned workspace
- Never force cleanup after untracked/modified-file refusal; explicit integration decision

Adaptation:
- No automatic merge/pull/push/new remote branch/branch deletion
- Exact menu and typed-discard rule do not supersede user scope
- Path name alone does not establish worktree ownership

Resources: none.

### receiving-code-review

Source: skills/receiving-code-review/SKILL.md.

- Read/understand/verify/evaluate/respond before implementing feedback
- Check real code usage, compatibility and architectural decisions; technical pushback with evidence
- Fix blocking then simple then complex items with covering tests; inline replies stay in thread

Adaptation:
- No blanket stop on every unclear unrelated item: continue independent work
- No publish/reply without explicit user authorization
- Style prohibitions are not technical acceptance criteria

Resources: none.

### requesting-code-review

Source: skills/requesting-code-review/SKILL.md.

- Prepare requirements + exact BASE/current diff + test evidence + scope for independent review
- Severity grades by effect; Critical/Important resolved; justified disagreement recorded
- Self-review does not silently claim independent reviewer capability

Adaptation:
- No mandatory subagent for all trivial edits; Andino owns review proportionality
- HEAD~1 example unsafe for uncommitted or multi-commit work; capture actual task BASE and working diff

Resources: skills/requesting-code-review/code-reviewer.md.

### subagent-driven-development

Source: skills/subagent-driven-development/SKILL.md.

- Scoped briefs, reports, status contract and exact review packages
- Separate spec compliance and code-quality verdicts in task review, whole-change final review
- Resume completed tasks from identity-bound ledger, check interface conflicts before dependent execution
- Bound fix loops; scoped re-review checks addressed findings/new breakage; explicit residual rulings
- Workers cannot spawn own duplicate reviewers; write ownership stays with parent

Adaptation:
- Five rounds/model tier escalation not imported over project retry/permission limits
- No unconditional explicit model override, auto commits, separate .superpowers workspace or cleanup
- Do not park material failing acceptance solely to continue at round cap

Resources: skills/subagent-driven-development/implementer-prompt.md; skills/subagent-driven-development/re-review-prompt.md; skills/subagent-driven-development/scripts/review-package; skills/subagent-driven-development/scripts/sdd-workspace; skills/subagent-driven-development/scripts/task-brief; skills/subagent-driven-development/task-reviewer-prompt.md.

### systematic-debugging

Source: skills/systematic-debugging/SKILL.md.

- Four phases: root investigation, working-pattern comparison, one hypothesis/minimal experiment, regression-tested root fix
- Trace bad values backward through call chain and component boundary evidence
- Condition-based bounded waits; test-polluter isolation; defense at meaningful validated boundaries
- After three failed fixes question architecture; document true environment/external uncertainty

Adaptation:
- No bundled unrelated refactoring or speculative symptom fix
- No secret value logging; source shell examples must be adapted safely
- find-polluter is sequential npm test, despite bisection label; spaces/glob/tool assumptions need adaptation
- Source 95% claim is anecdotal and cannot become Andino evidence

Resources: skills/systematic-debugging/CREATION-LOG.md; skills/systematic-debugging/condition-based-waiting-example.ts; skills/systematic-debugging/condition-based-waiting.md; skills/systematic-debugging/defense-in-depth.md; skills/systematic-debugging/find-polluter.sh; skills/systematic-debugging/root-cause-tracing.md; skills/systematic-debugging/test-academic.md; skills/systematic-debugging/test-pressure-1.md; skills/systematic-debugging/test-pressure-2.md; skills/systematic-debugging/test-pressure-3.md.

### test-driven-development

Source: skills/test-driven-development/SKILL.md.

- RED test for observable missing/broken behavior; observe expected assertion failure, not import/setup accident
- Minimal GREEN; rerun covering tests plus project suite; report all failures including baseline ones
- REFACTOR only after green; remove duplication/improve names/extract helpers without adding behavior
- Independent literal/hand-checked fixtures; name realistic mutation test catches; real behavior not mock/source text
- Mock slow/external layer only after understanding real side effects; complete doubles; no test-only production lifecycle methods

Adaptation:
- Do not delete pre-existing/user code under source delete/start-over rhetoric
- Permission exceptions/proportional verification follow locked project B-T02 decision
- No tautological keyword checks masquerading as skill behavior eval

Resources: skills/test-driven-development/writing-good-tests.md.

### using-git-worktrees

Source: skills/using-git-worktrees/SKILL.md.

- Detect existing linked isolation before creating; guard submodule false positives
- Prefer native worktree mechanism; user preference/location wins
- Verify baseline and safe target path; preserve host-owned workspaces

Adaptation:
- No new branch, .gitignore change, commit or dependency installation from upstream snippet
- No consent repetition where current user already authorized existing-branch isolation
- Permission denial cannot silently move branch-specific edits into wrong checkout

Resources: none.

### using-superpowers

Source: skills/using-superpowers/SKILL.md.

- Compatibility references describe unavailable todos/subagents and native tool equivalents
- Subagent-stop and host child-session detection illustrate bootstrap recursion failure to prevent

Adaptation:
- EXCLUDE entire 1% invocation/bootstrap/competing routing and automatic workflow chains
- No hooks, injected user context or runtime skill fetch; one Andino owner

Resources: skills/using-superpowers/references/antigravity-tools.md; skills/using-superpowers/references/claude-code-tools.md; skills/using-superpowers/references/codex-tools.md; skills/using-superpowers/references/gemini-tools.md; skills/using-superpowers/references/hermes-tools.md; skills/using-superpowers/references/muse-tools.md; skills/using-superpowers/references/pi-tools.md.

### verification-before-completion

Source: skills/verification-before-completion/SKILL.md.

- Identify claim and proving command; run/read complete result with exit/failure counts before status
- Regression must demonstrate catches bug; tests/build/lint/requirements prove different claims
- Verify agent changes and acceptance checklist independently of agent success report

Adaptation:
- Freshness anchored to exact tested tree/evidence, not ritual same-message wording
- Do not rerun unchanged evidence pointlessly; no unsupported pass claims

Resources: none.

### writing-plans

Source: skills/writing-plans/SKILL.md.

- Task deliverables independently testable, setup/docs folded into owning slice
- Exact paths/signatures/consumes/produces/test assertions/run commands/Expected outcomes
- Spec constraints stay attached; review-focus real-world cases added to owning tests
- Self-review spec coverage/interface consistency/task self-consistency/proportion

Adaptation:
- No second plan or mandatory new approval for accepted execution ticket
- No automatic commits, forced skill subchains or execution-method questionnaire after user selected execution

Resources: none.

### writing-skills

Source: skills/writing-skills/SKILL.md.

- Baseline consumer failure before guidance, minimal guidance, rerun and refine with evidence
- Classify failure form: discipline→guard, shape→positive recipe, omitted field→template slot, condition→observable predicate
- Match tests to discipline/technique/pattern/reference; micro-test wording with no-guidance control and multiple reps
- Trigger metadata guides discovery; heavy reference/resources lazy-loaded; package interpreter-safe scripts
- Pressure time/sunk cost/authority/exhaustion; behavior tests distinct from structural checks

Adaptation:
- No blanket deletion of user work, mandatory push, downstream bootstrap or forced subagents
- External Anthropic-adapted guide expression excluded pending provenance; retain independently written methods
- No claim behavior proven by deterministic Markdown/schema tests alone

Resources: skills/writing-skills/anthropic-best-practices.md; skills/writing-skills/examples/CLAUDE_MD_TESTING.md; skills/writing-skills/graphviz-conventions.dot; skills/writing-skills/persuasion-principles.md; skills/writing-skills/render-graphs.js; skills/writing-skills/testing-skills-with-subagents.md.

## B-T02 comparison evidence

TDD preserves the observed RED assertion failure, minimal GREEN, project suite, then behavior-preserving REFACTOR. writing-good-tests.md adds independently derived expectations, real consumer behavior, mutation sensitivity, narrow doubles, and no source-text checks posing as behavior tests.

Debugging preserves investigation before fixes: reproduce and trace boundary evidence, compare working examples, test one hypothesis, then regression-test a single root fix. Three failed fixes require architectural reassessment. The polluter helper is a sequential npm runner despite its bisection comment; its shell/glob/path assumptions require adaptation.

There is no standalone refactoring skill in this source. TDD limits refactoring to green behavior-preserving cleanup; debugging explicitly rejects bundled unrelated refactoring.

## Legal and excluded controls

Root LICENSE is MIT, Copyright (c) 2025 Jesse Vincent. Preserve its notice for substantial adapted expression. CODE_OF_CONDUCT.md explicitly overrides with Contributor Covenant 3.0 under CC BY-SA 4.0 and is excluded from runtime copying. The Anthropic best-practices adaptation is identified by the local design spec but has no independent file notice: exclude its expression and independently write methods.

- using-superpowers startup bootstrap and 1% skill invocation rule
- SessionStart/context/pre_llm_call injection and automatic workflow chaining
- Plugin/marketplace installation and runtime fetching/autoupdate
- Source-specific .superpowers ledger replacing durable Andino ticket
- Unapproved branch creation, commit/push/merge, .gitignore writes, environment installs
- Mandatory subagent fan-out/model override and fixed five-round retry policy
- Upstream visual companion remote branding/telemetry and background server lifecycle

## Host, resource and test evidence

- Codex manifest hooks is empty; skill discovery is configured, not hook bootstrap proof.
- Claude/Cursor/Muse hooks inject using-superpowers using platform-specific output envelope; Windows polyglot hook finds Git Bash.
- OpenCode .opencode/plugins/superpowers.js supports V1 named/server and V2 setup; native skill registration, frontmatter continuation handling, cache and child parentID detection. Lookup failure treats child as top-level (fail-open bootstrap); exclude injection.
- Pi resources_discover registers skills; context injection on start/compact until agent_end. Pi has no standard subagent/todo.
- Hermes register_skill requires Path and description; pre_llm_call first turn injects bootstrap.
- Gemini GEMINI.md force-imports bootstrap/tools; Kimi manifest sessionStart invokes using-superpowers.
- Antigravity plugin provides marketplace metadata and native tool reference.
- No agents/ directory exists: agent roles are inline reviewer/implementer/analyst Markdown resources, all included in file inventory.

All 238 tracked files are present and classified with raw-byte SHA-256, size, category, status and headings in superpowers-audit.json. It includes every skill resource, inline agent prompt, host adapter, hook, plugin manifest, test and legal path. Historical plans are context, not current instructions. Assets are hashed; visual content is not reviewed.

The upstream suite was not executed. Its test sources cover brainstorm HTTP/WebSocket auth and origin/lifecycle/reconnect/PID owner/platform launch; task brief/workspace/review-package/inline helper behavior; host manifests/packaging/sync/registration/bootstrap/cache/child session; explicit invocation and workflow live Claude Code scenarios; diagnosis structure/polluter glob/render graph/version bump/shell lint. Some live tests call models/host CLIs and mutate disposable fixtures. They cannot be claimed passing from source inspection.

## Completeness limits and blockers

- External superpowers-evals/Quorum referenced by README/AGENTS is not included in this snapshot; behavior-eval suite unavailable locally.
- No upstream host integration/live agent tests executed; snapshot source audit does not prove host support.
- Binary assets byte-hashed and classified, not visually reviewed; unused upstream branding excluded.
- Historical plans/specs inventoried and inspected for provenance/dependency/behavior conflicts; not treated as current executable requirements.
- anthropic-best-practices.md external adaptation lacks independent file-level redistribution notice; do not copy its expression.

No material source-byte omission was found. The external eval repository is absent, so full upstream behavioral-validation completeness is unverified. No fetching, host installation, upstream edits or Git mutations were performed.

## Accepted B-T02 alignment

Canonical TDD uses RED-GREEN for one behavior/public seam. Optional refactoring has its own GREEN-only behavior-preservation gate under review. Reuse an accepted seam and ask only about unresolved material interface choices. Shared reviews consume an actual working diff snapshot. Useful discovery/safety/capability distinctions from using-superpowers enter the root contract; its bootstrap remains excluded.
