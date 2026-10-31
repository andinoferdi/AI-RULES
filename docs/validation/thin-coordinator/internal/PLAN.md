# Local CSV export and archived state

Plan Depth: LITE
Planning status: DONE — saved planning deliverable; implementation has not started.
Execution status: TODO
Current phase: Phase 1 — local exports
Updated: 2026-10-31

## Objective, current state and authority

Implement the accepted R1–R3 in REQUEST.md: CSV output, archived filtering and
the exact Quickstart replacement. Keep JSON as the default with its existing
shape. R4 is a separate bounded discovery item with an explicitly unready
consumer; it must not hold up local work. This file is the sole checkpoint.

Inspected inputs: export.py, test_export.py, schema.json, README.md,
provider-notes.md, items.json, empty.json and REQUEST.md. All eight matched the
SHA-256 identities in baseline.json at planning time. No application changes or
tests were run. Python 3.11+ and its standard library are the only prerequisites;
no install, external service, package.json or test script is needed.

Existing interfaces and behavior:

- `export.py::load_rows(path: Path) -> list[dict[str, str]]` loads JSON from disk.
- `export.py::main(argv: list[str] | None = None) -> int` requires positional
  `source`, reads the sibling schema.json for `--state` choices, defaults to
  `all`, filters by exact equality, calls `print(json.dumps(rows))`, returns 0.
  The script entrypoint raises SystemExit(main()). Preserve both signatures.
- `schema.json` currently contains `{"states": ["active", "draft"]}`.
- `test_export.py::run_cli(*options)` captures main's stdout against items.json;
  `ExportTests` has test_json_default and test_active_filter.
- items.json contains a/archived with `Tea, "green"`, b/active with an embedded
  LF in `Baris\nbaru`, c/archived with Kopi, d/draft with Draft, in that order.
  empty.json is `[]`. Preserve these source fixtures.
- README.md::Quickstart contains `Use Python 3.11+.` and the exact old command
  specified below. Its command lacks mandatory source; the requested replacement
  also lacks source. Preserve the user's literal replacement rather than silently
  changing CLI positional arguments or adding an extra documentation fix.
- provider-notes.md states that endpoint/schema are unavailable and an authorized
  contract sample must be obtained before consumer design. No credentials exist.

This planning run writes PLAN.md only. The next executor is already authorized
by REQUEST.md to implement local changes after planning; no new approval gate is
required. No commit, push, installation or publication is authorized. Future
remote implementation is explicitly excluded until its contract is available.

On resume, compare relevant current inputs with these anchors and baseline.json.
If bytes or requirements drift, inspect the affected changes, update this plan's
task specification and invalidate only dependent evidence. Preserve unrelated
edits. Do not require chat, historical memory, or a clean Git tree to continue.

## Acceptance and approach

Use stdlib csv.writer, explicit `id,title,state` column order and a header before
all data rows. Add `--format` choices json/csv with default json. Reuse the existing
load/filter flow once, before both renderers. Keep JSON's existing dump expression
and row object shape; CSV projects the three required fields in input order.
Use LF as the writer line terminator. Extend the existing schema enum in place.
No new renderer API, dependency, normalization, remote option or unrelated refactor.

| Requirement / failure case | Owner | Observable proof |
| --- | --- | --- |
| R1 CSV columns, row order, comma/quote/LF roundtrip | T1 | test_csv_all and its literal expected matrix |
| R1 header for empty source and no matches | T1/T2 | test_csv_empty_source / test_no_matches_both_formats |
| R1 omitted/default and explicit JSON retain shape | T1 | test_json_shape plus existing tests |
| R2 archived after draft; active/draft unchanged | T2 | exact schema artifact check; test_state_filters_both_formats |
| R2 all retains every row in order for either renderer | T1/T2 | test_csv_all; test_json_shape; explicit all cases |
| R2 exact, case-sensitive row filtering before either renderer | T2 | test_case_sensitive_rows in both formats |
| R2 invalid state/format still argparse exit 2 | T1/T2 | test_invalid_format / test_invalid_states; stderr invalid-choice check |
| R2 load_rows/main signatures unchanged | T1/T2 | focused source review against inspected signatures above |
| R3 exact README replacement, setup line retained | T3 | Python artifact assertion below; focused content inspection |
| R4 no invented remote implementation | D1/F1 | unresolved provider recorded; F1 waits for verified contract |

