# Builder-Ready Design Specification: Final Skill System Refinement

**Specification ID**: SPEC-2026-11-01-SKILL-SYSTEM-REFINEMENT
**Status**: APPROVED — user approval recorded 2026-11-01
**Date**: 2026-11-01
**Author**: Claude Code (under Andino Workflow Governance)
**Target Path**: Architectural
**Parent Decision Map**: `docs/decision-maps/final-skill-system-review/map.md`

---

## 1. Overview & Business Objectives

### 1.1 Goal
Perform a comprehensive, evidence-driven refinement of the Andino skill system across the agreed **Elevated set + core** (18 folders) and shared supporting authoring infrastructure. Establish an Andino-native `skill-maker` evolved from `method-authoring`, sharpen skill discovery and selection within the existing coordinator contracts, eliminate operational defects, ambiguities, duplication, and purposeless decoration, and establish ratcheted verification protocols that prevent future behavioral drift.

### 1.2 Core Requirements & Constraints
1. **Preserve Existing Functionality**: Retain all operational capabilities, specialized craft, and working interfaces unless an intentional change is explicitly agreed (DEC-004).
2. **No Unnecessary Complexity**: Improve the existing coordinator; do not add competing routers, secondary execution lifecycles, or universal evaluation swarms.
3. **No Direct Copying**: Synthesize principles from upstream references (`obra/superpowers:writing-skills` and `addyosmani/agent-skills:using-agent-skills`) into Andino's local architecture without importing foreign dependencies, authority overrides, or bootstrap anti-patterns.
4. **Strict Repository-Local Boundary**: Refinement is strictly confined to local repository sources (`C:/Users/Lenovo/Downloads/AI-RULES`). Zero mutations to user-level global configuration files (e.g., `~/.andino/skill-catalog.json`, `~/.claude/CLAUDE.md`), zero package installations, and zero automated git commits or pushes occur without explicit, separate user authorization.
5. **Two-Stage Lifecycle Gate**: Conversational consensus permits this specification; explicit written approval of this specification permits invoking `andino-planning`. Zero production skill edits or directory restructuring occur prior to plan approval.

---

## 2. Review & Refinement Scope

### 2.1 The Agreed Member Inventory & Directory Architecture
The scope encompasses 18 canonical folders from the agreed boundary plus the supporting authoring transition:

| # | Directory Path | Canonical Internal Method ID | Role & Primary Responsibility |
|---|---|---|---|
| 1 | `skills/agent-document-authoring` | `andino-agent-document-authoring` | Passive document architecture, prompt context, multi-harness rules (`CLAUDE.md`, `AGENTS.md`). |
| 2 | `skills/api-and-interface-design` | `andino-api-and-interface-design` | Type-first API design, contract modeling, interface boundaries. |
| 3 | `skills/architecture-survey` | `andino-architecture-survey` | Bounded architectural discovery, topology mapping, dependency inspection. |
| 4 | `skills/article-shaping` | `andino-article-shaping` | Long-form technical document structuring, argument flow, deliverable prose. |
| 5 | `skills/brainstorming` | `andino-brainstorming` | Intent extraction, decision DAG grilling, in-flight ADRs, 3-path classification. |
| 6 | `skills/browser-testing-with-devtools` | `andino-browser-testing-with-devtools` | Headless/interactive browser verification, DOM/network inspection. |
| 7 | `skills/ci-cd-and-automation` | `andino-ci-cd-and-automation` | Pipeline automation, workflow automation, pre-commit/CI gating. |
| 8 | `skills/code-review` | `andino-code-review` | Correctness review, anti-pattern detection, code quality gates. |
| 9 | `skills/code-simplification` | `andino-code-simplification` | Complexity reduction, dead-code elimination, maintainability. |
| 10 | `skills/constraint-driven-development` | `andino-constraint-driven-development` | Boundary-first design, invariant definition, negative constraints. |
| 11 | `skills/context-engineering` | `andino-context-engineering` | Context budgeting, token efficiency, KV-cache alignment. |
| 12 | `skills/debugging` | `andino-debugging` | 6-phase systematic debugging, hypothesis testing, root-cause isolation. |
| 13 | `skills/decision-interview` | `andino-decision-interview` | Compatibility forwarding shim to `skills/brainstorming`. |
| 14 | `skills/decision-map` | `andino-decision-map` | Multi-session initiative mapping, DAG ticket lifecycles, fog-of-war management. |
| 15 | `skills/deep-module-design` | `andino-deep-module-design` | Information hiding, deep interface contracts, implementation encapsulation. |
| 16 | `skills/delegation` | `andino-delegation` | Tri-modal delegation, active frontier DAG, two-track review, workspace guards. |
| 17 | `skills/planning` | `andino-planning` | Actionable plan authoring, task decomposition, dependency sequencing. |
| 18 | `skills/plan-execution` | `andino-plan-execution` | Gated plan execution, task verification, checkpoint progression. |
| 19 | `skills/skill-maker` | `andino-skill-maker` | **Canonical authoring engine** evolved from `method-authoring`. |
| 20 | `skills/method-authoring` | `andino-method-authoring` | **Compatibility forwarding shim** to `skills/skill-maker`. |

