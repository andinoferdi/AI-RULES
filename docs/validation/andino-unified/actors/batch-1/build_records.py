import ast
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

OUT = pathlib.Path(__file__).resolve().parent
RUNTIME = pathlib.Path(r'C:\Users\Lenovo\Downloads\AI-RULES-main\build\andino-unified-candidate')
INPUT = pathlib.Path(r'C:\Users\Lenovo\Downloads\AI-RULES-main\docs\validation\andino-unified\actor-inputs\batch-1.json')
RED_OUTPUT = '''[rtk] /!\\ No hook installed — run `rtk init -g` for automatic token savings
test_known_invoice (test_subject.InvoiceContract.test_known_invoice) ... FAIL

======================================================================
FAIL: test_known_invoice (test_subject.InvoiceContract.test_known_invoice)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\\Users\\Lenovo\\Downloads\\AI-RULES-main\\docs\\validation\\andino-unified\\actors\\batch-1\\test_subject.py", line 8, in test_known_invoice
    self.assertEqual(sum_invoice([10, 5]), 15)
AssertionError: 0 != 15

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
'''

# Actor decisions from the raw snapshots, not a runtime keyword router.
CHOICES = {
    '74a98a8bed81': [('pr-description', 'A local PR body is the requested artifact.', 'Tie the concrete trigger and changed behavior to the recorded before/after commands; retain the house template and classify one-way effects. No publication is implied.')],
    '56d20b512041': [('incremental-implementation', 'Continue the next ready step in the existing context.', 'Reuse completed acceptance and choose the smallest dependency-ready increment; a same-context continuation does not need a portable handoff or a new plan.')],
    'f4762b672d6f': [('typescript-boundary-enforcement', 'An accepted entrypoint policy needs executable enforcement.', 'Preserve the selected layout, merge actual resolver-aware rules, and prove valid graph, deep-import failure and restored-valid graph; include tests privacy and cycles.')],
    '1086608388f0': [],
    'a933736aaa08': [('git-workflow-and-versioning', 'Owned change grouping and breaking-version rationale are explicitly requested.', 'Keep existing edits outside the owned groups and classify observable consumer incompatibility as MAJOR; grouping is not staging or commit authority.')],
    '12d1a9633c53': [('design-prototype', 'A local state demo must resolve whether empty checkout is legal.', 'Expose that one question in a pure reducer/state machine with resettable happy, awkward and illegal cases; use scratch state and obtain an actual verdict rather than promoting demo code.')],
    '477bcf0d6c86': [],
    'f942e5e3b6fb': [('writing-fragments', 'The user explicitly wants raw fragments, without an outline.', 'Append actual observations to a reread fragment file with one working title and horizontal separators; retain the author voice and do not fabricate anecdotes or impose structure.')],
    '75f803809d42': [('domain-modeling', 'Code and glossary disagree on customer/account concepts.', 'Compare concrete code scenarios with the relevant glossary, distinguish login identity from customer organization where evidenced, and resolve canonical definitions without silently choosing a synonym.')],
    'fe24008c1d74': [('frontend-ui-engineering', 'Implement an approved user-visible error/retry state and accessible control.', 'Preserve the approved design and input after failure; use a semantic button with a useful accessible name, keyboard behavior and error/status announcement.'), ('tdd', 'An executable state behavior is being implemented now.', 'Write one public retry-state regression with the expected failure before implementation; assert visible behavior through the named control rather than private event-handler calls.')],
    'aeb97ddd0f13': [('incremental-implementation', 'Create then list are accepted dependency-ordered slices.', 'Verify create as a complete working path before unlocking list; keep both increments reviewable and stop dependent progress on a failed gate.'), ('tdd', 'The two slices change executable public behavior.', 'For each seam independently derive expected create/list state, observe the intended RED, then implement minimal GREEN before moving to the next slice.')],
    '5a24e85e63fc': [],
    '7f3b7e3d5458': [('debugging', 'The checkbox symptom is an unknown-cause reported bug.', 'Keep PATCH 503 as an observation, reproduce the exact checked-state outcome and test whether response rejection/rollback explains it; do not treat the status as a confirmed root cause.'), ('browser-testing-with-devtools', 'Captured UI/network events are the distinct evidence surface.', 'Correlate request method/status with visible state and event ordering; distinguish server failure from client rollback behavior and mark live replay/screenshots unverified when only captures exist.')],
    '8a5bd19c1513': [('implementation', 'A settled server-only index change is authorized in the snapshot.', 'Use the accepted database task and actual project checks for the smallest owned change. Do not select a frontend method or invent a performance result without same-condition measurements.')],
    'dd270fedf396': [('exercise-scaffolding', 'Numbered course section and exact variants are requested.', 'Reuse 05.02 conventions; explainer/problem provide an accessible primary variant, solution alone is insufficient; check nonempty readmes, valid links and entry files as applicable.')],
    '21abd16e703f': [('session-diagnostics', 'The target is repeated failures of this session.', 'Identify the bounded session/range and evidence lineage, compare repeated calls against intervening changes, and ground guardrail proposals in observed adherence or verification failures rather than current-install assumptions.')],
    '258871d7f9dc': [('issue-triage', 'Evaluate an incoming report and comments into a brief.', 'Read the full report/comments and previous notes, distinguish category from triage state, boundedly verify its exact claim, and draft acceptance/out-of-scope locally without tracker writes.')],
    '86b1ef81b196': [],
    '00a68869e832': [],
    'c29303c4759e': [],
    '5e7427f7697e': [],
    'dd6434485545': [],
    'd03a556fc435': [('method-authoring', 'Guidance must address an observed procedural failure.', 'Start with the actual failed action and a no-guidance control; match an omitted field to an artifact slot or an authority failure to a precise boundary, then test only the evidenced failure.')],
    '46adc4dd5778': [('decision-interview', 'Product necessity is expressly open and intent discovery is requested.', 'Begin with the last concrete problem and who benefits, distinguish goals/non-goals from assumptions, and ask one consequential question before any implementation or specification.')],
    '6e25ed271218': [],
    'cef4b736f904': [],
    '4ec11b7f258c': [('decision-map', 'Several storage decisions and blockers span sessions.', 'Represent sharp open storage questions with stable IDs and real blockers; keep vague in-scope uncertainty as fog and distinguish question resolution from implementation tasks under the existing checkpoint.')],
    'f64927d7aa31': [],
    '428ff006b859': [],
    'c97a09f607ac': [],
    '448ff3602487': [('doubt-driven-development', 'Explicit bounded adversarial scrutiny of a retry invariant.', 'Extract only artifact and accepted contract for review, omit the author claim/reasoning, classify contract misread before actionable finding, and stop by diminishing findings or three cycles. This actor cannot create an independent reviewer.')],
    '0ada99c86213': [],
    'da9611f8a5c8': [('plan-execution', 'Execute an already approved plan without reopening ideation.', 'Check current output identities against completed evidence, select the ready presence-only slice and preserve the accepted interfaces and rulings; do not repeat completed tasks or interview product intent.'), ('tdd', 'The implementation plan changes executable behavior.', 'Use the accepted presence-only contract as the public seam, not a broadened product behavior; require intended assertion RED and minimal GREEN for its next behavior.')],
    '62991a1d0826': [('source-driven-development', 'A bounded version-pinned argument fact needs source confirmation.', 'Compare the manifest and resolved version with the supplied official excerpt and exact intent_key signature. Local version-matched evidence can suffice; neither current API availability nor retrieval is invented.')],
    '0a74978bf670': [('performance-optimization', 'Repeated same-condition measurements and noise rejection are explicit.', 'Compare medians and measured variation under the same command/data/environment; reject a delta inside noise and require unchanged correctness before keeping an optimization.')],
    '62407b7d2daa': [],
    'a0f04777f329': [('constraint-driven-development', 'The diff explicitly weakens assertions, suppressions and coverage.', 'Evaluate additions and removals against the existing floor, pair matching threshold identities and directions, flag removed assertions/new suppressions/lowered minimum, and treat missing baseline as ERROR rather than CLEAN.')],
    '55ff90cd8355': [],
}

