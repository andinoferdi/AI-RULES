"""Structured event log shipped to the shared log platform."""
import json

EVENTS: list[str] = []


def log_event(name: str, **fields) -> None:
    EVENTS.append(json.dumps({"event": name, **fields}, default=str, sort_keys=True))
