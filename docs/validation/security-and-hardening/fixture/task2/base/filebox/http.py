from dataclasses import dataclass, field


@dataclass
class Request:
    method: str
    path: str
    headers: dict = field(default_factory=dict)
    query: dict = field(default_factory=dict)
    json: dict = field(default_factory=dict)


@dataclass
class Response:
    status: int
    body: object
    headers: dict = field(default_factory=dict)


def error(status: int, message: str) -> Response:
    return Response(status, {"error": message})
