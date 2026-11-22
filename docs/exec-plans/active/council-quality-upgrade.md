# Council quality upgrade

Status: IN_PROGRESS
Plan Depth: STANDARD
Current Phase: Phase 1 — Council runtime
Last Updated: 2026-11-22

## Executive Snapshot

Goal: bring Council output quality to at least the level of
aiwithremy/claude-skills-llm-council (Reference 1) and karpathy/llm-council
(Reference 2) without losing evidence discipline, honest host fallback, Focus and
Andino integration. A Council consultation (5 advisors, 3 anonymous reviewers,
main agent as chair) chose a lean template-driven restructure. Next: T1.

## Objective

Every Council run uses the same written prompts, keeps the five lenses in real
tension, labels evidence, respects the user's sub-agent budget, and returns one
fixed verdict layout that README and SKILL.md describe identically. Ship it to
`ai-rules setup` by publishing the `council` branch and moving the stable pin.

## Acceptance Criteria

- [ ] R1: `references/prompts.md` holds the advisor, reviewer and single-agent
  templates and the chair checklist. SKILL.md requires reading it before the first
  advisor prompt is written.
- [ ] R2: Advisor template tells each lens to argue its angle at full strength and
  still label every material claim `[verified]`, `[reported]`, `[assumption]` or
  `[unknown]`, with no invented numbers.
- [ ] R3: Reviewer template asks exactly four things: strongest response, weakest
  consequential claim challenged against the brief, what all responses missed, and
  a final line `FINAL RANKING: X, X, X, X, X`.
- [ ] R4: SKILL.md defines a run plan: default 5 advisors + 3 reviewers, main agent
  as chair, waves no larger than the stricter of 3 or the host/user limit, one
  announcement of count/task/model/effort for every wave before dispatch, and
  waiting for approval when user or project rules require it.
- [ ] R5: Bounded context step: read only material the user named plus project
  instruction files relevant to the decision, never secrets or unrelated private
  files, and disclose what was read in the verdict.
- [ ] R6: One verdict layout, inline in SKILL.md and identical in README:
  recommendation first, then agreement, clash, blind spots, what would change the
  verdict, one first action, and a one-line run disclosure.
- [ ] R7: Single-agent fallback uses the same templates and keeps the label
  "single-agent perspective review".
- [ ] R8: `references/worked-example.md` shows one complete compact run.
- [ ] R9: `references/license.md` is MIT, Copyright (c) 2026 Andino Ferdiansah.
  Provenance says no text from the unlicensed references was copied.
- [ ] R10: `ai-rules setup --capability council` installs the new commit from
  `latest` source in an isolated project, together with Focus.

## Scope

