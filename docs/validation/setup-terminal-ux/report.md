# Setup terminal UX verification

Host: Windows 11, Python 3.12.10, Rich 14.3.4, Questionary 2.1.1.
Work performed on `main`; no commits, pushes or global skill installations.

## Implementation and observed work

`events.py` defines optional console-independent callbacks. Source resolution emits
events before fetching each repository and before exporting each bundle. Counts use
the actual repository groups, requested bundles and resolved reconciliation targets.
Installed-state inspection and plan/invocation checks emit before starting. Work
whose total is not known uses a status and elapsed time. No percentages or throughput
estimates are generated.

Execution counts resolved targets, including dependency targets. The existing
operation loop completes all operations for a target before emitting completion.
APPLIED, CURRENT, BLOCKED, FAILED, SKIPPED and MANUAL_ACTION_REQUIRED are distinct.
Final lock verification can remove a previously applied/current target from the
successful count. Filesystem stages emit before staging, backup, replacement,
verification and rollback. Git checkout updates emit their actual backup, fetch,
fast-forward and content checks; no unimplemented Git rollback is advertised.

Rich Live owns refresh and cursor cleanup. It runs only for interactive terminals;
plain output retains milestones and one result per target. Observer errors cannot
change installation/rollback outcomes. Existing normal exception/backup/fingerprint
behavior stays intact; interruption now also passes through rollback cleanup.

## Presentation

Five hosts produce five plan rows. The fixture examples below come from the real
resolver with all hosts, the Everything profile and an absent installed state:

- [60 columns](plan-60.txt)
- [80 columns](plan-80.txt)
- [120 columns](plan-120.txt)

They are fixture output, not an installation performed on this machine. Long target
paths, URLs and operation metadata stay in `--verbose`; conflicts and errors remain
visible by default. The overview explains global locations or shows the project
root. Backup candidates are conditional because a logical managed target can have
missing files; actual retained backup roots are shown after execution.

Design decisions: retain the existing banner for identity; use one orange activity
accent; align per-host action counts to reduce repeated target descriptions; reserve
motion for ongoing work. Energy/rhythm/motion: 1/1/1. No decorative panels, fabricated
progress values, invented statistics or new selection flows.

## Verification evidence

The focused suite is `python -m unittest tests.installer.test_terminal_ux -q`.
It exercises real local Git remotes, real atomic file operations in temporary
directories and Questionary with controlled keyboard input.

- PASS: callback is observed before a real fetch; source counts match actual groups.
- PASS: Live output grows while the main thread blocks in a real subprocess, and
  stops after cancellation with the cursor restored.
- PASS: target completion waits for multiple operations; success/current/blocked/
  failed/skipped/manual accounting is distinct; no false success percentage.
- PASS: final verification failure removes successful installation credit.
- PASS: atomic rollback restores previous content after errors and KeyboardInterrupt.
- PASS: 60/80/120-column rendering, long Windows target paths, verbose diagnostics.
- PASS: local-remote dry-run creates neither project nor state directories.
- PASS: redirected/non-TTY output ignores FORCE_COLOR; NO_COLOR, including an empty
  value, suppresses colors; plain mode emits no animation escapes.
- PASS: real Questionary host/profile selection, yes/no confirmation; cancellation
  preserves files and cleans temporary sources.
- PASS: display callback failure cannot fail an installation.
- PASS: mutation suppressing the pre-fetch event is detected by the pre-fetch test.

Full suite: `python -m unittest discover -s tests -q` ran 240 tests in 198.728s:
239 passed and one opt-in test skipped. The 17 focused UX tests passed again after
the final summary-width refinement. The earlier separate installer run executed
134 tests: 133 passed and one opt-in skip, before the last three UX cases were added.
`python -m compileall -q src/ai_rules` and `git diff --check` passed.

The existing PyInstaller spec built the final Windows executable successfully
(PyInstaller 6.22.3). The rebuilt executable passed all three smoke cases:

1. Bundled dry-run from outside the repository: exit 0, no ANSI, no project/state writes.
2. Bundled installation into a disposable project, exporting frozen refs from the
   local repository: exit 0, three skill artifacts present, three installed.
3. Repeat against that disposable project: exit 0, three already current, no ANSI.

The executable build did not stage or modify release bundles or the release manifest.
Temporary build and smoke evidence remain at
`C:/Users/Lenovo/AppData/Local/Temp/ai-rules-ux-build-pq4_l5le/`.
Final branch/whitespace checks passed; source, documentation and new example/test
files contain no trailing whitespace. Work remains uncommitted on `main`.

## Limits

NOT VERIFIED: manual Windows PowerShell/Windows Terminal interactions and native
Linux/macOS terminals. The available Windows PTY fails Questionary's native console
check (`No Windows console found`). This is separate from the passing controlled
Questionary tests and simulated Rich interactive-console tests. Real terminal
screenshots were unavailable; text renders and width assertions are provided.

The optional uncommitted Search First distribution installation test is skipped
without `AI_RULES_SEARCH_FIRST_CANDIDATE`; no candidate runtime publication is part
of this task. Native agent discovery/activation remains outside file verification.

## Dependency evidence

Rich's official [Live documentation](https://rich.readthedocs.io/en/stable/live.html)
and [console documentation](https://rich.readthedocs.io/en/stable/console.html) were
queried through Context7. Live supplies automatic refresh and context cleanup;
Rich supplies width handling and terminal rendering, while explicit stream/CI/TERM
checks enforce plain output. Packaging uses the existing PyInstaller spec and its
standard Rich hook; no runtime skill branches or release manifest were changed.
