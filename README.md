# Andino Workflow

An adaptive problem-solving protocol for AI agents. It matches the depth of investigation to the task, separates your goal from a suspected cause, and asks only about decisions the available context cannot settle. It covers development, troubleshooting, research, decisions, daily tasks, and conversation.

## When to use

- You name it explicitly, for any task, including a simple question.
- A problem is uncertain or spans several steps.
- You resume a task with a saved plan. It checks for repository drift first.
- A bug has an unknown cause.
- You need thesis progress or next steps, with `skripsi-skill` when it is installed.
- You need UI/UX design or evaluation.

## Limits

Routine conversation and trivial mechanical edits outside mapped needs do not trigger it automatically. Name it explicitly if you want it anyway.

## Requires

`focus` and `search-first`. Setup installs both as required dependencies. A manual clone does not, so use `ai-rules setup --capability andino-workflow --host <host>` to get the full set.

## Install

With the AI-RULES CLI (recommended):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup --capability andino-workflow --host <host>
```

Pass `--host` with `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`. Without it, setup targets Codex. For a project install, add `--scope project --project-root <path>`. Run the same command again to update.

Manual, for this skill only:

```sh
git clone --depth 1 --single-branch --branch andino-workflow https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/andino-workflow"
```

Install the whole folder, not only `SKILL.md`. The folder must keep the name `andino-workflow`. For another host, change the destination to the folder in this table:

| Host | Global folder |
| --- | --- |
| Codex | `~/.agents/skills/andino-workflow` |
| OpenCode | `~/.config/opencode/skills/andino-workflow` |
| Claude Code | `~/.claude/skills/andino-workflow` |
| Antigravity IDE and 2.0 | `~/.gemini/config/skills/andino-workflow` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/andino-workflow` |

For project scope, use `.agents/skills/andino-workflow` (Codex, OpenCode, Antigravity) or `.claude/skills/andino-workflow` (Claude Code) in the project root. Keep one copy per skill, and reload the host session after installing.

## Use

- Codex: `$andino-workflow <task>`
- Claude Code: `/andino-workflow <task>`
- OpenCode: ask the agent to use `andino-workflow`, or use the command that setup registers.
- Antigravity: ask the agent to use `andino-workflow`. In the IDE, check Customizations.

Example: `$andino-workflow resume the existing task plan and check repository drift`

Activating a skill grants no extra permission.

## Notes

- `focus` is the default communication style for every invocation, including direct answers.
- Andino loads other installed skills only when the task needs them, for example `search-first` for research or `ai-codebase-rescue` for codebase stabilization.
- To combine it with a specialist, install `ai-codebase-rescue` or `skripsi-skill` as a separate folder under the same skill root. Andino coordinates the work, and its plan stays the only lifecycle owner. Neither package installs the other.
