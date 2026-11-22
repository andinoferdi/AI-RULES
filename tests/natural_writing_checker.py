"""Load the Natural Writing checker shipped in the pinned skill package.

The checker lives in the `natural-writing` skill (`scripts/check.py`), not on
main, so main's tests read it from the commit pinned in the release manifest.
The commit must be present locally; `git fetch` of the skill branch provides it.
Set NATURAL_WRITING_CHECKER to a local check.py to test an unpinned copy.
"""
import importlib.util
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src" / "ai_rules" / "release" / "data" / "release_manifest.json"
_CACHE = {}


def checker_path() -> Path:
    override = os.environ.get("NATURAL_WRITING_CHECKER")
    if override:
        return Path(override)
    if "path" not in _CACHE:
        ref = json.loads(MANIFEST.read_text(encoding="utf-8"))["first_party"]["natural-writing"]["commit"]
        result = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:scripts/check.py"],
                                capture_output=True, text=True, encoding="utf-8")
        if result.returncode:
            raise RuntimeError(f"cannot read scripts/check.py from {ref}: {result.stderr.strip()}")
        directory = Path(tempfile.mkdtemp(prefix="nw-checker-"))
        path = directory / "check.py"
        path.write_text(result.stdout, encoding="utf-8", newline="\n")
        _CACHE["path"] = path
    return _CACHE["path"]


def load_checker():
    path = checker_path()
    spec = importlib.util.spec_from_file_location("natural_writing_check", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
