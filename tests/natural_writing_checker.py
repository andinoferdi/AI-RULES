"""Load the Natural Writing checker shipped in the skill package.

The checker lives in the `natural-writing` skill (`skills/natural-writing/scripts/check.py`),
so a change to the checker and the tests that use it land in one commit.
Set NATURAL_WRITING_CHECKER to another check.py to test a different copy.
"""
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "skills" / "natural-writing" / "scripts" / "check.py"


def checker_path() -> Path:
    override = os.environ.get("NATURAL_WRITING_CHECKER")
    return Path(override) if override else CHECKER


def load_checker():
    path = checker_path()
    spec = importlib.util.spec_from_file_location("natural_writing_check", path)
    module = importlib.util.module_from_spec(spec)
    # dataclasses look the module up in sys.modules while the class is created (Python 3.12).
    sys.modules[spec.name] = module
    # Keep skills/ free of __pycache__ folders.
    previous, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module
