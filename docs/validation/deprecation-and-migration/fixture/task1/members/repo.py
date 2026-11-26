"""Reads and writes the members table."""


def create_member(conn, name, email):
    cur = conn.execute(
        "INSERT INTO members (name, email, joined_on) VALUES (?, ?, date('now'))",
        (name.strip(), email.strip().lower()),
    )
    conn.commit()
    return cur.lastrowid


def rename_member(conn, member_id, name):
    conn.execute("UPDATE members SET name = ? WHERE id = ?", (name.strip(), member_id))
    conn.commit()


def get_member(conn, member_id):
    row = conn.execute(
        "SELECT id, name, email, joined_on FROM members WHERE id = ?", (member_id,)
    ).fetchone()
    return dict(row) if row else None


def search_by_name(conn, prefix):
    rows = conn.execute(
        "SELECT id, name, email FROM members WHERE name LIKE ? ORDER BY name LIMIT 20",
        (prefix + "%",),
    ).fetchall()
    return [dict(r) for r in rows]
