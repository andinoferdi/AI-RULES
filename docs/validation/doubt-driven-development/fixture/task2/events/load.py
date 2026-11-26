"""Load a day's events from the webhook dump."""
import json
from pathlib import Path


def load_events(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
