"""Run the acceptance checks the runners never see against a finished repository.

Each check prints PASS or FAIL with what was observed. The checks follow docs/spec.md:
R1 standard output and --out, R2 exact case-sensitive match, R3 columns and amounts,
R4 RFC 4180 quoting, R5 header only for an unknown customer, plus the whole suite.

    python hidden_check.py REPO
"""
import subprocess
import sys
import tempfile
from pathlib import Path

HEADER = "number,customer,amount\n"
CASES = [
    ("H1 Acme, Inc. to stdout", ["--customer", "Acme, Inc."],
     HEADER + 'INV-1001,"Acme, Inc.",1250.00\nINV-1005,"Acme, Inc.",-50.00\n'),
    ("H2 ACME, Inc. is another customer", ["--customer", "ACME, Inc."],
     HEADER + 'INV-1002,"ACME, Inc.",410.10\nINV-1006,"ACME, Inc.",300.00\n'),
    ("H3 lower case matches nobody", ["--customer", "acme, inc."], HEADER),
    ("H4 doubled quotes", ["--customer", 'Toko "Maju" Jaya'],
     HEADER + 'INV-1003,"Toko ""Maju"" Jaya",87.05\n'),
    ("H5 unknown customer", ["--customer", "Nobody"], HEADER),
]


def run(repo, args):
    """Standard output is compared with Windows text-mode line endings folded to \\n;
    the --out file (H6) is compared byte for byte."""
    result = subprocess.run([sys.executable, *args], cwd=repo, capture_output=True, timeout=60)
    result.stdout = result.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    result.stderr = result.stderr.decode("utf-8", "replace")
    return result


def main() -> int:
    repo = Path(sys.argv[1])
    failures = 0
    for name, extra, expected in CASES:
        result = run(repo, ["-m", "billing.cli", "export", *extra])
        ok = result.returncode == 0 and result.stdout == expected
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'} {name}: exit {result.returncode}, "
              f"stdout {result.stdout!r}" + (f", stderr {result.stderr[-300:]!r}" if not ok else ""))
    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp) / "acme.csv"
        result = run(repo, ["-m", "billing.cli", "export", "--customer", "Acme, Inc.",
                            "--out", str(target)])
        written = target.read_bytes().decode("utf-8") if target.exists() else None
        ok = result.returncode == 0 and written == CASES[0][2] and result.stdout == ""
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'} H6 --out writes the file: exit {result.returncode}, "
              f"file {written!r}, stdout {result.stdout!r}")
    suite = run(repo, ["-m", "unittest", "discover", "-s", "tests", "-t", "."])
    tail = suite.stderr.strip().splitlines()[-3:]
    ok = suite.returncode == 0
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} H7 whole suite: exit {suite.returncode}, {' | '.join(tail)}")
    version = run(repo, ["-c", "import billing; print(billing.__version__)"]).stdout.strip()
    print(f"INFO version: {version}")
    print(f"hidden checks failed: {failures}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
