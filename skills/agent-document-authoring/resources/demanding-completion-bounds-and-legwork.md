# Demanding Completion Bounds and Forcing Legwork

Internal method ID: `andino-agent-document-authoring` resource: `demanding-completion-bounds-and-legwork.md`.

---

## 1. The Mechanics of Completion Criteria

Every procedural step in an agent document must terminate on a **completion criterion**—an explicit observable condition that tells the agent whether the current step is finished.

A completion criterion operates along two distinct mechanical dimensions:
1. **Clarity:** Can the agent distinguish *done* from *not-done* with absolute mathematical certainty?
2. **Demand:** How much thoroughness, research, and validation does the criterion force the agent to perform before declaring completion?

```
                     High Demand
                          ^
                          |   [ THE GOLD STANDARD ]
       [ Blind Slogging ] |   Checkable & Exhaustive
       Heavy legwork with |   (e.g., "All 42 API routes covered
       ambiguous bounds   |   with integration tests; exit 0")
                          |
  Low Clarity <-----------+-----------> High Clarity
                          |
      [ PREMATURE FAILURE]|   [ The Shallow Pass ]
      Fuzzy & Weak        |   Easily checked, but skips
      (e.g., "Check code  |   necessary legwork
      thoroughly")        |   (e.g., "Run linter")
                          v
                     Low Demand
```

---

## 2. Preventing Premature Completion

### The Post-Completion Suction Effect
When an agent reads a multi-step document, visible upcoming steps exert an attentional pull known as **post-completion pull**. The agent's attention slips from *doing the work* to *being done*.

- If a step ends on a fuzzy bound (*"Verify that the architecture makes sense"*), the agent resolves the ambiguity in favor of speed. It generates a superficial conversational confirmation and rushes immediately to the next step.
- **The Remedy:** The criterion's **clarity** is the barrier that resists this suction. When the bound is binary and observable, the model cannot hallucinate completion.

### The Defense Escalation Protocol
When you observe an agent rushing past a critical step:
1. **Sharpen the bound first:** Replace subjective adjectives with falsifiable predicates (local, instantaneous, zero token cost).
2. **Increase demand:** Require positive evidence for every item in scope (e.g., *"every changed function has a corresponding test case"*).
3. **Isolate across a context boundary:** If the step is irreducibly fuzzy or requires extensive exploratory judgment, split the sequence across an independent subagent dispatch or execution phase so the remaining steps are invisible during execution.

---

## 3. Forcing Legwork Through Latent Demand

**Legwork** refers to the deep investigative digging, cross-referencing, and edge-case hunting that an agent does *within* a task.

You do not need to write 10 micro-steps instructing the agent how to dig. Instead, you encode the requirement for legwork directly into the **demand of the completion criterion**:

| Shallow Criterion (Encourages Shortcuts) | Demanding Criterion (Forces Deep Legwork) |
| :--- | :--- |
| "Produce a list of modified models." | "Identify all modified models. Done only when every foreign key relationship across the schema graph is cross-checked against database migrations." |
| "Check if the API handles errors." | "Done when negative integration tests assert exact HTTP status codes (400, 401, 403, 404, 422, 500) with matching error payloads." |
| "Review changed files for style issues." | "Done when every line in `git diff --name-only` is audited against the 5 floor invariants and zero unhandled edge cases remain." |

### Demand Binds Flat Reference
Demand is not limited to sequential steps. An all-reference document (such as a security checklist or code review guide) enforces legwork through an **exhaustiveness bar**:

> *"Audit the target interface against every rule in Section 3. Done only when an explicit pass/fail verdict with file and line evidence is rendered for every single listed invariant."*

---

## 4. Observable Binary Predicates Catalog

Never terminate a step with subjective language (*"ensure code is clean"*, *"verify performance feels fast"*, *"make sure edge cases are handled"*). Use these observable binary predicates:

| Task Type | Subjective Anti-Pattern | Observable Binary Predicate |
| :--- | :--- | :--- |
| **Test Verification** | "Run test suite and ensure everything passes." | `npm test` terminates with returncode `0`, `0` failing tests, and $>0$ assertions run. |
| **Working Tree Cleanliness** | "Make sure git repository is clean." | `git status --porcelain` emits exactly `0` lines of output. |
| **Build Artifact Generation** | "Compile the binary properly." | `test -f dist/server.bundle.js` returns true, and `file dist/server.bundle.js` confirms non-empty ELF/Mach-O/JS bundle. |
| **Schema Validation** | "Check that JSON matches format." | `jsonschema -i output.json schema.json` exits code `0` with zero validation errors. |
| **Linter Enforcement** | "Fix any styling issues in code." | `eslint --max-warnings 0 src/` exits `0` with zero errors and zero warnings. |
| **API Health Check** | "Ensure backend server is running." | `curl -f -s -o /dev/null -w "%{http_code}" http://localhost:8080/health` returns `200`. |
