"""Account storage."""
from dataclasses import dataclass
from itertools import count


@dataclass
class Account:
    id: int
    email: str
    password_hash: str


class InMemoryAccounts:
    def __init__(self):
        self._rows: dict[int, Account] = {}
        self._ids = count(1)

    def add(self, email: str, password_hash: str) -> Account:
        account = Account(next(self._ids), email, password_hash)
        self._rows[account.id] = account
        return account

    def find_by_email(self, email: str) -> Account | None:
        return next((row for row in self._rows.values() if row.email == email), None)

    def all(self) -> list[Account]:
        return list(self._rows.values())
