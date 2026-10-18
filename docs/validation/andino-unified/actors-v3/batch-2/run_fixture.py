import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/docs/validation/andino-unified/actor-inputs-v2/batch-2.json')
WORK = ROOT / 'work.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(work):
    WORK.write_text(json.dumps(work, indent=2) + '\n', encoding='utf-8')


def run(work, name, args):
    command = ['rtk', 'proxy', sys.executable, '-B', *args]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = result.stdout + result.stderr
    (ROOT / (name + '.log')).write_text(output, encoding='utf-8')
    event = {'name': name, 'command': command, 'cwd': str(ROOT),
             'timestamp_utc': datetime.now(timezone.utc).isoformat(),
             'exit_code': result.returncode, 'stdout': result.stdout,
             'stderr': result.stderr,
             'subject_sha256': digest(ROOT / 'subject.py')}
    work['commands'].append(event)
    save(work)
    print(json.dumps(event, indent=2))
    return result


def prepare():
    source = json.loads(INPUT.read_text(encoding='utf-8-sig'))['work']['files']['subject.py']
    for name in ('subject.py', 'subject.before.py'):
        path = ROOT / name
        if path.exists():
            raise RuntimeError('Refusing to overwrite existing fixture: ' + str(path))
        path.write_bytes(source.encode('utf-8'))
    oracle = {'source': 'Raw user contract: zero-based consecutive non-overlapping pages.',
              'items': ['A', 'B', 'C', 'D'], 'size': 2,
              'literal_expected_pages': [['A', 'B'], ['C', 'D'], []],
              'independence': 'Expected letters transcribed from the contract, not calculated using production arithmetic.'}
    (ROOT / 'oracle.json').write_text(json.dumps(oracle, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'reproduce.py').write_text('from subject import page\nprint(repr([page(["A", "B", "C", "D"], i, 2) for i in (0, 1)]))\n', encoding='utf-8')
    (ROOT / 'test_page.py').write_text('''import os
import runpy
import unittest

page = runpy.run_path(os.environ.get('PAGE_SUBJECT', 'subject.py'))['page']


class PaginationContract(unittest.TestCase):
    def test_consecutive_zero_based_pages(self):
        items = ['A', 'B', 'C', 'D']
        self.assertEqual(page(items, 0, 2), ['A', 'B'])
        self.assertEqual(page(items, 1, 2), ['C', 'D'])
        self.assertEqual(page(items, 2, 2), [])


if __name__ == '__main__':
    unittest.main()
''', encoding='utf-8')
    work = {'request': json.loads(INPUT.read_text(encoding='utf-8-sig'))['work']['request'],
            'host': 'Codex delegated agent', 'model': 'UNKNOWN', 'version': 'UNKNOWN',
            'runtime': {'python': platform.python_version(), 'executable': sys.executable},
            'scope': str(ROOT), 'status': 'IN_PROGRESS', 'plan_density': 'LITE',
            'current_state': 'Baseline source preserved byte-for-byte from supplied fixture; independent literal oracle and regression ready.',
            'current_phase': 'reproduce',
            'next_action': 'Run reproduce.py against subject.py, then run unittest to observe the contract assertion fail.',
            'acceptance': ['Actual first/second page symptom reproduced.', 'Falsifiable stride hypothesis tested before source fix.', 'Observed intended RED then GREEN on public page seam.', 'Same regression fails preserved faulty copy after GREEN.'],
            'before': {'path': str(ROOT / 'subject.before.py'), 'sha256': digest(ROOT / 'subject.before.py'), 'source': source},
            'oracle': oracle, 'commands': [], 'decisions': [], 'errors': [],
            'limits': ['Only supplied fixture tested; no user project or project-wide suite inspected.', 'No network, services, native picker, Git mutations or cross-host execution.']}
    save(work)
    result = run(work, 'reproduction', ['reproduce.py'])
    if result.returncode != 0 or result.stdout.strip() != "[['A', 'B'], ['B', 'C']]":
        raise RuntimeError('Reported symptom was not reproduced as expected; inspect work.json')
    work['observed_symptom'] = [['A', 'B'], ['B', 'C']]
    result = run(work, 'red', ['-m', 'unittest', '-v', 'test_page'])
    if result.returncode == 0 or "['B', 'C'] != ['C', 'D']" not in result.stderr:
        raise RuntimeError('RED did not fail the intended assertion')
    work['current_phase'] = 'hypothesis'
    work['current_state'] = 'Reported overlap reproduced; public regression failed with B,C instead of C,D.'
    work['hypothesis'] = {'statement': 'The page stride is size-1 instead of size, so the second page starts at B.',
                          'prediction': 'Changing only the stride multiplier to size yields A,B then C,D and an empty third page.',
                          'status': 'TO_TEST'}
    work['next_action'] = 'Probe changing only the stride in an isolated namespace against literal expected pages.'
    save(work)


def probe():
    work = json.loads(WORK.read_text(encoding='utf-8'))
    (ROOT / 'probe_hypothesis.py').write_text('''from pathlib import Path
source = Path('subject.before.py').read_text()
assert 'index * (size - 1)' in source
candidate = source.replace('index * (size - 1)', 'index * size', 1)
namespace = {}
exec(candidate, namespace)
pages = [namespace['page'](['A', 'B', 'C', 'D'], i, 2) for i in (0, 1, 2)]
assert pages == [['A', 'B'], ['C', 'D'], []], pages
print({'changed_variable': 'stride only', 'observed_pages': pages, 'prediction': 'confirmed'})
''', encoding='utf-8')
    result = run(work, 'hypothesis', ['probe_hypothesis.py'])
    if result.returncode != 0:
        raise RuntimeError('Hypothesis was not confirmed')
    work['hypothesis']['status'] = 'CONFIRMED_IN_ISOLATED_PROBE'
    work['current_phase'] = 'fix'
    work['current_state'] = 'Stride-only probe matched the independent literal oracle; production fixture unchanged.'
    work['next_action'] = 'Change the single stride expression in subject.py, run focused regression and fixture suite.'
    save(work)


def verify():
    work = json.loads(WORK.read_text(encoding='utf-8'))
    result = run(work, 'green', ['-m', 'unittest', '-v', 'test_page'])
    if result.returncode != 0:
        raise RuntimeError('GREEN failed')
    result = run(work, 'suite', ['-m', 'unittest', 'discover', '-v'])
    if result.returncode != 0:
        raise RuntimeError('Fixture suite failed')
    (ROOT / 'faulty_copy_sensitivity.py').write_text('''import os
import runpy
os.environ['PAGE_SUBJECT'] = 'subject.before.py'
runpy.run_path('test_page.py', run_name='__main__')
''', encoding='utf-8')
    result = run(work, 'faulty_copy_sensitivity', ['faulty_copy_sensitivity.py'])
    if result.returncode == 0 or "['B', 'C'] != ['C', 'D']" not in result.stderr:
        raise RuntimeError('Faulty copy did not fail expected assertion')
    result = run(work, 'original_scenario_after_fix', ['reproduce.py'])
    if result.returncode != 0 or result.stdout.strip() != "[['A', 'B'], ['C', 'D']]":
        raise RuntimeError('Original scenario still wrong')
    work['after'] = {'path': str(ROOT / 'subject.py'), 'sha256': digest(ROOT / 'subject.py'), 'source': (ROOT / 'subject.py').read_text()}
    work['root_cause'] = {'status': 'CONFIRMED', 'finding': 'The stride subtracts one from each page size, overlapping consecutive pages.'}
    work['decisions'] += ['One expression fixed at the supplied public seam; no negative-index/size policy invented.', 'No refactor: the corrected function is already minimal.']
    work['hashes'] = {p.name: digest(p) for p in ROOT.iterdir() if p.is_file() and p.name != 'work.json'}
    work['status'] = 'DONE'
    work['current_phase'] = 'complete'
    work['current_state'] = 'Exact symptom fixed; literal regression and fixture suite pass; preserved faulty copy fails the same assertion.'
    work['next_action'] = 'None — fixture task complete.'
    save(work)
    print('DONE: observed RED, hypothesis confirmed, GREEN, fixture suite pass, faulty-copy sensitivity fail as intended.')


if __name__ == '__main__':
    {'prepare': prepare, 'probe': probe, 'verify': verify}[sys.argv[1]]()
