# Garage

Ticketing and fees for the Mangga Dua parking garage. The exit gate calls
`TicketDesk.close_ticket`, which stamps the exit time, works out the fee and sends the
driver an SMS receipt.

## Tariff (current)

- Rp 5.000 for the first started hour, Rp 3.500 for every further started hour.
- At most Rp 40.000 per started 24 hours.
- Cars and motorbikes pay the same today.

## Layout

- `src/garage/billing.py`: the fee rules.
- `src/garage/tickets.py`: `TicketDesk`, used by the gate.
- `src/garage/clock.py`, `src/garage/sms.py`: the system clock and the SMS provider client.
  The SMS client calls the provider over HTTP; tests never use it.
- `tests/`: unit tests. `tests/helpers.py` has a recording SMS gateway for tests.

## Tests

The code lives under `src/`, so plain `python -m unittest` cannot import it. Use the wrapper,
which CI also runs:

    python scripts/test.py                                  # whole suite
    python scripts/test.py tests.test_billing               # one module
    python scripts/test.py tests.test_billing.FeeTest.test_first_hour   # one test
