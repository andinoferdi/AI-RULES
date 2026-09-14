# ANDINO-001 audit — 2026-09-14

Historical baseline: later core invocation hardening and current acceptance status
are recorded in [ANDINO-002 acceptance audit](acceptance-audit.md). Counts and
default worker eligibility below describe the earlier implementation snapshot.

## Decision and evidence

PROMPT.txt and the user's clarification are authoritative. Historical brainstorms and
Skills.txt are not current inventories. One bounded router manages a portable plan;
all four hosts can independently lead. No permanent host roles or memory dependency.

The initial Git tree was clean. Actual binaries: Codex CLI 0.152.1, Claude Code 2.1.258,
OpenCode 1.18.30. Antigravity has both legacy and current configuration directories;
the current global MCP file contains one server, not the 18 in the legacy file.
Secrets were inspected only through allowlisted metadata; backups remain under the
user's `.andino/backups/20260914-193824`, outside Git.
One pre-existing Claude project-scoped Draw.io entry remains scoped to its original
project; the global cleanup does not override that explicit project integration.

## Material changes

- README's 18,029-line unrelated personal prompt library moved intact to a manual
  reference. README now explains installation, task/resume and source boundaries.
- Core Agents.md is a thin contract and domain dispatcher. First-prompt is bootstrap
  only; Send-to-every-prompt is a reminder, not a repeated payload. Task and bug prompts
  no longer force the same investigation/approval ceremony for every edit.
- Detailed frontend/backend/Git/product specifications remain lazy. Chat rules no
  longer force reading both language references. Accepted UI coexistence policy is
  preserved as one reference, loaded only when relevant.
- One canonical Andino skill and identical hash-tracked generated copies. Sync rejects
  unreviewed local edits. Existing project-specific rules are not mass-rewritten.

## MCP disposition

Counts are configured direct servers, excluding plugin/app connectors and session caches.

| Host / scope | Initially enabled | New defaults | Disposition |
| --- | --- | --- | --- |
| Codex user | 12 | context7 (1) | 11 disabled in place |
| Claude user | 16 | context7 (1) | 15 moved to local manual configuration library |
| OpenCode V1 user | 17 | context7, claude-mem (2) | 15 disabled in place |
| Antigravity current | 1 | claude-mem (1) | retained |
| Antigravity legacy | 18 | context7, claude-mem (2) | 16 disabled to prevent old defaults returning |

Filesystem, Git, Fetch and Node REPL duplicates are disabled/manual because native
file/search/shell/Git/web capabilities cover ordinary work. Sequential Thinking is
default-off because it adds a second reasoning/tool loop. Browser automation is
selected per question; Playwright and DevTools no longer start together by default.
StarUML, Premiere, Blender, Cheat Engine, Draw.io and service-specific Figma/Vercel/
Sentry/Supabase/GitHub connections remain available for relevant work.

No MCP credentials or definitions were permanently deleted. `scripts/mcp-toggle.py`
re-enables an existing server without revealing secrets. Optional servers are explicitly
toggled; this is not a claim of automatic project-scoped or lazy process startup.
Existing app/plugin connectors stay under their native discovery mechanisms; disabling
direct MCP entries does not disable the corresponding Codex app/plugin.

## Skills and workflow ownership

Core in every host: andino-workflow, systematic-debugging, test-driven-development,
verification-before-completion and code-review-and-quality. Selected Superpowers 6.3.0
workers are installed standalone; the global Superpowers plugin/bootstrap is disabled.
Antigravity's old Superpowers 6.0.3 and Addy plugin packages are preserved outside automatic
plugin discovery. Vendor caches are not patched.
Three orphan Codex Serena hook groups were disabled after verifying their referenced
`serena-hooks` executable is absent. Their original hook file is backed up.

The following overlapping local groups are manual: agent-skills/using-agent-skills,
planning-and-task-breakdown/spec/constraint/idea/interview/doubt/incremental workflows,
the alternate debugger/TDD method, code-simplification, Ponytail family, legacy docx
and taste alias. Retired router entries redirect to Andino without a second lifecycle.
Specialists with distinct domain purposes remain eligible only for those domains.

Codex uses native implicit-invocation policy; Claude uses frontmatter manual controls.
OpenCode V1 uses skill permissions plus `/manual-<skill-id>` commands that read exact
preserved sources. Antigravity's manual alternatives are outside discovery, accessible
by recorded file path. The local `~/.andino/skill-catalog.json` records each disposition,
source and callable/readable path; alternatives are not four editable workflow sources.
Plugin catalogs are a distinct exception: Claude's documented `skillOverrides` does
not apply to plugin skills. claude-mem's capture/MCP bundle is retained; its optional
planning/full-codebase workflows are manual by the global routing contract, not falsely
claimed to be hidden by a nonexistent plugin setting. Vendor updates require re-audit.

## Memory and providers

claude-mem remains enabled as historical retrieval in Codex/Claude plugins and
OpenCode/Antigravity integrations. OpenCode keeps capture and MCP retrieval; its redundant
capture-plugin search tool is disabled. Startup observation count reduced 50 → 10,
session count 10 → 2, terminal output and last-summary injection disabled; semantic
per-prompt injection disabled. Targeted explicit retrieval remains available.

