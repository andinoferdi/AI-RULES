# Export formats and archived state

Status: BLOCKED (remote only; local R1-R3 DONE)
Plan depth: STANDARD
Current phase: local implementation and verification complete; remote consumer blocked
Authority: planning ended with PLAN.md; this copy now includes authorized execution evidence. REQUEST.md authorizes another executor to implement after planning, without a new approval gate. No commit/push is authorized.

## Executive snapshot

R1-R3 are DONE independently of the provider after sequential T1-T3 execution. D1 remains blocked by unavailable authorized provider contract; C1 remains explicitly unready. No application changes were made during planning; this plan now records local execution.

Inspected export.py, test_export.py, schema.json, items.json, empty.json, README.md, provider-notes.md and REQUEST.md. Existing public signatures are `load_rows(path: Path) -> list[dict[str, str]]` and `main(argv: list[str] | None = None) -> int`; preserve both. main builds argparse state choices from schema.json, loads the supplied source, filters using exact equality, then prints json.dumps(rows). Existing run_cli(*options) supplies items.json and captures main's stdout. The project requires Python 3.11+ and stdlib only.

Baseline: `python -m unittest discover -s . -p test_export.py -v` ran at this repository root during planning: 2 tests passed, exit 0. New checks and actual execution results are recorded below. The workflow package and canonical execution/TDD guides are unavailable in this fixture; this plan preserves the supplied skill's essential state/evidence/authority contract without claiming those guides were loaded.

## Objective and acceptance criteria

- R1: Add `--format csv`; omitted/default format stays JSON with its current shape. CSV columns are exactly id,title,state, in that order; preserve row order, quote commas/quotes/newlines correctly, and emit a header for empty results. Use stdlib csv, with no dependency additions.
- R2: schema.json states become exactly `["active", "draft", "archived"]`. --state accepts archived; all retains every row; matching is case-sensitive and precedes either renderer. Invalid options still exit 2 through argparse. Preserve public signatures.
- R3: In README.md Quickstart replace exactly `python export.py --state active` with `python export.py --state archived --format csv`; retain adjacent `Use Python 3.11+.` and all other content. The accepted literal omits the positional source; do not add one as an unrelated correction.
- R4: Include bounded discovery of the missing remote provider contract and an explicitly unready published-only consumer. Do not invent or implement the provider. It does not block R1-R3.

## Execution board

| ID | Status | Dependencies | Ownership |
| --- | --- | --- | --- |
| T1 CSV output | DONE | none | export.py, test_export.py |
| T2 Archived filtering | DONE | T1 | schema.json, test_export.py; export.py only if needed |
| T3 Quickstart and final local gate | DONE | T1, T2 | README.md, verification evidence in PLAN.md |
| D1 Provider discovery | BLOCKED: authorized endpoint/schema sample unavailable | none | discovery evidence in PLAN.md |
| C1 Published-only consumer | BLOCKED: D1 exit criterion unmet | D1 | no implementation files assigned yet |

T1/T2 shared writes are serialized. D1 can advance independently when an authorized contract is supplied; it does not gate local work. No delegation, installs or external services are required for R1-R3.

## Detailed execution

All commands run at the repository root containing REQUEST.md, with Python 3.11+ and the existing fixtures. On resume compare the relevant source with the snapshot above; preserve unrelated changes, rebaseline only affected tasks and keep valid evidence. Update board/detail statuses together using TODO, IN_PROGRESS, BLOCKED, DONE or SKIPPED.

### T1 — CSV through the CLI

Status: DONE. Requirements: R1; preserve existing filtering. Dependencies: none.
Consumes inspected load_rows and main's pre-render filter. Produces proposed argparse option `--format`, choices json/csv, default json; both renderers consume the same filtered rows. Owns export.py and test_export.py.

1. Retain existing tests and add these cases in test_export.py, importing csv. Reuse run_cli for items.json; for another source capture stdout around main([str(source), ...]) directly or add a test helper without changing application signatures.
   - `test_json_format_compatibility`: omitted format and `--format json` return 0 and exactly `json.dumps(json.loads(items.json text)) + "\n"`; decoded rows retain all fields/order.
   - `test_csv_quoting_and_order`: CSV returns 0; `list(csv.reader(io.StringIO(output, newline="")))` equals `["id","title","state"]`, then `["a", 'Tea, "green"', "archived"]`, `["b", "Baris\nbaru", "active"]`, `["c","Kopi","archived"]`, `["d","Draft","draft"]`. Also assert the title containing comma/quotes appears encoded as `"Tea, ""green"""`; embedded newline remains one field, not an extra record.
   - `test_csv_empty_source`: empty.json with CSV returns 0 and exactly one header row.
   - `test_csv_active_filter`: --state active with CSV returns header plus `["b","Baris\nbaru","active"]` only, exit 0.
   - `test_invalid_format`: --format yaml raises SystemExit with code 2; captured stderr identifies invalid choice and stdout contains no export.
