# Comparison rubric: optimize-prompt

Frozen on 2026-11-26 before any change to the candidate skill. Six arms run the same prompt on the
same fixture:

- the current `andino-optimize-prompt` (AI-RULES main at 1e78323);
- ECC `prompt-optimizer` (affaan-m/ECC, `skills/prompt-optimizer/SKILL.md`);
- GitHub awesome-copilot `prompt-optimizer` (github/awesome-copilot, `skills/prompt-optimizer/SKILL.md`);
- Sentry `prompt-optimizer` (getsentry/skills, `skills/prompt-optimizer/` with its references);
- Hashaam101 `prompt-optimizer` (`SKILL.md`);
- the candidate rewrite.

cnyet `prompt-optimization-skill` is not an arm: its `SKILL.md` is an index of rule files that
points to `USAGE.md`, with no procedure or reply format to run against a raw prompt.

A grader who sees only this rubric, the fixture and the six anonymised outputs (labelled A to F)
scores every criterion.

## Fixture

- `fixture/repo/`: a small Next.js 15 shop, "Toko Kopi". `package.json` scripts `dev`, `build` and
  `test` (`vitest run`); `AGENTS.md` says money is integer rupiah and to run `npm test` before
  finishing. `src/lib/cart.ts::cartTotal` applies the discount to the first unit only, so two items
  at 50000 with 10% give 95000 instead of 90000 (the bug p1 reports). `src/lib/cart.test.ts` has
  one test without a discount. `src/lib/orders.ts::listOrders` and `src/app/admin/orders/page.tsx`
  exist (p3). `src/app/checkout/page.tsx` exists (p4).
- `fixture/host/CLAUDE.md`: stands in for the host's `~/.claude/CLAUDE.md`. Its
  `ai-rules:global-defaults` block lists the installed skills and MCP servers. `skill-x-pro` is not
  installed. `playwright` is described as UI verification at 360, 768 and 1440 px.
- `fixture/prompts/p1.md` to `p6.md`: six user messages, each asking to optimize a raw prompt.
  - p1: bug report in Indonesian with numbers and a path.
  - p2: one weak line in Indonesian.
  - p3: English prompt in the template labels (`Skills`, `Tools/MCP`, `Mode: plan only`, `Task`), no
    done-when.
  - p4: long Indonesian story with three skills (one not installed), an MCP, a phase sequence, two
    URLs, a Windows path and "tanpa regresi performa".
  - p5: English research question (auth library, magic links, must stay on Next.js).
  - p6: Indonesian refactor naming `ponytail` while asking for every change explained in detail,
    "tanpa ubah perilaku".

## Run setup

Each arm gets its own run folder with copies of `fixture/repo/`, `fixture/host/` and
`fixture/prompts/` at `<RUN_DIR>/repo/`, `<RUN_DIR>/host/` and `<RUN_DIR>/prompts/`, and its own
copy of the skill folder at `<SKILL_DIR>`. One runner per arm: Claude Code subagent, Sonnet 5.5,
effort medium. Runners use no other skill, slash command or subagent and read nothing outside
`<SKILL_DIR>` and `<RUN_DIR>`.

Run prompt, identical for every arm (`<SKILL_DIR>` and `<RUN_DIR>` substituted):

> Read `<SKILL_DIR>/SKILL.md` first and follow it, opening any file it points you to when its
> condition applies. You are a coding agent in Claude Code. The project you are working in is
> `<RUN_DIR>/repo/`, which you may read but not change. The host instruction file is
> `<RUN_DIR>/host/CLAUDE.md`; treat it as `~/.claude/CLAUDE.md`, and treat the host's skill folder
> and MCP config as unavailable. `<RUN_DIR>/prompts/` holds six user messages, `p1.md` to `p6.md`.
> Process them in order, each as its own conversation, and open each only when you start it. Nobody
> can answer questions during this run. For each, write the exact reply you would send that user to
> `<RUN_DIR>/out/<id>.md` (for example `out/p1.md`). Do not mention which guidance you used. Use no
> skills, slash commands or subagents, and touch nothing outside `<RUN_DIR>/out/`.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote). Score what the reply
says. "The prompt" means the rewritten prompt the reply hands back; notes, tables and questions
around it are "the reply". Check claimed repository facts against `fixture/repo/` and claimed host
facts against `fixture/host/CLAUDE.md`. A criterion listing several prompts scores the weakest of
them.

