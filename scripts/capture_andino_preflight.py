"""Capture local integration evidence without modifying Git or source snapshots."""
import hashlib
import json
import platform
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True,
                            text=True, encoding='utf-8', check=True)
    return result.stdout.strip()


def capture(runtime):
    states = {}
    repositories = [('runtime', runtime), ('main', ROOT)]
    repositories += [(name, runtime / name) for name in
                     ('addyosmani-agent-skills', 'mattpocock-skills', 'obra-superpowers')]
    for name, root in repositories:
        status = git(root, 'status', '--porcelain=v1', '--untracked-files=all').splitlines()
        states[name] = {
            'path': str(root), 'root': git(root, 'rev-parse', '--show-toplevel'),
            'branch': git(root, 'branch', '--show-current'),
            'head': git(root, 'rev-parse', 'HEAD'),
            'head_tree': git(root, 'rev-parse', 'HEAD^{tree}'),
            'tracked_changes': [s for s in status if not s.startswith('??')],
            'untracked_by_top_level': dict(Counter(s[3:].split('/')[0] for s in status if s.startswith('??'))),
            'status_sha256': hashlib.sha256('\n'.join(status).encode()).hexdigest(),
            'worktrees': git(root, 'worktree', 'list', '--porcelain'),
            'remotes': git(root, 'remote', '-v'),
        }
    refs = git(runtime, 'for-each-ref', '--format=%(refname:short) %(objectname)',
               'refs/heads', 'refs/remotes/origin')
    prompts = {p: hashlib.sha256((runtime / p).read_bytes()).hexdigest()
               for p in ('ULTIMATE-PROMPT.md', 'GRAND-PLAN.md')}
    return dict(captured_at_utc=datetime.now(timezone.utc).isoformat(),
                platform=platform.platform(), states=states, refs=refs, prompts=prompts,
                safety='No branch creation, staging, commit, push, reset, stash or upstream write.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = capture(args.runtime.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({name: s['branch'] for name, s in result['states'].items()}))
