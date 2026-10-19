import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_andino_capabilities import NOT_VERIFIED_REASONS, case_prompt, validate_cases, validate_record, CAPABILITIES
from run_andino_capability_eval import (actor_command, opencode_permissions, resource_provenance,
                                        workspace_changes)

READ_ONLY_TEXT = 'Do not write files'
WRITABLE_TEXT = 'Creating, editing and running local files is allowed only inside the current working directory.'


def case(mode=None):
    value = dict(id='x', kind='behavior', prompt='User text', fixture='Fixture text',
                 expected='SECRET_EXPECTED', forbidden='SECRET_FORBIDDEN', capabilities=[])
    if mode:
        value['mode'] = mode
    return value


class PromptModeTest(unittest.TestCase):
    def test_read_only_prompt_never_allows_writes(self):
        prompt = case_prompt(case(), 'runtime', 'catalog')
        self.assertIn(READ_ONLY_TEXT, prompt)
        self.assertNotIn(WRITABLE_TEXT, prompt)

    def test_writable_prompt_drops_the_read_only_ban_but_keeps_outside_limits(self):
        prompt = case_prompt(case('isolated-writable'), 'runtime', 'catalog')
        self.assertIn(WRITABLE_TEXT, prompt)
        self.assertNotIn(READ_ONLY_TEXT, prompt)
        self.assertNotIn('read-only evaluation', prompt)
        for limit in ('outside it', 'commit', 'push', 'deploy', 'installed skills'):
            self.assertIn(limit, prompt)

    def test_both_modes_hide_the_oracle(self):
        for mode in ('read-only', 'isolated-writable'):
            prompt = case_prompt(case(mode), 'runtime', 'catalog')
            self.assertNotIn('SECRET_', prompt)
            self.assertTrue(prompt.endswith('User request:\nUser text'))

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            case_prompt(case('anything'), 'runtime', 'catalog')
        self.assertIn('case 0: invalid mode', validate_cases([case('anything')], CAPABILITIES))

    def test_fixture_files_must_stay_inside_the_workspace(self):
        bad = dict(case(), fixture_files={'../escape.txt': 'x'})
        self.assertIn('case 0: fixture_files must stay inside the workspace', validate_cases([bad], CAPABILITIES))


class ActorCommandTest(unittest.TestCase):
    def test_claude_writable_adds_only_file_edit_tools(self):
        command = actor_command('claude-code', Path('/w'), Path('/a'), False, mode='isolated-writable')
        self.assertEqual('Read,Glob,Grep,Skill,Write,Edit', command[command.index('--tools') + 1])
        self.assertIn('--restricted', command)
        self.assertNotIn('Bash', ' '.join(command))

    def test_claude_host_config_keeps_user_instructions(self):
        isolated = actor_command('claude-code', Path('/w'), Path('/a'), False)
        host = actor_command('claude-code', Path('/w'), Path('/a'), False, isolation='host-config')
        self.assertNotIn('--safe-mode', host)
        self.assertIn('--restricted', host)
        self.assertGreaterEqual(len(isolated), len(host))

    def test_codex_sandbox_follows_mode_and_excludes_temp_roots(self):
        read_only = actor_command('codex', Path('/w'), Path('/a'), False)
        self.assertEqual('read-only', read_only[read_only.index('--sandbox') + 1])
        writable = actor_command('codex', Path('/w'), Path('/a'), False, mode='isolated-writable')
        self.assertEqual('workspace-write', writable[writable.index('--sandbox') + 1])
        self.assertIn('sandbox_workspace_write.exclude_tmpdir_env_var=true', writable)
        self.assertIn('sandbox_workspace_write.network_access=false', writable)
        self.assertNotIn('--ignore-user-config', actor_command('codex', Path('/w'), Path('/a'), False, isolation='host-config'))

    def test_antigravity_mode_follows_case_mode(self):
        self.assertIn('plan', actor_command('antigravity-cli', Path('/w'), Path('/a'), False))
        self.assertIn('accept-edits', actor_command('antigravity-cli', Path('/w'), Path('/a'), False, mode='isolated-writable'))

    def test_opencode_permissions_deny_shell_and_outside_paths(self):
        for mode in ('read-only', 'isolated-writable'):
            rules = opencode_permissions(mode, False)['permission']
            self.assertEqual('deny', rules['*'])
            self.assertEqual('deny', rules['bash'])
            self.assertEqual('deny', rules['external_directory'])
            self.assertNotIn('ask', rules.values())
        self.assertEqual('deny', opencode_permissions('read-only', False)['permission']['edit'])
        self.assertEqual('allow', opencode_permissions('isolated-writable', False)['permission']['edit'])


class EvidenceTest(unittest.TestCase):
    def test_workspace_changes_exclude_evaluator_artifacts(self):
        before = {'note.txt': 'a', 'eval-plugin/x': 'p', 'gone.txt': 'g'}
        after = {'note.txt': 'b', 'eval-plugin/x': 'q', 'app.js': 'c', '.agents/skills/y/SKILL.md': 'd', 'answer.txt': 'e'}
        self.assertEqual(dict(created=['app.js'], modified=['note.txt'], deleted=['gone.txt']), workspace_changes(before, after))

    def test_provenance_separates_candidate_from_global_copies(self):
        root = Path('C:/Temp/andino-capability-eval-1')
        inside = {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': 'C:\\Temp\\andino-capability-eval-1\\work\\eval-plugin\\skills\\andino-workflow\\skills\\brainstorming\\GUIDE.md'}}
        relative = {'type': 'command_execution', 'command': 'Get-Content andino-workflow/SKILL.md'}
        outside = {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': 'C:\\Users\\me\\.claude\\skills\\andino-workflow\\SKILL.md'}}
        self.assertEqual('CANDIDATE_ONLY', resource_provenance([inside, relative], root)['status'])
        self.assertEqual('MIXED', resource_provenance([inside, outside], root)['status'])
        self.assertEqual('NONE_OBSERVED', resource_provenance([], root)['status'])
        global_skill = {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'andino-workflow'}}
        self.assertEqual('OUTSIDE_ONLY', resource_provenance([global_skill], root)['status'])

    def test_not_verified_reasons_do_not_extend_the_verdict_set(self):
        base = dict(case='x', scope='behavioral', host='codex', model='m', runtime_hash='0' * 64,
                    discovered=[], selected=[], invocations=[], fallback=[])
        for reason in NOT_VERIFIED_REASONS:
            self.assertEqual([], validate_record(dict(base, verdict='NOT_VERIFIED', reason=reason)))
        self.assertIn('record: invalid verdict', validate_record(dict(base, verdict='INCONCLUSIVE')))
        self.assertIn('record: reason applies only to NOT_VERIFIED', validate_record(dict(base, verdict='FAIL', reason='HOST_UNAVAILABLE')))
        self.assertIn('record: unknown NOT_VERIFIED reason', validate_record(dict(base, verdict='NOT_VERIFIED', reason='MAYBE')))


if __name__ == '__main__':
    unittest.main()
