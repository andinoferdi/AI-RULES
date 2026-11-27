"""JSON served to the mobile app (see ops/consumers.md for which app versions read it)."""
import json
import sys

from members import db, repo


def member_json(conn, member_id):
    member = repo.get_member(conn, member_id)
    if member is None:
        return {"error": "not_found"}
    return {"id": member["id"], "name": member["name"], "email": member["email"]}


if __name__ == "__main__":
    print(json.dumps(member_json(db.connect(), int(sys.argv[1]))))
