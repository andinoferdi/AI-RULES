"""Screen mode: the short, animated setup screen shown in an interactive terminal."""
import contextlib
import io
import os
import re
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock, patch

from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from rich.console import Console

from ai_rules import banner, cli
from ai_rules.agent_defaults import DefaultsResult
from ai_rules.banner import BannerInfo, mark_rows
from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.domain.models import InstallationPlan
from ai_rules.domain.statuses import ReconciliationAction as Action
from ai_rules.interactive import prompt_confirmation, prompt_selection
from ai_rules.events import WorkEvent
from ai_rules.planning.renderer import plan_summary
from ai_rules.profiles import load_profiles
from ai_rules.progress import SetupProgress
from ai_rules.resolver import ResolveRequest, build_resolver
from ai_rules.screen import UNICODE, Problem, Result, Screen, defaults_summary, detect_screen, fit_names


ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def plain(text):
    return ANSI.sub("", text)


class FakeTty(io.StringIO):
    def __init__(self, encoding="utf-8"):
        super().__init__()
        self._encoding = encoding

    def isatty(self):
        return True

    @property
    def encoding(self):
        return self._encoding


def make_screen(width=80, color=True, glyphs=UNICODE, sleep=lambda seconds: None):
    console = Console(file=FakeTty(), force_terminal=True, width=width, legacy_windows=False,
                      color_system="truecolor" if color else None, no_color=not color, highlight=False)
    return Screen(console, glyphs=glyphs, color=color, sleep=sleep)


def render_text(renderable, width):
    console = Console(file=io.StringIO(), width=width, record=True, force_terminal=True, legacy_windows=False)
    console.print(renderable)
    return console.export_text()


INFO = BannerInfo("0.1.0", "setup", ("Codex", "Claude Code"), (), "~\\Projects\\demo")


def example_plan():
    """Everything on every host from a clean machine: 40 targets to install."""
    catalog = load_catalog()
    return build_resolver(catalog, load_profiles(catalog), StaticCapabilityAdapter()).resolve(
        ResolveRequest(hosts=tuple(catalog.hosts), profile_id="everything"))


class DetectScreenTests(unittest.TestCase):
    def detect(self, environ=None, stream=None, **flags):
        return detect_screen(interactive=flags.get("interactive", True), progress=flags.get("progress", True),
                             stream=stream or FakeTty(),
                             environ=environ if environ is not None else {"TERM": "xterm-256color"})

    def test_plain_conditions_return_no_screen(self):
        self.assertIsNone(self.detect(interactive=False))
        self.assertIsNone(self.detect(progress=False))
        self.assertIsNone(self.detect(stream=io.StringIO()))
        for environ in ({"CI": "true"}, {"TERM": "dumb"}, {"TERM": "unknown"}):
            self.assertIsNone(self.detect(environ=environ))

    def test_terminal_gets_a_screen_with_colour_and_unicode(self):
        screen = self.detect()
        self.assertIsNotNone(screen)
        self.assertTrue(screen.color)
        self.assertEqual("◆", screen.glyphs.active)

    def test_no_color_and_cp1252_keep_screen_mode_plainly(self):
        screen = self.detect(environ={"TERM": "xterm", "NO_COLOR": "1"}, stream=FakeTty("cp1252"))
        self.assertIsNotNone(screen)
        self.assertFalse(screen.color)
        self.assertEqual("*", screen.glyphs.active)


class MarkTests(unittest.TestCase):
    def test_full_mark_is_unchanged(self):
        self.assertEqual("▄█▀ ▀  ▀█▄", mark_rows(color=False)[3])

    def test_mark_rows_build_from_the_bottom(self):
        self.assertEqual(["          "] * 3 + ["▄█▀    ▀█▄"], mark_rows(color=False, built=2, lit=0))

    def test_unlit_check_has_no_kunyit(self):
        self.assertNotIn("245;165;36", "".join(mark_rows(color=True, lit=0)))
        self.assertIn("154;164;178", "".join(mark_rows(color=True, lit=0)))
        self.assertIn("245;165;36", "".join(mark_rows(color=True, lit=5)))


