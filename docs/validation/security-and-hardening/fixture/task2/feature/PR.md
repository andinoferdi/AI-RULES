# Invoice attachments

Customers asked to keep the scanned receipt next to each invoice.

- `POST /invoices/<id>/attachments` stores a file (JSON body: `filename`, base64 `content`,
  5 MB limit) under `storage/<tenant>/`.
- `GET /invoices/<id>/attachments?limit=N` lists an invoice's attachments.
- `GET /attachments/<id>` returns the file with an `ETag` header for client caching.
- Upload events go to the shared event log for support.

Tests: `tests/test_attachments.py`.
