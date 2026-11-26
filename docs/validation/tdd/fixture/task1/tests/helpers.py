"""Test doubles for the boundaries the garage talks to."""


class RecordingSms:
    """Stands in for HttpSmsGateway: keeps every message instead of sending it."""

    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send(self, phone: str, text: str) -> None:
        self.sent.append((phone, text))
