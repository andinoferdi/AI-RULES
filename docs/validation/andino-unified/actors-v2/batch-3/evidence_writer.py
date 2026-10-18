import hashlib
import json
import platform
from pathlib import Path

ROOT = Path(r'C:\Users\Lenovo\Downloads\AI-RULES-main')
OUT = Path(__file__).resolve().parent
RUNTIME = ROOT / 'build/andino-unified-candidate-v2'
RAW = ROOT / 'docs/validation/andino-unified/actor-inputs-v2/batch-3.json'
data = json.loads(RAW.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

insights = {
    'implementation': 'Resolve the accepted task and ready frontier from integrated dependency evidence; implement one public behavior at a time without restarting settled decisions.',
    'tdd': 'Use one public seam and literal independent expected value; establish intended RED before minimal GREEN. Refactoring is a separate GREEN-only gate.',
    'incremental-implementation': 'Select the smallest dependency-ready complete path in the existing plan, serialize overlapping files, and stop dependent progress on a failed gate.',
    'git-operation-guard': 'Classify semantic publishing effect even with git -C; verify authority without executing push, and do not treat substring matching as enforcement.',
    'session-diagnostics': 'Confirm exact session identity and lineage, measure record sizes before bounded extraction, and separate observations from inferred causes.',
    'plain-language-repitch': 'Lead with practical meaning and one concrete example, preserve the original claim, and continue the authorized task without inventing file-edit authority.',
    'deep-module-design': 'Apply the deletion test to leaked policy and compare signatures, invariants, errors and caller simplicity; require a real second adapter before adding a port.',
    'pre-commit-setup': 'Inspect existing prepare/hooks and package manager, preserve them, and verify staged mutations only in a disposable fixture or isolated index without committing.',
    'primary-source-research': 'Define the consuming question, trace each material finding to the source that owns it, and retain version/date, contradictions and unknowns.',
    'code-review': 'Pin owned untracked bytes and exact lines, test literal requirements independently, and keep Spec and Standards verdicts separate.',
    'workflow-specification': 'Specify trigger, sources, outputs, human decisions, retries/idempotence, permissions and stopping without activating a schedule.',
    'decision-interview': 'Use existing evidence before one discriminating question about the concrete user moment; distinguish discoverable facts from user decisions.',
    'test-fixture-migration': 'Distinguish valid partial fixtures from deliberately malformed inputs; preserve negative-case wrongness and restrict helpers to tests.',
    'planning': 'Refine the existing plan with vertical slices, consumes/produces signatures, literal acceptance commands, an acyclic dependency graph and one NEXT ACTION.',
    'debugging': 'Reproduce the exact symptom and vary one input/config at a time before choosing a root fix; failed hypotheses change the investigation.',
    'verification': 'Bind each claim to current hashes, exact commands, observed cases and limitations; zero exit or old-tree green alone is insufficient.',
    'article-shaping': 'Keep the raw pile read-only, use a separate destination, ground prerequisite concepts, and offer opening choices without inventing lived evidence.',
    'api-and-interface-design': 'Atomically claim stable intent keys, reject payload mismatches, handle pending/unknown outcomes and verify concurrent duplicates; local DB uniqueness alone does not prove remote exactly-once.',
    'delivery': 'Report current acceptance and residual blockers with exact evidence; no-commit/no-push still permits an uncommitted factual handoff.',
    'code-simplification': 'Start GREEN, pin protected block hashes, preserve outputs/errors/effect order, and make one small change checked by unchanged tests.',
    'shipping-and-launch': 'Use real baseline/SLO and error budget to set advance/hold/rollback thresholds, pin candidate identity and recovery plan, and keep live rollout unexecuted without authority.',
    'deprecation-and-migration': 'Preserve mixed-version compatibility through expand, dual-write/backfill, read switch and later contract only after old consumers are gone.',
    'task-decomposition': 'Use complete independently verifiable tasks with genuine blocking edges; for wide renames expand, migrate caller batches, then contract.',
    'security-and-hardening': 'Map per-resource tenant authorization as a trust boundary and prioritize reachable disclosure; explicit dynamic-evaluation rules remain independently enforceable.',
}

# Each entry is an independent raw current-phase selection snapshot. No scenario is executed.
choices = [
    ([], 'Mechanical private rename; no framework/API fact, behavior change or migration is established.'),
    ([], 'Already-approved ready tickets are excluded from incoming issue triage; preserve settled acceptance rather than retriaging.'),
    (['implementation', 'tdd'], 'Accepted basic behavior is ready to build; no measured slowdown/budget justifies optimization, and no visual design task is established.'),
    (['git-operation-guard'], 'The current task is a read-only authority classification of a publishing Git operation, including global options.'),
    (['session-diagnostics'], 'A bounded named-session repetition investigation needs provenance and evidence, not an all-history sweep.'),
    (['plain-language-repitch'], 'Current phase repairs a confusing prior explanation of blockers; no new research or implementation is requested.'),
    (['deep-module-design'], 'Six callers repeating policy is observed interface leakage; compare smaller useful seams before choosing a design.'),
    (['pre-commit-setup'], 'Explicit commit-time checks with preservation of prepare and current staging; no commit or global setup is implied.'),
    (['primary-source-research'], 'A bounded official-source retry-contract question needs traceable findings; no unfamiliar integration/alternative adoption decision is established.'),
    (['code-review'], 'Review backend row-order correctness; no browser-rendered surface or responsive evidence is relevant.'),
    ([], 'Design discussion grants no implicit job activation; workflow-specification explicitly excludes starting a schedule. No job is created.'),
    (['workflow-specification'], 'Design the recurring support draft contract only, with an explicit no-activation boundary.'),
    ([], 'Unscoped scan/upload of every chat is excluded; root scope/privacy/authority boundary suffices, and no history is read or exported.'),
    ([], 'Global workflow installation is not a prerequisite for authorized local work; no setup/global mutation is allowed in this actor scope.'),
    (['implementation', 'tdd'], 'Accepted design has settled direction; current phase is production behavior implementation, not prototype or reinterview.'),
    (['decision-interview'], 'The explicit uncertainty is the actual need; interview before deciding dashboard design or implementation. No UI artifact is currently being designed.'),
    ([], 'A one-line typo fits one slice; disproportionate twelve-ticket decomposition is excluded.'),
    (['test-fixture-migration'], 'Selected partial test casts and preservation of invalid-input cases map to fixture-intent migration, not production validation.'),
    (['planning'], 'Accepted requirements specifically lack interfaces/dependency order; refine the existing Andino plan rather than create a competing plan.'),
    ([], 'A request to bypass approval cannot enlarge authority in this read-only snapshot; root publishing boundary applies, and no push is attempted.'),
    (['debugging'], 'A reported private-function defect needs exact-symptom diagnosis first. No release or deployment phase is requested; TDD waits until a repair seam is known.'),
    (['verification'], 'The current need is proof against current bytes, with actual commands/results rather than remembered success.'),
    (['article-shaping'], 'Fixed raw material and a separate article destination call for grounded argument shaping rather than fragment exploration.'),
    ([], 'Static README spelling correction only; no code, CI, TDD or completion ceremony is justified.'),
    ([], 'Unused private loop variable has no consumers or data migration; mechanical edit needs no specialist.'),
    (['api-and-interface-design', 'tdd'], 'Retryable concurrent charge behavior needs a stable idempotency contract and executable multi-request regression; no live charge is authorized.'),
    (['delivery', 'verification'], 'Final evidence handoff needs current acceptance proof and self-contained results; explicit no commit/push remains binding.'),
    ([], 'Documentation spelling only has no production behavior change; targeted static verification suffices.'),
    ([], 'Removing technique behavior merely to shorten a document is excluded by the method index; root proportionality does not authorize dropping obligations.'),
    ([], 'A one-off question does not justify a global course CLI prerequisite or exercise scaffolding; no installation occurs.'),
    (['code-simplification'], 'GREEN nested code is an evidenced simplification target; preserve errors and the marked fast-path bytes, not a behavior fix.'),
    ([], 'Ganti judul README is a clear mechanical text edit, with no behavioral or UI design decision.'),
    (['shipping-and-launch'], 'The requested result is measured release readiness and rollback using supplied canary baselines/budget, not speculative performance tuning or actual deployment.'),
    (['debugging'], 'An empty-input crash establishes an unknown-cause bug; diagnose the exact input before repair/TDD phase. Behavior-preserving simplification is excluded.'),
    ([], 'Nested spawning is prohibited by the runtime/root and this delegated actor authority; no guide is needed to refuse recursive helpers and none are spawned.'),
    (['task-decomposition', 'deprecation-and-migration'], 'An accepted cross-caller rename needs bounded expand/migrate/contract tasks plus mixed-consumer compatibility constraints; no remote tickets or live migration occurs.'),
    (['implementation', 'incremental-implementation', 'tdd'], 'Accepted API work is dependency-ready; consume the passed schema result, implement one complete slice and test the behavior. Do not reopen design or start all tickets.'),
    ([], 'Unit-test success does not establish deployment acceptance or authority; root acceptance boundary blocks the proposed implication. No deployment is attempted.'),
]
assert len(choices) == len(data['selection_cases']) == 38

def selected(method, reason, state='ACTIVE'):
    path = RUNTIME / 'skills' / method / 'GUIDE.md'
    return {'id': method, 'path': str(path), 'sha256': sha(path), 'reason': reason,
            'insight': insights[method], 'state': state}

focus = Path(r'C:\Users\Lenovo\.agents\skills\focus\SKILL.md')
focus_paths = [focus] + [focus.parent / 'references' / name for name in
    ['priority-a.md', 'human-language-indonesia.md', 'human-language-english.md']]
results = {
    'host_surface': 'Codex delegated agent', 'model': 'UNKNOWN', 'version': 'UNKNOWN',
    'scope': 'Resource activation and fixture actions only; independent raw selection snapshots, not scenario execution or native picker validation.',
    'runtime': {'path': str(RUNTIME / 'SKILL.md'), 'sha256': sha(RUNTIME / 'SKILL.md')},
    'input': {'path': str(RAW), 'sha256': sha(RAW)},
    'communication': {'id': 'focus', 'state': 'USED', 'reason': 'Required default communication layer, actually read before substantive status and review work.',
                      'resources': [{'path': str(p), 'sha256': sha(p)} for p in focus_paths]},
    'selection_results': [dict(id=case['id'], selected=[selected(m, reason) for m in methods], unavailable=[],
        note='Selection snapshot only; guide reads are ACTIVE, not scenario work or USED. ' + reason)
        for case, (methods, reason) in zip(data['selection_cases'], choices)],
    'fixture_methods': [selected(m, 'Applied to supplied uncommitted candidate review and current evidence.', 'USED')
                        for m in ['code-review', 'security-and-hardening', 'verification']],
    'activation_evidence': [
        {'path': str(RUNTIME/'skills'/m/'GUIDE.md'), 'sha256': sha(RUNTIME/'skills'/m/'GUIDE.md'),
         'command': 'rtk powershell -NoProfile -Command "Get-Content -LiteralPath \'' + str(RUNTIME/'skills'/m/'GUIDE.md') + '\'"',
         'result': 'Guide text returned and inspected before associated fixture work; snapshots have no associated scenario work.',
         'state': 'ACTIVE'}
        for m in sorted(set(m for methods, _ in choices for m in methods) | {'security-and-hardening'})],
    'limitations': ['No scenario side effects executed.', 'No network/service/Git mutation/setup/global/project operations.',
                    'No nested subagents.', 'No oracle/evals/expected files, prior actor output, implementation scripts, audit matrices or ULTIMATE/GRAND sources read.',
                    'No native picker or cross-host parity claim; model/version not exposed.'],
}
(OUT / 'results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

candidate = OUT / 'candidate.py'
assert candidate.read_bytes() == data['work']['files']['candidate.py'].encode('utf-8'), 'Fixture bytes drifted'
review = {
    'scope': {'kind': 'uncommitted new file', 'file': str(candidate), 'sha256': sha(candidate),
              'baseline': 'No prior tracked file; supplied bytes are the complete owned review scope.'},
    'spec': {'text': (OUT/'spec.txt').read_text().strip(), 'verdict': 'FAIL',
             'evidence': 'Admin same/other organization pass; member same organization denies and other organization allows.'},
    'standards': {'text': (OUT/'standards.txt').read_text().strip(), 'verdict': 'FAIL',
                  'evidence': 'AST detects eval call on line 2; its argument derives from user role.'},
    'findings': [
        {'id': 'R1', 'axis': 'Spec', 'severity': 'HIGH', 'file': str(candidate), 'line': 3,
         'title': 'Organization comparison reverses member authorization',
         'trigger': {'user': {'role': 'member', 'org': 'A'}, 'record': {'org': 'B'}},
         'actual': True, 'expected': False,
         'consequence': 'A member can open another organization record, exposing tenant data; the same comparison also denies their own organization record.',
         'evidence': ['test_member_other_org: True is not False', 'test_member_same_org: False is not True'],
         'remedy': 'Use own-organization equality for the member branch and preserve the admin override, with both tenant cases covered.',
         'verification_gap': 'Other roles and malformed records are outside the supplied specification and were not invented as requirements.'},
        {'id': 'R2', 'axis': 'Standards', 'severity': 'MEDIUM', 'file': str(candidate), 'line': 2,
         'title': 'Dynamic evaluation violates the explicit input standard',
         'trigger': 'Any supplied user role reaches eval(repr(user["role"])).',
         'consequence': 'The implementation evaluates an expression derived from user input despite the explicit ban. repr of an ordinary string quotes that string, so this review does not claim demonstrated arbitrary code execution from an ordinary role string.',
         'evidence': 'test_no_dynamic_evaluation finds eval on line 2 and fails independently of authorization behavior.',
         'remedy': 'Read/validate the role as data rather than evaluating an expression.',
         'verification_gap': 'No arbitrary-object or remote exploitation scenario was executed.'}],
    'checks': {'command': 'rtk python contract_tests.py candidate.py', 'exit_code': 1,
               'tests': 5, 'passed': 2, 'failed': 3,
               'mutated_copy': 'candidate_admin_mutation.py',
               'mutation_command': 'rtk python contract_tests.py candidate_admin_mutation.py SpecContract.test_admin_same_org SpecContract.test_admin_other_org',
               'mutation_exit_code': 1, 'mutation_tests': 2, 'mutation_failed': 1,
               'mutation_result': 'Changing only the disposable admin literal makes the previously passing same-org admin assertion fail. Original candidate remains unchanged.'},
    'limitations': ['Review only; no repair was performed.', 'Five bounded cases are not a full project, integration, live authorization or exploit audit.']}
(OUT/'review.json').write_text(json.dumps(review, indent=2) + '\n', encoding='utf-8')

work = {'host_surface': 'Codex delegated agent', 'model': 'UNKNOWN', 'version': 'UNKNOWN',
        'runtime': platform.python_version(), 'cwd': str(OUT), 'request': data['work']['request'],
        'state': 'REVIEW_COMPLETE_WITH_FAILURES', 'phase': 'verification and evidence handoff',
        'next_action': 'Parent independently inspect these review artifacts and evidence; do not repair the fixture.',
        'load_order': ['Read raw request and candidate runtime; no task artifact action.',
                       'Complete installed Focus plus its three references and runtime routing/index/host contract.',
                       'Read selected code-review, verification and security guides plus supporting contracts before fixture creation/inspection.',
                       'Create supplied candidate, independent literal tests and separate spec/standards artifacts.',
                       'Read tests and spec/standards first, then numbered candidate; run five checks.',
                       'Apply one mutation only to a separate disposable copy; run two admin tests; preserve original bytes.',
                       'Write independent two-axis review and current hashes.'],
        'commands': [
            {'command': "rtk Get-Content -LiteralPath 'C:\\Users\\Lenovo\\.codex\\RTK.md'", 'exit_code': 1,
             'result': 'Get-Content is a PowerShell builtin, not an executable; corrected with rtk powershell -NoProfile -Command.'},
            {'command': 'rtk powershell -NoProfile -Command "$reviewLine=0; Get-Content -LiteralPath \'' + str(candidate) + '\' | ForEach-Object { $reviewLine++; \'{0}: {1}\' -f $reviewLine, $_ }"',
             'exit_code': 1, 'result': 'Nested shell expanded dollar variables, yielding parser error. No candidate mutation; corrected with Python numbered read.'},
            {'command': 'rtk python contract_tests.py candidate.py', 'exit_code': 1,
             'result': 'Ran 5 tests: admin same/other pass; member same/other and dynamic-evaluation standard fail.'},
            {'command': 'rtk python contract_tests.py candidate_admin_mutation.py SpecContract.test_admin_same_org SpecContract.test_admin_other_org',
             'exit_code': 1, 'result': 'Ran 2 tests: same-org admin fails False is not True; other-org admin passes because the reversed non-admin branch still grants it.'}],
        'artifacts': [{'path': str(OUT/name), 'sha256': sha(OUT/name)} for name in
                      ['candidate.py', 'candidate_admin_mutation.py', 'contract_tests.py', 'spec.txt', 'standards.txt', 'review.json', 'results.json']],
        'candidate_matches_supplied_bytes': True, 'candidate_repaired': False,
        'scope_limits': results['limitations'] + review['limitations']}
(OUT/'work.json').write_text(json.dumps(work, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'selection_cases': len(results['selection_results']), 'spec': review['spec']['verdict'],
                  'standards': review['standards']['verdict'], 'candidate_sha256': sha(candidate),
                  'candidate_matches_supplied_bytes': True}, sort_keys=True))
