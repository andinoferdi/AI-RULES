from __future__ import annotations

import os
import shutil
import sys


_GLYPHS = {
    "A": ("01110", "11011", "11111", "11011", "11011"),
    "N": ("11001", "11101", "11111", "11011", "11001"),
    "D": ("11110", "11011", "11011", "11011", "11110"),
    "I": ("11111", "00100", "00100", "00100", "11111"),
    "O": ("01110", "11011", "11011", "11011", "01110"),
    "R": ("11110", "11011", "11110", "11011", "11011"),
    "U": ("11011", "11011", "11011", "11011", "01110"),
    "L": ("11000", "11000", "11000", "11000", "11111"),
    "E": ("11111", "11000", "11110", "11000", "11111"),
    "S": ("01111", "11000", "01110", "00011", "11110"),
    " ": ("000",) * 5,
}


def render_banner(width: int, *, color: bool = True, block: str = "█") -> str:
    words = ("ANDINO AI RULES",) if width >= 88 else ("ANDINO", "AI RULES")
    if width < 48:
        return "ANDINO AI RULES\n"
    lines = []
    for word in words:
        for row in range(5):
            pixels = "0".join(_GLYPHS[letter][row] for letter in word)
            line = ""
            for column, pixel in enumerate(pixels):
                if pixel == "0":
                    line += " "
                    continue
                if color:
                    t = column / max(1, len(pixels) - 1)
                    red, green, blue = (round(a + (b - a) * t) for a, b in zip((174, 20, 38), (255, 130, 40)))
                    line += f"\x1b[38;2;{red};{green};{blue}m"
                line += block
            lines.append("  " + line.rstrip() + ("\x1b[0m" if color else ""))
        lines.append("")
    return "\n" + "\n".join(lines) + "\n"


def print_setup_banner() -> None:
    if not sys.stdout.isatty() or os.environ.get("TERM") == "dumb":
        return
    from prompt_toolkit import ANSI, print_formatted_text
    from prompt_toolkit.output import ColorDepth

    block = "█"
    try:
        block.encode(sys.stdout.encoding or "utf-8")
    except UnicodeEncodeError:
        block = "#"
    banner = render_banner(
        shutil.get_terminal_size().columns,
        color=not bool(os.environ.get("NO_COLOR")),
        block=block,
    )
    print_formatted_text(ANSI(banner), color_depth=ColorDepth.TRUE_COLOR)
