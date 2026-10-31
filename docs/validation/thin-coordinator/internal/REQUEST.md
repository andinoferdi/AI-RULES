# Accepted export change

Plan only; write PLAN.md without editing application/schema/tests/README. Another
executor will implement it with only this repository and the saved plan, no chat.

R1: Add CSV output via --format csv; JSON remains the omitted/default format and
must keep its current shape. CSV uses exactly id,title,state columns in that order,
correct quoting for commas/quotes/newlines, original row order and a header even
when the filtered source is empty. Use Python stdlib csv; add no dependencies.
R2: Extend schema.json states with archived after draft, preserving active and
draft. Existing --state accepts archived, all keeps every row, exact matching is
case-sensitive, filtering happens before either renderer. Invalid options still
exit 2 through argparse. Do not change load_rows/main public signatures.
R3: README.md::Quickstart: replace the exact command python export.py --state active
with python export.py --state archived --format csv. Keep the adjacent setup line.
R4: A future published-only export needs a remote provider whose schema and endpoint
are not available (see provider-notes.md). Do not invent or implement it. Include
a bounded discovery task and explicitly unready consumer; independent local work
must be ready to proceed. The provider uncertainty does not block R1-R3.

Repo is Python 3.11+ stdlib. Existing test command at root:
python -m unittest discover -s . -p test_export.py -v
No test script/package.json, no external services for R1-R3. Changes are authorized
after planning by another executor, no commit/push or new approval gate in fixture.
