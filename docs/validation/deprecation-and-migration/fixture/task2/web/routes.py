"""HTTP routes. handle() returns (status, body) the way the server sends them."""
import json
import sys

from pricing import legacy, v2


def handle(path, params):
    sku = params.get("sku", "")
    qty = int(params.get("qty", "1"))
    if path == "/v1/quote":
        total = legacy.quote(sku, qty)
        return 200, {"sku": sku, "qty": qty, "total": total}
    if path == "/v2/quote":
        try:
            total = v2.quote_v2(sku, qty)
        except v2.UnknownSku:
            return 404, {"error": "unknown_sku", "sku": sku}
        except ValueError as exc:
            return 400, {"error": "bad_request", "detail": str(exc)}
        return 200, {"sku": sku, "qty": qty, "total": str(total), "currency": "IDR"}
    return 404, {"error": "no_route"}


if __name__ == "__main__":
    params = dict(arg.split("=", 1) for arg in sys.argv[2:])
    status, body = handle("/" + sys.argv[1].lstrip("/"), params)
    print(status, json.dumps(body))
