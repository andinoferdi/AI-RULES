"""Remove repeated deliveries of the same event."""


def dedupe_events(events):
    """Return events with duplicate ids removed."""
    first = {}
    for event in events:
        first.setdefault(event["id"], event)
    return list(first.values())
