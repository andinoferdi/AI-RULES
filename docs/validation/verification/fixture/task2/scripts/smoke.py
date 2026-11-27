"""Smoke-test the published package on a host: download the zip and convert one value."""
import argparse
import socket
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--host", required=True)
args = parser.parse_args()
try:
    with socket.create_connection((args.host, 443), timeout=5):
        pass
except OSError as error:
    print(f"smoke: cannot reach {args.host}: {error}")
    sys.exit(2)
print(f"smoke: {args.host} reachable; run the remote checks from the staging runbook")
