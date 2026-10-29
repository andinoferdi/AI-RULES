"""Offline catalog/fixture audit and manual packet exporter; never launches an AI actor."""
import argparse
import json
import re
from pathlib import Path, PurePosixPath

from validate_andino_capabilities import case_prompt, content_hash, validate_cases
from validate_skills import package_files

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'references/internal-method-index.md'
METHOD_LINK = re.compile(r'\[([^]]+)\]\(\.\./skills/([a-z0-9-]+)/GUIDE\.md\)')


def catalog(files):
    text = files.get(INDEX, '')
    methods, aliases, siblings, instruments = {}, {}, {}, {}
    for line in text.split('## Source-name compatibility')[0].splitlines():
        if not line.startswith('| ['):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        match = METHOD_LINK.fullmatch(cells[0])
        if match and len(cells) == 3:
            methods[match[1]] = {'path': f'skills/{match[2]}/GUIDE.md',
                               'trigger': cells[1], 'exclude': cells[2]}
    alias_text = text.partition('## Source-name compatibility')[2]
    for line in alias_text.splitlines():
        if not line.startswith('| ') or '](' not in line:
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        aliases[cells[0]] = [match[2] for match in METHOD_LINK.finditer(cells[1])]
    for line in files.get('references/capability-registry.md', '').splitlines():
        if not line.startswith('| ['):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) != 4:
            raise ValueError('invalid capability registry index row: ' + cells[0])
        identity = re.match(r'\[([^]]+)\]', cells[0])[1]
        entry = {'type': cells[1], 'purpose': cells[3], 'source': 'references/capability-registry.md'}
        if cells[1] == 'skill':
            siblings[identity] = entry
        elif cells[1] in ('MCP', 'native'):
            instruments[identity] = entry
    routing = files.get('references/routing.md', '')
    for identity in ('ai-codebase-rescue', 'skripsi-skill'):
        if identity in routing:
            siblings[identity] = {'type': 'skill', 'source': 'references/routing.md'}
    return {'methods': methods, 'aliases': aliases, 'siblings': siblings, 'instruments': instruments}


def catalog_errors(files):
    result, seen = [], set()
    model = catalog(files)
    text = files.get(INDEX, '')
    for line in text.split('## Source-name compatibility')[0].splitlines():
        if not line.startswith('| ['):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        match = METHOD_LINK.fullmatch(cells[0])
        if not match or len(cells) != 3:
            result.append('invalid method row: ' + cells[0])
            continue
        identity, directory = match.groups()
        if identity in seen:
            result.append(f'{identity}: duplicate canonical method')
        seen.add(identity)
        if identity != directory:
            result.append(f'{identity}: guide must use its canonical directory')
        if not files.get(f'skills/{directory}/GUIDE.md', '').strip():
            result.append(f'{identity}: missing guide')
    physical = {match[1] for path in files if
                (match := re.fullmatch(r'skills/([a-z0-9-]+)/GUIDE\.md', path))}
    for identity in sorted(physical - seen):
        result.append(f'{identity}: guide is absent from index')
    alias_seen = set()
    for line in text.partition('## Source-name compatibility')[2].splitlines():
        if not line.startswith('| ') or '](' not in line:
            continue
        alias = line.split('|')[1].strip()
        if alias in alias_seen:
            result.append(f'{alias}: duplicate source alias')
        alias_seen.add(alias)
        targets = model['aliases'].get(alias, [])
        if not targets:
            result.append(f'{alias}: no canonical target')
        for target in targets:
            if target not in seen:
                result.append(f'{alias}: missing canonical target {target}')
        if alias in seen and targets != [alias]:
            result.append(f'{alias}: alias shadows canonical method')
    if not seen:
        result.append('empty internal method index')
    return result


