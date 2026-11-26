"""Generate the primary feed and a partner feed of the size the partner sends (deterministic)."""
import argparse
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ["S", "M", "L", "XL"]
WORDS = ["Kaos", "Kemeja", "Celana", "Jaket", "Topi", "Tas", "Sepatu", "Sandal", "Batik", "Sarung"]


def write(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("sku,name,variant,price\n")
        for sku, name, variant, price in rows:
            handle.write(f"{sku},{name},{variant},{price}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary-rows", type=int, default=2000)
    parser.add_argument("--partner-rows", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    rng = random.Random(args.seed)

    primary = []
    for index in range(args.primary_rows):
        sku = f"AND-{index // 4:05d}"
        primary.append((sku, f"{rng.choice(WORDS)} {index}", VARIANTS[index % 4],
                        rng.randrange(50, 900) * 1000))

    partner = []
    for index in range(args.partner_rows):
        roll = rng.random()
        if roll < 0.05:  # the partner also lists some of our products, in its own casing
            sku, _, variant, _ = rng.choice(primary)
            sku = sku.lower()
        elif roll < 0.08 and partner:  # and repeats some of its own rows
            sku, _, variant, _ = rng.choice(partner)
        else:
            sku, variant = f"PTR-{index:06d}", rng.choice(VARIANTS)
        partner.append((sku, f"{rng.choice(WORDS)} {rng.choice(WORDS)}", variant,
                        rng.randrange(40, 800) * 1000))

    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    write(data / "primary.csv", primary)
    write(data / "feed-big.csv", partner)
    print(f"wrote data/primary.csv ({len(primary)} rows) and data/feed-big.csv ({len(partner)} rows)")


if __name__ == "__main__":
    main()
