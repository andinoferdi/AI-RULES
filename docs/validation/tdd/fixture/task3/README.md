# Accounts

Sign-up for the Kopi Kita loyalty app. `AccountService.register` creates an account, stores
it and sends a welcome email.

## Rules

- One account per email address. Addresses are compared without regard to letter case or
  surrounding spaces, and stored lower-cased and trimmed.
- Passwords have at least 8 characters.

## Layout

- `accounts/service.py`: `AccountService`, the public entry point.
- `accounts/repository.py`: in-memory storage used by the app and by tests.
- `accounts/mailer.py`: the SMTP client. It sends real email; tests use `tests/fakes.py`.

## Tests

    python -m unittest discover -s tests -t .
    python -m unittest tests.test_register        # one module

See `git log` for history.
