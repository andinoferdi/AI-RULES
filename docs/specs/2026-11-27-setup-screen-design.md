# Setup screen design

Status: approved by the owner on 2026-11-27 ("Setuju, lanjut"). Date: 2026-11-27.

## Intent

The owner finds `andino setup` solid but not nice to look at, and the dense text makes them not
want to read it ("tulisan yang ribet ngeruwel ngeruwel itu sumpah bikin saya males baca ...
pokonya saya mau waow enak dilihat").

- Outcome: in a terminal, `andino setup` looks alive and reads at a glance; what setup installs
  does not change.
- User: the owner, who runs setup after every skill change, and everyone who installs Andino
  Skills.
- Why now: the owner ran setup on five agents and found the screen cluttered (screenshots,
  2026-11-27).
- Success: the default screen holds only the folded answers, a one-line plan, the y/N question
  and the result with the next step; motion comes in three moments (the mark builds, a bar per
  agent fills, the check lands); the owner calls it "waow".
- Constraint: the brand guide (Kunyit only for done or verified marks, no gradients or sparkle);
  no new dependency; plain output for logs and scripts; Python 3.11+; Windows, macOS and Linux;
  lines fit 60, 80 and 120 columns; merged by PR with green CI.
- Out of scope: what setup resolves, installs or verifies; the output of `doctor`, `add`,
  `remove`, `snapshot` and `restore`; Indonesian UI text; effects libraries; replacing
  questionary; the A in Kertas being hard to see on light terminal themes (as today).
- Anti-goal: setup feels slower (an intro over 0.6 s), the screen hides something needed to answer
  y/N safely (blocked items, conflicts, replaced files), logs or scripts break, or the screen
  claims more than setup checked.

## Scope

- Goals: G1 brand motion in three moments; G2 a short default screen; G3 the details on
  `--verbose`; G4 a timer that counts only work time.
- Out of scope and anti-goals: as in Intent.

## Constraints

- Brand guide [docs/brand/README.md](../brand/README.md): Kunyit is the only accent, kept for the
  check and for done or verified marks; no gradients, shadows or sparkle; the mark is recoloured
  only within the palette.
- Installed versions, checked locally on 2026-11-27: rich 14.3.4 (`>=13.9,<15`: `Live` with
  `get_renderable` and `transient`, cursor-up and erase-in-line controls) and questionary 2.1.1
  (`>=2.1,<3`: `qmark`, `pointer`, `style` and `instruction` on select and checkbox; `qmark`,
  `style` and `instruction` on confirm).
- Tests that read plain output keep passing: `test_terminal_ux.py`, `test_local_source.py`,
  `test_agent_defaults.py`, `test_execution_state_cli.py`, `test_live_updates.py`. No `%` in
  progress output (existing tests assert it).
- The README tells users to look for a `Skill source:` line.

## Approaches considered

1. Chosen: rich and a restyled questionary, both already installed, with one new presenter
   module. No new dependency.
2. terminaltexteffects 0.15.0 for the intro and outro. On Windows its maintainer recommends only
   Windows Terminal for animation (VS Code's terminal is untested), its effects are built on
   gradients, and it adds a dependency to the release binary. Kept only as a fallback if the owner
   later wants a louder style.
3. python-clack for clack-style prompts. Needs Python 3.12 (this project supports 3.11) and had no
   release after January 2026. Ruled out.

## Design

### Two modes

- Screen mode: stdout is a terminal that supports cursor movement (not a legacy Windows
  console), and the run has no `--non-interactive`, no `--no-progress`, no `CI`, and `TERM` is
  not `dumb` or `unknown`. It gets everything below. `andino add` runs setup's code, so it gets
  the same screen.
- Plain mode: every other run. It prints exactly today's text (plus the timer fix), so CI logs,
  scripts and the existing tests stay stable.
- `NO_COLOR` keeps screen mode and its motion without colour codes; the check then appears instead
  of lighting up. A terminal that cannot encode the block glyphs gets the static ASCII banner and
  no cell animation.

### The screen

Everything profile, five agents, nothing blocked:

```
   ▄██▄     Andino Skills v0.1.0
  ▄█  ▀▄    andino setup
 ▄██ ▄▀█▄   AI tools: Codex · Claude Code · OpenCode · Antigravity CLI
▄█▀ ▀  ▀█▄  ~\Downloads\andino-skills

◇ Agents    Codex, Claude Code, OpenCode +2
◇ Profile   Everything
◇ Defaults  English
  Skill source: local folder ~\Downloads\andino-skills\skills

◆ Plan      5 to update · 35 current
  Instruction files  4 current
◇ Apply     yes

  Codex             ━━━━━━━━━━━━━━━━━━  8/8  ✓      live area, removed when work ends
  Claude Code       ━━━━━━━━━━━━──────  5/8
  OpenCode          ──────────────────  0/8
  ...
⠹ Updating Claude Code · council · 6.2s

   ▄██▄     ✓ Done in 18.6s
  ▄█  ▀▄    5 updated · 35 already current
 ▄██ ▄▀█▄   Next: open a new agent session
▄█▀ ▀  ▀█▄  Try: /andino-workflow /focus /search-first +5 more (Codex uses $)
  Files verified · skill loading is not checked by setup
```

### Behaviour by moment

1. Intro: the A cells appear bottom-up within 0.6 s; the four info lines are today's. The check
   cells stay unlit (dim gray; absent under `NO_COLOR`). The last frame stays on screen. Ctrl+C
   restores the cursor and exits as today.
2. Questions: questionary with a brand style: `◆` before the active question, `›` as pointer,
   bold for the highlighted choice, gray for hints, no orange. After each answer its line is
   rewritten in place as `◇ <Label>  <value>` (Agents, Profile, Skills, Defaults, Apply). A long
   agent list ends in `+N` to fit the width. If the rewrite fails, questionary's own line stays.
   The agents question keeps the word "agent" (a test tells the prompts apart by it). When flags
   replace the questions, the same `◇` lines are printed from the flags.
3. Checking sources: one transient line with a spinner, the current phase and the work time.
4. Plan: one line of the non-zero counts in a fixed order (to install, to update, to repair, to
   reconfigure, to adopt, to replace, to downgrade, current, manual, blocked), wrapped to the
   width; an empty plan reads `nothing to do`. Below it, only when they apply: the instruction-file summary (`4 current`, or
   each conflict or failure with its short path), one line per blocked or manual target with its
   reason or step, and `Backups are kept for files that get replaced` when the plan may replace
   files. A dry run ends here with `Dry run · nothing changed`.
5. Apply: a live area with one bar per agent (filled cells in the terminal's text colour, empty
   cells gray, `done/total`, an orange `✓` once all of that agent's targets finished as applied
   or current, `✗` when one failed) and a status line (spinner, the agent and skill being worked
   on, work time; between two targets it keeps naming the last one). Under 60 columns the bar
   is dropped and the count stays. Diagnostics print above the live area as they happen. The
   area is removed when work ends.
6. Outro: the mark again with the result beside it.
   - Verified run: the check cells light up in Kunyit Terang one by one in stroke order (within
     0.5 s), then `✓ Done in <work time>`, the counts, `Next: open a new agent session`, and one
     line of first-party commands: with `$` when Codex is the only agent, otherwise with `/` and
     the note that Codex uses `$`. Nothing to change: `✓ Up to date in <work time>`.
   - Flags without `--yes` (setup asks nothing and applies nothing): `Preview only · nothing
     changed` and `Next: add --yes to apply`.
   - Failure, block, manual step or cancel: the check stays unlit; the first line says what
     happened (`✗ 1 failed · 4 updated · 35 current`, `✗ Cancelled after 4.2s · 12 of 40 done`);
     every failed, blocked or manual target follows with its message, wrapped, never cut.
   - Below the result: `Files verified · skill loading is not checked by setup` after a verified
     run, and `Backups: ~\.ai-rules\backups` only when this run replaced files.
7. `--verbose` in screen mode adds today's detail blocks: after the plan (per-host table,
   operations, preflight line, agent-defaults lines) and after the outro (per-target results,
   installation records and backups paths, per-agent command lists).
8. `andino update` and `andino repair` show the same one-line plan in screen mode; their other
   lines stay as they are.
9. The timer, in both modes, counts only time spent inside `with progress:` blocks, so reading
   the plan and answering y/N no longer count (the 257.7 s in the owner's screenshot included it).

### Where it lives

- New `src/ai_rules/screen.py`: mode detection, symbols with ASCII fallbacks, colours, the mark
  frames (lit and unlit check), intro and outro animation, the plan line, the answered-line
  rewrite and the questionary style.
- `banner.py`: the mark gains an unlit-check variant; `print_setup_banner` plays the intro in
  screen mode.
- `interactive.py`: prompts take the style and hand back what the `◇` lines show.
- `progress.py`: the screen-mode render (bars, status line, outro) beside today's plain render;
  the work-time timer.
- `planning/renderer.py`: the one-line plan next to today's renderer.
- `cli.py`: picks the mode once and routes output; `--verbose` extras; update and repair.
- Decoration never stops setup: an exception while drawing in screen mode switches the rest of
  the run to plain text.

## Decisions

- Confirmed by the owner on 2026-11-27 ("Ya, pakai dua-duanya"):
  1. On-brand motion as in the sketch: orange only for done marks, no gradients or confetti.
  2. The short default screen above, with the details on `--verbose`.
  Also accepted without objection in the same exchange: the intro at most 1 s, the timer counting
  work only, the plain fallbacks kept, English text, update and repair getting the new plan.
- My calls:
  - Correction: detecting the AI tools takes about 0.09 s (measured), so the intro cannot hide
    behind it as first said; it adds about half a second before the first question. Capped at
    0.6 s.
  - Plain mode keeps today's text: logs, scripts and tests stay stable, and the complaint was
    about the screen people look at.
  - The check is unlit in the intro and lights up only after a verified run, which is the brand's
    own idea that the A is complete once the check is in place. Abu is in the palette.
  - Text uses the terminal's own colour; hints use dim or bright-black gray, so both read on light
    and dark themes.
  - Failed, blocked and manual items always show with their message: they decide what the owner
    does next.
  - `Skill source:` keeps its wording because the README points to it; paths shorten with `~`.
  - The banner keeps its four info lines; they sit beside the four-row mark.
  - After approval: `Screen mode` and `Plain mode` go into `CONTEXT.md`, and the decision into
    `docs/DECISIONS.md`.
  - Made while building (recorded in the implementation plan): the plan word `manual`; a legacy
    Windows console gets plain mode; `$` alone when Codex is the only agent; `andino add` shows
    the same screen; flags without `--yes` end in `Preview only`; an instruction-file conflict is
    a manual item.
- Open: none.

## Acceptance checks

1. Unit, screen mode forced at widths 60, 80 and 120: the recorded output has the `◇` answer
   lines and a one-line plan, no line is wider than the terminal, there is no `%`, and every path
   is shown through the home-folder shortening (`~` for paths under the home folder).
2. Unit: the Kunyit colour (`245;165;36`) appears only in lit check cells and `✓` marks, and
   never in a failed run.
3. Unit: a failing target leaves the check unlit, prints `✗ 1 failed`, and shows the failure
   message.
4. Unit: `NO_COLOR` keeps screen mode with no colour codes; redirected output, `CI`,
   `TERM=dumb`, `--no-progress` and `--non-interactive` give today's plain text.
5. Unit: the intro finishes within 0.6 s and the outro within 0.5 s.
6. Unit: time spent outside `with progress:` (a simulated prompt wait) is not in the reported
   time.
7. `python scripts/ci_checks.py --group installer` passes, with only the intended test edits.
8. Real terminal: `python -m ai_rules setup` from the clone shows the screen above in the app's
   terminal; the owner checks the motion and colours in their own terminal.

## Left to the builder

Exact frame timings within the caps, the ASCII fallback glyphs, the wording of hints and labels
within the patterns above, how `screen.py` splits into functions, and the test file layout.

## Terms

- Screen mode and plain mode: the two presentations above. Code: `screen.py`, `SetupProgress`.
- Intro and outro: the mark animation at the start and the result block at the end.
- The check: the Kunyit check mark inside the A ([brand guide](../brand/README.md)).
