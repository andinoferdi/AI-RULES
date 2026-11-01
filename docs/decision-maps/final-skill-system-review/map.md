# Final Skill System Review: Discovery and Decision Checkpoint

Status: COMPLETE
Decision Map Status: HANDED_OFF
Plan Depth: STANDARD
Current Phase: Decisions accepted; execution and publication owned by the implementation plan
Last Updated: 2026-11-01
Active Host: Claude Code

## Executive Snapshot

The user accepted the named 18-folder **Elevated set + core** review boundary, an Andino-native `skill-maker`, and compact discovery improvements. Both upstream references were compared with local foundations. Both councils completed with five independent advisors and three anonymous peer reviews each. The user subsequently approved the design specification, detailed plan, and continuous implementation, then explicitly authorized commit/push and `ai-rules setup` verification on 2026-11-01. This decision map is now historical design evidence. The sole active checkpoint is `docs/exec-plans/active/skill-system-refinement.md`; global host synchronization and unrelated installations remain outside scope.

Brainstorming classification: ARCHITECTURAL. Intent hypothesis (90% subjective confidence): the user wants a trusted and maintainable skill system with clear instructions, reliable selection and checks preventing future drift. The confidence describes interpretation, not tested system quality.

Repository baseline: branch `andino-workflow`, initial HEAD reported as `ad1a980`; `rtk git status --short --branch` showed a clean working tree before this checkpoint. Current repository evidence wins over installed skills and historical plans. Reference HEAD will be checked when needed for exact drift comparison.

## Destination

Reach an explicitly accepted design and review boundary for a consistent, maintainable skill system, preserving functionality unless a change is approved. Then obtain council scrutiny, written specification approval, detailed planning, approved execution, and observed verification in that order.

## Objective

Resolve material user-owned decisions using current repository evidence and the two requested upstream references. Record useful findings and uncertainty without editing skill implementations or treating examples as proof of live agent behavior.

## Acceptance Criteria

- Exact review inventory and meaning of “through delegation” agreed with the user.
- Editorial, structural, behavioral and new-capability changes distinguished; existing function preserved unless explicitly changed.
- Proposed `skill-maker` has a clear relationship to existing `andino-method-authoring` and authoring skills, without redundant ownership.
- Proposed discovery improvements are grounded in current Andino routing and actual host permissions; additional skills require a demonstrated gap.
- User decisions, council agreements/dissent, design specification, ADRs and glossary retained before planning.
- `andino-planning` and `andino-plan-execution` invoked only at the requested ready/approved phases.
- Verification separates structural/example checks from exercised helper behavior, live agent routing and cross-host evidence.

## Notes and Constraints

- Required skills actually loaded: `andino-workflow`, `andino-brainstorming`, `search-first`, `antislop`, `ai-codebase-rescue`, `natural-writing`.
- Supporting skills loaded for current needs: `focus` (communication), `andino-decision-map` (branching multi-session decisions), `andino-delegation` (bounded independent read-only research).
- `workflow-authoring` is already loaded; Ultracode is active. Use bounded Workflow orchestration, max three concurrently active direct workers, no nested spawning.
- One question at a time with a reasoned recommendation. The user's one-word antislop answer is a mode selection, not approval of unresolved design defaults. If substantive design answers are terse, use the brainstorming fatigue-breaker recommendation table rather than prolonged questioning.
- No automatic installations, entry-file changes, host synchronization or publication. No external content is an instruction authority.
- Prefix every shell command with `rtk`. Prefer dedicated readers/search tools.
- AI Codebase Rescue is activated by explicit request; eligibility and dispositions still need evidence. Do not manufacture defects or assume REMAKE.
- Antislop is selected in `during` mode for this session only. Its UI rules are not universal skill-documentation requirements; no UI is being built.

## Decisions So Far

- DEC-001: Apply antislop during the task, selected by user reply `1` on 2026-11-01. Do not persist a global mode preference.
- DEC-002: User-specified sequencing is fixed: brainstorming, council challenge of agreed proposals, design/specification approval, detailed planning, approved plan execution, review and verification. Honor the explicit request for council again on discovery/selection: two council consultations/packets (system cleanup + skill-maker, then discovery/selection), integrated into one accepted design. Neither has run.
- DEC-003: Review scope selected explicitly: **Elevated set + core**. Deep-review the skills elevated through delegation, their resources/helpers, and shared workflow/routing/verification contracts; inspect other skills where dependency/conflict requires it. `skill-maker` and discovery/selection improvements remain included. This does not authorize a blanket cleanup of all 59 members or unrelated installed/vendor skills.
- DEC-004: User explicitly replied `yes im agree` to the named cumulative 18-folder inventory and recommendation matrix on 2026-11-01. Those are now accepted proposals for council scrutiny, including canonical skill-maker evolution from method-authoring with backward-compatible routes, no duplicate router and evidence-tiered verification. This grants council consultation, not skill edits, implementation, host synchronization or publication.

