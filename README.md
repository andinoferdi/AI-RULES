# AI Codebase Rescue

Stabilizes fragile, patch-heavy code and bounded subsystems. It chooses KEEP, REFACTOR, REMAKE, REMOVE, or INVESTIGATE for each part from engineering evidence, and it establishes regression protection. AI authorship alone never justifies a rewrite.

## When to use

- Repeated regressions in the same area.
- Technical-debt recovery in a bounded subsystem.
- Production hardening of a fragile prototype.
- A bounded remake, when the evidence supports one.

## Limits

Not for routine local bugs, formatting, cosmetic cleanup, ordinary features, or code that is only described as AI-written. Use the normal workflow for these.

## Requires

None. It works standalone.

## Install

Requirements: Python 3.11+, Git, and an installed agent for CLI setup.

With the AI-RULES CLI (recommended):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup --capability ai-codebase-rescue --host <host>
```

Pass `--host` with `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`. Without it, setup targets Codex. For a project install, add `--scope project --project-root <path>`. Run the same command again to update.

Manual, for this skill only:

```sh
git clone --depth 1 --single-branch --branch ai-codebase-rescue https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/ai-codebase-rescue"
```

Install the whole folder, not only `SKILL.md`. The folder must keep the name `ai-codebase-rescue`. For another host, change the destination to the folder in this table:

| Host | Global folder |
| --- | --- |
| Codex | `~/.agents/skills/ai-codebase-rescue` |
| OpenCode | `~/.config/opencode/skills/ai-codebase-rescue` |
| Claude Code | `~/.claude/skills/ai-codebase-rescue` |
| Antigravity IDE and 2.0 | `~/.gemini/config/skills/ai-codebase-rescue` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/ai-codebase-rescue` |

For project scope, use `.agents/skills/ai-codebase-rescue` (Codex, OpenCode, Antigravity) or `.claude/skills/ai-codebase-rescue` (Claude Code) in the project root. Keep one copy per skill, and reload the host session after installing.

## Use

- Codex: `$ai-codebase-rescue <task>`
- Claude Code: `/ai-codebase-rescue <task>`
- OpenCode: ask the agent to use `ai-codebase-rescue`, or use the command that setup registers.
- Antigravity: ask the agent to use `ai-codebase-rescue`. In the IDE, check Customizations.

Example: `$ai-codebase-rescue investigate repeated checkout regressions within the payment module`

Activating a skill grants no extra permission. A rescue request alone does not authorize commits, pushes, publication, deployment or live-data operations.

## Notes

- To combine it with Andino, install `andino-workflow` as a separate folder under the same skill root. Andino coordinates the task and may route eligible rescue work here. Andino's plan stays the only lifecycle owner. Installing both does not activate both.

## Verify and explore

Keep one complete skill directory and preserve local edits before re-running setup.
Setup checks package files; native discovery and behavior need a separate session
check. After reloading the host, try a bounded repeated-regression request and
expect evidence before a KEEP/REFACTOR/REMAKE/REMOVE/INVESTIGATE decision. A request
to fix a typo should stay a normal local edit.

The [runtime contract](SKILL.md), [audit taxonomy](references/audit-taxonomy.md),
[regression guidance](references/regression-and-verification.md), and
[validation scenarios](references/validation-scenarios.md) explain the method.
The [main quality plane](https://github.com/andinoferdi/AI-RULES/tree/main)
owns installer tests and package validation; this branch distributes the entrypoint
and focused references. Consult source history and any applicable resource notices
for provenance; this README adds no license grant.
