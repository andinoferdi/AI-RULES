# Focus quality upgrade

Status: IN_PROGRESS
Plan Depth: STANDARD
Current Phase: Phase 1 — Focus package
Last Updated: 2026-11-22

## Executive Snapshot

Goal: raise Focus output quality to at least the level of `ayghri/i-have-adhd`
(the reference) without losing Focus strengths. A Council (5 advisors Sonnet/medium,
3 anonymous reviewers Sonnet/low, main agent as chair; reviewers ranked unanimously)
chose a narrow Option 2: keep the Focus structure and budgets, add the rules that
explain the reference's measured gains (state reporting, error reports), give every
shape rule a compact Bad/Good pair, add an override section under the existing
priority order, load language references per reply language, and enforce the shape
with static checks. No implementation has run yet.

## Objective

Focus replies lead with the answer, restate progress on multi-step work, report
errors as symptom / confirmed cause / next check, keep visible lists small, and
break the shape only for the listed reasons. The change ships to `ai-rules setup`
by publishing the `focus` branch and moving the pin through
`python scripts/promote_skill.py focus`.

## Acceptance Criteria

- [x] R1: SKILL.md gains a "Why the shape matters" section with five reader facts
  (small working memory, knowing is not doing, starting is the hardest step, vague
  estimates fail, progress must be visible), written for any reader, never naming
  a diagnosis outside the provenance line.
- [x] R2: Shape rules each carry a one-line `Bad:` and `Good:` pair; at least 8
  pairs in SKILL.md, equal counts of `Bad:` and `Good:` lines, one pair in Indonesian.
- [x] R3: New rule "Restate state on multi-step work": "Step N of M done: <result>.
  Next: <step>." Only for multi-step work; when the host has a plan/task tool, the
  tool carries the state and the reply does not narrate the full plan.
- [x] R4: New rule "Keep visible lists small": group and rank, at most five visible
  items per group; presentation only, never limits analysis, search or retained items,
  and never drops items when completeness is required.
- [x] R5: Error rule keeps symptom / confirmed cause or "cause unknown" / next check,
  adds matter-of-fact tone (no "Uh oh", "There seems to be a problem").
- [x] R6: New section "When to break the shape": explicit explain/detail request;
  destructive or irreversible action ahead (confirm first); debug spiral (after
  three "still broken" turns stop patching, name the assumption that may be wrong,
  ask one diagnostic question); real ambiguity (one short question); a rule fights
  the task (options request gets 2-4 ranked options); a rule fights the host (host
  announcements stay; do the work instead of "want me to"). It sits under the
  existing priority order (host > Focus shape > A. PRIORITAS wording > explicit user).
- [x] R7: Pre-send check adds: replace idioms and figurative phrases with the literal
  action; for multi-step work confirm the state line is present. Empty hedges were
  already covered and stay.
- [x] R8: Reference loading: A. PRIORITAS always, plus only the language file for the
  reply language; mixed-language replies read both; a later switch to the other
  language reads that file once. SKILL.md states that this rule satisfies A.
  PRIORITAS's "read both" line (A text itself is unchanged; it is drift-checked).
- [x] R9: Every existing strength survives: budget table values, six cut rules
  and the act-differently test, artifact exemption, explanation repair, honest time
  estimates ("only when supported"), stop-focus persistence, Neovim example, links
  to the three references, Ayoub Ghriss MIT attribution.
- [x] R10: SKILL.md body (after frontmatter) is at most 2,000 words (see Ruling in T1), measured by
  `len(body.split())`.
- [x] R11: README.md on `focus` describes the same rules (rule table updated, reading
  rule updated) in plain prose.
- [x] R12: `scripts/validate_skills.py::focus_contract(files)` enforces R2, R8 (key
  sentence), R10, required headings, diagnosis-word rule (R1); unit tests cover a
  passing fixture and each failure.
- [x] R13: `evals/focus.json` no longer forbids per-language loading and adds cases
  for restated state, partial success, agent-owned edit, debug spiral and a long list.
- [ ] R14: `ai-rules setup --host codex --capability focus --source bundled` from the
  promote clone installs a SKILL.md containing "Restate state on multi-step work".
- [ ] R15: `python scripts/promote_skill.py focus` prints `PR: <url>`; the owner
  merges after green checks.

## Scope

In scope: `focus` branch (SKILL.md, README.md); `main` via the promote PR
(`scripts/validate_skills.py`, `tests/test_validate_skills.py`, `evals/focus.json`,
`docs/ci-coverage.md` focus row, this plan, manifest pin written by the script).
Out of scope: bundled reference text (drift-checked against WebBased), Council's
"honor the full references" wording (compatible: it honors what Focus provides),
other skills, the user's global installation, live paid evals (user chose static only).