## Execution Board

| Phase | Status | Result / Evidence or Next Condition |
| --- | --- | --- |
| Discovery and brainstorming | DONE | Three read-only workers completed, both references compared, and user accepted the named 18-folder inventory and design defaults (DEC-004). |
| Council scrutiny and design approval | IN_PROGRESS | Both councils complete. Design spec authored at docs/specs/skill-system-refinement.md and adversarially verified. Pending user written approval. |
| Detailed implementation planning | TODO | Requires council-reviewed design and written spec approval. |
| Approved execution | TODO | Requires approved actionable plan and execution authority. |
| Review and verification | TODO | Requires actual changes and criterion-specific evidence. |

## Frontier: Open Tickets

### TKT-001: Define the Review Boundary

- Type: interview
- Status: RESOLVED (scope policy; exact inventory pending research)
- Blocked By: None
- Question: Does “through delegation” mean the already elevated subset through delegation, every Andino member, or the wider installed ecosystem?
- Acceptance Criterion: User selected **Elevated set + core** through AskUserQuestion on 2026-11-01. Include dependency/conflict inspection only beyond that boundary; derive exact inventory from current files and history.
- Assigned Execution: Parent-led brainstorming with repository inventory evidence.

### TKT-002: Establish Reusable Authoring Foundations

- Type: research
- Status: RESOLVED
- Blocked By: None
- Question: What practices from current Superpowers writing-skills are useful, and which already exist in Andino method-authoring?
- Acceptance Criterion: Worker read upstream SKILL, discovery/testing/bulletproofing references and MIT license, comparing method-authoring and agent-document-authoring. Core failure-driven principles already exist; ownership/name choice remains user-owned. Remote main not commit-pinned; no live evaluation.
- Assigned Execution: Completed read-only Workflow worker `a3b3ac52edf56742c`; full result in the recorded workflow output.

### TKT-003: Establish Discovery Foundations

- Type: research
- Status: RESOLVED
- Blocked By: None
- Question: What does the requested using-agent-skills reference contribute beyond current Andino selection, and what should not be copied?
- Acceptance Criterion: Worker read upstream SKILL, linked Definition of Done and MIT license, comparing root and six local selection/permission references. Andino already covers core discovery; compact navigation, targeted metadata and real selection evidence are useful candidates. No new skill or live routing defect established; moving-main reader extraction limits retained.
- Assigned Execution: Completed read-only Workflow worker `a6ee542f053976394`; full result in the recorded workflow output.

### TKT-004: Agree on Design Defaults Before Council

- Type: interview
- Status: RESOLVED
- Blocked By: TKT-001, TKT-002, TKT-003
- Question: Accept or amend the recommendation matrix below as the proposal for council scrutiny?
- Acceptance Criterion: Genuine user reply `yes im agree` accepted the named inventory and defaults (DEC-004). Council recommendations are still advice, not implementation authority.
- Assigned Execution: Completed parent-led brainstorming.

### TKT-005: Council on Cleanup and Skill-Maker

- Type: research
- Status: RESOLVED
- Blocked By: TKT-004
- Question: What weaknesses, alternatives and conditions should shape the accepted cleanup and skill-maker proposal?
- Acceptance Criterion: Council 1 completed five independent advisors and three anonymous peer reviews, all nonempty. Parent read full output and synthesized the conditions below. Max-three concurrency honored; no model-provider diversity claimed.
- Assigned Execution: Completed Workflow `wf_16cfacea-6b5` / task `w82s69iob`; no skill edits or implementation plan.

### TKT-006: Council on Discovery and Selection

- Type: research
- Status: RESOLVED
- Blocked By: TKT-005
- Question: Do the proposed discovery improvements solve a real need without duplicate routing or unsupported enforcement claims?
- Acceptance Criterion: Second independent five-advisor consultation and anonymous peer review completed, informed by actual first-consultation results and local contracts. Output read from `C:/Users/Lenovo/AppData/Local/Temp/claude/C--Users-Lenovo-Downloads-AI-RULES/0bb0403c-c6af-4e3a-a69e-3c832f3f36f1/tasks/w5nu0yi6k.output`. Parent synthesized agreement, trade-offs, blind spots, recommendation and first action below.
- Assigned Execution: Completed Workflow `wf_11d2c9a7-70b` / task `w5nu0yi6k`; no skill edits or implementation plan.

