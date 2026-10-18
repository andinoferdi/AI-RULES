import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
RAW = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/docs/validation/andino-unified/actor-inputs/batch-2.json')
FIXTURE = ROOT / 'fixture'
REPORT = ROOT / 'work.json'


def run(label, arguments, cwd=FIXTURE):
    result = subprocess.run([sys.executable, '-B', *arguments], cwd=cwd, capture_output=True, text=True)
    entry = {
        'label': label,
        'command': [sys.executable, '-B', *arguments],
        'cwd': str(cwd),
        'observed_at': datetime.now(timezone.utc).isoformat(),
        'exit_code': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
        'tested_files': {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(cwd.glob('*.py'))
        },
    }
    log = ROOT / (label + '.json')
    log.write_text(json.dumps(entry, indent=2) + '\n', encoding='utf-8')
    return entry


def baseline():
    if REPORT.exists():
        raise RuntimeError('Preserve existing report; baseline must not overwrite a prior run.')
    FIXTURE.mkdir(parents=True, exist_ok=False)
    files = json.loads(RAW.read_text(encoding='utf-8'))['work']['files']
    for name, content in files.items():
        destination = (FIXTURE / name).resolve()
        if not destination.is_relative_to(FIXTURE.resolve()):
            raise RuntimeError('Fixture path escapes owned directory')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding='utf-8')
    (ROOT / 'subject.before.py').write_bytes((FIXTURE / 'subject.py').read_bytes())
    (FIXTURE / 'test_page.py').write_text('''import unittest
from subject import page


class PaginationContract(unittest.TestCase):
    def test_reported_consecutive_pages(self):
        items = ['A', 'B', 'C', 'D']
        self.assertEqual(page(items, 0, 2), ['A', 'B'])
        self.assertEqual(page(items, 1, 2), ['C', 'D'])


if __name__ == '__main__':
    unittest.main()
''', encoding='utf-8')
    (FIXTURE / 'reproduce.py').write_text('''import json
from subject import page
items = ['A', 'B', 'C', 'D']
print(json.dumps({'first': page(items, 0, 2), 'second': page(items, 1, 2)}))
''', encoding='utf-8')
    (FIXTURE / 'probe_cause.py').write_text('''import json
from subject import page
items = ['A', 'B', 'C', 'D']
cases = [(1, ['B']), (2, ['C', 'D']), (3, ['D'])]
observations = []
for size, expected in cases:
    actual = page(items, 1, size)
    candidate_start = 1 * size
    candidate = items[candidate_start:candidate_start + size]
    observations.append({'size': size, 'actual': actual, 'expected': expected, 'candidate': candidate})
    assert actual != expected, 'Prediction requires the original incorrect stride'
    assert candidate == expected
print(json.dumps(observations))
''', encoding='utf-8')
    commands = [run('01-reproduce', ['reproduce.py']),
                run('02-red-exact-contract', ['-m', 'unittest', '-v', 'test_page.py']),
                run('03-hypothesis-stride-probe', ['probe_cause.py'])]
    assert commands[0]['exit_code'] == 0
    assert json.loads(commands[0]['stdout']) == {'first': ['A', 'B'], 'second': ['B', 'C']}
    assert commands[1]['exit_code'] == 1 and "['B', 'C'] != ['C', 'D']" in commands[1]['stderr']
    assert commands[2]['exit_code'] == 0
    report = {
        'runtime': {'python': sys.version, 'executable': sys.executable},
        'request': 'Zero-based pages must be consecutive non-overlapping slices.',
        'source': 'Exact supplied work.files subject.py copied into actor-owned fixture.',
        'commands': commands,
        'hypothesis': 'The stride uses size - 1; at index 1 this shifts the start one item left, and at size 1 every page starts at zero.',
        'prediction_and_probe': 'With size 1/2/3 and index 1, the original starts A/B/C; changing only stride to size starts B/C/D and gives the independently literal expected slices.',
        'status': 'REPRODUCED_AND_HYPOTHESIS_CONFIRMED',
        'limitations': ['Local Python fixture only; no live service, network, Git mutation or global configuration.'],
    }
    REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'checks': [(x['label'], x['exit_code']) for x in commands]}))


def verify():
    report = json.loads(REPORT.read_text(encoding='utf-8'))
    checks = [run('04-green-exact-contract', ['-m', 'unittest', '-v', 'test_page.py']),
              run('05-original-scenario-fixed', ['reproduce.py']),
              run('06-suite', ['-m', 'unittest', 'discover', '-v'])]
    mutation = ROOT / 'mutation'
    mutation.mkdir(exist_ok=False)
    (mutation / 'subject.py').write_bytes((ROOT / 'subject.before.py').read_bytes())
    (mutation / 'test_page.py').write_bytes((FIXTURE / 'test_page.py').read_bytes())
    checks.append(run('07-faulty-copy-sensitivity', ['-m', 'unittest', '-v', 'test_page.py'], cwd=mutation))
    assert all(check['exit_code'] == 0 for check in checks[:3])
    assert json.loads(checks[1]['stdout']) == {'first': ['A', 'B'], 'second': ['C', 'D']}
    assert checks[3]['exit_code'] == 1 and "['B', 'C'] != ['C', 'D']" in checks[3]['stderr']
    report['commands'].extend(checks)
    report['fix'] = 'Changed only start = index * (size - 1) to start = index * size.'
    report['refactor_decision'] = 'No refactor: no independent complexity concern is needed for this one-expression defect.'
    report['status'] = 'PASS'
    report['artifacts'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(ROOT.rglob('*.py'))}
    REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'checks': [(x['label'], x['exit_code']) for x in checks]}))


if __name__ == '__main__':
    {'baseline': baseline, 'verify': verify}[sys.argv[1]]()
