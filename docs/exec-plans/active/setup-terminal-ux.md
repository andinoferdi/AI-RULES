# Setup terminal UX

Status: DONE | Depth: STANDARD | Host: Codex | Branch: main

## Executive Snapshot
Setup now reports real work through optional console-independent events and Rich
Live. The plan groups actions by host; verbose output retains diagnostics. Final
counts distinguish all target outcomes and account for final verification failures.
Full suite: 240 run, 239 passed, one opt-in skip; focused UX: 17 passed. Final frozen
Windows executable passed disposable dry-run/install/current smoke tests.

## Objective
Observable real work, compact per-host plan, truthful execution outcomes and safe
terminal lifecycle without changing reconciliation or installation semantics.

## Acceptance Criteria
Events precede blocking work; indeterminate phases stay alive; target denominator
comes from resolved plan and includes registration operations within each target.
Failures, current, blocked, skipped and cancellation stay distinct. Plain non-TTY,
60/80/120-column output, verbose details, dry-run safety and existing regressions.
No global installation, commits, pushes, branches or manifest/runtime changes.

## Execution Board
1. Audit: DONE. Inspected CLI, selections, renderer, latest resolver, executor,
   atomic copy, banner, dependencies and installer tests.
2. Implement and regress: DONE. Console-independent events, Rich presenter,
   per-host plan, verbose/plain flags, cancellation cleanup and final accounting.
   Focused UX tests pass, including real Questionary pipe-input interaction.
3. Verify/document: DONE. README and 60/80/120-column examples written.
   Final full run: 240 tests, 239 passed and one opt-in skip; earlier installer:
   134 run, one skip. Expanded UX suite: 17 passed after final width refinement.
   Final frozen build and dry-run/install/repeat smoke tests passed. Compileall,
   whitespace checks and main branch check passed. No commits/pushes/global skills.

## Decisions / evidence
- Keep Questionary and banner. Rich owns refresh threading and width handling.
- Count targets after every operation finishes; never equate processed with success.
- Preserve default scope, fetching, backups, fingerprint checks and update order.
- Use bundled debugging and TDD methods under Andino; Search First for Rich API.
- Rich official docs via Context7 /textualize/rich: Live auto-refresh, context
  cleanup, indeterminate progress, terminal and NO_COLOR behavior. Adopt Rich
  >=13.9,<15; exercised 14.3.4. Questionary retained. Standard PyInstaller rich
  hook collects the dependency; no release-manifest or bundled-skill changes.
- Event observer exceptions cannot change installation results. Target completion
  waits for every associated operation; post-lock verification corrects counts.
- Extend the existing rollback exception boundary to KeyboardInterrupt/SystemExit;
  restore the prior tree and re-raise interruption, retaining normal error behavior.
- NO_COLOR with an empty value needs explicit color disabling (regression caught).
- Mutation check: suppressing the pre-fetch event fails the local-remote test.
- Final frozen executable: dry-run exit 0/no writes; disposable project installs
  three targets; repeat reports three current; redirected output has no ANSI.
- Manual PTY attempt: NOT VERIFIED, Questionary says no Windows console found.
  Real Questionary keyboard selection/confirmation works with pipe input/DummyOutput.

## NEXT ACTION
None; task complete. Manual native terminal checks remain NOT VERIFIED as recorded
in `docs/validation/setup-terminal-ux/report.md`; no available console supports them.