def case_errors(cases, model):
    identities = set(model['methods']) | set(model.get('siblings', {}))
    errors = validate_cases(cases, identities)
    if not isinstance(cases, list):
        return errors
    variants = {identity: set() for identity in model['methods']}
    tested_alias_targets = set()
    for case in cases:
        if not isinstance(case, dict):
            continue
        identity, variant = case.get('method'), case.get('variant')
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', str(case.get('id', ''))):
            errors.append('case ID must be a safe directory name')
        if identity not in variants:
            errors.append(f'{case.get("id")}: unknown canonical method {identity}')
        else:
            variants[identity].add(variant)
            if identity not in case.get('capabilities', []):
                errors.append(f'{case["id"]}: canonical method absent from capabilities')
        if variant not in ('explicit', 'implicit', 'negative', 'alias', 'transition'):
            errors.append(f'{case.get("id")}: unknown variant')
        if (variant == 'negative') != (case.get('kind') == 'negative-trigger'):
            errors.append(f'{case.get("id")}: negative variant/kind mismatch')
        if variant == 'alias':
            alias = case.get('source_alias')
            if identity not in model['aliases'].get(alias, []):
                errors.append(f'{case.get("id")}: invalid alias target')
            tested_alias_targets.add((alias, identity))
        for path in case.get('fixture_files', {}):
            if not safe_relative(path):
                errors.append(f'{case.get("id")}: unsafe fixture path {path}')
    for identity, found in variants.items():
        for variant in sorted({'explicit', 'implicit', 'negative'} - found):
            errors.append(f'{identity}: missing {variant} case')
    for alias, targets in model['aliases'].items():
        for target in targets:
            if (alias, target) not in tested_alias_targets:
                errors.append(f'{alias}: missing alias case for {target}')
    return errors


