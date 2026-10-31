# Preflight before implementation

Scope: inspect the supplied PLAN.md against REQUEST.md and current fixture source, using ../execution-skill/SKILL.md and resources/contract.md. No application, schema, tests, README or PLAN edits were made. This report is the bounded evaluation deliverable; PLAN.md remains the execution checkpoint and needs the corrections below before T1 starts.

## Evidence and identity

- Inspected PLAN.md, REQUEST.md, export.py, schema.json, test_export.py, README.md, items.json, empty.json, provider-notes.md and baseline.json in this fixture only.
- Python 3.12.10. At fixture root, `python -m unittest discover -s . -p test_export.py -v` exited 0: both existing tests passed (JSON default and active filter). These two tests do not establish R1/R2 acceptance.
- SHA-256 comparison against baseline.json matched all eight recorded files: export.py, test_export.py, items.json, empty.json, schema.json, README.md, provider-notes.md and REQUEST.md. No source drift from this supplied baseline was observed. PLAN.md has no recorded baseline identity and no completed implementation evidence to reuse.
- No git, network, delegation, provider access or implementation edits were used.

## Readiness before edits

| Task | Verdict | Reason |
| --- | --- | --- |
| T1 CSV and archived state | NOT READY as written; locally correctable | render_rows does not exist; args is local to main; schema replacement removes active; acceptance tests omit material R1/R2 cases. Exact corrections below make this task actionable without user input. |
| T2 Quickstart | READY | The exact old command occurs once in README.md::Quickstart. Replace it exactly as R3 requires and retain `Use Python 3.11+.` and all surrounding bytes. No implementation dependency is needed for this textual change. |
| Required R4 discovery task (absent) | READY to define bounded discovery; external evidence unavailable | Inspecting provider-notes.md establishes the missing endpoint/schema. A task must name the required contract evidence and its unavailable status, without inventing a service. |
| Required R4 published-only consumer (absent) | UNREADY / BLOCKED | No endpoint, provider schema, publication-state semantics or authorized contract sample exists. Its specification cannot be invented. This blocks only the future consumer. |

## Exact smallest PLAN.md corrections

### T1: correct source anchors and preserve the existing interfaces

Change Owns to `Modify export.py imports and main parser/render branch; Modify schema.json::states; Test test_export.py`. Replace `consumes render_rows(rows)` with `main(argv) loads via load_rows(path), filters rows once, then renders the filtered rows`. Preserve both public signatures verbatim:

```python
def load_rows(path: Path) -> list[dict[str, str]]:
def main(argv: list[str] | None = None) -> int:
```

Replace the nonexistent render_rows edit with this current-source edit specification:

1. Add `import csv` and `import sys` beside the existing imports.
2. In main, add `parser.add_argument("--format", choices=["json", "csv"], default="json")` before `args = parser.parse_args(argv)`.
3. Retain the source argument, schema-driven --state choices, load_rows call and exact case-sensitive filtering code. Replace only `print(json.dumps(rows))`, after filtering and before `return 0`, with:

```python
if args.format == "csv":
    writer = csv.writer(sys.stdout)
    writer.writerow(("id", "title", "state"))
    writer.writerows((row["id"], row["title"], row["state"]) for row in rows)
else:
    print(json.dumps(rows))
```

4. Replace the proposed schema value with the exact preserved-and-extended value `{"states": ["active", "draft", "archived"]}`. The stale `["draft", "archived"]` would regress --state active and fails R2.

Ruling: edit the actual main parser/render branch, retaining public signatures, and append archived after draft while retaining active and draft -- current export.py/schema.json and REQUEST R1/R2 establish these corrections -- a wrong correction would break CLI compatibility or state validation; scope is T1 and its tests only.

### T1: make acceptance discriminating and complete

Retain the recorded root unittest command and both existing tests. Extend the proposed tests, using csv.reader with io.StringIO(newline="") for CSV observations, with these exact expectations:

