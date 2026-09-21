# Initial family consistency matrix

Recorded 2026-09-21 before runtime or validator edits. Baseline refs are in the
[execution plan](../../exec-plans/active/agent-skill-family-audit.md).
All 44 runtime Markdown files were inspected: Andino 8, Rescue 9, Skripsi 27.
Main review covered README, all validator/test modules, evaluation schemas and
representative cases/fixtures, CI, live audit machinery, installer, traceability
inventory/ownership generation and historical audit/remediation records.

Cells use exactly GOOD, NEEDS_ALIGNMENT, INTENTIONAL_DIFFERENCE or NOT_APPLICABLE.
Evidence is a written/source review unless explicitly called executed below.
Abbreviations: A = andino-workflow, R = ai-codebase-rescue, S = skripsi-skill.

| Dimension | A | R | S | Evidence / rationale |
| --- | --- | --- | --- | --- |
| Product role | GOOD | GOOD | GOOD | Each SKILL introduction has a distinct purpose. |
| Lifecycle ownership | GOOD | GOOD | GOOD | A routing; R lifecycle boundary; S andino-integration agree. |
| Standalone support | GOOD | GOOD | GOOD | No mandatory sibling package in any runtime. |
| Relationship with Andino | GOOD | GOOD | GOOD | Specialists return evidence; no competing authoritative NEXT ACTION. |
| Activation description | GOOD | GOOD | NEEDS_ALIGNMENT | F04: S exclusions appear only after loading the body. |
| Positive activation boundary | GOOD | GOOD | GOOD | Coordination vs engineering fragility vs substantive research. |
| Negative triggers | GOOD | GOOD | NEEDS_ALIGNMENT | F04; body already excludes sentence polish/unrelated coding. |
| Metadata quality | GOOD | GOOD | NEEDS_ALIGNMENT | F04; names are unique and stable, no needless optional metadata. |
| Frontmatter correctness | GOOD | GOOD | GOOD | Baseline validator passes; manual portable-name review passes. |
| Folder/name agreement | GOOD | GOOD | GOOD | Installed clones and audit worktrees use exact skill IDs. |
| Terminology | INTENTIONAL_DIFFERENCE | INTENTIONAL_DIFFERENCE | INTENTIONAL_DIFFERENCE | Plan phases, dispositions, ResearchState field labels serve different objects. |
| SKILL responsibility | GOOD | GOOD | GOOD | Core contracts visible; detailed methods conditional. |
| Progressive disclosure | GOOD | GOOD | GOOD | No mandatory load-all route; line-count differences justified. |
| Reference topology | GOOD | GOOD | GOOD | Direct operational links; A template/UI reachable via owning references. |
| README introduction | GOOD | GOOD | GOOD | Role and use stated without marketing. |
| README install | GOOD | GOOD | GOOD | Whole named directory, shell-portable clone, preserve user edits. |
| README host paths | GOOD | GOOD | GOOD | First-party paths agree; IDE and CLI paths retained. |
| Discovery/duplicate semantics | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | F02: compatible roots mentioned incompletely, no host-specific duplicate distinction. |
| README invocation | GOOD | GOOD | GOOD | Existing native examples supported by docs; OpenCode prose avoids V1/V2 API mismatch. |
| Coexistence documentation | NEEDS_ALIGNMENT | GOOD | GOOD | F01: A README says combine the two skills and names only Rescue. |
| Update instructions | GOOD | GOOD | GOOD | Clean status then fast-forward; no overwrite of discoverable backups. |
| Verification/smoke testing | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | F03: generic refresh and scope query; no paired positive/negative manual cases. |
| Package/source explanation | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | GOOD | F03: A/R omit direct main quality-plane link. |
| Package structure | GOOD | GOOD | GOOD | 8/9/27 tracked Markdown files, no control-plane leakage. |
| Assets policy | NOT_APPLICABLE | NOT_APPLICABLE | INTENTIONAL_DIFFERENCE | Seven research output helpers have actual consumers. |
| Scripts policy | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | No runtime script requirement. Main installer is a local helper. |
| Evidence discipline | GOOD | GOOD | GOOD | Domain-specific observation/inference and unverified rules retained. |
| External-action boundary | NEEDS_ALIGNMENT | GOOD | NEEDS_ALIGNMENT | F05: A omits live-data operations; S ethical gates do not explicitly cover Git/publication actions in core. |
| Provenance | GOOD | GOOD | GOOD | A upstream README declares MIT; R historical field-note provenance qualified; S original-method/no-proprietary-copy contract and history agree. No family license inferred. |
| Deterministic package validation | GOOD | GOOD | GOOD | Baseline package validator passes all three refs. |
| Metadata validation | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | F06: name grammar/length and description maximum not enforced; scalar null accepted. |
| Relative-link validation | GOOD | GOOD | GOOD | Inline relative links checked throughout Markdown, including assets and README. |
| Runtime-path validation | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | F06: allowlist exists but missing README and non-regular tree entries can pass. |
| Positive behavior expectations | GOOD | GOOD | GOOD | 11/14/117 baseline eval cases with expected/forbidden. |
| Negative-trigger expectations | GOOD | GOOD | GOOD | Each has behavior and negative-trigger cases. |
| Regression coverage | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | GOOD | F07: A only rescue-specific coexistence; R main evals omit standalone/installed-inactive/active-owner cases already in runtime A-Q oracle. |
| Eval schema robustness | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | F06: unhashable JSON id/kind crashes instead of returning validation errors. |
| Live behavioral evidence | GOOD | GOOD | GOOD | A/R explicitly unverified; S historical records retain 58 PASS and 59 NOT_VERIFIED, not current cross-host proof. |
| Control-plane linkage | NEEDS_ALIGNMENT | NEEDS_ALIGNMENT | GOOD | F03: add navigable main link for A/R; S can make existing main text navigable. |

