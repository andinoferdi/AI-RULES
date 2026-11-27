"""Sign-up."""
import hashlib

from accounts.repository import Account


class DuplicateEmail(Exception):
    pass


class WeakPassword(Exception):
    pass


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class AccountService:
    def __init__(self, accounts, mailer):
        self._accounts = accounts
        self._mailer = mailer

    def register(self, email: str, password: str) -> Account:
        if len(password) < 8:
            raise WeakPassword("password must have at least 8 characters")
        if self._accounts.find_by_email(email) is not None:
            raise DuplicateEmail(email)
        account = self._accounts.add(email, _hash(password))
        self._mailer.send(email, "Selamat datang di Kopi Kita",
                          "Akun Anda sudah aktif. Selamat menikmati!")
        return account
