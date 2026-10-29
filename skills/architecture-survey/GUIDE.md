# Survey architecture friction

Internal method ID: `architecture-survey`. Stable technique adapted to Andino ownership.

## Purpose and selection

Surface architectural friction and propose evidence-backed **deepening opportunities**: refactoring shallow, fragmented modules into deep, high-leverage abstractions to maximize testability and AI-navigability without introducing speculative bloat.

Activate for: A named architecture pain point, a request to evaluate subsystem maintainability/testability, or a bounded inquiry into code complexity.

Do not activate for: Routine feature bug fixes, cosmetic formatting, arbitrary whole-repository scans without bounded direction, or repeated searches when no worthwhile candidate exists.

Positive request: "Survey the order processing subsystem for evidenced deepening opportunities."
Negative request: "Rename this local variable in handler.ts."

These are declared activation fixtures, not a claim that a model/router was executed.

## Inputs and dependencies

User scope or recent-change hotspots (`git log --oneline`), domain vocabulary (`GLOSSARY.md`), established Architecture Decision Records (`docs/adr/`), relevant code, callers, and test suites.

Use resources progressively: [worked procedure, visual report patterns, and diagnostic rubric](resources/worked-example.md). It provides end-to-end before-and-after case studies, hybrid HTML report scaffolds with zero-network fallback, 5 diagram patterns (Mermaid, Boxes & Arrows, Cross-section, Mass diagram, Call-graph collapse), red-flag heuristics, and a 6-point self-audit rubric.

---

## Core mental models & vocabulary

Architectural survey operates on strict, unambiguous design levers:

### 1. Scope Before Scanning (YAGNI & Hotspots)
Deepening a module pays off by making future modifications simpler and safer. Concentrating effort on dormant code produces negative ROI.
- If the user specifies a subsystem or pain point, immediately bound exploration to that target.
- Otherwise, inspect recent commit history (`git log --oneline`) to identify actual codebase hotspots—files and directories modified repeatedly. Let churn guide attention.

### 2. The Deletion Test for Shallowness
A shallow module has an interface nearly as complex as its implementation.
- **The Deletion Test:** If this module were deleted, would complexity vanish or merely disperse back into callers?
- If deleting it concentrates complexity into one cohesive place, the candidate is a shallow wrapper ripe for deepening.
- If deleting it scatters uncoordinated logic across disparate callers, the seam is load-bearing.

### 3. Locality vs Fragmented Testability
Extracting pure helper functions solely for unit testability often destroys locality. When logic is atomized across multiple files, real production defects hide in how callers stitch those fragments together.
- Prioritize **locality**: bugs and invariant enforcement should concentrate in one cohesive module rather than across multiple caller coordination sites.

### 4. Interface as the Test Surface
The public interface of a deep module is its test surface.
- Tests reaching past public seams into private internals signal shallow architecture.
- Deep modules absorb thin intermediate wrappers, allowing unit tests to assert meaningful business outcomes against a single stable public contract.

### 5. The Two-Adapter Rule for Seams
Never introduce indirection without proven variation.
- **One adapter = hypothetical seam:** An interface with only one production implementation and no testing substitution is accidental complexity.
- **Two adapters = justified seam:** A seam is justified when two distinct implementations exist (e.g. Postgres in production, in-memory repository in integration tests).

### 6. Architectural Vocabulary Enforcement
Clarity requires precise nouns and verbs. Drift into vague terminology obscures architectural boundaries:
- **USE EXACTLY:** `module`, `interface`, `implementation`, `depth`, `deep`, `shallow`, `seam`, `adapter`, `leverage`, `locality`.
- **NEVER SUBSTITUTE:** *component*, *service*, *unit* (for module); *API*, *signature* (for interface); *boundary* (for seam); *layer*, *wrapper* (when describing a module).
- **WINS MUST BE CONCRETE:** Express benefits in terms of locality, leverage, and test simplification (e.g., *"locality: pricing invariants concentrate in one module"*, *"leverage: 1 public interface absorbs 4 shallow wrappers"*). Never use empty phrases like *"cleaner code"* or *"easier to maintain"*.

---

## Procedure

### 1. Scope before scanning
Identify the boundary before reading code.
- If a subsystem was named, bound exploration strictly to that scope.
- Otherwise, inspect the last 50-100 commits via `git log --oneline` to discover files with high churn.
- Inspect `GLOSSARY.md` for accepted domain terms and `docs/adr/` for settled architectural decisions.
- *Done when:* A bounded set of hotspot paths and active domain constraints are identified.

### 2. Organic friction walk & deletion test
Walk callers and implementations within the bounded scope with a fresh perspective:
- Trace where understanding one concept forces jumping across 4+ small files.
- Spot shallow modules where parameter pass-through dominates the implementation.
- Spot caller-side policy duplication where multiple callers perform identical validation or sequencing before calling a downstream function.
- Identify seams with leaky abstractions (e.g. callers needing database transaction handles or transport types).
- Apply the **deletion test** to every suspected wrapper.
- *Done when:* Concrete friction points are documented with exact file paths, line references, and caller dependencies.

