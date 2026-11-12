---
name: andino-optimize-prompt
description: Use when the user explicitly asks to optimize, tidy or rewrite a raw task prompt for a coding agent, or invokes andino-optimize-prompt. Operates under Andino Workflow governance.
---

# Optimize a raw task prompt

Internal method ID: `andino-optimize-prompt` (alias: `optimize-prompt`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

## Purpose and selection

Make a raw task prompt easier for a coding agent to act on while it stays the user's prompt: their
shape, voice, language mix, order of thought and every choice they made. The smallest edit that
makes the prompt clear is the best result. Returning it almost unchanged is a valid result.

Activate for: an explicit request to optimize, tidy or rewrite a task prompt, including
`/andino-optimize-prompt` and `$andino-optimize-prompt`.

Do not activate for: an ordinary task prompt (do the task instead), polishing prose that is not a
task prompt (`natural-writing`), or a prompt for a web chatbot without skills (WebBased module R).

## Inputs

The raw prompt, the active host's Layer 1 block, and [prompt patterns](resources/prompt-patterns.md)
for the labels people use and the suggestion tables. Complete runs are in the
[worked example](resources/worked-example.md).

## Procedure

1. **Inventory the host.** Read the block between `<!-- ai-rules:global-defaults:start -->` and
   `<!-- ai-rules:global-defaults:end -->` in the active host's instruction file, opened with a file
   tool: a copy already loaded into context can lose these comment markers. Without the block, list
   the skill folder and the MCP config instead. Record which source you used. The inventory only
   checks what the user named and feeds suggestions; it never removes or adds anything in the prompt.

   | Host | Instruction file | Skill folder | MCP config |
   | --- | --- | --- | --- |
   | Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/skills` | `~/.claude.json` (`mcpServers`) |
   | Codex | `~/.codex/AGENTS.md` | `~/.agents/skills` | `~/.codex/config.toml` (`mcp_servers`) |
   | OpenCode | `~/.config/opencode/AGENTS.md` | `~/.config/opencode/skills` | `~/.config/opencode/opencode.json` (`mcp`) |
   | Antigravity CLI / IDE | `~/.gemini/AGENTS.md` | `~/.gemini/antigravity-cli/skills`, `~/.gemini/config/skills` | `~/.gemini/config/mcp_config.json` (`mcpServers`) |

2. **Pin the user's choices and facts.** Keep verbatim and in the user's order every skill,
   workflow member (`andino-*`, `andino-workflow`, `search-first`, `focus`), MCP server, mode and
   phase sequence the user wrote, such as "tanya dulu, lalu council, lalu andino-planning". Keep
   verbatim every error text, path, file name, version, URL, name, number, quoted title and count.
   The user chose these on purpose, so overlap with another skill or with the workflow's own phase
   routing is never a reason to drop, merge or reorder them. The prompt gains no skill, technology,
   cause, fix, requirement, device or check the user did not give.

3. **Edit lightly.** Allowed edits:
   - Keep the labels the user wrote (`skill:`, `mode:`, `mcp:`, `task:`, `Skills:`, Indonesian
     labels) with their spelling. If the user named skills inside a sentence, leave them there.
   - Fix typos in plain words when the meaning is certain. Never change identifiers, paths, names
     or quoted text.
   - Split a long paragraph into short paragraphs or bullets along the user's own points, in the
     same order.
   - Gather paths, URLs, references and target locations scattered through the story into a short
     list under the user's own wording (`referensi:`, `implementasikan di:`), keeping who likes what.
   - Remove exact repetition only.
   - When nothing in the prompt says how to tell the work is done, add one block in the user's
     language (`selesai jika:` or `done when:`) with checks taken only from what the user said.

   Not allowed: converting the prompt to a fixed template, renaming the user's labels, removing,
   merging or reordering a named skill or phase, collapsing a phase sequence into one mode, adding
   a skill or MCP server, adding placeholders, restating Layer 1 rules. A prompt that already uses
   the template labels (`Skills:`, `Mode:`, `Task:` and the rest) keeps them.

4. **Weak prompt.** When the prompt lacks a fact only the user knows and that fact changes the
   result (which project or page, what is wrong now, what done looks like), return the lightly
   edited prompt and at most three short questions about those facts. Do not fill the gap with a
   guess or a `[placeholder]`.

5. **Notes, suggestions only.** At most five lines, none applied to the prompt:
   - what changed, in one line;
   - a named skill or MCP server missing from the inventory (it stays in the prompt);
   - a conflict between two named choices and the goal, only when both sides can be named, for
     example `ponytail` for the least code while the result must be detailed. Overlap between
     workflow members is not a conflict;
   - optional additions from the suggestion tables, phrased as "you could add";
   - the inventory source and any added `done when` block.
   No note explains why a user choice is redundant or already covered.

6. **Return** in the user's language, in this order:
   1. the prompt in one `text` block;
   2. `Notes`;
   3. the questions, if any;
   4. one line offering to run the prompt in this session.

   Stop there. Run the prompt only after an explicit yes. It then becomes the task, and the
   workflow routes it like any other, honoring the choices it names.

## Ownership, precedence and permissions

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-optimize-prompt` and this guide expose one method, without recursive workflow invocation.

Reading the host's instruction file, skill folder and MCP config is read-only. The skill never
edits them, installs a capability or runs the task before the user says yes.

## Outputs and verification

Compare the output with the raw prompt: every pinned choice and fact appears unchanged and in the
user's order; no skill or MCP server was added to the prompt; the user's labels and overall shape
remain; every edit is on the allowed list; at most three questions; `Notes` has at most five lines
and no redundancy comment.

## Example and anti-patterns

Positive request: "Optimalkan prompt ini: bikin scene three.js pakai ponytail dan council."

Negative request: "Bikin scene three.js pakai ponytail dan council." (do the task)

Anti-patterns: dropping `andino-planning` because `mode: brainstorm-first` "already covers it";
rewriting a free-form prompt into seven slots; putting a suggested skill into the skill line;
copying checks from an example into `done when`; asking the user to fill placeholders for things
they never mentioned.

## Fallback

Without readable Layer 1, skill folder or MCP config, keep the prompt as edited, say in `Notes`
that the named capabilities could not be checked, and name nothing as installed.

## Provenance

Original Andino member. The fact-preservation and material-assumption rules adapt module R of the
WebBased branch of this repository ([references/license.md](references/license.md)).
