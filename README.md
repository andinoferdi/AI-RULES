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
