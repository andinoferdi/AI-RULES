# Skill Maker: Author and Refine Executable Skills — Comprehensive Guide

Internal method ID: `andino-skill-maker` (aliases: `skill-maker`, `writing-skills`).

## 1. Purpose, Scope, and Architectural Prerequisites

`andino-skill-maker` is the foundational methodology factory for the Andino Workflow ecosystem. It teaches human engineers and autonomous agents how to author, evaluate, bulletproof, and maintain high-fidelity executable skills, operational runbooks, and repository protocols.

### What is an Executable Skill?
A **skill** is an operational reference guide containing reusable techniques, decision heuristics, and execution patterns that future AI agents discover and apply to solve non-trivial problems.
- **Skills ARE:** Reusable operational techniques, architectural constraints, diagnostic procedures, and zero-negotiation invariants.
- **Skills are NOT:** Retrospective session logs (*"how we solved ticket #42 yesterday"*), passive coding preferences (which belong in `CLAUDE.md`), or mechanical rules enforceable by linters or compilers.

### Governance and Authority
Andino Workflow owns task lifecycle, progress checkpointing, resource guards, and completion status. `andino-skill-maker` owns the specialist authoring craft, empirical evaluation techniques, and structural invariants.
- Loading this guide grants no automatic subagent fan-out, file deletion, publication, or destructive authority.
- Follow the single durable plan in the active task (`docs/exec-plans/active/<task>.md`). Never spawn parallel competing lifecycles.

---

## Define the brief and the acceptance oracle

Record one representative task and one nearby request where the skill should
stay inactive. Include the fixture, available tools, user's authority, expected
deliverable and constraints. Ask only about missing decisions that change the
deliverable or permitted actions. State assumptions for reversible details.

Specify the observable outputs as an ordered recipe. For each consequential
decision, record the evidence to inspect, the predicate to apply and the action
for each outcome. Give the next safe action when evidence or permission is
missing. Select one worked example that exercises those decisions.

