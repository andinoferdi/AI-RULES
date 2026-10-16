"""Validate Three.js inventory, isolated packages and review-only routing scenarios."""

import argparse
import hashlib
import json
from pathlib import Path

from validate_skills import ROOT, directory_files, ref_files, package_files, THREEJS_SKILLS
from validate_andino_capabilities import validate_cases, CAPABILITIES, OPTIONAL_CAPABILITIES


def validate_inventory(inventory, files, original=None):
    errors = []
    names = [s['name'] for s in inventory['skills']]
    if len(names) != len(set(names)) or set(names) != THREEJS_SKILLS - {'threejs-skills'}:
        errors.append('inventory/catalog identity mismatch')
    expected_paths = {'README.md', 'SKILL.md', 'entrypoint/README.md', 'entrypoint/SKILL.md'}
    for skill in inventory['skills']:
        prefix = 'skills/' + skill['name'] + '/'
        for entry in skill['files'] + skill.get('added_files', []):
            path = prefix + entry['path']
            expected_paths.add(path)
            content = files.get(path)
            if content is None:
                errors.append(f'missing inventoried resource: {path}')
                continue
            data = content.encode('utf-8') if isinstance(content, str) else content
            if entry.get('kind') != 'binary':
                data = data.replace(b'\r\n', b'\n')
            expected = entry.get('runtime_sha256', entry['sha256'])
            if hashlib.sha256(data).hexdigest() != expected:
                errors.append(f'runtime resource changed since inventory: {path}')
            if original is not None and 'runtime_sha256' in entry:
                source = original / skill['name'] / entry['path']
                if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
                    errors.append(f'original source missing/changed: {source}')
            if entry.get('findings'):
                errors.append(f'unresolved sensitive-content finding: {path}')
    if set(files) != expected_paths:
        errors.append(f'uninventoried resources: {sorted(set(files)-expected_paths)}')
    if original is not None:
        actual = {p.relative_to(original).as_posix() for p in original.rglob('*') if p.is_file()}
        wanted = {s['name'] + '/' + e['path'] for s in inventory['skills'] for e in s['files']}
        if actual != wanted:
            errors.append('original file set differs from inventory')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument('--runtime-dir', type=Path)
    selection.add_argument('--runtime-ref')
    parser.add_argument('--original', type=Path, help='also prove supplied source has not changed')
    args = parser.parse_args()
    inventory = json.loads((ROOT / 'docs/threejs/inventory.json').read_text(encoding='utf-8'))
    files, modes = directory_files(args.runtime_dir) if args.runtime_dir else ref_files(args.runtime_ref)
    errors = validate_inventory(inventory, files, args.original)
    for name in sorted(THREEJS_SKILLS):
        prefix = 'entrypoint/' if name == 'threejs-skills' else f'skills/{name}/'
        errors += package_files({p[len(prefix):]: v for p, v in files.items() if p.startswith(prefix)},
                                name, {p[len(prefix):]: v for p, v in modes.items() if p.startswith(prefix)})
    cases = json.loads((ROOT / 'evals/threejs-routing.json').read_text(encoding='utf-8'))
    errors += validate_cases(cases, CAPABILITIES | OPTIONAL_CAPABILITIES)
    if errors:
        print('\n'.join('FAIL: ' + e for e in errors))
        return 1
    print(f"PASS: {len(inventory['skills'])} source skills, {sum(len(s['files']) for s in inventory['skills'])} original resources, {len(THREEJS_SKILLS)} standalone packages; {len(cases)} review-only scenario schemas")
    print('Live routing/host use is separate; schema validation is not behavioral verification.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
