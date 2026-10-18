# Eight-branch repository maintenance

Status: DONE | Depth: STANDARD | Date: 2026-10-18

## Executive Snapshot

CURRENT STATE: Six runtime README commits published and remote-confirmed; Council
is NO CHANGE. Frozen manifest sequence 14 uses their exact published commits.
Final current-src suite: 223 tests, zero failures, one opt-in skip. All package,
inventory, schema, traceability, README lint/link and canonical procedure gates pass.
Sixteen disposable installation scenarios pass, including real remote acquisition,
upgrade/backup, idempotency and local-edit protection. No global setup performed.
Main implementation ad80499fd1d588e52b00056c5472cfec705406f6 is pushed and remote-
confirmed. GitHub Actions run 39117329749 completed successfully. All runtime
worktrees are clean detached HEADs; main tracked state is clean and only the
user's original untracked prompt remains. No material blocker remains.
CURRENT PHASE: Complete.

## Objective

Audit exactly main and the seven first-party runtime branches, improve public
documentation, preserve runtime/legal/evidence files, verify and publish through
non-force pushes. WebBased and immutable communication files remain read-only.

## Acceptance Criteria

- Each scoped branch inspected; necessary changes verified and individually pushed.
- README commands, dependencies, host limits and bundled-method claims match source.
- Main references only published runtime commits; no tags or installer releases.
- No global setup, force push, merge, rebase, new branch, or evidence deletion.
- Final report includes baselines, verification, SHAs, publication and Git state.

## Execution Board

| Phase | Status | Evidence |
| --- | --- | --- |
| Baseline and audit | DONE | All packages classified; no obsolete file proved safe to delete |
| Runtime documentation and publication | DONE | Six README commits PUSHED; Council VERIFIED / NO CHANGE |
| Main reconciliation and verification | DONE | Sequence 14, seven exact remote pins; fresh suite and installation checks pass |
| Publication and final checks | DONE | Main ad80499 remote-confirmed; Actions 39117329749 SUCCESS; all final Git states checked |

## Baseline and matrix

| Branch | Baseline SHA | State |
| --- | --- | --- |
| main | 6b2875312fb03d6e6f977aa30a6d7044a336b3ce | PUSHED ad80499; final checkpoint identified by containing commit |
| ai-codebase-rescue | ff61f482eb85c8f4870ee74ffe208394a61cb433 | PUSHED 5b0b47c |
| andino-workflow | efd9c508d55ed94ab2a1229e3324a008e7db71f0 | PUSHED 8866a23 |
| council | 82984fa4dd75023e63d944e6cee1b61d191047c4 | VERIFIED / NO CHANGE |
| focus | 3effa779d14303ed33ee8be874e86c2c3a873f55 | PUSHED dbeff40 |
| search-first | 8383f8a329beff75867de80a517a8ef4d253e678 | PUSHED b55364b |
| skripsi-skill | 1161da8411c1914ad5207cde384ce151293d226e | PUSHED fceec66 |
| threejs-skills | f47d7c03a309703d6804b9e8e4787d54cbbdb53f | PUSHED 7ff3f57 |

## Decisions and evidence

- WebBased remote baseline: 9a5d0e1b31257c4fcb1554558266ec7afc2a6160.
- Native Git is sufficient. Runtime worktrees use detached HEADs and explicit
  HEAD-to-existing-branch push refspecs; no new branch refs are created.
- Andino Workflow, Search First and Anti-Slop loaded from installed SKILL.md files;
  Focus loaded as Andino's communication layer. No delegation.
- Search First research: read the public GitHub READMEs of addyosmani/agent-skills
  and mattpocock/skills through web.open. Adopt benefit-first introduction, direct
  installation instructions and a concise capability catalog; copy no branding.
- Main currently claims the unified package is unpublished, while its manifest
  and remote agree on published Andino efd9c508. Correct the stale public claim.
- Selective cleanup requires reference/evidence analysis; names alone justify no deletion.
- Runtime file counts: Rescue 9, Andino 127, Council 2, Focus 6, Search First 4,
  Skripsi 27, Three.js 775. Exactly one native SKILL.md in each; Andino 57 and
  Three.js 45 internal guides. All supporting/runtime/legal resources retained.
- Canonical Andino evidence check exposed pre-existing stale procedural identities,
  plus Windows CRLF differences. Systematic Debugging loaded; LF Git exports
  discriminated checkout differences from stale canonical hashes. Re-executed
  all 18 Addy, 28 Matt and 11 Superpowers procedures successfully. Original reports
  retained under docs/validation/andino-unified/pre-maintenance/. Refreshed reports
  pass the canonical validator; no checker or runtime instruction changed.
- markdownlint-cli2 0.23.3 installed only under the isolated maintenance tooling
  directory with install scripts disabled. All rules enabled except MD013 for
  existing long commands/tables. Eight READMEs pass with zero issues.
- Review corrected an ambiguous Andino claim: CLI may fetch the runtime branch;
  package installation executes no bundled example or upstream hook.
- Post-pin plain Python loaded stale site-packages rather than current src: six
  Search First fixture mismatches. Confirmed module __file__; reran all 223 tests
  with src inserted first, PASS / one opt-in skip. Global installation untouched.
- Final installation.json: five adapters x bundled fresh/repeat, real latest Codex
  fresh/repeat and baseline upgrade/backup/repeat, two modified-managed conflicts
  preserving local edits: 16 PASS scenarios. No source/catalog/network mocks.
- Fifty README local/first-party links pass; 17 external links return 200. Two npm
  pages deny HEAD with 403, so current availability is NOT_VERIFIED; no bypass.
- Release reconciliation updates six distributed packages and their sequences to
  14; unchanged Council entry retained. Previous Focus pin was older than already
  published references; new exact pin matches WebBased. No runtime instructions
  changed in this maintenance. Original three procedure reports preserved exactly.
- Evidence: docs/validation/repository-maintenance/README.md, verification.json and
  installation.json. Scope limits include unexecuted native host/model/rendering
  checks; existing revision-specific evidence remains intact.
- Implementation publication: main ad80499fd1d588e52b00056c5472cfec705406f6, normal
  push confirmed by ls-remote. Actions 39117329749 SUCCESS, including every validator
  and test step. Canonical exports of that main commit and actual published Andino
  pass source/procedure validation; all seven manifest pins match remote heads.
- Final checkpoint closes this plan and records the confirmed implementation commit;
  its own commit identity and push/CI result are reported in the final delivery.
  No self-referential SHA is invented. Runtime branches need no further changes.

## NEXT ACTION

None; implementation, runtime publication and acceptance checks complete.
