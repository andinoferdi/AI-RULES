from pathlib import Path
import argparse
import re
import subprocess
import sys
import tempfile
import textwrap

parser = argparse.ArgumentParser(description='Run literal planning example blocks together')
parser.add_argument('--runtime', type=Path, required=True)
document = (parser.parse_args().runtime / 'skills/planning/resources/worked-example.md').read_text(encoding='utf-8')
blocks = re.findall(r'```python\n(.*?)\n```', document, re.S)
assert len(blocks) == 5
with tempfile.TemporaryDirectory(prefix='andino-planning-example-') as temporary:
    root = Path(temporary)
    package = root / 'inventory'
    package.mkdir()
    (package / '__init__.py').write_text('')
    (package / 'store.py').write_text('def list_items():\n    return []\n')
    tests = root / 'tests'
    tests.mkdir()
    setup = '''import csv
import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from inventory.cli import main


def run_cli(argv, items):
    output = io.StringIO()
    with patch('inventory.cli.list_items', return_value=items), redirect_stdout(output):
        code = main(argv)
    return code, output.getvalue()


class CliTests(unittest.TestCase):
    def test_json_default(self):
        code, output = run_cli(['list'], [{'id': '1', 'name': 'Tea, green'}])
        self.assertEqual(0, code)
        self.assertEqual([{'id': '1', 'name': 'Tea, green'}], json.loads(output))
'''
    for stage in (1, 2):
        parser = blocks[0]
        if stage == 2:
            parser += "\nlist_parser.add_argument('--name', default=None)"
        rendering = blocks[1]
        if stage == 2:
            rendering = rendering.replace('rows = list_items()', 'rows = list_items()\n' + blocks[3])
        main = 'import argparse\nimport json\nimport csv\nimport sys\nfrom inventory.store import list_items\n\ndef main(argv):\n    parser = argparse.ArgumentParser()\n    subparsers = parser.add_subparsers(dest="command", required=True)\n'
        main += textwrap.indent(parser, '    ') + '\n    args = parser.parse_args(argv)\n'
        main += textwrap.indent(rendering, '    ') + '\n    return 0\n'
        (package / 'cli.py').write_text(main, encoding='utf-8')
        content = setup + '\n' + textwrap.indent(blocks[2], '    ')
        if stage == 2:
            content += '\n' + textwrap.indent(blocks[4], '    ')
        (tests / 'test_cli.py').write_text(content, encoding='utf-8')
        result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=root, capture_output=True, text=True)
        print(f'Stage {stage}: exit {result.returncode}\n{result.stderr}')
        assert result.returncode == 0
print('PASS: literal worked-example code and assertion blocks execute together')
