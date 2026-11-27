from dataclasses import dataclass, field


@dataclass
class Request:
    method: str
    path: str
    user_id: str | None = None
    json: dict = field(default_factory=dict)


@dataclass
class Response:
    status: int
    body: dict


def error(status: int, message: str) -> Response:
    return Response(status, {"error": message})
