# CSV and archived-state export

Status: DONE (R1-R3 local implementation verified; provider discovery remains blocked)
Plan Depth: STANDARD
Current Phase: Local implementation complete
Last Updated: 2026-10-31

## Executive Snapshot

Implement R1-R3 locally with Python 3.11+ and standard-library modules only. R4 is discovery and an explicitly unready future consumer. Another executor is authorized to implement R1-R3 after planning; no new approval gate, commits, pushes, external messages or provider implementation are authorized. This planning session changes only PLAN.md.

Current evidence: executor reread REQUEST.md and every named repository anchor without drift, recorded the pre-edit decision audit in EXECUTION.md, and preserved the original plan byte-for-byte as PLAN-before-execution.md before this first plan update. Baseline passed 2 tests. T1 RED: 6 tests, 3 expected missing-format errors; T1 GREEN: 6 pass. T2 RED: 11 tests, 1 schema failure and 4 archived parser subtest errors; T2 GREEN: 11 pass. Exact README/static interface/filter checks and public CLI smoke passed; final suite passed all 11 tests on 2026-10-31. Commands use Python 3.12 and stdlib only. The supplied planning skill, contract and worked examples were read by the planner; the workflow package was unavailable in this fixture. No material implementation decisions or corrections were invented by the executor.

## Objective and Acceptance Criteria

- [x] R1: `--format csv` emits exactly `id,title,state`, in that order, then source-order rows with correct comma, quote and embedded-newline quoting. Empty filtered output still emits a header. Omitted format and explicit `--format json` keep the existing JSON list-of-dictionaries shape.
- [x] R2: schema states become exactly `["active", "draft", "archived"]`; archived is accepted by the existing schema-driven `--state`. `all` keeps every row; filtering is exact, case-sensitive and occurs before either renderer. Invalid state/format choices exit 2 through argparse. `load_rows(path: Path) -> list[dict[str, str]]` and `main(argv: list[str] | None = None) -> int` remain unchanged.
- [x] R3: README.md::Quickstart changes only `python export.py --state active` to `python export.py --state archived --format csv`; retain the adjacent `Use Python 3.11+.` setup line.
- [x] R4 planning deliverable: bounded provider discovery D1 and a consumer C1 explicitly waiting on it. Do not invent an endpoint, schema, published-state mapping or provider implementation. Missing provider evidence does not block T1-T3.

## Approach, Constraints and Drift

`export.py::main` currently parses a required positional `source`, loads `schema.json` beside the script, builds state choices from `schema["states"]`, loads rows and filters with `row["state"] == args.state`, then prints `json.dumps(rows)`. Keep the loader, filter and JSON branch intact; branch into a standard `csv.writer` only after filtering. No network, dependency or persistence change is needed.

`test_export.py::run_cli(*options)` currently captures stdout and calls main with items.json. ExportTests has two tests checking default row count and active id `b`. items.json contains, in order, ids `a,b,c,d`; `a` has title `Tea, "green"` and state archived, `b` has title `Baris\nbaru` and state active, `c` is archived, `d` is draft. empty.json is `[]`.

README's accepted replacement omits the required source argument, just as its current line does. Preserve the requested exact copy. Execute public-flow verification with `items.json` supplied; do not silently amend the requested README command.

On resume, reread the owned anchors and REQUEST.md before edits. Preserve unrelated changes. If an anchor or interface drifted, update only the affected specifications and dependent tasks here before execution; retain valid evidence. Do not require a clean tree or use git operations. All commands below run from the repository root (directory containing export.py); paths are repository-relative for portability.

## Execution Board

| Task | Status | Readiness | Dependencies | Owned writes | Evidence/result |
| --- | --- | --- | --- | --- | --- |
| T1 CSV/default JSON | DONE | VERIFIED | none | export.py, test_export.py | Expected missing-format RED, then 6 tests pass; final 11 pass |
| T2 archived/exact filtering | DONE | VERIFIED | T1 | schema.json, test_export.py | Expected schema/archived RED, then 11 tests pass |
| T3 Quickstart | DONE | VERIFIED | T2 | README.md | Exact copy/setup checks and public archived CSV smoke pass; final 11 tests pass |
| D1 provider contract discovery | BLOCKED | WAITING_ON authorized sample | none | PLAN.md discovery record | Bounded reread found no sample/reference; endpoint/schema unavailable |
| C1 published-only provider consumer | BLOCKED | WAITING_ON D1 | D1 | Undetermined; do not edit application files | Missing authorized endpoint/schema and published semantics |

Serialize T1 then T2 because both write test_export.py. T3 follows T2 so its documented option has been verified. D1 has no shared application writes and may be considered independently; it does not authorize delegation. Complete the local gate without waiting for D1/C1.

## Coverage

