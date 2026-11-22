# Natural Writing quality-v2 record

Recorded 2026-11-22 for the upgrade from `a215ca4` (branch head before the change;
pinned `f359b7b`) to `e792e33`. Each line proves only what it names.

## Cases and grader

[cases.json](cases.json) holds 18 synthetic cases (11 Indonesian, 7 English;
8 marked `judge`, at least 5 KEEP cases that punish over-correction). Their failure
families follow the reference skills humanizer-id, naskah-id, bahasa-skills,
bahasa-indonesia-skill, asd-ste100-skill and SimpleEnglish (ideas only, no text).
`scripts/grade_natural_writing.py` grades `<id>.artifact.md` / `<id>.reply.md`
outputs with the skill's `scripts/check.py`; `tests/test_grade_natural_writing.py`
covers it.

## Observed

| Run | Generator | Result |
| --- | --- | --- |
| Baseline, skill `a215ca4` | 1 subagent, Sonnet/medium, prompts and inputs only | 16/18 after two harness fixes |

Baseline failures: `id-write-placeholder` (no `[PERLU RUJUKAN:` marker) and
`id-edit-keep-terms` (KEEP case: a correct "merupakan" in a definition was replaced
with "adalah"; the old Indonesian reference told it to). Both are addressed in
`e792e33`.

Harness fixes found by the baseline: the grader now compares stripped text (a trailing
newline failed an untouched review), and `check.py compare` ignores numbered-list
markers as protected numbers.

## Not verified

- Candidate `e792e33` on the 18 cases: outputs were generated but not graded; the
  owner asked to ship without the end-to-end round.
- Blind-judge round (old vs new vs naskah-id): not run, same reason.
- Native activation on any host after `ai-rules setup` with the new pin.
