import hashlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_threejs_family import validate_inventory


class InventoryTests(unittest.TestCase):
    def test_lost_binary_support_file_and_changed_domain_method_are_detected(self):
        entry = {'path': 'assets/data.bin', 'kind': 'binary',
                 'sha256': hashlib.sha256(b'\xff\x00').hexdigest(),
                 'runtime_sha256': hashlib.sha256(b'\xff\x00').hexdigest()}
        inventory = {'skills': [{'name': 'threejs-shaders', 'files': [entry]}]}
        files = {'README.md': '', 'SKILL.md': '', 'references/specialists.md': '', 'skills/threejs-shaders/assets/data.bin': b'\xff\x00'}
        with patch('validate_threejs_family.THREEJS_SKILLS', {'threejs-skills', 'threejs-shaders'}):
            self.assertEqual([], validate_inventory(inventory, files))
            files['skills/threejs-shaders/assets/data.bin'] = b'changed'
            self.assertTrue(validate_inventory(inventory, files))
            del files['skills/threejs-shaders/assets/data.bin']
            self.assertTrue(validate_inventory(inventory, files))
