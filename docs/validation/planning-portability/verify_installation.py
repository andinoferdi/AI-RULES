"""Read back installed native/nested resources against an immutable runtime ref."""
import argparse
import json
from pathlib import Path
import subprocess


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--runtime-ref', required=True)
parser.add_argument('--repo-root', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
catalog = json.loads((args.repo_root / 'src/ai_rules/catalog/data/hosts.json').read_text(encoding='utf-8'))
members = ('planning', 'plan-execution')
resources = ('SKILL.md', 'GUIDE.md', 'resources/contract.md', 'resources/worked-example.md')
paths = [f'skills/{member}/{resource}' for member in members for resource in resources]
paths += ['references/execution-plan.md', 'references/execution-plan-template.md']
expected = {path: subprocess.check_output(['git', 'show', f'{args.runtime_ref}:{path}'], cwd=args.repo_root)
            for path in paths}
checked = []
revisions = {}
for host in catalog['hosts']:
    skills = Path(host['global_skill_path'].replace('~', str(Path.home()), 1))
    workflow = skills / 'andino-workflow'
    if (workflow / '.git').exists():
        revision = subprocess.check_output(['git', '-C', str(workflow), 'rev-parse', 'HEAD'], text=True).strip()
        assert revision == args.runtime_ref, (host['id'], revision)
        revisions[host['id']] = revision
    for path, content in expected.items():
        locations = [workflow / path]
        if path.startswith('skills/'):
            _, member, resource = path.split('/', 2)
            locations.append(skills / f'andino-{member}' / resource)
        for installed in locations:
            assert installed.read_bytes().replace(b'\r\n', b'\n') == content.replace(b'\r\n', b'\n'), str(installed)
            checked.append({'host': host['id'], 'path': str(installed)})
profile = json.loads((Path.home() / '.ai-rules/profile.json').read_text(encoding='utf-8'))
assert profile == {
    'capabilities': ['andino-workflow', 'focus', 'search-first', 'ai-codebase-rescue',
                     'skripsi-skill', 'council', 'threejs-skills', 'natural-writing'],
    'hosts': ['codex', 'claude-code', 'opencode', 'antigravity-cli', 'antigravity-ide'],
    'profile': 'everything', 'schema_version': 1, 'scope': 'global',
}, 'Saved profile differs from the profile inspected before installation'
report = {'runtime_ref': args.runtime_ref, 'checked_files': len(checked),
          'host_revisions': revisions, 'resources': checked,
          'profile_preserved': {'profile': profile['profile'],
                                'capabilities': profile['capabilities'], 'hosts': profile['hosts']},
          'limits': 'File/content evidence only; future native session loading/use is not proved.'}
args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f'PASS: {len(checked)} installed resources, {len(catalog["hosts"])} hosts; saved profile preserved')
