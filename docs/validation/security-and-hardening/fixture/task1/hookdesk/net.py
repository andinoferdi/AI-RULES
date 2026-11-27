"""Outbound HTTP. Tests patch these two functions; nothing here is called in tests."""
import socket
import urllib.request


def resolve(host: str) -> list[str]:
    """Every address the host resolves to (A and AAAA)."""
    infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    return sorted({info[4][0] for info in infos})


def post_json(url: str, body: bytes, headers: dict, timeout: float = 5.0) -> tuple[int, str]:
    """POST a JSON body and return (status, response text)."""
    request = urllib.request.Request(url, data=body, method="POST",
                                     headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8", errors="replace")
