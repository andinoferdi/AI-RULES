---
name: andino-agent-document-authoring
description: Creating/reviewing an agent-facing guide, instruction pointer or durable procedure. Operates under Andino Workflow governance.
---

# Write documents agents can use

Internal method ID: `andino-agent-document-authoring` (alias: `agent-document-authoring`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Make agent-consumed documents predictable, exhaustive, and token-efficient. Whether authoring a skill, an internal method guide, an `AGENTS.md` / `CLAUDE.md`, or a reference file reached by a pointer, agent behavior is governed by shared cognitive and structural levers: the agent must take the same reliable *process* every run rather than producing accidental output.

Activate for: Creating, refactoring, or auditing any agent-facing instruction, skill document, context pointer, or durable procedure.

Do not activate for: Stylistic compression that deletes technique, superficial formatting edits, or creating unauthorized native skills / rogue router systems outside Andino governance.

## Inputs and dependencies

Consumer use case and failure modes, existing document hierarchy, environment conventions, target tool interfaces, and observable acceptance criteria.

Use resources progressively: [worked procedure and example](resources/worked-example.md). It provides before-and-after transformations, the 5-point diagnostic audit rubric, and a deterministic local validation suite.

---

## Core mental models

Agent instruction design operates across three foundational mechanics:

### 1. The Two Loads
Every line written spends one of two finite budgets:
- **Context load:** Cost of always-loaded material on the agent's attention window (skill descriptions, `AGENTS.md`, top-level system prompts). It burns tokens and dilutes attention on *every single turn*, whether fired or not.
- **Cognitive load:** Cost on the human index: remembering which files exist and when to dispatch them. It is the necessary price of human agency. Spend it where human judgment is required; automate or point where it is not.

### 2. Information Hierarchy Ladder
Organize document content into a strict three-tier ladder ranked by immediacy:
1. **In-file steps (Primary tier):** Ordered, sequential actions the agent must perform. Keep these legible and unburied.
2. **In-file reference (Consulted on demand):** Flat peer sets of rules, definitions, and invariants consulted while executing steps.
3. **Disclosed reference (Secondary tier):** Specialized detail, branch-specific edge cases, and heavy reference files pushed behind a context pointer and loaded only when that branch triggers.

*Progressive disclosure* moves non-universal reference down the ladder to protect the visibility of steps. *Co-location* ensures that a concept's definition, rules, and caveats sit under a single heading rather than scattering across the document. *Sprawl* occurs when excess reference thins attention across lines, turning step execution into a coin-flip.

### 3. Steps and Demanding Completion Criteria
Vague bounds ("understanding reached", "analyze thoroughly") trigger **premature completion**—the agent rushes to finish because visible upcoming steps (**post-completion steps**) exert an attentional pull.
- **Clarity:** The criterion must cleanly discriminate done from not-done.
- **Demand:** The criterion must enforce legwork ("every modified file accounted for" vs "list changes"). The highest-quality criteria are both checkable and exhaustive.

---

## Procedure

### 1. Design precision context pointers
A **context pointer** names an out-of-context resource and encodes the precise conditions for reading it. The wording of the pointer—not the content of the target—decides whether the agent reaches it.
- **Front-load the leading word:** Place the primary conceptual trigger at the very beginning of the pointer line.
- **One trigger per distinct branch:** Collapse synonymous trigger phrases. Multiple words describing the same branch inflate context load without increasing routing accuracy.
- **Prune redundant identity:** Never state what the body already establishes once reached.

### 2. Stratify into steps and reference
Separate what the agent *does* from what it *consults*.
- Inline what every execution path requires.
- Push branch-specific rules behind local pointers.
- When a document contains sequential steps, never let inline reference bury them. If post-completion pull causes premature completion on an irreducibly fuzzy step, split the sequence across a context boundary (e.g., subagent dispatch or handoff).

### 3. Establish observable, demanding completion bounds
Attach an explicit, checkable completion criterion to every sequential step.
- Require concrete observable evidence (a test assertion, a generated file, an exact AST node match, a command return code).
- Set the bar high enough that the agent cannot declare success while skipping required verification.

### 4. Recruit model priors with leading words
A **leading word** is a compact concept already established in the model's pretraining (*tight loop*, *tracer bullet*, *red-green*, *SSOT*, *sediment*).
- Use compact pretrained tokens to anchor complex behaviors in minimal tokens.
- Hunt for multi-word descriptions that can collapse into a single sharp token.
- **Defeat the Negation Trap:** Steering by prohibition ("do not use complex abstractions") drags the forbidden behavior into context, making it more salient—*don't think of an elephant*. Prompt the **positive target behavior** ("write flat functions") so the forbidden concept is never activated. Reserve prohibitions for hard, non-negotiable safety guardrails, and always pair them with the approved positive alternative.

### 5. Prune relentlessly: Single source of truth, cache, and no-ops
- **Single Source of Truth (SSOT):** Author each meaning in exactly one place. Duplication inflates token cost and creates synchronization bugs.
- **Environment vs. Cache:** The filesystem, `package.json`, git history, and `--help` output are sources of truth. A document restating them is merely a **cache**. Cache only what the agent cannot discover by inspecting the environment (the unwritten rule, the rationale, the invisible gotcha).
- **Sediment removal:** Eliminate obsolete historical layers that accumulate over time.
- **Sentence-by-sentence no-op hunting:** If an instruction describes behavior the model already performs by default (or if removing the line does not alter output quality), delete the entire sentence.

### 6. Enforce runtime execution contracts
Treat the document not as loose prose, but as an executable runtime contract:
- **Checkpoint-readiness:** Structure progress so work can resume after context eviction or handoff without reading conversation history.
- **Tool-budget & loop awareness:** Explicitly bound retries (e.g., maximum 2 attempts with backoff) to prevent infinite repair loops.
- **Multi-harness portability:** Ensure instructions operate cleanly whether running under Antigravity, Codex, Claude Code, or OpenCode without relying on host-specific idiosyncratic assumptions.

### 7. Perform empirical diagnostic verification
Verify the document against positive and negative test cases:
- Test whether positive triggers fire reliably.
- Test whether negative/out-of-scope requests are cleanly rejected.
- Execute local deterministic examples to ensure instructions produce verifiable artifacts.

---

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-agent-document-authoring` and this guide expose one method, without recursive workflow invocation.

All authoring operations respect existing repository permissions. Examples use temporary, disposable data. Real git mutations, external writes, credential modifications, and global installations require explicit user authorization.

## Outputs and verification

A successful agent document satisfies five verification criteria:
1. **Pointer integrity:** Pointers are front-loaded, deduplicated, and resolve to accessible local paths.
2. **Hierarchy clarity:** Steps and reference are distinctly separated; sequential steps remain prominently visible.
3. **Bound demand:** Completion criteria are checkable, observable, and prevent premature completion.
4. **Positive formulation:** Target behaviors are stated positively; negations are limited to strict safety boundaries.
5. **No-op & sediment free:** Every sentence actively changes model behavior; environment data is not redundantly cached.

Run the companion verification suite in `resources/worked-example.md` to confirm artifact generation and deterministic compliance.

## Example and anti-patterns

### Positive request:
“Refactor this monolithic deployment guide into an ordered operational sequence with demanding completion criteria, pushing platform-specific edge cases behind progressive disclosure pointers.”

### Negative request:
“Compress this instruction by stripping out the completion criteria and mental models to save lines.”

### Anti-patterns:
- **Pedagogy trap / Sprawl:** Pasting human-oriented essays or decorative metaphors that dilute agent attention without altering decision boundaries.
- **Negation cascade:** Defining procedures entirely through negative prohibitions (*don't do X, don't do Y*), triggering the elephant in context.
- **Environment shadowing:** Writing multi-line instructions summarizing command flags easily discovered via `--help` or config inspection.
- **Fuzzy bounds:** Terminating steps with unverifiable states like "ensure code looks clean" instead of "zero linter errors and tests green".
- **Dead disclosure:** Fragmenting essential core steps into obscure secondary files that agents overlook during execution.

## Fallback

If fresh-context multi-agent testing is unavailable, run the local deterministic artifact generator in `resources/worked-example.md` and perform a line-by-line manual audit against the 5-point verification criteria.

## Provenance

Independently adapted for the Andino Workflow runtime and multi-harness agent architectures from audited snapshot principles in:
- `mattpocock/skills:skills/productivity/writing-for-agents/SKILL.md`
- `mattpocock/skills:skills/productivity/writing-for-agents/SKILL-MECHANICS.md`

Upstream concepts are integrated with Andino runtime execution contracts, deterministic verification boundaries, and multi-host resilience standards.
