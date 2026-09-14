# ANDINO-001 — Cross-agent workflow refactor

Status: DONE
Current phase: Local implementation and validation complete

## Objective
Implement the authoritative Downloads/PROMPT.txt specification: four peer primary-capable hosts, a bounded andino-workflow router, portable ticket state, lean rules and reversible local configuration cleanup.

## Acceptance criteria
- One canonical andino-workflow with viable access from Codex, Claude Code, Antigravity and OpenCode.
- Compact project rules, bootstrap/task/bug/resume prompts and durable execution-plan template.
- Actual skill/MCP inventory and evidence-based defaults; alternatives remain recoverable.
- Supported config only; secrets stay outside this repository; no remote mutations or commits.
- Validate references, skill metadata, config syntax, synchronization and routing scenarios A–H.

## Constraints and decisions
- User confirmed PROMPT.txt overrides historical brainstorms. Current repository/config beats stale inventories; official current docs verify host mechanics.
- Active host is primary for that session. Memory is targeted historical context, available to any working integration, never a handoff dependency.
- Plan records outcomes and evidence, never raw reasoning, logs or duplicated source.
- Work directly in the initially clean checkout; preserve unrelated prompt library and user data.
- No commit, push, merge, publish, deploy, subscription purchase or new authentication.

## Dynamic phases
1. DONE — Audit actual settings/skills/hooks and official mechanics. Identified OpenCode V1 versus V2 schema difference and separate Antigravity current/legacy directories; evidence and sources in docs/audit.md.
2. DONE — Refactored prompts/core; preserved personal prompt library and domain references; canonical workflow/template and A–H routing inspections complete.
3. DONE — Backed up local config outside Git; synchronized workflow to four hosts; manualized overlapping skills; disabled duplicate MCPs/bootstrap and orphan hooks. Native Codex/OpenCode discovery succeeded. Config parsing and provider/credential preservation passed.
4. DONE — Final catalog/runtime limitations recorded; five isolated adapter tests, links, skill validator, known-credential scan and diff whitespace check passed. Native Codex plugin listing confirms Superpowers disabled and memory enabled.

## Findings
- Historical router mandates another bootstrap and defaults Ponytail on all coding; new contract supersedes these triggers.
- README is an 18,029-line general prompt library. Preserve its unrelated content as an on-demand reference rather than discard it.
- claude-mem retrieval is exposed in this Codex session, but observer currently fails on OpenRouter daily quota; no restart or credentials changed.
- Current Antigravity MCP file has one claude-mem server; legacy file has 18 entries. Defaults now 1/1/2/1 for Codex/Claude/OpenCode/current Antigravity; legacy retained with two defaults.
- Backup directory: ~/.andino/backups/20260914-193824. Catalog and sanitized verification JSON are under ~/.andino; never copy the backup's credential-bearing config into Git.
- Original personal prompt library content matches Git HEAD after normalizing working-tree CRLF versus Git LF.

## Files / areas touched
- AI-RULES: README, root AGENTS, existing prompt/core files, prompts/, skills/andino-workflow/, adapters/, scripts/, docs/, and references/personal-prompt-library.md.
- Local: relevant host instruction/config files, standalone/manual skill installs, MCP manual library and helper; no business project source changes.

## Verification evidence
- Initial `git status --short`: clean.
- Python 3.12.10 available; existing TOML and JSON host configs parse.
- `scripts/validate.py`: 5 tests pass (sync identity/idempotency/drift protection and lossless MCP toggles), Markdown links pass.
- Codex skill-creator `quick_validate.py`: Skill is valid.
- `scripts/sync-workflow.py --check`: all 4 generated installs match canonical source.
- Codex `features list` and app-server `skills/list`: exit/success; Andino and core found, zero discovery errors. OpenCode `--pure debug config/skill`: valid and Andino found, build steps=40.
- Claude `agents --json`: exit 0; JSON listing. Antigravity verification is filesystem/frontmatter + official path support, not live model execution.
- `git diff --check`: pass. Known local credential values absent from repository; MCP non-toggle fields and custom provider/model/credentials preserved.
- Structural measurements: Agents 1017→46 lines; bootstrap 370→12; per-message reminder 835→6; task prompt 198→13. No provider token/cache savings claimed.
- Codex app-server strict config accepted retained tool-output budget 6000 and max concurrent subagents 3; skills/list still returns Andino/core with no discovery errors.

## Blockers / unknowns
- Live model routing in all four UIs not exercised. Existing sessions can retain old plugin/tool catalogs until reload.
- claude-mem observer remains quota-limited; only user may restart the worker. No handoff dependency on it.

## Plan revisions
- Preserve OpenCode V1 config rather than adopting latest V2 syntax; explicit command fallback for manual skills.
- Preserve Claude plugin capture/retrieval bundle; unsupported per-plugin skill visibility controls are not invented. Optional memory workflows are explicitly manual by routing contract.

## NEXT ACTION
No local implementation work remains. For the next real ticket, invoke andino-workflow or continue its plan on the active host. If a running host shows an old catalog, reload it before testing new routing. Optional live model/UI checks can be recorded separately; do not repeat completed audit phases. The existing memory quota outage is independent of handoff and remains unresolved.
