import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
RAW = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/docs/validation/andino-unified/actor-inputs-v2/batch-1.json')
fixture = json.loads(RAW.read_text(encoding='utf-8'))['work']
subject = ROOT / 'subject.py'
original = fixture['files']['subject.py'].encode('utf-8')
subject.write_bytes(original)
(ROOT / 'subject.before.py').write_bytes(original)
test = ROOT / 'test_subject.py'
test.write_text('import unittest\nfrom subject import sum_invoice\n\nclass Contract(unittest.TestCase):\n    def test_known_invoice(self):\n        self.assertEqual(sum_invoice([10, 5]), 15)\n', encoding='utf-8')
records = []

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(label, cwd, args):
    command = ['rtk', 'proxy', sys.executable, '-B', '-m', 'unittest', '-v', *args]
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    entry = {'label': label, 'command_argv': command, 'command': subprocess.list2cmdline(command), 'cwd': str(cwd), 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr, 'subject_sha256': digest(cwd / 'subject.py'), 'test_sha256': digest(cwd / 'test_subject.py')}
    records.append(entry)
    print(json.dumps(entry))
    return result

red = run('RED_known_invoice', ROOT, ['test_subject.Contract.test_known_invoice'])
if red.returncode != 1 or '0 != 15' not in red.stderr:
    raise RuntimeError('RED did not fail for the intended assertion')
subject.write_text('def sum_invoice(values):\n    return sum(values)\n', encoding='utf-8')
green = run('GREEN_known_invoice', ROOT, ['test_subject.Contract.test_known_invoice'])
if green.returncode:
    raise RuntimeError('GREEN failed')
with test.open('a', encoding='utf-8') as stream:
    stream.write('\n    def test_empty_invoice(self):\n        self.assertEqual(sum_invoice([]), 0)\n')
suite = run('GREEN_complete_local_suite', ROOT, ['test_subject'])
if suite.returncode:
    raise RuntimeError('Complete local suite failed')
faulty = ROOT / 'faulty-copy'
faulty.mkdir(exist_ok=False)
shutil.copy2(test, faulty / 'test_subject.py')
(faulty / 'subject.py').write_text('def sum_invoice(values):\n    return values[0] if values else 0\n', encoding='utf-8')
sensitivity = run('FAULTY_COPY_sensitivity', faulty, ['test_subject'])
if sensitivity.returncode != 1 or '10 != 15' not in sensitivity.stderr:
    raise RuntimeError('Faulty copy did not fail as intended')
record = {'request': fixture['request'], 'status': 'PASS', 'runtime': sys.version, 'seam': 'sum_invoice(values)', 'before': {'path': str(ROOT / 'subject.before.py'), 'bytes_base64': base64.b64encode(original).decode(), 'text': original.decode(), 'sha256': hashlib.sha256(original).hexdigest()}, 'accepted_contract': ['sum_invoice([10,5]) == 15', 'sum_invoice([]) == 0', 'public function name and argument preserved'], 'records': records, 'prior_harness_error': {'command': 'rtk proxy C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -B -m unittest -v discover -s . -p test_subject.py', 'cwd': str(ROOT), 'exit_code': 2, 'stderr': 'python.exe -m unittest: error: unrecognized arguments: -s . -p test_subject.py', 'subject_sha256': digest(subject), 'test_sha256': digest(test), 'resolution': 'Use module test_subject for the two-test local suite; no production change. Earlier known-invoice RED and GREEN were valid; repeated after harness repair.'}, 'after': {'subject_sha256': digest(subject), 'test_sha256': digest(test), 'source': subject.read_text(encoding='utf-8')}, 'red_green': 'Observed 0 != 15 on original bytes, then passing known-invoice test on minimal implementation.', 'empty_case': 'Added after first GREEN and passed; original stub already satisfies empty input, so no fabricated empty-input RED.', 'mutation': 'Faulty copy returns only first amount; the same two tests expose 10 != 15 while empty still passes.', 'refactor': 'Not needed; minimal implementation already uses the standard sum operation.', 'limits': 'Only supplied isolated Python contract tested. No repository integration, network, service, Git, host parity or future model behavior claim.'}
(ROOT / 'work.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
