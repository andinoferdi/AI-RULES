import time

from retrykit.policy import backoff


def call_with_retry(fn, attempts=5, sleep=time.sleep):
    for attempt in range(attempts):
        try:
            return fn()
        except ConnectionError:
            if attempt == attempts - 1:
                raise
            sleep(backoff(attempt))
