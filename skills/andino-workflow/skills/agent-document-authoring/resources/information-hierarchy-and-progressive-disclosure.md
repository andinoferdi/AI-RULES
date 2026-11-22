# Information Hierarchy and Progressive Disclosure

Internal method ID: `andino-agent-document-authoring` resource: `information-hierarchy-and-progressive-disclosure.md`.

---

## 1. The Information Hierarchy Ladder

Every agent instruction document is constructed from two fundamental content types:
1. **Steps:** The ordered, sequential actions the agent must execute.
2. **Reference:** The flat peer sets of rules, definitions, constraints, and invariants consulted on demand.

The central design decision when authoring agent documents is determining where each piece of information sits on the **Information Hierarchy Ladder**, ranked by immediacy:

```
[ Tier 1: In-File Steps (Primary Tier) ]
        Ordered execution path. Must remain immediately visible and unburied.
                       |
                       v
[ Tier 2: In-File Reference (Consulted on Demand) ]
        Flat peer rules, schemas, definitions applicable across ALL branches.
                       |
                       v
[ Tier 3: Disclosed Reference (Secondary Tier) ]
        Branch-specific edge cases, deep diagnostics, large tables pushed behind context pointers.
```

### The Tension at the Core of the Ladder
- **Push too little down:** The root document bloats into an unreadable monolith (**Sprawl**). Attentional weight spreads thin, and the execution of basic steps becomes a coin-flip.
- **Push too much down:** Essential invariants are hidden behind pointers the agent overlooks (**Dead Disclosure**). The agent skips required checks because it never opens the secondary file.

---

## 2. Progressive Disclosure

**Progressive disclosure** is the deliberate movement of specialized detail down the ladder—out of the primary file and behind a precision context pointer.

### The Branching Test for Disclosure
The cleanest test for whether reference belongs in the primary file or behind a disclosed pointer:

$$\text{Universal vs. Conditional Rule:}$$
- **Inline in Tier 1/2:** Content required by *every single run* of this document.
- **Disclose to Tier 3:** Content required *only by specific execution branches* (e.g., Docker builds, Windows-specific path handling, edge-case rollback procedures).

```markdown
<!-- CORRECT PROGRESSIVE DISCLOSURE -->
### Step 3: Compile application package
1. Run `npm run build`. Done when `dist/index.js` exists.
2. For container targets: consult [`docker-build.md`](resources/docker-build.md). Read only when building container images.
```

In the example above, 90% of standard runs execute line 1 without burning attention on containerization rules. Container-specific details are disclosed only when the container branch triggers.

---

## 3. Co-Location vs. Scattering

While the ladder decides *how far down* a piece of information sits, **co-location** decides *what sits beside it* once placed.

### The Co-Location Rule
Keep a concept's definition, operational rules, schema constraints, and edge-case caveats under **one single heading**, rather than fragmenting them across multiple files or distant sections.

- **Duplication (Anti-Pattern):** Repeating the same meaning in multiple files. This inflates maintenance overhead and creates synchronization bugs.
- **Scattering (Anti-Pattern):** Splitting one coherent concept across disparate sections (e.g., putting authentication parameters in Section 1, authentication error handling in Section 7, and authentication invariants in an appendix). The agent reads Section 1 and acts immediately, missing the caveats in Section 7.
- **Co-Location (Standard):** Reading the heading provides the complete operational boundary in a single unified attention frame.

---

## 4. Sprawl and Premature Completion Dynamics

### The Sprawl Failure Mode
**Sprawl** occurs when a document becomes excessively long, even when every single sentence is live, unique, and non-redundant. 
- In long documents (>300 lines), model attention thins across the excess lines.
- Attention dissipation causes the agent to treat sequential steps as optional recommendations rather than mandatory transitions.
- **The Remedy:** Ruthlessly enforce the ladder. Disclose branch references behind pointers, and split lengthy linear procedures into distinct execution phases.

### Splitting by Sequence: Breaking Post-Completion Pull
When a procedure has many steps (e.g., Steps 1 through 8), the agent working on Step 2 can see Steps 3 through 8 directly below. The visible upcoming steps exert a powerful cognitive suction known as **post-completion pull**. The agent rushes through Step 2—skipping thorough validation or legwork—in an attentional hurry to reach the finish line.

To protect high-demand verification steps from premature completion:
1. **Sharpen the bound first:** Formulate an unyielding, checkable completion criterion.
2. **Split across a context boundary if rush persists:** If the model still rushes, split the sequence across a genuine context boundary (a subagent dispatch, an explicit handoff, or a phased execution plan).
   *Note:* Splitting an inline file without clearing context does not help—the remaining steps must be genuinely hidden from active attention during the legwork phase.

---

## 5. Multi-File Architecture Patterns

| Pattern | Structure | Best Used For |
| :--- | :--- | :--- |
| **Root-and-Spoke** | `SKILL.md` (<150 lines) + `resources/*.md` | Public executable skills with diverse operational branches. |
| **Triage Router** | Single router file pointing to peer skills | Navigating large catalogs without loading all skill bodies into context. |
| **Linear Pipeline** | Sequenced files (`phase-1.md` $\rightarrow$ `phase-2.md`) | High-stakes multi-stage releases where premature completion is catastrophic. |
| **Flat Peer Catalog** | Single resource file with uniform H2 sections | Rulebooks, linting rules, or diagnostic catalogs evaluated on demand. |
