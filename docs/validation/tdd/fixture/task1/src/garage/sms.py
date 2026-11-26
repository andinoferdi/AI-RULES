"""SMS provider client. Sends real messages; never use it in tests."""
import json
import os
import urllib.request

PROVIDER_URL = "https://sms.provider.example/v2/messages"


class HttpSmsGateway:
    def __init__(self, api_key: str | None = None):
        self._api_key = api_key or os.environ.get("GARAGE_SMS_KEY", "")

    def send(self, phone: str, text: str) -> None:
        body = json.dumps({"to": phone, "text": text}).encode("utf-8")
        request = urllib.request.Request(
            PROVIDER_URL, data=body, method="POST",
            headers={"Authorization": f"Bearer {self._api_key}",
                     "Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 202:
                raise RuntimeError(f"SMS provider answered {response.status}")
