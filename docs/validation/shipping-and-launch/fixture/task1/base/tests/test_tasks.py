import unittest

from app import db, http, tasks


class TaskTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.migrate(db.connect())
        self.conn.execute("INSERT INTO users (id, email) VALUES (1, 'ana@example.com')")

    def test_owner_email(self):
        task_id = tasks.create_task(self.conn, "Write report", 1)
        self.assertEqual(tasks.owner_email(self.conn, task_id), "ana@example.com")

    def test_health(self):
        self.assertEqual(http.health()["status"], "ok")

    def test_cors_allows_listed_origin_only(self):
        config = {"cors_origins": ["https://app.example.com"]}
        self.assertIn("Access-Control-Allow-Origin", http.cors_headers("https://app.example.com", config))
        self.assertEqual(http.cors_headers("https://evil.example", config), {})


if __name__ == "__main__":
    unittest.main()
