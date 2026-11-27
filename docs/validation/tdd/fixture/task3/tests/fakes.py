"""Test doubles for the boundaries accounts talk to."""


class FakeMailer:
    """Stands in for SmtpMailer: keeps every email instead of sending it."""

    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, subject: str, body: str) -> None:
        self.sent.append((to, subject))
