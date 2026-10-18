"""Console-independent observations of installer work."""
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class WorkEvent:
    phase: str
    kind: str = "phase"
    host: str = ""
    capability: str = ""
    action: str = ""
    status: str = ""
    completed: int | None = None
    total: int | None = None
    detail: str = ""


Reporter = Callable[[WorkEvent], None]


def emit(reporter: Reporter | None, phase: str, **kwargs) -> None:
    if reporter is not None:
        try:
            reporter(WorkEvent(phase, **kwargs))
        except Exception:
            # Observers must not change installation or rollback outcomes.
            pass
