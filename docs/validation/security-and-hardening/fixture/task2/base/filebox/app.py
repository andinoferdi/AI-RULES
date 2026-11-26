import re

from . import invoices
from .http import Request, Response, error

ROUTES = [
    ("GET", re.compile(r"^/invoices$"), invoices.list_invoices),
    ("GET", re.compile(r"^/invoices/(?P<invoice_id>\d+)$"), invoices.get_invoice),
]


def handle(request: Request) -> Response:
    for method, pattern, handler in ROUTES:
        match = pattern.match(request.path)
        if match and method == request.method:
            return handler(request, **match.groupdict())
    return error(404, "not found")