*Directory Invariant Note*: Retaining `skills/method-authoring` as a physical forwarding shim (matching `skills/decision-interview`) preserves backward compatibility for legacy invocations, ensures static directory count assertions (`>= 59` in test runners) remain unbroken, and eliminates the need for out-of-band global manifest edits.

### 2.2 Shared Core Governance & Infrastructure
- **Root Coordinator & Overview**: `SKILL.md`, `README.md`.
- **Method Dispatch & Index**: `references/method-dispatch.md`, `references/internal-method-index.md`.
- **Capability Coexistence & Registry**: `references/capability-coexistence.md`, `references/capability-registry.md`.
- **Host Invocation**: `references/invocation-adapter.md`.
- **Lifecycle & Execution Plan**: `references/routing.md`, `references/execution-plan.md`, `references/anti-loop.md`.
- **Legal & Provenance**: `references/legal/provenance.md` and related MIT licenses.
- **Verification Infrastructure**: `scripts/verify_*` scripts and embedded operational harnesses.

---

## 3. Capability & Identity Contract: `skill-maker`

### 3.1 The Council 1 Capability-and-Identity Contract Table
To fulfill Council 1's explicit first design action, the relationship between existing authoring assets and the elevated `skill-maker` is formally defined:

| Dimension | Architectural Specification |
|---|---|
| **Consumer Need** | Author, improve, evaluate, and maintain executable methodology bundles (skills) as well as broader repository operational procedures and human protocols. |
| **Current Owner** | `skills/method-authoring` (`andino-method-authoring`). |
| **Expected Added Capability** | Dual-mode authoring (remedial failure-driven vs greenfield contract-driven), minimal contracts (<150 lines), progressive disclosure schemas, and structured baseline/candidate evaluation records. |
| **Canonical Source Folder** | `skills/skill-maker/` (`SKILL.md`, `GUIDE.md`, `resources/`). |
| **Public / Native Names** | `skill-maker`, `andino-skill-maker`. |
| **Compatibility Paths** | `method-authoring`, `andino-method-authoring`, `writing-skills`. Implemented via physical forwarding shim at `skills/method-authoring/SKILL.md`. |
| **Separation from Document Authoring** | `skill-maker` owns *executable methodology bundles*; `agent-document-authoring` owns *passive repository guidance* (`CLAUDE.md`, `AGENTS.md`, prompt rules). |
| **Evidence Required** | Dual-mode operational harness passing in normal and negative mode; successful alias resolution across native entrypoints. |

### 3.2 Dual-Mode Authoring Lifecycle (Remedial vs Greenfield)
Unlike upstream references that mandate an observed failure before writing guidance, `skill-maker` supports both maintenance of failing flows and greenfield capability creation:

