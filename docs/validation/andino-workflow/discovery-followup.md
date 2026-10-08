# Discovery and routing follow-up

Date: 2026-10-08. Runtime: 52ceaaedc42fae86d7aeb550dd4b799264552725.
Reviewed native evidence: [discovery-followup.json](discovery-followup.json).

## Findings and bounded repairs

- HIGH / confirmed / REFACTOR installation layout: Antigravity CLI `/skills`
  omitted `skripsi-skill` although its SKILL.md existed. Same content in a regular
  project directory appeared; the junction fixture did not. Global CLI discovery
  found Skripsi after replacing its junctions with regular directories. Shared
  sources were not edited. Selected Andino/Rescue CLI junctions were also backed
  up and materialized so the selected installation set has no such discrepancy.
- HIGH / confirmed / REFACTOR verification: setup compared resolved file contents
  and called these junction installations current. The new Windows regression
  failed before the patch for both Antigravity adapters and passed afterward.
  Reconciliation now blocks that layout, preserving the link and source for
  reviewed repair. It does not automatically replace arbitrary user links.
- MEDIUM / reported / bounded instruction fix: the supplied Claude trace says
  Andino's main instructions were slash-injected but its routing reference was
  skipped. Move and clarify the existing routing prerequisite at entry. Do not
  force handoff/execution-plan or every specialist reference for a status question.
- KEEP: one router, existing host roots, phase-local selection and permissions.
  No registry expansion, second lifecycle, hooks or router executable.

## Validation and limits

| Check | Result |
| --- | --- |
| Unit/regression suite | PASS: 125 tests |
| Skill packages/links/eval schemas | PASS: 3 packages, 3 schemas |
| Capability contracts | PASS: 34 eval schemas, 55 contracts |
| Native CLI junction vs regular directory | PASS: discriminating reproduction |
| Native CLI after local repair | PASS: Skripsi catalog entry, model_invocable=true |
| Single Andino invocation in fresh CLI fixture | PASS scoped to observed routing -> Skripsi -> integration/state-reference loads |
| Complete thesis answer / USED | NOT_VERIFIED: subsequent command denied in headless mode; no permission bypass |
| Claude behavior after patch | NOT_VERIFIED: CLI auth status loggedIn=false |
| Antigravity IDE behavior | NOT_VERIFIED: files repaired; CLI evidence is not an IDE session replay |
| Previous ten behavioral cases on new revision | NOT_VERIFIED: not rerun; earlier results retain original hashes |

The official [Antigravity skill locations](https://antigravity.google/docs/skills?tab=ide)
match the existing roots. Missing legacy-root copies therefore do not justify
another installation root. The `/skills` experiment tests discovery, not task use.
User-reported Codex/OpenCode success is supplementary evidence, not a new automated run.

Setup was executed with Everything across five hosts using a separate task state
directory, preserving the user's default profile. All 15 file targets were checked;
five Andino copies advanced to the new runtime. Backup directory:
`C:/Users/Lenovo/.andino/backups/routing-discovery-20261008/`.

Residual risks: model compliance remains probabilistic; existing sessions may retain
old discovery/context. Regular host copies no longer inherit shared-source edits
through junctions; run setup for synchronization. Other user skills/junctions were
outside scope. The standalone release executable has not been rebuilt; the installed
Python CLI and source setup contain this fix.