## Execution board and dependencies

| Phase / task | Status | Readiness | Depends on | Owned writes |
| --- | --- | --- | --- | --- |
| Phase 1: local export slices | TODO | READY to begin T1 | none | task scopes below |
| T1 CSV and compatible JSON | TODO | READY | none | export.py, test_export.py |
| T2 archived and filter contract | TODO | READY after T1 | T1 | schema.json, test_export.py; export.py only if drift invalidates existing filter |
| T3 exact Quickstart | TODO | READY | none | README.md |
| Phase 2: future provider contract | TODO | D1 ready; F1 unready | none | PLAN.md only until discovery resolves scope |
| D1 bounded provider discovery | TODO | READY to attempt; unavailable evidence may block it | none | PLAN.md |
| F1 published-only remote consumer | TODO | WAITING_ON D1 | D1 | UNKNOWN, deliberately unassigned |

T1 and T2 share test_export.py, so execute them sequentially. T3 has a disjoint
scope and can proceed independently; no worker dispatch is requested. D1/F1 have
no dependency edge into T1–T3. All planned checks below remain NOT RUN. When
execution starts, update the active phase/task status and record actual evidence
beside the task rather than marking planned assertions as completed.

## T1 — CSV through the existing main entrypoint

Status: TODO. Readiness: READY. Requirements: R1, invalid format part of R2.
Depends on: none. Owns export.py imports/main and test_export.py helpers/tests.
Consumes existing load_rows and schema-driven state filter. Produces proposed
`--format {json,csv}` CLI option; no public Python signature changes.

### Change Specification

In export.py imports add `import csv` and `import sys`. In main, alongside the
existing argument declarations, before parse_args, add:

```python
parser.add_argument("--format", choices=("json", "csv"), default="json")
```

Leave required source, schema loading, --state parsing, load_rows and the existing
filter in their current order. Replace only `print(json.dumps(rows))` with:

```python
if args.format == "csv":
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(("id", "title", "state"))
    writer.writerows((row["id"], row["title"], row["state"]) for row in rows)
else:
    print(json.dumps(rows))
```

Keep return 0 and the __main__ guard. Do not print an additional CSV newline or
JSON wrapper. csv.writer owns escaping; do not construct CSV by joining strings.

In test_export.py add `import csv`. Add this proposed helper before run_cli;
replace run_cli's body with delegation, retaining its existing tuple interface:

```python
def run_source_cli(source, *options):
    output, error = io.StringIO(newline=""), io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
        try:
            code = main([str(source), *options])
        except SystemExit as exc:
            code = exc.code
    return code, output.getvalue(), error.getvalue()


def run_cli(*options):
    code, output, _ = run_source_cli(Path(__file__).with_name("items.json"), *options)
    return code, output
```

This captures argparse's real exit behavior so unsupported-format RED is an
assertion about exit status, not a test import/setup failure. Existing tests keep
their original semantics. New test fixtures below are literal independent
expectations. Define these proposed module constants once in test_export.py:

```python
EXPECTED_ROWS = [
    {"id": "a", "title": 'Tea, "green"', "state": "archived"},
    {"id": "b", "title": "Baris\nbaru", "state": "active"},
    {"id": "c", "title": "Kopi", "state": "archived"},
    {"id": "d", "title": "Draft", "state": "draft"},
]
EXPECTED_CSV = [
    ["id", "title", "state"],
    ["a", 'Tea, "green"', "archived"],
    ["b", "Baris\nbaru", "active"],
    ["c", "Kopi", "archived"],
    ["d", "Draft", "draft"],
]
```

Add these methods to ExportTests; preserve existing tests:

```python
def test_csv_all(self):
    for options in [("--format", "csv"), ("--format", "csv", "--state", "all")]:
        with self.subTest(options=options):
            code, output = run_cli(*options)
            self.assertEqual(0, code)
            self.assertEqual(EXPECTED_CSV, list(csv.reader(io.StringIO(output, newline=""))))
            self.assertIn('"Tea, ""green"""', output)
            self.assertIn('"Baris\nbaru"', output)

def test_csv_empty_source(self):
    code, output, _ = run_source_cli(Path(__file__).with_name("empty.json"), "--format", "csv")
    self.assertEqual(0, code)
    self.assertEqual([["id", "title", "state"]], list(csv.reader(io.StringIO(output))))

def test_json_shape(self):
    for options in [(), ("--format", "json"), ("--state", "all")]:
        with self.subTest(options=options):
            code, output = run_cli(*options)
            self.assertEqual(0, code)
            self.assertEqual(EXPECTED_ROWS, json.loads(output))
            self.assertEqual(json.dumps(EXPECTED_ROWS) + "\n", output)

def test_invalid_format(self):
    code, output, error = run_source_cli(Path(__file__).with_name("items.json"), "--format", "yaml")
    self.assertEqual(2, code)
    self.assertEqual("", output)
    self.assertIn("invalid choice", error)
```

### Actions and proof

From repository root (the directory containing export.py), with Python 3.11+:

1. Add helper/constants and test_csv_all only. Run
   `python -m unittest test_export.ExportTests.test_csv_all -v`.
   Expected RED on current source: status 2 differs from 0 because --format is
   unsupported. Confirm argparse reports that missing capability; syntax/import
   failures do not count as the intended RED.
2. Apply T1's production changes; rerun that command. Expected GREEN: both subcases
   pass and parsed row matrix, escaping and order match the literal expectations.
3. Add the other T1 tests individually and run their named unittest commands
   (`python -m unittest test_export.ExportTests.test_csv_empty_source -v`, and
   similarly test_json_shape / test_invalid_format). These regression checks may
   already pass after the first slice; record that honestly rather than invent RED.
4. Run `python -m unittest discover -s . -p test_export.py -v`.
   Expected exit 0, existing and new tests enumerated with no failures/errors.

Mutation sensitivity: in a disposable copy after GREEN, replace csv.writer output
with unescaped comma joining; test_csv_all must fail. Restore/discard the copy.
No refactor is proposed. Result / Evidence: NOT RUN; specified assertions only.

## T2 — Archived schema and exact filtering in both formats

Status: TODO. Readiness: READY after T1. Requirements: R2 and preservation of R1.
Depends on T1, because test helpers/format option are consumed and tests share a
write scope. Owns schema.json and test_export.py. Existing exact filter is reused;
no planned main/load_rows signature change or additional normalization.

### Change Specification

Replace schema.json's states value, preserving key and existing order:

```json
{"states": ["active", "draft", "archived"]}
```

The existing parser expands this list and will accept archived automatically.
Keep `if args.state != "all": rows = [row for row in rows if row["state"] == args.state]`
before the T1 render branch. Do not hardcode a second state list in production.

Add `import tempfile` to test_export.py and these methods to ExportTests:

```python
def test_state_filters_both_formats(self):
    for state, indexes in [("archived", [0, 2]), ("active", [1]), ("draft", [3]), ("all", [0, 1, 2, 3])]:
        for fmt in ("json", "csv"):
            with self.subTest(state=state, fmt=fmt):
                code, output = run_cli("--state", state, "--format", fmt)
                self.assertEqual(0, code)
                if fmt == "json":
                    self.assertEqual([EXPECTED_ROWS[i] for i in indexes], json.loads(output))
                else:
                    self.assertEqual([EXPECTED_CSV[0]] + [EXPECTED_CSV[i + 1] for i in indexes],
                                     list(csv.reader(io.StringIO(output, newline=""))))

def test_case_sensitive_rows(self):
    rows = [{"id": "x", "title": "upper", "state": "Archived"},
            {"id": "y", "title": "lower", "state": "archived"}]
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "rows.json"
        source.write_text(json.dumps(rows), encoding="utf-8")
        for fmt in ("json", "csv"):
            with self.subTest(fmt=fmt):
                code, output, _ = run_source_cli(source, "--state", "archived", "--format", fmt)
                self.assertEqual(0, code)
                if fmt == "json":
                    self.assertEqual([rows[1]], json.loads(output))
                else:
                    self.assertEqual([["id", "title", "state"], ["y", "lower", "archived"]],
                                     list(csv.reader(io.StringIO(output))))

def test_no_matches_both_formats(self):
    # Nonempty real source, but no exact active row; distinguishes filtering from empty loading.
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "rows.json"
        source.write_text('[{"id":"z","title":"only","state":"draft"}]', encoding="utf-8")
        for fmt in ("json", "csv"):
            with self.subTest(fmt=fmt):
                code, output, _ = run_source_cli(source, "--state", "active", "--format", fmt)
                self.assertEqual(0, code)
                if fmt == "json":
                    self.assertEqual([], json.loads(output))
                else:
                    self.assertEqual([["id", "title", "state"]], list(csv.reader(io.StringIO(output))))

def test_invalid_states(self):
    for state in ("Archived", "unknown"):
        with self.subTest(state=state):
            code, output, error = run_source_cli(Path(__file__).with_name("items.json"), "--state", state)
            self.assertEqual(2, code)
            self.assertEqual("", output)
            self.assertIn("invalid choice", error)
```

### Actions and proof

1. After T1 acceptance, add test_state_filters_both_formats, run
   `python -m unittest test_export.ExportTests.test_state_filters_both_formats -v`
   from repository root. Intended RED: archived subcases return 2 instead of 0
   due to schema choices; other states remain valid.
2. Apply the exact schema change; rerun that command to GREEN.
3. Add/run each remaining T2 regression test by its full unittest name. Existing
   exact filtering should already pass after enum expansion; no additional source
   change is needed unless actual observed evidence contradicts the inspected code.
4. Validate static enum: `python -c "import json; from pathlib import Path; assert json.loads(Path('schema.json').read_text())['states'] == ['active', 'draft', 'archived']"`.
5. Run the repository suite command. Expected exit 0 with all existing/T1/T2 tests
   enumerated. Confirm unchanged public function signatures by source inspection.

Mutation sensitivity: in an isolated disposable copy, remove the filter (must fail
test_state_filters_both_formats / test_no_matches_both_formats), then separately
change equality to case-insensitive comparison (must fail test_case_sensitive_rows).
Run each affected named command in that copy, observe assertion failure, then
discard it. Keep the real worktree at GREEN. Result / Evidence: NOT RUN.

## T3 — Exact Quickstart replacement

Status: TODO. Readiness: READY. Requirement: R3. Depends on none. Owns README.md
only. No interface change. Static artifact work; no TDD requirement.

Change Specification: under `## Quickstart`, replace the exact fenced command
line `python export.py --state active` with:

```text
python export.py --state archived --format csv
```

Preserve adjacent `Use Python 3.11+.` and all other content. Do not add a source
argument to this accepted literal, remove source from the CLI, or claim this bare
README command executes successfully. Runtime smoke checks below supply items.json.

Actions: apply that one line replacement; inspect the Quickstart context. From
repository root run this artifact check (exit 0 expected):

```text
python -c "from pathlib import Path; s=Path('README.md').read_text(); assert '## Quickstart' in s; assert 'Use Python 3.11+.' in s; assert 'python export.py --state archived --format csv' in s; assert 'python export.py --state active' not in s"
```

Compare before/after content to confirm only the requested line changed; the
assertions alone do not prove absence of unrelated edits. Result / Evidence: NOT RUN.

## D1 — Bounded remote-provider discovery

Status: TODO. Readiness: READY to attempt discovery. Requirement: R4.
Depends on none. Owns updates to this PLAN.md only. Consumes provider-notes.md and
an authorized provider contract sample, currently UNKNOWN/unavailable. Produces
a verified decision record for F1; not a fictional endpoint, implementation or API.

