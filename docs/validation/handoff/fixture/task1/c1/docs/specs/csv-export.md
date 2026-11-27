# CSV export of invoices

Source: docs/issue-412.md. Owner: Andi. Consumer: Budi's Excel import macro.

## Format

- Delimiter `;` (Budi's Excel runs the Indonesian locale, where `,` is the decimal separator).
- A header row, then one row per invoice, in this column order:
  `number;issued;customer;kind;amount_idr`.
- `issued` as an ISO date (`2026-11-03`).
- `amount_idr` as a whole number with no thousands separator and no currency prefix.
- Quote a field only when it contains `;`, `"` or a line break (minimal quoting).
- UTF-8 without BOM, `\n` line endings.

## Credit notes

Open: Budi has not said whether a credit note's amount should be negative or stay positive
with `kind=credit_note`. Asked on 2026-11-24.

## Acceptance

1. `python -m invoicekit.export --out invoices.csv` writes the file.
2. The header matches the column order above.
3. Budi's sample import (`docs/samples/budi-import-sample.csv`) and our output have the same
   header and the same field formats.
4. Credit notes follow Budi's answer.