2. Run `python -m unittest discover -s . -p test_export.py -v`. Expect valid --format cases to fail because the option is unrecognized. This is the missing behavior at the existing public entrypoint; broken imports/syntax/fixtures are setup failures. The invalid-format test may already pass and is preservation coverage, not the RED proof.
3. Add stdlib csv/sys imports and argparse format choices. Keep filtering before rendering. Preserve `print(json.dumps(rows))` for JSON. Use csv.writer on stdout with `lineterminator="\n"`, write the exact header unconditionally, and write id/title/state explicitly for each selected row. This avoids platform-dependent doubled carriage returns without changing signatures or adding packages.
4. Run the same command; expect all existing/T1 cases pass, nonzero count, exit 0. Record actual command/result and tested content identity before DONE.

Integration gate: tests call main -> argparse -> real schema/source loader -> filter -> renderer -> captured stdout, not just a CSV helper.
Evidence: `python -m unittest discover -s . -p test_export.py -v`: baseline 2 passed; T1 RED 7 tests, 4 missing-option errors and 1 missing-choice diagnostic failure, exit 1; T1 GREEN 7 passed, exit 0. SHA-256 export.py=d723d850efe91f6520d1252e512b8e23e3b5e357c4ca65e1323dd08bb02ffbad; test_export.py=b43480a1d33ea5b2ccf41e3c1f5cac6898b5f812b7752b878d89d504a69fd391.

### T2 — Archived choice and exact filtering

Status: DONE. Requirements: R2 and R1 preservation. Depends on T1.
Consumes T1's format option and inspected schema-driven choices. Produces schema states `["active", "draft", "archived"]`; no new application API.

1. Add cases in test_export.py:
   - `test_archived_both_formats`: --state archived yields source objects a,c in JSON; with CSV yields header plus `["a", 'Tea, "green"', "archived"]`, `["c","Kopi","archived"]`, in that order, exit 0.
   - `test_all_both_formats`: omitted --state and explicit --state all retain all four rows/order in both formats.
   - `test_state_choices_preserved`: active yields b and draft yields d in both formats; assert schema states equal exactly active,draft,archived in that order.
   - `test_case_sensitive_filter_and_empty_result`: use a temporary JSON source with e/title Upper/state Archived and f/title Lower/state archived. --state archived includes only f in both formats. A source containing only e yields `[]` in JSON and header only in CSV. Close temporary files before main opens them on Windows; preserve repository fixtures.
   - `test_invalid_state`: Archived and unknown each raise argparse SystemExit 2, with an invalid-choice stderr message and no exported stdout. Do not normalize case.
2. Run `python -m unittest discover -s . -p test_export.py -v`; expect valid archived cases to fail because argparse rejects archived, and the exact schema assertion to fail. Existing preservation assertions may pass.
3. Append archived after draft in schema.json, preserving active/draft. Existing equality filtering and schema-driven choices should suffice; change export.py only if evidence requires it, retaining signatures and filtering before both renderers.
4. Run the same command; all assertions must pass with nonzero count and exit 0. Record actual evidence.

Integration: schema -> parser -> loader -> shared exact filter -> both renderers, including empty filtered results. No provider dependency.
Evidence: `python -m unittest discover -s . -p test_export.py -v`: T2 RED 12 tests, 6 archived-choice subtest errors and 1 schema assertion failure, exit 1; T2 GREEN 12 passed, exit 0. SHA-256 export.py=d723d850efe91f6520d1252e512b8e23e3b5e357c4ca65e1323dd08bb02ffbad; test_export.py=334f7a51aced84930507ae41632c6c172ddc2af87113f8e4a4b6064ce98de4c5; schema.json=5383e0d85209eb09a2f7e471b98dee1746d830645b76fd5e8b530bbe8443aa1a.

### T3 — Quickstart and final local gate

Status: DONE. Requirements: R3 and final R1/R2 integration. Depends on T1,T2.
Owns README.md and verification evidence in PLAN.md. No new interface.

1. Confirm the old Quickstart command and adjacent setup line. Replace only that command with `python export.py --state archived --format csv`.
2. Inspect README.md: Quickstart contains the exact new command, no old command, and unchanged `Use Python 3.11+.`; compare against its pre-edit content to ensure no other changes. This is a static artifact check; the accepted README literal lacks required positional source and is not a valid standalone smoke command.
3. Run `python -m unittest discover -s . -p test_export.py -v`; expect all cases pass, nonzero count, exit 0.
4. Run `python export.py items.json --state archived --format csv`; expect header and a,c rows, with correctly escaped title. Run `python export.py empty.json --format csv`; expect header only. Run `python export.py items.json`; expect original JSON shape and row order. These commands supply the required source and test the actual script entrypoint.
5. Record results and limits; mark local tasks DONE only with their acceptance evidence. Report local R1-R3 separately from blocked remote work. No commit/push or additional approval step.

