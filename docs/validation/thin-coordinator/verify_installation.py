"""Compare the entire published workflow and all native members on installed hosts."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo-root', type=Path, required=True)
parser.add_argument('--runtime-ref', required=True)
parser.add_argument('--profile-baseline', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
archive = subprocess.check_output(['git', 'archive', '--format=zip', args.runtime_ref], cwd=args.repo_root)
with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
    expected = {entry.filename: bundle.read(entry).replace(b'\r\n', b'\n')
                for entry in bundle.infolist() if not entry.is_dir()}
catalog = json.loads((args.repo_root / 'src/ai_rules/catalog/data/hosts.json').read_text(encoding='utf-8'))
counts, revisions = {}, {}
for host in catalog['hosts']:
    skills = Path(host['global_skill_path'].replace('~', str(Path.home()), 1))
    workflow = skills / 'andino-workflow'
    if (workflow / '.git').exists():
        revision = subprocess.check_output(['git', '-C', str(workflow), 'rev-parse', 'HEAD'], text=True).strip()
        assert revision == args.runtime_ref, (host['id'], revision)
        revisions[host['id']] = revision
    count = 0
    for path, content in expected.items():
        destinations = [workflow / path]
        if path.startswith('skills/'):
            _, member, resource = path.split('/', 2)
            destinations.append(skills / f'andino-{member}' / resource)
        for destination in destinations:
            assert destination.read_bytes().replace(b'\r\n', b'\n') == content, str(destination)
            count += 1
    counts[host['id']] = count
profile = Path.home() / '.ai-rules/profile.json'
assert profile.read_bytes() == args.profile_baseline.read_bytes(), 'Saved profile changed'
digest = hashlib.sha256('\n'.join(path + ':' + hashlib.sha256(content).hexdigest()
                                for path, content in sorted(expected.items())).encode()).hexdigest()
report = {'runtime_ref': args.runtime_ref, 'source_files': len(expected),
          'source_content_manifest_sha256': digest, 'checked_files': sum(counts.values()),
          'per_host_checked_files': counts, 'host_revisions': revisions,
          'profile_unchanged': True,
          'limits': 'File equality/revision evidence; native host loading and future skill use are not proved.'}
args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f'PASS: {sum(counts.values())} complete workflow/native-member file comparisons across {len(counts)} hosts; profile unchanged')
