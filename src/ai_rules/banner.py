from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BannerInfo:
    version: str
    command: str
    tools_found: tuple[str, ...]
    tools_missing: tuple[str, ...]
    cwd: str
    program: str = "andino"


BRAND = "Andino Skills"

# The Andino Skills mark: an "A" whose crossbar is a check mark (see docs/brand).
# A is the letter, K is the check; two pixel rows per text row.
_ICON = (
    "....AA....",
    "...AAAA...",
    "...A..A...",
    "..AA...K..",
    "..AA..KA..",
    ".AAK.K.AA.",
    ".AA.K..AA.",
    "AA......AA",
)
KERTAS, KUNYIT_TERANG, ABU_TERANG = (240, 243, 246), (245, 165, 36), (154, 164, 178)
_COLORS = {"A": KERTAS, "K": KUNYIT_TERANG}
_ASCII_ICON = ("   /\\     ", "  /  \\    ", " / \\/ \\   ", "/      \\  ")
_BOLD, _DIM, _RESET = "\x1b[1m", "\x1b[2m", "\x1b[0m"
_ICON_WIDTH = len(_ICON[0])
_INDENT, _GAP = "  ", "   "


CHECK_STROKE = ((5, 3), (6, 4), (5, 5), (4, 6), (3, 7))  # check cells (row, column) in drawing order


def mark_rows(*, color: bool, built: int = 8, lit: int = 5) -> list[str]:
    """The mark with its lowest `built` pixel rows drawn and the first `lit` check cells lit.

    An unlit check cell is Abu Terang in colour and left out without colour, so the check
    appears only once setup has proven its work.
    """
    first = len(_ICON) - max(0, min(built, len(_ICON)))
    lit_cells = set(CHECK_STROKE[:max(0, lit)])

    def pixel(row: int, column: int) -> tuple[int, int, int] | None:
        kind = _ICON[row][column]
        if row < first:
            return None
        if kind == "K" and (row, column) not in lit_cells:
            return ABU_TERANG if color else None
        return _COLORS.get(kind)

    rows = []
    for top_row in range(0, len(_ICON), 2):
        cells = []
        for column in range(_ICON_WIDTH):
            top = pixel(top_row, column)
            bottom = pixel(top_row + 1, column)
            if top is None and bottom is None:
                cells.append(" ")
                continue
            background = None
            if top is not None and bottom is not None:
                # Two colors in one cell need ▀ with a background; plain mode has one color.
                glyph, foreground = ("█", top) if top == bottom or not color else ("▀", top)
                background = None if glyph == "█" else bottom
            elif top is not None:
                glyph, foreground = "▀", top
            else:
                glyph, foreground = "▄", bottom
            if not color:
                cells.append(glyph)
                continue
            prefix = "\x1b[38;2;{};{};{}m".format(*foreground)
            if background is not None:
                prefix += "\x1b[48;2;{};{};{}m".format(*background)
            cells.append(prefix + glyph + _RESET)
        rows.append("".join(cells))
    return rows


def _fit(segments: list[tuple[str, str]], limit: int, ellipsis: str, color: bool) -> str:
    total = sum(len(text) for text, _ in segments)
    if total > limit:
        budget, kept = max(0, limit - len(ellipsis)), []
        for text, style in segments:
            kept.append((text[:budget], style))
            budget -= len(kept[-1][0])
        kept.append((ellipsis, segments[-1][1]))
        segments = kept
    return "".join(f"{style}{text}{_RESET}" if color and style else text for text, style in segments if text)


def _fit_path(path: str, limit: int, ellipsis: str) -> str:
    if len(path) <= limit:
        return path
    return ellipsis + path[len(path) - max(0, limit - len(ellipsis)):]


