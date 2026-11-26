"""Clocks. The gate uses SystemClock; tests use FixedClock."""
from datetime import datetime, timedelta


class SystemClock:
    def now(self) -> datetime:
        return datetime.now()


class FixedClock:
    def __init__(self, start: datetime):
        self._now = start

    def now(self) -> datetime:
        return self._now

    def advance(self, **kwargs) -> None:
        self._now += timedelta(**kwargs)
