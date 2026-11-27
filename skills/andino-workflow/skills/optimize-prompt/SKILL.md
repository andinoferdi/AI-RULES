---
name: andino-optimize-prompt
description: Use when the user explicitly asks to optimize, tidy or rewrite a raw task prompt for a coding agent, or invokes andino-optimize-prompt. Operates under Andino Workflow governance.
---

# Optimize a raw task prompt

Internal method ID: `andino-optimize-prompt` (alias: `optimize-prompt`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Hand back the user's own prompt, made easy for a coding agent to act on: their shape, voice,
language mix, order of thought and every choice they made stay, and the prompt gains what an agent
needs to finish well and prove it: facts checked in the project, an observable end, the user's
limits stated plainly and a way to verify. Every addition is labelled and traceable to the user's
words, the project or the host. A prompt that already has all of this comes back almost unchanged.

## Trigger and non-trigger

Use when the user explicitly asks to optimize, tidy or rewrite a task prompt, including
`/andino-optimize-prompt` and `$andino-optimize-prompt`.

Do not select for:

- an ordinary task prompt: do the task instead;
- polishing prose that is not a task prompt: `natural-writing`;
- a prompt for a web chatbot without skills: WebBased module R.

## Select a resource, not a second lifecycle

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Which facts to check, what to ask and which verification step fits the task | [intent checklists](resources/intent-checklists.md) | Never: every run classifies the task |
| Labels people use, and the skill and MCP suggestion tables | [prompt patterns](resources/prompt-patterns.md) | No suggestion or label question arises |
| Two complete runs, a strong prompt and a weak one | [worked example](resources/worked-example.md) | The procedure is already clear |

## Prerequisites

The raw prompt, the active host's instruction file and read access to the working directory. Reading
is the only access this skill uses.

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
   cause, fix, requirement or device the user did not give.

3. **Classify the task** with the [intent checklists](resources/intent-checklists.md): bug, UI,
   feature, refactor, research, review, install or docs. The matching rows name the project facts to
   check, the facts to ask for and the verification step. Done when every task in the prompt has a
   row.

4. **Check the project.** When the prompt is about the working directory, read only what the rows
   name: `AGENTS.md` or `CLAUDE.md` in the project, the manifest (`package.json` scripts,
   `pyproject.toml`, `go.mod`, `Cargo.toml`), the files and functions the prompt names, their tests
   and their callers. Record each fact with the file it came from. Keep facts about where things
   are, which commands run them, what tests exist and which project rules apply; what the code does
   wrong is for the agent to find. When the prompt targets another project, or a read fails, record
   no facts and write "not checked" in the diagnosis. Done when every fact you will add has a
   source file you opened in this run.

5. **Edit.** The light edits:
   - Keep the labels the user wrote (`skill:`, `mode:`, `mcp:`, `task:`, `Skills:`, Indonesian
     labels) with their spelling. If the user named skills inside a sentence, leave them there.
   - Fix typos in plain words when the meaning is certain. Never change identifiers, paths, names
     or quoted text.
   - Split a long paragraph into short paragraphs or bullets along the user's own points, in the
     same order.
   - Gather paths, URLs, references and target locations scattered through the story into a short
     list under the user's own wording (`referensi:`, `implementasikan di:`), keeping who likes what.
   - Remove exact repetition only.

   Then add, after the user's text, only the blocks the prompt lacks, in the user's language, each
   from its one allowed source:

   | Block (Indonesian / English) | Source |
   | --- | --- |
   | `fakta proyek (dicek):` / `project facts (checked):` | Step 4, each fact naming its file |
   | `batasan:` / `constraints:` | Limits the user wrote ("tanpa ubah perilaku", "jangan ada field baru"), restated as lines |
   | `selesai jika:` / `done when:` | Observable checks built only from the user's own words and numbers |
   | `verifikasi:` / `verify:` | The checklist row's verification step, using the project's real commands and the host's tools, ending with "cocokkan hasil dengan `selesai jika` dan laporkan hasil cek yang sebenarnya" / "check the result against `done when` and report the real check output" |

   A prompt written in the template labels (`Skills:`, `Tools/MCP:`, `Mode:`, `Task:`,
   `Context/evidence:`, `Done when:`, `Constraints:`) keeps them: facts go under
   `Context/evidence:`, end checks and verification under `Done when:`, limits under
   `Constraints:`, one item per `- ` line. A block the user already wrote is extended, never
   duplicated. Done when every added line traces to the user's words, a checked file or the host
   block.

6. **Weak prompt.** When the prompt lacks a fact only the user knows and that fact changes the
   result (which project or page, what is wrong now, what done looks like), return the lightly
   edited prompt with no added blocks that would need that fact, and at most three short questions
   about those facts, each carrying your best guess from the project ("the Toko Kopi app in this
   folder?"). Never ask what the project already shows. Do not fill the gap with a guess or a
   `[placeholder]`.

7. **Diagnose.** One table, at most five rows, columns `Jenis | Isi` (English `Kind | Detail`).
   Row kinds, in this order, only when they apply: strength (what the prompt already does well);
   changed (the light edits); added (each block and its source); not installed, not checked or
   conflict (a named skill or MCP missing from the inventory, which stays in the prompt; facts you
   could not check; two named choices that pull against each other, such as `ponytail` for the
   least code while the result must be detailed, kept for the user to settle); could add (optional
   skills or MCP from the suggestion tables, phrased as "bisa ditambah" / "you could add"). Overlap
   between workflow members is not a conflict, and no row explains why a user choice is redundant.

8. **Return** in the user's language, in this order:
   1. the prompt in one `text` block;
   2. the diagnosis table;
   3. the questions, if any;
   4. one line offering to run the prompt in this session.

   Stop there. Run the prompt only after an explicit yes. It then becomes the task, and the
   workflow routes it like any other, honoring the choices it names.

## Rules for every prompt

- Added lines use imperative verbs and state one action or check each ("Tulis tes yang gagal untuk
  kasus 2 barang @50000 diskon 10%").
- Added text says what to do; a limit the user wrote is restated as they meant it.
- Size follows the prompt: a one-line task gains at most `selesai jika` and `verifikasi`; a long
  story gains structure along its own points.
- Every slot is filled with real content or left out: the user never receives a placeholder.
- One prompt per reply, with no second "short" version.

## Shortcuts that weaken a prompt

| Shortcut | Do instead |
| --- | --- |
| "The bug is obvious from the code, I'll name the cause." | Add where the code and its tests are; the agent proves the cause with a failing test. |
| "This feature obviously also needs security, pagination and logging." | Add only what the user wrote; offer the rest as a "could add" row. |
| "The template is clearer, I'll convert their story into seven labels." | Keep their shape; add blocks after their text. |
| "I'll ask which framework they use." | Read the manifest. Ask only what the project cannot show. |
| "A second, shorter version helps." | One prompt; the diagnosis carries the explanation. |
| "I'll settle the conflict between two named skills for them." | Name it in the diagnosis and keep both. |

## Red flags

- A named skill, MCP, mode or phase missing, renamed or moved in the output.
- A fact in `fakta proyek` without a file you read in this run.
- A root cause, library choice, page, device or requirement the user did not give, inside the
  prompt.
- A question the manifest or code already answers.
- More than five diagnosis rows, or more than three questions.
- The task carried out instead of the prompt handed back.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical checks.
Coordinator brevity never truncates these. User/project authority, Focus/research/domain
boundaries and real invocation controls still apply. Native `andino-optimize-prompt` and this guide
expose one method, without recursive workflow invocation.

Reading the host's instruction file, skill folder, MCP config and the project is read-only. The
skill never edits them, installs a capability or runs the task before the user says yes.

## Output

The reply from step 8: one prompt in a `text` block, a diagnosis table of at most five rows, up to
three questions and one offer to run it. Nothing else is produced.

## Verification

Compare the output with the raw prompt before sending:

- [ ] every pinned choice and fact appears unchanged and in the user's order;
- [ ] no skill or MCP server was added to the prompt; suggestions sit in the diagnosis;
- [ ] the user's labels and overall shape remain, and every edit is on the allowed list;
- [ ] every added block has its allowed source, and every project fact names a file read in this run;
- [ ] at most three questions, none answered by the project;
- [ ] the diagnosis has at most five rows and no redundancy comment.

## Worked example and anti-pattern

The [worked example](resources/worked-example.md) runs a strong prompt and a weak one end to end.

Positive request: "Optimalkan prompt ini: bikin scene three.js pakai ponytail dan council."
Negative request: "Bikin scene three.js pakai ponytail dan council." (do the task)

Anti-patterns: dropping `andino-planning` because `mode: brainstorm-first` "already covers it";
rewriting a free-form prompt into the template labels; putting a suggested skill into the skill
line; copying checks from an example into `selesai jika`; a "dugaan penyebab" line read off the
code; asking the user to fill placeholders for things they never mentioned.

## Fallback

Without a readable Layer 1 block, skill folder or MCP config, keep the prompt as edited, say in the
diagnosis that the named capabilities could not be checked, and name nothing as installed. Without
a readable project, add no `fakta proyek` block and use only the user's own words for the other
blocks.

## Local resources

- [Intent checklists](resources/intent-checklists.md)
- [Prompt patterns](resources/prompt-patterns.md)
- [Worked example](resources/worked-example.md)
- Notices: [references/license.md](references/license.md)

## Operational example (offline)

This fixture checks two properties of an output: pinned tokens keep their order, and added blocks
use only the allowed labels. It does not measure prompt quality.

```python andino-operational-example
import os
import re

ALLOWED = ('fakta proyek (dicek):', 'batasan:', 'selesai jika:', 'verifikasi:',
           'project facts (checked):', 'constraints:', 'done when:', 'verify:')

def problems(raw, output, pins):
    found = [output.find(pin) for pin in pins]
    issues = [pin for pin, at in zip(pins, found) if at < 0]
    if not issues and found != sorted(found):
        issues.append('order')
    added = output[len(raw):] if output.startswith(raw) else output
    for label in re.findall(r'(?m)^([a-z][a-z ()]*:)\s*$', added):
        if label not in ALLOWED:
            issues.append(label)
    return issues

if __name__ == '__main__':
    raw = 'skill: andino-workflow, council\ncek src/lib/cart.ts\n'
    good = raw + '\nselesai jika:\n- total 90000\n\nverifikasi:\n1. npm test\n'
    assert problems(raw, good, ['andino-workflow', 'council', 'src/lib/cart.ts']) == []
    bad = 'skill: council, andino-workflow\n\ndugaan penyebab:\n- diskon\n'
    assert problems(raw, bad, ['andino-workflow', 'council']) == ['order', 'dugaan penyebab:']
    raise SystemExit(1 if os.environ.get('ANDINO_NEGATIVE') == '1' else 0)
```

## Provenance

Original Andino member. The fact-preservation and material-assumption rules adapt module R of the
WebBased branch of this repository ([references/license.md](references/license.md)). The task
checklists, checked project facts, verification step and diagnosis table were added after a blind
comparison with the ECC, GitHub awesome-copilot, Sentry and Hashaam101 prompt optimizers, recorded in
`docs/validation/optimize-prompt/` of the AI-RULES repository; no text from those skills is copied.
