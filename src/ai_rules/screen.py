"""Screen mode: the animated, short setup screen for interactive terminals.

Plain mode (logs, pipes, CI, ``--no-progress``, ``--non-interactive``) keeps the line output
the installer always printed; this module only draws for a person at a terminal.
"""
from __future__ import annotations

import functools
import os
import sys
import time
from dataclasses import dataclass, fields
from math import ceil
from typing import Callable, Mapping, Sequence

from rich.cells import cell_len
from rich.console import Console
from rich.control import Control
from rich.live import Live
from rich.segment import ControlType
from rich.text import Text

from ai_rules.banner import (_ASCII_ICON, ABU_TERANG, CHECK_STROKE, KUNYIT_TERANG, _display_path, _fit, compose,
                             mark_rows, render_banner)


@dataclass(frozen=True)
class Glyphs:
    active: str
    answered: str
    pointer: str
    ok: str
    fail: str
    manual: str
    full: str
    empty: str
    spinner: str
    sep: str


UNICODE = Glyphs("◆", "◇", "›", "✓", "✗", "!", "━", "─", "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏", " · ")
ASCII = Glyphs("*", "-", ">", "+", "x", "!", "#", "-", "|/-\\", ", ")
KUNYIT = KUNYIT_TERANG  # the only accent: lit check and done marks
UNLIT = ABU_TERANG  # the check before setup has proven its work
_GLYPH_TEXT = "".join(getattr(UNICODE, field.name) for field in fields(Glyphs)) + "▀▄█…"
INTRO_STEP = 0.06  # 8 frames: the A builds in under half a second
OUTRO_STEP = 0.09  # 5 frames: the check lands in under half a second
LABEL_WIDTH = 10  # `◇ Agents    ` keeps every answer value in one column
LANGUAGE_NAMES = {"id": "Bahasa Indonesia", "en": "English"}


@dataclass(frozen=True)
class Problem:
    """Something the owner must look at: kind is failed, blocked, skipped or manual."""
    kind: str
    where: str
    message: str


@dataclass(frozen=True)
class Result:
    """What the outro reports about a finished (or previewed) run."""
    seconds: float
    tally: Mapping[str, int]
    problems: tuple[Problem, ...]
    verified: bool | None  # True: final verification passed; False: it failed; None: nothing applied
    commands: tuple[str, ...]  # first-party skill ids, plan order
    prefix: str  # "$" when Codex is the only agent, else "/"
    codex_note: bool  # add "(Codex uses $)"
    backups: str | None  # shown when this run replaced files


