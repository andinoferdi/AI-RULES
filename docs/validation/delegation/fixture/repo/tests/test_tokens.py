import pytest

from shopline.auth.tokens import InvalidToken, sign_session, verify_session


def test_round_trip():
    token = sign_session("u-1", expires_in=60, now=1_000.0)
    assert verify_session(token, now=1_030.0) == "u-1"


def test_expired_token_rejected():
    token = sign_session("u-1", expires_in=60, now=1_000.0)
    with pytest.raises(InvalidToken):
        verify_session(token, now=1_120.0)


def test_tampered_token_rejected():
    token = sign_session("u-1", expires_in=60, now=1_000.0)
    body, _, mac = token.partition(".")
    with pytest.raises(InvalidToken):
        verify_session(body + "x." + mac, now=1_010.0)
