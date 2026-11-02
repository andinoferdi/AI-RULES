# Agent Document Authoring: Complete Method Guide

Internal method ID: `andino-agent-document-authoring` (aliases: `agent-document-authoring`, `writing-for-agents`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow protocol: single durable checkpoint, proportional investigation, anti-loop guards.
> Loading this file does not invoke another skill or mutate repository state. Upstream references yield to current policy.

---

## 1. Executive Purpose

The purpose of `andino-agent-document-authoring` is to make agent-consumed instructions predictable, exhaustive, and token-efficient. Whether authoring a root `CLAUDE.md` / `AGENTS.md`, an internal repository runbook, or a modular context pointer file, model behavior is governed by shared cognitive and structural levers: the agent must take the same reliable *process* across runs rather than generating accidental output.

Activate for: Creating, refactoring, or auditing any agent-facing instruction, guidance file, context pointer, or durable operational procedure.

Do not activate for: Executable skills with step-by-step TDD (use `skill-maker`), durable architectural decisions (use `documentation-and-adrs`), or routine code edits enforceable by linters.

---

## 2. Foundational Cognitive Levers

Agent instruction design operates across four foundational mechanics:

### The Two Loads
Every line of guidance written spends one of two finite budgets:
- **Context Load:** The cost of always-loaded material on the agent's attention window (`CLAUDE.md`, top-level system prompts, skill descriptions). It burns tokens and dilutes model attention on *every single conversation turn*, whether fired or not.
- **Cognitive Load:** The cost on the human index: remembering which files exist and when to dispatch them. It is the necessary price of human agency. Spend it where human judgment is required; automate or point where it is not.

Material reached only through a context pointer escapes context load at the price of the pointer's own single line.

### The Information Hierarchy Ladder
Organize document content into a strict three-tier ladder ranked by immediacy:
1. **Tier 1 (In-File Steps):** Ordered, sequential actions the agent must execute. Must remain immediately visible and unburied.
2. **Tier 2 (In-File Reference):** Flat peer sets of rules, definitions, and invariants consulted while executing steps across all branches.
3. **Tier 3 (Disclosed Reference):** Specialized detail, branch-specific edge cases, and heavy reference tables pushed behind precision context pointers.

*Progressive disclosure* moves non-universal reference down the ladder to protect the visibility of steps. *Co-location* ensures that a concept's definition, rules, and caveats sit under a single heading rather than scattering across distant files. *Sprawl* occurs when excess reference thins attention across lines, turning step execution into a coin-flip.

### Demanding Observable Bounds and Anti-Premature Completion
Vague bounds (*"understand the code"*, *"analyze thoroughly"*) trigger **premature completion**—the agent rushes to finish because visible upcoming steps (**post-completion steps**) exert an attentional pull.
- **Clarity:** The criterion must cleanly discriminate done from not-done with mathematical certainty (binary observable predicates).
- **Demand:** The criterion must enforce legwork (*"every modified model accounted for"* vs *"list changes"*). The highest-quality criteria are both checkable and exhaustive.

### Positive Target Steering vs. The Negation Trap
Steering by prohibition (*"do not do X"*) drags the forbidden behavior into context, making it more salient—*don't think of an elephant*. Prompt the **positive target behavior** (*"write flat functions under 25 lines"*) so the forbidden concept is never activated. Reserve prohibitions for non-negotiable safety guardrails, and always pair them with the approved positive alternative.

---

## 3. Operational Refactoring Protocol

When refactoring a legacy or bloated document, execute five sequential passes:

1. **Pass 1 — Strip Environment Caching:** Grep for command explanations, directory layouts, and CLI flag documentation easily discovered via `--help` or `package.json`. Delete them.
2. **Pass 2 — Sentence-by-Sentence No-Op Purge:** Audit every sentence against the model-relative default test. Delete generic pleasantries (*"be thorough"*, *"think carefully"*, *"write clean code"*).
3. **Pass 3 — Positive Target Steering:** Identify every prohibition (*"do not"*, *"never"*). Rewrite it into the required positive target action.
4. **Pass 4 — Disclose Branch References:** Extract multi-line edge-case branches and platform-specific variations into separate files under `resources/`. Replace them with precision context pointers.
5. **Pass 5 — Attach Demanding Observable Bounds:** Replace every subjective termination phrase (*"ensure it works"*) with an observable binary predicate (exit code 0, file existence, schema assertion).

---

## 4. Modular Resources Directory

For specialized authoring techniques, consult the corresponding modular resource:

- [contract.md](resources/contract.md): Formal data contract, document schemas, and the 5-point diagnostic evaluation rubric.
- [context-pointer-and-leading-words.md](resources/context-pointer-and-leading-words.md): Mechanics of context pointers, trigger front-loading, leading words catalog, and defeating the negation trap.
- [information-hierarchy-and-progressive-disclosure.md](resources/information-hierarchy-and-progressive-disclosure.md): 3-tier ladder, progressive disclosure branching test, co-location vs scattering, sprawl prevention, and multi-file structures.
- [demanding-completion-bounds-and-legwork.md](resources/demanding-completion-bounds-and-legwork.md): Post-completion pull dynamics, clarity vs demand, forcing legwork through latent phrasing, and observable binary predicates catalog.
- [pruning-and-no-op-hunting.md](resources/pruning-and-no-op-hunting.md): SSOT enforcement, environment as live truth vs redundant caching, sediment excavation, and sentence-by-sentence no-op elimination.
- [agent-document-templates-and-runbooks.md](resources/agent-document-templates-and-runbooks.md): Ready-to-use production templates for `CLAUDE.md`, `AGENTS.md`, router skills, worked before-and-after case study, and 5-minute refactoring runbook.

---

## 5. Provenance and Governance

Independently adapted for the Andino Workflow runtime and multi-harness agent architectures from audited snapshot principles in:
- `mattpocock/skills:skills/productivity/writing-for-agents/SKILL.md`
- `mattpocock/skills:skills/productivity/writing-for-agents/SKILL-MECHANICS.md`

Upstream concepts are integrated with Andino runtime execution contracts, deterministic verification boundaries, and multi-host resilience standards. Substantive adapted material is covered by the packaged MIT notice ([references/license.md](references/license.md)).
