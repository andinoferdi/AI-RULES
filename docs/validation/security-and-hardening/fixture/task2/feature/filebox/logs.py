"""Structured event log, shipped to the shared log platform that support staff can search."""
import json

EVENTS: list[str] = []


def log_event(name: str, **fields) -> None:
    EVENTS.append(json.dumps({"event": name, **fields}, default=str, sort_keys=True))
