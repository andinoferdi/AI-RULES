# andino-optimize-prompt: authoring evaluation

Status: skill authored; local commit only, not pushed. Installed-host behavior in a new session is
not verified yet.

## Design decisions (accepted 2026-11-07)

- Bundled resource `resources/prompt-patterns.md` copies the slot block, skill and MCP pickers,
  the `council`/`ponytail` note and three examples verbatim from the `main` README. The `main`
  test `tests/test_optimize_prompt_patterns.py` fails when they drift. `main` stays the source of truth.
- After the prompt is written the skill returns it with notes and offers once to run it; it runs
  only after an explicit yes.
- Explicit invocation only. The index row excludes ordinary task prompts. A
  `disable-model-invocation` flag is not used because the runtime validator rejects boolean scalars.

## Method

Same six raw prompts, same instruction, same read access, one Sonnet worker per arm (effort
medium). The prompts are reconstructions written from the user's descriptions, approved before the
runs. The oracle was written before any run and was not shown to the workers.

Raw prompts:

- a: buatin animasi hover taskbar kayak macOS, referensinya video ini [link YouTube]. pake brainstorming dulu, terus council, design-taste-frontend, impeccable, abis itu planning terus eksekusi
- b: cek progres skripsi saya sampai mana dan langkah berikutnya apa, pakai council
- c: error next.js 16 "Encountered a script tag while rendering React component" di layout.tsx, tolong fix
- d: fix masalah kamera saya ini
- e: install chrome-devtools-mcp ke claude code, codex, opencode, antigravity cli sama antigravity ide, biar bisa kolaborasi sama playwright-mcp
- f: bikin scene three.js "The Airship That Cannot Dock" pake ponytail, antislop, council, taste, impeccable. kapal udaranya detail kayak miniatur, 7 tahap animasi

Criteria per prompt (PASS/FAIL): K1 slots complete and labels/`Mode` exact; K2 named skills and MCP
installed, no `andino-*` member, missing domain owner added; K3 conflicts flagged; K4 at most two
questions, only material ones, no invented facts.

## Results

| Arm | a | b | c | d | e | f | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline, no skill | 1 | 2 | 2 | 1 | 1 | 0 | 7/24 |
| Candidate 1 | 3 | 3 | 3 | 2 | 3 | 3 | 17/24 |
| Candidate 2 (after fixes) | 4 | 4 | 4 | 4 | 4 | 2 | 22/24 |

Baseline failures: `andino-*` phase members in `Skills` (5 of 6); phase lists inside `Mode`;
Layer 1 rules copied into `Constraints`; invented requirements (reduced motion, build/test,
`next/script`, airship parts); three to five questions duplicating placeholders. It did add
`skripsi-skill` and `threejs-skills` and flagged `ponytail` and `council` in a.

Candidate 1 gaps, fixed before candidate 2: phase order left in `Task`; slot label changed to
`Done when (usulan)`; Layer 1 markers judged missing from the in-context copy; an installed server
listed in `Tools/MCP`; a question duplicating a placeholder.

Candidate 2 gaps in f, fixed afterwards and NOT_VERIFIED by a further run: `Done when` copied
checks from the bundled 3D example; `antislop` relevance not questioned.

## Repository checks

Recorded in the session report: validator and test runs on `main` compared with a pre-change
baseline, and `ai-rules setup --dry-run` for the five hosts.
