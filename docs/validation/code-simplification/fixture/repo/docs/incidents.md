# Incidents

## INC-212 (2025-03): negative order totals

Credit lines (a negative `unit_price`, used for vouchers and goodwill credits) pushed some
order totals below zero, and the payment provider rejected those charges. Since then
`price_order` clamps the total at zero, and checkout relies on never sending a negative
amount to the provider.

## INC-240 (2025-06): export job timeout

The nightly export ran past its window after the customer table grew. The job was moved to
a larger worker. No code change.