```
                          ┌────────────────────────┐
                          │ skill-maker Initiation │
                          └───────────┬────────────┘
                                      │
                         Is this correcting a failure
                          or creating a new capability?
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
         [Mode A: Remedial]                       [Mode B: Greenfield]
  - Construct baseline reproduction        - Define observable capability goal
  - Verify unguided model fails            - Specify triggers and negative gates
  - Write minimal targeted counter         - Design positive operational recipe
  - Verify fix on candidate prompt         - Formulate progressive resource layout
                 │                                         │
                 └────────────────────┬────────────────────┘
                                      │
                                      ▼
                        [Shared Consumer Evaluation]
            - Test unguided control vs candidate guidance
            - Record variance across fresh contexts
            - Verify no user-file deletion or forced swarms
```

### 3.3 Retention of Broader Procedural Authoring
`skill-maker` retains the full operational scope of `method-authoring`: it is authorized and structured to author and maintain non-skill operational procedures, human runbooks, pre-commit protocols, and repository governance documents, ensuring zero regression of legacy authoring capabilities.

---

## 4. Compact Discovery & Selection Architecture

### 4.1 Root Coordinator Decision Lens (<40 Lines)
Embedded directly into root `SKILL.md` (lines 35–70) and detailed in `references/method-dispatch.md`:

```markdown
### Situation-to-Outcome Decision Lens (<40 lines)

| User Situation / Task Trigger | Active Phase | Primary Specialist | Direct Bypass / Negative Gate |
|---|---|---|---|
| Open idea, ambiguous goal, exploring direction | Inception | `andino-brainstorming` | If plan already approved, bypass to `plan-execution`. |
| Architecture settled, breaking into actionable tasks | Planning | `andino-planning` | If tasks are single-file/trivial (<50 LOC), execute inline. |
| Approved plan ready for sequential execution | Execution | `andino-plan-execution` | If scope is newly ambiguous, reopen `brainstorming`. |
| Unexplained test failure, crash, regression | Diagnostic | `andino-debugging` | If cause is confirmed and fix is small, execute inline. |
| Choosing external library, unfamiliar API | Investigation | `search-first` | If local code already provides utility, adopt local code. |
| Decoupled tasks across disjoint write paths | Implementation | `andino-delegation` | If tasks share state or common cause, execute inline. |
| Fragile subsystem, repeated regressions | Remediation | `ai-codebase-rescue` | If code is merely ugly but passing, keep unchanged. |
| Code written, ready for quality gate | Verification | `andino-code-review` | If diff touches only docs/prose, use `natural-writing`. |
| Authoring or maintaining a skill or procedure | Meta-Authoring | `skill-maker` | If editing passive rules (`CLAUDE.md`), use `agent-doc-authoring`. |
| Routine question, code explanation, typo | General Work | **Direct Execution** | **Zero method loading: execute directly without ceremony.** |
```

### 4.2 Contrastive Unprimed Matrix (Council 2 Mandate)
To validate the lens against natural, unprimed user prompts without benchmark contamination:

