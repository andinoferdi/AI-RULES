import json
import time
from collections import deque

RECENT = deque(maxlen=1000)  # shown on the worker's debug page


def event(kind, **fields):
    line = json.dumps({"ts": round(time.time(), 3), "event": kind, **fields}, sort_keys=True)
    RECENT.append(line)
    return line
