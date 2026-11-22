# Worked Example: CSV Export in One Lane

Internal Andino resource. This is a synthetic runnable example, not a report of a
real agent run. It shows implementation and handoff detail, not a model benchmark.

## 1. Cost decision and ready work

Accepted outcome: inventory listing supports JSON (default) and CSV. CSV quotes
commas, preserves row order and emits only a header for no items. Export is pure:
no persistence, dependency installation or network access.

The task graph has T1 (render CSV/JSON) then T2 (wire the CLI format option).
Both touch the same module/tests. They form one sequential lane. This small case
is cheaper inline: zero agents, zero reviewer start-ups. For the same tasks inside
an already approved larger lane, retain that lane's worker/model. Do not spawn two
workers or a merger simply because two task IDs exist.

Ready brief:
- Spec & Global Constraints: this accepted outcome; JSON remains default.
- Working directory / source: approved checkout, recorded BASE and owned WIP.
- Owned paths: `inventory_example.py`; in a real repo, name its exact test file too.
- Consumed interface: items are ordered dictionaries with string `id` and `name`.
- Produced interface: `main(argv, items, output)` returns 0, writes JSON or CSV.
- T1 acceptance: comma-bearing name round-trips; empty CSV has header only.
- T2 acceptance: CLI selects CSV; absent format selects JSON; invalid format errors.
- Proof: save/run the complete example below with Python 3; all five tests pass.
- Report: agreed plan-specific report path; no commit/push without scoped authority.

## 2. One complete runnable example

The assertions use literal expected rows, not the renderer to calculate its own
expected output. In a real implementation first run each relevant new assertion
against the old behavior and observe the intended failure, then implement it.

Save as `inventory_example.py`, run `python inventory_example.py`:

```python
import argparse
import csv
import io
import json
import unittest


def render(items, format_name, output):
    if format_name == "csv":
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(("id", "name"))
        writer.writerows((row["id"], row["name"]) for row in items)
    else:
        output.write(json.dumps(items) + "\n")


def main(argv, items, output):
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    args = parser.parse_args(argv)
    render(items, args.format, output)
    return 0


class InventoryTests(unittest.TestCase):
    def test_csv_quotes_comma(self):
        output = io.StringIO()
        render([{"id": "1", "name": "Tea, green"}], "csv", output)
        self.assertEqual([["id", "name"], ["1", "Tea, green"]],
                         list(csv.reader(io.StringIO(output.getvalue()))))

    def test_csv_empty_header(self):
        output = io.StringIO()
        render([], "csv", output)
        self.assertEqual("id,name\n", output.getvalue())

    def test_cli_csv_integration(self):
        output = io.StringIO()
        self.assertEqual(0, main(["--format", "csv"],
                                [{"id": "7", "name": "Coffee"}], output))
        self.assertEqual("id,name\n7,Coffee\n", output.getvalue())

    def test_cli_json_default(self):
        output = io.StringIO()
        self.assertEqual(0, main([], [{"id": "7", "name": "Coffee"}], output))
        self.assertEqual([{"id": "7", "name": "Coffee"}],
                         json.loads(output.getvalue()))

    def test_cli_rejects_invalid_format(self):
        import contextlib
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                main(["--format", "xml"], [], io.StringIO())
        self.assertEqual(2, error.exception.code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## 3. Report, parent acceptance and review

A worker's hypothetical short return might say:

```text
Status: DONE_WITH_CONCERNS
Task / lane: export / T1
Content identity: [actual BASE..HEAD or owned snapshot]
Evidence: [actual command, directory, five tests observed; report pointer]
Concerns: downstream command naming still needs confirmation for T2
Report: [absolute agreed report path]
```

Parent first determines whether the concern affects T1. T1's render contract can
be accepted only with current proof; T2 stays NEEDS_CONTEXT until its command is
settled. The worker does not guess an option name or automatically start T2.

Spec review checks quoting, empty output, row order, JSON default and exact option
against code and observed tests. Quality review checks real renderer/CLI wiring
and error behavior. Parent runs the integration cases on the combined current
bytes. A mock-only assertion that render was called cannot prove CSV correctness.

If the reviewer cannot inspect a required CLI result, mark that criterion
UNVERIFIED and obtain focused proof; do not accept it because render tests pass.
This small change needs parent self-review, disclosed as non-independent, rather
than another agent. A larger risk-bearing lane can propose one approved reviewer.

## 4. Recovery without hidden spend

Suppose an authorized lane worker stopped after T1 during a larger plan:
1. Read plan/report and inspect live status plus partial diff. Verify accepted T1
   source/check/environment identity before reusing it.
2. Record T2's exact missing contract and the stopped-worker condition.
3. Resolve discoverable command facts inline. If a real user decision remains,
   ask that single question and continue independent ready work.
4. Present any proposed resume/replacement with count, task, actual model, effort
   and planned review; wait for go-ahead. No automatic new child at round four.
5. Alternatively transfer ownership inline after confirming the worker has
   relinquished it, preserve edits and run the same gates.

At a repair cap, a genuine broken required CLI behavior remains incomplete. A
ruling may defer cosmetic naming; it cannot waive CSV correctness. Keep evidence
and the concrete NEXT ACTION in the plan; no automatic scratch deletion.

[Contract](contract.md) · [Brief/report recipes](subagent-brief-and-report-schemas.md)
· [MIT notices](../references/license.md)
