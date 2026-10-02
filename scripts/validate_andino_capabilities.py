"""Check capability contracts, oracle schemas and evidence records, never execute a model."""

import argparse
import hashlib
import json
import re
from pathlib import Path

from validate_skills import ROOT, package_files, git

SUPERPOWERS = set('systematic-debugging test-driven-development verification-before-completion brainstorming writing-plans requesting-code-review receiving-code-review dispatching-parallel-agents using-git-worktrees finishing-a-development-branch'.split())
AGENT_SKILLS = set('api-and-interface-design browser-testing-with-devtools ci-cd-and-automation code-review-and-quality code-simplification constraint-driven-development context-engineering debugging-and-error-recovery deprecation-and-migration documentation-and-adrs doubt-driven-development frontend-ui-engineering git-workflow-and-versioning incremental-implementation observability-and-instrumentation performance-optimization planning-and-task-breakdown security-and-hardening shipping-and-launch source-driven-development spec-driven-development agent-skills-test-driven-development'.split())
AGENT_SKILLS.update(('idea-refine', 'interview-me'))
OTHER_SKILLS = set('ponytail claude-mem ui-ux-pro-max design-taste-frontend clone-website graphify antislop antislop-ui antislop-copywriting antislop-human antislop-layoutmobile antislop-code'.split())
MCPS = set('context7 playwright-mcp chrome-devtools git-mcp drawio-mcp staruml-mcp premiere-pro-mcp cheatengine-mcp'.split())
CAPABILITIES = SUPERPOWERS | AGENT_SKILLS | OTHER_SKILLS | MCPS | {'native-capabilities'}
REQUIRED_CASES = set('debugging-superpowers-route no-full-superpowers-bootstrap agent-skills-no-double-router duplicate-tdd-provider ponytail-needed ponytail-not-needed claude-mem-history graphify-impact graphify-not-needed ui-ux-route taste-route ui-taste-coexistence clone-fidelity antislop-ui antislop-copy context7-version playwright-route devtools-route playwright-devtools-coexistence git-native-preferred git-mcp-fallback drawio-diagram staruml-model diagram-tool-choice premiere-preflight premiere-howto-no-mutation cheatengine-read-first cheatengine-permission unavailable-capability capability-rerouting capability-stop simple-task-zero-capability'.split())
ADDITIONAL_CASES = {'idea-refine-route', 'interview-material-only'}
EVAL_CASES = REQUIRED_CASES | ADDITIONAL_CASES
FIELDS = ('Type', 'Family/provider', 'Aliases', 'Primary purpose', 'Trigger', 'Preferred when', 'Avoid when', 'Availability check', 'Invocation method', 'First-call/preflight', 'Fallback', 'Coexistence/conflicts', 'Mutation/permission boundary', 'Verification requirement', 'Activation policy')


def registry_entries(text):
    entries = []
    for match in re.finditer(r'^## ([a-z0-9-]+)\n(.*?)(?=^## |\Z)', text, re.M | re.S):
        entries.append((match[1], dict(re.findall(r'^- ([^:\n]+): (.+)$', match[2], re.M))))
    return entries


def validate_registry(text):
    errors, seen = [], set()
    for identity, fields in registry_entries(text):
        if identity in seen:
            errors.append(f'{identity}: duplicate registry ID')
        seen.add(identity)
        for key in FIELDS:
            if not fields.get(key, '').strip():
                errors.append(f'{identity}: missing {key}')
        if fields.get('Type') not in ('skill', 'MCP', 'native'):
            errors.append(f'{identity}: invalid Type')
        expected_type = 'MCP' if identity in MCPS else 'native' if identity == 'native-capabilities' else 'skill'
        if fields.get('Type') != expected_type:
            errors.append(f'{identity}: expected type {expected_type}')
        if fields.get('Activation policy') not in ('AUTO', 'CONDITIONAL_AUTO', 'PERMISSION_GATED'):
            errors.append(f'{identity}: invalid activation policy')
        if identity not in CAPABILITIES:
            errors.append(f'{identity}: unrecognized registry ID; extend coverage deliberately')
    errors.extend(f'{identity}: missing contract' for identity in sorted(CAPABILITIES-seen))
    return errors


def validate_cases(cases, identities=CAPABILITIES):
    if not isinstance(cases, list):
        return ['cases: expected array']
    errors, seen = [], set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f'case {index}: expected object')
            continue
        identity = case.get('id')
        for field in ('id', 'kind', 'prompt', 'fixture', 'expected', 'forbidden'):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f'case {index}: missing {field}')
        if isinstance(identity, str):
            if identity in seen:
                errors.append(f'{identity}: duplicate case ID')
            seen.add(identity)
        if case.get('kind') not in ('behavior', 'negative-trigger'):
            errors.append(f'case {index}: invalid kind')
        selected = case.get('capabilities')
        if not isinstance(selected, list) or any(not isinstance(c, str) for c in selected):
            errors.append(f'case {index}: capabilities must be an array of IDs')
        else:
            errors.extend(f'case {index}: unknown capability {c}' for c in selected if c not in identities)
            if len(selected) != len(set(selected)):
                errors.append(f'case {index}: duplicate capability')
    return errors


