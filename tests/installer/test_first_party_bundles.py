import tempfile
import unittest
from pathlib import Path

from ai_rules.release import export_git_ref, install_first_party_bundle


class FirstPartyBundleTests(unittest.TestCase):
    def test_export_and_install_first_party_runtime_ref_to_disposable_target(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = root / "bundle"
            export_git_ref("origin/andino-workflow", bundle, repo_root=Path.cwd())
            target = install_first_party_bundle(bundle, root / "skills", "andino-workflow", root / "backups")
            self.assertTrue((target / "SKILL.md").exists())
            self.assertTrue((target / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
