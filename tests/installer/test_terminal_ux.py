import unittest
import contextlib
from dataclasses import replace
import io
import os
from pathlib import Path
import tempfile
import threading
import subprocess
import sys
from unittest.mock import patch

from rich.console import Console
from ai_rules import cli
from ai_rules.domain.models import InstallationPlan
from ai_rules.domain.statuses import ReconciliationAction as Action
from ai_rules.execution import Executor
from ai_rules.execution.executor import copy_tree_atomic
from ai_rules.progress import SetupProgress, WorkEvent
from ai_rules.release import latest
from tests.installer import test_live_updates as fixtures

from ai_rules.catalog import load_catalog
from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver
from ai_rules.planning.renderer import render_plan


def example_plan():
    catalog = load_catalog()
    return build_resolver(catalog, load_profiles(catalog), StaticCapabilityAdapter()).resolve(
        ResolveRequest(hosts=tuple(catalog.hosts), profile_id="everything")
    )


class TerminalUXTests(unittest.TestCase):
    def test_default_plan_groups_actual_targets_by_host_without_operation_metadata(self):
        plan = example_plan()
        output = render_plan(plan)
        self.assertIn("INSTALLATION PLAN", output)
        self.assertIn(f"{len(plan.targets)} targets", output)
        self.assertIn("Codex", output)
        self.assertNotIn("source=", output)
        self.assertNotIn("backup=", output)

    def test_plan_widths_and_long_windows_paths(self):
        plan = example_plan()
        long_path = "C:\\Users\\Example\\" + "very-long-directory\\" * 15
        target = plan.targets[0]
        plan = replace(plan, targets=(replace(target, operations=(replace(target.operations[0], target=long_path),)), *plan.targets[1:]))
        for width in (60, 80, 120):
            output = render_plan(plan, width=width)
            self.assertTrue(all(len(line) <= width for line in output.splitlines()))
            self.assertNotIn("very-long-directory", output)
        self.assertIn(long_path, render_plan(plan, verbose=True))

    def test_actual_action_counts_per_host_including_other_actions(self):
        target = example_plan().targets[0]
        actions = [Action.INSTALL, Action.UPDATE, Action.NO_OP, Action.BLOCK, Action.MANUAL_ACTION, Action.REPAIR]
        plan = InstallationPlan(1, None, tuple(replace(target, action=a) for a in actions))
        output = render_plan(plan, width=120)
        for action in actions:
            self.assertIn(f"1 {action.value}", output)
        self.assertIn("6 targets", output)

    def test_processed_counts_targets_after_all_operations_and_separates_outcomes(self):
        base = example_plan().targets[0]
        multi = replace(base, operations=(base.operations[0], replace(base.operations[0], kind="register_skill_invocation")))
        current = replace(base, capability_id="current", action=Action.NO_OP, operations=())
        blocked = replace(base, capability_id="blocked", action=Action.BLOCK, operations=())
        failed = replace(base, capability_id="broken", operations=(replace(base.operations[0], capability_id="broken"),))
        skipped = replace(base, capability_id="empty", operations=())
        manual = replace(base, capability_id="manual", action=Action.MANUAL_ACTION, operations=())
        plan = InstallationPlan(1, None, (multi, current, blocked, failed, skipped, manual))
        stream = io.StringIO()
        progress = SetupProgress(console=Console(file=stream, force_terminal=False, width=120))
        events = []
        def report(event):
            events.append(event)
            progress(event)
        def fail():
            raise ValueError("fixture install failed")
        with tempfile.TemporaryDirectory() as temp, progress:
            result = Executor(Path(temp), reporter=report,
                              first_party_installers={("broken", "codex"): fail}).execute(plan, dry_run=False, yes=True)
        done = [e for e in events if e.kind == "target_done"]
        self.assertEqual([1, 2, 3, 4, 5, 6], [e.completed for e in done])
        self.assertEqual(["APPLIED", "CURRENT", "BLOCKED", "FAILED", "SKIPPED", "MANUAL_ACTION_REQUIRED"], [e.status for e in done])
        self.assertEqual(6, len(result.results))
        self.assertEqual(1, progress.actions["INSTALL"])
        self.assertIn("1 failed", stream.getvalue())
        self.assertIn("1 skipped", stream.getvalue())
        self.assertIn("1 manual", stream.getvalue())
        self.assertIn("fixture install failed", stream.getvalue())
        self.assertNotIn("100%", stream.getvalue())
        self.assertNotIn("\x1b", stream.getvalue())

    def test_live_refresh_continues_during_blocking_work_and_stops_on_cancel(self):
        stream = io.StringIO()
        with patch.dict(os.environ, {"TERM": "xterm", "CI": ""}):
            console = Console(file=stream, force_terminal=True, legacy_windows=False, width=80)
            progress = SetupProgress(console=console)
            with self.assertRaises(KeyboardInterrupt):
                with progress:
                    progress(WorkEvent("Fetching remote branches"))
                    before = len(stream.getvalue())
                    subprocess.run([sys.executable, "-c", "import time; time.sleep(0.4)"], check=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.assertGreater(len(stream.getvalue()), before)
                    raise KeyboardInterrupt
            stopped = len(stream.getvalue())
            threading.Event().wait(0.2)
            self.assertEqual(stopped, len(stream.getvalue()))
        self.assertIn("Cancelled", stream.getvalue())
        self.assertIn("elapsed", stream.getvalue())
        self.assertNotIn("%", stream.getvalue())
        self.assertIn("\x1b[?25h", stream.getvalue())

    def test_plain_fallback_overrides_forced_color_and_no_progress(self):
        for env in ({"TERM": "dumb"}, {"CI": "true"}, {"NO_COLOR": "1"}):
            with patch.dict(os.environ, {**env, "FORCE_COLOR": "1"}):
                stream = io.StringIO()
                with SetupProgress(console=Console(file=stream, force_terminal=False), enabled=False) as progress:
                    progress(WorkEvent("Checking configuration"))
                self.assertNotIn("\x1b", stream.getvalue())

    def test_redirected_default_presenter_ignores_force_color(self):
        with patch.dict(os.environ, {"TERM": "xterm", "FORCE_COLOR": "1"}):
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream), SetupProgress() as progress:
                self.assertFalse(progress.dynamic)
                progress(WorkEvent("Checking sources"))
            self.assertNotIn("\x1b", stream.getvalue())

    def test_no_color_keeps_interactive_activity_without_color_codes(self):
        import re
        stream = io.StringIO()
        with patch.dict(os.environ, {"TERM": "xterm", "CI": "", "NO_COLOR": ""}):
            console = Console(file=stream, force_terminal=True, legacy_windows=False)
            with SetupProgress(console=console) as progress:
                self.assertTrue(progress.dynamic)
                progress(WorkEvent("Checking sources"))
        self.assertIsNone(re.search(r"\x1b\[(?:3[0-9]|9[0-7])(?:;|m)", stream.getvalue()))

    def test_rollback_and_interrupt_restore_previous_tree(self):
        for exception in (RuntimeError("verification failed"), KeyboardInterrupt()):
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                source, target = root / "source", root / "target"
                source.mkdir()
                target.mkdir()
                (source / "SKILL.md").write_text("new")
                (target / "SKILL.md").write_text("old")
                events = []
                def verify(path):
                    if path == target:
                        raise exception
                    return True
                with self.assertRaises(type(exception)):
                    copy_tree_atomic(source, target, root / "backups", verify=verify, reporter=events.append)
                self.assertEqual("old", (target / "SKILL.md").read_text())
                self.assertIn("Rolling back replacement", [e.phase for e in events])
                self.assertFalse(list(root.glob(".*.staged-*")))

    def test_final_verification_failure_removes_success_count(self):
        stream = io.StringIO()
        with SetupProgress(console=Console(file=stream, force_terminal=False)) as progress:
            progress(WorkEvent("Apply", kind="execution", total=1))
            progress(WorkEvent("done", kind="target_done", host="codex", capability="focus", action="INSTALL", status="APPLIED"))
            progress(WorkEvent("Verify failed", kind="verification_failed", host="codex", capability="focus", detail="missing artifact"))
        self.assertIn("0 installed", stream.getvalue())
        self.assertIn("1 failed", stream.getvalue())

    def test_questionary_real_keyboard_selection_and_confirmation(self):
        from prompt_toolkit.input import create_pipe_input
        from prompt_toolkit.output import DummyOutput
        from prompt_toolkit.application import create_app_session
        from ai_rules.interactive import prompt_selection, prompt_confirmation
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        with create_pipe_input() as pipe, create_app_session(input=pipe, output=DummyOutput()):
            pipe.send_text(" \r\r")
            selected = prompt_selection(catalog.hosts, profiles.profiles, catalog.capabilities)
            self.assertEqual(("codex",), selected.hosts)
            self.assertEqual("minimal", selected.profile_id)
            pipe.send_text("n")
            self.assertFalse(prompt_confirmation())
            pipe.send_text("y")
            self.assertTrue(prompt_confirmation())

    def test_observer_exception_cannot_break_installation(self):
        def broken_observer(event):
            raise RuntimeError("display unavailable")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("new")
            copy_tree_atomic(source, root / "target", reporter=broken_observer)
            self.assertEqual("new", (root / "target/SKILL.md").read_text())


