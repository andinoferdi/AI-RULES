# Final acceptance audit - 2026-09-14

Scope: accepted architecture; documentation and narrow hardening only. No new
skills, MCP servers, provider changes, capability installation, or raw cache inventory.
The request adopted the acceptance requirements in `gpt batch 2.txt`; its external
claims were checked against current native behavior/documentation rather than assumed.

## Status

| Area | Result | Evidence / limit |
| --- | --- | --- |
| Runtime independence | PARTIAL | Four global UI references fixed to installed skill paths. Isolated source-unavailable reference test passes for four installs. Full live operation with the real source absent remains untested because native generation is blocked. |
| Skill invocation | PARTIAL | Native core controls applied on Codex/Claude/OpenCode; Antigravity has only scoped descriptions. Plugin/bundled alternatives and full advertised behavior need live validation. |
| Cross-agent behavior | PARTIAL | Antigravity A-E smoke PASSed. Codex reached the model after update but read-only sandbox blocked full Andino loading and over-escalated initial browser diagnostics. Claude and Meda/OpenCode remain external/provider blockers. |
| Active surface metrics | PARTIAL | Actual discovery/catalog and user-root policy counts recorded below. Complete implicit/advertised and MCP tool counts are not exposed for every host. |
| Context7 decision | PASS | User selected default OFF/on-demand; Context7 was disabled in active Codex, Claude and OpenCode configs and legacy Antigravity without removing definitions or credentials. |

## Exact fixes

- Expanded README with initial project setup/alignment, CRUD task, continuation,
  automatic versus explicit skill selection, capability table, and prompt examples.
- Replaced the global UI coexistence reference in `.codex/AGENTS.md`,
  `.claude/CLAUDE.md`, `.config/opencode/AGENTS.md`, and `.gemini/GEMINI.md`
  with the appropriate existing installed Andino reference.
- Set `policy.allow_implicit_invocation: false` for the four Codex core workers.
- Set `disable-model-invocation: true` for the same Claude workers.
- Set OpenCode V1 `permission.skill.<core-worker> = deny`. Updated existing
  V2 portability metadata to false, but do not count that metadata as V1 enforcement.
- Scoped Antigravity worker descriptions to explicit selection/current Andino phase.
  No undocumented configuration flag was invented.
- Updated the canonical routing reference to respect native invocation restrictions
  and synchronized its four existing generated installs.
- Added idempotent `scripts/harden-runtime.py` and two isolated behavior tests.

Core means systematic-debugging, test-driven-development,
verification-before-completion, code-review-and-quality.

Native manual-only controls have a real tradeoff: Andino can choose/recommend a
method but cannot automatically invoke a worker the host prohibits. The user may
need to invoke it or adjust its native permission. Do not bypass a denial through
an alternate file-reading route. This remains functional friction, not a solved
universal hidden-worker mechanism.

Backups: `~/.andino/backups/acceptance-20260914-224128-894259/` and generated
sync backups under `~/.andino/backups/sync/`. Known source path occurrences in
Claude's project history and generated provenance markers are not runtime loads
and were preserved. Audit/migration scripts may intentionally reference their
editable source; they are not needed to use an installed skill.

## Native smoke attempts

Identical A-E semantic scenarios were supplied to three native CLIs from disposable
fixtures under `~/.andino/acceptance-20260914/`: label change, duplicate charge,
resume sample plan, module dependency, failed browser request. Probes requested
read-only routing decisions; even a successful answer would not prove full task
execution. No production data or actual payment was used.

| Host | Actual outcome | Required manual action |
| --- | --- | --- |
| Codex | CLI updated to 0.154.0 through the official updater using existing pwsh 7.6.5, where `Get-FileHash` is available. A-E probe completed without writes. A/B/C/D routing broadly matched, but read-only sandbox denied the installed Andino body and E required a plan too early. | Do not widen the sandbox merely for audit. Revisit only if real desktop use shows the same gap. |
| Claude Code | After correcting CLI prompt delivery, HTTP 403 `oauth_org_not_allowed`: organization disables subscription access for Claude Code. | Resolve access with the organization/admin or configure an authorized API credential, then rerun. No credential was changed. |
| OpenCode | Meda returned HTTP 400 `budget_exceeded`; the configured 9router endpoint was unreachable for a non-mutating `/models` check. | Resolve Meda budget/access, or make 9router reachable and explicitly authorize its smoke test. No provider was switched. |
| Antigravity | Official `agy` 1.2.2 installed through Google's PowerShell installer; User PATH contains its bin directory. A-E probe completed successfully from a disposable fixture without writes or login. | PASS. Keep only normal dogfooding evidence; no further hardening. |