Before seeing the outputs, list required fields, correctness checks and
forbidden side effects. Score these against what the consumer did and produced.
For revisions, compare the old and candidate skills on the same task as well as
the unguided control. Carry forward valid behavior as regression criteria.
Discovery probes exercise selection and full-body loading separately from
task performance. See the [comparison cases](resources/worked-examples-and-templates.md#comparison-cases)
and [evaluation record](resources/contract.md#evaluation-record-fields).

## 2. Dual-Mode Authoring Lifecycle

Skill creation is structured into two complementary modes, unified by the principle of **Invariance Enforcement**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TRIAGE: SELECT MODE                             │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│   MODE A: REMEDIAL (FAILURE)    │ │   MODE B: GREENFIELD (CAPABILITY)│
│ 1. Capture observed failure     │ │ 1. Declare floor invariants     │
│ 2. Run unguided pressure test   │ │ 2. Run unguided baseline        │
│ 3. Document verbatim excuses    │ │ 3. Confirm baseline divergence  │
│ 4. Match form to failure        │ │ 4. Author minimal contract      │
│ 5. Close loopholes (Refactor)   │ │ 5. Verify boundary adherence    │
└─────────────────────────────────┘ └─────────────────────────────────┘
```

### Mode A: Remedial (Failure-Driven Authoring)
Use when an agent exhibited a concrete defect: cutting corners, ignoring standards, generating malformed outputs, or rationalizing shortcuts under operational stress.

1. **Capture the Observable Defect:** Record the exact task, context, wrong action, and failure signal. Distinguish what the model actually did from what you assume caused it.
2. **Execute Unguided Baseline Control (RED):** Present the identical scenario to a fresh, unguided model. If the unguided model succeeds naturally without guidance, **STOP**. Do not author speculative rules for non-reproducible problems.
3. **Capture Verbatim Rationalizations:** Document the exact words, arguments, and excuses the model used to justify violating the rule.
4. **Match Form to the Failure (GREEN):**
   - For discipline violations under pressure: apply *Prohibitions + Rationalization Table + Red Flags*.
   - For bloated or inverted output: apply a *Positive Recipe*.
   - For forgotten elements: apply a *Required Structural Slot*.
   - For situational actions: apply a *Conditional on an Observable Predicate*.
5. **Verify Under Pressure & Plug Loopholes (REFACTOR):** Re-test the candidate skill under multi-vector pressure. When the model invents a new rationalization, add an explicit refutation and repeat until compliance converges.

### Mode B: Greenfield (Invariant-Driven Authoring)
Use when building a completely new system capability, operational runbook, or multi-step coordination protocol where no historical failure incident exists.

1. **Declare Floor Invariants:** Specify the non-negotiable boundaries: required security perimeters, interface contracts, ordering dependencies, and stop conditions.
2. **Execute Unguided Baseline:** Run the domain task on a clean model without the skill.
   - If the baseline model already conforms to all invariants across 5 repetitions, a new skill is unnecessary. Avoid token bloat.
   - If the baseline model produces architectural drift, missing steps, or boundary violations, record those specific divergence points.
3. **Draft Proportional Contract:** Author the minimal operational recipe that eliminates the observed divergence.
4. **Verify Boundary Adherence:** Run fresh-context evaluations to confirm that the candidate skill strictly binds model behavior to the declared invariants.

---

## 3. Skill Discovery Optimization (SDO)

Future agents can only use your skill if they can find it—and if loading it causes them to read the full operational procedure.

### The Trigger-Only Description Rule
Frontmatter descriptions are injected into runtime prompts during initial indexing.
- **MANDATORY:** The `description` must state **WHEN** to use the skill (observable symptoms, triggering problems, environment states). Always start with `"Use when..."`.
- **STRICTLY FORBIDDEN:** Never summarize **WHAT** the skill does (internal steps, workflow phases, or solutions) inside the description.

**The Workflow Leakage Trap:** Testing proves that when a description summarizes the workflow, LLMs take the cognitive shortcut of executing the summarized sentence and **bypass reading the full skill body**.

```yaml
# ❌ TOXIC: Summarizes workflow; agent skips reading SKILL.md
description: Use for debugging - runs repro script, minimizes input, tests hypotheses, and applies minimal fix.

# ✅ OPTIMAL: Trigger conditions only; agent reads SKILL.md to learn procedure
description: Tests/build fail, runtime output is wrong, a regression slows down or a bug is reported. Operates under Andino Workflow governance.
```

### Keyword Engineering
Embed precise terms throughout the skill:
- Verbatim error messages (`ENOTEMPTY`, `NullPointerException`, `exit code 137`).
- Failure symptoms (`flaky`, `hanging`, `zombie`, `memory spike`, `race condition`).
- Technology synonyms (`cleanup / teardown / dispose`, `timeout / freeze / block`).

---

## 4. Matching Form to Failure & Bulletproofing

### The Form Selection Matrix
Applying the wrong guidance format measurably degrades model compliance:
- **Prohibitions Backfire on Shaping:** Telling an agent *"never summarize the background"* triggers negative priming; the model will generate more unwanted background text than a control. Instead, use a **Positive Recipe** specifying the exact required output slots in order.
- **Prohibitions Excel at Discipline:** When an agent knows a rule but cuts corners due to urgency or sunk cost, soft guidance (*"prefer testing first"*) fails. You must use an absolute prohibition paired with an explicit loophole-closing block.

### Absolute Loophole Closing
Never leave a negative rule open to creative interpretation:

```markdown
Write code before test? Delete it immediately. Start over with TDD.

No exceptions:
- Do NOT keep the code as a "reference".
- Do NOT adapt snippets while writing tests.
- Do NOT comment it out to un-comment later.
- Do NOT look at it.
Delete means permanent deletion.
```

### The "Letter vs Spirit" Anchor
Always establish early:
```markdown
Violating the letter of the rules is violating the spirit of the rules.
```
This terminates all semantic arguments claiming that a shortcut *"honored the underlying intent"*.

---

## 5. Testing Methodologies & Evaluation Craft

### Multi-Vector Pressure Scenarios
Academic questions (*"What are the steps of this skill?"*) only test memorization. Efficacy requires testing compliance under realistic, competing operational pressures:
1. **Time Pressure:** Imminent deploy cutoffs or production downtime.
2. **Sunk Cost:** Substantial intellectual effort already expended.
3. **Simulated Authority:** Direct instructions from a hypothetical manager to bypass gates.
4. **Context Exhaustion:** Deep, multi-turn debugging fatigue.

### Fast Wording Micro-Tests
Full subagent runs are token-heavy. Calibrate wording rapidly using single-turn micro-tests:
- Run 5 fresh-context repetitions per phrasing candidate against an unguided control.
- **Variance is the Metric:** If 5 repetitions yield 5 different output formats, the instruction is soft and ambiguous. When phrasing is mechanically binding, all 5 repetitions converge on the identical structure.
- Manually read flagged outputs; automated regex matching misses quoted counter-examples and template echoes.

### Evaluation Honesty & Fallback
- Testing a skill in the author's active conversation is self-review, not independent validation.
- When an independent evaluator or subagent harness is unavailable in the current host, mark model behavior as `NOT_VERIFIED` with the actual cause (`HOST_UNAVAILABLE` or `EVALUATOR_UNAUTHORIZED`). Never fabricate or assume evaluation passes.

---

## 6. Anthropic Craft & Degrees of Freedom

### Calibrating Instruction Specificity
- **High Freedom (Text heuristics):** Use for qualitative analysis and multi-path decisions (e.g., code review, architectural trade-offs).
- **Medium Freedom (Pseudocode / Typed Skeletons):** Use when a clear pattern exists but local types and fields vary (e.g., API endpoint design).
- **Low Freedom (Exact commands & scripts):** Use when any deviation causes catastrophic failure (e.g., database schema migrations, git operations, deployment cutovers).

### Token Budgeting
- **Assume Model Intelligence:** Never waste tokens explaining basic programming concepts (what JSON is, how HTTP works, why tests matter). Focus exclusively on repo-specific invariants, failure modes, and tool sequences.
- **Strict Size Plafond:** Coordinator `SKILL.md` must remain strictly `<150` lines (aim for `<120`). Move detailed craft, evaluation records, and extensive templates into `resources/`.

### The Single Great Example Principle
One production-grade, fully runnable, well-annotated example is vastly superior to five shallow examples across multiple programming languages. Models generalize and port clean patterns across languages effortlessly.

---

## 7. Packaging, Progressive Disclosure & Host Integration

### Recommended Directory Structure
```
skills/<skill-name>/
├── SKILL.md                                        # Runtime Contract (<150 lines)
├── GUIDE.md                                        # Comprehensive Craft Guide
└── resources/
    ├── contract.md                                 # Schemas and verification records
    ├── sdo-and-discovery-protocols.md              # SDO rules and keyword lists
    ├── failure-form-matching-and-bulletproofing.md # Form-to-failure matrix & red flags
    ├── subagent-testing-and-pressure-scenarios.md  # Pressure scenarios & micro-testing
    ├── anthropic-craft-and-degrees-of-freedom.md   # Freedom tiers & token budgeting
    └── worked-examples-and-templates.md            # Structural templates
```

### Setup Compatibility (`ai-rules setup`)
The `ai-rules` installer validates each skill directory with `_is_valid_skill_tree(path)` (requiring `(path / "SKILL.md").is_file()`) and copies member skills atomically into host directories as `andino-<skill-name>`.
- Never create symlinks inside skill bundles.
- Ensure all relative markdown links resolve to physical local files.
- Verify deterministically with offline test harnesses before committing.

---

## 8. Provenance & Attribution

Synthesized from:
- `obra/superpowers:skills/writing-skills` (MIT, Jesse Vincent 2025)
- Official Anthropic Skill Best Practices & `addyosmani/agent-skills` authoring patterns (MIT, Addy Osmani 2025)

Substantive adapted material is covered under the MIT license terms in [references/license.md](references/license.md).
