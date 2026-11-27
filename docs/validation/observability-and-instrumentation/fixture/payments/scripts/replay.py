"""Simulates POST /invoices/{id}/replay as the web framework would call it."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from payments.api import handle_replay  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("invoice_id")
parser.add_argument("--request-id")
parser.add_argument("--traceparent")
args = parser.parse_args()

headers = {}
if args.request_id:
    headers["x-request-id"] = args.request_id
if args.traceparent:
    headers["traceparent"] = args.traceparent
status, body = handle_replay(headers, args.invoice_id)
print(status, body)
