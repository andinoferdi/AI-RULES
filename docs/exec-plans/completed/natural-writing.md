# Natural Writing integration

Status: DONE (local); publication pending authorization
Plan depth: STANDARD

## Executive Snapshot
Add an independent first-party `natural-writing` skill (Write, Rewrite, Review;
Indonesian and English; academic-safe), separate Focus communication from
requested writing artifacts, add an optional Skripsi companion route and an
Andino native-sibling route, and register the capability in main's catalog,
profiles, validators, evals and release manifest.

## Objective and acceptance
- Standalone installable runtime on its own orphan branch with original text and
  its own MIT license; upstream inspiration attributed without reuse.
- Focus, WebBased A/X and Skripsi state that conversational brevity never
  shortens a requested artifact; A stays byte-identical across Focus and WebBased.
- Andino routes by artifact intent; Natural Writing stays out of code, chat and
  machine-readable tasks.
- Catalog, profiles (`everything`, `research-skripsi`), validator flags, evals,
  installer tests, bounded semantic-preservation checker and local release pins.

## CURRENT STATE
Bases on 2026-10-19 (no drift after fetch): main 6bc5535, focus dbeff40,
skripsi-skill fceec66, andino-workflow 037a483, WebBased 9a5d0e1. Work lives in
worktrees under `C:/Users/Lenovo/Downloads/AI-RULES-wt/`. Local runtime commits:
natural-writing f359b7bdd07a0b931ff2924ddcb303c2182b11f9,
focus d119a80f2ac7567f3034eb6663e54c4ce9545de0,
WebBased cb7564446c487b0de929203a08c1f0404bfdd56a,
skripsi-skill 7ae5cd7a63bf40233296624b8e9d49ae3edf438c,
andino-workflow 634585a45866261e0d981a68098fa7f1b4bf4c0e. Nothing pushed.

## CURRENT PHASE
Complete locally. Publication is a separate, unauthorized step.

## Execution Board
| Phase | Status | Result / evidence |
| --- | --- | --- |
| P1 Audit | DONE | Branch layouts, A sync contract, Andino registry/validator whitelist, Council registration template, upstream license (none) and SHAs. |
| P2 Runtime and boundaries | DONE | natural-writing package; Focus SKILL/README; identical A block in Focus priority-a, WebBased chat-rules and README; WebBased X note and optional Y; Skripsi companion route; Andino registry, routing and coexistence rows. |
| P3 Main integration | DONE | Catalog, profiles, validate_skills flags, Andino whitelist and four routing evals, natural-writing evals, installer tests, semantic checker with mutation fixtures, CI fetch list, README, manifest pins marked LOCAL_COMMIT_UNPUBLISHED. |
| P4 Verification | DONE | See Evidence. |

## Decisions
- Independent native sibling, not an Andino GUIDE; `requires: []`.
- Artifacts are classified by purpose, not location.
- Phrase lists are diagnostic hints; no punctuation, sentence-length or structure
  quotas; no universal em-dash rule.
- Upstream mchardyan/anti-ai-writer has no license (main bdbcad4, references
  3a86ca0): concept-level attribution only, no reused text or lists.
- Semantic checker is a bounded safeguard: FAIL for exact protected values and
  spans, NEEDS_REVIEW for certainty, causality, limitation and negation shifts,
  WARNING for heavy length loss. It does not prove semantic equivalence.
- Manifest pins use real local SHAs with `LOCAL_COMMIT_UNPUBLISHED`;
  `--source latest` for natural-writing needs the remote branch.

## Evidence
See [validation record](../../validation/natural-writing/README.md).

## NEXT ACTION
With authorization: push runtime branches (natural-writing, focus, WebBased,
skripsi-skill, andino-workflow), verify remote SHAs, switch manifest statuses to
published, then publish main and rerun CI.
