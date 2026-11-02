"""Public helper regression tests using unpublished local package fixtures."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ai_rules import cli
from ai_rules.catalog import load_catalog
from ai_rules.domain.statuses import Scope
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.hosts.invocation import invocation_paths
from ai_rules.release.bundles import install_first_party_bundle
from ai_rules.release.family import FamilyPlan, recover, install as install_family, remove as remove_family


def bundle(root, members, retired=(), protocol=1):
    root.mkdir(parents=True, exist_ok=True)
    (root / 'SKILL.md').write_text('---\nname: andino-workflow\n---\nWorkflow\n')
    (root / 'references').mkdir(exist_ok=True)
    (root / 'references/portfolio.json').write_text(json.dumps({
        'schema_version': 1, 'installer_protocol': protocol,
        'members': list(members), 'retired': list(retired), 'resources': []}))
    for name in members:
        path = root / 'skills' / name
        path.mkdir(parents=True)
        (path / 'SKILL.md').write_text(f'---\nname: andino-{name}\n---\n{name}\n')
    return root


class PortfolioTransactionTests(unittest.TestCase):
    def test_upgrade_retires_only_owned_explicit_member(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = bundle(root / 'old', ['planning', 'delivery'])
            new = bundle(root / 'new', ['planning', 'git-skills'], ['delivery'])
            skills, state = root / 'skills', root / 'state'
            install_first_party_bundle(old, skills, 'andino-workflow', state)
            unrelated = skills / 'andino-user-owned'
            unrelated.mkdir()
            (unrelated / 'SKILL.md').write_bytes(b'user bytes')
            install_first_party_bundle(new, skills, 'andino-workflow', state)
            self.assertFalse((skills / 'andino-delivery').exists())
            self.assertTrue((skills / 'andino-git-skills/SKILL.md').is_file())
            self.assertEqual(b'user bytes', (unrelated / 'SKILL.md').read_bytes())
            install_first_party_bundle(new, skills, 'andino-workflow', state)
            self.assertFalse((skills / 'andino-delivery').exists())

    def test_modified_retired_member_blocks_before_parent_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = bundle(root / 'old', ['delivery'])
            new = bundle(root / 'new', ['git-skills'], ['delivery'])
            skills, state = root / 'skills', root / 'state'
            install_first_party_bundle(old, skills, 'andino-workflow', state)
            (skills / 'andino-delivery/user.txt').write_bytes(b'preserve me')
            before = (skills / 'andino-workflow/references/portfolio.json').read_bytes()
            with self.assertRaisesRegex(ValueError, 'modified|conflict|preserved'):
                install_first_party_bundle(new, skills, 'andino-workflow', state)
            self.assertEqual(before, (skills / 'andino-workflow/references/portfolio.json').read_bytes())
            self.assertEqual(b'preserve me', (skills / 'andino-delivery/user.txt').read_bytes())
            self.assertFalse((skills / 'andino-git-skills').exists())

    def test_unsupported_protocol_rejected_before_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = bundle(root / 'source', ['planning'], protocol=99)
            with self.assertRaisesRegex(ValueError, 'protocol'):
                install_first_party_bundle(source, root / 'skills', 'andino-workflow', root / 'state')
            self.assertFalse((root / 'skills/andino-workflow').exists())

    def test_unrelated_andino_sibling_never_glob_deleted_on_upgrade_or_removal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = bundle(root / 'old', ['planning'])
            new = bundle(root / 'new', ['planning', 'git-skills'], ['delivery'])
            skills, state = root / 'skills', root / 'state'
            install_first_party_bundle(old, skills, 'andino-workflow', state)
            unrelated = skills / 'andino-custom-tool'
            unrelated.mkdir()
            (unrelated / 'SKILL.md').write_text('---\nname: andino-custom-tool\n---\ncustom\n')
            (unrelated / 'data.txt').write_text('important user data\n')
            install_first_party_bundle(new, skills, 'andino-workflow', state)
            self.assertTrue(unrelated.exists())
            self.assertEqual('important user data\n', (unrelated / 'data.txt').read_text())
            remove_family(skills, state)
            self.assertFalse((skills / 'andino-workflow').exists())
            self.assertFalse((skills / 'andino-planning').exists())
            self.assertFalse((skills / 'andino-git-skills').exists())
            self.assertTrue(unrelated.exists())
            self.assertEqual('important user data\n', (unrelated / 'data.txt').read_text())

    def test_retired_member_invocation_is_retired_and_user_command_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / 'project'
            project.mkdir()
            state = root / 'state'
            catalog = load_catalog()
            adapter = build_host_adapters(catalog.hosts)['opencode']
            skills = project / '.opencode/skills'
            old = bundle(root / 'old', ['planning', 'delivery'])
            new = bundle(root / 'new', ['planning'], ['delivery'])

            plan_old = FamilyPlan(old, skills, state, adapter=adapter, scope=Scope.PROJECT, project_root=project)
            plan_old.apply()
            cmd_delivery = project / '.opencode/commands/andino-delivery.md'
            cmd_user = project / '.opencode/commands/user-note.md'
            cmd_user.write_text('user command note\n')
            self.assertTrue(cmd_delivery.is_file())
            self.assertTrue((skills / 'andino-delivery').exists())

            plan_new = FamilyPlan(new, skills, state, adapter=adapter, scope=Scope.PROJECT, project_root=project)
            plan_new.apply()
            self.assertFalse((skills / 'andino-delivery').exists())
            self.assertFalse(cmd_delivery.exists())
            self.assertEqual('user command note\n', cmd_user.read_text())

    def test_user_command_conflict_blocks_before_family_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / 'project'
            project.mkdir()
            state = root / 'state'
            catalog = load_catalog()
            adapter = build_host_adapters(catalog.hosts)['opencode']
            skills = project / '.opencode/skills'
            old = bundle(root / 'old', ['delivery'])
            new = bundle(root / 'new', ['planning'], ['delivery'])

            FamilyPlan(old, skills, state, adapter=adapter, scope=Scope.PROJECT, project_root=project).apply()
            cmd_delivery = project / '.opencode/commands/andino-delivery.md'
            cmd_delivery.write_text('modified user command\n')

            with self.assertRaisesRegex(ValueError, 'modified|conflict|preserved'):
                FamilyPlan(new, skills, state, adapter=adapter, scope=Scope.PROJECT, project_root=project).apply()

            self.assertTrue((skills / 'andino-delivery').exists())
            self.assertFalse((skills / 'andino-planning').exists())
            self.assertEqual('modified user command\n', cmd_delivery.read_text())

    def test_transaction_rollback_restores_prior_state_on_fault(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skills, state = root / 'skills', root / 'state'
            old = bundle(root / 'old', ['planning', 'delivery'])
            new = bundle(root / 'new', ['planning', 'git-skills'], ['delivery'])
            install_first_party_bundle(old, skills, 'andino-workflow', state)
            before_planning = (skills / 'andino-planning/SKILL.md').read_bytes()
            before_delivery = (skills / 'andino-delivery/SKILL.md').read_bytes()

            plan = FamilyPlan(new, skills, state)
            def inject_fault(index, target):
                if 'git-skills' in str(target):
                    raise RuntimeError('disk write failed mid-transaction')

            with self.assertRaisesRegex(RuntimeError, 'disk write failed'):
                plan.apply(fault=inject_fault)

            self.assertTrue((skills / 'andino-delivery').exists())
            self.assertEqual(before_delivery, (skills / 'andino-delivery/SKILL.md').read_bytes())
            self.assertEqual(before_planning, (skills / 'andino-planning/SKILL.md').read_bytes())
            self.assertFalse((skills / 'andino-git-skills').exists())

    def test_crash_recovery_from_unfinished_journal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skills, state = root / 'skills', root / 'state'
            old = bundle(root / 'old', ['planning', 'delivery'])
            new = bundle(root / 'new', ['planning', 'git-skills'], ['delivery'])
            install_first_party_bundle(old, skills, 'andino-workflow', state)
            before_delivery = (skills / 'andino-delivery/SKILL.md').read_bytes()

            plan = FamilyPlan(new, skills, state)
            # Simulate a crash right after a mutation by simulating os._exit or unhandled interruption
            def simulate_crash(index, target):
                # We simulate writing pending journal and partially mutating target
                pass
            # Create a pending journal simulating an interrupted process
            work = state / 'families' / 'crash-test'
            work.mkdir(parents=True)
            delivery_target = skills / 'andino-delivery'
            delivery_backup = work / 'backup-delivery'
            import shutil
            shutil.copytree(delivery_target, delivery_backup)
            # Simulate target was deleted during transaction before crash
            shutil.rmtree(delivery_target)
            from ai_rules.release.family import fingerprint
            journal = {
                'schema_version': 1,
                'status': 'pending',
                'roots': [str(skills)],
                'changes': [
                    {
                        'target': str(delivery_target),
                        'stage': str(work / 'stage'),
                        'backup': str(delivery_backup),
                        'before': fingerprint(delivery_backup),
                        'after': None,
                    }
                ]
            }
            (work / 'journal.json').write_text(json.dumps(journal, indent=2), encoding='utf-8')

            journal_file = work / 'journal.json'
            journal_data = json.loads(journal_file.read_text(encoding='utf-8'))
            self.assertEqual(journal_data.get('status'), 'pending')
            self.assertFalse(delivery_target.exists())

            recover(state)
            self.assertTrue(delivery_target.exists())
            self.assertEqual(before_delivery, (delivery_target / 'SKILL.md').read_bytes())
            reloaded_journal = json.loads(journal_file.read_text(encoding='utf-8'))
            self.assertEqual('rolled-back', reloaded_journal.get('status'))

    def test_staging_and_backups_remain_outside_discovery_roots(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skills, state = root / 'skills', root / 'state'
            b = bundle(root / 'bundle', ['planning'])
            install_first_party_bundle(b, skills, 'andino-workflow', state)
            # Verify no .staged or .previous or backup directory in skills root
            for item in skills.iterdir():
                self.assertFalse(item.name.startswith('.andino-workflow.staged-'))
                self.assertFalse(item.name.startswith('.andino-workflow.previous-'))
                self.assertFalse('backup' in item.name.lower())
            with self.assertRaisesRegex(ValueError, 'discovery roots'):
                FamilyPlan(b, skills, skills / 'forbidden-state')

    def test_latest_setup_retires_member_and_blocks_on_modified_retired_member(self):
        import shutil
        import subprocess
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = root / 'remote'
            remote.mkdir()
            subprocess.run(['git', 'init', '-b', 'andino-workflow'], cwd=remote, check=True, stdout=subprocess.PIPE)
            subprocess.run(['git', 'config', 'user.name', 'Fixture'], cwd=remote, check=True)
            subprocess.run(['git', 'config', 'user.email', 'fixture@example.invalid'], cwd=remote, check=True)

            # Old commit has delivery and planning
            (remote / 'SKILL.md').write_text('---\nname: andino-workflow\ndescription: Test\n---\nWorkflow\n', encoding='utf-8')
            (remote / 'README.md').write_text('Test\n', encoding='utf-8')
            (remote / 'references').mkdir()
            (remote / 'references/portfolio.json').write_text(json.dumps({
                'schema_version': 1, 'installer_protocol': 1,
                'members': ['planning', 'delivery'], 'retired': [], 'resources': []
            }), encoding='utf-8')
            (remote / 'skills/planning').mkdir(parents=True)
            (remote / 'skills/planning/SKILL.md').write_text('---\nname: andino-planning\n---\nPlanning\n', encoding='utf-8')
            (remote / 'skills/delivery').mkdir(parents=True)
            (remote / 'skills/delivery/SKILL.md').write_text('---\nname: andino-delivery\n---\nDelivery\n', encoding='utf-8')
            subprocess.run(['git', 'add', '.'], cwd=remote, check=True)
            subprocess.run(['git', 'commit', '-m', 'initial'], cwd=remote, check=True)

            project = root / 'project'
            project.mkdir()
            state = root / 'state'
            catalog = load_catalog()
            catalog.require_capability('andino-workflow').source['repository'] = str(remote)

            with patch.object(cli, 'load_catalog', return_value=catalog):
                result = cli.main([
                    'setup', '--host', 'codex', '--scope', 'project',
                    '--project-root', str(project), '--state-dir', str(state),
                    '--capability', 'andino-workflow', '--source', 'latest',
                    '--yes', '--non-interactive'
                ])
                self.assertEqual(0, result)
                skills_root = project / '.agents/skills'
                self.assertTrue((skills_root / 'andino-delivery/SKILL.md').is_file())
                self.assertTrue((skills_root / 'andino-planning/SKILL.md').is_file())

                # New commit retires delivery and adds git-skills
                shutil.rmtree(remote / 'skills/delivery')
                (remote / 'skills/git-skills').mkdir(parents=True)
                (remote / 'skills/git-skills/SKILL.md').write_text('---\nname: andino-git-skills\n---\nGit\n', encoding='utf-8')
                (remote / 'references/portfolio.json').write_text(json.dumps({
                    'schema_version': 1, 'installer_protocol': 1,
                    'members': ['planning', 'git-skills'], 'retired': ['delivery'], 'resources': []
                }), encoding='utf-8')
                subprocess.run(['git', 'add', '.'], cwd=remote, check=True)
                subprocess.run(['git', 'commit', '-m', 'retire delivery add git-skills'], cwd=remote, check=True)

                # Upgrade via latest
                result = cli.main([
                    'setup', '--host', 'codex', '--scope', 'project',
                    '--project-root', str(project), '--state-dir', str(state),
                    '--capability', 'andino-workflow', '--source', 'latest',
                    '--yes', '--non-interactive'
                ])
                self.assertEqual(0, result)
                self.assertFalse((skills_root / 'andino-delivery').exists())
                self.assertTrue((skills_root / 'andino-git-skills/SKILL.md').is_file())

                # Now test that if user had modified the retired member, it blocks
                # Re-create delivery with user edit
                (skills_root / 'andino-delivery').mkdir()
                (skills_root / 'andino-delivery/SKILL.md').write_text('user custom delivery\n', encoding='utf-8')
                result = cli.main([
                    'setup', '--host', 'codex', '--scope', 'project',
                    '--project-root', str(project), '--state-dir', str(state),
                    '--capability', 'andino-workflow', '--source', 'latest',
                    '--yes', '--non-interactive'
                ])
                self.assertNotEqual(0, result)
                self.assertEqual('user custom delivery\n', (skills_root / 'andino-delivery/SKILL.md').read_text())
