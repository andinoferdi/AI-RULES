# Plan: upgrade learning-workspace to the sibling layout

Status: IN_PROGRESS. Density: STANDARD. Branch `skill/learning-workspace-upgrade` from
`origin/main` 1e78323. Owner decisions (2026-11-26, confirmed in chat):

- D1 Quick learning stays in chat and creates no file; a workspace only for an explicit
  persistent goal or an existing workspace.
- D2 Workspace lessons are HTML with a shared stylesheet and quiz component; Markdown is the
  fallback.
- D3 Workspace location: an existing `MISSION.md` in the current folder means continue there;
  otherwise propose one path and ask once.
- D4 Suggest communities (never create accounts), respect this user's opt-out.
- D5 Full comparison trial (frozen rubric, blind grading).
- D6 Commit, push, PR to `main`; merge after green CI; then `ai-rules setup` from the clone.

Council verdict (5 advisors Sonnet 5.5 medium, 3 reviewers Haiku 5.5 low; reviewers ranked the
Executor response first in all three): Option 3, rewrite in the sibling layout with format,
lesson and pedagogy resources, router and safety kept. Risk all advisors named: over-production
of files on simple requests. Verdict flips if the candidate writes files on t1, t2 or t7, or does
not reach the teach and current scores on t4 to t6; then fall back to Option 2 (graft formats,
keep the old body).

## Acceptance

- A1 Candidate scores at least the teach arm and at least the current arm on every one of the 36
  criteria in [rubric.md](rubric.md), graded blind with all four arms.
- A2 `python scripts/ci_checks.py --group skills` passes.
- A3 `python scripts/check_andino_evolution_methods.py` and `scripts/check_andino_matt_methods.py`
  pass for `learning-workspace` against the edited runtime.
- A4 After merge, `ai-rules setup` from the clone installs the new `andino-learning-workspace`
  (installed `SKILL.md` equals `skills/andino-workflow/skills/learning-workspace/SKILL.md`).

## Constraints found in the repository

- The skill folder may hold only `.md` files (`runtime_files` in
  `scripts/validate_andino_capabilities.py`): CSS and JS starters live as fenced blocks.
- `GUIDE.md` is `SKILL.md` without frontmatter (debugging, brainstorming).
- `check_andino_evolution_methods.py` needs exactly one ```` ```python evolution-example ```` block
  in `GUIDE.md` with `choose_mode` and the four existing outcomes: keep it unchanged.
- `check_andino_matt_methods.py` runs the single ```` ```python ```` block of
  `resources/worked-example.md`, compares `result.json` with `EXPECTED["learning-workspace"]`, checks
  `ARTIFACT_CONTRACTS` strings and rejects `href`/`src` to `http(s)` in generated HTML.
- Neither checker runs in CI; both are run by hand for A3.

## Tasks

### T1 — Rewrite SKILL.md and GUIDE.md
Readiness: READY. Depends on: none. Owns `skills/andino-workflow/skills/learning-workspace/SKILL.md`,
`GUIDE.md`.

Change Specification: replace the whole body. Frontmatter `description` (trigger only):
"Use when the user asks to be taught or to learn a concept, tool or skill, now in the
conversation or over several sessions, names a folder for learning materials, or continues a
learning workspace (a MISSION.md with lessons or learning records). Operates under Andino Workflow
governance." Sections in sibling order: title "Teach so the learner can do something new, and
keep what they learned"; member box; Purpose; Trigger and non-trigger; Choose the route (table:
direct answer, quick lesson, repair, workspace, course exercises; with "no file before the
workspace route"); resource table (Current need / Resource / Skip when); Prerequisites; Quick
lesson Q1-Q3; Repair R1-R2; Workspace steps 1-7 each ending "Done when"; Continuing a workspace
(evidence, misconceptions, mission change, wisdom questions); Rules; Shortcuts; Red flags;
Ownership and permission boundary; Output; Verification checklist; Worked example and
anti-pattern; Fallback; Local resources; Learning mode example (existing `evolution-example`
block, byte-identical code); Provenance. Rules that close observed baseline gaps:

- reference sheet with every lesson (both arms missed it);
- community suggestion on a wisdom question unless this user opted out (both missed);
- preferences and opt-outs come only from this user's workspace (teach leaked one);
- one or two retrieval questions on earlier lessons in each new lesson (both thin);
- record a corrected misconception as a learning record (teach missed);
- research before workspace claims, sources cited next to claims (current did none);
- one open why-question with a guess when the mission is missing (current asked five);
- quiz options within two words of each other, correct position varied (current leaked).

GUIDE.md = SKILL.md minus the frontmatter block and the blank line after it.

Actions: write SKILL.md; generate GUIDE.md with
`python -c "import pathlib,re;p=pathlib.Path('skills/andino-workflow/skills/learning-workspace');t=(p/'SKILL.md').read_text(encoding='utf-8');(p/'GUIDE.md').write_text(re.sub(r'\A---\n.*?\n---\n\n','',t,flags=re.S),encoding='utf-8')"`.
Check: `diff <(tail -n +6 SKILL.md) GUIDE.md` empty; links resolve (T6 check).

### T2 — Workspace formats resource
Readiness: READY. Depends on: none. Owns `resources/workspace-formats.md` (new).

