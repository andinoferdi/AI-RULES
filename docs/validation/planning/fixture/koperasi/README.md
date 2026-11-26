# koperasi

Loan bookkeeping for a small savings-and-loan cooperative. Runs on the office PC
(Python 3.9, standard library only).

## Commands

    python -m koperasi.cli list [--data data/loans.json]

## Tests

Run from the repository root:

    python -m unittest discover -s tests -v

Every change keeps this suite green. There is no linter or type checker.

## Layout

- `koperasi/models.py`: `Loan` and `Installment` dataclasses.
- `koperasi/store.py`: reads and writes the JSON data file.
- `koperasi/money.py`: rupiah parsing and formatting (integers only).
- `koperasi/dates.py`: date helpers.
- `koperasi/cli.py`: the command line (`main(argv) -> int`).
- `docs/specs/`: accepted designs.