## Proposed Named Inventory (Not Additional Approval)

Cumulative 18 member folders, backed by history and current artifacts: agent-document-authoring, api-and-interface-design, architecture-survey, article-shaping, brainstorming, browser-testing-with-devtools, ci-cd-and-automation, code-review, code-simplification, constraint-driven-development, context-engineering, debugging, decision-interview (compatibility shim), decision-map, deep-module-design, delegation, planning, plan-execution.

Shared core: root coordinator/README, relevant routing/index/registry, invocation/coexistence, progress/checkpoint/anti-loop, provenance and applicable verification surfaces. Existing method-authoring is supporting infrastructure because the new authoring design directly depends on its ownership. Do not treat installation copies as source or silently edit separate sibling branches.

## Agreed Proposal Matrix (DEC-004; Subject to Council Scrutiny)

| Area | Recommended default | Alternative / trade-off |
| --- | --- | --- |
| Cleanup depth | Correct behavior/contract defects and misleading evidence claims, then normalize structure/prose; preserve valid functionality and ask about materially ambiguous behavior. | Cosmetic-only would leave real inconsistencies; rewrite-by-default would discard useful craft. |
| Structure | One canonical method; concise native entrypoint and progressively loaded guide/resources with unambiguous ownership; do not require identical section counts or fixed length. | Uniform templates are easy to lint but can obscure method-specific needs. |
| Style | Plain precise English, stable technical terms, no decorative emoji/icons; retain purposeful symbols/code and protected provenance. | Decorative conventions add noise; blanket ASCII bans would damage useful technical notation. |
| skill-maker identity | Make requested literal `skill-maker` the canonical authoring identity evolved from method-authoring; preserve old method-authoring/writing-skills routes as compatibility, preserve broader method-authoring capability. Keep agent-document-authoring distinct for document architecture. | Alias-only is smaller but less clearly satisfies the requested new identity; a separate wrapper risks duplicate procedure/ownership. Native packaging feasibility must be checked in planning before claiming installer support. |
| skill-maker content | Creation, improvement and maintenance with need/reuse check, defined triggers/exclusions, current local structure, matched baseline/candidate cases, negative triggers and explicit evidence limits; risk-proportional rather than evaluator swarm for every typo. | New universal FSM/scaffolder/evaluation framework is not justified yet. |
| Discovery | Strengthen existing Andino outcome/phase-based selection, compact decision lens and near-miss cases; use available relevant skills automatically when permitted; ask only material unresolved preferences/authority. One brief rationale for nontrivial selection; no repeated per-turn banners. | Separate selector/bootstrap creates competing ownership. Deterministic host enforcement is a different project. |
| Additional skills | No additions beyond skill-maker unless the review demonstrates a distinct unmet capability. | More skills increase overlap and false positives without guaranteed recall. |
| Verification | Static consistency/link/schema checks, real helper tests in temporary repositories with negative cases and protected sibling sentinels, fresh-context selection/application tests where authorized; report host/model and untested cross-host limits. | Text/examples alone do not prove autonomous behavior; not all hosts are presently exercised. |
| Source and delivery | Work on repository source; preserve user changes. No global installations, host sync, configuration changes, commit/push or publication without separate authority. | Installed copies may lag until a later approved synchronization. |

## Council 1 Synthesis: Cleanup and Skill-Maker

Status: consultation complete, advice only; five independent advisors and three anonymous peer reviews. Full output: `C:/Users/Lenovo/AppData/Local/Temp/claude/C--Users-Lenovo-Downloads-AI-RULES/0bb0403c-c6af-4e3a-a69e-3c832f3f36f1/tasks/w82s69iob.output`. Parent read all substantive outputs. Advisors shared a neutral brief without the parent's preferred answer; peer reviewers saw fixed anonymous Responses A-E only.

