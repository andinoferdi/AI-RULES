"""Run the hidden checks on one finished run and print the result as Markdown.

For each task, in a temporary copy of the run's repository:
- behaviour: the public API on cases the runner was not told about;
- sensitivity: the runner's final test suite run against the production code before the
  change (task1, task2) or before ACC-212 (task3); a guarding test must fail there;
- suite: the runner's final test suite on the final code.

    python check_run.py RUN_DIR
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TASKS = {
    "task1": {"test": ["python", "scripts/test.py"], "prod": ["src"]},
    "task2": {"test": ["python", "run_tests.py"], "prod": ["invoices"]},
    "task3": {"test": ["python", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"],
              "prod": ["accounts"]},
}

TASK1_PROBE = r"""
import sys
from datetime import datetime, timedelta
sys.path[:0] = ["src", "."]
from garage.billing import fee_for_stay
from garage.clock import FixedClock
from garage.tickets import TicketDesk
from tests.helpers import RecordingSms
E = datetime(2026, 12, 1, 8, 0)
cases = [
    ("car 15 min", dict(minutes=15), "car", 0),
    ("car 15 min 1 s", dict(minutes=15, seconds=1), "car", 5000),
    ("car 16 min", dict(minutes=16), "car", 5000),
    ("car 2 h", dict(hours=2), "car", 8500),
    ("car 25 h", dict(hours=25), "car", 45000),
    ("motorbike 15 min", dict(minutes=15), "motorbike", 0),
    ("motorbike 40 min", dict(minutes=40), "motorbike", 2500),
    ("motorbike 2 h (half of 8.500 = 4.250, up to 4.500)", dict(hours=2), "motorbike", 4500),
    ("motorbike 20 h (cap)", dict(hours=20), "motorbike", 20000),
    ("motorbike 30 h (half of 62.500 = 31.250, up to 31.500)", dict(hours=30), "motorbike", 31500),
]
for name, delta, vehicle, want in cases:
    try:
        got = fee_for_stay(E, E + timedelta(**delta), vehicle)
    except Exception as exc:
        got = f"{type(exc).__name__}: {exc}"
    print(f"- {name}: expected {want}, got {got} {'OK' if got == want else 'WRONG'}")
try:
    clock, sms = FixedClock(E), RecordingSms()
    desk = TicketDesk(clock, sms)
    ticket = desk.open_ticket("B 4321 ZZ", "motorbike", "0813-0000-0000")
    clock.advance(hours=2)
    closed = desk.close_ticket(ticket.id)
    ok = closed.fee == 4500 and "Rp 4.500" in sms.sent[-1][1]
    print(f"- close_ticket motorbike 2 h: fee {closed.fee}, sms {sms.sent[-1][1]!r} {'OK' if ok else 'WRONG'}")
except Exception as exc:
    print(f"- close_ticket motorbike 2 h: {type(exc).__name__}: {exc} WRONG")
"""

TASK2_PROBE = r"""
import subprocess, sys
sys.path.insert(0, ".")
from invoices.render import Invoice
cases = [
    ("INV-2026-0412 lines (subtotal 99.999)", [("a", 1, 33333)] * 3, 11000),
    ("one line 99.999", [("a", 1, 99999)], 11000),
    ("subtotal 150 (16,50 rounds half up)", [("a", 1, 150)], 17),
    ("subtotal 50 (5,50)", [("a", 1, 50)], 6),
    ("subtotal 250 (27,50)", [("a", 1, 250)], 28),
    ("two lines 75 + 75 (per-line 8,25 + 8,25; on subtotal 16,50)", [("a", 1, 75), ("b", 1, 75)], 17),
    ("INV-2026-0398 (510.000)", [("a", 10, 48000), ("b", 20, 1500)], 56100),
]
for name, lines, want in cases:
    try:
        got = Invoice("X", lines).tax
    except Exception as exc:
        got = f"{type(exc).__name__}: {exc}"
    print(f"- {name}: expected {want}, got {got} {'OK' if got == want else 'WRONG'}")
out = subprocess.run([sys.executable, "-m", "invoices.render", "INV-2026-0412"],
                     capture_output=True, text=True).stdout
print("- reporter's command output:")
print("\n".join("    " + line for line in out.splitlines()))
"""


def run(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", **kw)


def suite_summary(cmd, cwd) -> str:
    result = run([sys.executable if c == "python" else c for c in cmd], cwd)
    lines = (result.stdout + result.stderr).splitlines()
    picked = [l for l in lines if l.rstrip().endswith(("FAIL", "ERROR")) or l.startswith(
        ("Ran ", "OK", "FAILED", "FAIL:", "ERROR:"))]
    return "\n".join("    " + l for l in picked) or "    (no output)"


def main() -> int:
    run_dir = Path(sys.argv[1]).resolve()
    bases = json.loads(run_dir.with_name(run_dir.name + ".bases.json").read_text(encoding="utf-8"))
    report = ["# Hidden checks"]
    for task, spec in TASKS.items():
        repo = run_dir / task
        report.append(f"\n## {task}")
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / task
            shutil.copytree(repo, copy, ignore=shutil.ignore_patterns("__pycache__"))
            if task == "task1":
                report.append("Behaviour on the final code:")
                probe = run([sys.executable, "-c", TASK1_PROBE], copy)
                report.append((probe.stdout + probe.stderr).rstrip())
            elif task == "task2":
                report.append("Behaviour on the final code:")
                probe = run([sys.executable, "-c", TASK2_PROBE], copy)
                report.append((probe.stdout + probe.stderr).rstrip())
            else:
                changed = run(["git", "diff", "--stat", bases["task3"], "--", "accounts"], copy).stdout
                report.append("Production code changed against the ACC-212 commit: "
                              + (changed.strip() or "no"))
                status = run(["git", "status", "--porcelain"], copy).stdout.strip()
                head = run(["git", "log", "--oneline", "-3"], copy).stdout.strip()
                report.append("git log -3:\n    " + head.replace("\n", "\n    "))
                report.append("git status --porcelain:\n    " + (status.replace("\n", "\n    ") or "(clean)"))
            report.append("Final suite on the final code:")
            report.append(suite_summary(spec["test"], copy))
            old = bases["task3-pre-fix"] if task == "task3" else bases[task]
            for path in spec["prod"]:
                run(["git", "checkout", old, "--", path], copy)
            label = "before ACC-212" if task == "task3" else "before the change (baseline)"
            report.append(f"Final suite against the production code {label}:")
            report.append(suite_summary(spec["test"], copy))
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