| # | Unprimed User Prompt | Expected Outcome / Tool Action | Negative Gate / Contrast Rationale |
|---|---|---|---|
| 1 | *"How does the auth token signing work in our middleware?"* | **Direct Execution (Inline)** | Informational explanation; does NOT invoke `debugging` or `delegation`. |
| 2 | *"Fix the typo in README.md line 42."* | **Direct Execution (Inline)** | Trivial mechanical edit (<50 LOC); zero skill loading. |
| 3 | *"We need to add a multi-tenant search engine, but don't know the scale or storage."* | Invoke `andino-brainstorming` | Open architectural uncertainty requires decision DAG grilling. |
| 4 | *"The search spec is approved; let's break down the implementation steps."* | Invoke `andino-planning` | Specification exists; requires actionable task decomposition. |
| 5 | *"Plan is ready. Proceed with Task 1."* | Invoke `andino-plan-execution` | Execution phase; does NOT reopen ideation in `brainstorming`. |
| 6 | *"Integration test test_auth.py fails with HTTP 500 intermittently."* | Invoke `andino-debugging` | Unexplained behavioral defect requires systematic root-cause isolation. |
| 7 | *"Should we use PyJWT or Authlib for token validation?"* | Invoke `search-first` | Solution discovery and library evaluation prior to implementation. |
| 8 | *"Implement these 3 independent microservice modules in parallel."* | Invoke `andino-delegation` | Disjoint write sets and independent domains justify parallel dispatch. |
| 9 | *"Create a new skill for database migration auditing."* | Invoke `skill-maker` | Executable methodology authoring; does NOT use `agent-doc-authoring`. |
| 10 | *"Update CLAUDE.md with our new rtk shell prefix rule."* | Invoke `agent-document-authoring` | Passive guidance update; does NOT use `skill-maker`. |

### 4.3 Low Ceremony Protocol
- **Single-Line Rationale**: When a nontrivial skill is selected, emit a single concise line in chat:
  `[andino-workflow] Active method: <method-name> — <reason>.`
- **Zero Banner Spam**: Never emit multi-turn status banners or decorative ASCII borders.
- **Zero Persistent Ledgers**: Discovery decisions are executed immediately; no separate discovery ledger files (`discovery.md`) are created or maintained.

### 4.4 Selection-to-Loading Enforcement (Internal Cognitive State)
The 5-state lifecycle (`DISCOVERED -> AVAILABLE -> INVOKABLE -> ACTIVE -> USED`) represents the coordinator's **internal verification discipline**, not an external prompt ledger:
1. **Tool-Mediated Loading**: The coordinator must issue an explicit host tool call (`Skill`) or read the canonical `SKILL.md` before governed work begins. Text claims of activation without a tool call are rejected.
2. **Usage Verification**: A skill is marked `USED` in the task record only when its specific procedural gates (e.g., hypothesis testing in debugging, two-track review in delegation) are observed in execution.

---

## 5. Capability Preservation & Cleanup Stopping Rules

### 5.1 The 5-Point Capability-Preservation Baseline
Across the 18 folders and shared core, refinement must pass this concrete checklist:
1. **Invocation Invariance**: All public skill names and aliases (`delegation`, `debugging`, `brainstorming`, `method-authoring`) resolve to their canonical methods without broken paths.
2. **Trigger & Gate Invariance**: Dominant Negative Gates in each skill remain intact; no skill may be modified to trigger on trivial/inline tasks.
3. **Resource Loading Protocols**: Progressive disclosure paths (`resources/*.md`) must exist, be non-empty, and resolve via relative links from `SKILL.md` and `GUIDE.md`.
4. **Authority & Safety Invariants**: Zero automated subagent spawning by workers, zero unapproved git commits, zero deletions of user workspace files, and zero repository-wide `.andino` wipes.
5. **Checkpoint Interfaces**: Existing execution plans (`docs/exec-plans/active/*.md`) and decision maps retain their standard section headers, frontmatter schemas, and `NEXT ACTION` protocols.

### 5.2 Line Budget & Formatting Standards
- **Root Coordinator `SKILL.md`**: Strictly `< 150 lines`. To accommodate the 17-line Decision Lens table, existing prose in "Select work methods first" (lines 30–59) and "Bounded execution" (lines 102–123) will be condensed by 25 lines, maintaining root `SKILL.md` at ~138 lines.
- **Specialized Member Contracts**: Operational `SKILL.md` files maintain high density (<150 lines where feasible), but domain FSMs and negative gates take precedence. Deep craft belongs in `GUIDE.md` and `resources/`.
- **Decoration Removal**: Purge all non-functional emojis, decorative badges, and marketing buzzwords. Retain functional ASCII diagrams, markdown tables, and code notation.

---

