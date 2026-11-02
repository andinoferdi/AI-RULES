# Pruning Discipline and Sentence-by-Sentence No-Op Hunting

Internal method ID: `andino-agent-document-authoring` resource: `pruning-and-no-op-hunting.md`.

---

## 1. Single Source of Truth (SSOT)

Every operational meaning, constraint, and rule must live in **exactly one authoritative place**.

- **Duplication is a Variance Bug:** Writing the same rule in both `CLAUDE.md` and a sub-skill means that when the rule evolves, one copy will inevitably be left behind. Discrepant instructions cause random behavioral variance across runs.
- **Inflated Ladder Prominence:** Repeating a secondary rule multiple times gives it artificial attentional salience, causing the model to prioritize a minor detail over primary operational steps.
- **Leading Words vs. Duplication:**
  - *Leading Word:* Deliberately repeats a single compact token (e.g. *red*, *tight*) across documents to recruit shared latent priors.
  - *Duplication:* Accidentally repeats an entire explanatory meaning or instruction block across multiple locations.

---

## 2. Environment as Truth vs. The Caching Trap

The local environment—filesystem hierarchy, `package.json`, `--help` outputs, compiler errors, and git history—is a live, authoritative source of truth.

A document that restates what the environment already provides for free is merely an **unreliable cache**:

```
[ Authoritative Environment ]                     [ Documentation Cache ]
  package.json ("test": "vitest")    <---restated as--->   "To run tests, type npm test"
  tsconfig.json (target: "ES2022")   <---restated as--->   "We compile to ES2022"
```

### The Caching Rule
Cache only what the agent **cannot discover by inspecting the environment**:
- The unwritten architectural invariant.
- The historical rationale behind an otherwise counter-intuitive design choice.
- The invisible gotcha that no error message confesses.

Leave one-command lookups, directory listings, and CLI flag summaries to the environment, where they cannot go stale.

---

## 3. Sediment Excavation Protocol

**Sediment** consists of obsolete historical layers that accumulate in agent documents over time. Sediment forms because adding guidance feels safe (*"let's add a reminder for this bug"*) while deleting guidance feels risky. Over months, documents turn into geological strata of dead rules.

### The 4-Step Excavation Drill
1. **Identify the Historical Trigger:** When was this line written? Was it responding to a transient bug or a one-time migration?
2. **Inspect Current Tooling:** Has the compiler, linter, or test suite made this rule redundant? If a linter now catches the error, delete the documentation rule immediately.
3. **Verify Active Reach:** Does any active branch or workflow still encounter this situation?
4. **Ruthless Purge:** If the condition is historical or already automated, delete the entire section.

---

## 4. Sentence-by-Sentence No-Op Hunting

A **no-op** is an instruction that the model already obeys by default. Writing a no-op spends context load to achieve zero behavioral change.

### The Model-Relative Baseline Test
Whether a sentence is a no-op is strictly **model-relative, not reader-relative**:

$$\text{Behavioral Delta} = \text{Output}(\text{Prompt with Line}) - \text{Output}(\text{Prompt without Line})$$

- If $\text{Behavioral Delta} = 0$, the line is a no-op.
- You do not settle no-ops through debate; you settle them by observing the model running the task with and without the line.

### The Deletion Protocol
When a sentence fails the test: **delete the entire sentence**. 
Do not attempt to salvage a no-op by trimming words, softening clauses, or rephrasing prose. Deleting the entire sentence clears attention bandwidth for decision-bearing rules.

### Common No-Op Anti-Patterns Catalog

| No-Op Anti-Pattern | Why It Fails the Baseline Test | Required Action |
| :--- | :--- | :--- |
| "Please think carefully and be thorough." | Modern models already attempt thoroughness by default. "Be thorough" is too weak to alter sampling distributions. | **Delete sentence.** (If intense legwork is required, use a demanding completion bound instead). |
| "Ensure code is clean, well-structured, and readable." | Generic platitude that alters zero decision boundaries. | **Delete sentence.** |
| "Analyze the requirements before proceeding." | Every reasoning model runs an analysis pass automatically. | **Delete sentence.** |
| "Output your response in clean markdown." | Default behavior in virtually all contemporary frontier models. | **Delete sentence.** |
| "Do your best to minimize errors." | Non-actionable pleasantry with zero mechanical leverage. | **Delete sentence.** |

### Upgrading Weak Leading Words
If an instruction addresses a real failure mode but uses a token too weak to beat model inertia (*"be careful"* or *"be thorough"*), the fix is not more prose—the fix is a **stronger leading word**:
- Replace *"be careful with edge cases"* $\rightarrow$ **"adversarial boundary verification"**.
- Replace *"run tests frequently"* $\rightarrow$ **"tight loop"**.