- Omitted format and explicit `--format json`: decoded output equals the complete loaded items.json list, including all keys and values, order and title text; exit 0. Keep the existing json.dumps rendering to preserve current output shape.
- `--format csv`: header exactly `['id', 'title', 'state']`; decoded records exactly `[[row['id'], row['title'], row['state']] for row in loaded_items]`, in a,b,c,d order. Assert the comma/quote title `Tea, "green"` and embedded-newline title `Baris\nbaru` survive round-trip. This exercises stdlib CSV quoting rather than merely checking IDs.
- `--state archived` with each format: only a,c, in that order, and every returned state is archived. Retain JSON fields and the exact CSV header.
- `--state all` with each format: all a,b,c,d, in that order. `--state active` returns b and `--state draft` returns d with each format, proving existing states and pre-render filtering survive.
- Empty source `empty.json` with CSV: a header and no records; JSON: `[]`. Also use `--state archived` against a temporary source containing no archived records to prove an empty filtered result still gets the CSV header. Do not modify shared items.json.
- Invalid `--format xml`, invalid `--state missing`, and case-mismatched `--state Archived` raise argparse SystemExit with code 2. Capture stderr to avoid noisy test output. The uppercase case must not silently match archived.
- Parse schema.json and assert states exactly `['active', 'draft', 'archived']` in that order.

The current run_cli fixes the source to items.json. Add a separate test helper accepting a source path (or invoke main directly with that path under redirected stdout) for empty and temporary-source checks; preserve existing helper callers. No package script or external service is needed.

Before implementation, add a meaningful CSV assertion and observe its failure because --format is unsupported (test code must catch/express argparse rejection as the behavior failure). Then implement the bounded edit and run the focused suite, expecting all assertions exercised and passing. A syntax/import/fixture failure is not RED evidence. Record command, root directory, Python version, actual counts/results and modified-file identity in PLAN.md; the present baseline PASS must not be relabeled completed R1/R2 evidence.

### T2: retain the exact accepted textual scope

No task correction is required. The adjacent setup text in this README is prose (`Use Python 3.11+.`), not a shell setup command; preserve it byte-for-byte. The accepted command lacks the source positional required by main, but R3 explicitly requires this exact replacement. Do not invent a source argument or rewrite the surrounding quickstart in this task.

### R4: add the omitted discovery and explicitly unready consumer

Add a provider discovery task with no dependency on T1/T2. Anchor it to provider-notes.md and REQUEST R4. Inputs needed: an authorized endpoint description and request/response schema sample, including how published-only status is represented and selected. Acceptance: either record obtained contract evidence and its source with exact fields/semantics, or explicitly record that evidence is unavailable and the consumer stays UNREADY. Current outcome is unavailable; no credentials or service contract are supplied. Do not claim the external discovery itself complete.

Add a separate future published-only consumer task depending on successful provider contract discovery, with `Readiness: UNREADY`, `Status: BLOCKED`, and the unavailable contract as its named dependency. Its exact file/symbol anchors, consumer transformation and executable acceptance checks remain unspecified until evidence exists; do not add invented URLs, fields, authentication or response shapes. T1 and T2 retain no dependency on either provider task.

Ruling: add the missing discovery/unready consumer entries and isolate their dependency -- REQUEST R4 explicitly requires these entries and provider-notes.md confirms unavailable evidence -- an invented contract would misdirect future integration; scope is the plan, not any provider implementation.

## Consequential missing decisions and next action

R1-R3 have no missing consequential user-owned decision: the corrections are grounded in accepted requirements and inspected source. Already-authorized local implementation needs no new approval gate. The future provider consumer lacks material contract evidence (endpoint, schema and published selection semantics); only that consumer must wait for an authorized contract sample.

NEXT ACTION for the executor: apply the bounded T1 and R4 plan corrections above to the existing PLAN.md; start corrected T1 with discriminating tests and execute independent T2. Keep the future provider consumer explicitly unready. This preflight does not implement or claim acceptance of the export change.
