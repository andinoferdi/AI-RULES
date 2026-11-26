"""Write the page images to img/ (plain PNG, standard library only)."""
import random
import struct
import zlib
from pathlib import Path


def png(path, width, height, colours, seed):
    rng = random.Random(seed)
    palette = [bytes(rng.randrange(256) for _ in range(3)) for _ in range(colours)]
    rows = bytearray()
    for _ in range(height):
        rows.append(0)
        for _ in range(width):
            rows += palette[rng.randrange(colours)]
    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                     + chunk(b"IDAT", zlib.compress(bytes(rows), 6)) + chunk(b"IEND", b""))


def main():
    out = Path(__file__).resolve().parent.parent / "img"
    out.mkdir(exist_ok=True)
    png(out / "hero.png", 1600, 900, 48, 1)
    for n in (1, 2, 3):
        png(out / f"team-{n}.png", 480, 480, 6, 10 + n)
    for path in sorted(out.iterdir()):
        print(f"{path.name} {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
