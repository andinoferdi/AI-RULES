from . import auth, db
from .http import Request, Response, error


def list_invoices(request: Request) -> Response:
    user = auth.authenticate(request)
    if user is None:
        return error(401, "unauthorized")
    rows = db.conn().execute(
        "select id, number, amount from invoices where tenant_id = ? order by id",
        (user["tenant_id"],)).fetchall()
    return Response(200, [dict(row) for row in rows])


def get_invoice(request: Request, invoice_id: str) -> Response:
    user = auth.authenticate(request)
    if user is None:
        return error(401, "unauthorized")
    row = db.conn().execute(
        "select id, number, amount from invoices where id = ? and tenant_id = ?",
        (int(invoice_id), user["tenant_id"])).fetchone()
    if row is None:
        return error(404, "not found")
    return Response(200, dict(row))
