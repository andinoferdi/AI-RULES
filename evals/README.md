# Skill evaluation cases

Each JSON file contains prompts with an expected decision and a forbidden failure signal. `behavior` cases exercise core rules; `negative-trigger` cases probe over-activation. The validator checks case shape and package structure only.

For a live evaluation, give a coding agent the relevant skill and one prompt at a time in a disposable repository. Keep the expected and forbidden fields hidden from that agent. Record the host, skill commit, prompt, relevant fixture state, observed action/output, and reviewer verdict. Compare actual behavior with both fields; do not score wording alone. For negative cases, check whether the skill was invoked unnecessarily. Live execution requires host-specific access and is currently **NOT VERIFIED**.

Run the deterministic check from `main` after fetching the two skill branch refs:

```sh
python3 scripts/validate_skills.py
```

No model provider or third-party Python package is required. The skill branches remain the installed runtime packages; these cases and checks live on `main`.
The metadata checker intentionally supports the current plain-scalar YAML subset; new YAML structures require extending the checker or adding a parser dependency with justification.
