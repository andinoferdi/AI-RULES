# Required capability routing and setup delivery

Status: IMPLEMENTATION_DELIVERED; behavioral acceptance PARTIAL
Owner: Andino Workflow / Codex
Date: 2026-10-08
Density: LITE

## Objective and acceptance

Apply the approved three runtime-file patches and backed-up global Claude contract.
Preserve one router/lifecycle and native permissions. Run structural validators,
existing regression tests and ten isolated behavioral scenarios with honest evidence.
Publish runtime and setup metadata, verify remote setup and align local installations.
User explicitly authorized commit/push in the final instruction; no force push.

## Current state

CURRENT PHASE: discovery follow-up delivered; behavioral acceptance remains partial.
Runtime baseline: effc3b8d7326d121317da86aff205de7c0bb0e80.
Main baseline: 20b840f059a6c6c25b41dfe498119735caa30c9f.
WebBased checkout remains untouched and clean. Separate managed worktrees:
`andino-routing/AI-RULES` and `andino-setup-release/AI-RULES`.
EVIDENCE: runtime 6cb04a4 pushed; 124 unit/regression tests and structural validators
pass. Ten final-runtime Codex cases: 4 scoped PASS, 2 FAIL, 4 NOT_VERIFIED. Exact
hash and reasons are in required-routing-review.md and the reviewed JSON records.
Claude authentication expired; no native permission bypass performed. Both setup
sources and five host target artifacts pass installation/NO_OP checks. Global
installed skill clones updated with backups and repeated setup reports NO_OP.
Decisions: approved runtime scope only; quality-plane evidence and release pins are
additional distribution work explicitly requested. No delegated development agents.
Live actor processes are isolated test executions, not implementation delegation.

## Execution board

| Phase | Status | Evidence |
| --- | --- | --- |
| Drift inspection and isolated checkouts | DONE | Remote refs, clean WebBased and local clones checked |
| Approved patches and verification | DONE | Runtime/global patch; 124 tests PASS; ten live samples reviewed with honest limits |
| Publication, setup and local alignment | DONE | Runtime 6cb04a4 and main delivery 9d4a1cb pushed; installed CLI verified from WebBased; all five local targets match commit/hash and report NO_OP |

## NEXT ACTION

Restart/reload the affected IDE session and check its actual skill activation.
Authenticate Claude before replaying the reported status request. The ten prior
cases retain their original revision/results; rerun them on an authenticated host
permitting fixture reads/writes before expanding behavioral acceptance.

## Discovery follow-up, 2026-10-08

Repository drift: primary checkout is now clean main at 30b3675 (user change),
not WebBased. Reused the two managed worktrees; no unrelated checkout edits.
User screenshots show Claude selected Skripsi but skipped routing references;
native slash injection explains why Andino need not have another Skill tool row.
Antigravity CLI /skills reproduced missing Skripsi for a Windows junction and
found identical content in a regular directory. KEEP host roots (official docs
confirm them); replace only selected local junctions, with backups and shared
sources preserved. Installer now blocks this unsupported layout instead of
reporting current; ordinary setup distinguishes file checks from runtime discovery.
Andino entry now explicitly reads routing; other references stay conditional.
Runtime: 52ceaaedc42fae86d7aeb550dd4b799264552725.
Evidence: discovery-followup.json; 125 tests PASS; native CLI activation order
PASS, final task NOT_VERIFIED because headless command permission was denied.
Claude loggedIn=false; IDE conversation replay NOT_VERIFIED.
Local setup Everything/all five hosts updated Andino and checked all 15 artifacts.
Backups: ~/.andino/backups/routing-discovery-20261008/.
