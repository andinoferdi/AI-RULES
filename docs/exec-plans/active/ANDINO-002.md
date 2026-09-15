# ANDINO-002 - Documentation and acceptance hardening

Status: PARTIAL (Antigravity PASS; Codex smoke has a read-only skill-access gap)
Current phase: evidence recorded; no additional hardening authorized

## Objective
Expand the user guide with setup and practical examples. Apply the accepted final
acceptance audit from gpt batch 2 without redesign, new skills, or new MCPs.

## Acceptance criteria
- README covers initial alignment, tasks, automatic/explicit routing and examples.
- Installed runtime references no longer require the source repository path.
- Record actual worker invocation mechanisms and their limitations.
- Attempt bounded, non-destructive native host behavior checks; distinguish results
  from static validation and record manual-only checks honestly.
- Apply the user's Context7 default-off decision without removing configuration.
- AI-Rules-WebBased.md remains unchanged.

## Constraints
Keep one source, generated installs, existing providers/credentials and accepted
architecture. Do not install Antigravity CLI without user authorization, add skills,
add MCPs, or inventory raw caches.

## Current state / evidence
README walkthrough and prompt examples added. All four global UI references now
resolve to installed skill copies. Codex core workers are non-implicit; Claude
user-only; OpenCode V1 denied through native skill permission; Antigravity soft
description guards only. Native restrictions are not bypassed by file reads.
Seven isolated tests and Markdown links pass; four generated installs match;
git diff --check passes. WebBased SHA256 remains unchanged.
Fresh catalogs: Codex 91, Claude 128, OpenCode 121; full advertised surface remains
partially measured. Context7 is default-off in Codex, Claude, OpenCode, and legacy
Antigravity, with definitions/credentials preserved. Codex CLI is now 0.154.0 after
the official updater ran through installed pwsh 7.6.5, which provides `Get-FileHash`;
the checksum was not bypassed. `agy` 1.2.2 is installed and its User PATH is present.
Antigravity A-E smoke PASSed. Codex A-E smoke reached the model but its read-only
sandbox denied loading the installed Andino body; its B/C decisions followed global
AGENTS.md instead. Codex also classified browser initial diagnostics as plan-needed,
contrary to the expected initial no-plan route. Claude remains organization-auth
blocked (403). OpenCode Meda remains budget blocked (400); 9router is configured but
its local endpoint was unavailable for a non-mutating model-list check.
See ../../acceptance-audit.md and ../../invocation-matrix.md for evidence/limits.

## NEXT ACTION
Use the installed workflow on real tickets and collect evidence before changing the
architecture. Keep Claude as external organization-auth blocked and Meda/OpenCode as
provider-budget blocked. Do not switch providers, change credentials/budgets, widen
the Codex smoke sandbox, or perform further hardening solely to improve this audit.
Revisit the Codex skill-access gap only if dogfooding shows normal desktop sessions
cannot load Andino or route browser diagnostics correctly.
