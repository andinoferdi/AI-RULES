# Worked planning examples

These synthetic fixtures demonstrate plan construction, not actual repository
inspection or completed implementation. Paths, signatures and commands are stated
scenario inputs. Real plans derive them from the target repository. Planned
assertions below are not reported test results.

## STANDARD: two complete CLI capabilities

Scenario: a Python inventory CLI already has `inventory/cli.py::main(argv:
list[str]) -> int`, `inventory/store.py::list_items() -> list[dict[str, str]]`
and `tests/test_cli.py`, whose `run_cli(argv, items)` returns `(exit_code, stdout)`
while patching `inventory.cli.list_items` to return `items`.
Store fixtures contain `[{"id": "1", "name": "Tea, green"}]`; an empty fixture
returns `[]`. JSON listing already exists. Tests use standard-library unittest.
`cli.py` imports argparse/json, uses `subparsers.add_parser('list')` in main,
and after `args = parser.parse_args(argv)` calls `print(json.dumps(list_items()))`
then returns 0. The accepted request adds CSV export and an optional exact-name
filter for either format. The
existing checkpoint is reused; publication has not been authorized.

````markdown
# Inventory export
Status: IN_PROGRESS
Plan Depth: STANDARD
Current Phase: Phase 1 — CSV export
Last Updated: 2026-10-30

## Executive Snapshot
Accepted: CSV output and exact-name filtering; existing JSON remains default.
Inspected scenario interfaces are listed above. No implementation or tests run.
T1 establishes CSV; T2 adds filtering. Shared CLI/test writes are sequential.

## Objective
Export inventory through the existing CLI with correct quoting and optional filtering.

## Acceptance Criteria
- [ ] R1: `list --format csv` emits `id,name` followed by current rows using CSV quoting.
- [ ] R2: Empty CSV emits only the header; default JSON preserves its existing behavior.
- [ ] R3: `list --format csv --name NAME` emits exact matches, or just the header if none.

## Approach and Constraints
Use the existing CLI/store boundary and Python csv.writer; add no dependency.
Filter returned rows before rendering. JSON options/behavior remain compatible.
No persistence or public store-interface change. No commit/push authorization.

## Execution Board
| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — CSV export | IN_PROGRESS | R1/R2 through CLI | cli.py, test_cli.py | Scenario interface inspection; implementation not run |
| Phase 2 — Name filter | TODO | R3 through CLI | same files after T1 | Not run |

## Coverage
| Requirement / failure case | Task | Check |
| --- | --- | --- |
| R1 and comma in name | T1 | csv.reader(output) == [['id','name'],['1','Tea, green']] |
| R2 empty CSV | T1 | csv.reader(output) == [['id','name']] |
| R2 existing JSON | T1/T2 gate | existing JSON regression tests still pass |
| R3 match / missing name | T2 | exact row for 'Tea, green'; header only for 'Coffee' |

## Detailed Execution

### Phase 1 — CSV export
Status: IN_PROGRESS

#### T1 — Export current inventory as CSV
Status: TODO
Readiness: READY
Requirements: R1, R2
Depends on: none
Owns: Modify inventory/cli.py::main; Test tests/test_cli.py
Interfaces: consumes inspected list_items() -> list[dict[str,str]];
produces proposed CLI option `list --format csv`; existing main signature unchanged.

Acceptance: exact parsed rows above, exit 0; empty store yields header only.

Change Specification:
- `inventory/cli.py` imports: add `import csv` and `import sys`.
- `main` parser setup: replace `subparsers.add_parser('list')` with:

```python
list_parser = subparsers.add_parser('list')
list_parser.add_argument('--format', choices=('json', 'csv'), default='json')
```

- `main` rendering: replace the existing `print(json.dumps(list_items()))`
  with the following. Keep argument parsing, main signature and final return 0.

```python
rows = list_items()
if args.format == 'csv':
    writer = csv.writer(sys.stdout, lineterminator='\n')
    writer.writerow(('id', 'name'))
    writer.writerows((row['id'], row['name']) for row in rows)
else:
    print(json.dumps(rows))
```

