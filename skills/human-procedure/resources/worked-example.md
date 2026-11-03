# Human procedure stages and worked example

Use these fields in order. Render only fields relevant to the stage.

| Field | What the human needs |
| --- | --- |
| Stage N of M | One outcome, plus account, environment and prerequisites |
| Open and do | Verified URL or command, exact actions and manual-open fallback |
| Input and destination | Field name, source, sensitivity, approved destination and consumer |
| Before confirming | Impact and an affirmative gate for irreversible actions |
| Done when | An observable result that discloses no sensitive values |
| If interrupted | How to check prior effects and where to resume |

End with completed, pending and blocked stages, applied effects by name,
and the first remaining action. For example, if a cutover was submitted and
the dashboard connection dropped, inspect the active target and health signal
before retrying. Resume verification if the new target is active. If the active
target is ambiguous, stop and ask the operator to reconcile it. A dashboard
toggle with no copied value still needs its own completion signal.

## Run the example

Use a fresh disposable directory. The fixture assumes the operator has
confirmed the labels on a fictional dashboard. The `.invalid` address is a
placeholder for this offline exercise. The main repository's
`scripts/check_andino_matt_methods.py --runtime-root <package>` executes the
Python block and checks the generated files. Python standard library only.

```python
from pathlib import Path
import json

stages = [
    ("SERVICE_KEY", True, """> Stage 1 of 2 · Save the test key

Open https://sandbox.example.invalid/settings/keys in the test workspace.
Select API keys → Test → Reveal. Enter SERVICE_KEY privately in your
approved local editor and save it under SERVICE_KEY in .env for the sandbox
client. Keep the editor local and never paste into chat.

Done when the sandbox client's read-only credential check reports success.
If interrupted, run the check first and reuse the saved key if it passes.
"""),
    ("MODE", False, """> Stage 2 of 2 · Confirm test mode

In .env, set MODE=test for the sandbox client. Restart the local client.

Done when its status shows test mode. If it shows production, stop and
check the workspace and config path before retrying.
"""),
]
checklist = "# Configure the sandbox client\n\nNo external writes.\n\n"
checklist += "\n".join(instructions for _, _, instructions in stages)
checklist += "\nAfter both checks pass, report the two statuses only.\n"
Path("manual-steps.md").write_text(checklist, encoding="utf-8")
result = {
    "variables": [name for name, _, _ in stages],
    "secret_names": [name for name, secret, _ in stages if secret],
    "secret_values": [],
    "external_writes": [],
}
Path("result.json").write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
```

## What the observation establishes

The generated checklist has ordered stages, input destinations, a success
signal per stage and a safe restart instruction. The generator writes only
the checklist and its result metadata. The fixture establishes the output
contract for this example. Live dashboard labels, model activation and
interactive wizard execution require separate evidence.
