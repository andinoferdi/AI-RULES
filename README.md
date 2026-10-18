# Focus

A communication style for AI answers. It puts the answer or result first, uses short concrete steps, and removes filler, while keeping the detail, evidence, and uncertainty you need. It matches the language you write in.

## When to use

- You want direct answers without filler.
- You want steps you can follow right away.
- You want status updates that say what is done and what comes next.

## Limits

Focus changes how work is written. It does not reduce investigation, verification, or scope. Your explicit style requests override it.

It is unnecessary when the current style already fits your request. It supplies
no research method, implementation workflow, or independent factual authority.

## Requires

None. Every `ai-rules setup` profile includes Focus through Andino's dependency.

## Install

Requirements: Python 3.11+, Git, and an installed agent for CLI setup.

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

- Andino's contract calls for Focus as its default communication layer. Actual loading follows the host's permitted invocation mechanism; installation alone does not activate it.
- Focus owns no plan, tool permissions, or task execution.
- For web chatbots, copy `A. PRIORITAS` and `X. FOCUS` from the [WebBased branch README](https://github.com/andinoferdi/AI-RULES/tree/WebBased).
- Adapted from [i-have-adhd](https://github.com/ayghri/i-have-adhd) by Ayoub Ghriss under the MIT license. See the [retained notice](references/license.md).

## Verify

Preserve the whole folder and local edits when updating. Setup verifies files;
after reloading, invoke Focus and check that a practical answer leads with usable
steps and retains relevant uncertainty. An explicit request for a formal style
should still be honored. These are manual checks, not claimed live-host results.

[SKILL.md](SKILL.md) defines the loading contract for the bundled Priority A and
both language references. Main's [package validator](https://github.com/andinoferdi/AI-RULES/blob/main/scripts/validate_skills.py)
also compares those references with WebBased without changing either source.
