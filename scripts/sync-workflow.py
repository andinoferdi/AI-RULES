"""Generate identical Andino skill installs; never silently overwrite local edits."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/andino-workflow'
DESTINATIONS = ['.agents/skills/andino-workflow', '.claude/skills/andino-workflow',
                '.config/opencode/skills/andino-workflow', '.gemini/config/skills/andino-workflow']

def hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and p.name != '.andino-generated.json'}

def sync(home, check=False):
    expected = hashes(SOURCE)
    for relative in DESTINATIONS:
        destination = home / relative
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
        shutil.copytree(SOURCE, temp, dirs_exist_ok=True)
        (temp / '.andino-generated.json').write_text(json.dumps({'source': str(SOURCE), 'files': expected}, indent=2))
        if destination.exists():
            backup_root = home / '.andino/backups/sync'
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = Path(tempfile.mkdtemp(prefix='previous-', dir=backup_root)) / 'andino-workflow'
            if not destination.absolute().is_relative_to(home.absolute()):
                raise RuntimeError('Destination outside selected home')
            destination.rename(backup)
        temp.rename(destination)
        print(f'SYNC {relative}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home(), help='Target home; defaults to current user')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    sync(args.home.resolve(), args.check)
