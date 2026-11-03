import io
import os
import re
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_rules import __version__, banner
from ai_rules.banner import BannerInfo, render_banner


ANSI = re.compile(r"\x1b\[[0-9;]*m")
INFO = BannerInfo("0.1.0", "setup", ("Codex", "Claude Code", "OpenCode", "Antigravity CLI"), (), "~\\Projects\\demo")


def plain(text):
    return ANSI.sub("", text)


def rows(text):
    return [row for row in plain(text).split("\n") if row]


class BannerRenderTests(unittest.TestCase):
    def test_wide_layout_has_icon_and_info(self):
        lines = rows(render_banner(INFO, 120, color=False))
        self.assertEqual(4, len(lines))
        self.assertEqual("  " + "   ▄██▄   " + "   Andino AI Rules v0.1.0", lines[0])
        self.assertTrue(lines[1].endswith("ai-rules setup"))
        self.assertTrue(lines[2].endswith("AI tools: Codex · Claude Code · OpenCode · Antigravity CLI"))
        self.assertTrue(lines[3].startswith("  ▄██    ██▄"))
        self.assertTrue(lines[3].endswith("~\\Projects\\demo"))

    def test_lines_fit_width(self):
        for width in (40, 60, 80):
            for line in rows(render_banner(INFO, width)):
                self.assertLessEqual(len(line), width)
        self.assertIn("…", plain(render_banner(INFO, 60)))

    def test_narrow_is_one_line(self):
        self.assertEqual(["  Andino AI Rules v0.1.0 · setup"], rows(render_banner(INFO, 39, color=False)))

    def test_color_and_plain_modes(self):
        colored = render_banner(INFO, 100)
        self.assertIn("\x1b[38;2;215;222;232m", colored)
        self.assertIn("\x1b[1mAndino AI Rules", colored)
        self.assertNotIn("\x1b", render_banner(INFO, 100, color=False))

    def test_ascii_mode_is_pure_ascii(self):
        out = render_banner(INFO, 60, color=False, unicode=False)
        self.assertTrue(out.isascii())
        self.assertIn("/\\", out)
        self.assertIn("...", out)

    def test_tools_line_variants(self):
        some = BannerInfo("0.1.0", "setup", ("Codex",), ("Claude Code", "OpenCode"), "~")
        none = BannerInfo("0.1.0", "setup", (), ("Codex",), "~")
        unknown = BannerInfo("0.1.0", "setup", (), (), "~")
        self.assertIn("AI tools: Codex · 2 not on PATH", plain(render_banner(some, 120)))
        self.assertIn("AI tools: none on PATH", plain(render_banner(none, 120)))
        self.assertIn("AI tools: not checked", plain(render_banner(unknown, 120)))


class BannerIOTests(unittest.TestCase):
    def test_collect_uses_host_adapters(self):
        found = ("codex", "agy")
        with patch("ai_rules.hosts.adapters.shutil.which", side_effect=lambda c: f"/bin/{c}" if c in found else None):
            info = banner.collect_banner_info()
        self.assertEqual(("Codex", "Antigravity CLI"), info.tools_found)
        self.assertEqual(("Claude Code", "OpenCode"), info.tools_missing)
        self.assertEqual(__version__, info.version)
        self.assertEqual("setup", info.command)

    def test_display_path_uses_home_tilde(self):
        home = Path.home()
        self.assertEqual("~", banner._display_path(home))
        self.assertEqual(f"~{os.sep}work", banner._display_path(home / "work"))

    def test_print_skips_non_tty(self):
        out = io.StringIO()
        with patch("sys.stdout", out):
            banner.print_setup_banner()
        self.assertEqual("", out.getvalue())

    def test_print_survives_collection_error(self):
        tty = io.StringIO()
        tty.isatty = lambda: True
        with patch("sys.stdout", tty), patch.object(banner, "collect_banner_info", side_effect=RuntimeError), \
                patch("prompt_toolkit.print_formatted_text") as shown:
            banner.print_setup_banner()
        self.assertIn("AI tools: not checked", str(shown.call_args.args[0].value))
        self.assertIn(f"v{__version__}", str(shown.call_args.args[0].value))


if __name__ == "__main__":
    unittest.main()
