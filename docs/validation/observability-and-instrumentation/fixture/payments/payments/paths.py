import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAR = Path(os.environ.get("PAYMENTS_VAR", ROOT / "var"))
TELEMETRY = VAR / "telemetry"
