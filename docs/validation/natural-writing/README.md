# Natural Writing validation record

Recorded 2026-10-19 against local, unpublished runtime commits (natural-writing
f359b7b, focus d119a80, WebBased cb75644, skripsi-skill 7ae5cd7, andino-workflow
634585a). Each level below proves only what it names.

## 1. Static structural validation (STRUCTURAL VERIFIED)
- `python scripts/validate_skills.py --andino-ref andino-workflow --skripsi-ref skripsi-skill --focus-ref focus --natural-writing-ref natural-writing --webbased-ref WebBased`:
  PASS, 7 skill packages and 7 eval schemas; Focus references match WebBased and
  both WebBased A sources are equivalent.
- `python scripts/validate_andino_capabilities.py --runtime-ref andino-workflow`:
  PASS, 58 eval schemas, 60 registry contracts.

## 2. Deterministic routing, installer and procedure tests
- `python -m unittest discover -s tests` (with `PYTHONPATH=src`): 280 tests, OK, 1 skipped.
- Installer from the bundled manifest (local commits exported by the CLI):
  project install for all five hosts INSTALL; repeat install NO_OP; a locally
  edited installed SKILL.md is BLOCKED and the edit is preserved; `everything`
  and `research-skripsi` include natural-writing, `minimal` does not.
- `python scripts/build_release.py --stage-only`: 8 bundles exported.

## 3. Semantic-preservation checks
`scripts/check_semantic_preservation.py` is a bounded safeguard, not a proof of
equal meaning. Its tests cover Rewrite, Write and Review modes, with mutation
fixtures (changed percentage, fabricated citation, edited code, changed DOI)
that FAIL and causality or limitation shifts that return NEEDS_REVIEW.

## 4. Language-quality review
Manager review of the two live rewrites below: claims, statistics, citation,
correlation wording and limitations were preserved. S1 softened "sangat krusial"
to "penting" and said so; S2 removed a generic opening sentence with no
technical claim and reported the removal. Judged acceptable. This is one
reviewer's judgment, not a benchmark.

## 5-6. Native activation and real host execution (LIVE HOST VERIFIED, Claude Code only)
Claude Code 2.1.300, model claude-sonnet-5-5, one disposable project per
scenario with the skill installed by `ai-rules setup` (no global copy existed).
Details, prompts, tool sequences, hashes and outputs: [live-records.json](live-records.json);
inputs: [fixtures](fixtures).

| Scenario | Skill tool call | Fixture unchanged | Checker |
| --- | --- | --- | --- |
| S1 Indonesian academic rewrite | natural-writing | yes | PASS |
| S2 English technical rewrite | natural-writing | yes | PASS |
| S3 Indonesian review only | natural-writing | yes | PASS (review mode) |
| S4 API endpoint (negative) | none | yes | not applicable |

Four scenarios are a smoke check, not broad behavioral proof. Codex, OpenCode,
Antigravity CLI and Antigravity IDE: NOT VERIFIED (files install; no live run).

## 7. Remote installer verification
NOT VERIFIED. Nothing is pushed; `--source latest` cannot resolve
`natural-writing` until the branch exists on origin.
