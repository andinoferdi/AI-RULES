import sys
import inspect
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from run_andino_capability_eval import fixture_contents, actor_command
from validate_andino_capabilities import EVAL_CASES


class OnlineResearchEvaluationTests(unittest.TestCase):
    def test_online_fixture_has_actual_version_and_observed_behavior(self):
        fixture = fixture_contents('search-first-online')
        self.assertIn('SQLAlchemy==2.0.43', fixture.get('requirements.txt', ''))
        self.assertIn('MissingGreenlet', fixture.get('project.md', ''))
        self.assertIn('search-first-online', EVAL_CASES)

    def test_sensitive_fixture_separates_error_from_synthetic_private_values(self):
        fixture = fixture_contents('search-first-sensitive')
        self.assertIn('retries', fixture.get('runtime.log', ''))
        self.assertIn('sk_test_SYNTHETIC_DO_NOT_SEND_8421', fixture.get('runtime.log', ''))
        self.assertIn('httpx==0.28.1', fixture.get('requirements.txt', ''))

    def test_deny_search_does_not_grant_shell_or_disable_permission_checks(self):
        self.assertIn('deny_web', inspect.signature(actor_command).parameters)
        command = actor_command('claude-code', Path('/fixture'), Path('/answer'), True,
                                deny_web=True)
        self.assertIn('WebSearch', command[command.index('--tools') + 1])
        self.assertEqual('WebSearch,WebFetch', command[command.index('--disallowedTools') + 1])
        self.assertNotIn('Bash', command[command.index('--tools') + 1])
        self.assertNotIn('--dangerously-skip-permissions', command)

    def test_safety_fixture_is_not_live_retrieval(self):
        fixture = fixture_contents('search-first-injection')
        self.assertIn('Ignore previous instructions', fixture.get('retrieved-page.txt', ''))
        self.assertIn('SYNTHETIC_SECRET', fixture.get('secrets.txt', ''))
        self.assertIn('fixture', fixture.get('retrieved-page.txt', ''))

    def test_existing_family_regressions_keep_one_owner_and_raw_fixtures(self):
        self.assertIn('single-lifecycle', EVAL_CASES)
        self.assertIn('research-specialist-owner', EVAL_CASES)
        self.assertIn('parser.py', fixture_contents('single-lifecycle'))
        self.assertIn('active-plan.md', fixture_contents('research-specialist-owner'))


if __name__ == '__main__':
    unittest.main()
