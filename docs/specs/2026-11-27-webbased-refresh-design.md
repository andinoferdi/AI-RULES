# WebBased refresh design

Status: approved by the owner on 2026-11-27 ("Ya, lanjut council"). After the Council review the
owner kept approach 1 with the Council's additions ("Ya, tetap Opsi 1"). Date: 2026-11-27.

## Intent

The `WebBased` branch started as this repository's main branch: copy-paste rules for web
chatbots, lettered A to Z, with A. PRIORITAS sent first in every chat to set the language. Coding
agents and then skills came later, and `main` (andino-skills) now covers the engineering side and
several of the daily roles. The owner still uses `WebBased`, but its README has grown to 19,036
lines (about 424 KB), which they describe as "banyak banget dan bertele tele dan bikin ai chatbot
makin pusing sendiri mahami nya". They want it to keep only what a daily prompt needs ("yang perlu
perlu aja buat daily prompt la ya bukan engineering"), aligned with andino-skills.

- Outcome: `WebBased` becomes a short set of daily, non-engineering rules for web chatbots:
  A. PRIORITAS, set once, and seven modules (D, E, G, H, R, S, U) that can be uploaded as skills
  or pasted into a chat.
- User: the owner, in Claude.ai, ChatGPT and Gemini, and anyone who copies the modules.
- Why now: andino-skills already covers what the dropped modules and files did, and web chatbots
  can now upload skills: Claude.ai on every plan, Free included, and Gemini on personal Google
  accounts (help centers read on 2026-11-27, sources at the end).
- Success: a chatbot follows a module on first use without extra explanation; the README fits on
  a few screens; A fits in 5,000 characters; no module loses a mode or an output it had; `main`
  CI stays green before, between and after the two PRs.
- Constraint: one A text shared by `WebBased` and Focus and enforced by `main` CI; `main` changes
  only by PR with green CI; commits, pushes and PRs need the owner's approval; prose follows
  natural-writing; modules use a skill format all three chatbots accept.
- Out of scope: new modules; engineering content in `WebBased`; testing inside the real chatbot
  apps; release archives or zip files; renaming the `WebBased` branch; changes to other andino
  skills beyond their mentions of A, the language references or `WebBased`.
- Anti-goal: A or a module silently loses a rule, mode or output the owner relies on; the README
  grows long again; `main` CI turns red; the text reads as machine-written; a daily module picks
  up engineering ceremony.

## Scope

- Goals:
  1. Delete the 17 retired modules (B, F, I, J, K, L, M, N, O, P, Q, T, V, W, X, Y, Z),
     `FOCUS-LICENSE.md`, the four prompt files at the branch root and everything under
     `put-in-your-projects/`.
  2. Rewrite A. PRIORITAS to at most 5,000 characters and use the same text in Focus.
  3. Rewrite D, E, G, H, R, S and U as one `SKILL.md` each, consistent in shape, keeping every
     mode and output.
  4. Replace the README with a short guide: how to use it, the A text, the module list and a
     migration table.
  5. Update `main` so its CI, Focus and documentation match the new `WebBased`.
- Out of scope and anti-goals: as listed under Intent.

## Constraints

- `focus_reference_drift` in `scripts/validate_skills.py` compares Focus's
  `references/priority-a.md` with the A text in `WebBased` at the commit pinned in
  `src/ai_rules/release/data/release_manifest.json` (today `76f9af1`). It also reads
  `put-in-your-projects/chat-rules.md` and the two `human-language-*.md` files. CI fetches
  `origin WebBased` before the skill checks. The pin keeps a push to `WebBased` from turning
  `main` red ([ADR 0002](../adr/0002-skills-live-on-main.md)); that ADR stays accurate.
- Skill format: a folder holding `SKILL.md` with YAML frontmatter, under the same rules `main`'s
  validator applies to `skills/<id>`: `name` equals the folder name and has 1 to 64 lowercase
  letters, digits and hyphens; `description` has at most 1,024 characters. Claude.ai takes a ZIP
  of the folder; Gemini takes the file or the folder.