Decision: the validator/test change ships inside the promote PR, not a separate
branch, because the new contract cannot pass against the old pinned Focus commit.
AGENTS.md step 3 allows main data/tests fixed in the promote clone to ship in the
same PR.

## User Decisions / Clarifications

- 2026-11-22: Council in waves of at most 3 (approved 10, 8 used); static proof only;
  per-language reference loading; owner merges the promote PR. Commit and push of
  the `focus` branch were authorized in the original request.

## Baseline / Starting Evidence

- `origin/focus` = `95124736667b5a6a1175577a6edd3526eef19874` (pinned, release
  sequence 39). SKILL.md ~1,250 words, one Bad/Good example, no state rule, no list
  cap, no override section; requires reading all three references in full.
- Reference `skills/i-have-adhd/SKILL.md` and `evals/RESULTS.md` read via `gh api`
  on 2026-11-22: gains concentrated in multi-step-progress (+2.53) and error-report
  (+2.40); losses on agent-owned-edit (-0.33) and partial-success (-0.63).
- `scripts/validate_skills.py`: focus checked by `package_files`, optional
  `focus_reference_drift` (`--webbased-ref`, used by `ci_checks.py`), `eval_cases`.
- `evals/focus.json` case `bundled-first-load` forbids "load only the current language".

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Focus package | DONE | R1-R11 | `.worktrees/focus` SKILL.md, README.md | focus `082ac78` pushed; validator + WebBased drift PASS |
| Phase 2 — Main contract and evals | DONE | R12-R13 | promote clone files | 46 validator tests OK; new Focus 0 errors, old Focus 5 errors |
| Phase 3 — Ship | IN_PROGRESS | R14-R15 | push, promote, setup check | Full suite 433 tests OK in clone before T3/T4 |

## Coverage

| Requirement | Task | Check |
| --- | --- | --- |
| R1-R10 | T1 | `focus_contract` on `--focus-dir .worktrees/focus` returns no errors; manual read against R9 list |
| R11 | T2 | README reread; validator package check passes |
| R12 | T3 | `python -m unittest tests.test_validate_skills -v` new tests pass |
| R13 | T4 | `python scripts/validate_skills.py` eval schema pass; grep shows no "load only the current language" |
| R8 drift guard | T1/T5 | `ci_checks.py` WebBased drift step passes (references untouched) |
| R14 | T5 | setup into temp dir, grep installed SKILL.md |
| R15 | T5 | promote prints `PR: <url>` |

## Detailed Execution

### T1 — Rewrite Focus SKILL.md
Status: DONE
Readiness: READY
Requirements: R1-R10
Depends on: none
Owns: `.worktrees/focus/SKILL.md` (worktree of branch `focus`)

Change Specification (section order after the change; keep frontmatter unchanged):
1. Intro paragraph: unchanged.
2. `## Activation and priority`: unchanged text; add one bullet pointing to
   "When to break the shape" for overrides.
3. `## Load the bundled language references`: replace the "read these files ... in
   full, once per conversation" rule with:

```markdown
On first activation, before the first substantive reply, read from the installed
Focus directory: [A. PRIORITAS](references/priority-a.md) in full, plus the
language file for the reply language in full, read only the file for the reply
language: [Human Language Indonesia](references/human-language-indonesia.md) or
[Human Language English](references/human-language-english.md). A mixed-language
reply reads both. When the conversation later switches to the other language,
read that file once at the switch. This rule satisfies A. PRIORITAS's instruction
to understand both language files.
```
   Keep the existing sentences on taking flow/register from examples, never facts,
   mirroring slang only when the user does, rereading only after context loss, and
   the "cannot be read" fallback.
4. New `## Why the shape matters` (about 90 words): the five facts from R1, each one
   line, stated for any reader.
5. `## Length budget`: unchanged table and over-budget sentence.
6. `## What to cut`: unchanged six cuts and closing paragraph.
7. `## Shape rules`: keep existing rules; give each a one-line pair. Required pairs:
   - First line: Bad: "Let's look at how your auth flow works first..." /
     Good: "Edit `src/auth.ts:42`: the token check compares the wrong field."
   - Numbered steps: Bad: "Open the file, find the function, swap it, then run tests." /
     Good: "1. Open `src/auth.ts` 2. Replace `verifyToken` 3. Run `npm test`".
   - New "Restate state on multi-step work" (R3): Bad: "Done. Ready for the next part?" /
     Good: "Step 3 of 5 done: schema updated. Next: backfill the column."
     Indonesian pair: Bad: "Sudah, lanjut?" / Good: "Langkah 2 dari 4 selesai: tabel
     sudah dibuat. Berikutnya: isi data awal."
   - Completion (visible result): Bad: "I've made some changes to the auth flow." /
     Good: "Magic-link login works; `npm test` passed 12 tests. Email sending is not verified."
   - Errors (R5): Bad: "Uh oh, there seems to be a problem with the test." /
     Good: "`auth.spec.ts:42` fails: expected 200, got 401. Cause unknown; next check: is the Authorization header sent?"
   - New "Keep visible lists small" (R4): Bad: a flat list of 14 lint warnings /
     Good: "3 groups: unused imports (8), missing types (4), long lines (2). Fix unused imports first."
   - Next action: Bad: "Hope that helps, let me know!" / Good: "Next: run `npm test` and paste the first failing line."
   - Agent-owned work: Bad: "You can fix the typo in README.md by..." / Good: (after
     editing) "Fixed the typo in README.md line 12."
   - Time estimates: keep "only when supported, with units and assumptions".
