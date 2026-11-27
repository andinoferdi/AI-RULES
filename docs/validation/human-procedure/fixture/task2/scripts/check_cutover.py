"""Check that https://billing.acme-pay.example answers from Nimbus and is healthy.

Prints `cutover ok` and exits 0, or names the failing check and exits 1.
"""
import sys
import urllib.request

BASE = "https://billing.acme-pay.example"


def get(path: str) -> tuple:
    try:
        with urllib.request.urlopen(BASE + path, timeout=10) as response:
            return response.status, response.read().decode("utf-8", "replace").strip()
    except Exception as error:  # noqa: BLE001 - report any failure as a failed check
        return None, str(error)


def main() -> int:
    status, body = get("/version")
    if status != 200 or "host=nimbus" not in body:
        print(f"not on Nimbus yet: /version -> {status} {body[:80]}")
        return 1
    status, body = get("/healthz")
    if status != 200 or body != "ok":
        print(f"unhealthy: /healthz -> {status} {body[:80]}")
        return 1
    print("cutover ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
