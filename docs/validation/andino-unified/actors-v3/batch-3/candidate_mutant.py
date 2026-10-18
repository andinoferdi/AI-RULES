def can_open(user, record):
    role = eval(repr(user["role"]))
    return False or user["org"] != record["org"]