| Requirement/failure case | Owner | Observable check |
| --- | --- | --- |
| R1 headers, row order, comma/quote/newline quoting | T1 | test_csv_rows_and_quoting parses actual CLI stdout to exact three-column rows |
| R1 empty filtered source | T1/T2 | test_csv_empty_source, test_csv_filter_has_no_matches both yield only header |
| R1 omitted/explicit JSON compatibility | T1 | test_json_shapes compares full decoded rows and unchanged json.dumps text |
| R2 archived, active, draft and all; both renderers | T2 | test_state_matrix compares ids/rows for each state and format |
| R2 exact case-sensitive filtering before either renderer | T2 | test_state_case_sensitive excludes a row whose state is `Archived` |
| R2 argparse rejects invalid options | T1/T2 | test_invalid_format and test_invalid_state assert SystemExit.code == 2 |
| R2 schema order/public signatures | T2 | test_schema_states plus signature/source inspection at gate |
| R3 exact copy/setup preserved | T3 | Static assertions below plus public CLI smoke check with source argument |
| R4 uncertainty isolated, no invented consumer | D1/C1 | Evidence record identifies missing fields; C1 stays unready until a verified contract and task-local change/tests are written |

## Detailed Execution

### T1 — CSV rendering with unchanged JSON

Status: DONE. Readiness: VERIFIED. Requirements: R1, R2 invalid-format behavior. Depends on: none.
Owns: export.py imports/main parser/rendering; test_export.py imports/helpers/ExportTests.
Consumes inspected `load_rows` and the existing filtered `rows`; produces proposed CLI `--format {json,csv}`. No new public function or signature.

Change Specification:

1. In export.py imports add `import csv` and `import sys`. In main, immediately after the existing `--state` parser argument, add:

```python
parser.add_argument("--format", choices=("json", "csv"), default="json")
```

2. Replace only `print(json.dumps(rows))` after the existing filter with:

```python
if args.format == "csv":
    writer = csv.writer(sys.stdout, lineterminator="\n", quoting=csv.QUOTE_ALL)
    writer.writerow(("id", "title", "state"))
    writer.writerows((row["id"], row["title"], row["state"]) for row in rows)
else:
    print(json.dumps(rows))
```

Use the standard CSV dialect with explicit LF terminators and QUOTE_ALL. LF avoids doubled carriage returns from Windows stdout translation; quoting every field also preserves standalone carriage returns in titles. Quoted header cells still decode to exactly id/title/state. Write the header outside the row loop, preserve order, and project only the named three keys. Keep return 0, parser error handling, existing filter and loader unchanged. Do not manually join or escape fields.

3. In test_export.py add `import csv`. Introduce proposed helper `run_source(source, *options)` with the same capture pattern currently in run_cli, calling `main([str(source), *options])`; return `(code, output.getvalue())`. Replace run_cli's body with `return run_source(Path(__file__).with_name("items.json"), *options)`. Existing tests stay. This permits real empty.json loading without changing production APIs.
4. Add these concrete tests to ExportTests; io/json/contextlib/Path/main already exist:

```python
def test_csv_rows_and_quoting(self):
    code, output = run_cli("--format", "csv")
    self.assertEqual(0, code)
    self.assertEqual([
        ["id", "title", "state"],
        ["a", 'Tea, "green"', "archived"],
        ["b", "Baris\nbaru", "active"],
        ["c", "Kopi", "archived"],
        ["d", "Draft", "draft"],
    ], list(csv.reader(io.StringIO(output))))
    self.assertIn('"Tea, ""green"""', output)
    self.assertIn('"Baris\nbaru"', output)

def test_csv_empty_source(self):
    code, output = run_source(Path(__file__).with_name("empty.json"), "--format", "csv")
    self.assertEqual(0, code)
    self.assertEqual([["id", "title", "state"]], list(csv.reader(io.StringIO(output))))

def test_json_shapes(self):
    expected = json.loads(Path(__file__).with_name("items.json").read_text(encoding="utf-8"))
    for options in ((), ("--format", "json")):
        with self.subTest(options=options):
            code, output = run_cli(*options)
            self.assertEqual(0, code)
            self.assertEqual(expected, json.loads(output))
            self.assertEqual(json.dumps(expected) + "\n", output)

def test_invalid_format(self):
    with contextlib.redirect_stderr(io.StringIO()):
        with self.assertRaises(SystemExit) as raised:
            run_cli("--format", "xml")
    self.assertEqual(2, raised.exception.code)
```

Actions/proof (Python 3.11+, local fixture files; no install): add tests/helper first. Run `python -m unittest discover -s . -p test_export.py -v`. Expect missing `--format` behavior to fail with argparse SystemExit 2 for CSV/explicit JSON cases; the invalid-format and omitted-JSON cases may already pass. Import/setup/syntax errors are not valid RED evidence. Apply production changes, rerun the same command: all existing/new tests must pass, exit 0. These tests call main and load actual fixtures, exercising the parser → loader → renderer path.

