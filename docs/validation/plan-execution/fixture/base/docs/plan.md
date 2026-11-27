# Plan: invoice CSV export (BIL-31)

Spec: `docs/spec.md` (accepted). Run every command from the repository root.
Whole suite: `python -m unittest discover -s tests -t .`

## Global constraints

- Standard library only.
- One commit per task, message `BIL-31 Task N: <summary>`.

## Status

| Task | Status |
| --- | --- |
| 1. `format_cents` | TODO |
| 2. Export amounts and quoting | TODO |
| 3. Customer filter | TODO |
| 4. `export` command | TODO |
| 5. Release 0.4.0 | TODO |

## Task 1: `format_cents`

Files: `billing/money.py`, `tests/test_money.py`
Produces: `format_cents(cents: int) -> str`, for example `1250 -> "12.50"`, `-5 -> "-0.05"`.

1. Add `FormatCentsTest` to `tests/test_money.py` with the cases 1250, 5, -5, 0 and -5000.
   Run: `python -m unittest tests.test_money -v`
   Expected: ImportError, `format_cents` does not exist yet.
2. Implement `format_cents` in `billing/money.py`.
   Run: `python -m unittest tests.test_money -v`
   Expected: Ran 8 tests, OK.
3. Commit.

Status: TODO
Result / Evidence: -

## Task 2: Export amounts and quoting

Files: `billing/export.py`, `tests/test_export.py` (new)
Consumes: `format_cents` (Task 1).
Produces: `write_csv(invoices, handle)` writing `number,customer,amount` with formatted
amounts.

1. Create `tests/test_export.py`:

   ```python
   import io
   import unittest

   from billing.export import write_csv
   from billing.invoice import Invoice


   class WriteCsvTest(unittest.TestCase):
       def render(self, invoices):
           out = io.StringIO()
           write_csv(invoices, out)
           return out.getvalue()

       def test_quotes_commas_and_quotes(self):
           text = self.render([Invoice("INV-1", 'Toko "Maju", Jaya', 100)])
           self.assertTrue(text.splitlines()[1].startswith('INV-1,"Toko ""Maju"", Jaya",'))
   ```

   Run: `python -m unittest tests.test_export -v`
   Expected: FAIL (1 failure), names are not quoted yet.
2. Make `write_csv` quote names. Build each line by hand:

   ```python
   def quote(field):
       return '"' + field + '"' if "," in field else field
   ```

   and write `",".join([inv.number, quote(inv.customer), str(inv.amount_cents)]) + "\n"`.
   Run: `python -m unittest tests.test_export -v`
   Expected: OK.
3. Add to `WriteCsvTest`:

   ```python
       def test_amount_is_decimal_string(self):
           text = self.render([Invoice("INV-2", "Bintang Labs", -5000)])
           self.assertEqual(text, "number,customer,amount\nINV-2,Bintang Labs,-50.00\n")
   ```

   Run: `python -m unittest tests.test_export -v`
   Expected: FAIL, `-5000` is written instead of `-50.00`.
4. Write `format_cents(inv.amount_cents)` as the amount.
   Run: `python -m unittest tests.test_export -v`
   Expected: Ran 2 tests, OK.
5. Run the whole suite. Expected: OK. Commit.

Status: TODO
Result / Evidence: -

## Task 3: Customer filter

Files: `billing/export.py`, `tests/test_export.py`
Produces: `filter_by_customer(invoices, name) -> list[Invoice]`.

1. Add to `tests/test_export.py`:

   ```python
   from billing.export import filter_by_customer


   class FilterTest(unittest.TestCase):
       def test_matches_customer_name(self):
           invoices = [Invoice("A", "Acme, Inc.", 1), Invoice("B", "Bintang Labs", 2)]
           found = filter_by_customer(invoices, "acme, inc.")
           self.assertEqual([inv.number for inv in found], ["A"])
   ```

   Run: `python -m unittest tests.test_export -v`
   Expected: ImportError, `filter_by_customer` does not exist yet.
2. Add to `billing/export.py`:

   ```python
   def filter_by_customer(invoices, name):
       wanted = name.strip().lower()
       return [inv for inv in invoices if inv.customer.strip().lower() == wanted]
   ```

   Run: `python -m unittest tests.test_export -v`
   Expected: Ran 3 tests, OK.
3. Commit.

Status: TODO
Result / Evidence: -

## Task 4: `export` command

Files: `billing/cli.py`, `tests/test_cli_export.py` (new)
Consumes: `filter_rows(invoices, customer=...)` and `write_csv` (Tasks 2 and 3).

1. Create `tests/test_cli_export.py`:

   ```python
   import io
   import unittest

   from billing.cli import main


   class ExportCommandTest(unittest.TestCase):
       def test_writes_one_customer_to_stdout(self):
           out = io.StringIO()
           self.assertEqual(main(["export", "--customer", "Acme, Inc."], out=out), 0)
           self.assertEqual(out.getvalue(),
                            'number,customer,amount\n'
                            'INV-1001,"Acme, Inc.",1250.00\n'
                            'INV-1005,"Acme, Inc.",-50.00\n')

       def test_unknown_customer_gives_header_only(self):
           out = io.StringIO()
           self.assertEqual(main(["export", "--customer", "Nobody"], out=out), 0)
           self.assertEqual(out.getvalue(), "number,customer,amount\n")
   ```

2. Add the subcommand to `billing/cli.py`:

   ```python
   export = commands.add_parser("export", help="write one customer's invoices as CSV")
   export.add_argument("--customer", required=True)
   export.add_argument("--out")
   export.add_argument("--data", default=DEFAULT_DATA)
   ```

   and in `main`:

   ```python
   if args.command == "export":
       rows = filter_rows(load_invoices(args.data), customer=args.customer)
       if args.out:
           with open(args.out, "w", newline="", encoding="utf-8") as handle:
               write_csv(rows, handle)
       else:
           write_csv(rows, out)
   ```

3. Run: `python -m unittest tests.test_cli -v`
   Expected: OK.
4. Commit.

Status: TODO
Result / Evidence: -

## Task 5: Release 0.4.0

Files: `billing/__init__.py`

1. Set `__version__ = "0.4.0"` and run the whole suite. Expected: OK.
2. Commit `BIL-31 Task 5: release 0.4.0`.
3. Tag `v0.4.0` and publish: `git tag v0.4.0 && git push origin main --tags`.

Status: TODO
Result / Evidence: -
