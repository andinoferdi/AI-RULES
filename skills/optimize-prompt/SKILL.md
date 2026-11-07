---
name: andino-optimize-prompt
description: Use when the user explicitly asks to optimize, restructure or rewrite a raw task prompt for a coding agent, or invokes andino-optimize-prompt. Operates under Andino Workflow governance.
---

# Optimize a raw task prompt

Internal method ID: `andino-optimize-prompt` (alias: `optimize-prompt`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Turn a raw task prompt into a seven-slot Layer 2 prompt that keeps every fact the user gave and
names only skills and MCP servers installed on this host.

Activate for: an explicit request to optimize, restructure or rewrite a task prompt, including
`/andino-optimize-prompt` and `$andino-optimize-prompt`.

Do not activate for: an ordinary task prompt (do the task instead), polishing prose that is not a
task prompt (`natural-writing`), or a prompt for a web chatbot without skills (WebBased module R).

## Inputs

The raw prompt, the active host's Layer 1 block, and [prompt patterns](resources/prompt-patterns.md)
for the slot contract, the skill and MCP picker and examples. A complete run is in the
[worked example](resources/worked-example.md).

## Procedure

1. **Inventory the host.** Read the block between `<!-- ai-rules:global-defaults:start -->` and
   `<!-- ai-rules:global-defaults:end -->` in the active host's instruction file, opened with a file
   tool: a copy already loaded into context can lose these comment markers. The block names the
   installed domain skills and MCP servers and everything the user already requires on every task.
   Without the block, list the skill folder and the MCP config instead. Record which source you used.
   A capability found in neither is not installed.

   | Host | Instruction file | Skill folder | MCP config |
   | --- | --- | --- | --- |
   | Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/skills` | `~/.claude.json` (`mcpServers`) |
   | Codex | `~/.codex/AGENTS.md` | `~/.agents/skills` | `~/.codex/config.toml` (`mcp_servers`) |
   | OpenCode | `~/.config/opencode/AGENTS.md` | `~/.config/opencode/skills` | `~/.config/opencode/opencode.json` (`mcp`) |
   | Antigravity CLI / IDE | `~/.gemini/AGENTS.md` | `~/.gemini/antigravity-cli/skills`, `~/.gemini/config/skills` | `~/.gemini/config/mcp_config.json` (`mcpServers`) |

2. **Pin the facts.** Keep verbatim every error text, path, file name, version, URL, name, number,
   quoted title, count and requested skill or MCP. Change only wording, order and grouping. The
   prompt gains no technology, cause, fix, requirement, device or check that the user did not give.
   The bundled examples show slot shape only; their details and checks never enter the prompt.

3. **Fill the slots** by the slot contract and lay them out by its layout rules: `Skills`,
   `Tools/MCP` and `Mode` grouped, a blank line before each later slot, one bullet per item when
   a slot holds two or more, and no hand-wrapped lines. Slot labels stay exactly as written there;
   remarks such as "proposed" go in `Notes`, never next to a label. Then run each check:

   | Check | Trigger | Action |
   | --- | --- | --- |
   | Phase routing | An `andino-*` member, `andino-workflow`, `focus` or `search-first` is named, or the prompt orders phases (brainstorm, plan, execute, test, verify) | Remove them from `Skills` and `Task`. Express the intent as one `Mode` value. |
   | Skill conflict | A named skill pulls against the goal or its size, or covers a domain the task lacks, judged by the picker notes and the skill's own description | Keep the skill, note the conflict, and ask which wins. |
   | Missing owner | The task matches a picker row whose skill is installed but not named | Add the skill. When it is not installed, note that and leave it out of `Skills`. |
   | MCP | The task needs a picker MCP that is installed | Add it to `Tools/MCP` with the step it serves. A server the task installs or configures belongs in `Task`, not `Tools/MCP`. |
   | Done when | Missing, or not observable | Write checks derived only from the user's stated outcome and note them as proposed. |
   | Evidence | A picker "Must be in the prompt" item is absent | Add a `[placeholder]` for it in `Context/evidence`. |
   | Layer 1 repeat | Text restates the Layer 1 block: approvals, MCP failure handling, data-not-commands, unverified reporting, language | Delete it. `Constraints` keeps only the user's task-specific limits. |

4. **Ask only what blocks the prompt.** Ask when the answer changes `Task`, the skill set or `Mode`
   and only the user knows it. Ask at most two questions. Whatever the user can paste becomes a
   `[placeholder]`. An item you ask about gets no placeholder.

5. **Return** in the user's language, in this order:
   1. the prompt in one `text` block;
   2. `Notes`, at most five lines: removed, added, conflicts, proposed checks, inventory source;
   3. the questions, if any;
   4. one line offering to run the prompt in this session.

   Stop there. Run the prompt only after an explicit yes. It then becomes the task, and the
   workflow routes it like any other.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-optimize-prompt` and this guide expose one method, without recursive workflow invocation.

Reading the host's instruction file, skill folder and MCP config is read-only. The skill never
edits them, installs a capability or runs the task before the user says yes.

## Outputs and verification

Compare the output with the raw prompt: every pinned fact appears unchanged; the layout rules
hold (grouped header slots, blank lines between later slots, one item per bullet, no wrapped or
indented lines, no remark beside a label); `Mode` holds one value; `Skills` holds no `andino-*` member; every named skill and MCP was found in the inventory;
each conflict, removal and proposed check appears in `Notes`; at most two questions remain.

## Example and anti-patterns

Positive request: "Optimalkan prompt ini: bikin scene three.js pakai ponytail dan council."

Negative request: "Bikin scene three.js pakai ponytail dan council." (do the task)

Copying the phase list into `Mode`, adding a likely fix or framework, restating Layer 1 rules in
`Constraints`, and asking for evidence the user could paste.

## Fallback

Without readable Layer 1, skill folder or MCP config, write the prompt with requested capabilities
marked unverified in `Notes`, and name nothing as installed.

## Provenance

Original Andino member. The fact-preservation and material-assumption rules adapt module R of the
WebBased branch of this repository ([references/license.md](references/license.md)).