Result / Evidence: Added the exact saved helper and four tests before production edits. `python -B -m unittest discover -s . -p test_export.py -v` produced RED: 6 tests, 3 errors, all argparse SystemExit 2 for missing --format (CSV cases and explicit JSON); baseline and invalid-format checks passed. Applied the saved parser/import/rendering changes without modification. Same command GREEN: 6 tests pass, exit 0. Final integration suite: all 11 tests pass. No source/interface drift or material guesses.

### T2 — Archived schema and exact filtering for both formats

Status: DONE. Readiness: VERIFIED. Requirements: R2, empty filtered R1. Depends on: T1.
Owns: schema.json::states; test_export.py imports/ExportTests. Consumes T1's format option and helper. Existing production filtering already meets the case-sensitive pre-render contract; do not replace it.

Change Specification:

- Replace schema.json's complete current `{"states": ["active", "draft"]}` value with `{"states": ["active", "draft", "archived"]}`. Preserve the order and old states; no new schema shape.
- In test_export.py add `from unittest.mock import patch` and these methods to ExportTests. The matrix uses actual fixture loading; only the mixed-case/no-match probes mock load_rows to isolate exact equality without changing shared fixtures.

```python
def test_schema_states(self):
    schema = json.loads(Path(__file__).with_name("schema.json").read_text(encoding="utf-8"))
    self.assertEqual(["active", "draft", "archived"], schema["states"])

def test_state_matrix(self):
    source = json.loads(Path(__file__).with_name("items.json").read_text(encoding="utf-8"))
    for state, ids in (("all", ["a", "b", "c", "d"]), ("active", ["b"]),
                       ("draft", ["d"]), ("archived", ["a", "c"])):
        expected = [row for row in source if row["id"] in ids]
        for fmt in ("json", "csv"):
            with self.subTest(state=state, fmt=fmt):
                code, output = run_cli("--state", state, "--format", fmt)
                self.assertEqual(0, code)
                if fmt == "json":
                    self.assertEqual(expected, json.loads(output))
                else:
                    self.assertEqual([["id", "title", "state"]] +
                        [[r["id"], r["title"], r["state"]] for r in expected],
                        list(csv.reader(io.StringIO(output))))

def test_state_case_sensitive(self):
    rows = [{"id": "lower", "title": "one", "state": "archived"},
            {"id": "upper", "title": "two", "state": "Archived"}]
    for fmt in ("json", "csv"):
        with self.subTest(fmt=fmt), patch("export.load_rows", return_value=rows):
            code, output = run_cli("--state", "archived", "--format", fmt)
            self.assertEqual(0, code)
            if fmt == "json":
                self.assertEqual([rows[0]], json.loads(output))
            else:
                self.assertEqual([["id", "title", "state"], ["lower", "one", "archived"]],
                                 list(csv.reader(io.StringIO(output))))

def test_csv_filter_has_no_matches(self):
    with patch("export.load_rows", return_value=[{"id": "x", "title": "X", "state": "active"}]):
        code, output = run_cli("--state", "draft", "--format", "csv")
    self.assertEqual(0, code)
    self.assertEqual([["id", "title", "state"]], list(csv.reader(io.StringIO(output))))

def test_invalid_state(self):
    for value in ("Archived", "missing"):
        with self.subTest(value=value), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                run_cli("--state", value)
            self.assertEqual(2, raised.exception.code)
```

Actions/proof: after T1, add the tests and run `python -m unittest discover -s . -p test_export.py -v` from root. Expect test_schema_states to show the missing archived enum and archived parser cases to fail with SystemExit 2. Existing filter probes not requiring archived may already pass. Apply the schema replacement and rerun the same command: all tests pass with nonzero count, exit 0. Inspect export.py to confirm unchanged load_rows/main signatures and the equality filter before both rendering branches. Record command/results here.

Result / Evidence: Added the five exact saved tests and patch import after T1 GREEN. `python -B -m unittest discover -s . -p test_export.py -v` produced RED: 11 tests, one missing-archived schema failure and four expected archived parser errors across matrix/case-sensitive subtests. Applied only the planned schema enum replacement. Same command GREEN: 11 tests pass, exit 0. AST signature checks and source inspection verified unchanged load_rows/main signatures and the original equality filter before both renderer branches.

### T3 — Exact Quickstart replacement and local integration gate

Status: DONE. Readiness: VERIFIED. Requirements: R3 and integrated R1-R2. Depends on: T2.
Owns: README.md::Quickstart only. Interfaces: no code interface change.

Change Specification: in the existing text code fence replace exactly:

```text
python export.py --state active
```

with:

```text
python export.py --state archived --format csv
```

