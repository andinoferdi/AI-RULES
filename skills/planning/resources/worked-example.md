# Worked planning examples

These synthetic fixtures demonstrate plan construction, not actual repository
inspection or completed implementation. Paths, signatures and commands are stated
scenario inputs. Real plans derive them from the target repository. Planned
assertions below are not reported test results.

## STANDARD: two complete CLI capabilities

Scenario: a Python inventory CLI already has `inventory/cli.py::main(argv:
list[str]) -> int`, `inventory/store.py::list_items() -> list[dict[str, str]]`
and `tests/test_cli.py`, whose `run_cli(argv)` captures stdout and exit status.
Store fixtures contain `[{"id": "1", "name": "Tea, green"}]`; an empty fixture
returns `[]`. JSON listing already exists. Tests use standard-library unittest.
The accepted request adds CSV export and an optional exact-name filter. The
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
Requirements: R1, R2
Depends on: none
Owns: Modify inventory/cli.py::main; Test tests/test_cli.py
Interfaces: consumes inspected list_items() -> list[dict[str,str]];
produces proposed CLI option `list --format csv`; existing main signature unchanged.

Acceptance: exact parsed rows above, exit 0; empty store yields header only.
Actions:
- [ ] Add test_csv_quotes_name and test_csv_empty using existing run_cli/store fixtures.
      Parse stdout with csv.reader; assert the literal rows in Coverage and exit 0.
- [ ] Run `python -m unittest discover -s tests -p test_cli.py -v` at repository root.
      Expect CSV-option/output assertions to fail; fix broken test setup separately.
- [ ] Add the csv format option and csv.writer rendering in main's list branch.
      Preserve existing JSON branch and list_items interface.
- [ ] Rerun the focused command; expect new and existing CLI assertions PASS, exit 0.

Verification prerequisites: repository's supported Python; existing test fixtures.
Integration gate: CLI tests invoke main and the existing store fixture, asserting
stdout and status, rather than checking only a rendering helper.
Result / Evidence: Not run — planned checks only.

### Phase 2 — Name filter
Status: TODO

#### T2 — Export only exact-name matches
Status: TODO
Requirements: R3; preserve R1/R2
Depends on: T1
Owns: Modify inventory/cli.py::main; Test tests/test_cli.py (serialize after T1)
Interfaces: consumes T1's CSV option; produces proposed `--name NAME` list option.

Acceptance: 'Tea, green' retains row 1; 'Coffee' emits only header, both exit 0.
Actions:
- [ ] Add test_csv_name_match and test_csv_name_missing using the literal cases above.
- [ ] Run `python -m unittest discover -s tests -p test_cli.py -v` at repository root;
      expect assertions for missing filter behavior to fail.
- [ ] Filter current rows by exact name before rendering; omitted --name retains all rows.
- [ ] Rerun focused tests, then `python -m unittest discover -s tests -v` at repository
      root; expect nonzero test count, all assertions PASS, exit 0, including existing JSON.

Verification prerequisites: T1 accepted; same Python/test setup.
Result / Evidence: Not run — planned checks only.

## NEXT ACTION
Review the saved plan. Implementation awaits authorization because this scenario
requested a plan only; once authorized, add T1's two cases in tests/test_cli.py,
run the focused CLI command and inspect RED.
````

The example fixes a boundary decision (standard CSV quoting), states exact
assertions, names dependencies and preserves the real entrypoint. Neither task is
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
Actions: replace the one command in README.md; inspect the diff against pyproject.toml.
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
Its readiness is discovery's accepted artifact, not an invented `stream_items()`
signature. Keep unrelated authorized work moving. Ask only if the findings change
a user-owned requirement or exceed existing authority.

## Failure patterns caught by self-review

| Failure | Repair |
| --- | --- |
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