Evidence: README byte comparison confirmed the exact command replacement and all other bytes preserved. Final `python -m unittest discover -s . -p test_export.py -v`: 12 passed, exit 0. Actual script checks (via local subprocess, checked stdout/stderr/exit): `python export.py items.json --state archived --format csv` produced header and correctly quoted a,c rows; `python export.py empty.json --format csv` produced header only; `python export.py items.json` matched original JSON serialization and row order. All three exited 0 with empty stderr. Public signatures inspected unchanged; application imports argparse,csv,json,sys,pathlib are stdlib. No dependencies added.

### D1 — Bounded provider contract discovery

Status: BLOCKED. Requirement: R4. Dependencies: none.
Blocker: provider-notes.md says endpoint/schema are unavailable and requires an authorized contract sample; no credentials supplied. Owns discovery findings in PLAN.md only.

Use provider-notes.md as the local starting point. When supplied, inspect one authorized provider contract/sample through the existing project channel. Do not guess a provider/URL, search unrelated services, contact others or implement network behavior.

Exit criterion: record authoritative source/version, endpoint/method, request/response schema, exact published-only meaning and any mapping to local states, pagination/order, authentication mechanism without secrets, and error contract. Missing fields stay UNKNOWN; stop the bounded discovery with C1 blocked rather than inventing interfaces. The discovery artifact must distinguish documented facts from remaining questions. D1 does not gate T1-T3.

Evidence: inspected provider-notes.md confirms the blocker; no remote validation available.

### C1 — Future published-only consumer, explicitly unready

Status: BLOCKED by D1. Requirement: R4. Depends on D1.
No endpoint, schema, provider function signature or implementation is approved by this plan. After D1 meets its exit criterion, replace this placeholder with a grounded task in the same plan: owned files, verified producer/consumer contract, and named contract/public-flow tests for published-only selection, paging and provider failures. Readiness requires complete D1 evidence plus that concrete task. Until then do not implement C1. External actions require their actual authority.

## Coverage and validation limits

| Requirement / failure case | Owner | Observable check |
| --- | --- | --- |
| CSV columns, quoting, multiline field, row order | T1 | test_csv_quoting_and_order literal rows and escaping |
| Empty source / empty filtered CSV | T1,T2 | test_csv_empty_source; test_case_sensitive_filter_and_empty_result |
| Default/explicit JSON compatibility | T1 | test_json_format_compatibility exact text and decoded rows |
| Archived appended, active/draft retained | T2 | test_state_choices_preserved exact schema/order and outputs |
| Archived, all, case-sensitive matching; filter before both renderers | T1,T2 | test_csv_active_filter; test_archived_both_formats; test_all_both_formats; case-sensitive temporary fixture |
| Invalid options exit 2 through argparse | T1,T2 | test_invalid_format; test_invalid_state |
| Public signatures and stdlib-only imports | T1,T2 final review | compare definitions with snapshot, inspect imports/dependencies |
| Exact README command, adjacent setup retained | T3 | focused artifact comparison |
| Actual script integration | T3 | full test command and source-supplied smoke commands |
| Discovery, unready consumer, local independence | D1,C1 | D1 exit artifact, explicit blocked states, no local dependency on provider |

Unavailable evidence: provider endpoint/schema and live remote behavior; C1 cannot yet be designed or validated. Local R1-R3 are verified by 12 passing tests, focused README byte comparison and actual script smoke checks. Remote behavior remains unverified.

## NEXT ACTION

Local R1-R3 require no further implementation. D1 can resume only when an authorized provider contract/sample is supplied; record its source/version and required contract fields before making C1 ready. Do not invent a provider or implement the blocked consumer.

## Final tested content identity (SHA-256)

- export.py: `d723d850efe91f6520d1252e512b8e23e3b5e357c4ca65e1323dd08bb02ffbad`
- schema.json: `5383e0d85209eb09a2f7e471b98dee1746d830645b76fd5e8b530bbe8443aa1a`
- test_export.py: `334f7a51aced84930507ae41632c6c172ddc2af87113f8e4a4b6064ce98de4c5`
- README.md: `564360cc67fb7e4483071f705fc9954c1cd84b1e2066d20dfc4ea6b5f69b4014`
- items.json: `53145d24c1e9854158263e696584a27ff34342b8a59fdb4305dbdb61e70dbeb7`
- empty.json: `a5338d955b09046ec0b16f3a9625b7955c763aae07dc722e474e6078745f932f`
- provider-notes.md: `9fdf5647f935c4467142ecf321e363363aeaf7bb17151d3cb6313b62f1ad027e`
- REQUEST.md: `cd1c7243f4202ba539e6a569ff7087319f14e77b1cf72fa51676b0c2942c15e0`
