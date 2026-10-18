def can_open(user, record):
    role = eval(repr(user["role"]))
    return role == "admin" or user["org"] != record["org"]