## Findings eligible for implementation

| ID | Classification | Evidence and minimal action | Allowed files |
| --- | --- | --- | --- |
| F01 | NEEDS_ALIGNMENT | A README's two-skill model lags S's released integration. Generalize optional specialists; keep routing domain-neutral, no forced dependency. | A README.md |
| F02 | NEEDS_ALIGNMENT | Host docs distinguish discovery, duplicates and refresh. Add concise host-specific notes, full compatibility roots and dated source links; avoid universal symlink claims. | All runtime README.md |
| F03 | NEEDS_ALIGNMENT | Install verification lacks representative positive/negative cases and A/R lack main link. Add manual cases and bounded evidence labels. | All runtime README.md |
| F04 | NEEDS_ALIGNMENT | S metadata omits already-established negative boundaries. Add concise exclusions without changing research methodology. | S SKILL.md |
| F05 | NEEDS_ALIGNMENT | Common authorization rule is explicit in R, incomplete in A, absent from S core. Clarify activation grants no Git/publication/deploy/live-data permission; retain research ethics gates. | A and S SKILL.md; runtime README.md; supplemental S eval sources |
| F06 | NEEDS_ALIGNMENT | Validator accepts malformed portable metadata and missing distribution README; tree modes unchecked; malformed eval types crash. Add focused fail-closed checks and regression tests. | main scripts/validate_skills.py, tests/test_validate_skills.py |
| F07 | NEEDS_ALIGNMENT | Runtime coexistence contract not represented in A/R control-plane cases. Add bounded standalone/inactive/owner examples; add S external-action case without altering 110 SRS cases. | main evals/andino-workflow.json, evals/ai-codebase-rescue.json, evals/skripsi-supplemental.json, evals/skripsi-skill.json, corresponding new S unverified record/review |
| F08 | NEEDS_ALIGNMENT | No durable family standard; main README lacks owner/specialist explanation. Evals README's blanket live NOT VERIFIED obscures historical S evidence. Add concise standard, audit evidence and link; qualify existing evidence. | main README.md, evals/README.md, docs/agent-skill-family-standard.md, docs/validation/agent-skill-family/*, execution plan |

## Intentional differences and limits

No runtime references/assets need methodology changes. Rescue's larger entrypoint,
six remake gates and five dispositions stay intact. Skripsi keeps all eighteen
references, seven assets, seven field statuses and its larger SRS traceability.
No fake equivalent requirement registers for A/R. No optional license, host-only
metadata, scripts or empty directories added.

Native discovery and actual behavior will be reported separately. Historical S
results do not certify new revisions. Windows junction portability is not inferred
from Codex/Claude symlink documentation; the local installer is not a family-wide
host certification. An upstream README's MIT declaration is attribution evidence,
not a license grant for this family or an endorsement.