## 6. Safety Fixes & Verification Protocols

### 6.1 Dangerous Cleanup Remediation & Workspace Overrides
1. **The Defect**: `scripts/verify_delegation_elevation.py` (lines 122–126) executes `shutil.rmtree(andino_dir)`, deleting the entire repository `.andino/` directory and destroying sibling plans and global settings.
2. **The Remediation**:
   - Update `skills/delegation/scripts/delegation_workspace.py` to respect an environment variable:
     ```python
     override = os.environ.get("ANDINO_WORKSPACE_OVERRIDE")
     base_dir = Path(override) if override else repo_root / ".andino" / "delegation"
     ```
   - Update `scripts/verify_delegation_elevation.py` to run tests inside a disposable `tempfile.TemporaryDirectory()`, setting `ANDINO_WORKSPACE_OVERRIDE`.
   - Implement Windows NTFS-safe cleanup with an `onerror` handler clearing `stat.S_IWRITE` on locked files:
     ```python
     def handle_remove_readonly(func, path, exc):
         os.chmod(path, stat.S_IWRITE)
         func(path)
     shutil.rmtree(temp_dir, onerror=handle_remove_readonly)
     ```
   - Sibling plan isolation is strictly enforced: test teardown never touches the root `.andino` directory.

### 6.2 Deterministic Verification Tiers
1. **Tier 1 (Static Contract Integrity)**:
   - Root `SKILL.md` line count strictly `< 150 lines`.
   - Mandatory sections present across all 18 folders + `skill-maker`.
   - Zero broken relative links to `resources/` or `references/`.
   - Zero decorative emojis in core contracts.
2. **Tier 2 (Isolated Helper Harnesses)**:
   - Execute all helper scripts (`delegation_workspace.py`, `task_brief.py`, `review_package.py`) within isolated temporary workspaces.
   - Verify zero mutations to repository working tree.
3. **Tier 3 (Deterministic Decision Lens Fixture)**:
   - Commit a frozen test fixture `tests/fixtures/decision_lens_cases.json` containing the 10 contrastive unprimed prompts.
   - Run a deterministic Python verification script evaluating trigger matching against the decision lens without launching expensive LLM evaluator swarms.

---

## 7. In-Flight Architectural Decision Record (ADR-0001)