- Who can upload skills: Claude.ai on every plan, with code execution on; Gemini for personal
  Google accounts aged 18 or over, on the web, Mac and mobile apps; ChatGPT only on Business,
  Enterprise, Healthcare and Edu. Everyone else pastes the module.
- ChatGPT custom instructions hold 1,500 characters on Free and Go and 5,000 on Plus and above.
  Claude and Gemini also apply account-wide instructions to every chat, and Gemini lets every
  user add them; neither help page states a length limit.
- The owner's ChatGPT, Claude.ai and Gemini accounts are all on free plans. ChatGPT Free has
  Projects, whose Instructions field applies to every chat in the project and overrides custom
  instructions; OpenAI publishes no length limit for it.
- `AGENTS.md` tells agents to leave `WebBased` alone; this task changes it at the owner's
  request.

## Approaches considered

1. One folder per module, `skills/<name>/SKILL.md`, with a short README as the index. Each module
   has one source, laid out like `skills/<id>/` on `main`. Uploading means zipping one folder and
   pasting means copying one file. The cost: a reader opens one file per module.
2. One README holding every module as a block already in `SKILL.md` format. Everything stays on
   one page, but the README stays long and uploading means creating the file by hand first.
3. The README as the source, with a script that generates the folders and a CI check that keeps
   them in step. Both conveniences, at the price of a generator and a check to maintain for seven
   modules.

Chosen: approach 1 (the owner: "Pendekatan 1").

## Design

### `WebBased` after the change

```
WebBased
├── README.md
└── skills/
    ├── parafrase-multibahasa/SKILL.md    D
    ├── riset-jalur-pendakian/SKILL.md    E
    ├── kalori-komposisi-tubuh/SKILL.md   G
    ├── penjawab-ujian-tulis/SKILL.md     H
    ├── pengoptimal-prompt/SKILL.md       R
    ├── alur-cerita/SKILL.md              S
    └── pencari-penantang/SKILL.md        U
```

Everything else on the branch is deleted. The old tree stays reachable at commit
`76f9af105cc1a5bffda2ff0f9fdcd39b69c63845`, and the README links to it.

### README

Indonesian, at most 200 lines, in this order:

1. Two lines on what the branch is, and that coding agents use `main`.
2. How to use it, in three steps:
   - Set A once, free plans first: in Claude under Settings > Your Claude > Instructions; in
     Gemini under Settings > Personal Intelligence > Instructions for Gemini; in ChatGPT Free in
     the Instructions field of one project (for example "Harian"), then chat inside that project.
     On ChatGPT Plus and above, custom instructions (5,000 characters) also work. If a field
     rejects A, paste A at the start of the chat, as the owner does today.
   - Add a module when a task needs it: upload it as a skill where the chatbot allows that,
     otherwise paste its `SKILL.md` into the chat.
   - For a coding agent, use `main` and its "How to Prompt" section.
3. `## A. PRIORITAS` followed by one fence opened with ` ````text ` that holds the A text. The
   validator depends on this heading and this fence.
4. The module table: letter, name, folder link and when to use it.
5. Skills from `main` that can be uploaded the same way, `focus` and `natural-writing`, marked as
   not yet tested in web chatbots. A short note says that skills uploaded to Claude.ai also load
   in Claude Code for the same account, and that `syncClaudeAiSkills: false` in Claude Code's
   settings turns that off.
6. A link to Focus's two language references on `main`, for anyone who wants to attach them to a
   chatbot project.
7. The migration table below and the link to the old tree.

### A. PRIORITAS

- It keeps today's rule areas: the conditional rule about the language references; natural,
  plain, active language; the answer first; relevance; honest facts, with no invented sources
  and fact kept apart from estimate; adaptive forms of address; the patterns to avoid;
  formatting; disclaimers only when they matter; current information and supplied sources;
  ambiguity; adaptive output length; writing artifacts that keep their own length; and the
  human-style examples.