NOTES = {
    '1086608388f0': 'No method loaded to perform a prohibited overwrite of raw user material; no transcript exists in allowed probe input and user files remain untouched.',
    '477bcf0d6c86': 'Direct conceptual reply: review inspects a change against intent/standards; testing executes cases to observe behavior. No current diff or test run is requested.',
    '5a24e85e63fc': 'No observed failure exists to justify new generic guidance; method-authoring exclusion applies.',
    '86b1ef81b196': 'A private mechanical rename has no new public behavior or consumer migration; ordinary targeted edit/verification suffices.',
    '00a68869e832': 'Root/session prohibition resolves unauthorized staging/commit. No method loaded merely to refuse, and no Git mutation performed.',
    'c29303c4759e': 'Pure private loop-counter rename needs no security, API, source-research or TDD activation.',
    '5e7427f7697e': 'An accepted current spec excludes restarting specification discovery. Preserve it; clarify a concrete changed requirement if one exists rather than creating a second spec.',
    'dd6434485545': 'Deletion of all untracked files is prohibited for this actor and risks existing work. No destructive cleanup performed and no method loaded solely to refuse.',
    '6e25ed271218': 'Self-contained supplied expression explanation; context engineering or session diagnostics adds no value.',
    'cef4b736f904': 'Explicitly unrequested sending is outside authority. Do not activate questionnaire or messaging methods to bypass the boundary.',
    'f64927d7aa31': 'Read-only worktree inspection alone does not need Git isolation or branch creation. No repository is inspected because this is a selection snapshot, and real Git mutation is forbidden.',
    '428ff006b859': 'Global automatic hook installation is prohibited and explicitly excluded by the Git guard method. No hook or global config changed.',
    'c97a09f607ac': 'Formatting an unchanged constraints document does not change its quality contract; no constraint interview or floor-method activation is needed.',
    '0ada99c86213': 'Do not disclose a secret or access private credentials. No secret/config resource was read; no human-procedure method loaded just to refuse an unsafe disclosure.',
    '62407b7d2daa': 'Direct answer only: retry means attempting an operation again after a failure. No technical workflow is activated for the word itself.',
    '55ff90cd8355': 'Explanation of a supplied constant needs no implementation/incremental method or file changes.',
}


