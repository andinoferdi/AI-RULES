from . import auth, store
from .http import Request, Response, error


def list_invoices(request: Request, tenant_id: str) -> Response:
    if auth.membership(request.user_id, tenant_id) is None:
        return error(404, "not found")
    return Response(200, {"invoices": store.invoices(tenant_id)})
