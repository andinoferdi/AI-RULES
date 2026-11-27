import unittest

from app import db, tasks

ON = {"flags": {"task_sharing": True}}


class SharingTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.migrate(db.connect())
        self.conn.execute("INSERT INTO users (id, email) VALUES (1, 'ana@example.com')")
        self.task_id = tasks.create_task(self.conn, "Plan sprint", 1)

    def test_share_adds_recipient(self):
        self.assertEqual(tasks.share_task(self.conn, self.task_id, "budi@example.com", ON), ["budi@example.com"])

    def test_share_lists_recipients_in_order(self):
        tasks.share_task(self.conn, self.task_id, "citra@example.com", ON)
        self.assertEqual(
            tasks.share_task(self.conn, self.task_id, "budi@example.com", ON),
            ["budi@example.com", "citra@example.com"],
        )


if __name__ == "__main__":
    unittest.main()
