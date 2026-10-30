"""Execute candidate guide procedures in isolation; never a runtime model router."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

from check_andino_addy_methods import run_example

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def procedure(runtime, identity, marker):
    path = runtime / 'skills' / identity / 'GUIDE.md'
    blocks = re.findall(r'```python ' + re.escape(marker) + r'\n(.*?)\n```',
                        path.read_text(encoding='utf-8'), re.S)
    if len(blocks) != 1:
        raise ValueError(f'{identity}: exactly one {marker} required')
    tree = ast.parse(blocks[0])
    tree.body = [node for node in tree.body if not (
        isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name) and node.value.func.id == 'print')]
    return ast.unparse(tree)


def exercise(code, expression, expected, mutation):
    suffix = '\nprint(json.dumps(' + expression + ', sort_keys=True))\n'
    observed = run_example(code + suffix, False)
    if not observed['ok'] or observed['observed'] != expected:
        raise AssertionError(f'procedure outcome mismatch: {observed}; expected {expected}')
    old, new = mutation
    if old not in code:
        raise AssertionError(f'mutation location missing: {old}')
    mutant = run_example(code.replace(old, new) + suffix, False)
    # Reject setup errors as evidence of mutation sensitivity.
    if not mutant['ok']:
        raise AssertionError(f'mutant must execute before its outcome is assessed: {mutant}')
    if mutant['observed'] == expected:
        raise AssertionError('faulty procedure survived independent expected outcomes')
    return {'observed': observed['observed'], 'mutant_observed': mutant['observed'],
            'mutation_killed': True}


def check_new_method(runtime, method):
    identity = method['id']
    code = procedure(runtime, identity, 'andino-example')
    if identity == 'brainstorming':
        expression = "[route({'accepted_spec': True, 'fixed_options': False, 'material_criteria_missing': False}), route({'accepted_spec': False, 'fixed_options': True, 'material_criteria_missing': False}), route({'accepted_spec': False, 'fixed_options': False, 'material_criteria_missing': False}), route({'accepted_spec': False, 'fixed_options': True, 'material_criteria_missing': True}), route({'accepted_spec': False, 'fixed_options': False, 'material_criteria_missing': False, 'delegated': True}), route({'accepted_spec': True, 'fixed_options': False, 'material_criteria_missing': False, 'reopen': True})]"
        expected = ['normal-workflow', 'normal-workflow', 'brainstorming', 'decision-interview', 'normal-workflow', 'brainstorming']
        mutation = ("request['accepted_spec']", 'False')
    elif identity == 'workflow-advisor':
        expression = "[advise('independent-perspectives', {'id': 'council', 'fit': 'independent-perspectives'}), advise('repair', {'id': 'council', 'fit': 'independent-perspectives'})]"
        expected = [
            {'recommendation': 'council', 'availability': 'UNKNOWN', 'invoked': False,
             'next': 'check current host availability and invocation permission'},
            {'recommendation': 'inspect-relevant-options', 'availability': 'UNKNOWN', 'invoked': False},
        ]
        mutation = ("'invoked': False", "'invoked': True")
    else:
        raise ValueError('unowned evolution method: ' + identity)
    result = exercise(code, expression, expected, mutation)
    return {'id': identity, 'status': 'PASS', **result,
            'guide_sha256': digest(runtime / 'skills' / identity / 'GUIDE.md'),
            'metadata_sha256': hashlib.sha256(json.dumps(
                method, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}


def check_policy(runtime, identity, expression, expected, mutation):
    result = exercise(procedure(runtime, identity, 'evolution-example'),
                      expression, expected, mutation)
    return {'id': identity, **result,
            'guide_sha256': digest(runtime / 'skills' / identity / 'GUIDE.md')}


def policy_checks(runtime):
    checks = [
        check_policy(runtime, 'learning-workspace',
            "[choose_mode({'last_explanation_unclear': False, 'multi_session_goal': False, 'explicit_learning_request': False}), choose_mode({'last_explanation_unclear': False, 'multi_session_goal': False, 'explicit_learning_request': True}), choose_mode({'last_explanation_unclear': False, 'multi_session_goal': True, 'explicit_learning_request': True}), choose_mode({'last_explanation_unclear': True, 'multi_session_goal': True, 'explicit_learning_request': True})]",
            [{'mode': 'direct-answer', 'persistent_goal': False},
             {'mode': 'quick', 'persistent_goal': False},
             {'mode': 'structured', 'persistent_goal': True},
             {'mode': 'repair', 'persistent_goal': False}],
            ("request['multi_session_goal']", 'False')),
        check_policy(runtime, 'session-diagnostics',
            "[metric({}, 'cost'), metric({'cost': None}, 'cost'), metric({'count': 0}, 'count'), cause_status(True, False), cause_status(True, True), cause_status(False, True)]",
            ['UNKNOWN', 'UNKNOWN', 0, 'UNKNOWN', 'CONFIRMED', 'UNKNOWN'],
            ('value is None', 'not value')),
    ]
    task = {'small': False, 'coupled': False, 'delegation_value': True,
            'implementation': False, 'review_value': False, 'independent': True}
    expression = (
        f"[strategy({task!r}, host), strategy({task!r}, dict(host, worker_available=False)), "
        f"strategy(dict({task!r}, implementation=True, review_value=True), host), "
        f"strategy(dict({task!r}, coupled=True), host), "
        "model_choice(['implementation'], host), "
        "model_choice(['implementation'], dict(host, model_selection_exposed=False)), "
        "model_choice(['architecture'], host)]")
    checks.append(check_policy(runtime, 'delegation', expression,
        ['parallel', 'inline', 'subagent-driven', 'inline',
         {'selection': 'host-confirmed', 'identity': 'exposed-1'},
         {'selection': 'host-default'}, {'selection': 'host-default'}],
        ("not host['worker_available']", 'False')))
    checks.append(check_policy(runtime, 'plan-execution',
        "[reusable_tasks(tasks, prior, current), reusable_tasks(tasks, prior, prior), reusable_tasks(tasks, prior, dict(current, base=dict(current['base'], source='changed'))), reusable_tasks(tasks, dict(prior, base=dict(prior['base'], result='FAIL')), current)]",
        [{'reusable': ['base', 'docs'], 'rerun': ['ui']},
         {'reusable': ['base', 'docs', 'ui'], 'rerun': []},
         {'reusable': [], 'rerun': ['base', 'docs', 'ui']},
         {'reusable': [], 'rerun': ['base', 'docs', 'ui']}],
        ("old.get('check') == now.get('check')", 'True')))
    checks.append(check_policy(runtime, 'browser-testing-with-devtools',
        "[select_evidence(['navigation', 'screenshot'], host), select_evidence(['navigation', 'network'], host), select_evidence(['screenshot'], {}), select_evidence(['screenshot', 'network'], {'instruments': [{'name': 'capture', 'available': True, 'authorized': True, 'capabilities': ['screenshot']}]}), select_evidence(['screenshot'], dict(host, native={'available': True, 'authorized': False, 'capabilities': ['screenshot']})), select_evidence(['interaction'], {'instruments': [{'name': 'existing-tests', 'available': True, 'authorized': True, 'capabilities': ['interaction']} ]})]",
        [{'tools': ['native'], 'missing': []},
         {'tools': ['native', 'instrument'], 'missing': []},
         {'tools': [], 'missing': ['screenshot']},
         {'tools': ['capture'], 'missing': ['network']},
         {'tools': ['instrument'], 'missing': []},
         {'tools': ['existing-tests'], 'missing': []}],
        ("native['authorized']", 'True')))
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--methods', type=Path, default=ROOT / 'docs/validation/andino-evolution/evolution-methods.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/validation/andino-evolution/evolution-operational.json')
    args = parser.parse_args()
    methods = json.loads(args.methods.read_text(encoding='utf-8'))
    if len(methods) != 2 or {m['id'] for m in methods} != {'brainstorming', 'workflow-advisor'}:
        raise ValueError('exactly the two new owned methods required')
    records = [check_new_method(args.runtime, method) for method in methods]
    policies = policy_checks(args.runtime)
    report = {'source_family': 'evolution', 'records': records, 'policy_checks': policies,
              'inputs': {'scripts/check_andino_evolution_methods.py': digest(Path(__file__)),
                         'scripts/check_andino_addy_methods.py': digest(ROOT / 'scripts/check_andino_addy_methods.py'),
                         args.methods.resolve().relative_to(ROOT).as_posix(): digest(args.methods)},
              'limits': 'Executed isolated guide procedures and faulty-copy mutations; no autonomous LLM routing or cross-host parity claim.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(records)} new methods, {len(policies)} extended policies; {len(records) + len(policies)} killed mutations')


if __name__ == '__main__':
    main()
