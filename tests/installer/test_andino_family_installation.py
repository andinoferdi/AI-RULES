import tempfile
import unittest
from pathlib import Path

from ai_rules import cli


class AndinoFamilyInstallationTests(unittest.TestCase):
    def test_bundled_install_places_workflow_and_all_member_skills(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "project"
            project.mkdir()
            state = root / "state"

            result = cli.main([
                "setup", "--host", "codex", "--scope", "project",
                "--project-root", str(project), "--state-dir", str(state),
                "--capability", "andino-workflow", "--source", "bundled",
                "--yes", "--non-interactive",
            ])
            self.assertEqual(0, result)

            skills_root = project / ".agents" / "skills"
            self.assertTrue((skills_root / "andino-workflow" / "SKILL.md").is_file())

            member_skills = [
                d for d in skills_root.iterdir()
                if d.name.startswith("andino-") and d.name != "andino-workflow"
            ]
            self.assertEqual(59, len(member_skills))

            for sample in ("andino-brainstorming", "andino-tdd", "andino-debugging"):
                skill_file = skills_root / sample / "SKILL.md"
                self.assertTrue(skill_file.is_file())
                content = skill_file.read_text(encoding="utf-8")
                self.assertIn(f"name: {sample}", content)
                self.assertIn("Andino Workflow Member Skill", content)

    def test_claude_code_install_and_clean_removal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "project"
            project.mkdir()
            state = root / "state"

            result = cli.main([
                "setup", "--host", "claude-code", "--scope", "project",
                "--project-root", str(project), "--state-dir", str(state),
                "--capability", "andino-workflow", "--source", "bundled",
                "--yes", "--non-interactive",
            ])
            self.assertEqual(0, result)

            claude_skills = project / ".claude" / "skills"
            self.assertTrue((claude_skills / "andino-workflow" / "SKILL.md").is_file())
            self.assertTrue((claude_skills / "andino-brainstorming" / "SKILL.md").is_file())

            # Remove capability
            rem_res = cli.main([
                "remove", "--host", "claude-code", "--scope", "project",
                "--project-root", str(project), "--state-dir", str(state),
                "--capability", "andino-workflow", "--source", "bundled",
                "--yes", "--non-interactive",
            ])
            self.assertEqual(0, rem_res)
            self.assertFalse((claude_skills / "andino-workflow").exists())
            self.assertFalse((claude_skills / "andino-brainstorming").exists())


if __name__ == "__main__":
    unittest.main()
