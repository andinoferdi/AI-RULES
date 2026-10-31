# CSV and archived-state export

Status: IN_PROGRESS (planning complete; implementation not started)
Plan Depth: STANDARD
Current Phase: Local implementation, T1 next
Last Updated: 2026-10-31

## Executive Snapshot

Implement R1-R3 locally with Python 3.11+ and standard-library modules only. R4 is discovery and an explicitly unready future consumer. Another executor is authorized to implement R1-R3 after planning; no new approval gate, commits, pushes, external messages or provider implementation are authorized. This planning session changes only PLAN.md.

Current evidence: inspected REQUEST.md, export.py, test_export.py, schema.json, README.md, items.json, empty.json and provider-notes.md. `python -B -m unittest discover -s . -p test_export.py -v` passed both existing tests on 2026-10-31. No new behavior has been implemented or verified. The supplied planning skill, contract and worked examples were read; the workflow package is unavailable in this fixture, so its canonical lifecycle/TDD guides were not loaded. This document preserves essential state, authority, readiness and handoff fields directly.

## Objective and Acceptance Criteria

- [ ] R1: `--format csv` emits exactly `id,title,state`, in that order, then source-order rows with correct comma, quote and embedded-newline quoting. Empty filtered output still emits a header. Omitted format and explicit `--format json` keep the existing JSON list-of-dictionaries shape.
- [ ] R2: schema states become exactly `["active", "draft", "archived"]`; archived is accepted by the existing schema-driven `--state`. `all` keeps every row; filtering is exact, case-sensitive and occurs before either renderer. Invalid state/format choices exit 2 through argparse. `load_rows(path: Path) -> list[dict[str, str]]` and `main(argv: list[str] | None = None) -> int` remain unchanged.
- [ ] R3: README.md::Quickstart changes only `python export.py --state active` to `python export.py --state archived --format csv`; retain the adjacent `Use Python 3.11+.` setup line.
- [ ] R4 planning deliverable: bounded provider discovery D1 and a consumer C1 explicitly waiting on it. Do not invent an endpoint, schema, published-state mapping or provider implementation. Missing provider evidence does not block T1-T3.

## Approach, Constraints and Drift

`export.py::main` currently parses a required positional `source`, loads `schema.json` beside the script, builds state choices from `schema["states"]`, loads rows and filters with `row["state"] == args.state`, then prints `json.dumps(rows)`. Keep the loader, filter and JSON branch intact; branch into a standard `csv.writer` only after filtering. No network, dependency or persistence change is needed.

`test_export.py::run_cli(*options)` currently captures stdout and calls main with items.json. ExportTests has two tests checking default row count and active id `b`. items.json contains, in order, ids `a,b,c,d`; `a` has title `Tea, "green"` and state archived, `b` has title `Baris\nbaru` and state active, `c` is archived, `d` is draft. empty.json is `[]`.

README's accepted replacement omits the required source argument, just as its current line does. Preserve the requested exact copy. Execute public-flow verification with `items.json` supplied; do not silently amend the requested README command.

On resume, reread the owned anchors and REQUEST.md before edits. Preserve unrelated changes. If an anchor or interface drifted, update only the affected specifications and dependent tasks here before execution; retain valid evidence. Do not require a clean tree or use git operations. All commands below run from the repository root (directory containing export.py); paths are repository-relative for portability.

## Execution Board

| Task | Status | Readiness | Dependencies | Owned writes | Evidence/result |
| --- | --- | --- | --- | --- | --- |
| T1 CSV/default JSON | TODO | READY | none | export.py, test_export.py | Existing 2-test baseline passes; new checks not run |
| T2 archived/exact filtering | TODO | READY after T1 | T1 | schema.json, test_export.py | Source/filter inspected; new checks not run |
| T3 Quickstart | TODO | READY after T2 | T2 | README.md | Exact old line inspected; replacement not applied |
| D1 provider contract discovery | TODO | READY for bounded evidence check | none | PLAN.md discovery record | provider-notes.md says endpoint/schema unavailable |
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

Status: TODO. Readiness: READY. Requirements: R1, R2 invalid-format behavior. Depends on: none.
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

Result / Evidence: Planned only; no T1 checks run.

### T2 — Archived schema and exact filtering for both formats

Status: TODO. Readiness: READY after T1 acceptance. Requirements: R2, empty filtered R1. Depends on: T1.
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

Result / Evidence: Planned only; no T2 checks run.

### T3 — Exact Quickstart replacement and local integration gate

Status: TODO. Readiness: READY after T2 acceptance. Requirements: R3 and integrated R1-R2. Depends on: T2.
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

Result / Evidence: Planned only; no T3 checks run.

### D1 — Resolve the provider evidence boundary

Status: TODO. Readiness: READY for discovery only. Requirements: R4. Depends on: none.
Owns: this PLAN.md discovery record and, on successful discovery, C1's specification. No provider code writes or network calls.

Inspected starting point: provider-notes.md says endpoint/schema unavailable and to obtain an authorized contract sample before designing a consumer; no credentials supplied. Bounded action: reread that file once and inspect any specifically supplied authorized contract sample referenced there or provided with the execution handoff. Do not scan unrelated directories, guess URLs, contact anyone or request credentials. If no sample is supplied, record `D1: BLOCKED — awaiting authorized provider contract sample` and keep C1 BLOCKED; proceed with T1-T3.

Required decision artifact in this plan: exact evidence source/version, endpoint/method, response/row schema and field mapping to export rows, how published-only is selected and what "published" means, ordering/pagination and relevant authentication/error behavior. Distinguish supplied facts from remaining unknowns. An unavailable or contradictory field keeps discovery incomplete. Exit criterion: the authorized sample/documentation answers these consumer decisions and supports concrete fixtures; then rewrite C1 with exact owned files/anchors, decided interfaces/change blocks, failure rules, test fixtures/assertions and runnable verification before marking its readiness READY. D1 DONE alone never readies C1. Contract acquisition outside the provided local evidence requires a later user-supplied artifact or separately authorized action; no provider behavior is inferred here.

Result / Evidence: Provider endpoint/schema unavailable as recorded in provider-notes.md; bounded follow-up not performed. This is a deliberate R4 boundary, not a local implementation blocker.

### C1 — Future published-only provider export (roadmap)

Status: BLOCKED. Readiness: WAITING_ON D1. Requirements: future consumer in R4. Depends on: D1.
Blocker: no authorized remote endpoint/schema or published-selection contract. Files/interfaces, implementation, tests and commands are intentionally unresolved; do not create a provider module, CLI option or schema state. D1 must first populate a complete task-local Change Specification and proof in this plan. Implementation of this future consumer is outside the current authorization; a resolved plan does not itself authorize it.

## Handoff Review and Completion Rules

The local path is executable from repository files plus this plan: exact parser/renderer/schema/copy changes, fixture assertions, serial ownership and root commands are specified. All accepted local outcomes map to checks. The provider consumer is explicitly unready. Tests above are planned evidence, distinct from the two-test baseline actually run. No provider validation is possible with current evidence.

During execution update this board and matching task status together; use TODO, IN_PROGRESS, BLOCKED, DONE or SKIPPED. Mark DONE only after its acceptance and integration evidence. Local completion means T1-T3 pass the final gate; R4's planning requirement is satisfied by this bounded discovery and blocked consumer, not by pretending remote export exists.

## NEXT ACTION

At repository root, check T1's export.py/test_export.py anchors for drift, add T1's helper and four tests to test_export.py, then run `python -m unittest discover -s . -p test_export.py -v` and record the expected missing-format RED before changing export.py. Another executor already has authorization for this local implementation; no new approval step is required.