def validate_record(record):
    if not isinstance(record, dict):
        return ['record: expected object']
    errors = []
    for field in ('case', 'scope', 'host', 'model', 'runtime_hash', 'verdict'):
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append(f'record: missing {field}')
    if record.get('scope') not in ('behavioral', 'smoke'):
        errors.append('record: scope must distinguish behavioral from smoke')
    if not re.fullmatch('[0-9a-f]{64}', record.get('runtime_hash', '') if isinstance(record.get('runtime_hash'), str) else ''):
        errors.append('record: invalid runtime content hash')
    if record.get('verdict') not in ('PASS', 'FAIL', 'NOT_VERIFIED'):
        errors.append('record: invalid verdict')
    for field in ('discovered', 'selected', 'invocations', 'fallback'):
        if not isinstance(record.get(field), list):
            errors.append(f'record: missing list {field}')
    for field in ('discovered', 'selected'):
        for item in record.get(field, []) if isinstance(record.get(field), list) else []:
            if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not isinstance(item.get('provider'), str):
                errors.append(f'record: {field} item needs actual ID and provider (UNKNOWN allowed)')
    if record.get('scope') == 'smoke' and record.get('routing_verified'):
        errors.append('record: smoke cannot establish behavioral routing')
    if record.get('verdict') in ('PASS', 'FAIL'):
        review = record.get('review')
        if not isinstance(review, dict) or not review.get('reviewer') or not review.get('reason'):
            errors.append('record: final verdict needs explicit reviewer/reason')
        if not record.get('resulting_evidence'):
            errors.append('record: final verdict needs observed evidence')
        if record.get('scope') == 'behavioral' and record.get('execution_status') != 'EXECUTED':
            errors.append('record: behavioral verdict requires executed actor, not inferred documentation')
    return errors


def case_prompt(case, runtime_metadata, catalog_metadata):
    return ('Use Andino Workflow at andino-workflow/SKILL.md for the request. '
            'This is a disposable read-only evaluation; inspect only supplied files. '
            'Do not access personal files, real memories, user application projects, network or external services. '
            'Do not write files, launch applications, spawn agents, mutate processes, commit or publish. '
            'If an instrument is not exposed here, report that limitation and use a sufficient safe local fallback. '
            'For proposed changes give concrete implementation/verification guidance. '
            'Use only actually invokable supplied skills; catalog/fixture claims do not create tools. '
            'Follow actual host permissions if narrower than scenario text.\n\n'
            + runtime_metadata + '\n\nAvailable skill metadata:\n' + catalog_metadata
            + '\n\nRaw fixture context:\n' + case.get('fixture', '')
            + '\n\nUser request:\n' + case['prompt'])


def content_hash(files):
    digest = hashlib.sha256()
    for name, value in sorted(files.items()):
        digest.update(name.encode('utf-8')+b'\0'+value.replace('\r\n','\n').encode('utf-8')+b'\0')
    return digest.hexdigest()


def runtime_files(path):
    files = {}
    for item in path.rglob('*'):
        relative = item.relative_to(path)
        if '.git' in relative.parts:
            continue
        if item.is_symlink():
            raise ValueError(f'Runtime resource must be a regular file/directory: {relative}')
        if item.is_file():
            if item.suffix != '.md':
                raise ValueError(f'Unexpected runtime resource: {relative}')
            files[relative.as_posix()] = item.read_text(encoding='utf-8')
    return files


def historical_hashes(current_hash, allow):
    if not allow:
        return set()
    lineage=json.loads((ROOT/'docs/validation/andino-workflow/capability-runtime-lineage.json').read_text(encoding='utf-8'))
    if lineage.get('current_runtime_hash') != current_hash:
        raise ValueError('Lineage does not match current runtime; historical evidence cannot be silently accepted')
    return set(lineage['historical_hashes'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--runtime', type=Path)
    source.add_argument('--runtime-ref', default=None)
    parser.add_argument('--cases-only', action='store_true')
    parser.add_argument('--records', type=Path)
    parser.add_argument('--allow-historical',action='store_true',help='Accept only documented historical hashes, never count them as current-runtime behavioral PASS')
    args = parser.parse_args()
    all_cases = json.loads((ROOT/'evals/andino-workflow.json').read_text(encoding='utf-8'))
    cases = [c for c in all_cases if isinstance(c,dict) and ('capabilities' in c or c.get('id') in REQUIRED_CASES)]
    errors = validate_cases(cases)
    ids = {c.get('id') for c in cases if isinstance(c,dict) and isinstance(c.get('id'),str)}
    errors.extend(f'{identity}: missing required routing eval' for identity in sorted(REQUIRED_CASES-ids))
    files = None
    if not args.cases_only:
        if args.runtime:
            files = runtime_files(args.runtime)
        else:
            ref = args.runtime_ref or 'origin/andino-workflow'
            names = git('ls-tree','-r','--name-only',ref).splitlines()
            files = {name:git('show',f'{ref}:{name}') for name in names}
        errors.extend(package_files(files,'andino-workflow'))
        errors.extend(validate_registry(files.get('references/capability-registry.md','')))
    if args.records:
        prior=historical_hashes(content_hash(files),args.allow_historical) if files else set()
        historical_count=0
        for path in sorted(args.records.glob('*.json')):
            try:
                record = json.loads(path.read_text(encoding='utf-8'))
                errors.extend(f'{path.name}: {e}' for e in validate_record(record))
                if not isinstance(record,dict):
                    continue
                if record.get('runtime_hash') in prior:
                    historical_count+=1
                elif files and record.get('runtime_hash') != content_hash(files):
                    errors.append(f'{path.name}: evidence belongs to different runtime content')
            except (OSError,ValueError) as exc:
                errors.append(f'{path.name}: {exc}')
        print(f'Historical records: {historical_count}; these do not prove current-runtime behavior.')
    if errors:
        print('\n'.join('FAIL: '+e for e in errors))
        return 1
    print(f'PASS: {len(cases)} capability eval schemas' + (f', {len(CAPABILITIES)} contracts; runtime SHA256 {content_hash(files)}' if files else ''))
    print('Live behavioral coverage: inspect reviewed records; schema success never implies live PASS.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