class IntroTests(unittest.TestCase):
    def test_intro_builds_the_mark_within_the_cap(self):
        waits = []
        screen = make_screen(width=100, sleep=waits.append)
        screen.intro(INFO)
        out = screen.console.file.getvalue()
        self.assertEqual(8, len(waits))
        self.assertLessEqual(sum(waits), 0.6)
        self.assertIn("Andino Skills", plain(out))
        self.assertNotIn("245;165;36", out)

    def test_banner_hands_the_intro_to_the_screen(self):
        screen = Mock()
        with patch.object(banner, "collect_banner_info", return_value=INFO):
            banner.print_setup_banner(screen=screen)
        screen.intro.assert_called_once_with(INFO)


class AnswerTests(unittest.TestCase):
    NAMES = ["Codex", "Claude Code", "OpenCode", "Antigravity CLI", "Antigravity IDE"]

    def test_fit_names_keeps_whole_names_and_counts_the_rest(self):
        self.assertEqual("Codex, Claude Code, OpenCode +2", fit_names(self.NAMES, 40))
        self.assertEqual(", ".join(self.NAMES), fit_names(self.NAMES, 80))
        self.assertEqual("Codex +4", fit_names(self.NAMES, 8))
        self.assertEqual("5 selected", fit_names(self.NAMES, 7))

    def test_rewrite_moves_up_erases_and_aligns(self):
        screen = make_screen()
        screen.rewrite_answer("Agents", "Codex")
        out = screen.console.file.getvalue()
        self.assertTrue(out.startswith("\x1b[1A\x1b[2K"), repr(out[:20]))
        self.assertIn("◇ Agents    Codex", plain(out))

    def test_prompts_fold_answers_in_screen_mode(self):
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        screen = make_screen()
        with create_pipe_input() as pipe, create_app_session(input=pipe, output=DummyOutput()):
            pipe.send_text(" \r\r")
            selected = prompt_selection(catalog.hosts, profiles.profiles, catalog.capabilities, screen=screen)
            pipe.send_text("y")
            self.assertTrue(prompt_confirmation(screen=screen))
        self.assertEqual(("codex",), selected.hosts)
        text = plain(screen.console.file.getvalue())
        self.assertIn("◇ Agents    Codex", text)
        self.assertIn("◇ Profile   Minimal", text)
        self.assertIn("◇ Apply     yes", text)

    def test_flags_print_answer_lines_and_a_short_source(self):
        screen = make_screen(width=100)
        with tempfile.TemporaryDirectory() as temp, patch.object(cli, "detect_screen", return_value=screen), \
                patch.object(cli, "print_setup_banner"), contextlib.redirect_stdout(io.StringIO()):
            code = cli.main(["setup", "--host", "codex", "--profile", "minimal", "--scope", "project",
                             "--project-root", str(Path(temp) / "project"), "--state-dir", str(Path(temp) / "state"),
                             "--source", "local", "--dry-run"])
        text = plain(screen.console.file.getvalue())
        self.assertEqual(0, code)
        self.assertIn("◇ Agents    Codex", text)
        self.assertIn("◇ Profile   Minimal", text)
        self.assertIn(f"Skill source: local folder {banner._display_path(Path.cwd() / 'skills')}", text)

    def test_long_project_paths_stay_on_their_answer_line(self):
        screen = make_screen(width=80)
        with tempfile.TemporaryDirectory() as temp, patch.object(cli, "detect_screen", return_value=screen), \
                patch.object(cli, "print_setup_banner"), contextlib.redirect_stdout(io.StringIO()):
            deep = Path(temp) / ("very-long-folder-name-" * 5) / "project"
            cli.main(["setup", "--host", "codex", "--profile", "minimal", "--scope", "project",
                      "--project-root", str(deep), "--state-dir", str(Path(temp) / "state"),
                      "--source", "local", "--dry-run"])
        scope = next(line for line in plain(screen.console.file.getvalue()).splitlines() if line.startswith("◇ Scope"))
        self.assertTrue(scope.endswith(f"{os.sep}project"), scope)
        self.assertLessEqual(len(scope), 80)


