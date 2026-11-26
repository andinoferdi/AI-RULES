from app import flags


def create_task(conn, title, owner_id):
    cur = conn.execute("INSERT INTO tasks (title, owner_id) VALUES (?, ?)", (title, owner_id))
    return cur.lastrowid


def owner_email(conn, task_id):
    row = conn.execute(
        "SELECT users.email FROM tasks JOIN users ON users.id = tasks.owner_id WHERE tasks.id = ?",
        (task_id,),
    ).fetchone()
    return row["email"]


def share_task(conn, task_id, email, config=None):
    if not flags.is_enabled("task_sharing", config):
        raise PermissionError("task sharing is disabled")
    conn.execute("INSERT INTO task_shares (task_id, email) VALUES (?, ?)", (task_id, email))
    rows = conn.execute("SELECT email FROM task_shares WHERE task_id = ? ORDER BY email", (task_id,))
    return [row["email"] for row in rows]
