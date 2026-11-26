# Invoices

Renders the sales invoices of CV Sinar Kertas from the CSV files in `data/invoices/`.

    python -m invoices.render INV-2026-0412

## Tax rule

PPN is 11% of the invoice subtotal, rounded half up to the whole rupiah (Rp 16,50 becomes
Rp 17). It is worked out once per invoice, on the subtotal, never per line.

## Layout

- `invoices/money.py`: parsing and formatting rupiah amounts (`33.333` means 33,333 rupiah).
- `invoices/tax.py`: the PPN calculation.
- `invoices/render.py`: reads an invoice CSV and prints the invoice.
- `invoices/footer.py`: the legal footer.

## Tests

    python run_tests.py                         # whole suite
    python run_tests.py tests.test_render       # one module

### Known issue INV-77

`tests/test_footer.py::FooterTest::test_footer_shows_16_digit_npwp` fails. It describes the
new 16-digit NPWP format, which we switch to once Legal sends the company's new number. Leave
the test and the footer as they are until then.