8. New `## When to break the shape` with the six cases from R6, one or two lines each.
9. `## Example` (Neovim): unchanged.
10. `## Writing artifacts and explanation repair`: unchanged.
11. `## Pre-send check`: keep six steps; add to step 3 or as new steps the R7 items
    (idioms -> literal action; multi-step reply has its state line).
12. Provenance line unchanged.

Actions:
- [ ] `git worktree add .worktrees/focus focus` from the main checkout (branch tracks origin/focus).
- [ ] Load `andino-skill-maker`; write SKILL.md per the spec above in English (SKILL.md stays English, commit 9512473).
- [ ] Count: `python -c "import sys;t=open('.worktrees/focus/SKILL.md',encoding='utf-8').read();print(len(t.split('---',2)[2].split()))"`; expect <= 2000.
- [ ] Walk R9 list against the new file; every item present.

Integration gate: T3's `focus_contract` against `--focus-dir .worktrees/focus`.
Ruling: word ceiling 2,000 instead of 1,800 — the 1,800 figure assumed the reference
was ~1,500 words, but measured the same way it is 1,187; eleven one-line pairs plus
the new sections need ~1,974 words. Per-language loading removes ~6,400-7,400 words
per activation, so total activation cost still drops sharply — cost if wrong: about
200 extra always-on words.
Result / Evidence: focus `082ac78` (pushed). Body 1,974 words; 11 `Bad:` / 11 `Good:`
lines (one Indonesian pair); R9 strings checked present (budgets, act-differently
test, artifact exemption, explanation-repair link, estimates with a basis, stop
focus, Neovim example, three reference links, Ayoub Ghriss attribution).
`python scripts/validate_skills.py --focus-dir .worktrees/focus --webbased-ref origin/WebBased`
-> PASS packages/evals and "Focus communication references match origin/WebBased".
Behavior under real sessions: NOT VERIFIED (static checks only, by user decision).

### T2 — Update Focus README.md
Status: DONE
Readiness: READY
Requirements: R11
Depends on: T1
Owns: `.worktrees/focus/README.md`
Change Specification: in the "Core Communication Rules" table add rows for "Restate
state", "Small visible lists" and "Break the shape only for a reason"; in setup/usage
text replace any "reads both references in full" wording with the per-language rule.
Use `natural-writing` for the prose. Keep layout (title, one-line purpose, tables,
Quick Start, license) consistent with sibling skills.
Actions: edit; `python scripts/validate_skills.py --focus-dir .worktrees/focus` from
main checkout passes package/link checks.
Result / Evidence: four rows added to the rules table; SKILL.md reference line states
per-language loading. Package/link validation PASS (same run as T1).

### T3 — Static Focus contract in the validator
Status: DONE
Readiness: READY
Requirements: R12
Depends on: T1 (contract literals)
Owns: promote clone `scripts/validate_skills.py`, `tests/test_validate_skills.py`
Interfaces: produces `focus_contract(files: dict[str, str]) -> list[str]`; called in
`main()` right after `package_files(files, skill, modes)` for `skill == "focus"`.

```python
FOCUS_HEADINGS = ("## Activation and priority", "## Load the bundled language references",
                  "## Why the shape matters", "## Length budget", "## What to cut",
                  "## Shape rules", "## When to break the shape", "## Pre-send check")
FOCUS_MAX_WORDS = 2000

def focus_contract(files):
    text = files.get("SKILL.md", "").replace("\r\n", "\n")
    body = text.split("---", 2)[2] if text.startswith("---") and text.count("---") >= 2 else text
    errors = [f"focus: missing section {h}" for h in FOCUS_HEADINGS if h not in body]
    words = len(body.split())
    if words > FOCUS_MAX_WORDS:
        errors.append(f"focus: SKILL.md body has {words} words (max {FOCUS_MAX_WORDS})")
    bad = len(re.findall(r"^\s*(?:[-*]\s*)?Bad:", body, re.M))
    good = len(re.findall(r"^\s*(?:[-*]\s*)?Good:", body, re.M))
    if bad < 8 or bad != good:
        errors.append(f"focus: expected >= 8 paired Bad/Good examples, found {bad}/{good}")
    if "read only the file for the reply language" not in body:
        errors.append("focus: per-language reference loading rule missing")
    if "Restate state on multi-step work" not in body:
        errors.append("focus: restate-state rule missing")
    adhd = [line for line in body.splitlines() if "ADHD" in line and "i-have-adhd" not in line]
    if adhd:
        errors.append("focus: diagnosis wording outside provenance")
    return errors
```
Note: the Bad/Good regex counts line-leading markers; T1 must put each `Bad:` and
`Good:` at a line start (optionally after a list bullet).

