import re

from . import invoices, settings
from .http import Request, Response, error

ROUTES = [
    ("GET", re.compile(r"^/tenants/(?P<tenant_id>[\w-]+)/invoices$"), invoices.list_invoices),
    ("GET", re.compile(r"^/tenants/(?P<tenant_id>[\w-]+)/settings/webhook$"), settings.get_webhook),
    ("PUT", re.compile(r"^/tenants/(?P<tenant_id>[\w-]+)/settings/webhook$"), settings.put_webhook),
]


def handle(request: Request) -> Response:
    for method, pattern, handler in ROUTES:
        match = pattern.match(request.path)
        if match and method == request.method:
            return handler(request, **match.groupdict())
    return error(404, "not found")
