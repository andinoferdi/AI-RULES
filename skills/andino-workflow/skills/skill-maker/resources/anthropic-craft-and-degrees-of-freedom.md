# Anthropic Craft, Degrees of Freedom, and Token Efficiency

Supporting craft protocol for `andino-skill-maker`. Read with [SKILL.md](../SKILL.md) and [GUIDE.md](../GUIDE.md).

## 1. Calibrating Degrees of Freedom

Match the specificity of instructions to the inherent fragility and risk of the task. Over-constraining heuristic tasks stifles model reasoning; under-constraining fragile tasks causes catastrophic execution failures.

```
HIGH FREEDOM ───────────────▶ MEDIUM FREEDOM ───────────────▶ LOW FREEDOM
Text heuristics,             Pseudocode, parameterized       Exact executable scripts,
guiding principles           templates, scaffold patterns    non-negotiable sequences
(e.g., Code Review)          (e.g., Component Scaffolding)   (e.g., DB Migration, Git)
```

| Freedom Tier | Operational Scope | When to Apply | Recommended Instruction Format |
| :--- | :--- | :--- | :--- |
| **High Freedom** | Heuristics & Analysis | Multiple paths are valid; decisions depend heavily on codebase style and subjective trade-offs. | Ordered qualitative checklist with evaluation criteria. |
| **Medium Freedom** | Structured Generation | A clear preferred pattern exists, but local parameters and types vary by domain. | Typed skeleton, interface signatures, or parameterized templates. |
| **Low Freedom** | Fragile / Risky Operations | Any deviation causes silent data loss, corrupt git state, or security breaches. | Exact, copy-pasteable commands and non-negotiable deterministic scripts. |

---

## 2. Token Budgeting: Context is a Public Good

The active context window is a scarce shared resource. Every token in a skill competes directly with conversation memory, file contents, tool outputs, and the user's primary prompt.

### The Default Assumption: "The Model is Already Smart"
Never spend tokens teaching a frontier model what it already knows from pre-training.
- **Do NOT Explain:** What JSON is, why unit tests are good, how HTTP verbs work, what a PDF container consists of, or how to import standard libraries.
- **DO Explain:** Repo-specific invariants, non-obvious failure modes, exact boundary conditions, required interface schemas, and mandatory tool call sequences.

```markdown
<!-- ❌ BAD: Token Bloat (Explaining the Obvious) -->
JSON (JavaScript Object Notation) is a lightweight data-interchange format.
To parse JSON in Python, you must import the json module and call json.loads().
Make sure to handle JSONDecodeError in case the data is corrupted...

<!-- ✅ GOOD: High-Density Craft (Focused on Invariants) -->
Parse worker payloads with `json.loads(raw)`. Wrap in schema validator;
reject missing `task_id` with `ValidationError(code="INVALID_TASK_PAYLOAD")`.
```

---

## 3. The "Single Great Example" Principle

One complete, runnable, well-annotated production example is vastly superior to five shallow, hypothetical templates across multiple programming languages.

### Rules for Example Construction
1. **From a Real Scenario:** Ground the example in a genuine problem domain, not a synthetic `foo()` / `bar()` toy case.
2. **Annotate the "Why":** Comments should explain the non-obvious engineering decisions and trade-offs, not restate the obvious syntax.
3. **Language Selection:** Pick the language most idiomatic for the task:
   - System & debugging tools: Shell, Python.
   - Web & frontend architectures: TypeScript, React.
   - Systems & performance: Rust, Go.
   LLMs translate clean code across languages effortlessly; they do not need multi-language boilerplate.
4. **Invoke Scripts Through Interpreters:** Always write `python scripts/tool.py` or `node scripts/tool.js` rather than bare `./scripts/tool.py` to prevent executable-bit permission failures across platforms.

---

## 4. The Anti-Patterns Catalog

Audit candidate skills against these documented failure patterns:

### Anti-Pattern 1: Retrospective Session Narratives
- **Defect:** Writing *"In session 2026-10-02, we discovered that the pool connection leaked when Redis timed out..."*.
- **Fix:** Extract the general rule: *"When connection timeouts occur, verify that pool sockets are explicitly reclaimed in an exception block."*

### Anti-Pattern 2: Multi-Language Dilution
- **Defect:** Providing `example-py.py`, `example-js.js`, `example-go.go`, and `example-rs.rs` all demonstrating the identical basic concept.
- **Fix:** Keep a single, high-fidelity example in the primary ecosystem language.

### Anti-Pattern 3: Code Inside Diagram Shapes
- **Defect:** Placing multi-line code or bash commands inside Mermaid or Graphviz flowchart boxes.
- **Fix:** Diagrams illustrate decision trees and state loops. Code belongs in standard syntax-highlighted code blocks.

### Anti-Pattern 4: Meaningless Generic Identifiers
- **Defect:** Naming nodes or functions `step1`, `helper2`, `process_data()`, or `handle_it()`.
- **Fix:** Use domain-semantic identifiers: `validate_payload_schema()`, `acquire_lock()`, `circuit_breaker_open`.

### Anti-Pattern 5: Mechanical Rules in Prose
- **Defect:** Writing 100 lines of prose instructing agents to format code, place semicolons, or avoid unused imports.
- **Fix:** Automate mechanical rules using linters, formatters, and pre-commit hooks. Reserve skills for judgment calls and complex workflows.