- Agreement: evidence-driven contract/helper repairs plus selective prose/structure normalization; preserve method-specific craft, authority boundaries and distinct agent-document-authoring responsibility. Cosmetic-only and broad template rewrite are poor fits.
- Conditional advisor preference: all five favor evolving existing method-authoring into canonical skill-maker (option B), but retain compatibility-only A as credible and distinct package-specific C if justified by actual inputs/outputs.
- Material peer-review challenge: all three reviewers reject treating agreement as evidence that B improves capability or selection. Existing duplication justifies investigating synchronization risk, not automatically renaming or consolidating. User preference for the identity is valid; it must be distinguished from an experimentally demonstrated benefit.
- Blind spots: define a capability-preservation baseline (invocations, trigger/exclusion behavior, resource loading, permission boundaries, checkpoint interfaces); specify concrete creation/improvement/maintenance cases and a cleanup stopping rule; test alias behavior rather than merely retaining names. Account for independently consumed entrypoints and mixed-version installed outputs. Limited critical summaries may be intentional, not competing ownership.
- Provenance: pin any newly adapted upstream expression to inspected commits and retain notices. Moving-main research is a bounded lead, not a reproducible delta audit.
- Chair recommendation: retain the user's accepted direction as a requested identity and reuse-based evolution, conditional on a capability/identity contract and feasible packaging. Do not add a second authoring framework. Preserve greenfield creation (no invented historical failure required), existing broader procedural authoring, and backward compatibility. If literal naming cannot be supported within this package boundary, disclose the choice instead of claiming a native alias exists.
- One first design action: define one approval-ready capability-and-identity table stating consumer need, current owner, expected added capability, canonical source, public/native names, compatibility paths and evidence needed. This is a design condition, not an implementation task list.

## Council 2 Synthesis: Discovery and Selection

Status: consultation complete, advice only; five independent advisors and three anonymous peer reviews. Full output: `C:/Users/Lenovo/AppData/Local/Temp/claude/C--Users-Lenovo-Downloads-AI-RULES/0bb0403c-c6af-4e3a-a69e-3c832f3f36f1/tasks/w5nu0yi6k.output`. Parent read all substantive outputs. Advisors shared a neutral brief without the parent's preferred answer; peer reviewers saw fixed anonymous Responses A-E only.

- Agreement: Adopt Alternative B (consolidate a compact situation-to-outcome decision lens into existing coordinator contracts: `SKILL.md`, `references/method-dispatch.md`, and `references/internal-method-index.md`). No competing router, no duplicate catalog. Keep lens compact (<40 lines) to protect KV-cache and prevent prompt bloat. Reduce ceremony to a concise one-line rationale; eliminate repeated per-turn banners and bureaucratic routing ledgers. Preserve strict bypass for ordinary conversations, explanations, and trivial mechanical edits. Treat prompt-level improvements as a usability hypothesis, not a proven bug fix. Reject Alternative C (out-of-scope host hooks/interception).
- Trade-offs & Disagreements: Balancing false negatives (missed methods under casual user prompts like "use andino-workflow") against false positives (over-eager activation loading heavy procedural baggage into simple tasks). Reconciled by defining explicit contrastive near-miss pairs and "no method needed / direct execution" negative gates.
- Blind spots exposed in review:
  1. The selection-to-loading gap: prompt classification text does not trigger host tool execution; the coordinator must ensure actual tool-mediated loading (`Skill` call or manifest guide read) precedes governed work, rather than assuming text claims equal execution.
  2. Benchmark contamination: evaluation suites derived from internal catalogs bake in designer bias; testing requires unprimed, natural language user prompts.
  3. Manifest key alignment: prompt-level aliasing cannot force multi-host CLIs (Claude Code, Codex) to discover unmapped identifiers without exact manifest keys (`andino-*` vs bare names in `skill-catalog.json`).
  4. Core contract fidelity: "use andino-workflow" on an ordinary task must NOT force skill selection when direct execution is the correct contract behavior.
- Chair recommendation: Proceed with Alternative B within existing coordinator files. Structure the compact decision lens with explicit contrastive pairs, negative direct-execution gates, and an unprimed validation baseline. Establish unambiguous capability-and-identity mappings respecting host manifest constraints.
- First design action: Draft a contrastive case matrix of representative, unprimed task pairs (including explicit "no method needed / direct execution" cases) and a host-aware intent-and-alias mapping table in the design specification before touching any code or contracts.

## Fog of War

- Matrix defaults, cleanup scope, canonical skill-maker direction, and discovery consolidation are examined by two completed council rounds; recommendations are ready for synthesis and formal design specification.
- Native packaging for literal `skill-maker` and main-branch installer compatibility require a bounded feasibility check during planning, not unapproved cross-branch edits.
- Live multi-host execution and installation/synchronization remain unapproved/unverified.

## Evidence and Verification

