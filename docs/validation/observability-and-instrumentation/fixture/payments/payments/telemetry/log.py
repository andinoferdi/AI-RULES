"""Structured JSON-lines logger. One object per line; bind() returns a child logger."""
import json
import os
import time

from payments.paths import TELEMETRY

LEVELS = {"debug": 10, "info": 20, "warn": 30, "error": 40}


class Logger:
    def __init__(self, fields=None):
        self._fields = dict(fields or {})

    def bind(self, **fields):
        return Logger({**self._fields, **fields})

    def _emit(self, level, event, fields):
        threshold = LEVELS.get(os.environ.get("LOG_LEVEL", "info"), 20)
        if LEVELS[level] < threshold:
            return
        record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "level": level,
                  "event": event, **self._fields, **fields}
        TELEMETRY.mkdir(parents=True, exist_ok=True)
        with open(TELEMETRY / "app.jsonl", "a", encoding="utf-8") as sink:
            sink.write(json.dumps(record, default=str) + "\n")

    def debug(self, event, **fields):
        self._emit("debug", event, fields)

    def info(self, event, **fields):
        self._emit("info", event, fields)

    def warn(self, event, **fields):
        self._emit("warn", event, fields)

    def error(self, event, **fields):
        self._emit("error", event, fields)


logger = Logger({"service": "payments-worker"})