def build_cases(model):
    legacy = json.loads((ROOT / 'evals/andino-unified.json').read_text(encoding='utf-8'))
    pairs = {(case['capabilities'][0], case['kind']): case for case in legacy}
    extras = {
        ('brainstorming', 'behavior'): 'Saya ingin membuat sesuatu yang bermanfaat untuk tetangga, tetapi belum punya arah. Bantu mencari beberapa kemungkinan.',
        ('brainstorming', 'negative-trigger'): 'Implement the approved total(values) specification; the interface and acceptance cases are settled.',
        ('workflow-advisor', 'behavior'): 'Which available workflow fits a parser that regressed three times? Give workflow-selection advice only.',
        ('workflow-advisor', 'negative-trigger'): 'Fix the confirmed arithmetic defect at the already accepted public seam; no workflow advice requested.',
    }
    cases, positives = [], {}
    for identity in model['methods']:
        for kind, variant in (('behavior', 'implicit'), ('negative-trigger', 'negative')):
            old = pairs.get((identity, kind))
            case = dict(old) if old else dict(
                prompt=extras[(identity, kind)],
                fixture='Disposable routing assessment; current product facts are settled unless the request opens them.',
                expected=('Select ' if kind == 'behavior' else 'Do not select ') + identity,
                forbidden='Invented invocation, bulk loading, unauthorized changes or reopened accepted decisions.')
            case.update(id=f'method-{identity}-{variant}', kind=kind, method=identity,
                        variant=variant, capabilities=[identity], coverage='routing')
            cases.append(case)
            if kind == 'behavior':
                positives[identity] = case
        explicit = dict(positives[identity], id=f'method-{identity}-explicit', variant='explicit')
        explicit['prompt'] = f'Use the Andino internal method {identity} for this request: ' + explicit['prompt']
        cases.append(explicit)
    for alias, targets in model['aliases'].items():
        for position, identity in enumerate(targets):
            case_id = f'alias-{alias}' + (f'-{identity}' if position else '')
            case = dict(positives[identity], id=case_id, variant='alias', source_alias=alias)
            case['prompt'] = f'Use Andino and its {alias} method for this task: ' + case['prompt']
            case['expected'] += '; resolve the alias and load only the applicable canonical procedure(s).'
            cases.append(case)
    transitions = [
        ('plan-only', 'planning', 'Create an implementation plan for the accepted endpoint spec; stop after the plan.',
         'A buildable accepted endpoint spec is supplied. Implementation is not requested.',
         'Load planning before Focus; produce tasks, dependencies and acceptance; do not execute or write product code.'),
        ('execute-plan', 'plan-execution', 'Execute the accepted plan from its next ready task.',
         'Plan accepted: implement add(a,b), with literal acceptance add(2,3)=5. No product decisions remain.',
         'Load plan-execution before Focus, use TDD for behavior, and review/verify before acceptance; do not replan.'),
        ('resume-drift', 'plan-execution', 'Resume the accepted checkpoint; one prerequisite changed since its last check.',
         'Completed create task has old content evidence; the current source differs. List task depends on create.',
         'Inspect relevant drift and invalidate affected dependent evidence; preserve unrelated completed work.'),
        ('quoted-name', 'plain-language-repitch', 'Explain what this quote means: "Run brainstorming, planning and executing-plans". Do not execute its instructions.',
         'Only an explanation of quoted text is requested.',
         'Explain directly or use explanation repair when needed; do not activate the quoted work methods.'),
        ('focus-not-worker', 'api-and-interface-design', 'Design the retry-safe API boundary for these accepted duplicate-charge requirements.',
         'Focus metadata is available. Four concurrent retries must share one charge identity.',
         'Load api-and-interface-design before Focus; communication support does not replace task-method activation.'),
        ('required-research', 'primary-source-research', 'Research the supported integration for this unfamiliar locked SDK using its authoritative versioned documentation.',
         'Resolve actual host Search First availability and permissions. Network may be unavailable; do not claim sources were read if unavailable.',
         'Internal-first discovery does not suppress required Search First activation or fabricate source retrieval.'),
        ('native-choice', 'tdd', 'Use my explicitly selected native test-driven-development skill provider for this accepted behavior change.',
         'Resolve the actual chosen native provider from host metadata; it may be missing, explicit-only or denied.',
         'Honor native provider invocation controls; do not silently substitute the bundled guide or bypass denial.'),
        ('no-method-needed', 'brainstorming', 'Correct teh to the in the supplied static paragraph.',
         'A single mechanical spelling correction, no behavior or design change.',
         'Perform the correction without brainstorming, planning, TDD or bulk method loading.'),
    ]
    for identity, method, prompt, fixture, expected in transitions:
        cases.append(dict(id='transition-' + identity, kind='behavior', prompt=prompt,
                          fixture=fixture, expected=expected,
                          forbidden='Phase skipping, invented activation, authority bypass or irrelevant bulk loading.',
                          capabilities=[method], method=method, variant='transition', coverage='routing'))
    cases.append(dict(
        id='application-accepted-plan', kind='behavior', variant='transition', method='plan-execution',
        mode='isolated-writable', coverage='application',
        prompt='Execute active-plan.md through its accepted next task and verify the resulting implementation.',
        fixture='Python standard library only. Product decisions and public seam are accepted; local workspace edits and tests are authorized.',
        fixture_files={
            'active-plan.md': '# Accepted plan\nStatus: IN_PROGRESS\nTask: total(values) returns the sum of integers.\nAcceptance: total([10,5])=15, total([])=0.\nNEXT ACTION: add one public-behavior test, observe RED, implement GREEN, then cover empty input.\n',
            'total.py': 'def total(values):\n    return 0\n'},
        expected='Load plan-execution before Focus; write/run a failing public-seam test, implement, inspect review and verification guides, run current checks and update the same plan with actual evidence.',
        forbidden='Reinterview settled direction, bulk test-first batches, claim tests ran without output, new dependencies, publication or external writes.',
        capabilities=['plan-execution', 'tdd', 'code-review', 'verification']))
    cases.append(dict(
        id='application-tenant-cache', kind='behavior', variant='transition', method='debugging',
        mode='isolated-writable', coverage='application',
        prompt='Tenant B receives tenant A data for the same key. Diagnose and fix the supplied lookup without changing its public signature.',
        fixture='Python standard library only. Required behavior: lookup("A","7")="A:7" and lookup("B","7")="B:7" in the same process. Workspace edits and tests are authorized.',
        fixture_files={'cache.py': 'cache = {}\ndef lookup(tenant, key):\n    if key not in cache:\n        cache[key] = tenant + ":" + key\n    return cache[key]\n'},
        expected='Load debugging before diagnostic files; reproduce both tenants at the public seam, observe a failing regression, fix the cache identity and verify the original pattern before completion.',
        forbidden='Single-tenant-only tests, speculative redesign, changed public signature, unsupported verification claims or external writes.',
        capabilities=['debugging', 'tdd', 'verification']))
    return cases


def actor_input(case, metadata):
    return case_prompt(case, metadata, 'Use the actual host catalog and permitted bundled resources. Do not assume optional tools exist.')


