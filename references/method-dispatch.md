# Internal method dispatch

This contract covers all internal methods in the [index](internal-method-index.md)
and its source-name aliases. It is a loading and handoff procedure, not a runtime router,
a second catalog, a new plan or an instruction to activate every method.

## Method ownership

Andino coordinates selection, dependency handoff, shared progress, permissions and
resource guards. The selected skill owns its complete procedure, required resource
reads, artifact structure/detail and technical checks. This applies equally to
native Andino members, AI-RULES siblings and relevant installed external skills.
MCP/native tools execute actual operations; they do not replace a selected method.

Follow the loaded method rather than just announcing it or producing a coordinator
summary. Resolve output/detail conflicts in favor of the selected method and user
requirements. Checkpoint density, Focus and acquisition/output limits cannot remove
required decisions or proof. Permission, concurrency and evidence guards still
apply; a method does not gain authority by being selected.

Use one authoritative progress source, which may link complete skill artifacts.
No compulsory shared artifact schema or second routing/planning ceremony is added.
Release the method when its need ends; select the next only for an actual phase
change or distinct evidenced concern, not to complete a skill chain.

## Explicit requests

1. Distinguish a user instruction from quoted text, filenames, examples and an inventory.
2. Resolve a requested canonical ID or source-name alias through the index. A clear
   request for the procedure also counts: asking for an implementation plan selects
   planning; asking to execute an accepted plan selects plan-execution. The rule
   applies equally to architecture, writing, security, learning and every other method.
3. Check applicability, accepted decisions, phase and resource permissions. For an
   alias with several destinations, choose the relevant procedure(s), not every target.
   An explicit native provider choice retains the host invocation contract.
4. Load the selected native skill `andino-<name>` (or canonical `SKILL.md`/`GUIDE.md`) before Focus and before governed work.
   Read needed supporting resources, then apply the procedure. A name mention,
   metadata lookup or remembered technique is not activation.
5. If a requested method is excluded, explain the material conflict and route to the
   actual need. If absent or denied, record UNAVAILABLE and an honest permitted fallback.
   Never fetch another copy to bypass a denied guide or claim fallback is method use.

## Implicit requests

Name the requested outcome and present phase internally, then inspect the index's
selection and exclusion columns for plausible methods. No skill name is required.
Choose by meaning and evidence, not a keyword match or a compulsory engineering chain.
Select the narrowest method(s) covering distinct current needs and load their guides.
If no internal method fits, retain direct work or resolve appropriate native support.
Do not search all external skill bodies before checking the bundled index.

### Situation-to-Outcome Decision Lens

| User Situation / Task Trigger | Active Phase | Primary Specialist | Direct Bypass / Negative Gate |
|---|---|---|---|
| Open idea, ambiguous goal, exploring direction | Inception | `andino-brainstorming` | If plan already approved, bypass to `plan-execution`. |
| Architecture settled, breaking into actionable tasks | Planning | `andino-planning` | If tasks are single-file/trivial (<50 LOC), execute inline. |
| Approved plan ready for sequential execution | Execution | `andino-plan-execution` | If scope is newly ambiguous, reopen `brainstorming`. |
| Unexplained test failure, crash, regression | Diagnostic | `andino-debugging` | If cause is confirmed and fix is small, execute inline. |
| Choosing external library, unfamiliar API | Investigation | `search-first` | If local code already provides utility, adopt local code. |
| Decoupled tasks across disjoint write paths | Implementation | `andino-delegation` | If tasks share state or common cause, execute inline. |
| Fragile subsystem, repeated regressions | Remediation | `ai-codebase-rescue` | If code is merely ugly but passing, keep unchanged. |
| Code or behavioral contract ready for correctness review | Verification | `andino-code-review` | Use `natural-writing` only for prose/style review, not execution or safety contracts. |
| Authoring or maintaining a skill or procedure | Meta-Authoring | `skill-maker` | For passive repository guidance, use `agent-document-authoring`; auditing such files can still be an executable skill. |
| Routine question, code explanation, typo | General Work | **Direct Execution** | **Zero method loading: execute directly without ceremony.** |

### Contrastive Near-Miss Pairs

1. **Code Explanation vs Debugging**:
   - *"How does auth token signing work?"* -> **Direct Execution** (pure factual explanation).
   - *"Why does test_auth fail intermittently with 500?"* -> `andino-debugging` (behavioral defect with unknown cause).
2. **Mechanical Edit vs Method Loading**:
   - *"Fix typo on line 42 of README.md"* -> **Direct Execution** (<50 LOC, zero ceremony).
   - *"Restructure the skill discovery matrix across 5 files"* -> `andino-planning` / `andino-plan-execution`.
3. **Spec Formulation vs Ideation**:
   - *"We need search but don't know the scale or storage engine"* -> `andino-brainstorming` (exploring architecture).
   - *"The search spec is approved; break down tasks"* -> `andino-planning` (task breakdown).