class PlanBlockTests(unittest.TestCase):
    def test_plan_summary_counts_every_action_in_a_fixed_order(self):
        target = example_plan().targets[0]
        actions = [Action.INSTALL, Action.UPDATE, Action.NO_OP, Action.BLOCK, Action.MANUAL_ACTION, Action.REPAIR]
        plan = InstallationPlan(1, None, tuple(replace(target, action=a) for a in actions))
        self.assertEqual("1 to install · 1 to update · 1 to repair · 1 current · 1 manual · 1 blocked",
                         plan_summary(plan))
        self.assertEqual("nothing to do", plan_summary(InstallationPlan(1, None, ())))

    def test_screen_plan_is_one_line_and_fits(self):
        for width in (40, 59, 60, 80, 120):
            screen = make_screen(width=width)
            screen.plan(example_plan(), load_catalog())
            lines = [line for line in plain(screen.console.file.getvalue()).splitlines() if line.strip()]
            self.assertTrue(lines)
            self.assertEqual("◆ Plan      40 to install", lines[0])
            self.assertTrue(all(len(line) <= width for line in lines), lines)
            self.assertNotIn("source=", "\n".join(lines))

    def test_defaults_summary_counts_and_lists_conflicts(self):
        home = Path.home()
        results = (DefaultsResult(home / ".codex/AGENTS.md", ("codex",), "CURRENT"),
                   DefaultsResult(home / ".claude/CLAUDE.md", ("claude-code",), "UPDATE"),
                   DefaultsResult(home / ".gemini/AGENTS.md", ("antigravity-cli",), "CONFLICT", "edited locally; preserved"))
        summary, issues = defaults_summary(results)
        self.assertEqual("1 to update · 1 current · 1 conflict", summary)
        self.assertEqual([("manual", f"~{os.sep}.gemini{os.sep}AGENTS.md", "edited locally; preserved")], issues)

    def run_screen(self, *argv, command="setup"):
        screen = make_screen(width=100)
        with tempfile.TemporaryDirectory() as temp, patch.object(cli, "detect_screen", return_value=screen), \
                patch.object(cli, "print_setup_banner"), contextlib.redirect_stdout(io.StringIO()) as stdout:
            code = cli.main([command, "--host", "codex", "--scope", "project",
                             "--project-root", str(Path(temp) / "project"), "--state-dir", str(Path(temp) / "state"),
                             "--source", "local", "--dry-run", *argv])
        return code, plain(screen.console.file.getvalue()), stdout.getvalue()

    def test_dry_run_ends_after_the_plan(self):
        code, text, stdout = self.run_screen("--profile", "minimal")
        self.assertEqual(0, code)
        self.assertIn("◆ Plan      3 to install", text)
        self.assertIn("Dry run · nothing changed", text)
        self.assertNotIn("INSTALLATION PLAN", text + stdout)

    def test_verbose_screen_adds_todays_details(self):
        code, text, stdout = self.run_screen("--profile", "minimal", "--verbose")
        both = text + stdout
        self.assertEqual(0, code)
        self.assertIn("◆ Plan      3 to install", both)
        for detail in ("INSTALLATION PLAN", "source=", "Preflight"):
            self.assertIn(detail, both)

    def test_update_uses_the_plan_line_in_screen_mode(self):
        code, text, stdout = self.run_screen(command="update")
        both = text + stdout
        self.assertIn("Andino Skills update preview", both)
        self.assertIn("◆ Plan", both)
        self.assertNotIn("INSTALLATION PLAN", both)