### Keeping what the user wrote

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| K1 | Named choices kept (p3, p4, p6) | Every skill, MCP, mode and phase the user named appears in the prompt verbatim and in the user's order, including `skill-x-pro`, `Mode: plan only` and the sequence tanya dulu, council, andino-planning, andino-plan-execution | One choice renamed, merged or moved | A named choice dropped, or a phase sequence collapsed |
| K2 | Facts kept (p1, p4) | 10%, 2, @50000, 90000, 95000, `src/lib/cart.ts`, both URLs and `C:\work\shop\new` appear unchanged in the prompt | One fact altered or missing | Two or more |
| K3 | Nothing invented in the prompt (all) | The prompt gains no skill, MCP, library, framework, cause, page, device or requirement the user, the repository or the host file did not give; a suggestion stays outside the prompt | One invented item in one prompt | Invented items in two or more prompts, or a guessed root cause or library choice |
| K4 | User's language, labels and shape (p3, p4) | p3 keeps its four labels and English; p4 stays Indonesian with the user's `skill:` and `mcp:` lines; neither is converted to a different fixed template | Language and labels kept but the overall shape replaced by a different template | Language changed or labels renamed |

### Making the prompt actionable

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| A1 | Checked project facts (p1, p6) | The prompt uses at least two true repository facts relevant to the task (for example `npm test` / Vitest, `cartTotal`, `src/lib/cart.test.ts`, integer rupiah), marked as coming from the project, and states no false fact | One true relevant fact, or facts not marked as checked | No repository facts, or a false one |
| A2 | Observable done-when (p1, p3) | p1: a check a builder can run, using the user's numbers (2 × 50000 with 10% gives 90000); p3: a done-when built only from the user's request (the admin orders page offers a CSV export of orders) | Done-when present but vague, or present in only one | None, or built from invented requirements |
| A3 | Scope and constraints from the user's words (p4, p6) | p4 states "alur tetap sama", "tidak ada field baru" and "tanpa regresi performa" as constraints; p6 states "tanpa ubah perilaku" as a constraint; nothing the user did not say is added as a constraint | Constraints kept in the story but not made explicit, or one missing | Missing, or invented constraints |
| A4 | Fitting verification step (p1, p6) | p1: reproduce with a failing test for the user's case, fix, then run `npm test`; p6: run the tests before and after to show behaviour is unchanged | A generic "run the tests" without the reproduce or before/after step | None |
| A5 | Proportional structure (p2, p4) | p2 is not inflated into a long spec built from guesses; p4 is split into short readable parts following the user's own points and order | One of the two | Neither |

### Gaps, diagnosis and delivery

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Weak prompt questions (p2) | At most three targeted questions about facts only the user knows (which site or page, what is wrong now, what "lebih bagus" means or what done looks like), with no guessed framework, page or style inside the prompt | Questions present but more than three, generic, or partly answered by the repository | No questions, or the gap filled with guesses |
| Q2 | No placeholders (all) | No `[...]`, `{...}`, `<your ...>` or `___` slot for the user to fill in any prompt | One placeholder | Two or more |
| D1 | Diagnosis (all) | Each reply says briefly what was changed or added and why, separating additions from the user's own text | Says what changed without the why, or only for some prompts | No explanation, or a long essay |
| D2 | Inventory and conflict (p4, p6) | p4 says `skill-x-pro` is not installed on this host and keeps it in the prompt; p6 names the tension between `ponytail` (least code) and "sedetail mungkin" and keeps both for the user to settle | One of the two | Neither, or a choice dropped to resolve it |
| D3 | Suggestions outside the prompt (p5) | Any suggested skill or MCP (for example `search-first`, `context7`) is offered outside the prompt, and the prompt keeps magic links and Next.js as given | A suggestion inserted into the prompt | The research answered instead of the prompt optimized |
| D4 | Does not run the task (all) | No reply carries out the task (no code fix, no library recommendation as the answer, no design); each offers to run the prompt or hand it back | One reply starts the task | Two or more |
| L1 | Proportionate reply (all) | Replies are as long as the prompt needs: short for p2, readable for p4; no repeated copies of the prompt or long rationale tables for small prompts | One overlong or padded reply | Several |

## Totals and gate

Sixteen criteria, maximum 32. The candidate passes when its total is at least every other arm's total and each K
criterion scores at least as high as the current skill's.