### 3. Structure candidate deepening proposals
Synthesize findings into candidate cards. For each candidate:
- **Title:** Action-oriented deepening statement (e.g. *"Collapse Order intake pipeline"*).
- **Recommendation Strength:** `Strong` (high churn, clear shallowness), `Worth exploring` (moderate leverage), or `Speculative` (lower frequency, trade-offs present).
- **Dependency Classification:** `in-process`, `local-substitutable`, `ports & adapters`, or `mock`.
- **Problem:** Exactly one sentence stating what hurts today.
- **Solution:** Exactly one sentence describing the structural consolidation.
- **Wins:** Bullet points (<= 6 words each) framed in terms of locality, leverage, and test surface reduction.
- **ADR Callout:** Flag existing ADR contradictions *only* if concrete friction warrants reopening the decision.
- *Done when:* Each candidate has concrete before/after definitions ready for visual rendering.

### 4. Generate and launch the self-contained Hybrid HTML Report
Write a single self-contained HTML file to the OS temporary directory (`$TMPDIR` or `%TEMP%`, e.g. `architecture-survey-<timestamp>.html`) so no disposable files pollute the repository.
- Use the **Hybrid Report Scaffold**: load Tailwind and Mermaid via CDN for rich rendering when online, but include embedded fallback CSS and inline SVG styling so cards, seams, and badges render cleanly even in offline or air-gapped environments.
- Provide a side-by-side **Before / After diagram** for every candidate, choosing the most expressive pattern:
  - *Mermaid graph:* Call flows and dependency webs.
  - *Boxes and arrows (CSS/SVG):* Deep module consolidation with faded internals.
  - *Cross-section:* Collapsing multiple thin horizontal layers into one solid band.
  - *Mass diagram:* Visualizing interface width shrinking relative to deep implementation volume.
  - *Call-graph collapse:* Visualizing nested calls consolidated behind a single seam.
- Include a **Top Recommendation** card highlighting the highest-ROI opportunity.
- Open the generated HTML file using the host platform launcher (`start` on Windows, `open` on macOS, `xdg-open` on Linux) and provide the absolute path to the user.
- *Done when:* The visual report exists in temporary storage and the user has immediate access to inspect it.

### 5. Interactive candidate selection & domain alignment
Present the findings concisely in chat and prompt: *"Which of these candidates would you like to explore?"*
Do NOT draft implementation code or refactor product files during the survey phase.
When the user selects a candidate:
- If a new concept was named, verify whether `GLOSSARY.md` requires updating.
- If the user rejects a candidate with an enduring architectural reason, offer to record an ADR so future surveys do not re-suggest it.
- Seamlessly transition into `deep-module-design` for interface specification.
- *Done when:* The user confirms their chosen candidate direction or records a durable rejection.

### 6. Carry selected candidate into the Andino plan
Record the chosen candidate, identified files, and target seam into the active Andino execution plan checkpoint.
- *Done when:* The selected direction is preserved in the plan without losing context.

---

## Ownership, precedence and permissions

Andino retains discovery, reasoning depth, the single durable plan/checkpoint, delegation, permission decisions, and final acceptance. This guide contributes the survey technique; it is not a native skill, router, or second lifecycle. Focus owns communication style; Search First owns external library/pattern research; domain siblings and manual controls remain authoritative.

The survey phase is non-destructive: it inspects code and writes a report to temporary OS storage only. Product files, Git state, and project configuration are never mutated during an architecture survey.

## Outputs and verification

1. Each candidate links to concrete source files, names observed friction, and presents a visual before/after comparison.
2. The HTML report is self-contained and opens reliably in the default browser.
3. Zero product code or Git tracking changes occur during the survey.
4. Verify by running the deterministic reference script in `resources/worked-example.md`, proving correct report generation and invariant checking.

## Anti-patterns to avoid

- **Global codebase scan:** Scanning hundreds of files without scoping or inspecting churn hotspots first.
- **Speculative candidate inflation:** Inventing refactoring suggestions for dormant, stable code.
- **Corporate dashboard noise:** Bloating reports with paragraphs of prose instead of crisp before/after diagrams.
- **Vocabulary drift:** Describing modules as "services", interfaces as "APIs", or seams as "boundaries".
- **Premature implementation:** Writing code or modifying modules before the user selects a candidate.
- **Network-fragile reports:** Generating HTML that fails to display when CDN assets cannot be reached.

## Provenance

Independently adapted and elevated from these audited local snapshot paths:
- `mattpocock/skills:skills/engineering/improve-codebase-architecture/SKILL.md`
- `mattpocock/skills:skills/engineering/improve-codebase-architecture/HTML-REPORT.md`
- `mattpocock/skills:skills/engineering/codebase-design/SKILL.md`

Snapshot identities and licensing are recorded in package legal records (`references/legal/matt-license.md`). Upstream bootstrap, automatic commit/push, hooks, and installers are not imported as authority.
