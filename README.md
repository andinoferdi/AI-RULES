# Focus

A communication style for AI answers. It puts the answer or result first, uses short concrete steps, and removes filler, while keeping the detail, evidence, and uncertainty you need. It matches the language you write in.

## When to use

- You want direct answers without filler.
- You want steps you can follow right away.
- You want status updates that say what is done and what comes next.

## Limits

Focus changes how work is written. It does not reduce investigation, verification, or scope. Your explicit style requests override it.

## Requires

None. Every `ai-rules setup` profile includes Focus through Andino's dependency.

## Install

With the AI-RULES CLI (recommended):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup --capability focus --host <host>
```

Pass `--host` with `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`. Without it, setup targets Codex. For a project install, add `--scope project --project-root <path>`. Run the same command again to update.

Manual, for this skill only:

```sh
git clone --depth 1 --single-branch --branch focus https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/focus"
```

Install the whole folder, not only `SKILL.md`. The folder must keep the name `focus`. For another host, change the destination to the folder in this table:

| Host | Global folder |
| --- | --- |
| Codex | `~/.agents/skills/focus` |
| OpenCode | `~/.config/opencode/skills/focus` |
| Claude Code | `~/.claude/skills/focus` |
| Antigravity IDE and 2.0 | `~/.gemini/config/skills/focus` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/focus` |

For project scope, use `.agents/skills/focus` (Codex, OpenCode, Antigravity) or `.claude/skills/focus` (Claude Code) in the project root. Keep one copy per skill, and reload the host session after installing.

## Use

- Codex: `$focus <request>`
- Claude Code: `/focus <request>`
- OpenCode: ask the agent to use `focus`, or use the command that setup registers.
- Antigravity: ask the agent to use `focus`. In the IDE, check Customizations.

Example: `$focus explain how to roll back the last database migration`

To turn it off, say `stop focus`. Activating a skill grants no extra permission.

## Notes

- With Andino, Focus loads once automatically. You do not invoke it again.
- Focus owns no plan, tool permissions, or task execution.
- For web chatbots, copy `A. PRIORITAS` and `X. FOCUS` from the [WebBased branch README](https://github.com/andinoferdi/AI-RULES/tree/WebBased).
- Adapted from [i-have-adhd](https://github.com/ayghri/i-have-adhd) by Ayoub Ghriss under the MIT license. The notice is in `references/license.md`.
