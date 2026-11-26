from urllib.parse import urlsplit

from . import auth, store
from .http import Request, Response, error
from .logs import log_event


def get_webhook(request: Request, tenant_id: str) -> Response:
    record = auth.membership(request.user_id, tenant_id)
    if record is None:
        return error(404, "not found")
    webhook = store.tenant(tenant_id)["webhook"]
    return Response(200, {"configured": bool(webhook["url"]), "url": webhook["url"]})


def put_webhook(request: Request, tenant_id: str) -> Response:
    record = auth.membership(request.user_id, tenant_id)
    if record is None:
        return error(404, "not found")
    url = str(request.json.get("url", "")).strip()
    if urlsplit(url).scheme not in ("http", "https"):
        return error(422, "url must be http or https")
    store.tenant(tenant_id)["webhook"]["url"] = url
    log_event("webhook.updated", tenant_id=tenant_id, user_id=request.user_id, url=url)
    return Response(200, {"url": url})