def render_banner(info: BannerInfo, width: int, *, color: bool = True, unicode: bool = True,
                  built: int = 8, lit: int = 5) -> str:
    sep = " · " if unicode else ", "
    ellipsis = "…" if unicode else "..."
    if width < 40:
        title = [(BRAND, _BOLD), (f" v{info.version}{sep}{info.command}", "")]
        return "\n" + _INDENT + _fit(title, width - len(_INDENT), ellipsis, color) + "\n"

    if info.tools_found:
        tools = f"AI tools: {sep.join(info.tools_found)}"
        if info.tools_missing:
            tools += f"{sep}{len(info.tools_missing)} not on PATH"
    elif info.tools_missing:
        tools = "AI tools: none on PATH"
    else:
        tools = "AI tools: not checked"
    limit = width - len(_INDENT) - _ICON_WIDTH - len(_GAP)
    lines = [
        [(BRAND, _BOLD), (f" v{info.version}", _DIM)],
        [(f"{info.program} {info.command}", _DIM)],
        [(tools, "")],
        [(_fit_path(info.cwd, limit, ellipsis), _DIM)],
    ]
    icon = mark_rows(color=color, built=built, lit=lit) if unicode else list(_ASCII_ICON)
    return compose(icon, lines, width, color=color, ellipsis=ellipsis)


def compose(rows: list[str], lines: list[list[tuple[str, str]]], width: int, *, color: bool, ellipsis: str) -> str:
    """The mark's rows, each with one fitted line of (text, ANSI style) segments beside it."""
    limit = width - len(_INDENT) - _ICON_WIDTH - len(_GAP)
    lines = list(lines) + [[] for _ in range(len(rows) - len(lines))]
    composed = [
        (_INDENT + cell_row + _GAP + _fit(line, limit, ellipsis, color)).rstrip()
        for cell_row, line in zip(rows, lines)
    ]
    return "\n" + "\n".join(composed) + "\n"


def _display_path(path: Path) -> str:
    try:
        relative = path.relative_to(Path.home())
    except ValueError:
        return str(path)
    return "~" if relative == Path(".") else f"~{os.sep}{relative}"


def _program_name() -> str:
    """The command the user typed: `andino`, `ai-rules` or a release binary name."""
    name = Path(sys.argv[0]).stem if sys.argv and sys.argv[0] else ""
    return name if name.startswith(("andino", "ai-rules")) else "andino"


def collect_banner_info(command: str = "setup") -> BannerInfo:
    from ai_rules import __version__
    from ai_rules.catalog import load_catalog
    from ai_rules.domain.statuses import DetectionStatus
    from ai_rules.hosts.adapters import HOST_COMMANDS, build_host_adapters

    found, missing = [], []
    for host_id, adapter in build_host_adapters(load_catalog().hosts).items():
        if host_id not in HOST_COMMANDS:
            continue  # no PATH probe exists for this host, so "not on PATH" would be a guess
        target = found if adapter.detect().status == DetectionStatus.PRESENT else missing
        target.append(adapter.host.display_name)
    return BannerInfo(__version__, command, tuple(found), tuple(missing), _display_path(Path.cwd()),
                      _program_name())


def print_setup_banner(command: str = "setup", *, screen=None) -> None:
    """Screen mode plays the intro; otherwise a terminal gets today's static banner."""
    if screen is None and (not sys.stdout.isatty() or os.environ.get("TERM") == "dumb"):
        return
    from prompt_toolkit import ANSI, print_formatted_text
    from ai_rules import __version__

    try:
        info = collect_banner_info(command)
    except Exception:
        # The banner is decoration; detection trouble must never stop setup.
        info = BannerInfo(__version__, command, (), (), _display_path(Path.cwd()), _program_name())
    if screen is not None and screen.intro(info):
        return
    try:
        "▀▄█·…".encode(sys.stdout.encoding or "utf-8")
        unicode = True
    except UnicodeEncodeError:
        unicode = False
    print_formatted_text(ANSI(render_banner(
        info,
        shutil.get_terminal_size().columns,
        color="NO_COLOR" not in os.environ,
        unicode=unicode,
    )))
