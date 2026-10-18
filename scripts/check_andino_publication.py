"""Verify published default-latest setup in disposable projects, never global skills."""
import contextlib
import io
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'scripts')]
from ai_rules import cli
from ai_rules.release.bundles import export_git_ref
from ai_rules.release.latest import contents
from validate_andino_capabilities import content_hash, runtime_files


def main():
    evidence = ROOT / 'docs/validation/andino-unified'
    manifest = json.loads((ROOT / 'src/ai_rules/release/data/release_manifest.json').read_text(encoding='utf-8'))
    expected = manifest['first_party']['andino-workflow']['commit']
    lineage = json.loads((evidence / 'publication-lineage.json').read_text(encoding='utf-8'))
    old_manifest = json.loads((evidence / 'pre-publication/release_manifest.json').read_text(encoding='utf-8'))
    prior = old_manifest['first_party']['andino-workflow']['commit']
    records = []
    with TemporaryDirectory(prefix='andino-published-proof-') as temporary:
        workspace = Path(temporary).resolve()
        home = workspace / 'home'
        home.mkdir()
        old = workspace / 'prior-official'
        export_git_ref(prior, old, ROOT)
        original = contents(old)
        for scenario in ('fresh', 'upgrade'):
            project = workspace / scenario
            state = workspace / (scenario + '-state')
            target = project / '.agents/skills/andino-workflow'
            if scenario == 'upgrade':
                export_git_ref(prior, target, ROOT)
            for attempt in ('first', 'repeat'):
                args = ['setup', '--host', 'codex', '--scope', 'project',
                        '--project-root', str(project), '--state-dir', str(state),
                        '--capability', 'andino-workflow', '--yes', '--non-interactive']
                output = io.StringIO()
                # Only the home path is redirected. Source/catalog/manifest/network
                # acquisition are real; --source is deliberately omitted (latest).
                with patch.object(Path, 'home', return_value=home), \
                     contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                    code = cli.main(args)
                observed = output.getvalue()
                assert code == 0, observed
                installed_hash = content_hash(runtime_files(target))
                assert installed_hash == lineage['to_runtime_hash']
                lock = json.loads((state / 'lock.json').read_text(encoding='utf-8'))
                if attempt == 'repeat':
                    assert all(t['action'] == 'NO_OP' for t in lock['targets'])
                if scenario == 'upgrade' and attempt == 'first':
                    assert any(contents(p) == original for p in (state / 'backups').glob('*/andino-workflow'))
                assert expected in json.dumps(lock)
                records.append(dict(scenario=scenario, attempt=attempt, exit_code=code,
                                    command=['python', '-m', 'ai_rules', *args],
                                    installed_runtime_hash=installed_hash,
                                    actions=[t['action'] for t in lock['targets']],
                                    output=observed.replace(str(workspace), '<disposable-root>')))
    report = dict(result='PASS', source='real default latest; no source/catalog/network override',
                  repository='https://github.com/andinoferdi/AI-RULES.git',
                  published_runtime_commit=expected, previous_commit=prior,
                  sibling_pins_unchanged=all(v == manifest['first_party'][k]
                      for k, v in old_manifest['first_party'].items() if k != 'andino-workflow'),
                  global_installation_modified=False, records=records,
                  limit='Actual remote acquisition and disposable file/state verification; native host discovery/use is not proved.')
    (evidence / 'published-setup.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('PASS: remote fresh/repeat and official upgrade/backup/repeat; published runtime', expected)


if __name__ == '__main__':
    main()
