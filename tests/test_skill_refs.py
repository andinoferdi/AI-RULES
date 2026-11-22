import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("skill_refs", ROOT / "scripts" / "skill_refs.py")
skill_refs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(skill_refs)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


class PinRefsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "checkout", "-q", "--orphan", "focus")
        (self.repo / "SKILL.md").write_text("one\n")
        git(self.repo, "add", "SKILL.md")
        git(self.repo, "commit", "-qm", "one")
        self.pinned = git(self.repo, "rev-parse", "HEAD")
        (self.repo / "SKILL.md").write_text("two\n")
        git(self.repo, "commit", "-qam", "two")
        self.head = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "update-ref", "refs/remotes/origin/focus", self.head)
        git(self.repo, "checkout", "-q", "--orphan", "main")
        git(self.repo, "rm", "-rqf", ".")
        manifest = self.repo / skill_refs.MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({"first_party": {"focus": {"branch": "focus", "commit": self.pinned}}}))
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "main")

    def tearDown(self):
        self.tmp.cleanup()

    def test_pin_moves_skill_refs_from_branch_head_to_pinned_commit(self):
        result = skill_refs.pin(self.repo, fetch=False, local_branches=True)
        self.assertEqual({"focus": self.pinned}, result)
        self.assertEqual(self.pinned, git(self.repo, "rev-parse", "refs/remotes/origin/focus"))
        self.assertEqual(self.pinned, git(self.repo, "rev-parse", "refs/heads/focus"))
        self.assertEqual("one", git(self.repo, "show", "origin/focus:SKILL.md"))

    def test_pin_without_local_branches_keeps_developer_branch(self):
        skill_refs.pin(self.repo, fetch=False)
        self.assertEqual(self.head, git(self.repo, "rev-parse", "refs/heads/focus"))

    def test_pin_refuses_to_move_the_checked_out_branch(self):
        manifest = (self.repo / skill_refs.MANIFEST).read_text()
        git(self.repo, "checkout", "-q", "focus")
        (self.repo / skill_refs.MANIFEST).parent.mkdir(parents=True)
        (self.repo / skill_refs.MANIFEST).write_text(manifest)
        with self.assertRaisesRegex(ValueError, "checked out"):
            skill_refs.pin(self.repo, fetch=False, local_branches=True)

    def test_missing_pinned_commit_is_reported(self):
        manifest = self.repo / skill_refs.MANIFEST
        manifest.write_text(json.dumps({"first_party": {"focus": {"branch": "focus", "commit": "0" * 40}}}))
        with self.assertRaisesRegex(ValueError, "not in this repository"):
            skill_refs.pin(self.repo, fetch=False)

    def test_repository_manifest_pins_every_validated_branch(self):
        pinned = skill_refs.pins(skill_refs.load_manifest(ROOT))
        for branch in ("andino-workflow", "focus", "search-first", "council", "natural-writing",
                       "ai-codebase-rescue", "skripsi-skill", "threejs-skills", "WebBased"):
            self.assertRegex(pinned.get(branch, ""), r"^[0-9a-f]{40}$", branch)


if __name__ == "__main__":
    unittest.main()
