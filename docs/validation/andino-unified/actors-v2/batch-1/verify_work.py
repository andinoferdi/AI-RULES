import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

original = b"def sum_invoice(values):\n    return 0\n"
assert (ROOT / "subject.before.py").read_bytes() == original
test_bytes = (ROOT / "test_subject.py").read_bytes()
events = []
for name, code, expected_exit in [
    ("final", None, 0),
    ("faulty_zero", original, 1),
    ("faulty_empty", b"def sum_invoice(values):\n    return sum(values) if values else 1\n", 1),
]:
    folder = ROOT if code is None else ROOT / name
    if code is not None:
        folder.mkdir(exist_ok=True)
        (folder / "subject.py").write_bytes(code)
        (folder / "test_subject.py").write_bytes(test_bytes)
    args = ["rtk", "proxy", sys.executable, "-B", "-m", "unittest", "-v", "test_subject"]
    result = subprocess.run(args, cwd=folder, text=True, capture_output=True)
    event = {"phase": name, "command": subprocess.list2cmdline(args), "cwd": str(folder),
             "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
             "subject_sha256": sha(folder / "subject.py"), "test_sha256": sha(folder / "test_subject.py")}
    events.append(event)
    assert result.returncode == expected_exit, event
    if name == "faulty_zero":
        assert "0 != 15" in result.stderr
    if name == "faulty_empty":
        assert "1 != 0" in result.stderr

evidence = {"request": "sum_invoice([10,5]) returns 15; empty input returns 0",
    "status": "PASS", "scope": "Local supplied pure-Python fixture only",
    "public_seam": "sum_invoice(values)", "oracle": {"independent": True, "source": "Literal user contract, no expected-value calculation through production sum", "cases": [{"input": [10, 5], "expected": 15}, {"input": [], "expected": 0}]},
    "before": {"path": str(ROOT / "subject.before.py"), "sha256": sha(ROOT / "subject.before.py"), "bytes_preserved_exactly": True},
    "red": {"command": "rtk proxy python -B -m unittest -v test_subject", "cwd": str(ROOT), "exit_code": 1,
        "output": "test_integer_invoice ... FAIL\nAssertionError: 0 != 15\nRan 1 test\nFAILED (failures=1)", "output_kind": "Bounded exact observed failure excerpt; complete initial RED is in actor tool transcript", "subject_sha256": sha(ROOT / "subject.before.py"),
        "test_source": "import unittest\n\nfrom subject import sum_invoice\n\n\nclass InvoiceContract(unittest.TestCase):\n    def test_integer_invoice(self):\n        self.assertEqual(sum_invoice([10, 5]), 15)\n\n\nif __name__ == \"__main__\":\n    unittest.main()\n"},
    "first_green": {"command": "rtk proxy python -B -m unittest -v test_subject", "exit_code": 0, "output": "test_integer_invoice ... ok\nRan 1 test\nOK", "output_kind": "Bounded observed result excerpt; complete output in actor transcript"},
    "verification": events,
    "tested_hashes": {"subject.py": sha(ROOT / "subject.py"), "test_subject.py": sha(ROOT / "test_subject.py"), "verify_work.py": sha(Path(__file__))},
    "runtime": sys.version, "implementation": "return sum(values)",
    "refactor": "No refactor was needed; direct minimal GREEN implementation preserves the public function.",
    "limits": ["No real repository, native picker or other host evaluated", "No input validation semantics outside the integer contract claimed", "No network or external services used"]}
evidence["red"]["test_sha256"] = hashlib.sha256(evidence["red"]["test_source"].encode()).hexdigest()
(ROOT / "work.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": evidence["status"], "runs": [{"phase": e["phase"], "exit": e["exit_code"]} for e in events], "tested_hashes": evidence["tested_hashes"]}, indent=2))
