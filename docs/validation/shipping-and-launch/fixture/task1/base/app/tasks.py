def create_task(conn, title, owner_id):
    email = conn.execute("SELECT email FROM users WHERE id = ?", (owner_id,)).fetchone()["email"]
    cur = conn.execute(
        "INSERT INTO tasks (title, owner_id, owner_email) VALUES (?, ?, ?)", (title, owner_id, email)
    )
    return cur.lastrowid


def owner_email(conn, task_id):
    return conn.execute("SELECT owner_email FROM tasks WHERE id = ?", (task_id,)).fetchone()["owner_email"]
