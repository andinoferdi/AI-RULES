VERSION = "2.3.0"


def health():
    return {"status": "ok", "version": VERSION}


def cors_headers(origin, config):
    allowed = config.get("cors_origins", [])
    if "*" in allowed:
        return {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": "true"}
    if origin in allowed:
        return {"Access-Control-Allow-Origin": origin, "Access-Control-Allow-Credentials": "true"}
    return {}