```markdown
# ADR-0001: Skill System Refinement, Skill-Maker Evolution, and Compact Discovery Lens

- **Status**: Accepted (In-Flight)
- **Date**: 2026-11-01
- **Decision Makers**: User, Claude Code (Andino Workflow)
- **Target Path**: Architectural

### Context
The user requested a comprehensive review and refinement of the Andino skill system across existing skills up to and including delegation, the creation of an Andino-native `skill-maker`, and improved discovery and selection when invoking `use andino-workflow`. Two independent council consultations (Council 1 on cleanup/skill-maker, Council 2 on discovery/selection) and a 3-agent adversarial verification workflow evaluated the architectural direction.

### Decision
1. Bound the refinement scope to the **Elevated set + core** (18 folders) plus the supporting authoring transition (total 20 on-disk directories including forwarding shims).
2. Evolve `skills/method-authoring` into canonical `skills/skill-maker` (`andino-skill-maker`), retaining `skills/method-authoring` as a physical forwarding shim for total backward compatibility. Retain `agent-document-authoring` as the distinct owner of passive guidance.
3. Consolidate a compact (<40 lines) situation-to-outcome decision lens with contrastive near-miss pairs into existing coordinator files (`SKILL.md`, `references/method-dispatch.md`, `references/internal-method-index.md`). Reject separate router skills or external host interception hooks.
4. Enforce low ceremony: single-line selection rationales; eliminate per-turn banners and discovery ledgers. Enforce strict direct execution bypass for routine questions and small mechanical edits (<50 LOC).
5. Remediate the dangerous verifier cleanup in `scripts/verify_delegation_elevation.py` by introducing `ANDINO_WORKSPACE_OVERRIDE` and tempfile isolation, guaranteeing zero root `.andino` directory deletions.
6. Condense root `SKILL.md` prose by 25 lines to accommodate the decision lens while strictly honoring the `< 150 lines` invariant.

### Alternatives Considered & Trade-offs
1. **Alternative B (Chosen Approach: Coordinator Consolidation & Skill-Maker Evolution)**:
   - *Pros*: Eliminates duplicate authoring engines, resolves selection friction with zero host coupling, preserves full backward compatibility, maintains high KV-cache efficiency.
   - *Cons / Costs*: Requires maintaining alias redirection shims and tight line budgets.
2. **Alternative A (Status Quo / Minimal Metadata Repair Only)**:
   - *Pros*: Lowest churn.
   - *Why Rejected*: Leaves casual prompts vulnerable to false negatives and ignores the user's explicit request for `skill-maker`.
3. **Alternative C (Dedicated Router Skill or Host Interception Hooks)**:
   - *Pros*: Programmatic pre-execution interception.
   - *Why Rejected*: Exceeds repository boundary, breaks multi-host portability, and introduces fragile external dependencies.

### Consequences & Floor Invariants
- **Positive**: Clean authoring lifecycle, intuitive colloquial skill selection, zero context pollution from bureaucratic ledgers, safe test execution.
- **Negative**: Adds physical forwarding shims (`skills/method-authoring`).
- **Floor Invariants**:
  1. No production skill code or configuration is edited prior to written specification approval.
  2. The decision lens in `SKILL.md` must not exceed 40 lines; root `SKILL.md` must not exceed 150 lines.
  3. Routine tasks and small edits (<50 LOC) must bypass specialist skill loading entirely.
  4. Test runners must never delete parent `.andino` or sibling workspaces.
  5. Refinement is strictly repository-local; zero unauthorized mutations to global host configs (`~/.andino/`).
```

---

## 8. Domain Glossary (Ubiquitous Language)

| Domain Term | Canonical Definition | Anti-Terms (Do NOT Use) | Code / File Representation |
|---|---|---|---|
| **skill-maker** | Canonical authoring methodology for creating, improving, and maintaining executable skills and operational procedures. | "skill-creator", "writing-skills", "method-builder" | `skills/skill-maker/` (`andino-skill-maker`) |
| **method-authoring (shim)** | Physical forwarding directory redirecting legacy invocations to `skills/skill-maker`. | "deprecated skill", "old authoring", "dead code" | `skills/method-authoring/` |
| **agent-document-authoring** | Methodology for designing passive repository guidance and rules files (`CLAUDE.md`, `AGENTS.md`). | "skill-authoring", "rules-editor", "doc-maker" | `skills/agent-document-authoring/` |
| **Decision Lens** | Compact, high-density matrix translating user situation and active phase into mapped method selection. | "Router", "Dispatch Engine", "Selector Bot" | Embedded in `SKILL.md` & `method-dispatch.md` |
| **Near-Miss Pair** | Semantic contrast between superficially similar user tasks that resolve to different execution paths. | "Edge cases", "Ambiguities", "Collisions" | Section in `method-dispatch.md` |
| **Direct Execution Bypass** | Immediate execution of routine conversational, explanatory, or small mechanical tasks without loading skills. | "Fallback", "Drop-through", "Default route" | Negative gate in `SKILL.md` |
| **Active Frontier** | The unblocked set of tasks or tickets whose dependencies are completely satisfied. | "Backlog", "Queue", "To-do list" | `Frontier` (`frontier-and-dag-protocols.md`) |
| **Floor Invariant** | A mandatory structural constraint that can never be relaxed without a formal architectural decision. | "Guideline", "Best practice", "Rule of thumb" | Hard gates in `SKILL.md` |
| **Two-Track Review** | Independent verification separating specification compliance from code quality. | "Self-check", "Code audit", "PR review" | `two-track-review-and-fix-loop.md` |
