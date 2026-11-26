# Arrears report, payments and late fees

Status: accepted by the treasurer, Bu Sari, on 2026-11-20.

## Intent

Before each monthly meeting the treasurer needs one command that shows who is behind on
which installment, by how much, and the late fee owed, and a way to record the payments
members bring to the office. Today she works this out by hand from the paper ledger.

## Global constraints

- Runs on the office PC: Python 3.9. No `match` statements and no `X | None` annotations.
- Standard library only. No new packages.
- Money is whole rupiah (`int`) everywhere, never `float`.
- Data files written before this change (installments without payment data) must still load.

## Requirements

**R1 Payments on installments.** An installment can be paid in part or in full. Each
installment stores `paid_amount` (whole rupiah). When a data file has no `paid_amount` for an
installment, it is 0. The overdue amount of an installment is `amount - paid_amount`; an
installment whose overdue amount is 0 is settled.

**R2 Days late.** An unsettled installment is late on a date `as_of` when `as_of` is after its
due date. Days late is the number of calendar days from the due date to `as_of`. An
installment due on `as_of` or later is not late.

**R3 Late fee.** There are 3 days of grace: fee days = days late - 3 when days late is more
than 3, otherwise 0. The fee is 0.5% of the overdue amount for each fee day, rounded down to
whole rupiah, and never more than 10% of the overdue amount (also rounded down). Examples:

| Overdue | Days late | Fee days | Fee |
| --- | --- | --- | --- |
| Rp 400.000 | 10 | 7 | Rp 14.000 |
| Rp 400.000 | 40 | 37 | Rp 40.000 (capped) |
| Rp 333.333 | 5 | 2 | Rp 3.333 |
| Rp 400.000 | 3 | 0 | Rp 0 |

**R4 Arrears command.**
`python -m koperasi.cli arrears --as-of YYYY-MM-DD [--data PATH]` prints one line per late
installment, fields separated by two spaces:

    <member_id>  <member_name>  cicilan <number>  <days late> hari  <overdue>  denda <fee>

Amounts use the existing rupiah format (`Rp 400.000`). Lines are sorted by days late, most
first, then by member id. The last line is:

    Total tunggakan: <sum of overdue>  Total denda: <sum of fees>

**R5 Nothing late.** When no installment is late, the command prints exactly
`Tidak ada tunggakan per <YYYY-MM-DD>.` and exits with code 0.

**R6 Bad date.** When `--as-of` is not a valid `YYYY-MM-DD` date, the command prints
`Tanggal tidak valid: <value>` to stderr and exits with code 2.

**R7 Recording a payment.**
`python -m koperasi.cli pay <loan_id> <installment_number> <amount> [--data PATH]` adds the
amount to that installment's `paid_amount` and saves the file. The amount accepts the same
forms as everywhere else (`150000`, `Rp 150.000`). A payment larger than the installment's
overdue amount is refused with `Pembayaran melebihi sisa cicilan (sisa <overdue>)` on stderr,
exit code 1, and the file is not changed. An unknown loan or installment number prints
`Cicilan tidak ditemukan` on stderr and exits with code 1. On success it prints
`Tercatat: <loan_id> cicilan <number>, sisa <overdue after payment>` and exits with code 0.

**R8 Cooperative holidays.** When an installment's due date falls on a cooperative holiday,
the due date moves to the next day that is not a holiday (weekends are working days at the
cooperative). Holidays come from the treasurer's calendar export, `kalender-koperasi.csv`.
Bu Sari will send a sample export; its columns and date format are not known yet.

## Out of scope

- Reminders to members (WhatsApp or SMS).
- Recalculating interest or changing installment amounts.
- Editing or deleting payments once recorded.
