# Worked example: auditing a testing section

An audit of the "Testing" section of an `AGENTS.md` for a repository with a TypeScript web
app and a Python worker. It shows the findings table, the ledger, the revised section and a
structural check you can adapt to your own revision.

## Before

```markdown
## Testing

Please write good tests and be careful.

1. Run the affected tests before you commit.
2. Write the test first when fixing a bug.
3. Make sure the tests are good.

TypeScript fixtures: build objects with `fromPartial()` from `@total-typescript/shoehorn`,
for example `const user = fromPartial<User>({ id: "u1" })`. Use `fromAny()` only for
deliberately invalid input, for example `fromAny<User>({ id: 123 })`. Keep fixtures next to
the test file as `<name>.fixtures.ts`. Never import fixtures into production code.

Remember: reproduce a bug in a test before you fix it.
```

## Classify and map

The section sits in root guidance, so it loads on every turn. Two branches read it: work in
the TypeScript app and work in the Python worker. The fixture paragraph serves only the
TypeScript branch.

## Findings

| # | Location | Check | Finding (evidence) | Fix | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Opening line | Pruning | "Please write good tests and be careful" asks for default behavior (no-op, hypothesis) | Delete the sentence | fixed |
| 2 | Last line | Pruning | Repeats step 2, "Write the test first when fixing a bug" | Keep step 2, delete the reminder | fixed |
| 3 | Step 3 | Completion criteria | "Make sure the tests are good" has no observable end | Fold a done-when into each remaining step | fixed |
| 4 | Fixture paragraph | Hierarchy | TypeScript-only examples inline; Python work never needs them | Move to `docs/agents/ts-fixtures.md` behind a pointer naming the branch | fixed |
| 5 | Fixture paragraph, last sentence | Wording | "Never import fixtures into production code" has no positive path | In the moved file: "Import fixtures only from test files." | fixed |

## Ledger

| Original rule | Verdict | Where now, or why removed |
| --- | --- | --- |
| Write the test first when fixing a bug | kept | Step 1, with a done-when |
| Reproduce a bug in a test before fixing it | merged | Step 1 (same meaning) |
| Run the affected tests before you commit | kept | Step 2, with a done-when |
| Make sure the tests are good | merged | The done-when of steps 1 and 2 |
| `fromPartial()` for fixtures, `fromAny()` for invalid input, fixtures beside tests | moved | `docs/agents/ts-fixtures.md` |
| Never import fixtures into production code | moved | `docs/agents/ts-fixtures.md`, as "Import fixtures only from test files" |
| Please write good tests and be careful | removed | Asks for default behavior; no-op claim not run |

Not verified: no with/without run checked that agents behave differently after the edit.

## After

```markdown
## Testing

1. When fixing a bug, write a test that reproduces it first; done when that test fails on
   the unfixed code for the reason the bug report gives.
2. Before you commit, run the tests of every package you changed; done when each run exits
   0 with a test count above 0.

- TypeScript fixtures: `docs/agents/ts-fixtures.md`, only for TypeScript tests.
```

## Structural check

The script rebuilds the revised section and checks the properties the audit claims: each
meaning appears once, every step carries a done-when, and the TypeScript material sits
behind one pointer that names its branch. It checks the document, not agent behavior.

```python
import json
import re
from pathlib import Path

# (meaning, wording) for every rule line of the original section.
BEFORE_RULES = [
    ("run-before-commit", "Run the affected tests before you commit."),
    ("test-first", "Write the test first when fixing a bug."),
    ("test-first", "Remember: reproduce a bug in a test before you fix it."),
]
BRANCH = "TS-specific fixture examples"
AFTER = """## Testing

1. When fixing a bug, write a test that reproduces it first; done when that test fails on
   the unfixed code for the reason the bug report gives.
2. Before you commit, run the tests of every package you changed; done when each run exits
   0 with a test count above 0.

- TypeScript fixtures: `docs/agents/ts-fixtures.md`, only for TypeScript tests.
"""

meanings = {meaning for meaning, _ in BEFORE_RULES}
steps = re.findall(r"^\d+\. .*?(?=\n\d+\. |\n\n|\Z)", AFTER, re.M | re.S)
pointers = [line for line in AFTER.splitlines() if line.startswith("- ")]

assert len(steps) == len(meanings), steps
assert all("done when" in step for step in steps), steps
assert len(pointers) == 1 and "only for TypeScript tests" in pointers[0], pointers
assert "fromPartial" not in AFTER, "branch material left in the always-loaded section"

Path("consumer-guide.md").write_text(AFTER, encoding="utf-8")
result = {
    "meanings": len(meanings),
    "duplicate_removed": len(BEFORE_RULES) - len(meanings),
    "branch_reference": BRANCH,
    "live_model_verified": False,
}
Path("result.json").write_text(json.dumps(result), encoding="utf-8")
print(json.dumps(result, sort_keys=True))
```
