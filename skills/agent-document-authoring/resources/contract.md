# Agent Document Evaluation Contract and Diagnostic Rubric

Internal method ID: `andino-agent-document-authoring` resource: `contract.md`.

## Purpose and Scope

This document defines the formal data contract, structural schema, and 5-point diagnostic evaluation rubric for all agent-facing instructions, context pointers, skills, `CLAUDE.md`, and `AGENTS.md` documents.

---

## 1. Document Classification Contract

Every agent-consumed document belongs to exactly one primary category:

| Category | Primary Target | Loaded When | Governing Invariants |
| :--- | :--- | :--- | :--- |
| **Passive Root Guidance** | `CLAUDE.md`, `AGENTS.md` | Session initialization (Always in context) | Strict token floor (<100 lines), zero cached environment data, zero procedural step sequences that belong in skills. |
| **Executable Skill** | `SKILL.md` (via `skill-maker`) | Dynamically on trigger condition | SDO trigger-only frontmatter, dominant negative gates, deterministic completion criteria. |
| **Context Pointer Reference** | `resources/*.md` | On demand when pointer fires | Front-loaded leading word, single branch isolation, flat peer reference. |
| **Router Skill** | Root router (e.g. workflow advisor) | User or agent manual dispatch | Cognitive load index, pointer routing table, zero execution steps. |

---

## 2. The 5-Point Diagnostic Audit Rubric

Every candidate agent document must be audited against these five dimensions before deployment:

| Dimension | Audit Check | Pass Criteria | Reject Condition (Failure Mode) |
| :--- | :--- | :--- | :--- |
| **1. Pointer Integrity** | Does the context pointer front-load the leading word and isolate one branch? | Pointer starts with primary conceptual trigger; synonyms collapsed; target path resolves locally. | Pointer buried in conversational prose; multiple synonyms for identical branch; broken target link. |
| **2. Information Hierarchy** | Are sequential steps separated from flat reference and edge cases? | Sequential actions visible in primary tier; specialized reference disclosed behind pointer. | Inlined edge cases or deep reference burying operational steps (**Sprawl**). |
| **3. Demanding Bounds** | Can the agent distinguish done from not-done with observable certainty? | Criterion specifies observable, checkable evidence (exit code, AST match, file existence). | Subjective bounds ("ensure quality", "check thoroughly") triggering **Premature Completion**. |
| **4. Positive Formulation** | Are target behaviors prompted positively rather than through prohibitions? | Positive target actions explicitly stated; negations limited to absolute safety gates. | Negation cascade ("do not do X, never do Y") activating the forbidden state in model attention. |
| **5. No-Op & Sediment Free** | Does every single sentence actively alter model behavior from default? | Environment data not cached; zero dead historical sediment; zero default model pleasantries. | Restating `package.json` scripts, `--help` menus, or generic pleasantries. |

---

## 3. Structural Evaluation Schema (JSON Contract)

Automated and semi-automated audit tools evaluate agent documents against this schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AgentDocumentEvaluationContract",
  "type": "object",
  "required": [
    "document_path",
    "category",
    "line_count",
    "rubric_scores",
    "no_ops_detected",
    "status"
  ],
  "properties": {
    "document_path": {
      "type": "string",
      "description": "Relative path to the audited document."
    },
    "category": {
      "type": "string",
      "enum": ["passive-root", "executable-skill", "context-pointer-ref", "router"]
    },
    "line_count": {
      "type": "integer",
      "description": "Total line count of the document."
    },
    "rubric_scores": {
      "type": "object",
      "required": [
        "pointer_integrity",
        "hierarchy_clarity",
        "bound_demand",
        "positive_formulation",
        "pruning_discipline"
      ],
      "properties": {
        "pointer_integrity": { "type": "boolean" },
        "hierarchy_clarity": { "type": "boolean" },
        "bound_demand": { "type": "boolean" },
        "positive_formulation": { "type": "boolean" },
        "pruning_discipline": { "type": "boolean" }
      }
    },
    "no_ops_detected": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of sentences identified as model defaults or zero-yield statements."
    },
    "status": {
      "type": "string",
      "enum": ["CONTRACT_VERIFIED", "REVISION_REQUIRED", "REJECTED"]
    }
  }
}
```

---

## 4. Verification Gate

A document achieves status `CONTRACT_VERIFIED` only when:
1. All 5 rubric dimensions evaluate to `true`.
2. Total `no_ops_detected` is exactly 0.
3. Line count remains strictly within the designated tier ceiling (<100 lines for root guidance, <150 lines for skill root).
