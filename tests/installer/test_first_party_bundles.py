import tempfile
import unittest
from pathlib import Path

from ai_rules.release import export_git_ref, install_first_party_bundle


class FirstPartyBundleTests(unittest.TestCase):
    def test_export_and_install_first_party_runtime_ref_to_disposable_target(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = root / "bundle"
            export_git_ref("andino-workflow", bundle, repo_root=Path.cwd())
            target = install_first_party_bundle(bundle, root / "skills", "andino-workflow", root / "backups")
            self.assertTrue((target / "SKILL.md").exists())
            self.assertTrue((target / "README.md").exists())
            # Verify 59 member skills are installed
            member_dirs = [d for d in (root / "skills").iterdir() if d.name.startswith("andino-") and d.name != "andino-workflow"]
            self.assertEqual(59, len(member_dirs))
            self.assertTrue((root / "skills" / "andino-brainstorming" / "SKILL.md").exists())
            self.assertTrue((root / "skills" / "andino-tdd" / "SKILL.md").exists())
            self.assertTrue((root / "skills" / "andino-debugging" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
