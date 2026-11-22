from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import shutil
import sys
import re
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ai_rules.release.bundles import export_git_ref, validate_subpath
from validate_skills import directory_files, package_files


def stage_bundles(targets: dict, destination: Path, repo_root: Path) -> dict:
    if not targets:
        raise ValueError('release manifest has no first-party bundles')
    for identifier in targets:
        validate_subpath(identifier)
        if '/' in identifier:
            raise ValueError('release capability must be a single directory name')
    # Refuse pre-existing bundles: they may contain maintainer work.
    destination.mkdir(parents=True, exist_ok=False)
    for identifier, target in targets.items():
        package = destination / identifier
        export_git_ref(target['commit'], package, repo_root, subpath=target.get('subpath'))
        body = (package / 'SKILL.md').read_text(encoding='utf-8')
        if not re.search(rf'^name:\s*{re.escape(identifier)}\s*$', body, re.M):
            raise ValueError(f'release bundle identity mismatch: {identifier}')
        files, modes = directory_files(package)
        errors = package_files(files, identifier, modes)
        if errors:
            raise ValueError(f'invalid release bundle {identifier}:\n' + '\n'.join(errors))
    return targets


def release_targets(root: Path) -> dict:
    # Every first-party skill ships from skills/<id> at the commit being built.
    catalog = json.loads((root / 'src/ai_rules/catalog/data/capabilities.json').read_text(encoding='utf-8'))
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    return {item['id']: {'commit': commit, 'subpath': item['source']['subpath']}
            for item in catalog['capabilities'] if item['ownership'] == 'FIRST_PARTY'}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and checksum the standalone AI-RULES executable")
    parser.add_argument("--output", type=Path, default=Path("dist"))
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--asset-name", help="published filename (defaults to the PyInstaller filename)")
    parser.add_argument('--stage-only', action='store_true', help='export bundles and source evidence locally without building an executable')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (root / args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    staged_bundles = root / "src" / "ai_rules" / "release" / "data" / "bundles"
    targets = release_targets(root)
    if args.stage_only:
        stage_bundles(targets, output / 'bundles', root)
        (output / 'bundle-sources.json').write_text(json.dumps(targets, indent=2) + '\n', encoding='utf-8')
        print(f'Exported {len(targets)} bundles with source traceability to {output}')
        return 0
    if staged_bundles.exists():
        raise SystemExit(f'preserving existing bundles; review before building: {staged_bundles}')
    stage_bundles(targets, staged_bundles, root)
    # Bundled installs compare versions by this commit count; it only grows along main.
    sequence = int(subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], cwd=root, text=True).strip())
    (staged_bundles / 'bundle-sources.json').write_text(json.dumps(
        {'commit': next(iter(targets.values()))['commit'], 'sequence': sequence}) + '\n', encoding='utf-8')
    try:
        if not args.skip_build:
            subprocess.run(
                [sys.executable, "-m", "PyInstaller", "packaging/ai_rules.spec", "--noconfirm",
                 "--workpath", str(output / 'pyinstaller-work'), "--distpath", str(output)],
                cwd=root,
                env=dict(os.environ, PYTHONPATH=str(root / 'src') + os.pathsep + os.environ.get('PYTHONPATH', '')),
                check=True,
            )
    finally:
        shutil.rmtree(staged_bundles, ignore_errors=True)
    built = output / ("ai-rules.exe" if platform.system().lower() == "windows" else "ai-rules")
    if args.asset_name and built.exists() and built.name != args.asset_name:
        built.rename(output / args.asset_name)
    artifacts = sorted(path for path in output.iterdir() if path.is_file() and path.name.startswith("ai-rules"))
    if not artifacts:
        raise SystemExit("no standalone ai-rules artifact found")
    manifest = {
        "schema_version": 1,
        "platform": {"system": platform.system().lower(), "architecture": platform.machine().lower()},
        "artifacts": [{"name": path.name, "sha256": sha256(path), "size": path.stat().st_size} for path in artifacts],
        "first_party": targets,
    }
    try:
        manifest["source_commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        manifest['source_dirty'] = bool(subprocess.check_output(
            ['git', 'status', '--porcelain', '--untracked-files=no'], cwd=root, text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        manifest["source_commit"] = "unknown"
    (output / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (output / "SHA256SUMS").write_text(
        "".join(f"{entry['sha256']}  {entry['name']}\n" for entry in manifest["artifacts"]),
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
