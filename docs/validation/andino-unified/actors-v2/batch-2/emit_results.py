import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/build/andino-unified-candidate-v2')
INPUT = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/docs/validation/andino-unified/actor-inputs-v2/batch-2.json')
FOCUS = Path('C:/Users/Lenovo/.agents/skills/focus/SKILL.md')
SEARCH = Path('C:/Users/Lenovo/.agents/skills/search-first/SKILL.md')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected(identifier, reason, insight):
    path = FOCUS if identifier == 'focus' else SEARCH if identifier == 'search-first' else ROOT / 'skills' / identifier / 'GUIDE.md'
    return {'id': identifier, 'path': str(path), 'sha256': digest(path), 'reason': reason,
            'insight': insight, 'state': 'ACTIVE', 'mechanism': 'actual permitted full file read',
            'used': False}


routes = {
    '5ad2fb667acf': ([], 'Accepted one-line rename summary is DIRECT; no consequential completion or specialist method is needed.'),
    '52ac50f632f2': ([], 'Root scope discipline excludes comments that merely restate increments; do not select documentation to add narration.'),
    '4c9b5e6b8815': ([('verification', 'Existing suite execution and evidence reporting.', 'A zero exit alone is insufficient; inspect actual cases, skips, failures and tested bytes.')], 'Current phase is checking, not implementing; no TDD or CI configuration route.'),
    '2945d7ddf125': ([('specification', 'Accepted billing discussion needs a buildable contract.', 'Reuse settled decisions and existing spec conventions; make acceptance falsifiable without reinterviewing.')], 'Discovery is settled; no decision interview.'),
    'cb7dbafba722': ([('project-configuration', 'Requested local tracker and triage convention documentation.', 'Map category and state to actual labels and preserve existing pointers; local docs grant no external label/setup permission.')], 'No automatic tracker service or global setup.'),
    '5af5921054aa': ([('idea-refine', 'Rough collaboration idea needs a bounded assumption test.', 'Presence-only MVP should test the riskiest coordination assumption and make non-goals explicit.')], 'No implementation or full CRDT design is authorized by the snapshot.'),
    '35a0077b5dc6': ([('observability-and-instrumentation', 'Origin attribution in a shared retry log is the stated need.', 'Propagate entryPoint from scheduler/replay origin with correlation; correlation alone does not prove origin.')], 'Instrument the named distinction; no speculative vendor telemetry.'),
    '7aaee84047e6': ([('api-and-interface-design', 'An existing public API changes its invoice output.', 'Inspect provider and consumers and preserve compatibility, error/order/null behavior at the public seam.')], 'Select the boundary method now; load regression support before actual executable implementation, which this snapshot does not authorize.'),
    '97adb1b99213': ([], 'A file inventory needs a sufficient native listing instrument, no methodology or graph.'),
    '1c5886e258e4': ([('incremental-implementation', 'The next already specified dependency-ready API slice is requested.', 'Reuse the accepted graph, build the smallest complete slice, and block dependent progression on failed gates.')], 'No new planning/specification or product discovery; TDD applies when real behavioral implementation begins.'),
    '5378d05d3e6e': ([('agent-document-authoring', 'Rewrite an agent-facing procedure with functional triggers and completion bounds.', 'Separate branch-only references from common steps and demand observable completion; do not compress away required behavior.')], 'This is document structure and consumer behavior, not a native skill installer.'),
    '3d17a0dd1324': ([('code-review', 'Review explicitly includes new untracked files.', 'Pin staged, unstaged and owned untracked bytes and preserve separate Spec and Standards verdicts.')], 'HEAD-only review would omit requested scope.'),
    '7b8f67c0de48': ([('architecture-survey', 'Bounded order-subsystem friction survey.', 'Trace actual concepts/callers and report evidenced candidates or none; survey grants no redesign authority.')], 'Interface deepening follows a selected candidate; no premature implementation.'),
    'e08782084ea0': ([], 'Healthy existing-cache explanation needs bounded source reading; a cache keyword does not establish a bug or performance problem.'),
    '36feb4262cb5': ([], 'A personal preference belongs to the user and cannot be researched or invented. Directly elicit the preference if needed; no UI design/evaluation action is requested.'),
    'adfe38adca99': ([('debugging', 'A reported cross-tenant wrong-result symptom has unknown cause.', 'Reproduce two-search order and trace identity before confirming cache or any proposed fix.')], 'Security impact matters to diagnosis, but no confirmed cause or remediation is selected in advance.'),
    '4ca6b6700667': ([], 'Private local variable rename is a mechanical SIMPLE edit with targeted checking, no migration/API/TDD ceremony.'),
    'ad962d2c7fea': ([('handoff', 'Explicit portable continuation for another colleague and checkout.', 'Reference durable reachable artifacts, current state, permissions and a concrete next action; recipient checks drift.')], 'No new host, background process or message is authorized.'),
    '3a62a9e3ac0a': ([], 'One README typo is a static SIMPLE edit; no TDD, plan or specialist ceremony.'),
    'd6e6853eae28': ([('article-shaping', 'Fixed raw writing material is ready for a final article.', 'Preserve raw pile, ground concepts before dependent claims and do not invent anecdotes; settled user choices remain settled.')], 'Use a separate output and preserve accepted direction; no exploratory writing-fragments route.'),
    'c0d38829fba5': ([('learning-workspace', 'Explicit multi-lesson learning folder.', 'Teach one bounded tangible lesson, distinguish coverage from demonstrated learning and keep lesson paths within the selected workspace.')], 'No automatic recurring schedule or community account.'),
    '1faa1ed6c8b3': ([('context-engineering', 'A bounded context packet must retain scope/current failure and drop old logs.', 'Protect original scope, binding constraints and active failure; compress resolved material to evidence breadcrumbs in the existing checkpoint.')], 'This is context selection, not a second execution plan.'),
    '587b325770f9': ([('implementation', 'The invoice retry ticket is already approved and ready.', 'Resolve exact ticket/accepted graph, inspect drift and execute one ready public behavior without reopening intent.')], 'TDD and review activate at their real work phases; no new product interview.'),
    '360fbe25a5c2': ([('ci-cd-and-automation', 'Configure lint/unit/build/release dependency gating.', 'Model actual stage dependencies so every failed ancestor blocks advancement; keep hosted enforcement and local model proof distinct.')], 'The request is pipeline preparation, not deployment authorization.'),
    '246432375a1a': ([], 'Two plus three is five; sufficient DIRECT answer needs no repository inspection, guide or verification ritual.'),
    '800f809b56fa': ([], 'Universal TypeScript restructuring is excluded by the layout method; root scope/convention discipline resolves the boundary without loading it.'),
    '44c630f34d7e': ([('deprecation-and-migration', 'Schema rename must coexist with old clients.', 'Expand, dual-write, bounded backfill and switch reads precede a separate guarded contract after old consumers are gone.')], 'Live data/destructive changes remain separately bounded; no in-place rename.'),
    '8d19111bb034': ([('stakeholder-questionnaire', 'Named platform owner holds launch capacity and retention facts.', 'Map each decision gap to one recipient-appropriate question with answer space; draft locally without inventing urgency or sending it.')], 'Question drafting is distinct from messaging authority.'),
    '4d48c2b89af5': ([('plan-execution', 'Resume accepted plan after checking drift.', 'Compare actual artifact identities and reopen only affected evidence; resume concrete NEXT ACTION instead of reinitializing.')], 'Root handoff/execution-plan references were also read; no mandatory history or memory service.'),
    'ad15210b7f8f': ([], 'Replanning every plan without a cause contradicts reuse of accepted durable state; no planning method is needed merely to refuse the pointless restart.'),
    'b9f721de7bc3': ([('security-and-hardening', 'Owned cleanup path and SQL injection trust boundaries are explicit.', 'Resolve containment and authenticated ownership before teardown; parameterize the SQL value, and do not treat markers alone as security proof.')], 'Selection grants no deletion or live database operation.'),
    '98fa914fb8f5': ([], 'Greeting only: no change, result or completion claim, so no verification or plan.'),
    '0304b7c94b26': ([('search-first', 'Explicit unfamiliar framework technical research.', 'Research need remains selected even offline; absent authorized network evidence leaves external findings unknown.'), ('primary-source-research', 'Technical findings need source-owned support.', 'Separate facts, interpretation and gaps, preserving version/date and exact supporting sources.')], 'ACTIVE only. No network/services or research action authorized in these snapshots; neither research method is USED.'),
    '4552083726eb': ([], 'Test-fixture fromAny casting is explicitly excluded from production/runtime validation. Resolve boundary without loading the test migration method.'),
    '03a09343cf18': ([('documentation-and-adrs', 'Record a queue decision preserving existing ADR-004 .rst conventions.', 'Inspect numbering/location/format and preserve throughput caveats and history; do not create a competing ADR system.')], 'No generic comment expansion or publication.'),
    '80778696001c': ([('human-procedure', 'Credential dashboard journey must be performed by the human.', 'Use verified/current journey steps and secret destinations; never invent UI paths or request secrets in chat.')], 'Manual steps can be drafted; no dashboard access or credential handling is authorized.'),
    '082c8d19b4bb': ([('plan-execution', 'Continue a task in an already complete graph.', 'Reuse the graph, reconcile evidence and choose the verified ready frontier; complete graph structure is not proof all task results are accepted.')], 'No replacement planning/decomposition phase.'),
    '289d07b21a28': ([('delegation', 'Planning-only parent delegation safety assessment for two independent audit tasks.', 'Authorized parent can consider bounded disjoint ready tasks with real child tools, at most three direct workers and no nested spawning; inspect reports before acceptance.')], 'Guide ACTIVE only. Actor is a delegated child and cannot spawn; no dispatch was attempted or claimed.')
}

