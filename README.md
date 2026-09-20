# AI-RULES development

This branch (`main`) is the repository control plane for validation, evaluation cases, CI, and development notes. It shares Git history with `WebBased` but does not distribute the Web/chat rules or either Agent Skill.

## Distribution branches

| Branch | Contents |
| --- | --- |
| [`WebBased`](https://github.com/andinoferdi/AI-RULES/tree/WebBased) | Web/chat rules and project templates |
| [`andino-workflow`](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow) | Andino Workflow runtime skill |
| [`ai-codebase-rescue`](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue) | AI Codebase Rescue runtime skill |

Install or use a distribution from its own branch. `main` deliberately contains no copy of those runtime packages.

## Quality checks

The [evaluation cases](evals/README.md) cover expected behavior and cases that should not trigger either skill. The validator reads the two skill branches through Git refs, so fetch those branches before running:

```sh
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

These commands check package structure and evaluation-case format. They do not run live agent behavior. CI is configured for pushes and pull requests targeting `main`, manual dispatch, and a daily schedule. GitHub runs scheduled workflows from the latest commit on the **default branch**; while `WebBased` remains default, the schedule on `main` will not run. Changing the default branch is a separate repository decision.