def _guarded(method):
    """Drawing is decoration: a failure marks the screen broken instead of stopping setup.

    The method returns True when it drew, False when the caller should fall back to plain text.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.broken:
            return False
        try:
            method(self, *args, **kwargs)
        except Exception:
            self.broken = True
            return False
        return True
    return wrapper


class Screen:
    def __init__(self, console: Console, *, glyphs: Glyphs, color: bool,
                 sleep: Callable[[float], None] = time.sleep):
        self.console = console
        self.glyphs = glyphs
        self.color = color
        self.unicode = glyphs is UNICODE
        self.sleep = sleep
        self.broken = False

    @_guarded
    def intro(self, info) -> None:
        """The banner, with the A building from the bottom and the check still unlit."""
        width = self.console.width
        if not self.unicode or width < 40:
            self.console.print(Text.from_ansi(render_banner(info, width, color=self.color,
                                                            unicode=self.unicode, lit=0)))
            return
        with Live(console=self.console, auto_refresh=False, transient=False) as live:
            for built in range(1, 9):
                frame = render_banner(info, width, color=self.color, built=built, lit=0)
                live.update(Text.from_ansi(frame), refresh=True)
                self.sleep(INTRO_STEP)
        self.console.line()

    def _answer_line(self, label: str, value: str) -> None:
        line = Text(f"{self.glyphs.answered} ", style="dim")
        line.append(label.ljust(LABEL_WIDTH), style="dim")
        line.append(value)
        self.console.print(line)

    @_guarded
    def answer(self, label: str, value: str) -> None:
        """One folded answer: `◇ Agents    Codex, Claude Code`."""
        self._answer_line(label, value)

    @_guarded
    def rewrite_answer(self, label: str, value: str, *, rows: int = 1) -> None:
        """Replace the prompt's own answered line(s), just above the cursor, with a folded answer."""
        controls = []
        for _ in range(max(1, rows)):
            controls += [Control.move(0, -1), Control((ControlType.ERASE_IN_LINE, 2))]
        self.console.control(*controls, Control.move_to_column(0))
        self._answer_line(label, value)

    @_guarded
    def note(self, text: str) -> None:
        self._note(text)

    def _note(self, text: str) -> None:
        self.console.print(Text(f"  {text}", style="dim"))

    def _issue(self, kind: str, where: str, text: str) -> None:
        mark = self.glyphs.manual if kind == "manual" else self.glyphs.fail
        line = Text(f"  {mark} ")
        line.append(where, style="bold")
        line.append(f"  {text}" if text else "")
        self.console.print(line)  # long messages wrap; they are never cut

    @_guarded
    def plan(self, plan, catalog, defaults=None) -> None:
        """`◆ Plan  5 to update · 35 current`, then only what needs a look before saying yes."""
        from ai_rules.planning.renderer import count_backups, plan_issues, plan_summary

        head = Text(f"{self.glyphs.active} ", style="bold")
        head.append("Plan".ljust(LABEL_WIDTH), style="bold")
        head.append(plan_summary(plan, sep=self.glyphs.sep))
        self.console.line()
        self.console.print(head)
        issues = []
        if defaults:
            summary, issues = defaults_summary(defaults, sep=self.glyphs.sep)
            self._note(f"Instruction files  {summary}")
        for kind, where, text in [*issues, *plan_issues(plan, catalog)]:
            self._issue(kind, where, text)
        if count_backups(plan, catalog):
            self._note("Backups are kept for files that get replaced")

    @_guarded
    def outro(self, result: Result) -> None:
        """The mark again with the result beside it; the check lights up only after a verified run."""
        trouble = bool(result.problems) or any(result.tally.get(key, 0) for key in TROUBLE_KEYS)
        ok = result.verified is True and not trouble
        width = self.console.width
        beside = self._outro_lines(result, ok)
        ellipsis = "…" if self.unicode else "..."
        if width < 40:
            self.console.line()
            for line in beside:
                if line:
                    self.console.print(Text.from_ansi(_fit(line, width, ellipsis, self.color)))
        elif ok and self.unicode:
            with Live(console=self.console, auto_refresh=False, transient=False) as live:
                for lit in range(1, len(CHECK_STROKE) + 1):
                    frame = compose(mark_rows(color=self.color, lit=lit), beside, width,
                                    color=self.color, ellipsis=ellipsis)
                    live.update(Text.from_ansi(frame), refresh=True)
                    self.sleep(OUTRO_STEP)
        else:
            rows = mark_rows(color=self.color, lit=0) if self.unicode else list(_ASCII_ICON)
            self.console.print(Text.from_ansi(compose(rows, beside, width, color=self.color, ellipsis=ellipsis)))
        for problem in result.problems:
            self._issue(problem.kind, problem.where, problem.message)
        if result.verified is True:
            self._note(f"Files verified{self.glyphs.sep}skill loading is not checked by setup")
        if result.backups:
            self._note(f"Backups: {result.backups}")

    def _outro_lines(self, result: Result, ok: bool) -> list[list[tuple[str, str]]]:
        """Up to four lines beside the mark, as (text, ANSI style) segments for `compose`."""
        glyphs, sep, took = self.glyphs, self.glyphs.sep, f"{result.seconds:.1f}s"
        if ok:
            total = sum(result.tally.values())
            title = "Up to date" if total and result.tally.get("current", 0) == total else "Done"
            return [
                [(f"{glyphs.ok} ", _KUNYIT_SGR), (f"{title} in {took}", _BOLD)],
                [(_tally_text(result.tally, sep, ok=True), "")],
                [("Next: open a new agent session or reload its window", "")],
                [(_try_line(result, self.console.width - 15), _DIM)],
            ]
        if result.verified is None:
            return [
                [(f"Preview only{sep}nothing changed", _BOLD)],
                [(_tally_text(result.tally, sep, ok=False), "")],
                [("Next: add --yes to apply", "")],
            ]
        return [
            [(f"{glyphs.fail} {_tally_text(result.tally, sep, ok=False) or 'Setup did not finish'}", _BOLD)],
            [(f"Finished in {took}", _DIM)],
            [("Next: fix the items below, then run andino setup again", "")],
        ]

    def prompt_rows(self, message: str, shown: str) -> int:
        """Terminal rows questionary's answered line takes: `<qmark> <message> <answer>`."""
        width = max(1, self.console.width)
        return max(1, ceil(cell_len(f"{self.glyphs.active} {message} {shown}") / width))

    def question_style(self):
        import questionary

        hint = "fg:ansibrightblack"
        return questionary.Style([
            ("qmark", "bold"), ("question", "bold"), ("answer", "bold"), ("pointer", "bold"),
            ("highlighted", "bold"), ("selected", ""), ("instruction", hint), ("separator", hint),
            ("text", ""), ("disabled", f"{hint} italic"),
        ])


