"""Exercise an unpublished working-tree bundle through the real offline setup CLI.

Only disposable project/home/state directories are mutated. No fixture commits,
branches, remote fetch, global setup or release-manifest file changes are made.
"""
import argparse
import contextlib
import copy
import hashlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from ai_rules import cli
from ai_rules.catalog import load_catalog
from ai_rules.profiles import load_profiles
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.domain.statuses import Scope
from ai_rules.release.bundles import export_git_ref
from ai_rules.release.latest import contents
from validate_skills import directory_files, package_files
from validate_andino_capabilities import content_hash


def run_checks(runtime, workspace):
    files, modes = directory_files(runtime)
    assert not package_files(files, 'andino-workflow', modes)
    candidate_hash = content_hash(files)
    assert len(list(runtime.rglob('SKILL.md'))) == 1
    catalog = load_catalog()
    manifest = json.loads((ROOT/'src/ai_rules/release/data/release_manifest.json').read_text())
    bundles = {'andino-workflow': runtime}
    for identity in catalog.capabilities:
        if identity == 'andino-workflow':
            continue
        bundle = workspace/'bundles'/identity
        ref = f'origin/{identity}'
        export_git_ref(ref, bundle, repo_root=ROOT)
        bundles[identity] = bundle
        manifest['first_party'][identity]['commit'] = subprocess.check_output(
            ['git', 'rev-parse', ref], cwd=ROOT, text=True).strip()
    # Versions here identify fixture transitions, not published candidate commits.
    manifest['first_party']['andino-workflow']['release_sequence'] += 1
    manifest['first_party']['andino-workflow']['publication_status'] = 'UNPUBLISHED_WORKING_TREE_FIXTURE'
    home = workspace/'home'
    home.mkdir()
    profiles = load_profiles(catalog)
    records = []

    def invoke(project, state, host, selections, expected=0, current_manifest=None):
        chosen_manifest = current_manifest or manifest
        output = io.StringIO()
        with patch.object(Path, 'home', return_value=home), \
             patch.object(cli, 'packaged_bundle', side_effect=lambda identity: bundles[identity]), \
             patch.object(cli, 'export_git_ref', side_effect=AssertionError('Git fallback forbidden in offline fixture')), \
             patch.object(cli, 'LatestSources', side_effect=AssertionError('Network source forbidden')), \
             patch.object(cli, '_release_manifest', return_value=chosen_manifest), \
             patch('ai_rules.capabilities.adapters._load_release_manifest', return_value=chosen_manifest), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = cli.main(['setup', '--host', host, '--scope', 'project',
                             '--project-root', str(project), '--state-dir', str(state),
                             '--source', 'bundled', '--yes', '--non-interactive', *selections])
        assert code == expected, (code, output.getvalue())
        return output.getvalue()

    with patch.object(Path, 'home', return_value=home):
        adapters = build_host_adapters(catalog.hosts)
    for host, adapter in adapters.items():
        for profile in [*profiles.profiles, 'custom']:
            project = workspace/'projects'/host/profile
            state = project/'fixture-state'
            selections = ['--capability', 'andino-workflow'] if profile == 'custom' else ['--profile', profile]
            invoke(project, state, host, selections)
            target = adapter.skill_target(Scope.PROJECT, project)/'andino-workflow'
            assert contents(target) == contents(runtime)
            assert len(list(target.rglob('SKILL.md'))) == 1
            assert len(list(target.glob('skills/*/GUIDE.md'))) == len(list(runtime.glob('skills/*/GUIDE.md')))
            assert not any((target/p).exists() for p in ('addyosmani-agent-skills', 'mattpocock-skills', 'obra-superpowers'))
            invoke(project, state, host, selections)
            lock = json.loads((state/'lock.json').read_text())
            assert all(t['action'] == 'NO_OP' for t in lock['targets'])
            records.append(dict(host=host, profile=profile, fresh='PASS', repeat='NO_OP',
                                files=len(contents(target)), native_identities=1,
                                verification='STRUCTURAL VERIFIED; native live discovery NOT VERIFIED'))

        project = workspace/'edited'/host
        state = project/'fixture-state'
        invoke(project, state, host, ['--capability', 'andino-workflow'])
        target = adapter.skill_target(Scope.PROJECT, project)/'andino-workflow'
        personal = target/'skills/tdd/GUIDE.md'
        personal.write_text('User-owned content to preserve\n', encoding='utf-8')
        before = contents(target)
        invoke(project, state, host, ['--capability', 'andino-workflow'], expected=1)
        assert contents(target) == before
        records.append(dict(host=host, scenario='managed-user-edit', blocked=True, preserved=True))

        conflict_project = workspace/'conflict'/host
        conflict_state = conflict_project/'fixture-state'
        conflict = adapter.skill_target(Scope.PROJECT, conflict_project)/'andino-workflow'
        conflict.mkdir(parents=True)
        (conflict/'personal.txt').write_text('unmanaged user file', encoding='utf-8')
        before = contents(conflict)
        invoke(conflict_project, conflict_state, host, ['--capability', 'andino-workflow'], expected=1)
        assert contents(conflict) == before
        records.append(dict(host=host, scenario='unmanaged-conflict', blocked=True, preserved=True))

    project, state = workspace/'upgrade', workspace/'upgrade-state'
    invoke(project, state, 'codex', ['--capability', 'andino-workflow'])
    target = adapters['codex'].skill_target(Scope.PROJECT, project)/'andino-workflow'
    original = contents(target)
    upgraded = workspace/'upgrade-source'
    shutil.copytree(runtime, upgraded)
    with (upgraded/'README.md').open('a', encoding='utf-8') as handle:
        handle.write('\nDisposable update fixture.\n')
    bundles['andino-workflow'] = upgraded
    next_manifest = copy.deepcopy(manifest)
    next_manifest['first_party']['andino-workflow']['release_sequence'] += 1
    invoke(project, state, 'codex', ['--capability', 'andino-workflow'], current_manifest=next_manifest)
    assert contents(target) == contents(upgraded)
    backups = list((state/'backups').glob('*/andino-workflow'))
    assert any(contents(backup) == original for backup in backups)
    invoke(project, state, 'codex', ['--capability', 'andino-workflow'], current_manifest=next_manifest)
    lock = json.loads((state/'lock.json').read_text())
    assert all(t['action'] == 'NO_OP' for t in lock['targets'])
    records.append(dict(host='codex', scenario='clean-update', updated=True, original_backup_verified=True, repeat='NO_OP'))
    return dict(result='PASS', candidate_runtime_sha256=candidate_hash,
                records=records, profiles=len(profiles.profiles), host_surfaces=len(adapters),
                upstream_sources_available_to_installer=False, network_source_used=False,
                limitation='Bundled working-tree bytes and actual sibling exports; synthetic fixture version transitions are not publication pins. Host paths and invocation-file checks do not prove native discovery or model use.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'docs/validation/andino-unified/installation.json')
    args = parser.parse_args()
    with TemporaryDirectory(prefix='andino-install-proof-') as temporary:
        result = run_checks(args.runtime.resolve(), Path(temporary))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(f"PASS: {len(result['records'])} offline installer scenarios; candidate {result['candidate_runtime_sha256']}")


if __name__ == '__main__':
    main()
