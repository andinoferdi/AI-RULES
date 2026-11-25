# Adapted sources

The 2026-11-25 upgrade of AI Codebase Rescue adapts techniques from two MIT-licensed
skill collections. The text is rewritten for this skill's contracts; no source file is
copied, and the sources are not runtime dependencies or endorsements.

| Source | Audited commit | Adapted into | Notice |
| --- | --- | --- | --- |
| [Rune](https://github.com/Rune-kit/rune) `skills/rescue`, `autopsy`, `safeguard`, `surgeon`, `hallucination-guard`, `logic-guardian` | 66ab37db7ad5c9ed4ad57da037555b7f3e3e9ec8 | Git churn hotspot commands, hotspot x complexity ranking, migration patterns (Strangler Fig, Branch by Abstraction, Expand-Migrate-Contract, Extract and Simplify), blast-radius check, test after every edit, phantom import and package checks, deleted-logic checks, Done when and sharp-edges table shape | [MIT, Rune Contributors 2026](rune-license.md) |
| [Wondel.ai skills](https://github.com/wondelai/skills) `working-with-legacy-code`, `refactoring-patterns`, `remove-technical-debt`, `improve-code-quality` | c37678106e63ef1c5472d848fb3d8b8c5b33fafe | Legacy change sequence, characterization recipe, known-bug pinning, golden masters, seams and dependency-breaking moves, sprout and wrap, effect sketches and pinch points, structure-only versus behavior-only steps, revert on red, smell-to-move mapping, starting-module heuristic | [MIT, Wondel.ai sp. z o.o. 2025](wondelai-license.md) |

Not adopted: 0-100 health scores and weighted dimensions, automatic `git add -A`,
commits and tags, `@legacy` source markers, config freeze copies, `RESCUE-STATE.md` and
other state or docs files written into the target project, fixed limits such as five
files or one module per session (kept as signals), and multi-phase book journeys. These
conflict with this skill's evidence rules, its single lifecycle owner and the user's
commit authority.

Updates are manual: compare the source bytes and notices at a new commit, review each
changed technique against the references above, then run the skill checks.