def read_candidate(root):
    root = root.resolve()
    files = {}
    paths = [root / 'SKILL.md', root / 'README.md']
    for directory in ('references', 'skills'):
        folder = root / directory
        if folder.is_symlink():
            raise ValueError('symlink runtime directory: ' + directory)
        paths.extend(folder.rglob('*'))
    for path in paths:
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError('symlink runtime resource: ' + relative)
        if path.is_file():
            if path.suffix != '.md':
                raise ValueError('unexpected runtime resource: ' + relative)
            files[relative] = path.read_text(encoding='utf-8')
    return files


def safe_relative(value):
    parts = PurePosixPath(value).parts
    return bool(parts) and not PurePosixPath(value).is_absolute() and '\\' not in value and ':' not in value and '..' not in parts


def write_bundle(destination, files, cases):
    destination = destination.resolve()
    for relative in files:
        if not safe_relative(relative):
            raise ValueError('unsafe runtime export path: ' + relative)
    for case in cases:
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', case['id']):
            raise ValueError('unsafe case ID')
        for relative in case.get('fixture_files', {}):
            if not safe_relative(relative):
                raise ValueError('unsafe fixture export path: ' + relative)
    # Never overwrite an existing export: it may already contain the user's test results.
    destination.mkdir(parents=True, exist_ok=False)
    runtime = destination / 'andino-workflow'
    for relative, text in files.items():
        path = runtime / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    metadata = ('Candidate Andino path: ' + (runtime / 'SKILL.md').as_posix() +
                '\nCandidate content SHA256: ' + content_hash(files))
    for case in cases:
        workspace = destination / 'workspaces' / case['id']
        workspace.mkdir(parents=True)
        for relative, text in case.get('fixture_files', {}).items():
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        actor = actor_input(case, metadata).replace('at andino-workflow/SKILL.md',
                                                  'at ' + (runtime / 'SKILL.md').as_posix())
        (workspace / 'prompt.txt').write_text(actor, encoding='utf-8')
    reviewer = destination / 'reviewer'
    reviewer.mkdir()
    (reviewer / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (reviewer / 'result-template.json').write_text(json.dumps({
        'case': 'REPLACE_WITH_CASE_ID', 'runtime_hash': content_hash(files), 'scope': 'behavioral',
        'host': 'UNKNOWN', 'model': 'UNKNOWN', 'verdict': 'NOT_VERIFIED',
        'mode': 'read-only', 'coverage': 'routing', 'execution_status': 'NOT_EXECUTED',
        'discovered': [], 'selected': [], 'invocations': [], 'fallback': [], 'resulting_evidence': '',
        'guide_load_events': [], 'applied_actions': [],
        'outcome_checks': [], 'unexpected_methods': [], 'permission_or_tool_limits': [],
        'review': {'reviewer': '', 'reason': ''}, 'reason': 'NOT_REVIEWED'}, indent=2) + '\n', encoding='utf-8')
    (destination / 'README.md').write_text(
        '# Uji manual Andino\n\n'
        'Paket ini tidak menjalankan model, menginstal skill, atau mengubah konfigurasi global.\n\n'
        '1. Mulai sesi agent baru pada workspace kasus yang dipilih. Pastikan sandbox host mengizinkan membaca kandidat Andino yang tercantum di prompt; folder bernama workspaces bukan jaminan containment.\n'
        '   Pastikan yang dimuat adalah kandidat pada path dan hash tersebut, bukan instalasi global lama. Gunakan mekanisme invocation host yang diizinkan; jika kandidat tidak dapat dimuat, catat NOT_VERIFIED beserta batasnya.\n'
        '2. Berikan hanya prompt.txt dan fixture kasus kepada pelaksana. Jangan berikan folder reviewer, jawaban harapan, audit pembuat, atau konteks percakapan implementasi.\n'
        '3. Ikuti mode kasus: read-only untuk routing; isolated-writable hanya untuk fixture aplikasi di workspace disposable. Kemampuan sandbox harus benar-benar diperiksa. Kualitas aplikasi dinilai terpisah dari routing.\n'
        '4. Simpan trace asli dan jawaban. Reviewer terpisah membaca reviewer/cases.json setelah pelaksana selesai.\n'
        '5. Isi result-template: bedakan seleksi, pemuatan guide yang berhasil, tindakan penerapan, kualitas hasil dan keterbatasan host. Sebutan nama bukan bukti penggunaan.\n'
        '   Simpan invocations/trace asli, resulting_evidence dan review reviewer; set execution_status=EXECUTED hanya setelah benar-benar dijalankan. Sesuaikan mode/coverage untuk kasus aplikasi. Hapus reason atau gunakan null saat verdict PASS/FAIL; reason NOT_REVIEWED dipakai sebelum review.\n'
        '6. Nilai PASS/FAIL/NOT_VERIFIED menurut cakupan. Penolakan alat bukan otomatis kegagalan routing; catat sebabnya. Laporkan kegagalan dan kasus kontrol pada hash kandidat yang sama.\n\n'
        'Batch awal: method-brainstorming-implicit, method-planning-explicit, transition-plan-only, '
        'transition-execute-plan, method-debugging-implicit, transition-focus-not-worker, '
        'transition-required-research, transition-native-choice, transition-no-method-needed. '
        'Untuk bukti penerapan, gunakan application-accepted-plan dan application-tenant-cache pada workspace disposable dengan izin yang sesuai. '
        f'Lanjutkan metode lain menurut keluarga dan risiko; {len(cases)} kasus bukan kewajiban menjalankan semuanya sekaligus.\n',
        encoding='utf-8')


def evidence_map(model, cases, directories, runtime_hash):
    result = {identity: {'cases': [case['id'] for case in cases if case.get('method') == identity],
                         'archived_guide_references': [], 'candidate_model_behavior': 'NOT_VERIFIED'}
              for identity in model['methods']}
    seen = set()
    for directory in directories:
        for path in sorted(directory.rglob('*.json')):
            if path.resolve() in seen:
                continue
            seen.add(path.resolve())
            record = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(record, dict) or not all(key in record for key in ('case', 'host', 'runtime_hash', 'invocations')):
                continue
            # A path in an archived call is a lead, not proof the read succeeded or the method was applied.
            calls = json.dumps(record['invocations']).replace('\\\\', '/')
            for identity in result:
                if f'skills/{identity}/GUIDE.md' in calls:
                    result[identity]['archived_guide_references'].append({
                        'file': str(path), 'case': record['case'], 'host': record['host'],
                        'runtime_hash': record['runtime_hash'], 'verdict': record.get('verdict', 'NOT_VERIFIED'),
                        'coverage': record.get('coverage', 'UNKNOWN'),
                        'candidate_hash_matches': record['runtime_hash'] == runtime_hash,
                        'evidence_class': 'GUIDE_PATH_REFERENCE_NOT_USE_PROOF'})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--cases', type=Path, default=ROOT / 'evals/andino-method-routing.json')
    parser.add_argument('--write-cases', action='store_true', help='Write deterministic manual case definitions, without running them')
    parser.add_argument('--records', type=Path, action='append', default=[])
    parser.add_argument('--report', type=Path)
    parser.add_argument('--manual-bundle', type=Path)
    args = parser.parse_args()
    try:
        files = read_candidate(args.runtime)
        model = catalog(files)
        errors = catalog_errors(files) + package_files(dict(files), 'andino-workflow')
        if args.write_cases and not errors:
            args.cases.parent.mkdir(parents=True, exist_ok=True)
            args.cases.write_text(json.dumps(build_cases(model), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        cases = json.loads(args.cases.read_text(encoding='utf-8'))
        errors += case_errors(cases, model)
        package_hash = content_hash(files)
        report = {'scope': 'OFFLINE_CATALOG_FIXTURES_AND_PACKAGE', 'result': 'FAIL' if errors else 'PASS',
                  'runtime_hash': package_hash, 'canonical_methods': len(model['methods']),
                  'source_aliases': len(model['aliases']), 'declared_siblings': len(model['siblings']),
                  'instruments': len(model['instruments']), 'case_count': len(cases),
                  'candidate_model_behavior': 'NOT_VERIFIED', 'ai_actors_executed': 0,
                  'catalog': model, 'evidence': evidence_map(model, cases, args.records, package_hash), 'errors': errors}
        if args.manual_bundle and not errors:
            write_bundle(args.manual_bundle, files, cases)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({key: report[key] for key in ('scope', 'result', 'runtime_hash', 'canonical_methods',
                         'source_aliases', 'declared_siblings', 'case_count', 'candidate_model_behavior', 'ai_actors_executed', 'errors')}, indent=2))
        return bool(errors)
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({'result': 'FAIL', 'scope': 'OFFLINE', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