- Before rewriting, the builder lists every rule in today's A. Each rule maps to a place in the
  new text, or goes to the owner as a proposed drop before anything is cut.
- Duplicate rules merge and the examples shrink. The text stays in Indonesian, starts with the
  line `A. PRIORITAS` as it does today, and has at most 5,000 Unicode characters. No platform
  requires that cap for the owner's free accounts; it stays as the brevity target.
- `skills/focus/references/priority-a.md` holds the same text, equal after line-ending
  normalization.

### Modules

- One `SKILL.md` per module, in Indonesian, with frontmatter holding only `name` and
  `description`, and a title that keeps the letter ("D. Parafrase Multibahasa").
- Every module has the same parts in the same order. The exact headings are settled at writing
  time under andino-skill-maker and andino-agent-document-authoring.
- A module works on its own and follows A when A is present.
- Before rewriting a module, the builder lists its modes, outputs and hard rules from the old
  text, and the new text keeps every item. Repetition goes; behaviour stays. Anything that should
  still be dropped goes to the owner first.
- One file per module and no reference files, so pasting stays a single copy. A module that
  still runs past 500 lines is flagged to the owner.
- R produces task prompts in Layer 2's seven slots (Skills, Tools/MCP, Mode, Task,
  Context/evidence, Done when, Constraints) from `main`'s README, in line with
  `andino-optimize-prompt`.

### Migration table

Every old row links to its file at commit `76f9af1`, so nothing has to be dug out of Git history.

| Old | Now |
| --- | --- |
| B. Penasehat Kritis | `council` |
| F. Penjelas dari Nol, I. Pembelajaran ala Feynman, P. Guru Adaptif | `andino-learning-workspace` |
| L. Penulisan Skripsi D4 TI UNAIR | `skripsi-skill` |
| O. Asisten Desain Web Non-AI-Looking | `impeccable`, `design-taste-frontend` |
| V. Pembuat Grand-Plan Project | `andino-brainstorming`, `andino-planning` |
| W. Kolaborasi AI Web × Coding Agent | module R (a Layer 2 prompt), `andino-handoff` |
| X. Focus | `focus` |
| Y. Natural Writing | `natural-writing` |
| Z. Reset Konteks | a new session |
| J, K, M, N, Q, T | removed, no replacement |
| `prompt-awal.md` | Layer 1 in `main`'s README |
| `Prompt-task.md`, `2. Send-to-every-prompt.md` | Layer 2's seven slots; `Mode: brainstorm first` |
| `1. First-prompt.md`, `Agents.md`, `Project Markdown Alignment Prompt.md` | `andino-agent-document-authoring` |
| `Repository Commit Push Prompt.md`, `git-naming.md`, `git-workflow.md`, `git-branch-tips.md` | `andino-git-skills`; personal conventions go in the Layer 1 file |
| `be-rules.md`, `fe-rules.md`, `code-rules.md` | `andino-workflow` and its member skills |
| `chat-rules.md` | A. PRIORITAS in the README |
| `human-language-indonesia.md`, `human-language-english.md` | `skills/focus/references/` on `main` |
| `prd.md`, `srs.md`, `optional/brd-(optional).md` | `andino-brainstorming` (design document), `andino-planning` |
| `FOCUS-LICENSE.md` | `skills/focus/references/legal/` on `main` |

### `main` after the change

