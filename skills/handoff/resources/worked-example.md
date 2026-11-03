# Prepare a portable handoff: procedure detail and bounded example

Preserve primary-source pointers when the next phase depends on reasoning that compression could flatten. The ordered context choices are Continue, discard irrelevant context, portable Handoff, bounded delegation, then compaction if needed; this is judgment under host constraints, not mandatory commands. No handoff replaces current Andino task state.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
Path("spec.md").write_text(
    "# Export ticket\n\n## Acceptance\nThe export exposes a status field.\n",
    encoding="utf-8",
)
Path("changes.diff").write_text(
    "--- a/export.txt\n+++ b/export.txt\n@@ -1 +1 @@\n-state\n+status\n",
    encoding="utf-8",
)
Path("check_export.py").write_text(
    "from pathlib import Path\n"
    "assert '+status' in Path('changes.diff').read_text().splitlines()\n"
    "print('Export status field present')\n",
    encoding="utf-8",
)
Path("handoff.md").write_text(
    """# Export ticket handoff

## Resume here

Review the export field change against spec.md, section Acceptance. Start in
the directory containing this handoff. The current phase is verification.

## Current state and evidence

Slice implemented, verification pending. changes.diff contains the exact
proposed change. It is a standalone patch in this fixture.

## Decisions and boundaries

Use the field name status because the consumer contract names it. The reviewer
may run local checks. Permission to commit is false.

## NEXT ACTION

From this directory, run `python check_export.py` to run the accepted public-interface test
for this fixture. Expect `Export status field present`.
""",
    encoding="utf-8",
)
result = {
    "next_action": "run the accepted public-interface test",
    "references": ["spec.md", "changes.diff"],
    "commit_allowed": False,
    "spawned": False,
}
Path("result.json").write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
```

## What the observation establishes

Read `handoff.md` as the recipient, resolve its pointers from the fixture root,
and run the stated command. Compare the observed output with the stated signal.
The check exercises the patch fixture only.

For a blocked assignment, suppose the consumer owner has yet to confirm the
field name. Mark verification pending and make the next action obtaining their
recorded decision in the Acceptance section. Resume the check once that section
contains the confirmed name.

For a cross-host transfer, copy the fixture to another directory and repeat the
recipient check from that root. If `changes.diff` was omitted, record it as missing.
The next action is to obtain the exact patch from the sender and confirm it is
present before running the check.

The deterministic result covers artifact structure and the local recipient
procedure. Model activation, host delegation and human decisions require their
own evidence.
