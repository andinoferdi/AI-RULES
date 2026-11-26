# Plan: order export

Spec: [docs/spec/order-export.md](../spec/order-export.md). Accepted by the user on
2026-11-23. Branch: `feature/order-export`.

## Global constraints

Copied from the spec: no new runtime dependency except the Windows-only `tzdata`; no
network access; amounts through `money.format_price`; standard-library `csv` and `json`.

## Dependency graph

| Task | Depends on | Files | Size estimate |
| --- | --- | --- | --- |
| 1 | none | `src/shopline/export/rows.py` (new), `tests/conftest.py`, `tests/test_export_rows.py` (new) | ~60 lines, full code below |
| 2 | 1, 6 | `src/shopline/export/csv_export.py` (new), `tests/test_csv_export.py` (new) | ~120 lines |
| 3 | none | `src/shopline/auth/tokens.py`, `tests/conftest.py`, `tests/test_tokens.py` | ~150 lines |
| 4 | 1, 2, 3 | `src/shopline/cli.py`, `tests/test_cli_export.py` (new) | ~200 lines |
| 5 | none | `pyproject.toml`, `src/shopline/cli.py`, `tests/test_since.py` (new) | ~40 lines |
| 6 | none | `src/shopline/i18n/messages_en.py`, `messages_id.py`, `messages_de.py` | 18 lines |
| 7 | 4, 5 | `docs/cli.md` | ~30 lines |

## Tasks

### Task 1: Export row model and JSON renderer

Create `src/shopline/export/rows.py` with exactly this code:

```python
import json
from dataclasses import dataclass
from datetime import timezone

from shopline.money import format_price

FIELDS = ("id", "created_at", "customer", "currency", "total", "status")


@dataclass(frozen=True)
class ExportRow:
    id: str
    created_at: str
    customer: str
    currency: str
    total: str
    status: str


def to_row(order) -> ExportRow:
    created = order.created_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return ExportRow(order.id, created, order.customer, order.currency,
                     format_price(order.total(), order.currency), order.status)


def render_json(rows) -> str:
    return json.dumps([{name: getattr(row, name) for name in FIELDS} for row in rows])
```

Add a `sample_orders` fixture to `tests/conftest.py` returning two `Order` objects (one
with a total of `1234.495`). In `tests/test_export_rows.py`, test that `render_json([])` is
`"[]"`, that the keys come out in `FIELDS` order, and that `created_at` ends in `Z`.

### Task 2: CSV renderer

Create `render_csv(rows, locale) -> str` in `src/shopline/export/csv_export.py`. The header
labels come from `shopline.i18n.get(locale, key)` for the six `export.header.*` keys
(Task 6). Use `csv.writer` with `lineterminator="\n"`. Acceptance:

- `render_csv([], "en")` is `"ID,Created (UTC),Customer,Currency,Total,Status\n"`.
- A row whose total is `1,234.50` is written as `"1,234.50"` (quoted).
- `render_csv(rows, "de")` uses the German labels from Task 6.

### Task 3: Signed download links

In `src/shopline/auth/tokens.py` add `sign_download(order_ids, expires_in: int = 600,
now=None) -> str` and `verify_download(token, now=None) -> list[str]`, following the format
of `sign_session`. Reuse the module's `LEEWAY_SECONDS` for expiry checks. Add a
`frozen_clock` fixture to `tests/conftest.py`. Tests in `tests/test_tokens.py`: round trip,
expired token rejected, tampered token rejected, token signed for other order ids rejected.

### Task 4: `export` CLI command

Add the `export` sub-command to `src/shopline/cli.py` as the spec describes: options,
defaults, JSON and CSV output through Tasks 1 and 2, `--link` through Task 3, and the
`--since` filter through `parse_since` (Task 5). Orders come from
`shopline.orders.load_all()`; add that function as a stub returning an empty list if it does
not exist yet. Tests in `tests/test_cli_export.py`: default JSON, CSV with `--locale id`,
`--link` prints only a URL, unknown format exits with code 2.

### Task 5: Shop-timezone `--since` parsing

Add `parse_since(text) -> datetime` to `src/shopline/cli.py`: parse `YYYY-MM-DD`, attach
`zoneinfo.ZoneInfo("Asia/Jakarta")` at 00:00, return it converted to UTC. Add
`tzdata; sys_platform == "win32"` to `dependencies` in `pyproject.toml`. Tests in
`tests/test_since.py`: `2026-11-24` becomes `2026-11-23T17:00:00+00:00`; an invalid date
exits with code 2.

### Task 6: Export header messages

Add these keys to the three catalogues:

| Key | en | id | de |
| --- | --- | --- | --- |
| `export.header.id` | ID | ID | ID |
| `export.header.created_at` | Created (UTC) | Dibuat (UTC) | Erstellt (UTC) |
| `export.header.customer` | Customer | Pelanggan | Kunde |
| `export.header.currency` | Currency | Mata uang | Währung |
| `export.header.total` | Total | Total | Summe |
| `export.header.status` | Status | Status | Status |

### Task 7: Document the export command

Add an "Exporting orders" section to `docs/cli.md` with the synopsis, the options and one
example per format and for `--link`.
