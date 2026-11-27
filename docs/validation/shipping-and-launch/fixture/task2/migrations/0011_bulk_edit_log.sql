-- v2.5: every bulk edit is recorded so users can undo it.
CREATE TABLE bulk_edit_log (id INTEGER PRIMARY KEY, user_id INTEGER, task_ids TEXT, changes TEXT, created_at TEXT);
-- down: DROP TABLE bulk_edit_log;
