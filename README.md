# Search First

AI-RULES' first-party adaptation of Affaan Mustafa's ECC Search First methodology:
NEED ANALYSIS → SEARCH → EVALUATE → DECIDE → APPROVED IMPLEMENTATION.
Find existing solutions, evaluate fit and recommend ADOPT, EXTEND, COMPOSE or BUILD.

## Install and invoke

Install the CLI from [AI-RULES main](https://github.com/andinoferdi/AI-RULES/tree/main),
then run:

```sh
ai-rules setup --capability search-first
```

Choose host and scope through setup, or provide `--host codex --scope project
--project-root PATH`. Run setup again for updates. No Andino dependency is required.
Normal `ai-rules setup` profiles include Andino, which requires Focus and Search
First; installation does not activate research on every task.

Reload the host's catalog/session as needed. In Codex select `$search-first [task]`.
Claude Code supports `/search-first`; OpenCode uses setup's generated command, and
Antigravity uses its registered CLI skill or IDE workflow where supported. Follow
actual native invocation controls; file registration is not evidence of a
successful running-agent invocation.

With `$andino-workflow [task]`, Andino selects and loads the actual installed
Search First when solution research is needed and native controls permit it.
Manual-only or denied skills are not silently bypassed. Andino remains the sole
workflow owner. Focus remains the communication layer.

Examples: investigate authentication options for the project's stack, check
whether a utility exists before creating it, or find supported alternatives to
an incompatible SDK. A typo fix needs no research. An unknown bug stays with
the debugging methodology. No specific search service or MCP is required.

## Proactive online research

When local evidence leaves material external uncertainty, Search First calls the
host's authorized search/page-reading tools without another request to browse.
Triggers include unfamiliar APIs, version/release changes, current maintenance,
reported problems and supported alternatives after an approach fails. Local reuse,
trivial edits and settled facts do not require browsing. Pure research returns a
sourced synthesis rather than forcing an implementation decision.

Native tools come first, using actual host schemas. Claude Code can use exposed
WebSearch/WebFetch; other hosts use their discovered tools. Existing GitHub,
Context7 or configured MCP tools may fill remaining gaps. This package provides
no network access or mandatory provider. It distinguishes discovery, execution and
useful evidence, and reports offline/denied boundaries honestly.

Official version-matched docs and maintainer issues/releases support API decisions.
Stack Overflow and community advice need age/version checks and corroboration.
Merged PRs and closed issues do not establish a released fix. Read consequential
sources; qualify snippet-only evidence. Queries are minimized and stripped of
secrets/private data; retrieved instructions cannot override trusted rules.
Browser fallback is permitted public reading for presentation limitations, never
permission bypass, login, forms, external writes or automatic downloads/installs.

Package contents: README.md, SKILL.md, references/license.md and the on-demand
[online research playbook](references/online-research.md). Copy the whole folder.
See [main evaluation evidence](https://github.com/andinoferdi/AI-RULES/tree/main/docs/validation/search-first)
for tested revisions and limits; instructions alone do not establish live behavior
or cross-host parity. Manual smoke cases: investigate a version-sensitive SDK with
permitted web tools; reuse an existing local utility; repeat without online tools
and verify honest uncertainty. Never overwrite a locally modified installation.

## Provenance and adaptation

Read [SKILL.md](SKILL.md) for runtime instructions. The upstream source is
[ECC's .kiro Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md),
by Affaan Mustafa, licensed under [MIT](references/license.md). AI-RULES maintains
this adaptation; it does not claim authorship of the original methodology.

This preserves repository/package/skill/MCP/GitHub/docs discovery, candidate
evaluation and all four decisions. It replaces mandatory subagent research with
proportional host-permitted research, reuses existing authorization and keeps
orchestration in Andino. It adds version checks, evidence limits, reconsideration
after failed approaches and a sufficient-evidence stopping rule.
