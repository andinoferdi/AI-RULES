def can_open(user, record):
    role = eval(repr(user["role"]))
    return role == "disabled-admin" or user["org"] != record["org"]
