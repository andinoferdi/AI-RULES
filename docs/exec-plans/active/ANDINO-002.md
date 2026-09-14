# ANDINO-002 - Documentation and acceptance hardening

Status: BLOCKED (native behavioral acceptance requires host access)
Current phase: documentation and local hardening complete; live acceptance pending

## Objective
Expand the user guide with setup and practical examples. Apply the accepted final
acceptance audit from gpt batch 2 without redesign, new skills, or new MCPs.

## Acceptance criteria
- README covers initial alignment, tasks, automatic/explicit routing and examples.
- Installed runtime references no longer require the source repository path.
- Record actual worker invocation mechanisms and their limitations.
- Attempt bounded, non-destructive native host behavior checks; distinguish results
  from static validation and record manual-only checks honestly.
- Report active surface metrics and Context7 tradeoffs without changing Context7.
- AI-Rules-WebBased.md remains unchanged.

## Constraints
Keep one source, generated installs, existing providers/credentials and accepted
architecture. Do not install capabilities, change Context7, or inventory raw caches.

## Current state / evidence
README walkthrough and prompt examples added. All four global UI references now
resolve to installed skill copies. Codex core workers are non-implicit; Claude
user-only; OpenCode V1 denied through native skill permission; Antigravity soft
description guards only. Native restrictions are not bypassed by file reads.
Seven isolated tests and Markdown links pass; four generated installs match;
git diff --check passes. WebBased SHA256 remains unchanged.
Fresh catalogs: Codex 91, Claude 128, OpenCode 121; full advertised surface and
Antigravity runtime remain only partially measured. Context7 unchanged; recommend
on-demand based on observed two-tool exposure, not inferred token savings.
Native probes: Codex model/CLI incompatibility (400); Claude org access denied
(403); OpenCode provider budget exceeded (400). Antigravity CLI unavailable.
No useful model routing output was generated; no four-host behavioral PASS claim.
See ../../acceptance-audit.md and ../../invocation-matrix.md for evidence/limits.

## NEXT ACTION
After the user restores supported Codex CLI/model access, Claude organization/API
access and OpenCode provider budget, rerun independent A-E fixture tasks and record
actual routing/tool/plan behavior. Run Antigravity cases manually in its UI.
Do not retry current deterministic access errors, change credentials/budgets, or
declare acceptance complete based on static checks alone.
