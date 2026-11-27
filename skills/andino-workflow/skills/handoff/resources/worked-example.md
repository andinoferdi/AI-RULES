# Worked example: handing an export change to a reviewer

Rina finished a one-line export change and stops for the day. Tomorrow Bayu reviews it in
his own checkout, with his own agent. This example follows the procedure from the boundary
decision to Bayu's first command, then covers two things that go wrong.

## Step 1: the move

The next phase (review) runs in another checkout and with another person, so question 3 of
the boundary table answers yes: a handoff document. Continue fails because the work leaves
this session; a subagent would fit an unattended review here, but Bayu wants to review it
himself.

## Steps 2 to 7: the document

Recipient: Bayu, his own checkout, starting tomorrow; focus: verify the change against the
spec. Rina reruns the check, notes that `changes.diff` is not committed anywhere Bayu can
fetch, and ships it beside the handoff instead of asking him to find it. Commit permission
was not given, so the handoff says so.

## Run the example

The block uses only Python's standard library and writes inside the current working
directory. Read it, then run it in a fresh, disposable directory. The repository's
`scripts/check_andino_matt_methods.py --runtime-root <package>` runs this exact block in a
temporary directory and checks its results independently.

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
    """# Handoff: export status field, for Bayu (his checkout, tomorrow)

Written by Rina. Next session's focus: review the change against the spec.

## Before you start
`changes.diff` exists only on Rina's machine and is shipped next to this file. Check it is
there: `python check_export.py` must print `Export status field present`.
Checked from your side: `ls spec.md changes.diff check_export.py` -> all three present in
the folder that holds this file.

## Read first
- spec.md, section Acceptance: the export exposes a status field.

## Current state and evidence
- Slice implemented; verification pending. The diff renames `state` to `status`.
- `python check_export.py` run by Rina before writing this: passed.

## Decisions that must hold
- The field is named status, because the consumer contract names it. Rejected: keeping
  state with an alias, because the consumer rejects unknown fields.

## Open questions and boundaries
- None open. Out of scope: other export fields.
- The reviewer may run local checks. Permission to commit: false.

## NEXT ACTION
From this directory, run `python check_export.py` to run the accepted public-interface test
for this fixture. Expect `Export status field present`. Then compare changes.diff with the
Acceptance section of spec.md.

## Suggested skills
- Comparing the diff with the spec: andino-code-review, if installed.
- Before calling the review accepted: andino-verification, if installed.
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

## Step 6: check it as Bayu

Read `handoff.md` alone, resolve `spec.md` and `changes.diff` from the directory that holds
it, and run the NEXT ACTION. The output must match the stated signal. The check exercises the
patch fixture only; it says nothing about how a model applies the skill.

## When things go wrong

**The patch is missing.** Copy the folder without `changes.diff` and repeat Bayu's check: the
presence check fails before any review starts. The handoff's first action is then to get the
exact patch from Rina, and the review waits until `python check_export.py` prints the signal.

**The repository moved before Bayu started.** Suppose another commit renamed `export.txt` to
`export.csv` after Rina wrote the handoff. On receipt Bayu compares HEAD with the recorded
commit, finds the rename, applies the patch to the new path, reruns the check and tells Rina
what he adapted. He does not restore the old name to make the handoff literally true.

**The consumer owner has not confirmed the field name.** Then the handoff marks verification
pending and its NEXT ACTION is to get that decision recorded in the Acceptance section; the
review resumes once the section names the field.
