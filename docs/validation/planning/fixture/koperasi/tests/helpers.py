import contextlib
import io
import json
import os
import tempfile
from typing import List, Tuple

from koperasi.cli import main


def run_cli(args: List[str]) -> Tuple[int, str, str]:
    """Run the CLI in-process and return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(args)
        except SystemExit as exc:  # argparse errors
            code = exc.code
    return code, out.getvalue(), err.getvalue()


def write_data(loans: list) -> str:
    """Write a temporary data file holding `loans` and return its path."""
    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    with handle:
        json.dump({"loans": loans}, handle)
    return handle.name


def remove(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