class ProgressScreenTests(unittest.TestCase):
    def run_events(self, width, *statuses):
        progress = SetupProgress(screen=make_screen(width=width))
        progress.expect([("codex", "Codex", 2), ("claude-code", "Claude Code", 1)])
        progress(WorkEvent("Apply", kind="execution", total=3))
        for capability, status in zip(("focus", "search-first"), statuses):
            progress(WorkEvent("done", kind="target_done", host="codex", capability=capability,
                               action="UPDATE", status=status))
        return progress

    def test_bars_fill_per_agent_and_mark_done_agents(self):
        text = render_text(self.run_events(80, "APPLIED", "CURRENT").render(), 80)
        self.assertRegex(text, r"Codex\s+━+\s+2/2\s+✓")
        self.assertRegex(text, r"Claude Code\s+─+\s+0/1")
        self.assertNotIn("%", text)

    def test_narrow_terminal_drops_the_bar(self):
        text = render_text(self.run_events(59, "APPLIED", "CURRENT").render(), 59)
        self.assertNotIn("━", text)
        self.assertIn("2/2", text)

    def test_failed_target_marks_its_agent(self):
        text = render_text(self.run_events(80, "FAILED", "CURRENT").render(), 80)
        self.assertRegex(text, r"Codex\s+━+\s+2/2\s+✗")
        self.assertNotIn("✓", text)

    def test_status_line_shows_phase_and_work_time(self):
        progress = SetupProgress(screen=make_screen(width=80))
        progress(WorkEvent("Fetching remote branches"))
        self.assertRegex(render_text(progress.render(), 80), r"Fetching remote branches · \d+\.\ds")

    def test_status_line_names_the_last_target_between_targets(self):
        progress = SetupProgress(screen=make_screen(width=80))
        progress.expect([("codex", "Codex", 2)])
        progress(WorkEvent("Apply", kind="execution", total=2))
        progress(WorkEvent("Processing target", kind="target_start", host="codex", capability="focus", action="UPDATE"))
        progress(WorkEvent("Target finished", kind="target_done", host="codex", capability="focus",
                           action="UPDATE", status="APPLIED"))
        text = render_text(progress.render(), 80)
        self.assertIn("Updating Codex · focus", text)
        self.assertNotIn("Target finished", text)

    def test_elapsed_counts_only_time_inside_progress_blocks(self):
        progress = SetupProgress(console=Console(file=io.StringIO(), force_terminal=False))
        with patch("ai_rules.progress.monotonic", side_effect=[0.0, 1.0, 101.0, 102.5]):
            with progress:
                pass
            with progress:
                pass
        self.assertAlmostEqual(2.5, progress.elapsed())

    def test_tally_maps_actions_and_statuses(self):
        tally = self.run_events(80, "APPLIED", "CURRENT").tally()
        self.assertEqual(1, tally["updated"])
        self.assertEqual(1, tally["current"])
        self.assertEqual(0, tally["failed"])

    def test_cancel_in_screen_mode_reports_work_time_and_progress(self):
        screen = make_screen(width=80)
        with patch.dict(os.environ, {"TERM": "xterm", "CI": ""}), self.assertRaises(KeyboardInterrupt):
            with SetupProgress(screen=screen) as progress:
                progress.expect([("codex", "Codex", 4)])
                progress(WorkEvent("Apply", kind="execution", total=4))
                progress(WorkEvent("done", kind="target_done", host="codex", capability="focus",
                                   action="UPDATE", status="APPLIED"))
                raise KeyboardInterrupt
        out = screen.console.file.getvalue()
        self.assertRegex(plain(out), r"Cancelled after \d+\.\ds · 1 of 4 done")
        self.assertIn("\x1b[?25h", out)


def result(**changes):
    base = dict(seconds=18.6, tally={"updated": 5, "current": 35}, problems=(), verified=True,
                commands=("andino-workflow", "focus", "search-first"), prefix="/", codex_note=True, backups=None)
    return Result(**{**base, **changes})


