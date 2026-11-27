# Spec: invoice CSV export (BIL-31)

Status: accepted by Rina (product owner) on 2026-11-20.

Finance sends each customer a CSV of that customer's invoices. Today they copy rows by hand.

## Requirements

- R1. `python -m billing.cli export --customer NAME [--out PATH] [--data PATH]` writes the
  invoices of one customer as CSV. Without `--out` it writes to standard output. `--data`
  defaults to `data/invoices.csv`.
- R2. The customer match is exact and case-sensitive. "Acme, Inc." (Jakarta) and
  "ACME, Inc." (Surabaya) are different legal entities with different tax numbers; mixing
  their invoices in one file is a reportable error.
- R3. Columns `number,customer,amount`, header first, rows in file order. Amounts are
  decimal strings with two places and a leading minus for credit notes (`1250.00`,
  `-50.00`).
- R4. The file follows RFC 4180: a field containing a comma, a double quote or a line break
  is quoted, and a double quote inside a field is doubled. Lines end with `\n`.
- R5. A customer with no invoices gives the header line only, with exit status 0.
- R6. Release 0.4.0 carries this feature. Publishing (pushing `main` and the tag) is done by
  whoever is authorized for the release.

## Out of scope

Totals per customer, other output formats, renaming `calcualte_total` (BIL-12).