| File | Change |
| --- | --- |
| `scripts/validate_skills.py` | `focus_reference_drift` reads only `README.md` from `WebBased` and compares its A fence with `references/priority-a.md`; `main()` fetches only `README.md`; the PASS line names A only |
| `tests/test_validate_skills.py` | Fixtures without `put-in-your-projects/`; cases for a matching A, a changed A, a missing section, an unterminated fence and CRLF endings; written first and seen failing |
| `src/ai_rules/release/data/release_manifest.json` | The pin moves to the new `WebBased` commit |
| `skills/focus/references/priority-a.md` | The new A |
| `skills/focus/references/human-language-*.md` | Mentions of `chat-rules.md` point to A. PRIORITAS (`priority-a.md`); the examples stay unchanged |
| `skills/focus/SKILL.md` | The line that maps `chat-rules.md` to `priority-a.md` is updated or removed |
| `skills/focus/README.md` | The web chatbot link points to `andinoferdi/andino-skills/tree/WebBased` and mentions upload or paste |
| `evals/focus.json` | The `webbased` case no longer mentions X. Focus |
| `README.md` | "In web chatbots (no skills)" is rewritten for upload or paste with the remaining letters; the What's Inside row drops "47 ready-to-use prompt templates" |
| `AGENTS.md`, `CONTEXT.md`, `docs/ci-coverage.md`, `docs/agent-skill-family-standard.md` | Describe the A-only check and the language references living in Focus; `AGENTS.md` says to change `WebBased` only when a task targets it |
| `skills/andino-workflow/skills/optimize-prompt/references/license.md` | The WebBased link uses the andino-skills repository name; module R stays the source |
| `docs/DECISIONS.md` | One dated entry pointing to this design |
| `docs/validation/webbased-refresh/` | Module inventories, test scenarios and results |

This design and the decision entry land in the `main` PR.

### Order and failure

1. The old-vs-new A comparison (below) passes before either PR opens. PR 1 into `WebBased`
   carries the new tree. `WebBased` has no CI of its own.
2. After PR 1 merges, PR 2 into `main` carries every change in the table above, with the pin at
   PR 1's merge commit. CI runs the new validator against that commit.
3. Between the two merges, `main` still pins `76f9af1`, which stays reachable in `WebBased`
   history, so `main` CI stays green.
4. If PR 2 fails CI, the A in `WebBased` and the A in Focus differ until it is fixed; nothing else
   reads them. Either PR can be reverted.

Commits, pushes and both PRs wait for the owner's approval.

### Testing the modules

The plan fixes the details.

- Static checks: the frontmatter rules, the length of A, the README line count, link targets and
  the module inventories.
- A, by proxy: 5 to 10 representative prompts answered under the old A and under the new A by
  Claude subagents, compared rule by rule against the A inventory. A rule the new A loses goes
  back to the owner (raise the cap or split the texts) before any PR.
- Behaviour, by proxy: a subagent given only one module (plus A) answers one realistic request,
  judged against PASS and FAIL lines written before the run. One more subagent sees all seven
  descriptions and must pick the right module for seven prompts and none for two unrelated
  prompts. These runs use Claude models, not ChatGPT or Gemini, and the record says so. The
  subagent count, model and effort need the owner's approval first.

## Decisions