class SourceProgressTests(unittest.TestCase):
    setUp = fixtures.LiveUpdateTests.setUp
    git = fixtures.LiveUpdateTests.git
    commit = fixtures.LiveUpdateTests.commit
    run_cli = fixtures.LiveUpdateTests.run_cli

    def test_event_precedes_real_local_fetch_and_bundle_preparation(self):
        events = []
        original_git = latest.git
        def observed_git(root, *args):
            if args[0] == "fetch":
                self.assertEqual("Fetching remote branches", events[-1].phase)
                self.assertEqual(1, events[-1].total)
                self.assertEqual(0, events[-1].completed)
            return original_git(root, *args)
        with patch.object(latest, "git", side_effect=observed_git):
            sources = latest.LatestSources(self.catalog, ["focus"], reporter=events.append)
        self.addCleanup(sources.close)
        self.assertEqual("Checking source configuration", events[0].phase)
        self.assertIn("Preparing source bundle", [e.phase for e in events])

    def test_dry_run_is_plain_and_does_not_create_project_or_state(self):
        code, output = self.run_cli("--dry-run")
        self.assertEqual(0, code, output)
        self.assertFalse(self.project.exists())
        self.assertFalse(self.state.exists())
        self.assertNotIn("\x1b", output)
        self.assertIn("INSTALLATION PLAN", output)
        self.assertLess(output.index("Checking sources"), output.index("Fetching remote"))

    def test_verbose_and_no_progress_flags_expose_real_operation_details(self):
        code, output = self.run_cli("--dry-run", "--verbose", "--no-progress")
        self.assertEqual(0, code, output)
        self.assertIn("source=", output)
        self.assertIn("target=", output)
        self.assertIn("backup=", output)
        self.assertNotIn("\x1b", output)
        self.assertFalse(self.project.exists())

    def test_setup_selection_and_declined_confirmation_preserve_files(self):
        from ai_rules.interactive import InteractiveSelection
        with patch.object(cli, "prompt_selection", return_value=InteractiveSelection(("codex",), "minimal", ())), \
             patch.object(cli, "prompt_confirmation", return_value=False) as confirm, \
             contextlib.redirect_stdout(io.StringIO()):
            code = cli.main(["setup", "--scope", "project", "--project-root", str(self.project), "--state-dir", str(self.state)])
        self.assertEqual(0, code)
        confirm.assert_called_once()
        self.assertFalse(self.project.exists())
        self.assertFalse(self.state.exists())

    def test_interrupt_during_fetch_cleans_source_workspace_and_returns_130(self):
        original_git = latest.git
        roots = []
        def interrupt(root, *args):
            roots.append(root.parent)
            if args[0] == "fetch":
                raise KeyboardInterrupt
            return original_git(root, *args)
        with patch.object(latest, "git", side_effect=interrupt):
            code, output = self.run_cli()
        self.assertEqual(130, code, output)
        self.assertIn("Cancelled", output)
        self.assertIn("Fetching remote branches", output)
        self.assertTrue(all(not root.exists() for root in roots))


if __name__ == "__main__":
    unittest.main()
