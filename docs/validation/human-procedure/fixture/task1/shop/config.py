"""Settings for the shop, read from the environment (and `.env` in development)."""
import os
import re
from pathlib import Path

# key -> (pattern the value must match, used by)
REQUIRED = {
    "PAYLANE_PUBLISHABLE_KEY": (r"pk_test_\w+", "checkout page (sent to the browser)"),
    "PAYLANE_SECRET_KEY": (r"sk_test_\w+", "server: creates payments"),
    "PAYLANE_WEBHOOK_SECRET": (r"whsec_\w+", "server: verifies PayLane webhooks"),
    "MAILBIRD_API_TOKEN": (r"mb_[A-Za-z0-9]{24,}", "server: sends order emails"),
    "MAILBIRD_SENDER": (r"[^@\s]+@[^@\s]+", "server: From address of order emails"),
    "APP_BASE_URL": (r"https?://\S+", "links in emails, webhook URL"),
    "DATABASE_URL": (r"postgres://\S+", "server: database"),
}


def read_dotenv(path: Path) -> dict:
    values = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def load(env_only: bool = False) -> dict:
    values = {} if env_only else read_dotenv(Path(".env"))
    values.update({k: v for k, v in os.environ.items() if k in REQUIRED})
    return values


def check(values: dict) -> dict:
    status = {}
    for key, (pattern, _) in REQUIRED.items():
        value = values.get(key, "")
        if not value:
            status[key] = "missing"
        elif not re.fullmatch(pattern, value):
            status[key] = "bad format"
        else:
            status[key] = "ok"
    return status
