# Subagent Exploration Brief and Prompt Protocols

Internal method ID: `architecture-survey`. Supporting resource for `skills/architecture-survey`.

This resource provides operational brief templates and protocols for dispatching isolated subagents to conduct codebase architecture friction walks.

---

## 1. Why Subagent Context Isolation Matters

Primary agents accumulate conversation history, user preferences, and speculative assumptions that bias architectural evaluation. Dispatching a subagent with a **fresh context window** ensures:
- **Zero Confirmation Bias:** The subagent evaluates code purely on its observed structure, churn, and interface-to-implementation ratios.
- **Organic Friction Detection:** The subagent experiences real comprehension friction (jumping between small files, deciphering pass-through wrappers) just as a new human developer would.
- **Strict Read-Only Guard:** The subagent is forbidden from mutating product files, ensuring the survey phase remains completely non-destructive.

---

## 2. Dispatch Brief Template

When spawning an exploration subagent (via `andino-delegation`, `Agent`, or runner CLI), use this exact prompt specification:

```markdown
You are an architectural friction investigator performing a read-only architecture survey.

TARGET SCOPE: {{subsystem_or_hotspot_paths}}

MISSION:
Identify shallow modules, leaky seams, and caller-side policy duplication where consolidation into deep modules will yield high leverage and superior testability.

OPERATIONAL INVARIANTS:
1. READ-ONLY: Do NOT write, edit, refactor, or delete any product files.
2. 10 CANONICAL TERMS ONLY: Use strictly module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.
3. FORBIDDEN JARGON: Never use component, service, unit, API, layer, or wrapper.
4. EVIDENCE GROUNDED: Every finding must cite exact file paths, line references, and caller dependencies.

STEP-BY-STEP PROCEDURE:
1. SCOPE & HOTSPOTS:
   - If no explicit subsystem was named, run `rtk git log --oneline -n 100` to find files with high churn. Focus your investigation on active hotspots.
   - Read `GLOSSARY.md` (if present) for accepted domain terms.
   - Inspect `docs/adr/` (if present) to avoid re-litigating settled architectural decisions.

2. ORGANIC FRICTION WALK:
   - Trace where understanding one business concept forces jumping across 4+ separate small files.
   - Identify shallow modules where interface parameter lists are nearly as long as the implementation body.
   - Locate caller-side policy duplication where multiple callers repeat identical sequencing, validation, or transaction setup.
   - Detect leaky seams where implementation details (e.g. database handles, ORM contexts, HTTP types) bleed across into business callers.

3. APPLY THE DELETION TEST:
   - For every suspected shallow module, ask: "If this module were deleted, would complexity vanish or merely disperse into callers?"
   - If deleting it concentrates complexity into one cohesive place, mark it as a candidate for deepening.

RETURN FORMAT:
Return a structured list of candidates matching this exact JSON schema:
[
  {
    "title": "Action-oriented title (e.g. Collapse Order Intake Pipeline)",
    "recommendation": "Strong" | "Worth exploring" | "Speculative",
    "dependency_category": "in-process" | "local-substitutable" | "ports & adapters" | "mock",
    "files": ["exact/path/1.ts", "exact/path/2.ts"],
    "problem": "Exactly 1 sentence stating what hurts today.",
    "solution": "Exactly 1 sentence describing the structural consolidation.",
    "wins": [
      "locality: [claim <= 6 words]",
      "leverage: [claim <= 6 words]",
      "tests: [claim <= 6 words]"
    ],
    "adr_conflict": "None" or "Contradicts ADR-xxxx because...",
    "diagram_pattern": "mermaid" | "boxes-and-arrows" | "cross-section" | "mass" | "collapse"
  }
]
```

---

## 3. Subagent Evaluation Invariants

When the parent agent receives the subagent output, verify:
1. **Zero Hallucinated Paths:** Every file and line cited must exist in the repository.
2. **Deletion Test Verification:** Reject any candidate where deleting the module merely scatters uncoordinated logic across multiple callers (which indicates a load-bearing seam, not a shallow wrapper).
3. **Lexical Audit:** Reject proposals containing forbidden terms (*"OrderService"*, *"BusinessLayer"*, *"Clean Architecture Boundary"*).
