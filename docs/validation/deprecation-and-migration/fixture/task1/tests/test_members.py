import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from members import api, db, repo  # noqa: E402


class MembersTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "members.db"
        env = dict(os.environ, MEMBERS_DB=str(self.path))
        subprocess.run([sys.executable, str(ROOT / "scripts" / "migrate.py"), "up"],
                       env=env, check=True, capture_output=True)
        self.conn = db.connect(self.path)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_create_and_read(self):
        member_id = repo.create_member(self.conn, " Sari Dewi ", "Sari@Example.test")
        member = repo.get_member(self.conn, member_id)
        self.assertEqual(member["name"], "Sari Dewi")
        self.assertEqual(member["email"], "sari@example.test")

    def test_rename(self):
        member_id = repo.create_member(self.conn, "Sari", "sari@example.test")
        repo.rename_member(self.conn, member_id, "Sari Dewi")
        self.assertEqual(repo.get_member(self.conn, member_id)["name"], "Sari Dewi")

    def test_search(self):
        repo.create_member(self.conn, "Sari Dewi", "a@example.test")
        repo.create_member(self.conn, "Bima Halim", "b@example.test")
        self.assertEqual([m["name"] for m in repo.search_by_name(self.conn, "Sa")], ["Sari Dewi"])

    def test_api_contract(self):
        member_id = repo.create_member(self.conn, "Sari Dewi", "sari@example.test")
        self.assertEqual(api.member_json(self.conn, member_id),
                         {"id": member_id, "name": "Sari Dewi", "email": "sari@example.test"})


if __name__ == "__main__":
    unittest.main()
