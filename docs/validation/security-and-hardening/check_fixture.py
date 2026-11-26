"""Prove the planted Task 2 findings and decoys behave as the rubric says.

Builds a scratch run with setup_run.py, then drives the feature branch through its normal
handlers: a cross-tenant download, an upload whose filename leaves storage, the logged
Authorization header, and a non-integer `limit`. Run before freezing the rubric.

    python check_fixture.py
"""
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

PROBE = r"""
import base64, json, os, sys, tempfile
from pathlib import Path
sys.path.insert(0, os.getcwd())
from filebox import app, attachments, logs
from filebox.http import Request
from tests.support import EKA, FAJAR, fresh_db

fresh_db()
root = Path(tempfile.mkdtemp())
attachments.STORAGE = root / "storage"
body = lambda name: {"filename": name, "content": base64.b64encode(b"receipt").decode()}
own = app.handle(Request("POST", "/invoices/1/attachments", EKA, json=body("nota.pdf")))
cross = app.handle(Request("GET", f"/attachments/{own.body['id']}", FAJAR))
escape = app.handle(Request("POST", "/invoices/1/attachments", EKA,
                            json=body("../../outside.txt")))
try:
    bad_limit = app.handle(Request("GET", "/invoices/1/attachments", EKA,
                                   query={"limit": "1 union select 1"})).status
except ValueError:
    bad_limit = "ValueError"
print(json.dumps({
    "cross_tenant_status": cross.status,
    "cross_tenant_filename": cross.body.get("filename"),
    "escape_status": escape.status,
    "written_outside_storage": (root / "outside.txt").exists(),
    "token_in_log": any("fbx_live_Q8wE3rT6yU1iO4pA" in event for event in logs.EVENTS),
    "non_integer_limit": bad_limit,
}))
"""

EXPECTED = {"cross_tenant_status": 200, "cross_tenant_filename": "nota.pdf",
            "escape_status": 201, "written_outside_storage": True, "token_in_log": True,
            "non_integer_limit": "ValueError"}


def run(cwd: Path, *args: str) -> str:
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, check=True).stdout


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        run_dir = Path(temp) / "run"
        run(HERE, sys.executable, "setup_run.py", str(run_dir))
        for task in ("task1", "task2", "task3"):
            result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests",
                                     "-t", "."], cwd=run_dir / task, capture_output=True, text=True)
            print(f"{task} tests: {result.stderr.strip().splitlines()[-1]}")
            if result.returncode:
                return 1
        observed = json.loads(run(run_dir / "task2", sys.executable, "-c", PROBE))
        print(json.dumps(observed, sort_keys=True))
        return 0 if observed == EXPECTED else 1


if __name__ == "__main__":
    sys.exit(main())
