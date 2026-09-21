# Final family consistency matrix

Recorded after commits `9172810d` (Andino), `b34f4d79` (Rescue), `6f7c57c8`
(Skripsi) and `2acce637` (main). Every initial NEEDS_ALIGNMENT finding is either
implemented or explicitly limited below; no unexplained NEEDS_ALIGNMENT remains.

| Area | Classification | Final evidence |
| --- | --- | --- |
| Roles and lifecycle ownership | GOOD | Main standard, all three SKILL boundaries and specialist references agree: Andino owns active lifecycle; specialists return evidence; both standalone. |
| Activation and negative triggers | GOOD | Distinguishable frontmatter plus Andino/Rescue/Skripsi README smoke cases and eval coverage. |
| Host paths and discovery | GOOD | README tables and dated first-party source record distinguish Codex, Claude, OpenCode V1/V2, and Antigravity surfaces. |
| Duplicate and refresh claims | KNOWN_LIMITATION | Documented host-specific rules are recorded; OpenCode local refresh, Antigravity precedence/refresh and Windows junction behavior remain undocumented/unverified. |
| Package structure and hygiene | GOOD | Runtime allowlists, required README/SKILL, regular Git modes and relative-link checks pass at exact final runtime SHAs. |
| Metadata constraints | GOOD | Name grammar/length, description bounds and plain-string scalar checks are validated; host-specific optional fields remain out of scope. |
| Evidence terminology | GOOD | Main standard and README guidance separate structural, documentation, live and unverified evidence. |
| External-action boundary | GOOD | All runtime packages state activation does not authorize Git/publication/deployment/live-data actions. |
| Runtime domain methods | INTENTIONAL_DIFFERENCE | Rescue dispositions/gates and Skripsi ResearchState/SRS/assets remain specialized; no artificial symmetry added. |
| Assets and scripts | INTENTIONAL_DIFFERENCE | Skripsi has seven used assets; A/R have none; no runtime scripts are required. |
| Quality depth | INTENTIONAL_DIFFERENCE | Skripsi retains formal 335-item traceability and 117-case evidence; A/R use proportionate family evals without fake requirement inventories. |
| Live behavioral parity | KNOWN_LIMITATION | OpenCode visibility was observed for installed baseline paths; no cross-host activation suite was run. Skripsi saved records remain 58 PASS/0 FAIL/60 NOT_VERIFIED and revision-scoped. |
| Unsupported license/provenance claims | NOT_APPLICABLE | No new family license or endorsement asserted; existing Andino attribution and source-qualified notes retained. |
