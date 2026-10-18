import hashlib
import json
import platform
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/build/andino-unified-candidate-v3')
INPUT = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/docs/validation/andino-unified/actor-inputs-v2/batch-3.json')
FOCUS = Path('C:/Users/Lenovo/.agents/skills/focus')
SEED = json.loads((OUT / 'record_seed.json').read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def identity(path):
    return {'path': str(path).replace('\\', '/'), 'sha256': sha(path)}

def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

common = [
    {'id': 'andino-workflow', **identity(ROOT / 'SKILL.md'), 'state': 'USED',
     'action': 'Applied phase-local routing and permission boundaries to 38 raw snapshots and owned untracked review bytes.'},
    {'id': 'focus', **identity(FOCUS / 'SKILL.md'), 'state': 'USED',
     'action': 'Loaded installed skill and all three communication references; used for bounded factual progress/report wording.'},
]
references = [identity(ROOT / 'references' / x) for x in
              ['routing.md', 'internal-method-index.md', 'invocation-adapter.md']]
references += [identity(FOCUS / 'references' / x) for x in
               ['priority-a.md', 'human-language-indonesia.md', 'human-language-english.md']]
cases = []
for case_id, methods, note in SEED['rows']:
    selected = []
    for method in methods:
        path = (Path('C:/Users/Lenovo/.agents/skills/search-first/SKILL.md') if method == 'search-first'
                else ROOT / 'skills' / method / 'GUIDE.md')
        selected.append({'id': method, **identity(path), 'state': 'ACTIVE',
                         'reason': note, 'insight': SEED['insights'][method]})
    cases.append({'id': case_id, 'selected': selected, 'unavailable': [],
                  'note': note + ' Selection snapshot only; no scenario action executed.'})
results = {
    'batch': 3, 'host_surface': 'Codex delegated agent', 'model_version': 'UNKNOWN',
    'scope': 'Resource activation and the supplied review fixture only; no scenario actions.',
    'input': identity(INPUT), 'common_activation': common, 'references_read': references,
    'selection_results': cases,
    'actual_work_methods': [
        {'id': m, **identity(ROOT / 'skills' / m / 'GUIDE.md'), 'state': 'USED', 'action': action}
        for m, action in [('code-review', 'Separate spec/standards review of exact candidate bytes, literal cases and isolated admin mutation.'),
                          ('verification', 'Recorded commands/exits/results and confirmed candidate hash/source equality after checks.')]],
    'limits': ['No native picker test or cross-host parity claim.',
               'All per-case ACTIVE states mean actual full guide instruction reads, not execution of the scenario.',
               'No external source research, service call, Git operation, schedule, installation or nested spawning.'],
}
candidate = OUT / 'candidate.py'
raw = json.loads(INPUT.read_text(encoding='utf-8'))['work']['files']['candidate.py'].encode('utf-8')
assert candidate.read_bytes() == raw
review = {
    'request': 'Review supplied candidate.py as an uncommitted new file without repair.',
    'scope': {'baseline': 'absent file; complete supplied owned new-file bytes',
              'candidate': identity(candidate), 'byte_count': len(raw),
              'new_file_scope_supplied': True, 'git_status_not_queried': True},
    'spec': 'Admins may open every record; members may open only records from their own organization.',
    'standard': 'Never evaluate user input dynamically.',
    'spec_verdict': 'FAIL', 'standards_verdict': 'FAIL',
    'findings': [
        {'id': 'F1', 'axis': 'spec', 'severity': 'P1', 'file': str(candidate).replace('\\', '/'), 'line': 3,
         'title': 'Member organization predicate is inverted',
         'trigger': 'member org A with record org B; also member org A with record org A',
         'actual': 'Cross-organization record allowed; own-organization record denied.',
         'expected': 'Cross-organization record denied; own-organization record allowed.',
         'consequence': 'Members can access records outside their organization and cannot open their own records.',
         'evidence': 'Literal member_other_org and member_own_org cases both fail; both admin cases pass.',
         'concrete_remedy': 'Use an own-organization equality condition for members while retaining the admin rule. No repair performed.',
         'verification_gap': 'Only supplied admin/member dictionary domain is covered; unspecified roles and malformed data are outside this spec.'},
        {'id': 'F2', 'axis': 'standards', 'severity': 'P2', 'file': str(candidate).replace('\\', '/'), 'line': 2,
         'title': 'Role input is routed through dynamic eval',
         'trigger': 'Every can_open call evaluates repr(user["role"]) with eval.',
         'actual': 'Dynamic evaluator consumes a representation derived from user input.',
         'expected': 'Use the role value without dynamic evaluation.',
         'consequence': 'Violates the explicit hard standard and retains an unnecessary dynamic execution surface.',
         'evidence': 'AST finds an eval Call at line 2; direct source inspection confirms input lineage.',
         'concrete_remedy': 'Remove dynamic evaluation and use validated role data directly. No repair performed.',
         'verification_gap': 'Arbitrary code execution from ordinary string role values was not demonstrated; repr quotes those values. Finding is the explicit standards violation.'},
    ],
    'checks': SEED['fixtureResults'],
    'independent_oracle': 'Four literal expected booleans derived directly from the two role rules, not calculated from candidate logic.',
    'mutation': {'artifact': identity(OUT / 'candidate_mutant.py'),
                 'change': 'Only the disposable copy replaces the admin equality branch with False.',
                 'result': 'admin_own_org changes from PASS to FAIL; three total failures, proving admin acceptance sensitivity.',
                 'original_unchanged': True},
    'candidate_preserved': candidate.read_bytes() == raw,
    'candidate_post_checks_sha256': sha(candidate),
    'runtime': {'python': platform.python_version(), 'platform': platform.platform()},
    'limits': ['No repairs, production changes, real Git operations or live authorization environment tested.',
               'AST rule check is appropriate to this exact three-line supplied fixture; it is not a general dynamic-input analyzer.'],
}
dump('review.json', review)
dump('results.json', results)
work = {
    'host_surface': 'Codex delegated agent', 'model_version': 'UNKNOWN',
    'current_state': 'COMPLETE: 38 selection snapshots recorded; supplied review completed and candidate preserved.',
    'current_phase': 'Verified resource selection and fixture review',
    'decisions': ['No scenario actions; only reads and owned fixture artifacts in this directory.',
                  'Use literal role/organization cases and separate AST/source standards review.',
                  'No repair; mutation occurs solely in a separately named disposable copy.'],
    'evidence': {'input': identity(INPUT), 'candidate': identity(candidate),
                 'harness': identity(OUT / 'test_review.py'),
                 'review': identity(OUT / 'review.json'), 'results': identity(OUT / 'results.json')},
    'commands': SEED['fixtureResults'],
    'record_command': 'rtk proxy python write_records.py',
    'candidate_matches_input_bytes': candidate.read_bytes() == raw,
    'spec_result': '2 PASS, 2 FAIL; exit 1', 'standards_result': 'FAIL line 2; exit 1',
    'mutation_result': '1 PASS, 3 FAIL; exit 1; admin_own_org newly fails',
    'errors': [
        {'operation': 'Initial RTK instruction read', 'detail': 'Get-Content was invoked before learning the RTK prefix requirement; subsequent shell commands were prefixed.'},
        {'operation': 'PowerShell batched guide read', 'detail': 'Nested variable interpolation produced a parser error. No guide activation claimed from that attempt; corrected with Python.'},
        {'operation': 'First Python multi-guide read', 'detail': 'cp1252 stdout could not encode an arrow after complete code-review output. Subsequent full guide reads explicitly configured UTF-8.'},
        {'operation': 'Oversized combined read output', 'detail': 'Tool output truncated combined reads. Root/routing/index and priority were reread in bounded calls; no missing full-read claims used.'},
    ],
    'limits': results['limits'], 'next_action': 'Parent inspects these artifacts and integrates evaluation evidence; no scenario execution authorized.',
}
dump('work.json', work)
print(json.dumps({'selection_cases': len(cases), 'spec_verdict': review['spec_verdict'],
                  'standards_verdict': review['standards_verdict'], 'candidate_preserved': True,
                  'candidate_sha256': sha(candidate),
                  'artifacts': [identity(OUT / x) for x in ['results.json', 'review.json', 'work.json']]}, indent=2))