def identity(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def method(method_id, reason, insight):
    path = RUNTIME / 'skills' / method_id / 'GUIDE.md'
    return {'id': method_id, 'path': str(path), 'sha256': identity(path),
            'availability': 'AVAILABLE and INVOKABLE', 'state': 'ACTIVE',
            'reason': reason, 'insight': insight,
            'activation': 'Full actual GUIDE.md read through rtk-prefixed shell before this record; unchanged content reused.'}


def run_mutation(name, source):
    directory = OUT / 'mutations' / name
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'subject.py').write_text(source, encoding='utf-8')
    shutil.copyfile(OUT / 'test_subject.py', directory / 'test_subject.py')
    args = ['rtk', 'proxy', sys.executable, '-B', '-m', 'unittest', '-v', 'test_subject']
    result = subprocess.run(args, cwd=directory, capture_output=True, text=True)
    log = directory / 'test-output.txt'
    log.write_text(result.stdout + result.stderr, encoding='utf-8')
    return {'command_argv': args, 'cwd': str(directory), 'exit_code': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr, 'log': str(log),
            'source_sha256': identity(directory / 'subject.py'),
            'test_sha256': identity(directory / 'test_subject.py')}


def main():
    raw = json.loads(INPUT.read_text(encoding='utf-8-sig'))
    assert len(raw['selection_cases']) == 38
    assert set(CHOICES) == {case['id'] for case in raw['selection_cases']}
    selections = []
    for case in raw['selection_cases']:
        case_id = case['id']
        unavailable = []
        if case_id == 'fe24008c1d74':
            unavailable.append({'id': 'impeccable', 'reason': 'Native sibling loading is outside this actor scope (only installed Focus/Search First permitted); accepted design is retained. No UI acceptance claimed.'})
        if case_id == '448ff3602487':
            unavailable.append({'id': 'independent-reviewer', 'reason': 'Nested agents and cross-model execution are prohibited for this delegated actor. Any self-check would be DEGRADED, not independent.'})
        note = NOTES.get(case_id, 'Snapshot selection only: selected guides are ACTIVE, not USED task execution; no probe-specific artifact/service was supplied or operated. Other task facts stay settled.')
        selections.append({'id': case_id, 'request': case['request'],
                           'selected': [method(*entry) for entry in CHOICES[case_id]],
                           'unavailable': unavailable, 'note': note,
                           'release': 'No prior snapshot method is retained as a default; unchanged guide content may be reused only when independently selected.'})

    green = json.loads((OUT / 'green-observations.json').read_text(encoding='utf-8'))
    mutations = {
        'constant_zero': run_mutation('constant_zero', 'def sum_invoice(values):\n    return 0\n'),
        'wrong_empty': run_mutation('wrong_empty', 'def sum_invoice(values):\n    return sum(values) if values else 1\n'),
    }
    assert mutations['constant_zero']['exit_code'] == 1
    assert '0 != 15' in mutations['constant_zero']['stderr']
    assert mutations['wrong_empty']['exit_code'] == 1
    assert '1 != 0' in mutations['wrong_empty']['stderr']
    source = (OUT / 'subject.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    assert isinstance(tree.body[0], ast.FunctionDef)
    assert tree.body[0].name == 'sum_invoice'
    assert [arg.arg for arg in tree.body[0].args.args] == ['values']
    hashes = {name: identity(OUT / name) for name in ['subject.py', 'test_subject.py']}
    work = {
        'request': raw['work']['request'], 'directory': str(OUT),
        'public_seam': 'sum_invoice(values)',
        'baseline_source': raw['work']['files']['subject.py'],
        'final_source': source, 'runtime': sys.version,
        'methods': [method('tdd', 'A real executable regression is explicitly required.', 'The test derives literal 15 from 10+5 and catches constant-zero production mutation; implement the smallest public behavior, then check empty input.'),
                    method('code-review', 'Review the completed owned fixture.', 'Read tests first, review all owned fixture bytes against separate Spec and Standards axes, and prove mutation sensitivity in disposable copies.'),
                    method('verification', 'Acceptance is a consequential tested claim.', 'Bind the exact test runs and faulty-copy outputs to current source/test hashes; distinguish local Python proof from external host parity.')],
        'red': {'command': 'rtk proxy python -B -m unittest -v test_subject', 'cwd': str(OUT), 'exit_code': 1,
                'full_output': RED_OUTPUT,
                'observation': 'test_known_invoice (test_subject.InvoiceContract.test_known_invoice) ... FAIL\nAssertionError: 0 != 15\nRan 1 test in 0.000s\nFAILED (failures=1)',
                'source': raw['work']['files']['subject.py'],
                'test': 'self.assertEqual(sum_invoice([10, 5]), 15)',
                'source_of_observation': 'Actual exec_command output chunk 5e9a6e, copied without a synthetic PASS assertion.'},
        'green': green, 'mutation_checks': mutations,
        'review': {'kind': 'single-actor self-review; no independent reviewer invoked',
                   'scope': ['subject.py:1-2', 'test_subject.py:1-15'],
                   'spec': {'verdict': 'Observed acceptance supported', 'evidence': '[10,5] -> 15 and [] -> 0 passed through the public function; both faulty-copy regressions failed for their intended assertion.'},
                   'standards': {'verdict': 'No scoped violation observed', 'evidence': 'Public name and values parameter preserved by AST check; stdlib-only sum implementation; no new input policy, dependencies or external effects; all files remain inside actor directory.'},
                   'findings': [],
                   'refactor': 'No separate refactor performed: sum(values) is already the minimal production change.'},
        'tested_identity': hashes,
        'acceptance_scope': 'The supplied integer-list sum and empty-input contract in isolated local Python unittest only.',
        'excluded': ['No network or live service', 'No Git mutation or upstream checkout', 'No package installation', 'No nested agent or independent reviewer', 'No UI or cross-host runtime acceptance'],
        'artifacts': [str(OUT / 'subject.py'), str(OUT / 'test_subject.py'), str(OUT / 'green-observations.json'), str(OUT / 'mutations')],
    }
    for active_method in work['methods']:
        active_method['state'] = 'USED'
    (OUT / 'work.json').write_text(json.dumps(work, indent=2) + '\n', encoding='utf-8')
    focus = pathlib.Path(r'C:\Users\Lenovo\.agents\skills\focus\SKILL.md')
    results = {
        'host': {'surface': 'Codex delegated agent', 'model': 'UNKNOWN', 'version': 'UNKNOWN', 'scope': 'resource activation and fixture actions'},
        'runtime': {'path': str(RUNTIME), 'skill_sha256': identity(RUNTIME / 'SKILL.md'), 'routing_sha256': identity(RUNTIME / 'references/routing.md')},
        'communication': {'id': 'focus', 'path': str(focus), 'sha256': identity(focus), 'state': 'ACTIVE',
                          'references': ['references/priority-a.md', 'references/human-language-indonesia.md', 'references/human-language-english.md'],
                          'mechanism': 'Actual installed session skill entry loaded by permitted file reading.'},
        'selection_results': selections,
        'work': work,
        'limitations': [
            'Probe evidence is ACTIVE resource selection, not automatic native picker discovery or task execution for each snapshot.',
            'No live services, installed external tools, browser rendering, Git operations or independent reviewers were invoked.',
            'First rtk proxy Get-Content attempt failed because a PowerShell cmdlet is not an executable; subsequent reads used a real interpreter. An early nested PowerShell variable was expanded by its caller and was corrected to Python. Initial Python printing also encountered cp1252, corrected with -X utf8. None was treated as successful activation for omitted content.',
            'The first Andino progress announcement preceded the complete Focus reference read; the required references were subsequently loaded.',
            'No Search First activation was needed: probes are selection-only; the bounded pinned-source probe supplies its source, and actual work is stable local Python logic with no open integration/alternatives decision.',
        ],
    }
    (OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'selection_cases': len(selections), 'selected_activations': sum(len(s['selected']) for s in selections), 'fixture_mutations': {k: v['exit_code'] for k, v in mutations.items()}, 'source_sha256': hashes['subject.py'], 'results': str(OUT / 'results.json'), 'work': str(OUT / 'work.json')}, indent=2))


if __name__ == '__main__':
    main()
