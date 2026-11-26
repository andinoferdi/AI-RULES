import json
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "config" / "production.json"


def load(path=CONFIG):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def is_enabled(name, config=None):
    config = load() if config is None else config
    return bool(config.get("flags", {}).get(name, False))
