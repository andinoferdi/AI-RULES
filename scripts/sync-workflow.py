"""Generate identical Andino skill installs; never silently overwrite local edits."""
from pathlib import Path
import argparse, importlib.util

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/andino-workflow'
DESTINATIONS = ['.agents/skills/andino-workflow', '.claude/skills/andino-workflow',
                '.config/opencode/skills/andino-workflow', '.gemini/config/skills/andino-workflow']

_spec = importlib.util.spec_from_file_location("managed_skill_sync", ROOT / "scripts/sync-skills.py")
_managed = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_managed)
hashes = _managed.hashes

def sync(home, check=False):
    return _managed.sync_tree(SOURCE, DESTINATIONS, home, check)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home(), help='Target home; defaults to current user')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    sync(args.home.resolve(), args.check)