raw = json.loads(INPUT.read_text(encoding='utf-8-sig'))
assert set(routes) == {case['id'] for case in raw['selection_cases']}
rows = []
for case in raw['selection_cases']:
    methods, note = routes[case['id']]
    entries = [selected('focus', 'Required Andino default communication layer.', 'Preserve evidence and uncertainty while keeping output direct; Focus owns no lifecycle.')]
    entries += [selected(*method) for method in methods]
    rows.append({'id': case['id'], 'request': case['request'], 'selected': entries,
                 'unavailable': [], 'note': note, 'snapshot_only': True,
                 'actual_task_actions_authorized': False})

results = {
    'host': {'surface': 'Codex delegated agent', 'model': 'UNKNOWN', 'version': 'UNKNOWN',
             'scope': 'Resource activation and isolated fixture actions only; native picker and universal-host behavior not tested.'},
    'candidate': {'root': str(ROOT), 'skill_sha256': digest(ROOT / 'SKILL.md'),
                  'routing_sha256': digest(ROOT / 'references/routing.md'),
                  'index_sha256': digest(ROOT / 'references/internal-method-index.md')},
    'input': {'path': str(INPUT), 'sha256': digest(INPUT)},
    'state_semantics': {'DISCOVERED': 'Metadata known', 'AVAILABLE': 'Actual resource exists',
                        'INVOKABLE': 'Current permissions allow file read', 'ACTIVE': 'Actual full permitted guide read',
                        'USED': 'Loaded guide plus relevant fixture action/result',
                        'UNAVAILABLE': 'Needed resource/action missing or denied', 'NOT_NEEDED': 'No current evidenced need'},
    'selection_results': rows,
    'selection_limits': 'Reads establish ACTIVE only. Snapshot actions were not executed. Other product facts and current phases treated as settled; no oracle/expected/evals, prior actors, implementation scripts or audit/coverage artifacts read.',
    'work': str(HERE / 'work.json')
}
(HERE / 'results.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
before = (HERE / 'before.py').read_bytes()
assert before == raw['work']['files']['subject.py'].encode('utf-8')
assert (HERE / 'subject.py').read_bytes() == before.replace(b'index * (size - 1)', b'index * size')
print(json.dumps({'selection_cases': len(rows), 'before_matches_input': True,
                  'minimal_fix_only': True, 'before_sha256': digest(HERE / 'before.py'),
                  'after_sha256': digest(HERE / 'subject.py'),
                  'results_sha256': digest(HERE / 'results.json')}, sort_keys=True))

used_methods = [
    ('debugging', 'Exact page0/page1 reproduction, controlled start-stride hypothesis and confirmed minimal root fix.'),
    ('tdd', 'Literal public-seam regression RED on faulty source, minimal GREEN, additional boundary cases and isolated faulty-copy failures.'),
    ('verification', 'Three actual passing tests, before-copy mutation sensitivity, exact input/changed-byte checks and hashes.'),
    ('focus', 'Concise evidence-based progress reporting without attributing unsupported causes or tool success.')
]
used = []
for identifier, action in used_methods:
    item = selected(identifier, 'Required at its fixture phase.', action)
    item['state'] = 'USED'
    item['used'] = True
    item['action_result'] = action
    used.append(item)
commands = json.loads((HERE / 'command-evidence.json').read_text())
work = {
    'host': results['host'], 'request': raw['work']['request'],
    'runtime': {'python': '3.12.10', 'surface': 'Windows PowerShell shell commands through rtk'},
    'permission_scope': str(HERE),
    'plan': str(HERE / 'plan.md'),
    'before': {'path': str(HERE / 'before.py'), 'bytes_utf8': before.decode(),
               'sha256': digest(HERE / 'before.py'), 'equals_supplied_input_bytes': True},
    'reported': {'page0': ['A', 'B'], 'page1': ['B', 'C']},
    'observed_reproduction': {'command': 'rtk python reproduce.py', 'stage': 'before fix',
                              'page0': ['A', 'B'], 'page1': ['B', 'C'], 'exit_code': 0},
    'hypothesis': {'statement': 'The start advances by size-1, creating overlapping slices.',
                   'prediction': 'Change only stride to size; page index 1 at size 2 begins at index 2 and returns C,D.',
                   'probe_command': 'rtk python hypothesis.py',
                   'observed': {'old_start': 1, 'predicted_start': 2, 'page1': ['C', 'D']},
                   'status': 'CONFIRMED by single-variable probe and regression'},
    'independent_literal_expected_values': [
        {'items': ['A', 'B', 'C', 'D'], 'index': 0, 'size': 2, 'expected': ['A', 'B']},
        {'items': ['A', 'B', 'C', 'D'], 'index': 1, 'size': 2, 'expected': ['C', 'D']},
        {'items': ['A', 'B', 'C'], 'index': 0, 'size': 1, 'expected': ['A']},
        {'items': ['A', 'B', 'C'], 'index': 1, 'size': 1, 'expected': ['B']},
        {'items': ['A', 'B', 'C'], 'index': 2, 'size': 1, 'expected': ['C']},
        {'items': ['A', 'B', 'C', 'D', 'E'], 'index': 1, 'size': 3, 'expected': ['D', 'E']},
        {'items': ['A', 'B', 'C', 'D', 'E'], 'index': 2, 'size': 3, 'expected': []},
        {'items': [], 'index': 0, 'size': 2, 'expected': []}],
    'expectation_basis': 'Literal worked values from the supplied consecutive non-overlapping zero-indexed page contract; not calculated using the subject implementation.',
    'red': {'command': 'rtk python test_page.py', 'exit_code': 1,
            'signal': "AssertionError: Lists differ: ['B', 'C'] != ['C', 'D']", 'tests': 1, 'failures': 1},
    'fix': {'path': str(HERE / 'subject.py'), 'change': 'start = index * size',
            'sha256': digest(HERE / 'subject.py'), 'only_expected_source_replacement': True},
    'green': {'command': 'rtk python -m unittest discover -s . -p test_page.py -v',
              'exit_code': 0, 'tests': 3, 'failures': 0, 'skipped': 0,
              'test_sha256': digest(HERE / 'test_page.py')},
    'faulty_copy_sensitivity': {'command': 'rtk python run_faulty.py', 'source': str(HERE / 'before.py'),
                              'exit_code': 1, 'tests': 3, 'failures': 3,
                              'reported_scenario_failed': True, 'fixed_subject_preserved': True},
    'tool_failures': [
        {'command_index': 0, 'observation': 'Copy-Item succeeded; Get-FileHash was not available.',
         'correction': 'Python hashlib establishes before/after identity and exact supplied bytes.'},
        {'command_index': 7, 'observation': 'Nested PowerShell expanded PAGE_SUBJECT before assignment; error followed by fixed-source tests. Zero exit is not faulty-copy evidence.',
         'correction': 'run_faulty.py sets environment in Python and actually selects before.py; observed intended assertion failures.'}],
    'commands': commands,
    'method_use': used,
    'extra_activation': {'id': 'decision-interview', 'path': str(ROOT / 'skills/decision-interview/GUIDE.md'),
                         'sha256': digest(ROOT / 'skills/decision-interview/GUIDE.md'),
                         'state': 'ACTIVE', 'used': False,
                         'note': 'Read while considering preference clarification; direct user-owned preference elicitation suffices, so not selected or claimed used.'},
    'focus_references': [{'path': str(FOCUS.parent / 'references' / filename),
                           'sha256': digest(FOCUS.parent / 'references' / filename),
                           'state': 'ACTIVE', 'full_read': True}
                          for filename in ['priority-a.md', 'human-language-indonesia.md', 'human-language-english.md']],
    'hashes': {filename: digest(HERE / filename) for filename in
               ['subject.py', 'before.py', 'test_page.py', 'reproduce.py', 'hypothesis.py', 'run_faulty.py', 'command-evidence.json', 'results.json']},
    'limitations': ['Only the supplied isolated Python contract was tested.',
                    'No application, repository-wide suite, native picker, universal host, network, child dispatch or live-service claim.',
                    'Negative indices and nonpositive sizes have no supplied acceptance contract; no new validation behavior was invented.',
                    'Selection snapshots establish ACTIVE guide reads only; no snapshot product actions executed.'],
    'state': 'DONE', 'next_action': 'None - assigned fixture and selection records complete'
}
(HERE / 'work.json').write_text(json.dumps(work, indent=2) + '\n', encoding='utf-8')
