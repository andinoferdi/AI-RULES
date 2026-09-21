from __future__ import annotations

import re


SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|password|secret)=([^\s&]+)"),
    re.compile(r"(?i)(bearer\s+)[a-z0-9._~+/=-]+"),
)


def redact(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        if pattern.pattern.startswith("(?i)(bearer"):
            redacted = pattern.sub(r"\1[REDACTED]", redacted)
        else:
            redacted = pattern.sub(r"\1=[REDACTED]", redacted)
    return redacted
