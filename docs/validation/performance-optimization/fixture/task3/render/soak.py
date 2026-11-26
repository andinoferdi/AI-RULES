import argparse
import random
import time
import tracemalloc

from .catalog import NAMES, STRINGS
from .templates import render


def main():
    parser = argparse.ArgumentParser(description="Replay a production-like request mix.")
    parser.add_argument("--requests", type=int, default=3000)
    args = parser.parse_args()
    rng = random.Random(7)
    locales = sorted(STRINGS)
    tracemalloc.start()
    start = time.perf_counter()
    step = max(1, args.requests // 5)
    for n in range(1, args.requests + 1):
        render(rng.choice(NAMES), rng.choice(locales),
               {"name": f"user{n % 500}", "item": n % 97, "amount": f"{n % 1000}.00"},
               request_id=f"req-{n:08d}")
        if n % step == 0 or n == args.requests:
            current, peak = tracemalloc.get_traced_memory()
            print(f"requests={n} elapsed_s={time.perf_counter() - start:.2f} "
                  f"traced_mb={current / 1e6:.1f} peak_mb={peak / 1e6:.1f}")


if __name__ == "__main__":
    main()
