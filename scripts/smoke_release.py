"""Check a standalone install against every file in its frozen bundles."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def verify_bundle_files(expected: Path, installed: Path) -> int:
    checked = 0
    for source in expected.rglob('*'):
        if not source.is_file():
            continue
        relative = source.relative_to(expected)
        target = installed / relative
        if not target.is_file():
            raise ValueError(f'release resource missing: {relative.as_posix()}')
        if target.read_bytes() != source.read_bytes():
            raise ValueError(f'release resource changed: {relative.as_posix()}')
        checked += 1
    if not checked:
        raise ValueError('no release resources checked')
    return checked


def main() -> int:
    from build_release import stage_bundles

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executable', type=Path, required=True)
    args = parser.parse_args()
    executable = args.executable.resolve(strict=True)
    root = Path(__file__).resolve().parents[1]
    manifest = root / 'src/ai_rules/release/data/release_manifest.json'
    targets = json.loads(manifest.read_text(encoding='utf-8'))['first_party']
    with tempfile.TemporaryDirectory(prefix='ai-rules-release-smoke-') as directory:
        temporary = Path(directory).resolve()
        if not temporary.is_relative_to(Path(tempfile.gettempdir()).resolve()):
            raise ValueError('smoke directory is outside the temporary root')
        expected, project, state = temporary / 'expected', temporary / 'project', temporary / 'state'
        stage_bundles(targets, expected, root)
        env = dict(os.environ, PATH='')
        subprocess.run([str(executable), '--help'], cwd=temporary, env=env, check=True)
        subprocess.run([
            str(executable), 'setup', '--source', 'bundled', '--profile', 'everything',
            '--host', 'codex', '--scope', 'project', '--project-root', str(project),
            '--state-dir', str(state), '--yes', '--non-interactive',
        ], cwd=temporary, env=env, check=True)
        checked = verify_bundle_files(expected, project / '.agents/skills')
        lock = json.loads((state / 'lock.json').read_text(encoding='utf-8'))
        if (len(lock['targets']) != len(targets)
                or any(target['status'] != 'VERIFIED' for target in lock['targets'])):
            raise ValueError('bundled installation did not verify every target')
        print(f'PASS: {len(targets)} bundled packages, {checked} identical resource files, '
              'verified lock targets; installation without Git')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