- `tests/test_cli.py`: add `import csv` and `import io` if absent; add the two
  unittest methods below to the existing CLI test class. Existing JSON tests remain.

```python
def test_csv_quotes_name(self):
    code, output = run_cli(['list', '--format', 'csv'],
                           [{'id': '1', 'name': 'Tea, green'}])
    self.assertEqual(0, code)
    self.assertEqual([['id', 'name'], ['1', 'Tea, green']],
                     list(csv.reader(io.StringIO(output))))

def test_csv_empty(self):
    code, output = run_cli(['list', '--format', 'csv'], [])
    self.assertEqual(0, code)
    self.assertEqual([['id', 'name']], list(csv.reader(io.StringIO(output))))
```

Actions:
- [ ] Add test_csv_quotes_name and test_csv_empty using existing run_cli/store fixtures.
      Parse stdout with csv.reader; assert the literal rows in Coverage and exit 0.
- [ ] Run `python -m unittest discover -s tests -p test_cli.py -v` at repository root.
      Expect CSV-option/output assertions to fail; fix broken test setup separately.
- [ ] Apply T1's parser, imports and rendering replacements in main.
      Preserve the list_items interface and default JSON output.
- [ ] Rerun the focused command; expect new and existing CLI assertions PASS, exit 0.

Verification prerequisites: repository's supported Python; existing test fixtures.
Integration gate: CLI tests invoke main and the existing store fixture, asserting
stdout and status, rather than checking only a rendering helper.
Result / Evidence: Not run — planned checks only.

### Phase 2 — Name filter
Status: TODO

#### T2 — Export only exact-name matches
Status: TODO
Readiness: READY after T1 acceptance
Requirements: R3; preserve R1/R2
Depends on: T1
Owns: Modify inventory/cli.py::main; Test tests/test_cli.py (serialize after T1)
Interfaces: consumes T1's CSV option; produces proposed `--name NAME` list option.

Acceptance: 'Tea, green' retains row 1; 'Coffee' emits only header, both exit 0.

Change Specification:
- `inventory/cli.py::main`, after T1's format argument: add
  `list_parser.add_argument('--name', default=None)`.
- Immediately after `rows = list_items()`, before either renderer, insert:

```python
if args.name is not None:
    rows = [row for row in rows if row['name'] == args.name]
```

  Matching is case-sensitive equality with no trimming; omitted --name keeps all
  rows. Filtering before rendering also applies to JSON. No new helper/store API.
- `tests/test_cli.py`, existing test class: use these decisive cases with run_cli.
  Add the JSON case to preserve the shared filter contract.

```python
def test_csv_name_match(self):
    code, output = run_cli(['list', '--format', 'csv', '--name', 'Tea, green'],
                           [{'id': '1', 'name': 'Tea, green'},
                            {'id': '2', 'name': 'tea, green'}])
    self.assertEqual(0, code)
    self.assertEqual([['id', 'name'], ['1', 'Tea, green']],
                     list(csv.reader(io.StringIO(output))))

def test_csv_name_missing(self):
    code, output = run_cli(['list', '--format', 'csv', '--name', 'Coffee'],
                           [{'id': '1', 'name': 'Tea, green'}])
    self.assertEqual(0, code)
    self.assertEqual([['id', 'name']], list(csv.reader(io.StringIO(output))))

def test_json_name_match(self):
    items = [{'id': '1', 'name': 'Tea, green'}, {'id': '2', 'name': 'Coffee'}]
    code, output = run_cli(['list', '--name', 'Coffee'], items)
    self.assertEqual(0, code)
    self.assertEqual([items[1]], json.loads(output))
```

Actions:
- [ ] Add test_csv_name_match and test_csv_name_missing using the literal cases above.
- [ ] Run `python -m unittest discover -s tests -p test_cli.py -v` at repository root;
      expect assertions for missing filter behavior to fail.
- [ ] Apply T2's argument and filter insertion at the named anchors.
- [ ] Rerun focused tests, then `python -m unittest discover -s tests -v` at repository
      root; expect nonzero test count, all assertions PASS, exit 0, including existing JSON.

