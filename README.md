# AI-RULES development

This branch (`main`) is the repository control plane for validation, evaluation cases, CI, and development notes. It shares Git history with `WebBased` but does not distribute the Web/chat rules or the Agent Skills.

## Distribution branches

| Branch | Contents |
| --- | --- |
| [`WebBased`](https://github.com/andinoferdi/AI-RULES/tree/WebBased) | Web/chat rules and project templates |
| [`andino-workflow`](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow) | Andino Workflow runtime skill |
| [`ai-codebase-rescue`](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue) | AI Codebase Rescue runtime skill |
| [`skripsi-skill`](https://github.com/andinoferdi/AI-RULES/tree/skripsi-skill) | Thesis and research runtime skill |

Install or use a distribution from its own branch. `main` deliberately contains no copy of those runtime packages.

Andino owns lifecycle, execution plans and checkpoints when active. Rescue supplies
engineering rescue methods; Skripsi supplies research methods. Both specialists
work standalone, and installation does not activate Andino or each other. The
[family standard](docs/agent-skill-family-standard.md) defines shared requirements
while preserving their methods. The [initial family audit](docs/validation/agent-skill-family/initial-matrix.md)
and [host evidence](docs/validation/agent-skill-family/host-documentation.md) record
the reviewed baseline and documented host claims.

## Quality checks

The [evaluation cases](evals/README.md) cover expected behavior and cases that should not trigger a skill. The validator reads the three skill branches through Git refs, so fetch those branches before running:

```sh
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
python3 scripts/validate_skripsi_traceability.py
python3 scripts/audit_skripsi_live.py
```

These commands check package structure and evaluation-case format. They do not run live agent behavior. CI runs on pushes and pull requests targeting `main`, manual dispatch, and a daily schedule. Because `main` is the repository default branch, scheduled runs use the latest commit on `main`.

For unpublished runtime commits, use
`python scripts/validate_skills.py --andino-ref andino-workflow --rescue-ref ai-codebase-rescue --skripsi-ref skripsi-skill`
and `python scripts/validate_skripsi_traceability.py --runtime-ref skripsi-skill`.
The live-audit command checks saved evidence consistency without executing a model;
run it locally in addition to CI's package, unit-test and traceability checks.

The [skripsi v0.9 audit](docs/validation/skripsi-skill/contract-review.md) and [requirement inventory](docs/validation/skripsi-skill/traceability.json) distinguish implementation ownership from live behavioral evidence. The [evaluation guide](evals/README.md) describes opt-in isolated execution; CI never invokes a model or incurs live evaluation usage.
