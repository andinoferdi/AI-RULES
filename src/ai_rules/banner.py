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


# Andes peak that doubles as an "A": S is snow, # is rock; two pixel rows per text row.
_ICON = (
    "....SS....",
    "...SSSS...",
    "...####...",
    "..######..",
    "..##..##..",
    ".########.",
    ".##....##.",
    "###....###",
)
_SNOW = (215, 222, 232)
_TOP, _BOTTOM = (255, 130, 40), (174, 20, 38)
_ASCII_ICON = ("   /\\     ", "  /  \\    ", " / /\\ \\   ", "/_/  \\_\\  ")
_BOLD, _DIM, _RESET = "\x1b[1m", "\x1b[2m", "\x1b[0m"
_ICON_WIDTH = len(_ICON[0])
_INDENT, _GAP = "  ", "   "


def _pixel_color(row: int, column: int) -> tuple[int, int, int] | None:
    pixel = _ICON[row][column]
    if pixel == ".":
        return None
    if pixel == "S":
        return _SNOW
    t = (row - 2) / (len(_ICON) - 3)
    return tuple(round(a + (b - a) * t) for a, b in zip(_TOP, _BOTTOM))


def _icon_rows(color: bool) -> list[str]:
    rows = []
    for top_row in range(0, len(_ICON), 2):
        cells = []
        for column in range(_ICON_WIDTH):
            top = _pixel_color(top_row, column)
            bottom = _pixel_color(top_row + 1, column)
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


def render_banner(info: BannerInfo, width: int, *, color: bool = True, unicode: bool = True) -> str:
    sep = " · " if unicode else ", "
    ellipsis = "…" if unicode else "..."
    if width < 40:
        title = [("Andino AI Rules", _BOLD), (f" v{info.version}{sep}{info.command}", "")]
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
        [("Andino AI Rules", _BOLD), (f" v{info.version}", _DIM)],
        [(f"ai-rules {info.command}", _DIM)],
        [(tools, "")],
        [(_fit_path(info.cwd, limit, ellipsis), _DIM)],
    ]
    icon = _icon_rows(color) if unicode else list(_ASCII_ICON)
    rows = [
        (_INDENT + cell_row + _GAP + _fit(line, limit, ellipsis, color)).rstrip()
        for cell_row, line in zip(icon, lines)
    ]
    return "\n" + "\n".join(rows) + "\n"


def _display_path(path: Path) -> str:
    try:
        relative = path.relative_to(Path.home())
    except ValueError:
        return str(path)
    return "~" if relative == Path(".") else f"~{os.sep}{relative}"


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
    return BannerInfo(__version__, command, tuple(found), tuple(missing), _display_path(Path.cwd()))


def print_setup_banner(command: str = "setup") -> None:
    if not sys.stdout.isatty() or os.environ.get("TERM") == "dumb":
        return
    from prompt_toolkit import ANSI, print_formatted_text
    from ai_rules import __version__

    try:
        "▀▄█·…".encode(sys.stdout.encoding or "utf-8")
        unicode = True
    except UnicodeEncodeError:
        unicode = False
    try:
        info = collect_banner_info(command)
    except Exception:
        # The banner is decoration; detection trouble must never stop setup.
        info = BannerInfo(__version__, command, (), (), _display_path(Path.cwd()))
    print_formatted_text(ANSI(render_banner(
        info,
        shutil.get_terminal_size().columns,
        color="NO_COLOR" not in os.environ,
        unicode=unicode,
    )))