Verification prerequisites: T1 accepted; same Python/test setup.
Result / Evidence: Not run — planned checks only.

## NEXT ACTION
Review the saved plan. Implementation awaits authorization because this scenario
requested a plan only; once authorized, add T1's two cases in tests/test_cli.py,
run the focused CLI command and inspect RED.
````

The example fixes boundary decisions (standard CSV quoting and exact matching),
shows what code changes, states assertions, names dependencies and preserves the
real entrypoint. The short branch bodies carry actual decisions; the parser,
fixture machinery and store are not copied wholesale. Neither task is
an isolated database/service/UI layer. A necessary shared foundation would be
valid if its own check and named consumer justified it.

## LITE: static artifact, no TDD ceremony

Scenario: the user requests a short saved plan to repair one inspected README
command. `README.md` says `python app.py`; inspected `pyproject.toml` declares
the supported entrypoint `inventory = inventory.cli:main`.

```markdown
# Correct the quickstart
Status: TODO
Plan Depth: LITE
Current State: inspected README command disagrees with the declared entrypoint.
Objective / Acceptance: quickstart uses `inventory --help`; adjacent setup steps remain accurate.
Constraints: documentation only; preserve unrelated edits; no commit authorization.
Readiness: READY
Change Specification: README.md::Quickstart, replace the exact code-fence line
`python app.py` with `inventory --help`. Do not change the surrounding setup commands.
Actions: apply that replacement; inspect the diff against pyproject.toml.
Verification: from repo root run `git diff --check` (exit 0), then review
`git diff -- README.md` for exactly the intended command change. Runtime help
is unverified unless the installed entrypoint is available and exercised.
NEXT ACTION: edit the inspected README command, then inspect the focused diff.
```

## Discovery before dependent implementation

If a requested export must stream millions of rows but the store's streaming API
is unknown, add D1: inspect the store implementation and a bounded representative
memory experiment; produce the verified iterator/error contract or evidence that
the requirement needs a different approach. The streaming task depends on D1.
Mark the consumer `Readiness: WAITING_ON D1`; do not invent `stream_items()`.
D1 can be READY if its inspection/experiment and success criterion are specified.
After D1 succeeds, write the verified iterator signature, error/close semantics,
exact consumer edit and discriminating test into the dependent task, then reassess
readiness. D1's DONE marker alone does not supply implementation instructions.
Keep unrelated authorized work moving. Ask only if the findings change
a user-owned requirement or exceed existing authority.

## Failure patterns caught by self-review

| Failure | Repair |
| --- | --- |
| Milestone says "restore About geometry" with a file directory and acceptance | Keep it a roadmap until inspected selectors, decided formula/values, concrete code/CSS change and check are written into tasks. |
| Ready task says "implement the API" or "follow existing patterns" | Specify file/symbol, operation, exact interface/literals and decision-bearing change block; name the actual pattern and differences. |
| Precise snippet still edits a removed symbol or contradicts the spec | Reconcile with current source/accepted requirements before execution; log the bounded correction and update consumers. |
| Goal promises crash recovery; tasks only add a table and route | Add the recovery task and fault-condition proof, or narrow scope with an authorized decision. |
| Test calls a helper while acceptance concerns a complete mutation | Exercise the public operation and observe both side effects, including rollback. |
| Five speculative risks inflate a tiny document fix | Keep the relevant artifact check; no quota. |
| 'Handle errors' / 'tests pass' leaves behavior undecided | Give the input, expected output/state, named assertion and actual command. |
| One-task plan contains the entire implementation | Keep boundary decisions, fixtures and assertions; let executor write routine bodies. |
| Planning automatically commits or asks again despite authorization | Respect existing authority and record a useful boundary only when applicable. |

## Evidence limits

Review can establish that this artifact covers its stated requirements and has
coherent ownership/dependencies. Running fixture checks establishes only those
checks. Claiming consistently better AI output requires repeated independent
consumer evaluations; a schema pass or one favorable sample cannot establish it.
