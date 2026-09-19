"""Sync an explicit set of canonical skills; never overwrite unmanaged or local drift."""
from pathlib import Path
import argparse, hashlib, json, shutil, tempfile

ROOT = Path(__file__).resolve().parents[1]
MANAGED_SKILLS = ("andino-workflow", "ai-codebase-rescue")
HOST_ROOTS = (".agents/skills", ".claude/skills",
              ".config/opencode/skills", ".gemini/config/skills")

def hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and p.name != '.andino-generated.json'}

def sync_tree(source, destinations, home, check=False):
    if not (source / 'SKILL.md').is_file():
        raise RuntimeError(f'Missing canonical skill: {source}')
    expected = hashes(source)
    for relative in destinations:
        destination = home / relative
        if not destination.resolve().is_relative_to(home.resolve()):
            raise RuntimeError("Destination outside selected home")
        marker = destination / '.andino-generated.json'
        if destination.exists():
            current = hashes(destination)
            if current == expected:
                print(f'OK {relative}')
                continue
            if check:
                raise RuntimeError(f'Drift: {relative}')
            if not marker.exists() or current != json.loads(marker.read_text())['files']:
                raise RuntimeError(f'Unmanaged or locally edited install: {relative}; reconcile before sync')
        elif check:
            raise RuntimeError(f'Missing: {relative}')
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Copy the full tree before replacing; retain old install in the local backup area.
        temp = Path(tempfile.mkdtemp(prefix='andino-stage-', dir=destination.parent))
        shutil.copytree(source, temp, dirs_exist_ok=True)
        (temp / '.andino-generated.json').write_text(json.dumps({'source': str(source), 'files': expected}, indent=2))
        if destination.exists():
            backup_root = home / '.andino/backups/sync'
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = Path(tempfile.mkdtemp(prefix='previous-', dir=backup_root)) / destination.name
            if not destination.absolute().is_relative_to(home.absolute()):
                raise RuntimeError('Destination outside selected home')
            destination.rename(backup)
        temp.rename(destination)
        print(f'SYNC {relative}')

def sync(home, check=False, skills=MANAGED_SKILLS, source_root=None):
    """Sync only named managed skills; source_root supports isolated fixtures."""
    selected = tuple(dict.fromkeys(skills))
    if not selected or any(name not in MANAGED_SKILLS for name in selected):
        raise ValueError('Select only explicit managed skills: ' + ', '.join(MANAGED_SKILLS))
    source_root = ROOT / 'skills' if source_root is None else Path(source_root)
    for name in selected:
        if not (source_root / name / 'SKILL.md').is_file():
            raise RuntimeError(f'Missing canonical skill: {source_root / name}')
    for name in selected:
        sync_tree(source_root / name, [f'{root}/{name}' for root in HOST_ROOTS], home, check)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home(), help='Target home; defaults to current user')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--skill', action='append', choices=MANAGED_SKILLS,
                        help='Select a managed skill; repeat to select several; defaults to both')
    args = parser.parse_args()
    sync(args.home.resolve(), args.check, MANAGED_SKILLS if args.skill is None else args.skill)

