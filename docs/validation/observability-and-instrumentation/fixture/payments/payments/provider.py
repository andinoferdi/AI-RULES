"""Payment provider client. This copy is a fake that follows data/provider_script.json."""
import json
import os
import time

from payments.paths import ROOT
from payments.telemetry.log import logger

SCRIPT = json.loads((ROOT / "data" / "provider_script.json").read_text(encoding="utf-8"))
API_KEY = os.environ.get("PAYMENTS_API_KEY", "pay_test_local_only")


class ProviderTimeout(Exception):
    retryable = True


class CardDeclined(Exception):
    retryable = False


_attempts = {}


def charge(invoice):
    payload = {"invoice": invoice["id"], "amount": invoice["amount"],
               "card_token": invoice["card_token"], "email": invoice["customer_email"]}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    if os.environ.get("PAYMENTS_LOG_BODIES") == "1":
        logger.info("provider_request", body=payload, headers=headers)
    else:
        logger.debug("provider_request", body=payload, headers=headers)

    n = _attempts.get(invoice["id"], 0)
    _attempts[invoice["id"]] = n + 1
    outcomes = SCRIPT.get(invoice["id"], ["ok"])
    outcome = outcomes[min(n, len(outcomes) - 1)]
    if outcome == "timeout":
        time.sleep(0.03)
        raise ProviderTimeout("provider did not answer within 30s")
    time.sleep(0.01)
    if outcome == "declined":
        raise CardDeclined("card_declined: insufficient_funds")
    return {"charge_id": f"ch_{invoice['id']}_{n + 1}"}