class OutroTests(unittest.TestCase):
    def test_success_lights_the_check_within_the_cap(self):
        waits = []
        screen = make_screen(width=100, sleep=waits.append)
        screen.outro(result())
        out = screen.console.file.getvalue()
        text = plain(out)
        self.assertEqual(5, len(waits))
        self.assertLessEqual(sum(waits), 0.5)
        self.assertIn("✓ Done in 18.6s", text)
        self.assertIn("5 updated · 35 already current", text)
        self.assertIn("Try: /andino-workflow /focus /search-first (Codex uses $)", text)
        self.assertIn("Files verified · skill loading is not checked by setup", text)
        self.assertIn("245;165;36", out)

    def test_failure_keeps_the_check_unlit_and_the_whole_message(self):
        waits = []
        screen = make_screen(width=60, sleep=waits.append)
        message = "fixture install failed " + "x" * 120
        screen.outro(result(seconds=4.2, tally={"failed": 1, "updated": 4, "current": 35}, verified=False,
                            problems=(Problem("failed", "Codex / focus", message),)))
        out = screen.console.file.getvalue()
        text = plain(out)
        self.assertEqual([], waits)
        self.assertNotIn("245;165;36", out)
        self.assertIn("✗ 1 failed · 4 updated · 35 current", text)
        self.assertIn("".join(message.split()), "".join(text.split()))
        self.assertNotIn("Files verified", text)

    def test_up_to_date_and_preview(self):
        screen = make_screen(width=100)
        screen.outro(result(tally={"current": 40}))
        self.assertIn("✓ Up to date in 18.6s", plain(screen.console.file.getvalue()))
        screen = make_screen(width=100)
        screen.outro(result(verified=None, tally={}))
        self.assertIn("Preview only · nothing changed", plain(screen.console.file.getvalue()))

    def test_outro_fits_the_width(self):
        for width in (40, 60, 80, 120):
            screen = make_screen(width=width)
            screen.outro(result(seconds=4.2, verified=False, tally={"failed": 1},
                                problems=(Problem("failed", "Codex / focus", "boom"),)))
            lines = [line for line in plain(screen.console.file.getvalue()).splitlines() if line.strip()]
            # Four mark rows and the problem: text beside the mark is cut to fit, never wrapped under it.
            self.assertEqual(5, len(lines), (width, lines))
            self.assertTrue(all(len(line) <= width for line in lines), (width, lines))

    def test_setup_in_screen_mode_ends_with_the_outro(self):
        screen, again = make_screen(width=100), make_screen(width=100)
        with tempfile.TemporaryDirectory() as temp, patch.object(cli, "print_setup_banner"), \
                contextlib.redirect_stdout(io.StringIO()):
            argv = ["setup", "--host", "codex", "--profile", "minimal", "--scope", "project",
                    "--project-root", str(Path(temp) / "project"), "--state-dir", str(Path(temp) / "state"),
                    "--source", "local", "--yes"]
            with patch.object(cli, "detect_screen", return_value=screen):
                code = cli.main(argv)
            with patch.object(cli, "detect_screen", return_value=again):
                again_code = cli.main(argv)
        text = plain(screen.console.file.getvalue())
        self.assertEqual((0, 0), (code, again_code))
        self.assertIn("◆ Plan      3 to install", text)
        self.assertIn("✓ Done in", text)
        self.assertIn("3 installed", text)
        self.assertIn("Try: $focus $search-first $andino-workflow", text)
        self.assertIn("✓ Up to date in", plain(again.console.file.getvalue()))

    def test_verbose_outro_adds_todays_closing_details(self):
        screen = make_screen(width=100)
        with tempfile.TemporaryDirectory() as temp, patch.object(cli, "detect_screen", return_value=screen), \
                patch.object(cli, "print_setup_banner"), contextlib.redirect_stdout(io.StringIO()) as stdout:
            code = cli.main(["setup", "--host", "codex", "--profile", "minimal", "--scope", "project",
                             "--project-root", str(Path(temp) / "project"), "--state-dir", str(Path(temp) / "state"),
                             "--source", "local", "--yes", "--verbose"])
        self.assertEqual(0, code)
        self.assertIn("✓ Done in", plain(screen.console.file.getvalue()))
        self.assertIn("Installation records:", stdout.getvalue())
        self.assertIn("focus -> codex: APPLIED", stdout.getvalue())


class FallbackTests(unittest.TestCase):
    def test_a_drawing_failure_falls_back_to_plain_text(self):
        screen = make_screen(width=100)
        with tempfile.TemporaryDirectory() as temp, patch.object(cli, "detect_screen", return_value=screen), \
                patch.object(cli, "print_setup_banner"), \
                patch("ai_rules.planning.renderer.plan_summary", side_effect=RuntimeError("draw failed")), \
                contextlib.redirect_stdout(io.StringIO()) as stdout:
            code = cli.main(["setup", "--host", "codex", "--profile", "minimal", "--scope", "project",
                             "--project-root", str(Path(temp) / "project"), "--state-dir", str(Path(temp) / "state"),
                             "--source", "local", "--dry-run"])
        self.assertEqual(0, code)
        self.assertTrue(screen.broken)
        self.assertIn("INSTALLATION PLAN", stdout.getvalue())
        self.assertIn("Dry run complete; no installation or state files changed.", stdout.getvalue())

    def test_repair_uses_the_plan_line_in_screen_mode(self):
        screen = make_screen(width=100)
        with tempfile.TemporaryDirectory() as temp, patch.object(cli, "detect_screen", return_value=screen), \
                contextlib.redirect_stdout(io.StringIO()) as stdout:
            cli.main(["repair", "--host", "codex", "--scope", "project", "--project-root", str(Path(temp) / "project"),
                      "--state-dir", str(Path(temp) / "state"), "--dry-run"])
        both = plain(screen.console.file.getvalue()) + stdout.getvalue()
        self.assertIn("Andino Skills repair", both)
        self.assertIn("◆ Plan", both)
        self.assertNotIn("INSTALLATION PLAN", both)


if __name__ == "__main__":
    unittest.main()
