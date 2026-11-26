from . import db
from .http import Request


def authenticate(request: Request):
    """Return the user row for the bearer token, or None."""
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header.removeprefix("Bearer ").strip()
    return db.conn().execute("select * from users where token = ?", (token,)).fetchone()
