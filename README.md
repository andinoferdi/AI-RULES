# Search First

Finds existing solutions before you write custom code. It searches local code and online sources, judges how well each option fits, and recommends ADOPT, EXTEND, COMPOSE, or BUILD for implementation decisions. Pure research requests get a sourced synthesis instead.

## When to use

- You are choosing a library, SDK, or integration.
- You want to check whether a utility already exists before building it.
- You work with a version-sensitive API, or you need an alternative after an approach failed.
- You ask for technical research.

## Limits

Trivial edits, typo fixes, and settled local answers need no research. Unknown bugs belong to debugging. Without search or page-reading tools, unresolved online claims are marked UNKNOWN.

## Requires

None. No search service, paid API, or MCP server is required.

## Install

With the AI-RULES CLI (recommended):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup --capability search-first --host <host>
```

Pass `--host` with `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`. Without it, setup targets Codex. For a project install, add `--scope project --project-root <path>`. Run the same command again to update.

Manual, for this skill only:

```sh
git clone --depth 1 --single-branch --branch search-first https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/search-first"
```

Install the whole folder, not only `SKILL.md`. The folder must keep the name `search-first`. For another host, change the destination to the folder in this table:

| Host | Global folder |
| --- | --- |
| Codex | `~/.agents/skills/search-first` |
| OpenCode | `~/.config/opencode/skills/search-first` |
| Claude Code | `~/.claude/skills/search-first` |
| Antigravity IDE and 2.0 | `~/.gemini/config/skills/search-first` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/search-first` |

For project scope, use `.agents/skills/search-first` (Codex, OpenCode, Antigravity) or `.claude/skills/search-first` (Claude Code) in the project root. Keep one copy per skill, and reload the host session after installing.

## Use

- Codex: `$search-first <task>`
- Claude Code: `/search-first <task>`
- OpenCode: ask the agent to use `search-first`, or use the command that setup registers.
- Antigravity: ask the agent to use `search-first`. In the IDE, check Customizations.

Example: `$search-first compare authentication options for this project's stack`

Activating a skill grants no extra permission.

## Notes

- With `andino-workflow`, Andino loads Search First when research is needed and the host permits it. Installing it does not run research on every task.
- Adapted from [ECC Search First](https://github.com/affaan-m/ECC/blob/main/.kiro/skills/search-first/SKILL.md) by Affaan Mustafa under the MIT license. The notice is in `references/license.md`.
