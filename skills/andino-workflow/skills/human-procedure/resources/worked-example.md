# Worked example: a two-stage sandbox procedure

The stage fields, layouts and script requirements live in the
[stage contract](stage-contract.md). This example applies them to the smallest useful case:
one secret and one setting for a local sandbox client, delivered as a checklist because there
are two short stages and no remote write.

How the gates shaped it:

1. Scope: `.env.example` lists `SERVICE_KEY` and `MODE`; no CI workflow reads them. Value map:
   `SERVICE_KEY` from the sandbox dashboard, secret, written to `.env`, read by the sandbox
   client; `MODE` typed by the person, public, written to `.env`, read by the same client.
2. What already happened: `.env` may already hold a key from an earlier try, so each stage
   starts with the client's read-only credential check and reuses a saved key that passes.
3. Journey: the operator confirmed the dashboard labels (API keys → Test → Reveal); nothing is
   marked unconfirmed.
4. Artifact: a checklist; two stages and no value the agent must route.
5. Stages: each has Open, Do, Enter, Done when and If interrupted; neither has a hard-to-undo
   effect, so neither needs a typed word.

A cutover differs in gate 2. If a DNS change was submitted and the session dropped, the first
stage reads the record and the health signal before anything else: the new target is active,
skip to verification; still the old target, continue; anything else, stop and ask the operator
to reconcile it. A dashboard toggle with no copied value still gets its own Done when.

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
