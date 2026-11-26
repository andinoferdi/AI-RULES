import unittest

from accounts.repository import InMemoryAccounts
from accounts.service import AccountService, WeakPassword
from tests.fakes import FakeMailer


class RegisterTest(unittest.TestCase):
    def setUp(self):
        self.accounts = InMemoryAccounts()
        self.mailer = FakeMailer()
        self.service = AccountService(self.accounts, self.mailer)

    def test_new_account_gets_a_welcome_email(self):
        account = self.service.register("dimas@mail.example", "kopisusu123")

        self.assertEqual(account.email, "dimas@mail.example")
        self.assertEqual(self.mailer.sent, [("dimas@mail.example", "Selamat datang di Kopi Kita")])

    def test_short_password_is_rejected(self):
        with self.assertRaises(WeakPassword):
            self.service.register("dimas@mail.example", "kopi")
        self.assertEqual(self.accounts.all(), [])


if __name__ == "__main__":
    unittest.main()
