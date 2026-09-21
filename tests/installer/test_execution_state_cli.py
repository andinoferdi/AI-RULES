import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.execution import Executor
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver
from ai_rules.state import create_snapshot, read_json, write_profile
from ai_rules.verification import doctor_from_plan


class ExecutionStateCliTests(unittest.TestCase):
    def test_dry_run_does_not_write_state(self):
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        plan = build_resolver(catalog, profiles, StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("codex",), profile_id="minimal")
        )
        with tempfile.TemporaryDirectory() as temp:
            state_dir = Path(temp) / "state"
            result = Executor(state_dir).execute(plan, dry_run=True)
            self.assertFalse(state_dir.exists())
            self.assertTrue(result.dry_run)

    def test_executor_requires_confirmation_for_mutation(self):
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        plan = build_resolver(catalog, profiles, StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("codex",), profile_id="minimal")
        )
        with tempfile.TemporaryDirectory() as temp:
            result = Executor(Path(temp)).execute(plan, dry_run=False, yes=False)
            self.assertEqual("BLOCKED", result.results[0].status)

    def test_profile_and_snapshot_are_secret_free(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            profile = root / "profile.json"
            snapshot = root / "snapshot.json"
            write_profile(profile, "minimal", ("codex",), ("andino-workflow",), "global")
            create_snapshot(profile, None, snapshot)
            data = read_json(snapshot)
            self.assertEqual("desired", data["mode"])
            self.assertNotIn("secret", json.dumps(data).lower())

    def test_doctor_reports_blocked_unmanaged_state(self):
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        plan = build_resolver(catalog, profiles, StaticCapabilityAdapter()).resolve(
            ResolveRequest(hosts=("codex",), profile_id="recommended")
        )
        report = doctor_from_plan(plan)
        statuses = {target.capability_id: target.status.value for target in report.targets}
        self.assertEqual("MANUAL_ACTION_REQUIRED", statuses["superpowers"])

    def test_cli_setup_dry_run_smoke(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "ai_rules",
                "setup",
                "--profile",
                "minimal",
                "--host",
                "codex",
                "--dry-run",
                "--non-interactive",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("INSTALL", completed.stdout)

    def test_cli_doctor_repair_preview_mentions_no_upgrade(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "ai_rules",
                "doctor",
                "--profile",
                "minimal",
                "--host",
                "codex",
                "--repair",
                "--dry-run",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("does not upgrade versions", completed.stdout)


if __name__ == "__main__":
    unittest.main()
