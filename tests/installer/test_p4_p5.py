from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_rules.cli import cmd_setup
from ai_rules.interactive import InteractiveSelection


class StateAndReleaseTests(unittest.TestCase):
    def test_interactive_confirmation_authorizes_execution(self):
        """Fails if accepting the interactive plan still reaches the executor as unconfirmed."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = type("Args", (), {
                "hosts": [], "capabilities": [], "profile": "minimal", "non_interactive": False,
                "scope": "project", "project_root": root / "project", "state_dir": root / "state",
                "dry_run": False, "yes": False,
            })()
            with patch(
                "ai_rules.cli.prompt_selection",
                return_value=InteractiveSelection(("codex",), "minimal", ()),
            ), patch("ai_rules.cli.prompt_confirmation", return_value=True):
                self.assertEqual(0, cmd_setup(args))
            self.assertTrue((root / "project" / ".agents" / "skills" / "andino-workflow" / "SKILL.md").exists())

    def test_setup_persists_verified_lock_after_successful_install(self):
        """Fails if desired profile is persisted without an exact verified lock target."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            command = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                "--yes", "--non-interactive",
            ]
            completed = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, completed.returncode, completed.stderr)
            lock = json.loads((root / "state" / "lock.json").read_text(encoding="utf-8"))
            self.assertEqual(1, lock["schema_version"])
            self.assertEqual("verified", lock["status"])
            self.assertEqual("codex", lock["targets"][0]["host"])
            self.assertEqual("project", lock["targets"][0]["scope"])

    def test_missing_managed_skill_directory_is_repair_not_install(self):
        """Fails if deleting a managed skill directory causes duplicate INSTALL instead of safe REPAIR."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            command = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                "--yes", "--non-interactive",
            ]
            first = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, first.returncode, first.stderr)
            skill_dir = root / "project" / ".agents" / "skills" / "andino-workflow"
            for child in skill_dir.iterdir():
                if child.is_file():
                    child.unlink()
                else:
                    import shutil
                    shutil.rmtree(child)
            skill_dir.rmdir()
            repaired = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(0, repaired.returncode, repaired.stderr)
            self.assertIn("APPLIED REPAIR", repaired.stdout)

    def test_update_yes_applies_update_and_writes_verified_lock(self):
        """Fails if update --yes remains a preview or records a lock before execution succeeds."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            setup = [
                sys.executable, "-m", "ai_rules", "setup", "--profile", "minimal", "--host", "codex",
                "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"),
                "--yes", "--non-interactive",
            ]
            self.assertEqual(0, subprocess.run(setup, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode)
            state_path = root / "state" / "managed-installations.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["installations"]["andino-workflow:codex:project"]["version"] = "release-manifest:andino-workflow@0000000"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            updated = subprocess.run(
                [sys.executable, "-m", "ai_rules", "update", "--profile", "minimal", "--host", "codex",
                 "--scope", "project", "--project-root", str(root / "project"), "--state-dir", str(root / "state"), "--yes"],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(0, updated.returncode, updated.stderr)
            self.assertIn("APPLIED UPDATE", updated.stdout)

    def test_restore_dry_run_reports_unknown_host_before_mutation(self):
        """Fails if restore previews a snapshot without surfacing unsupported host compatibility."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            snapshot = root / "snapshot.json"
            snapshot.write_text(
                json.dumps({"schema_version": 1, "mode": "desired", "profile": {
                    "profile": "minimal", "hosts": ["future-host"], "capabilities": ["andino-workflow"]
                }}),
                encoding="utf-8",
            )
            restored = subprocess.run(
                [sys.executable, "-m", "ai_rules", "restore", str(snapshot)],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(0, restored.returncode, restored.stderr)
            self.assertIn("incompatible host: future-host", restored.stdout)


if __name__ == "__main__":
    unittest.main()
