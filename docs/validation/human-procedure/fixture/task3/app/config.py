"""Settings for notes-api. `python -m app.config --check` reports problems by name."""
import sys
from pathlib import Path

LEVELS = {"debug", "info", "warning", "error"}


def read_dotenv(path: Path = Path(".env")) -> dict:
    values = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
    return values


def problems(values: dict) -> list:
    found = []
    if values.get("LOG_LEVEL") not in LEVELS:
        found.append("missing LOG_LEVEL" if "LOG_LEVEL" not in values else "invalid LOG_LEVEL")
    if not values.get("PORT", "").isdigit():
        found.append("missing PORT" if "PORT" not in values else "invalid PORT")
    return found


if __name__ == "__main__" and "--check" in sys.argv:
    issues = problems(read_dotenv())
    print("\n".join(issues) if issues else "config ok")
    sys.exit(1 if issues else 0)
