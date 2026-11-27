"""SMTP client. Sends real email; never use it in tests."""
import os
import smtplib
from email.message import EmailMessage


class SmtpMailer:
    def __init__(self, host: str | None = None):
        self._host = host or os.environ.get("KOPI_SMTP_HOST", "smtp.kopikita.example")

    def send(self, to: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = "halo@kopikita.example"
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)
        with smtplib.SMTP(self._host, 587, timeout=10) as smtp:
            smtp.starttls()
            smtp.send_message(message)
