# Skill evaluation cases

Each JSON file contains prompts with an expected decision and a forbidden failure signal. `behavior` cases exercise core rules; `negative-trigger` cases probe over-activation. The validator checks case shape and package structure only.

For a live evaluation, give a coding agent the relevant skill and one prompt at a time in a disposable repository. Keep the expected and forbidden fields hidden from that agent. Record the host, skill commit, prompt, relevant fixture state, observed action/output, and reviewer verdict. Compare actual behavior with both fields; do not score wording alone. For negative cases, check whether the skill was invoked unnecessarily. Live execution requires host-specific access and is currently **NOT VERIFIED**.

The eval files cover `andino-workflow`, `ai-codebase-rescue`, and `skripsi-skill`. Run the deterministic check from `main` after fetching the three skill branch refs:

```sh
python3 scripts/validate_skills.py
```

No model provider or third-party Python package is required. The skill branches remain the installed runtime packages; these cases and checks live on `main`.
The metadata checker intentionally supports the current plain-scalar YAML subset; new YAML structures require extending the checker or adding a parser dependency with justification.

## Skripsi v0.9

`skripsi-skill.json` includes all 110 SRS initial cases and six supplemental activation/coexistence/integrity cases. `skripsi-fixtures.json` supplies explicitly synthetic context, not real research evidence. The separate supplemental source lets source-case imports preserve the SRS wording.

Optional live execution requires an installed, authenticated Codex CLI. It runs an ephemeral read-only context with only a disposable runtime copy and scenario context; expected/forbidden are not included in its prompt. This is an opt-in host adapter, not a runtime dependency:

```sh
python scripts/run_skripsi_smoke.py --runtime /path/to/skripsi-runtime --case EVAL-035 --output /path/to/result.json
python scripts/run_skripsi_suite.py --runtime /path/to/skripsi-runtime
```

Execution success initially records NOT_VERIFIED, never automatic PASS. Review actual output, relevant tool actions and fixture adequacy against expected and forbidden. One-turn cases cannot alone prove multi-turn follow-up; record that limit and exercise a follow-up separately. Source access is deliberately unavailable in these isolated fixtures, so real database retrieval, institutional compliance and actual empirical analysis remain outside their proof.