Action boundary: reread provider-notes.md once. Check whether an authorized,
versioned provider contract/sample has been supplied in the repository. If absent,
record D1 as BLOCKED, name the missing contract/sample, and request that specific
evidence from its owner. Do not search indefinitely, guess an endpoint, obtain
credentials, install a client or make a remote request as part of this plan.
This discovery can finish its bounded attempt without affecting T1–T3.

If an authorized sample becomes available, inspect it to establish endpoint/method,
authentication reference (never embed secrets), response envelope and field types,
published-state definition, pagination/order, failure behavior and a representative
success/error response. Record provenance/version and unresolved fields. Exit to
DONE only when enough verified evidence exists to design the future seam without
inventing behavior. If insufficient, retain BLOCKED with the exact remaining gap.

Before F1 becomes READY, revise F1 here with actual owned paths/symbols, verified
provider/consumer interfaces, exact change blocks, fixture assertions and runnable
commands. A D1 DONE marker alone does not make F1 ready. Network validation and
remote side effects would need actual access/action authority at that future stage.
Result / Evidence: NOT RUN; existing notes establish unavailable endpoint/schema.

## F1 — Future published-only remote consumer (roadmap only)

Status: TODO. Readiness: WAITING_ON D1. Requirement: R4. Depends on D1 only.
Owned files, endpoint, schema, provider signature and published predicate: UNKNOWN.
No implementation change is authorized or specified here. Do not add --published,
provider modules, fake data contracts, external dependencies or guessed schema
fields in T1–T3. Acceptance/test design is intentionally unavailable until D1
provides the contract and this task receives its complete Change Specification.

## Final local integration gate

After T1–T3, from repository root, Python 3.11+:

```text
python -m unittest discover -s . -p test_export.py -v
python export.py items.json --state archived --format csv
python export.py items.json --state archived
python export.py empty.json --format csv
```

Expect suite exit 0 and nonzero enumerated tests. Archived CSV has only a and c
in source order with the exact header and properly escaped Tea title. Archived
JSON is the list of original a/c objects, not a wrapper or column projection.
Empty CSV is header only. Also run the T2 enum and T3 artifact commands.
Inspect the final owned changes for unchanged signatures, fixtures, setup line,
JSON branch and no remote implementation/dependency additions. Record commands,
observed results, runtime and affected content identities here. Only then mark
local tasks/Phase 1 DONE; R4's unresolved future seam stays separate.

## Planning evidence and limitations

Method used: canonical `andino-planning`, activated by permitted read of
`../runtime/andino-workflow/skills/planning/GUIDE.md`; applied its six steps to
source grounding, task-local changes/assertions, dependency ordering, coverage
and fresh-executor review of this file against REQUEST.md and inspected sources.
Loaded mandatory planning resources: `resources/contract.md` and
`resources/worked-example.md`. Also read bundled `skills/tdd/GUIDE.md` and its
`resources/contract.md` to specify later RED/GREEN/public-seam checks; TDD was
not executed. Coordinator reads: SKILL.md, relevant internal-index/routing entries,
method-dispatch.md, invocation-adapter.md, execution-plan.md and anti-loop.md.

Focus is not loaded: this evaluation prohibits outside skills and no permitted
Focus resource was supplied. Concise communication is a direct fallback, not
claimed Focus use. No outside skill/history, sibling fixture, network, Git,
delegation or installation was used. No behavior was exercised; all test results
remain prospective. Planning review cannot establish implementation correctness.
Provider behavior remains unverified and F1 is unready. Initial coordinator read
included REQUEST.md before the planning guide was loaded; application/schema/test
inspection and task drafting occurred after the selected guide/resources read.

## NEXT ACTION

The authorized executor should compare current export.py/test_export.py/schema.json
with the inspected anchors, then add T1's helper/constants and test_csv_all to
test_export.py and run `python -m unittest test_export.ExportTests.test_csv_all -v`
at repository root. Confirm the expected argparse status assertion RED, then
apply T1's specified CSV change and rerun to GREEN. Do not wait for D1/F1.
