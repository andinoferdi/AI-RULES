# Decisions

- 2026-11-29: The repository keeps only files that the skills, the installer, the checks or
  their users need ("saya mau branch main dan webbased bener bener clean"). Trial records, dated
  design specs and plans are removed from `main` and stay out: `.gitignore` closes
  `docs/specs/` and `docs/validation/`, and what remains tracked there is
  `docs/specs/changing-skills.md` plus the data the checks read. Skill provenance lines that
  name old records stay as written. `WebBased`'s README drops its table of the old version.
  The decisions, open questions and ADRs stay.

- 2026-11-27: `WebBased` holds only what a daily chat needs: A. PRIORITAS and seven modules,
  each a `skills/<name>/SKILL.md` that can be uploaded as a skill or pasted (D, E, G, H, R, S,
  U). Modules B, F, I to Q, T and V to Z, the root prompt files and `put-in-your-projects/`
  (engineering rules, PRD, SRS, BRD) are removed. A is rewritten to 4,827 characters so it fits a
  5,000-character instructions field and is set once per chatbot; module G's personal data
  becomes a fill-in template. The Focus check compares only the README's A with
  `priority-a.md`, and the language references live only in Focus. The pin moves to `84406ba`
  (PR 55). Council verdict: keep one folder per module and add the A inventory, the old-versus-new
  A comparison and the Claude Code sync note; the owner agreed ("Ya, tetap Opsi 1").

- 2026-11-27: `ai-rules setup` gets a screen mode for people at a terminal ("Ya, pakai
  dua-duanya"): the Checked A builds, answers fold into one line each, the plan is one line, a
  bar fills per agent, and the check lights up in Kunyit only after a verified run. Kunyit stays
  reserved for done marks; no gradients or confetti. Full paths, installation records and
  per-file lines move to `--verbose`; failed, blocked and manual items always show. Plain mode
  (CI, pipes, `--no-progress`, `--non-interactive`) keeps the old text. No new dependency:
  rich and questionary only; terminaltexteffects was set aside (its maintainer recommends only
  Windows Terminal for animation on Windows, and its effects are built on gradients).

- 2026-11-27: andino-workflow gets its own loop for multi-unit work
  (`skills/andino-workflow/references/orchestration.md`, with a short trigger in SKILL.md): a
  counted work list, results written to the checkpoint in batches, an attempt to clear each
  consequential finding (CONFIRMED / REFUTED / UNVERIFIED), a second sweep until a round adds
  nothing, and a coverage line with the stop reason, inline by default. Claude Code's Workflow
  tool may run approved units under the 3-agent limit; the ultracode keyword or mode is not
  approval. Council verdict: Option 2 plus targeted fixes.

- 2026-11-23: Monorepo. Every skill moves into `skills/<id>/` on `main`; skill
  pins, `promote_skill.py` and `skill_refs.py` are removed. `ai-rules setup` is
  the only install path (no `npx skills` option), installs the clone's `skills/`
  when run inside a clone and GitHub `main` otherwise. Old installs are
  recognized from setup's own records. `WebBased` stays a separate branch with
  one validation pin. Old skill branches are deleted only after the owner
  approves. Entries below dated 2026-11-22 describe the pinned layout and are
  superseded. See [ADR 0002](adr/0002-skills-live-on-main.md).

- 2026-11-22: Main's `release_manifest.json` is the only version anything reads.
  CI, the tests and `ai-rules setup --source latest` use the pinned skill commits;
  a skill branch head reaches users only after a promote PR passes CI and is
  merged. Promotion is started locally with `python scripts/promote_skill.py
  <skill>` under the owner's `gh` login. A ruleset on `main` requires a PR with
  green CI. `natural-writing` is the first real promotion; the other branches
  ahead of their pins follow so users are not downgraded. See
  [ADR 0001](adr/0001-main-pins-skill-versions.md).

- 2026-11-22: `threejs-skills` is pinned at `4fe9d9c` instead of `7ff3f57`, because
  `docs/threejs/inventory.json` (now `src/ai_rules/verification/data/threejs_inventory.json`) on main already describes `4fe9d9c` (README-only
  changes). Pinning the older commit made the inventory check fail.

- 2026-11-22: CI and the promote clone pin only `origin/<skill>`, as CI always had.
  Tests that read a local branch name keep skipping on runners; reviving them is
  tracked in [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