Retain `Use Python 3.11+.` and all surrounding content. No new README sections or source argument correction in this task.

Actions/proof: apply the replacement. From root run the static artifact check:

```text
python -c "from pathlib import Path; t=Path('README.md').read_text(encoding='utf-8'); q=t.split('## Quickstart',1)[1]; assert 'Use Python 3.11+.' in q; assert q.count('python export.py --state archived --format csv') == 1; assert 'python export.py --state active' not in q"
```

Expect exit 0; visually compare the surrounding Quickstart against the inspected original to confirm only that command changed. Run `python export.py items.json --state archived --format csv`: exit 0, decoded header `["id", "title", "state"]`, rows `a` then `c`, proper doubled quotes in the first title, no active/draft rows. Finally run `python -m unittest discover -s . -p test_export.py -v`: every test passes, including existing default JSON/active tests. This is the local release gate; no external services or extra tools. Record observed evidence before marking T1-T3 DONE.

Result / Evidence: Applied the exact one-line README command replacement. Static assertions verified the entire README against its inspected original with only that replacement, the retained setup line, one new command and no old command: exit 0. A subprocess invoked `python -B export.py items.json --state archived --format csv`, exited 0 and decoded to the exact header then rows a,c, including doubled quotes in the first title. Final `python -B -m unittest discover -s . -p test_export.py -v`: 11 tests pass, exit 0. Public interface/filter inspection passed in the same static gate.

### D1 — Resolve the provider evidence boundary

Status: BLOCKED. Readiness: WAITING_ON authorized provider contract sample. Requirements: R4. Depends on: none.
Owns: this PLAN.md discovery record and, on successful discovery, C1's specification. No provider code writes or network calls.

Inspected starting point: provider-notes.md says endpoint/schema unavailable and to obtain an authorized contract sample before designing a consumer; no credentials supplied. Bounded action: reread that file once and inspect any specifically supplied authorized contract sample referenced there or provided with the execution handoff. Do not scan unrelated directories, guess URLs, contact anyone or request credentials. If no sample is supplied, record `D1: BLOCKED — awaiting authorized provider contract sample` and keep C1 BLOCKED; proceed with T1-T3.

Required decision artifact in this plan: exact evidence source/version, endpoint/method, response/row schema and field mapping to export rows, how published-only is selected and what "published" means, ordering/pagination and relevant authentication/error behavior. Distinguish supplied facts from remaining unknowns. An unavailable or contradictory field keeps discovery incomplete. Exit criterion: the authorized sample/documentation answers these consumer decisions and supports concrete fixtures; then rewrite C1 with exact owned files/anchors, decided interfaces/change blocks, failure rules, test fixtures/assertions and runnable verification before marking its readiness READY. D1 DONE alone never readies C1. Contract acquisition outside the provided local evidence requires a later user-supplied artifact or separately authorized action; no provider behavior is inferred here.

Result / Evidence: Bounded follow-up completed on 2026-10-31: reread provider-notes.md once; it supplies no sample or referenced artifact. D1: BLOCKED — awaiting authorized provider contract sample. Exact evidence source is local provider-notes.md (no version supplied). Endpoint/method, row schema/field mapping, published selection/meaning, ordering/pagination, authentication and errors remain unknown. C1 remains BLOCKED/WAITING_ON D1; no consumer writes or inferred provider facts. R4 planning boundary is satisfied; local T1-T3 are complete.

### C1 — Future published-only provider export (roadmap)

Status: BLOCKED. Readiness: WAITING_ON D1. Requirements: future consumer in R4. Depends on: D1.
Blocker: no authorized remote endpoint/schema or published-selection contract. Files/interfaces, implementation, tests and commands are intentionally unresolved; do not create a provider module, CLI option or schema state. D1 must first populate a complete task-local Change Specification and proof in this plan. Implementation of this future consumer is outside the current authorization; a resolved plan does not itself authorize it.

## Handoff Review and Completion Rules

The local path is executable from repository files plus this plan: exact parser/renderer/schema/copy changes, fixture assertions, serial ownership and root commands are specified. All accepted local outcomes map to checks. The provider consumer is explicitly unready. Tests above are planned evidence, distinct from the two-test baseline actually run. No provider validation is possible with current evidence.

During execution update this board and matching task status together; use TODO, IN_PROGRESS, BLOCKED, DONE or SKIPPED. Mark DONE only after its acceptance and integration evidence. Local completion means T1-T3 pass the final gate; R4's planning requirement is satisfied by this bounded discovery and blocked consumer, not by pretending remote export exists.

## NEXT ACTION

No local implementation work remains. Await a user-supplied authorized provider contract sample for D1; do not implement C1 under the current authorization. T1-T3 and their integrated gate are DONE. EXECUTION.md records the blind executor audit/actions; PLAN-before-execution.md preserves the unmodified received plan.