TALLY_ORDER = ("failed", "blocked", "manual", "skipped", "installed", "updated", "repaired",
               "reconfigured", "adopted", "replaced", "downgraded", "current")
TROUBLE_KEYS = ("failed", "blocked", "manual", "skipped")
_BOLD, _DIM = "\x1b[1m", "\x1b[2m"
_KUNYIT_SGR = "\x1b[38;2;{};{};{}m".format(*KUNYIT)


def _tally_text(tally: Mapping[str, int], sep: str, *, ok: bool) -> str:
    """`1 failed · 4 updated · 35 current`; trouble first, `already current` after a clean run."""
    return sep.join(f"{tally[key]} {'already current' if ok and key == 'current' else key}"
                    for key in TALLY_ORDER if tally.get(key, 0))


def _try_line(result: Result, room: int) -> str:
    """`Try: /focus /search-first +6 more (Codex uses $)`, as many commands as fit in `room`."""
    names = [result.prefix + name for name in result.commands]
    if not names:
        return ""
    suffix = " (Codex uses $)" if result.codex_note else ""
    for keep in range(len(names), 0, -1):
        more = f" +{len(names) - keep} more" if keep < len(names) else ""
        text = f"Try: {' '.join(names[:keep])}{more}{suffix}"
        if cell_len(text) <= room:
            return text
    return text  # the shortest form; the layout cuts it with an ellipsis


DEFAULTS_WORDS = (("INSTALL", "to add"), ("UPDATE", "to update"), ("REPLACE", "to replace"),
                  ("ADOPT", "to adopt"), ("CURRENT", "current"), ("CONFLICT", "conflict"), ("FAILED", "failed"))


def defaults_summary(results, *, sep: str = " · ") -> tuple[str, list[tuple[str, str, str]]]:
    """`1 to update · 3 current` for the instruction files, plus each conflict or failure."""
    counts = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    words = dict(DEFAULTS_WORDS)
    known = [f"{counts[status]} {word}" for status, word in DEFAULTS_WORDS if counts.get(status)]
    other = [f"{count} {status.lower()}" for status, count in counts.items() if status not in words]
    # A conflict needs --replace-agent-defaults, so it is the owner's manual step.
    issues = [("manual" if result.status == "CONFLICT" else "failed", _display_path(result.path), result.message)
              for result in results if result.status in {"CONFLICT", "FAILED"}]
    return sep.join(known + other), issues


def fit_names(names: Sequence[str], room: int) -> str:
    """Whole names that fit in `room` cells, then `+N` for the rest, or `<n> selected`."""
    names = list(names)
    text = ", ".join(names)
    if cell_len(text) <= room:
        return text
    for keep in range(len(names) - 1, 0, -1):
        candidate = ", ".join(names[:keep]) + f" +{len(names) - keep}"
        if cell_len(candidate) <= room:
            return candidate
    return f"{len(names)} selected"


def _encodes(stream, text: str) -> bool:
    try:
        text.encode(getattr(stream, "encoding", None) or "utf-8")
    except (UnicodeEncodeError, LookupError):
        return False
    return True


def detect_screen(*, interactive: bool, progress: bool, stream=None,
                  environ: Mapping[str, str] | None = None) -> Screen | None:
    """A screen for a person at a capable terminal, or None for plain output."""
    stream = sys.stdout if stream is None else stream
    environ = os.environ if environ is None else environ
    if not interactive or not progress:
        return None
    try:
        if not stream.isatty():
            return None
    except Exception:
        return None
    if environ.get("CI") or environ.get("TERM") in {"dumb", "unknown"}:
        return None
    color = "NO_COLOR" not in environ
    # Only the real stdout can be a legacy Windows console; any other stream is ours.
    console = Console(file=stream, highlight=False, markup=False, no_color=not color,
                      legacy_windows=None if stream is sys.__stdout__ else False)
    if console.legacy_windows:
        return None  # no cursor movement, so no animation or folded answers
    return Screen(console, glyphs=UNICODE if _encodes(stream, _GLYPH_TEXT) else ASCII, color=color)
