# Natural Writing

A writing skill for Indonesian and English prose. It writes, rewrites and reviews requested documents so they read naturally and fit their reader, while keeping facts, numbers, citations, technical terms and the required depth intact.

## When to use

- You want an essay, article, report, email draft, documentation prose or an academic section written well.
- You want existing text rewritten for clarity and naturalness without changing what it says.
- You want a review of writing quality without the file being changed.

## Limits

Natural Writing governs prose inside writing artifacts. It does not handle ordinary chat answers, code, JSON or other machine-readable output, statistics, research validity or task orchestration. It never promises that text will pass AI detectors.

An artifact is classified by purpose, not location: an essay written in chat is still an artifact. Its length, structure and depth follow the request and the genre, not conversational brevity.

## Requires

None. It works standalone. With other AI-RULES skills:

- Focus keeps the surrounding communication (progress, explanations, completion reports) concise and never shortens the artifact body.
- Skripsi Skill keeps authority over academic research, evidence and campus rules; Natural Writing only refines how supported content is expressed.
- Andino Workflow routes to it as a native sibling when the task needs artifact prose work, and keeps the lifecycle.

## Install

Requirements: Python 3.11+, Git, and an installed agent for CLI setup.

With the AI-RULES CLI (recommended):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup --capability natural-writing --host <host>
```

Pass `--host` with `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`. Without it, setup targets Codex. For a project install, add `--scope project --project-root <path>`. Run the same command again to update. The `everything` and `research-skripsi` profiles include it; installing it does not activate it on every task.

Manual, for this skill only:

```sh
git clone --depth 1 --single-branch --branch natural-writing https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/natural-writing"
```

Install the whole folder, not only `SKILL.md`. The folder must keep the name `natural-writing`. For another host, change the destination to the folder in this table:

| Host | Global folder |
| --- | --- |
| Codex | `~/.agents/skills/natural-writing` |
| OpenCode | `~/.config/opencode/skills/natural-writing` |
| Claude Code | `~/.claude/skills/natural-writing` |
| Antigravity IDE and 2.0 | `~/.gemini/config/skills/natural-writing` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/natural-writing` |

For project scope, use `.agents/skills/natural-writing` (Codex, OpenCode, Antigravity) or `.claude/skills/natural-writing` (Claude Code) in the project root. Keep one copy per skill, and reload the host session after installing.

## Use

- Codex: `$natural-writing <request>`
- Claude Code: `/natural-writing <request>`
- OpenCode: ask the agent to use `natural-writing`, or use the command that setup registers.
- Antigravity: ask the agent to use `natural-writing`. In the IDE, check Customizations.

Examples:

- Rewrite: `/natural-writing rewrite this English technical report for clarity; keep claims, numbers, API names, code and citations`
- Review: `/natural-writing review this Indonesian article for repetition and inconsistent register; do not modify the file`
- Write, with other skills: `use andino-workflow, skripsi-skill, search-first, natural-writing and focus to write this thesis section from verified sources in natural Indonesian academic prose`

The three modes are Write (new prose from supplied facts), Rewrite (meaning-preserving edits) and Review (prioritized findings, original unchanged). Activating a skill grants no extra permission.

## Package

- [SKILL.md](SKILL.md): activation, modes, ownership, protected content and verification.
- [references/indonesian-writing.md](references/indonesian-writing.md) and [references/english-writing.md](references/english-writing.md): independent guidance per language.
- [references/academic-writing.md](references/academic-writing.md): claim strength, citation integrity and institutional precedence.
- [references/editing-and-review.md](references/editing-and-review.md): Rewrite and Review procedures.

## Verify

After reloading, invoke it with a short paragraph that contains a number and a citation and ask for a rewrite: both must survive unchanged. Ask for a review: the file must stay unchanged. Ask an unrelated coding question: the skill should not be used. These are manual checks; main's validators and semantic-preservation tests live in the [main branch](https://github.com/andinoferdi/AI-RULES/tree/main).

## Provenance

Original AI-RULES work by Andino Ferdiansah under the [MIT license](references/license.md). The idea of a writing skill that removes formulaic AI patterns was inspired by [mchardyan/anti-ai-writer](https://github.com/mchardyan/anti-ai-writer) (inspected at main `bdbcad4` and references `3a86ca0`). That repository publishes no license, so none of its text, word lists or examples are reused here, and no endorsement is implied.