In scope: `council` branch (SKILL.md, README.md, references/*), `main` branch
(`src/ai_rules/release/data/release_manifest.json`, `evals/council.json`, this plan).
Out of scope: renaming the skill, catalog or profile changes, other skills,
updating the user's global installation without a separate request.

## User Decisions / Clarifications

- 2026-11-22: user accepted all five recommendations: keep standalone `council`
  with sibling layout; consultation with 8 sub-agents (5 advisors Sonnet/medium,
  3 reviewers Sonnet/low, chair = main agent); one live verification run of the
  new skill on the auth-library fixture with the same composition; MIT license
  for Andino Ferdiansah; commit and push both `council` and `main`.

## Baseline / Starting Evidence

- `origin/council` at `aafc9a089fbfc27aa1ee745ead2f781e67218cf4`: SKILL.md (74 lines)
  and README.md only. No prompt templates; advisors share one balanced answer shape;
  SKILL.md output headings (Trade-offs, Agreement and dissent, Uncertainty, First
  action) differ from README (Titik Temu, Perbedaan, Hal Terlewat, Rekomendasi,
  Langkah Pertama); reviewer count unspecified; no context step; no example.
- Reference 1 SKILL.md read through `gh api` on 2026-11-22: full templates,
  lean-in advisors, context scan, 5 reviewers with 3 questions, separate chairman,
  fixed five-heading verdict. GitHub license: null.
- Reference 2 `backend/council.py` read on 2026-11-22: reviewers end with a strict
  `FINAL RANKING:` list that is parsed and averaged. GitHub license: null.
- `origin/main` at `85b4e4d79de94f90eb6ac57155e0be7fafe4e664`; manifest
  `release_sequence` 39; council pin `aafc9a0…`, council `release_sequence` 36.
- Validator allows `README.md`, `SKILL.md` and `references/*.md` in the package.

## Council decision record

Brief: options A (templates only), B (template-driven restructure), C (port
Reference 1's full flow). All five advisors chose a lean B. Reviewers ranked the
anonymized responses unanimously: Expansionist, Executor, First Principles,
Contrarian, Outsider.

- Agreement: templates and lean-in advisors fix the named causes of variance; C
  breaks the sub-agent rules (11 agents, more waves); A leaves lens convergence.
- Clash: aggregate ranking. Three advisors called it noise with one model family;
  the top-ranked response wanted it for eval-able output. Chair decision: keep
  one `FINAL RANKING` line per reviewer (cost: one line) and report the tally as a
  same-model signal, never as proof. No averaged score drives the verdict.
- Clash: optional "full council" profile. Reviewers flagged it as a second code
  path. Chair decision: one parameter instead. Default 3 reviewers; 5 only when
  the user asks or approves the larger budget.
- Blind spots from review: context scan can leak private data (R5); agents may
  skip references, so the verdict layout and the reading step stay inline (R1, R6);
  waves are sequential (advisors before reviewers), so the announcement covers all
  waves at once (R4); fallback must use the templates (R7); pin rollback (below).
- Lean-in risk: advisors may overstate. Countered by mandatory evidence labels in
  the advisor template and the chair's evidence check (R2).

## Constraints & Invariants

- Keep frontmatter `name: council` and the existing description (routing, catalog
  and `test_optimize_prompt_patterns` depend on current identity).
- Write all text fresh. Reuse ideas only; references have no license.
- Keep Focus/Andino relationship, privacy rules, conditional recommendations and
  the no-auto-trigger rule from the current SKILL.md.
- Validator path rules: only `README.md`, `SKILL.md`, `references/*.md`.
- Rollback: restore council pin `aafc9a089fbfc27aa1ee745ead2f781e67218cf4` and
  `release_sequence` 39 in the manifest; the old branch commit stays reachable.

## Artifact / System Impact Map

### Create (council branch)
- `references/prompts.md` — advisor, reviewer, single-agent templates, chair checklist
- `references/worked-example.md` — one compact complete run
- `references/license.md` — MIT notice

### Modify
- `SKILL.md` (council) — restructured contract
- `README.md` (council) — verdict layout, run budget, references, license link
- `src/ai_rules/release/data/release_manifest.json` (main) — new pin and sequence
- `evals/council.json` (main) — budget, context-privacy and verdict-layout cases
- this plan (main) — evidence and status

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Council runtime | IN_PROGRESS | R1-R9 | council branch T1-T3 | Not run |
| Phase 2 — Verification | TODO | R1-R9 behavior | T4 | Not run |
| Phase 3 — Publish and setup | TODO | R10 | T5-T6 | Not run |

## Coverage

| Requirement | Task | Check |
| --- | --- | --- |
| R1, R2, R3, R7 | T1 | grep checks in T1; live run in T4 |
| R4, R5, R6 | T2 | grep checks in T2; live run in T4 |
| R6 README parity | T3 | heading comparison in T3 |
| R8, R9 | T1, T3 | file exists, links resolve via validator |
| Package validity | T5 | `scripts/validate_skills.py` with local council ref |
| R10 | T6 | isolated `setup --source latest`, installed blob equals pushed blob |

## Detailed Execution

### Phase 1 — Council runtime

#### T1 — Prompt templates, worked example and license
Status: TODO
Readiness: READY
Requirements: R1, R2, R3, R7, R8, R9
Depends on: none
Owns: create `references/prompts.md`, `references/worked-example.md`,
`references/license.md` on branch `council`.

Change Specification:
- `references/prompts.md` sections, in order: `## Advisor template`,
  `## Lens cards` (one paragraph per lens plus the three tensions: Contrarian vs
  Expansionist, First Principles vs Executor, Outsider as fresh eyes),
  `## Peer reviewer template`, `## Single-agent variant`, `## Chair checklist`.
- Advisor template fields (placeholders in braces): `{lens name}`, `{lens card}`,
  `{decision brief}`, `{word range}` (default 150-300). Required instructions:
  argue the lens at full strength and leave balance to the chair; state preferred
  option, strongest reason tied to a named criterion, most consequential downside,
  one observation that would change the choice; label material claims with the four
  tags; no invented figures; no preamble; no tools unless the run plan grants them.
- Reviewer template ends with this exact block:

```text
1. Strongest response against the brief's criteria, and why.
2. Weakest consequential claim or biggest blind spot, challenged against the brief.
3. What every response missed.
FINAL RANKING: X, X, X, X, X
```

- Chair checklist: de-anonymize only after all reviews; tally rankings as signal;
  re-check every decisive claim against the brief's evidence tags; may overrule
  the majority with stronger evidence; one first action.
- `references/worked-example.md`: the auth-library decision from
  `evals/council.json` (`architecture-switch-condition`), short excerpts of each
  stage and the final verdict in the R6 layout. Excerpts are illustrative, marked
  as such.
- `references/license.md`: standard MIT text, `Copyright (c) 2026 Andino Ferdiansah`
  (same body as `origin/natural-writing:references/license.md`).

Actions:
- [ ] Write the three files.
- [ ] `grep -c "FINAL RANKING: X, X, X, X, X" references/prompts.md` expect 1;
  `grep -c "\[assumption\]" references/prompts.md` expect ≥1.

Result / Evidence: Not run — planned checks only.

#### T2 — Restructure SKILL.md
Status: TODO
Readiness: READY
Requirements: R1, R4, R5, R6, R7, R9
Depends on: T1 (links)
Owns: `SKILL.md` on branch `council`.

Change Specification (sections, in order):
1. Frontmatter unchanged. Intro paragraph unchanged in meaning; add Reference 2.
2. `## Relationship to AI-RULES` — keep current bullets.
3. `## When to convene` — keep.
4. `## Context and brief` — current evidence/framing text plus the bounded context
   rule (R5) and "Record which sources were read for the run disclosure."
5. `## Five advisor lenses` — keep list; add the three tensions in one sentence;
   point to `references/prompts.md` lens cards.
6. `## Run plan and budget` (new) — default composition, wave rule, model tier
   rule (advisors mid tier medium effort, reviewers mid or low tier low effort,
   never max effort, never every agent on the strongest tier or high effort), one
   announcement for all waves, approval when required, no relaunch without asking,
   5 reviewers only on request.
7. `## Conduct the council` — 1 read `references/prompts.md`; 2 independent round;
   3 anonymize with a recorded shuffle; 4 peer review; 5 chair synthesis by the main
   agent; 6 present; 7 persistence (keep current rule).
8. `### Host and fidelity limits` — keep; add that the fallback uses the
   single-agent variant.
9. `## Output contract` — the layout block below, localized headings allowed.
10. `## Provenance` — inspired by Reference 1 (Ole Lehmann) and Reference 2 (Andrej
    Karpathy); neither declares a license; no text copied; link `references/license.md`.

```markdown
## Council Verdict: {topic}
**Recommendation:** {choice and decisive reason}
### Where the council agrees
### Where the council clashes
### Blind spots from review
### What would change the verdict
### First action
{exactly one step}
_Run: {N advisors, M reviewers, models/effort, or single-agent perspective review}; context read: {sources}._
```

Indonesian heading set (used when the user writes Indonesian): Rekomendasi, Titik
temu, Perbedaan, Hal terlewat, Yang bisa mengubah verdict, Langkah pertama.

Actions:
- [ ] Rewrite SKILL.md as specified; keep under ~150 lines.
- [ ] `grep -n "references/prompts.md" SKILL.md` expect ≥2 hits;
  `grep -c "^### " SKILL.md` includes the layout headings.

Result / Evidence: Not run — planned checks only.

#### T3 — README parity
Status: TODO
Readiness: READY
Requirements: R6, R9
Depends on: T2
Owns: `README.md` on branch `council`.

Change Specification: keep install and usage sections; replace "Verdict Output
Format" with the R6 layout in both languages; add a short "Run budget" note
(default 8 sub-agents, waves of at most 3, announcement before dispatch); list the
three reference files; add a License line linking `references/license.md`.

Actions:
- [ ] Compare the heading list in README against SKILL.md by eye and grep.

Result / Evidence: Not run — planned checks only.

### Phase 2 — Verification

#### T4 — Package validation and live trial
Status: TODO
Readiness: READY after T1-T3 commit on local `council`
Requirements: R1-R9
Depends on: T1, T2, T3
Actions:
- [ ] Commit on `council` (authorized). From the `main` checkout run
  `python scripts/validate_skills.py --council-ref council` and expect no council
  errors.
- [ ] Live trial: follow the new SKILL.md on the `architecture-switch-condition`
  prompt with 5 advisors (Sonnet, medium) and 3 reviewers (Sonnet, low), main agent
  as chair. Pass criteria: every advisor uses the template fields and evidence
  tags; five distinct preferred positions or explicitly argued agreement; every
  reviewer ends with a parseable `FINAL RANKING`; verdict follows the R6 layout,
  names the audit requirement as a switch condition, treats it as unverified, and
  gives exactly one first action.
- [ ] Record pass/fail per criterion here. Parity with Reference 1 stays
  unmeasured unless the same fixture is also run through it (not authorized).

Result / Evidence: Not run — planned checks only.

### Phase 3 — Publish and setup

#### T5 — Publish council and move the pin
Status: TODO
Readiness: READY after T4 pass
Depends on: T4
Owns: branch `council`; `src/ai_rules/release/data/release_manifest.json`,
`evals/council.json`, this plan on `main`.

Change Specification:
- Manifest: top-level `"release_sequence": 40`, `"verified_at": "2026-11-22"`;
  `first_party.council.commit` = new council SHA, `release_sequence` 40.
- `evals/council.json`: append cases `run-budget` (announces count, task, model
  and effort for every wave before dispatch; forbidden: dispatch before approval
  when rules require it), `context-privacy` (reads only relevant named sources and
  discloses them; forbidden: passing secrets or unrelated private files to
  advisors), `verdict-layout` (recommendation first and the six sections;
  forbidden: missing run disclosure or more than one first action).

Actions:
- [ ] `git push origin council`; confirm `git ls-remote origin council` equals the SHA.
- [ ] Edit main files, run `python -m unittest tests.installer.test_council
  tests.installer.test_live_updates` and `python scripts/validate_skills.py`
  with the existing venv interpreter and `PYTHONPATH=src`.

#### T6 — Isolated setup proof and main push
Status: TODO
Depends on: T5
Actions:
- [ ] `ai-rules setup --scope project --project-root <scratch>/proj --state-dir
  <scratch>/state --host claude-code --capability council --source latest --yes
  --non-interactive --no-agent-defaults --no-progress`; expect council and focus
  installed; `git hash-object` of installed SKILL.md equals the blob in the new
  council commit.
- [ ] Commit and push `main`; confirm remote SHA; switch the checkout back to `council`.

## NEXT ACTION

T1: on branch `council`, write `references/prompts.md`, `references/worked-example.md`
and `references/license.md`, then run the T1 grep checks.
