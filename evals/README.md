# Skill evaluation cases

Each JSON file contains prompts with an expected decision and a forbidden failure signal. `behavior` cases exercise core rules; `negative-trigger` cases probe over-activation. The validator checks case shape and package structure only.

For a live evaluation, give a coding agent the relevant skill and one prompt at a time in a disposable repository. Keep the expected and forbidden fields hidden from that agent. Record the host, skill commit, prompt, relevant fixture state, observed action/output, and reviewer verdict. Compare actual behavior with both fields; do not score wording alone. For negative cases, check whether the skill was invoked unnecessarily. Live execution requires host-specific access. Andino and Rescue have no recorded behavioral runs here; Skripsi has historical revision-scoped records. No cross-host behavioral parity is claimed.

The eval files cover `andino-workflow`, `ai-codebase-rescue`, and `skripsi-skill`. Run the deterministic check from `main` after fetching the three skill branch refs:

```sh
python3 scripts/validate_skills.py
```

No model provider or third-party Python package is required. The skill branches remain the installed runtime packages; these cases and checks live on `main`.
The metadata checker supports a plain-string YAML subset; new structures require extending it or justifying a parser dependency. It enforces portable name/description bounds, required README/SKILL files, allowed paths and regular Git file modes. Links are checked, not the truth of prose or live host behavior. The [family standard](../docs/agent-skill-family-standard.md) defines the minimum contract. Andino and Rescue include lifecycle/coexistence regression expectations.

## Skripsi v0.9

`skripsi-skill.json` includes all 110 SRS initial cases and eight supplemental activation/coexistence/integrity/follow-up/authorization cases. `skripsi-fixtures.json` supplies explicitly synthetic context, not real research evidence. The separate supplemental source lets source-case imports preserve the SRS wording. The family audit adds SUP-ACTION-BOUNDARY as NOT_VERIFIED; the previous 117 records retain their historical evidence. Run `python scripts/audit_skripsi_live.py` to check recorded verdict consistency, not to execute or automatically grade behavior.

Optional live execution requires an installed, authenticated Codex CLI. It runs an ephemeral read-only context with only a disposable runtime copy and scenario context; expected/forbidden are not included in its prompt. This is an opt-in host adapter, not a runtime dependency:

```sh
python scripts/run_skripsi_smoke.py --runtime /path/to/skripsi-runtime --case EVAL-035 --output /path/to/result.json
python scripts/run_skripsi_suite.py --runtime /path/to/skripsi-runtime
```

Execution success initially records NOT_VERIFIED, never automatic PASS. Review actual output, relevant tool actions and fixture adequacy against expected and forbidden. One-turn cases cannot alone prove multi-turn follow-up; record that limit and exercise a follow-up separately. Source access is deliberately unavailable in these isolated fixtures, so real database retrieval, institutional compliance and actual empirical analysis remain outside their proof.