- Confirmed by the owner:
  - Delete modules B, F, I, J, K, L, M, N, O, P, Q, T, V, W, X, Y and Z, and `FOCUS-LICENSE.md`
    (first message).
  - A may change, provided Focus and the skills that depend on it change with it (first message).
  - Length is free as long as the chatbot understands; prose follows natural-writing, and the
    modules follow andino-skill-maker consistently (first message).
  - Modules D to U can be uploaded as skills and can still be pasted (decision 1, "Ya, setuju
    semua").
  - One A for `WebBased` and Focus, at most 5,000 characters, set once in custom instructions
    (decision 2).
  - Delete every engineering file, PRD, SRS and BRD included; the README gets a migration table,
    and the old content stays in Git history (decision 3).
  - Approach 1 ("Pendekatan 1").
  - All of the owner's chatbot accounts are free ("semua ai chatbot yang saya punya itu free");
    approach 1 stays, with A set in a project's instructions on ChatGPT Free ("Ya, tetap Opsi 1").
- Council verdict (5 advisors, 3 reviewers, 2026-11-27): keep approach 1 and add the A inventory,
  the old-vs-new A comparison before any PR, permalinks in the migration table and the Claude
  Code sync note. The Outsider preferred two A texts; the others held that two unchecked texts
  drift, and that ChatGPT Free can still take A by pasting or through a project.
- My calls, with reasons:
  - The module letters stay, so "module R" in `main` (optimize-prompt) and the owner's habits stay
    valid.
  - Folder names are Indonesian kebab-case without the letter, because the name appears in the
    chatbot's skill list.
  - The language references live only in Focus on `main`, and CI checks only A. The shared A is
    the text that matters; two 41 KB copies on different branches only invite drift.
  - `chat-rules.md` goes, so the README fence is the only A in `WebBased`.
  - The README and the modules stay in Indonesian, as today.
  - R emits Layer 2's seven slots, so a prompt written in a chatbot drops straight into the coding
    workflow.
  - `focus` and `natural-writing` are listed as uploadable and labelled untested in web chatbots.
  - The old tree is linked by its commit; no archive tag is pushed.
  - The modules get no new CI. Their checks run once in this task and are recorded in
    `docs/validation/webbased-refresh/`.
  - This design is in English like the other specs; the README and the modules are in Indonesian.
- Open: none.

## Acceptance checks

1. `git ls-tree -r --name-only <new WebBased head>` lists `README.md` and the seven
   `skills/<name>/SKILL.md` files, and nothing else.
2. The A text in the README fence has at most 5,000 characters and equals
   `skills/focus/references/priority-a.md` after line-ending normalization.
3. In each `SKILL.md`, `name` equals its folder and matches `^[a-z0-9]+(-[a-z0-9]+)*$` within 64
   characters, and `description` has 1 to 1,024 characters.
4. For each module, every item in its inventory (modes, outputs, hard rules) appears in the new
   text.
5. The README has at most 200 lines, and every relative link and every link into `main`
   resolves.
6. The new validator tests fail on the old `focus_reference_drift` and pass on the new one;
   `python scripts/validate_skills.py --webbased-ref <new pin>` prints PASS; `python
   scripts/ci_checks.py --group skills` passes.
7. No live text in `main` or `WebBased` still points to `put-in-your-projects/`,
   `chat-rules.md` or a deleted module, outside the migration table, `docs/validation/` and dated
   records.
8. Each module's proxy scenario meets its PASS lines and none of its FAIL lines; the description
   probe picks the right module for all seven prompts and none for the two unrelated ones.
9. The README, A and the modules pass a natural-writing review: `check.py scan` runs on each, and
   every hit is either fixed or kept for a stated reason.
10. Every rule in the A inventory maps to the new A or carries the owner's approval to drop it,
    and the old-vs-new A comparison shows no lost rule.
11. Every old row in the migration table links to its file at commit `76f9af1`, and each link
    resolves.

## Left to the builder

The headings inside the modules, the exact wording, the order of README sections, branch names,
how commits are split, the PASS and FAIL lines (written before the runs), and a last check of
each chatbot's menu wording against its help page.

## Terms

- Module (modul): one daily-use skill in `WebBased`, a folder holding one `SKILL.md`.
- A. PRIORITAS (A): the always-on wording rules shared by `WebBased` and Focus.
- Pin: the `WebBased` commit in `release_manifest.json` that CI checks Focus against.
- Layer 1 and Layer 2: the global defaults and the seven-slot task prompt in the "How to Prompt"
  section of `main`'s README.

Sources, read on 2026-11-27: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude),
[Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt),
[Create and manage skills for Gemini Apps](https://support.google.com/gemini/answer/17094296?hl=en&co=GENIE.Platform%3DDesktop),
[About the transition from Gems to skills](https://support.google.com/gemini/answer/18560919?hl=en),
[ChatGPT Custom Instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions),
[Understanding Claude's personalization features](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features),
[Manage what Gemini remembers about you and customize responses](https://support.google.com/gemini/answer/16598625?hl=en&co=GENIE.Platform%3DDesktop),
[Projects in ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt).
