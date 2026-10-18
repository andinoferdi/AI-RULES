# Skripsi Skill

A thesis and research workflow for AI agents. It guides topic, proposal, literature, methodology, analysis, revision, and defense preparation from your current stage. It keeps approved decisions and evidence limits explicit, and it follows institutional guidance.

## When to use

- Planning a research topic or checking a title.
- Writing a proposal or a thesis chapter.
- Literature synthesis or a systematic review.
- Revising a thesis after supervisor feedback.
- Preparing for a defense.

## Limits

Single-sentence polishing, unrelated coding, and ordinary conversation do not need the full workflow.

## Requires

None. It works standalone. The companion `andino-workflow` is optional (see Notes).

## Install

Requirements: Python 3.11+, Git, and an installed agent for CLI setup.

With the AI-RULES CLI (recommended):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup --capability skripsi-skill --host <host>
```

Pass `--host` with `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`. Without it, setup targets Codex. For a project install, add `--scope project --project-root <path>`. Run the same command again to update.

Manual, for this skill only:

```sh
git clone --depth 1 --single-branch --branch skripsi-skill https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/skripsi-skill"
```

Install the whole folder, including `references/` and `assets/`. The folder must keep the name `skripsi-skill`. For another host, change the destination to the folder in this table:

| Host | Global folder |
| --- | --- |
| Codex | `~/.agents/skills/skripsi-skill` |
| OpenCode | `~/.config/opencode/skills/skripsi-skill` |
| Claude Code | `~/.claude/skills/skripsi-skill` |
| Antigravity IDE and 2.0 | `~/.gemini/config/skills/skripsi-skill` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/skripsi-skill` |

For project scope, use `.agents/skills/skripsi-skill` (Codex, OpenCode, Antigravity) or `.claude/skills/skripsi-skill` (Claude Code) in the project root. Keep one copy per skill, and reload the host session after installing.

## Use

- Codex: `$skripsi-skill <request>`
- Claude Code: `/skripsi-skill <request>`
- OpenCode: ask the agent to use `skripsi-skill`, or use the command that setup registers.
- Antigravity: ask the agent to use `skripsi-skill`. In the IDE, check Customizations.

Example: `$skripsi-skill My title is approved. Help me outline the proposal for chapters 1 to 3.`

Activating a skill grants no extra permission. Skill activation does not authorize commits, pushes, merges, publication, deployment, live-data changes or unrelated external actions.

## Notes

- With `andino-workflow`, Andino owns the lifecycle, plan, and checkpoints. Skripsi Skill returns research findings and recommended actions without a competing plan. Install both as separate folders under the same skill root. Installing both does not activate both.

## Research integrity and verification

The [runtime contract](SKILL.md) and
[evidence guidelines](references/evidence-guidelines-integrity.md) require traceable
sources and honest limits. They do not supply missing literature, participant data,
ethics approval, or campus requirements. Use your institution's actual guidance.
The [research templates](assets/research-core-templates.md) support that work;
they are not completed research evidence.

Preserve the full references/assets directories and local edits before updating.
After reloading the host, provide your approved topic and current stage: expect
guidance for that stage without reopening settled decisions. A single-sentence
polish should not start the full workflow. These are manual smoke cases; setup
verifies files rather than academic correctness or live host behavior.

The [main quality plane](https://github.com/andinoferdi/AI-RULES/tree/main)
owns evaluation cases, requirement traceability and installer tests. Consult source
history and applicable notices for provenance; this README adds no license grant.