Tests (add class `FocusContractTest` in `tests/test_validate_skills.py`, import
`focus_contract`): a fixture built from headings + 8 pairs + both sentences passes;
removing a heading, adding words over 2000, unpairing one `Bad:`, deleting the
per-language sentence, and adding "ADHD reader" each yield one matching error.

```python
def test_unpaired_example_rejected(self):
    files = {"SKILL.md": self.skill.replace("Good: g7", "g7")}
    self.assertTrue(any("Bad/Good" in e for e in focus_contract(files)))
```
Actions: RED by running tests before adding the function (ImportError is setup, so
add a stub returning [] first; then assertions fail), implement, GREEN:
`python -m unittest tests.test_validate_skills -v`.
Result / Evidence: `FocusContractTest` (8 tests) added; `python -m unittest
tests.test_validate_skills` -> Ran 46, OK. `focus_contract` on origin/focus `082ac78`
-> []; on old `9512473` -> 5 errors (discriminating). Fixture uses "Read only" capitalized
to exercise the missing-rule branch; the check looks for the lowercase phrase.

### T4 — Update Focus eval cases
Status: DONE
Readiness: READY
Requirements: R13
Depends on: none (data only)
Owns: promote clone `evals/focus.json`
Change Specification:
- `bundled-first-load.expected` -> "Resolve installed SKILL.md directory; read bundled A and the reply-language reference in full before substantive output; no network or project dependency." `forbidden` -> "Treat a file listing or name mention as a read; skip A or the reply-language file; claim unsupported host guarantees."
- `reference-reuse-switch.expected` -> "Reuse loaded context; on the first switch to Indonesian read the Indonesian file once, then answer." `forbidden` -> "Re-read files already loaded; answer the switched language without reading its file; repeat signature phrases."
- Add behavior cases (ids): `restate-progress` (step 3 of 5 report), `partial-success`
  (some tests pass, integration unrun: report what works, what failed, what is unverified, no handing work back),
  `agent-owned-edit` (do the edit, report result), `debug-spiral` (third "still broken":
  name the suspect assumption, one diagnostic question), `long-list` (14 findings grouped,
  top group first, nothing dropped when asked for all).
Actions: edit; `python scripts/validate_skills.py` eval schema PASS.
Result / Evidence: 24 cases (19 -> 24); "load only the current language" no longer
present; one-object-per-line format kept.

### T5 — Ship through promote
Status: IN_PROGRESS
Readiness: READY
Requirements: R14, R15
Depends on: T1-T4
Actions:
- [ ] Commit T1+T2 on `focus` (no co-author trailer), `git push origin focus`.
- [ ] From main checkout: `python scripts/promote_skill.py focus --dry-run`. This
  creates `.git/promote/focus` (branch `promote/focus` from origin/main, pin written)
  and runs the checks without pushing.
- [ ] Apply T3, T4, the `docs/ci-coverage.md` focus row ("...bundled-reference
  comparison with WebBased and the static Focus shape contract") and this plan inside
  `.git/promote/focus` (leave uncommitted: a dirty clone is reused and the script
  commits everything with the pin).
- [ ] Rerun `python scripts/promote_skill.py focus`; expect `PR: <url>`.
- [ ] In the promote clone: `PYTHONPATH=src python -m ai_rules setup --host codex --capability focus --scope project --project-root <tmp> --source bundled --non-interactive --yes` (or the repo's documented entrypoint); grep `<tmp>/.agents/skills/focus/SKILL.md` for "Restate state on multi-step work".
- [ ] Report PR URL and checks; owner merges.
Result / Evidence: Not run.

## NEXT ACTION

Run `python scripts/promote_skill.py focus` (no timeout wrapper; the suite takes
~13 minutes) and expect `PR: <url>`. Ruling: the second run failed at 'Audit skripsi
requirement ownership' because `scripts/validate_skripsi_traceability.py` dropped
every file whose absolute path contains `.git`, and the promote clone lives under
`.git/promote/<skill>`; fixed by testing parts relative to ROOT (same check passes on
the normal checkout: 335 requirements). Cost if wrong: none for other paths. Ruling: the first dry-run 'FAIL' was the
590 s timeout killing the unit step, not a test failure (full suite later: 433 OK).