Observer outage is an existing OpenRouter free daily quota failure. No credentials,
subscription or provider changed, and the worker was not restarted. Worker-loaded
settings may need the user to restart; a restart does not itself replenish daily quota.
Memory is never needed for plan handoff.

OpenCode uses custom `meda/deepseek-chat` and other proxy providers. Current DeepSeek
documentation is not evidence that those proxies expose the same model/protocol.
Provider/model options were preserved rather than adding unverified thinking settings.
Codex's existing medium reasoning effort was retained. Task-level effort selection is
behavioral unless the active host exposes a real control.

## Guards and measurements

Codex retained tool-output history budget: 6,000 tokens per result; concurrent subagent
ceiling: 3, while routing still defaults to zero spawned agents. These supported settings
passed the installed app-server's strict configuration loader. They limit retained output
and concurrency, not total task token spend.

OpenCode V1 build steps: 40; existing explorer subagent: 12. These are supported step
caps and conservative local defaults, not measured optimal values. The workflow requires
a checkpoint before exhaustion. No unsupported universal step/output/retry settings added.

Behavioral: same-state result reuse, no unproductive A/B tool cycles, at most two transient
retries, targeted output slices, no automatic graph rebuild, no default subagents, and
no repeated verification without changed evidence. Default subagents for this refactor: zero.

Counts measure file/catalog structure, not provider input tokens, cache hit rate, latency
or runtime savings. Current sessions may retain their old tool/skill catalogs until reload.

| Entry | Before lines | After lines |
| --- | ---: | ---: |
| Project core template | 1,017 | 46 |
| Bootstrap | 370 | 12 |
| Per-prompt reminder | 835 | 6 |
| Task prompt | 198 | 13 |

The filesystem inventory covers 831 skill definitions including cached vendor versions,
with 439 distinct content hashes. These are not 831 active skills. Local user-root
implicit-eligible counts after cleanup are Codex 20 (plus shared/system skills), Claude
27, OpenCode 56 and Antigravity 9; plugin catalogs are separate. Exact sources/dispositions
and actual catalog evidence remain in the sanitized local audit files.

## Verified official sources and compatibility decisions

- [Codex skills](https://learn.chatgpt.com/docs/build-skills): `.agents/skills`, progressive
  loading, generated installs and implicit invocation policy. [Configuration](https://learn.chatgpt.com/docs/config-file/config-reference)
  documents server disable flags. [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  defines instruction discovery. Existing `.codex/skills` is also visible in this actual session.
- [Claude skills](https://code.claude.com/docs/en/skills): native manual controls and
  user skill paths. [Memory/instructions](https://code.claude.com/docs/en/memory) and
  [MCP](https://code.claude.com/docs/en/mcp) distinguish user config from per-project
  disabled-server lists; a per-project opt-out was not misrepresented as a global flag.
- [OpenCode V1 skills](https://opencode.ai/docs/skills/), [MCP](https://opencode.ai/docs/mcp-servers/)
  and [agents](https://opencode.ai/docs/agents/) match the installed V1 CLI. V2's
  [autoinvoke metadata](https://opencode.ai/v2/docs/skills) and
  [mcp.servers / disabled](https://opencode.ai/v2/docs/mcp-servers) were verified but
  deliberately not substituted into V1. No claim of V2 Code Mode enforcement on V1.
- [Antigravity skills](https://antigravity.google/docs/skills),
  [MCP](https://antigravity.google/docs/mcp) and [rules](https://antigravity.google/docs/rules-workflows):
  current `.gemini/config` paths, `disabled` and global GEMINI.md. Existing local
  migration evidence corroborates the new paths; legacy configs remain recoverable.
- [Agent Skills specification](https://agentskills.io/specification): portable lowercase
  ID, compact name/description frontmatter and progressive disclosure.
- [Superpowers source/version](https://github.com/obra/superpowers/blob/main/.claude-plugin/plugin.json):
  6.3.0, MIT. Installed session-start hook loads using-superpowers automatically;
  standalone workers avoid that bootstrap while preserving their methods.
- [claude-mem configuration](https://docs.claude-mem.ai/configuration): bounded startup
  context. Actual installed Codex tools and OpenCode/Antigravity integration files
  establish cross-host availability, not proof the currently failing observer works.
- [DeepSeek thinking/tool protocol](https://api-docs.deepseek.com/guides/thinking_mode/):
  preserve protocol-required reasoning fields; do not infer custom proxy capabilities.

## Validation

See [routing scenarios](routing-scenarios.md) for A–H inspection and the final execution
checkpoint for actual command results. Static checks do not prove model routing on all
four live UIs. Host reload and unavailable live generation checks are reported separately.

Codex app-server `skills/list` from the installed binary found Andino and the core workers
with no discovery errors. Its protocol does not expose implicit-invocation policy in
the listing; policy is validated from metadata and official support, not inferred from
`enabled: true`. OpenCode `--pure debug config/skill` parsed config and found Andino.
Claude `agents --json` returned successfully; the interactive form initially required
a TTY, so the documented noninteractive form was used. Antigravity path/frontmatter
validation is static; no live model invocation was used as a substitute for these checks.
The installed Codex `plugin list --json` confirms Superpowers disabled and claude-mem
enabled. The desktop's already-open session may still display its old plugin skill list.
