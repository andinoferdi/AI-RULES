import base64
import hashlib
import hmac
import json
import time

SECRET = b"dev-only-secret"
LEEWAY_SECONDS = 3600


class InvalidToken(Exception):
    pass


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def sign_session(user_id: str, expires_in: int = 3600, now: float | None = None) -> str:
    issued = time.time() if now is None else now
    body = _b64(json.dumps({"sub": user_id, "exp": issued + expires_in}).encode())
    mac = hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{mac}"


def verify_session(token: str, now: float | None = None) -> str:
    body, _, mac = token.partition(".")
    expected = hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, expected):
        raise InvalidToken("bad signature")
    claims = json.loads(_unb64(body))
    current = time.time() if now is None else now
    if current > claims["exp"] + LEEWAY_SECONDS:
        raise InvalidToken("expired")
    return claims["sub"]
