"""Reset local state: fresh var/invoices.json from data/, empty queue and telemetry."""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from payments.paths import ROOT, VAR  # noqa: E402

if VAR.exists():
    shutil.rmtree(VAR)
VAR.mkdir(parents=True)
shutil.copy(ROOT / "data" / "invoices.json", VAR / "invoices.json")
print(f"reset {VAR}")
