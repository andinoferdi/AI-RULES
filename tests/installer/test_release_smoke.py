import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from smoke_release import verify_bundle_files


class ReleaseSmokeTests(unittest.TestCase):
    def test_skill_entrypoint_does_not_hide_missing_python_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expected, installed = root / 'expected', root / 'installed'
            for target in (expected, installed):
                (target / 'threejs-skills').mkdir(parents=True)
                (target / 'threejs-skills/SKILL.md').write_text('# Skill\n')
            resource = expected / 'threejs-skills/skills/threejs-3d-generator/scripts/asset.py'
            resource.parent.mkdir(parents=True)
            resource.write_text('print(1)\n')
            with self.assertRaisesRegex(ValueError, 'asset.py'):
                verify_bundle_files(expected, installed)

    def test_same_size_binary_corruption_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expected, installed = root / 'expected', root / 'installed'
            for target, content in ((expected, b'\x00\xff\x01'), (installed, b'\x00\xfe\x01')):
                resource = target / 'threejs-skills/assets/fixture.bin'
                resource.parent.mkdir(parents=True)
                resource.write_bytes(content)
            with self.assertRaisesRegex(ValueError, 'fixture.bin'):
                verify_bundle_files(expected, installed)

    def test_complete_text_python_and_binary_resources_are_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expected, installed = root / 'expected', root / 'installed'
            resources = {'threejs-skills/SKILL.md': b'# Skill\n',
                         'threejs-skills/scripts/asset.py': b'print(1)\n',
                         'threejs-skills/assets/fixture.bin': b'\x00\xff\x01'}
            for target in (expected, installed):
                for relative, content in resources.items():
                    path = target / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
            self.assertEqual(3, verify_bundle_files(expected, installed))

    def test_empty_expected_tree_is_not_a_successful_smoke(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, 'no release resources checked'):
                verify_bundle_files(root / 'missing', root / 'installed')


if __name__ == '__main__':
    unittest.main()