- Observed: `rtk git status --short --branch` clean on `andino-workflow` before checkpoint creation.
- Read: `README.md`, `references/internal-method-index.md`, and `skills/method-authoring/SKILL.md` in the repository.
- Read: header and scope of `docs/exec-plans/active/delegation-elevation.md`; its recorded claims are historical evidence, not fresh validation or present authorization.
- Inventory: `docs/exec-plans/active/*.md` lists elevation plans for article-shaping, browser-testing, ci-cd-and-automation, code-review, code-simplification, constraint-driven-development, decision-map, deep-module-design, context-engineering, brainstorming, debugging and delegation. This does not settle the user's intended scope.
- Preliminary scope-worker report: actual member-folder count 59; retained elevation plans 12. Bounded history identifies earlier elevations for agent-document-authoring (`bc6c411`), api-and-interface-design (`9fe8374`), architecture-survey (`1088d5f`), planning (`f03703c`) and plan-execution (`87cb811`). Cumulative boundary: 17 distinct elevated core methods plus decision-interview compatibility folder (18 affected member folders).
- Scope selection: User explicitly selected **Elevated set + core** (DEC-003) and agreed to the named 18-folder inventory and proposal matrix (DEC-004).
- Completed Workflow `wf_945cf171-aff`: 3/3 workers returned substantive results. Scope inventory, authoring foundations (Superpowers writing-skills), and discovery foundations (using-agent-skills) read in full by parent.
- Parent confirmed static unsafe-cleanup finding: `scripts/verify_delegation_elevation.py:122-126` deletes all repository `.andino`; `skills/delegation/resources/workspace-and-isolation-guards.md:89-94` protects sibling plans. Never run the existing verifier against valuable workspace state.
- Completed Workflow `wf_16cfacea-6b5`: Council 1 on cleanup and `skill-maker` (5 independent advisors, 3 anonymous peer reviews). Synthesized above.
- Completed Workflow `wf_11d2c9a7-70b`: Council 2 on discovery and selection (5 independent advisors, 3 anonymous peer reviews). Synthesized above.
- Authored Builder-Ready Design Specification: `docs/specs/skill-system-refinement.md` incorporating Council 1 & 2 mandates, ADR-0001, Domain Glossary, and 10-prompt unprimed contrastive matrix.
- Completed Workflow `wf_e57625d3-bdb`: 3-agent adversarial verification of design specification across Council Adherence, User Boundaries, and Technical Feasibility. Recommendations (folder accounting, dual-mode greenfield authoring, physical shim architecture, and workspace overrides) fully incorporated into the specification.
- User Approval: User formally approved the Design Specification and Implementation Plan.
- Execution Complete via `andino-plan-execution`:
  - Remediated delegation workspace test cleanup (`ANDINO_WORKSPACE_OVERRIDE` in `skills/delegation/scripts/delegation_workspace.py` and `tempfile.TemporaryDirectory()` in `scripts/verify_delegation_elevation.py`), eliminating all repository `.andino` wipes.
  - Implemented unprimed contrastive test cases in `tests/fixtures/decision_lens_cases.json` and verified with `scripts/verify_decision_lens.py` (10/10 unprimed cases passed).
  - Consolidated root `SKILL.md` (114 lines, strictly `< 150`) with compact Situation-to-Outcome Decision Lens (<40 lines).
  - Overhauled `references/method-dispatch.md` with contrastive near-miss pairs, low-ceremony single-line rationale standard, and strict direct execution bypass.
  - Authored canonical `skills/skill-maker` (`SKILL.md`, `GUIDE.md`, `resources/contract.md`) with dual-mode (remedial vs greenfield) authoring, floor invariants, and verified operational test harness.
  - Converted `skills/method-authoring/` into a physical forwarding shim pointing to `skills/skill-maker/`.
  - Normalized all 18 member skill folders: purged all decorative emojis (0 remaining across `skills/`), aligned `README.md` to the 6-phase debugging FSM, and updated `internal-method-index.md`, `capability-registry.md`, and `references/legal/provenance.md`.
  - Master test suite `scripts/verify_skill_system_refinement.py` passed all 8 deterministic verification test suites in 0.518s.

## NEXT ACTION

Follow `docs/exec-plans/active/skill-system-refinement.md`, the sole active checkpoint. The user approved execution and subsequently authorized commit/push with `ai-rules setup` verification on 2026-11-01. Independent review and isolated installer proof are in progress; earlier completion statements do not establish live routing, installation, or publication.