No useful model routing answer was produced. The initial Claude command also had a
local argument parsing issue; stdin delivery corrected that before the final access
error. Deterministic auth/model/budget errors were not retried blindly.

The claude-mem startup hook additionally reports its existing OpenRouter daily
quota outage. Memory settings/provider were left unchanged as requested. Existing
startup status injection still occurs; per-prompt semantic injection and startup
context are distinct mechanisms.

## Active surface metrics

Snapshot is from fresh native CLI discovery/startup, not this desktop session's
possibly stale catalog. Catalog availability is not proof of model advertisement.

| Host | Native discovered/catalog entries | User-root implicit eligible | User-root manual/denied | Direct MCP active | MCP tools exposed in observed native snapshot | Global core instruction size |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Codex | 91 | 16, plus shared/system/plugin scope | 38 | 1 | 243 including app/plugin servers | 1,699 bytes / 206 words |
| Claude | 128 including plugins/bundled | 23 | 38 | 1 | 50; 3 connected of 7 listed integrations | 1,676 bytes / 206 words |
| OpenCode | 121 (pure discovery) | 52; 54 permission-eligible across native discovery | 67 | 2 | Not measured | 1,678 bytes / 205 words |
| Antigravity | Not measured natively; 9 current user-root entries | 9 with soft core guards | 0 in active root; archived manuals excluded | 1 current config | Not measured | 1,676 bytes / 205 words |

Core instruction sizes exclude imported RTK, project instructions, system prompts,
plugin hooks and conditional references; they are not total always-loaded prompt size.
Codex reports shortened descriptions due to its skill context budget, confirming
that reduced user-root counts do not remove plugin/app surface cost.

No duplicate exact names occurred in the three native listings. Semantic overlap
remains: OpenCode prefixed/unprefixed Superpowers alternatives (denied), Claude
bundled debug/review/planning alongside optional claude-mem workflows, and manual
router aliases. Plugin catalog presence is not evidence of implicit invocation.
See [invocation matrix](invocation-matrix.md) for focused worker/alternative rows.

## Context7 decision and applied state

Decision: **DEFAULT OFF / ON-DEMAND** for a mixed local engineering workflow.
This is applied only to Context7; it is not a measured token-saving claim.

- Codex had exposed `resolve-library-id` and `query-docs`: two tools, with
  4,973 bytes of JSON tool definitions in the local RPC serialization. This is
  serialized schema size, not billed tokens or guaranteed prompt payload.
- Claude startup had exposed the same two tool names; exact schema/token size was not
  available from that event. It is now disabled from the active configuration.
- OpenCode direct config now sets Context7 `enabled: false`; its exposed schema cost
  was not measured.
- Antigravity current config has no Context7. Legacy Context7 is now disabled.

For local label edits, business logic, SQL or regression work, native source/search
usually suffices. On-demand Context7 avoids keeping that optional integration
available when unused, at the cost of enable/reload/setup friction when version-specific
documentation is needed. Default ON may suit frequent documentation-heavy tasks,
but actual user frequency and provider token impact were not measured here.

## Verification and remaining acceptance

Seven isolated tests pass, including source-unavailable installed references,
idempotent hardening, unchanged MCP fixture values, local-drift protection and
lossless MCP toggles. Source-unavailable testing moves a temporary source copy,
not the live Downloads repository. Four installs were synchronized.

Antigravity now supplies actual routing evidence. Codex supplies partial routing
evidence only: its read-only sandbox did not expose the installed Andino body, even
though normal discovery/configuration is present. Keep Claude and Meda/OpenCode
recorded as external/provider blocked until their owners restore access. Read-only
routing probes, config parses and frontmatter checks cannot substitute for normal
desktop behavior. Overall acceptance remains PARTIAL; do not declare four-host
behavioral parity proven.

## Verified mechanism references

- [Claude skill invocation controls](https://code.claude.com/docs/en/skills): manual-only mode blocks model invocation, not merely discovery.
- [OpenCode V1 skill permissions](https://opencode.ai/docs/skills/): use the installed V1 permission mechanism, not V2 metadata as enforcement.
- [Antigravity skill discovery](https://antigravity.google/docs/skills): descriptions guide selection; a native non-implicit switch was not established.
- Codex local skill-creator `references/openai_yaml.md` documents its implicit policy; installed app-server schema/discovery validated configuration parsing.