Change Specification: templates and rules for `MISSION.md`, `RESOURCES.md` (Knowledge, Wisdom,
Gaps, opt-out line), `NOTES.md`, `learning-records/NNNN-slug.md` (when to write, what does not
qualify, Status superseded), `GLOSSARY.md` (add a term only after correct use; Avoid aliases),
the folder layout and numbering. Adapted from teach's four `*-FORMAT.md` files (MIT, ad5400b),
rewritten, with Andino additions: per-user isolation, quiz score is not mastery, health limits
in Constraints.

### T3 — Lesson and assets resource
Readiness: READY. Depends on: none. Owns `resources/lesson-and-assets.md` (new).

Change Specification: lesson page contract (one HTML file, sections in order: the win, what you
need to know with citations, practice with immediate feedback, review of earlier lessons, primary
source, ask-me-back reminder, links); starter `assets/lesson.css` (```css block) and
`assets/quiz.js` (```js block, `data-answer`, `data-why`, feedback paragraph); reference sheet
template; quiz rules; Markdown fallback with an answer key separated from the questions.

### T4 — Pedagogy resource
Readiness: READY. Depends on: none. Owns `resources/pedagogy.md` (new).

Change Specification: knowledge, skills, wisdom; fluency vs storage strength; retrieval,
spacing, interleaving; difficulty low for new knowledge and high for practice; choosing the next
lesson from mission and records; designing feedback loops for knowledge, procedures and physical
skills; what counts as evidence; answering wisdom questions and choosing communities; health and
safety topics.

### T5 — Worked example and its checker
Readiness: READY. Depends on: T2, T3. Owns `resources/worked-example.md`,
`scripts/check_andino_matt_methods.py` (`EXPECTED["learning-workspace"]`,
`ARTIFACT_CONTRACTS["learning-workspace"]`).

Change Specification: prose walk-through of one session (mission question, files, lesson,
answer, record), then one ```` ```python ```` block that builds a workspace in the current folder
and writes `result.json`:

```python
result = {"files": sorted(...), "recorded": ["timeouts", "idempotency"],
          "covered_not_learned": ["retry identity"], "quiz_positions": [2, 0, 1],
          "quiz_options_within_two_words": True, "links_resolve": True, "scheduled": False}
```

Checker: `EXPECTED["learning-workspace"]` becomes that dict with the literal file list;
`ARTIFACT_CONTRACTS["learning-workspace"]` checks `MISSION.md` ("diagnose safe retries",
"Out of scope"), `lessons/0001-retry-identity.html` ("../assets/lesson.css",
"../reference/retry-identity.html", "Primary source"), and the misconception record.
Proof: `python scripts/check_andino_matt_methods.py` (see its `--help`) PASS for the method.

### T6 — Package records
Readiness: READY. Depends on: T1-T5. Owns `references/license.md` (skill),
`skills/andino-workflow/references/internal-method-index.md` (row 31 trigger text),
`skills/andino-workflow/README.md` (row 59), `skills/andino-workflow/references/legal/provenance.md`
(new paragraph), `evals/andino-method-routing.json` (one new behavior case: quick lesson stays in
chat), `docs/validation/andino-evolution/matt-methods.json` (trigger and dispositions point at the
new resources).

Proof: `python scripts/ci_checks.py --group skills` PASS (A2); every relative link in the skill
folder resolves (small script over `](...)`).

### T7 — Candidate run and blind grading
Readiness: READY. Depends on: T1-T5. Owns `docs/validation/learning-workspace/trial.md`,
`scores.md`.

Actions: `setup_run.py run-4 --guide <candidate copy>`; one runner (Sonnet 5.5, medium) with the
rubric's run prompt; collect; shuffle run-1..4 to A-D (mapping kept outside the grading folder);
one grader (Sonnet 5.5, medium) with rubric, fixture and A-D; write trial.md and scores.md.
Gate A1. On a miss: fix the text for the failed criterion, rerun only after asking the user.

### T8 — Deliver
Readiness: READY. Depends on: T6, T7. Commit (authorized), push, PR to `main`, wait for green CI,
merge (authorized after green), `git pull` in the main clone, `ai-rules setup`, compare the
installed SKILL.md (A4).

## Result / Evidence (2026-11-27)

- T1-T6 DONE. GUIDE.md equals SKILL.md without frontmatter (byte check); every relative link
  in the skill folder resolves; `check_andino_matt_methods.py` reports `learning-workspace` PASS
  (the script fails on other methods whose folders no longer exist, unchanged by this branch);
  the `learning-workspace` policy of `check_andino_evolution_methods.py` returns the four
  expected routes and kills its mutant (the script as a whole stops earlier on `brainstorming`,
  unchanged by this branch).
- T7 DONE with a ruling: three rounds, candidate 71, 70 and 71 of 72 against at most 62 for any
  other arm; in each round one different criterion fell to 1, each fixed in the text afterwards
  and each scoring 2 in the other rounds. The owner accepted the result on 2026-11-27 without a
  fourth round. Details: [trial.md](trial.md).
  Ruling: A1 accepted at 35 of 36 criteria per round with every miss fixed — the owner's
  decision after round 3 — if wrong, one criterion may still score 1 in a future run.
- Ruling: the worked example records `retry safety misconception` instead of `idempotency` as
  the second record, to show a corrected misconception — plan text only — none.
- A2: `python scripts/ci_checks.py --group skills` PASS run alone before the last two text edits
  (286 tests, OK, skipped 3); after them, `validate_skills.py`, `validate_andino_capabilities.py`
  and 145 affected tests PASS. Two earlier full runs failed one setup-distribution test each
  while a dozen other worktrees ran CI on this machine; both tests pass alone.

## NEXT ACTION

T8: commit, push, open the PR and wait for GitHub CI.
