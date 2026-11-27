import time


class TTLCache:
    """Tiny in-process cache: get_or_load(key, loader) with a fixed time-to-live."""

    def __init__(self, ttl_seconds=60.0):
        self.ttl = ttl_seconds
        self._entries = {}

    def get_or_load(self, key, loader):
        now = time.monotonic()
        hit = self._entries.get(key)
        if hit and hit[0] > now:
            return hit[1]
        value = loader()
        self._entries[key] = (now + self.ttl, value)
        return value

    def clear(self):
        self._entries.clear()
