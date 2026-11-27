# Discount codes

`invoicekit.apply_code(lines, code, today=None)` returns the invoice total after the code,
rounded to cents. `today` defaults to the current date.

- **R1** A percentage code takes that percentage off the subtotal.
- **R2** A fixed-amount code takes that amount off the subtotal. The total never goes below 0.00.
- **R3** Codes match case-insensitively, and spaces around the code are ignored.
- **R4** A code used after its `expires` date raises `ExpiredCode` (the expiry day itself is still
  valid). An unknown code raises `UnknownCode`.

Active codes:

| Code | Kind | Value | Expires |
| --- | --- | --- | --- |
| SPRING10 | percent | 10 | 2026-04-30 |
| VIP25 | percent | 25 | 2027-12-31 |
| WELCOME50 | fixed | 50.00 | 2027-12-31 |