4. **Library Evaluation vs Custom Implementation**:
   - *"Should we use PyJWT or Authlib?"* -> `search-first` (compare external packages).
   - *"Write custom JWT validation logic from scratch"* -> `andino-tdd` (if approved) or `search-first` (to check existing code first).
5. **Executable Skill vs Passive Rules**:
   - *"Create a new skill for database migration auditing"* -> `skill-maker` (executable procedure, test harness).
   - *"Update CLAUDE.md with a new rtk command rule"* -> `agent-document-authoring` (passive markdown guidance).
6. **Parallel Delegation vs Inline Execution**:
   - *"Implement 3 independent microservices with disjoint paths"* -> `andino-delegation` (disjoint write sets).
   - *"Fix 3 tests that all fail due to the same database connection timeout"* -> `andino-debugging` inline (shared root cause).

7. **Correctness Contract vs Prose Polish**:
   - *"Review this Markdown execution contract for lost permission gates"* -> `andino-code-review` (behavior and authority).
   - *"Polish the wording of this release note"* -> `natural-writing` (prose/style only).
8. **Failure Diagnosis vs Factual Explanation**:
   - *"What is causing the crash in production?"* -> `andino-debugging`, not the routine-question bypass.
   - *"What is this middleware's purpose?"* -> **Direct Execution** when only explanation is requested.
9. **Authoring Intent vs Filename Mention**:
   - *"Author a skill that audits CLAUDE.md for syntax mistakes"* -> `skill-maker` (an executable auditing procedure).
   - *"Edit CLAUDE.md with our new rule"* -> `agent-document-authoring` (the passive guidance is the deliverable).
10. **Requested Parallelism vs Negated Parallelism**:
   - *"Implement independent modules in parallel"* -> `andino-delegation` after authority and write-independence checks.
   - *"Do not implement in parallel; inspect the approved plan only"* -> inspect/review the plan; do not dispatch workers or start implementation.

### Low Ceremony Interaction Standard

When selecting a governed specialist method, maintain low-ceremony communication:
- **Single-Line Rationale**: Announce the activation in chat with one clean line:
  `[andino-workflow] Active method: <method-name> — <reason>.`
- **Zero Banner Spam**: Never emit multi-turn status banners, progress ascii boxes, or decorative emoji headers.
- **Zero Persistent Ledgers**: Execute discovery decisions immediately; never write temporary `discovery.md` files or external prompt logs.

### Selection-to-Loading Enforcement

The 5-state lifecycle (`DISCOVERED -> AVAILABLE -> INVOKABLE -> ACTIVE -> USED`) is an **internal cognitive verification discipline**:
1. `DISCOVERED`: Known in index or catalog.
2. `AVAILABLE`: File exists on disk and is readable.
3. `INVOKABLE`: Tool/permissions allow execution.
4. `ACTIVE`: The coordinator has issued an explicit host tool call (`Skill`) or read the canonical `SKILL.md` before governed work begins. (Text mentions alone are rejected).
5. `USED`: The specific procedural invariants of the method (e.g. hypothesis testing in debugging, two-track review in delegation) were observed in execution evidence.

Internal-first is a default provider preference, not a veto on required domain owners,
required Search First research, explicit native provider requests or the accepted UI
policy. Those supports may be complementary and must activate before their own work.
An internal research guide does not replace a required Search First invocation.
Focus shapes communication after work-method selection/loading and never owns routing.

## Phase transitions

At an actual change of need, reconsider the index; keep valid activation instead of
rereading it. Do not accumulate all methods in anticipation of future phases.

| Current condition | Next method and exit evidence |
| --- | --- |
| Direction remains open and is not delegated | brainstorming; chosen/delegated direction before dependent design |
| Accepted work needs implementation ordering | planning; scoped tasks, dependencies, acceptance and next action |
| Accepted plan ready and execution is authorized | plan-execution; dependency-ready task, current interfaces and evidence |
| Executable behavior is about to change | tdd; intended RED then focused GREEN at the accepted seam |
| Implementation ready for review | code-review; Spec and Standards findings resolved or explicitly retained |
| Consequential acceptance claim | verification; current observation supports each material criterion |

Other methods keep their index conditions and guide outputs. Stop after a requested
plan/review/advice deliverable unless execution is also authorized. An unresolved
user-owned decision blocks dependent work, not independent authorized tasks.

## Evidence

Use the current plan or task context, not a second ledger. Retain these compact fields
when method use matters to acceptance:

| Requested outcome | Current method | Activation evidence | Work/result | Next condition |
| --- | --- | --- | --- | --- |
| Actual task and phase | Canonical ID and selected alias if any | Actual permitted guide read/path or precise UNAVAILABLE boundary | Identifiable action/artifact/check applying the guide | Evidence needed to continue, or deliverable complete |

Metadata establishes discovery; a guide read establishes ACTIVE; applying it produces
USED evidence; acceptance still requires the result to satisfy the task. Keep these
separate. Read-only, structural, fixture and package checks cannot establish autonomous
model routing. When live agent testing is delegated to the user, supply raw cases and
separate reviewer expectations; report model behavior NOT_VERIFIED until executed.
