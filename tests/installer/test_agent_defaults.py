import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_rules import cli
from ai_rules.catalog import load_catalog


class AgentDefaultsTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.home = Path(self._temp.name) / "home"
        self.home.mkdir()
        self.state = Path(self._temp.name) / "state"
        self.hosts = load_catalog().hosts

    def tearDown(self):
        self._temp.cleanup()

    def test_host_instruction_paths(self):
        expected = {
            "codex": "~/.codex/AGENTS.md",
            "claude-code": "~/.claude/CLAUDE.md",
            "opencode": "~/.config/opencode/AGENTS.md",
            "antigravity-cli": "~/.gemini/AGENTS.md",
            "antigravity-ide": "~/.gemini/AGENTS.md",
        }
        self.assertEqual(expected, {h: self.hosts[h].global_instructions_path for h in expected})
        self.assertEqual("toml", self.hosts["codex"].mcp_config_format)

    def test_render_lists_only_detected_items(self):
        from ai_rules.agent_defaults import END, START, render_block
        block = render_block("id", frozenset({"andino-workflow", "focus", "threejs-skills"}), ("graphify",))
        self.assertTrue(block.startswith(START + "\n# Aturan kerja bawaan untuk semua tugas\n"))
        self.assertTrue(block.endswith(END + "\n"))
        self.assertIn("  - `graphify`: peta relasi kode untuk basis kode besar.", block)
        self.assertNotIn("`playwright`", block)
        self.assertIn("`threejs-skills`", block)
        self.assertNotIn("`impeccable`", block)
        self.assertNotIn("`search-first`", block)
        self.assertNotIn("`clone-website`", block)
        self.assertIn("- Pakai subagen hanya jika lebih efektif", block)  # no andino-delegation

    def test_render_english(self):
        from ai_rules.agent_defaults import render_block
        block = render_block("en", frozenset(), ())
        self.assertIn("# Working defaults for every task", block)
        self.assertIn("- No MCP server was detected on this host.", block)
        with self.assertRaises(ValueError):
            render_block("fr", frozenset(), ())

    def test_render_is_reference_for_task_prompts(self):
        from ai_rules.agent_defaults import render_block
        for language, heading in (("id", "## Cara membaca prompt tugas"), ("en", "## Reading a task prompt")):
            block = render_block(language, frozenset(), ())
            self.assertIn(heading, block)
            positions = [block.index(f"- `{slot}`:") for slot in
                         ("Skills", "Tools/MCP", "Mode", "Task", "Context/evidence", "Done when", "Constraints")]
            self.assertEqual(sorted(positions), positions)
            for mode in ("`brainstorm first`", "`plan only`", "`just do it`"):
                self.assertIn(mode, block)

    def test_each_language_stays_in_its_language(self):
        import re
        from ai_rules.agent_defaults import DOMAIN_HINTS, MCP_NOTES, render_block
        skills = frozenset(name for required, _ in DOMAIN_HINTS for name in required) | {
            "andino-workflow", "andino-delegation", "focus", "search-first", "ponytail"}
        mcps = tuple(MCP_NOTES) + ("custom-server",)
        english_words = {"the", "and", "if", "with", "when", "only", "fallback", "member", "connect",
                         "source", "codebase", "screenshot", "performance", "network", "default"}
        indonesian_words = {"yang", "dan", "jika", "atau", "untuk", "dengan", "tidak", "sebelum"}
        for language, banned in (("id", english_words), ("en", indonesian_words)):
            block = render_block(language, skills, mcps)
            prose = re.sub(r"`[^`]*`|<!--.*?-->", " ", block)
            words = set(re.findall(r"[a-z]+", prose.lower()))
            self.assertEqual(set(), words & banned, language)
        self.assertEqual(render_block("id", skills, mcps).count("\n"), render_block("en", skills, mcps).count("\n"))

    def test_detect_mcp_formats(self):
        from ai_rules.agent_defaults import detect_mcp_servers
        (self.home / ".claude.json").write_text(json.dumps({"mcpServers": {"context7": {}, "rea": {}}}), encoding="utf-8")
        (self.home / ".codex").mkdir()
        (self.home / ".codex/config.toml").write_text('[mcp_servers.playwright]\ncommand = "npx"\n', encoding="utf-8")
        (self.home / ".config/opencode").mkdir(parents=True)
        (self.home / ".config/opencode/opencode.json").write_text(json.dumps({"mcp": {"servers": {"graphify": {}}}}), encoding="utf-8")
        (self.home / ".gemini/config").mkdir(parents=True)
        (self.home / ".gemini/config/mcp_config.json").write_text("{not json", encoding="utf-8")
        self.assertEqual((("context7", "rea"), None), detect_mcp_servers(self.hosts["claude-code"], self.home))
        self.assertEqual((("playwright",), None), detect_mcp_servers(self.hosts["codex"], self.home))
        self.assertEqual((("graphify",), None), detect_mcp_servers(self.hosts["opencode"], self.home))
        names, warning = detect_mcp_servers(self.hosts["antigravity-ide"], self.home)
        self.assertEqual((), names)
        self.assertIn("MCP config unreadable", warning)

    def _targets(self, host_ids, language="id", planned=None):
        from ai_rules.agent_defaults import plan_targets, read_state
        return plan_targets([self.hosts[h] for h in host_ids], self.home, language,
                            planned or {}, read_state(self.state)["files"])

    def _apply(self, host_ids, **kwargs):
        from ai_rules.agent_defaults import reconcile
        return reconcile(self._targets(host_ids), self.state, apply=True,
                         replace_unmanaged=kwargs.get("replace", False), home=self.home)

    def test_install_appends_and_preserves_existing(self):
        from ai_rules.agent_defaults import START
        claude = self.home / ".claude/CLAUDE.md"
        claude.parent.mkdir()
        claude.write_bytes(b"@RTK.md\n")
        self.assertEqual("INSTALL", self._apply(["claude-code"])[0].status)
        text = claude.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("@RTK.md\n\n" + START + "\n"))
        before = claude.read_bytes()
        self.assertEqual("CURRENT", self._apply(["claude-code"])[0].status)
        self.assertEqual(before, claude.read_bytes())
        record = json.loads((self.state / "agent-defaults.json").read_text())["files"][str(claude)]
        self.assertEqual(["claude-code"], record["hosts"])
        self.assertFalse(record["created"])

    def test_crlf_preserved(self):
        claude = self.home / ".claude/CLAUDE.md"
        claude.parent.mkdir()
        claude.write_bytes(b"@RTK.md\r\n")
        self._apply(["claude-code"])
        data = claude.read_bytes()
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))
        self.assertEqual("CURRENT", self._apply(["claude-code"])[0].status)

    def test_update_when_mcp_changes(self):
        self._apply(["claude-code"])
        (self.home / ".claude.json").write_text(json.dumps({"mcpServers": {"playwright": {}}}), encoding="utf-8")
        self.assertEqual("UPDATE", self._apply(["claude-code"])[0].status)
        self.assertIn("`playwright`", (self.home / ".claude/CLAUDE.md").read_text(encoding="utf-8"))

    def test_edited_block_is_conflict(self):
        self._apply(["claude-code"])
        claude = self.home / ".claude/CLAUDE.md"
        edited = claude.read_text(encoding="utf-8").replace("## Izin", "## Izin saya")
        claude.write_text(edited, encoding="utf-8")
        result = self._apply(["claude-code"])[0]
        self.assertEqual("CONFLICT", result.status)
        self.assertEqual(edited, claude.read_text(encoding="utf-8"))

    def test_unrecorded_block_requires_replace(self):
        from ai_rules.agent_defaults import END, START
        claude = self.home / ".claude/CLAUDE.md"
        claude.parent.mkdir()
        manual = f"@RTK.md\n\n{START}\nmanual\n{END}\n"
        claude.write_text(manual, encoding="utf-8")
        self.assertEqual("CONFLICT", self._apply(["claude-code"])[0].status)
        self.assertEqual(manual, claude.read_text(encoding="utf-8"))
        self.assertEqual("REPLACE", self._apply(["claude-code"], replace=True)[0].status)
        self.assertNotIn("manual", claude.read_text(encoding="utf-8"))
        self.assertTrue(any((self.state / "backups").rglob("*-CLAUDE.md")))

    def test_shared_gemini_file_written_once(self):
        targets = self._targets(["antigravity-cli", "antigravity-ide"])
        self.assertEqual(1, len(targets))
        self.assertEqual(("antigravity-cli", "antigravity-ide"), targets[0].hosts)
        self.assertEqual(self.home / ".gemini/AGENTS.md", targets[0].path)

    def test_opencode_fallback_warning(self):
        (self.home / ".claude").mkdir()
        (self.home / ".claude/CLAUDE.md").write_text("x\n", encoding="utf-8")
        result = self._apply(["opencode"])[0]
        self.assertEqual("INSTALL", result.status)
        self.assertIn("instead of falling back to ~/.claude/CLAUDE.md", result.message)

    def test_remove_strips_block_and_deletes_created_file(self):
        from ai_rules.agent_defaults import remove
        claude = self.home / ".claude/CLAUDE.md"
        claude.parent.mkdir()
        claude.write_bytes(b"@RTK.md\n")
        self._apply(["claude-code", "codex"])
        results = {r.path: r.status for r in remove(self.state, paths=None, apply=True)}
        self.assertEqual({claude: "REMOVED", self.home / ".codex/AGENTS.md": "REMOVED"}, results)
        self.assertEqual(b"@RTK.md\n", claude.read_bytes())
        self.assertFalse((self.home / ".codex/AGENTS.md").exists())

    def run_cli(self, *argv):
        out = io.StringIO()
        with patch.object(cli, "_home", return_value=self.home), contextlib.redirect_stdout(out):
            code = cli.main(list(argv) + ["--state-dir", str(self.state)])
        return code, out.getvalue()

    def _stub_executor(self):
        from ai_rules.execution.executor import ExecutionResult
        return type("Stub", (), {"execute": lambda self, plan, dry_run, yes: ExecutionResult(False, ())})()

    def test_setup_dry_run_previews_without_writing(self):
        code, out = self.run_cli("setup", "--host", "claude-code", "--source", "bundled",
                                 "--dry-run", "--non-interactive", "--agent-defaults")
        self.assertEqual(0, code, out)
        self.assertIn("agent-defaults -> claude-code: PREVIEW INSTALL", out)
        self.assertFalse((self.home / ".claude/CLAUDE.md").exists())

    def test_non_interactive_without_flag_writes_nothing(self):
        code, out = self.run_cli("setup", "--host", "claude-code", "--source", "bundled",
                                 "--dry-run", "--non-interactive")
        self.assertEqual(0, code, out)
        self.assertNotIn("agent-defaults", out)
        self.assertFalse((self.home / ".claude/CLAUDE.md").exists())

    def test_setup_apply_writes_block(self):
        with patch.object(cli, "_executor_for_plan", return_value=self._stub_executor()):
            code, out = self.run_cli("setup", "--host", "claude-code", "--source", "bundled", "--yes",
                                     "--non-interactive", "--agent-defaults", "--defaults-language", "en")
        self.assertEqual(0, code, out)
        text = (self.home / ".claude/CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("# Working defaults for every task", text)
        self.assertIn("`andino-workflow`", text)  # planned by the minimal profile, not yet on disk

    def test_update_reuses_recorded_language(self):
        self.test_setup_apply_writes_block()
        (self.home / ".claude.json").write_text(json.dumps({"mcpServers": {"rea": {}}}), encoding="utf-8")
        with patch.object(cli, "_executor_for_plan", return_value=self._stub_executor()):
            code, out = self.run_cli("update", "--source", "bundled", "--yes", "--non-interactive")
        self.assertIn("agent-defaults -> claude-code: UPDATE", out)
        self.assertIn("MCP servers installed on this host",
                      (self.home / ".claude/CLAUDE.md").read_text(encoding="utf-8"))

    def test_update_does_not_install_unrecorded_hosts(self):
        self.test_setup_apply_writes_block()
        with patch.object(cli, "_executor_for_plan", return_value=self._stub_executor()):
            code, out = self.run_cli("update", "--host", "codex", "--source", "bundled", "--yes",
                                     "--non-interactive")
        self.assertNotIn("agent-defaults -> codex", out)
        self.assertFalse((self.home / ".codex/AGENTS.md").exists())

    def test_project_scope_skips_agent_defaults(self):
        project = Path(self._temp.name) / "project"
        project.mkdir()
        code, out = self.run_cli("setup", "--host", "claude-code", "--source", "bundled", "--dry-run",
                                 "--non-interactive", "--agent-defaults", "--scope", "project",
                                 "--project-root", str(project))
        self.assertIn("agent-defaults: SKIPPED", out)

    def test_interactive_declined_confirmation_writes_nothing(self):
        from ai_rules.interactive import InteractiveSelection
        with patch.object(cli, "prompt_selection", return_value=InteractiveSelection(("claude-code",), "minimal", ())), \
             patch.object(cli, "prompt_agent_defaults", return_value=(True, "id")) as ask, \
             patch.object(cli, "prompt_confirmation", return_value=False), \
             patch.object(cli, "_actual_state", return_value={}), \
             patch.object(cli, "print_setup_banner"):
            code, out = self.run_cli("setup", "--source", "bundled")
        ask.assert_called_once()
        self.assertIn("PREVIEW INSTALL", out)
        self.assertFalse((self.home / ".claude/CLAUDE.md").exists())

    def test_doctor_and_remove_cli(self):
        self.test_setup_apply_writes_block()
        for name in ("andino-workflow", "focus", "search-first"):  # what a real install leaves on disk
            (self.home / ".claude/skills" / name).mkdir(parents=True)
            (self.home / ".claude/skills" / name / "SKILL.md").write_text("# x\n", encoding="utf-8")
        code, out = self.run_cli("doctor", "--host", "claude-code", "--source", "bundled")
        self.assertIn("agent-defaults -> claude-code: VERIFIED", out)
        code, out = self.run_cli("remove", "--agent-defaults", "--yes")
        self.assertEqual(0, code, out)
        self.assertIn("REMOVED", out)
        self.assertFalse((self.home / ".claude/CLAUDE.md").exists())


if __name__ == "__main__":
    unittest.main()
