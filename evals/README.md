# Skill evaluation cases

Each JSON file contains prompts with an expected decision and a forbidden failure signal. `behavior` cases exercise core rules; `negative-trigger` cases probe over-activation. The validator checks case shape and package structure only.

For a live evaluation, give the tested agent the relevant skill and one prompt at a time in an isolated context. Use a disposable repository only when the scenario requires one. Keep expected, forbidden and evaluator conclusions hidden. Materialize scenario fixture facts as raw artifacts/tool evidence; do not give the actor an evaluator's root-cause summary. Record model and host, loaded skill path and commit, prompt, fixture state, observable inspection sequence, questions, changes, verification, output and reviewer verdict. Compare actual behavior with both oracle fields; do not score wording alone. For negative cases, check whether the skill was invoked unnecessarily. Live execution requires host-specific access. Andino's capability records distinguish isolated behavioral runs from MCP service smoke checks; Rescue has no recorded behavioral runs here. Skripsi has historical revision-scoped records. No cross-host behavioral parity is claimed.

The eval files cover `andino-workflow`, `ai-codebase-rescue`, `skripsi-skill`, and `focus`. Run the deterministic check from `main` after fetching the four skill branch refs:

```sh
python3 scripts/validate_skills.py
```

No model provider or third-party Python package is required. The skill branches remain the installed runtime packages; these cases and checks live on `main`.
The metadata checker supports a plain-string YAML subset; new structures require extending it or justifying a parser dependency. It enforces portable name/description bounds, required README/SKILL files, allowed paths and regular Git file modes. Links are checked, not the truth of prose or live host behavior. The [family standard](../docs/agent-skill-family-standard.md) defines the minimum contract. Andino and Rescue include lifecycle/coexistence regression expectations.

## Andino adaptive problem solving

`andino-workflow.json` contains 62 specifications: all 28 adaptive cases preserved,
32 required capability selection/invocation cases and two supplemental cases for
idea-refine and interview-me.
The existing `standard-plan` case now explicitly needs cross-session handoff;
non-trivial reasoning alone does not require persistence. New cases cover diagnosis
contradictions, runtime failures, repository-answerable questions, existing features,
material clarification, daily/casual use, current research, existing capabilities,
cross-feature impact, sufficient-evidence stopping, non-code resume, ephemeral
investigation and limits of a passing local reproduction attempt.

The optional `fixture` field describes scenario setup, not an executed environment.
Prioritize false-user-diagnosis, repository-answerable-question,
material-question-only, explicit-casual-use and explicit-daily-use. Then expand
proportionally if no failure appears. Classify failures as implementation, model,
host, fixture, environment or unknown before changing accepted instructions.
See [integration evidence and next action](../docs/validation/andino-workflow/integration-review.md).

## Andino capability integration

The 32 new cases cover individual Superpowers/Agent Skills and no meta-router
bootstrap, duplicate TDD provenance, conditional Ponytail, targeted memory,
Graphify impact versus native references, UI/Taste coexistence, fidelity cloning,
Anti-Slop concern selection, versioned Context7, Playwright/DevTools boundaries,
native Git versus MCP, Draw.io versus StarUML, Premiere preflight, Cheat Engine
read/permission boundaries, unavailable fallback, rerouting, stopping and simple
zero-specialist work. `capabilities` is evaluator-only identity metadata;
`fixture` describes raw setup, not proof that tools exist.

```sh
python scripts/validate_andino_capabilities.py --cases-only
python scripts/validate_andino_capabilities.py --runtime /path/to/edited-andino-worktree
python scripts/run_andino_capability_eval.py --runtime /path/to/edited-andino-worktree --case debugging-superpowers-route --catalog /path/to/selected-real-skill-catalog.json --output /path/to/record.json
python scripts/run_andino_capability_suite.py --runtime /path/to/edited-andino-worktree --catalog /path/to/selected-real-skill-catalog.json --skip-recorded
```

The catalog is a JSON array of actual `id`, `provider` (UNKNOWN if unresolved),
and `path` to installed SKILL.md directories. This is evaluation input, not an
installer configuration. Supply useful candidate skills plus distractors rather
than telling the actor the expected selection. The runner copies actual permitted
resources into a disposable directory, preserves an exact runtime content hash,
materializes raw local fixtures and captures observable commands/MCP events. It
hides expected/forbidden/capabilities, ignores user CLI config and disables web
search. It uses existing authentication without reading secrets. It does not
expose MCP servers, so positive MCP routing/application coverage remains
NOT_VERIFIED in this adapter; run those cases on a host with actual selected
instruments and safe disposable application fixtures. Global skill metadata may
still be advertised by the CLI; record that host limitation. Model is UNKNOWN if
not exposed in events; never infer it from this parent conversation.

Runner success always leaves NOT_VERIFIED until an explicit reviewer examines
actions, loaded provider, output and oracle. Selection/loading and local reasoning
are separable from a requested implementation or mutation. A negative case may
pass with no specialist invocation; the harness's initial required Andino load
is core setup, not a specialist or an unnecessary investigation tool. Record any
fixture inadequacy rather than grading a missing tool as a successful invocation.
Transport/read smoke records use `scope: smoke` and cannot establish autonomous
routing or cross-host behavior. CI validates structure only and never calls a model.

The recorded 32-case batch belongs to the exact 53-contract runtime hash; the final
55-contract registry adds the two installed Agent Skills extras without changing
prior contracts or other runtime files. Historical evidence audit is explicit:

```sh
python scripts/audit_andino_capability_live.py --runtime /path/to/edited-andino-worktree --allow-historical
```

The [lineage](../docs/validation/andino-workflow/capability-runtime-lineage.json)
must match the current content hash before documented historical records are
accepted. It does not establish latest-runtime or added-route live PASS. Corrected
future fixtures include a disposable Git repository/index without commits, a
memory proposal and a separate library error log. Earlier inadequate fixtures
retain NOT_VERIFIED and are not silently relabeled as successful reruns.

Current Andino runtime samples are recorded separately in the
[current-runtime review](../docs/validation/andino-workflow/current-runtime-review.md):
six completed actors, four scoped PASS and two NOT_VERIFIED. Audit that directory
without `--allow-historical`; missing unsampled cases remain visible.

## Skripsi v0.9

`skripsi-skill.json` includes all 110 SRS initial cases and eight supplemental activation/coexistence/integrity/follow-up/authorization cases. `skripsi-fixtures.json` supplies explicitly synthetic context, not real research evidence. The separate supplemental source lets source-case imports preserve the SRS wording. The family audit adds SUP-ACTION-BOUNDARY as NOT_VERIFIED; the previous 117 records retain their historical evidence. Run `python scripts/audit_skripsi_live.py` to check recorded verdict consistency, not to execute or automatically grade behavior.

Optional live execution requires an installed, authenticated Codex CLI. It runs an ephemeral read-only context with only a disposable runtime copy and scenario context; expected/forbidden are not included in its prompt. This is an opt-in host adapter, not a runtime dependency:

```sh
python scripts/run_skripsi_smoke.py --runtime /path/to/skripsi-runtime --case EVAL-035 --output /path/to/result.json
python scripts/run_skripsi_suite.py --runtime /path/to/skripsi-runtime
```

Execution success initially records NOT_VERIFIED, never automatic PASS. Review actual output, relevant tool actions and fixture adequacy against expected and forbidden. One-turn cases cannot alone prove multi-turn follow-up; record that limit and exercise a follow-up separately. Source access is deliberately unavailable in these isolated fixtures, so real database retrieval, institutional compliance and actual empirical analysis remain outside their proof.
