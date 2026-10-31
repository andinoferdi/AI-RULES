import contextlib
import io
import json
from pathlib import Path
import unittest
from export import main


def run_cli(*options):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = main([str(Path(__file__).with_name("items.json")), *options])
    return code, output.getvalue()


class ExportTests(unittest.TestCase):
    def test_json_default(self):
        code, output = run_cli()
        self.assertEqual(0, code)
        self.assertEqual(4, len(json.loads(output)))

    def test_active_filter(self):
        code, output = run_cli("--state", "active")
        self.assertEqual(0, code)
        self.assertEqual(["b"], [row["id"] for row in json.loads(output)])
