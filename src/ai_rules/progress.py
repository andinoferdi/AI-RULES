"""Optional work events and a terminal presenter; installers need no console."""
from collections import Counter
from dataclasses import replace
import os
import sys
from time import monotonic

from rich.console import Console, Group
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from ai_rules.events import WorkEvent
from ai_rules.screen import KUNYIT

# Screen mode's status line: what happens to the target being worked on.
VERB = {"INSTALL": "Installing", "UPDATE": "Updating", "NO_OP": "Checking", "REPAIR": "Repairing",
        "RECONFIGURE": "Reconfiguring", "ADOPT": "Adopting", "REPLACE": "Replacing",
        "DOWNGRADE": "Downgrading", "MANUAL_ACTION": "Checking", "BLOCK": "Skipping"}
TROUBLE = {"FAILED", "BLOCKED", "MANUAL_ACTION_REQUIRED", "SKIPPED"}
BAR_CELLS = 18


class SetupProgress:
    def __init__(self, *, console: Console | None = None, enabled: bool = True, verbose: bool = False,
                 screen=None):
        self.screen = screen
        if console is None and screen is not None:
            console = screen.console
        terminal = sys.stdout.isatty() and os.environ.get("TERM") not in {"dumb", "unknown"}
        self.console = console or Console(highlight=False, markup=False,
                                          force_terminal=None if terminal else False,
                                          color_system="auto" if terminal else None)
        if "NO_COLOR" in os.environ:
            self.console.no_color = True
        self.dynamic = (enabled and self.console.is_terminal and not self.console.is_dumb_terminal
                        and os.environ.get("TERM") not in {"dumb", "unknown"} and not os.environ.get("CI"))
        self.verbose = verbose
        self.started = monotonic()
        self._worked = 0.0  # seconds spent inside `with progress:` blocks
        self._entered = None
        self.event = WorkEvent("Preparing setup")
        self.counts = Counter()
        self.actions = Counter()
        self.total = 0
        self.processed = 0
        self.running = False
        self.spinner = Spinner("dots", style="dark_orange")
        self.live = None
        self.last_phase = None
        self.active_host = ""
        self.active_capability = ""
        self.active_action = ""
        self.outcomes = {}
        self.executing = False
        self.last_work_phase = ""
        self.hosts: list[tuple[str, str, int]] = []
        self.host_done = Counter()
        self.host_trouble: set[str] = set()

    def expect(self, hosts) -> None:
        """Screen mode: the agents in plan order as (host id, display name, target count)."""
        self.hosts = [(host_id, name, total) for host_id, name, total in hosts]

    def elapsed(self) -> float:
        """Work time only: reading the plan and answering questions between blocks do not count."""
        running = monotonic() - self._entered if self._entered is not None else 0.0
        return self._worked + running

    def tally(self) -> dict[str, int]:
        return {
            "installed": self.actions["INSTALL"], "updated": self.actions["UPDATE"],
            "repaired": self.actions["REPAIR"], "reconfigured": self.actions["RECONFIGURE"],
            "adopted": self.actions["ADOPT"], "replaced": self.actions["REPLACE"],
            "downgraded": self.actions["DOWNGRADE"], "current": self.counts["CURRENT"],
            "failed": self.counts["FAILED"], "blocked": self.counts["BLOCKED"],
            "manual": self.counts["MANUAL_ACTION_REQUIRED"], "skipped": self.counts["SKIPPED"],
        }

    def __enter__(self):
        self._entered = monotonic()
        if self.dynamic:
            self.live = Live(console=self.console, get_renderable=self.render,
                             refresh_per_second=12 if self.screen is not None else 8, transient=True)
            self.live.start(refresh=True)
        return self

    def __call__(self, event: WorkEvent):
        if event.kind == "target_start":
            self.active_host, self.active_capability, self.active_action = event.host, event.capability, event.action
            self.last_work_phase = event.phase
        if self.running and event.kind == "phase":
            self.last_work_phase = event.phase
            event = replace(event, host=event.host or self.active_host,
                            capability=event.capability or self.active_capability,
                            action=event.action or self.active_action)
        self.event = event
        if event.kind == "execution":
            self.executing = True
            self.total = event.total or 0
        elif event.kind == "target_start":
            self.running = True
        elif event.kind == "target_done":
            self.processed += 1
            self.running = False
            self.counts[event.status] += 1
            self.outcomes[(event.host, event.capability)] = (event.status, event.action)
            self.host_done[event.host] += 1
            if event.status in TROUBLE:
                self.host_trouble.add(event.host)
            if event.status == "APPLIED":
                self.actions[event.action] += 1
        elif event.kind == "verification_failed":
            self.host_trouble.add(event.host)
            key = (event.host, event.capability)
            previous, action = self.outcomes.get(key, ("", ""))
            if previous != "FAILED":
                if previous:
                    self.counts[previous] -= 1
                if previous == "APPLIED":
                    self.actions[action] -= 1
                self.counts["FAILED"] += 1
                self.outcomes[key] = ("FAILED", action)
        if event.kind in {"diagnostic", "verification_failed"}:
            if self.screen is not None:
                where = " / ".join(v for v in (self._name(event.host), event.capability) if v)
                self.console.print(Text(f"  {self.screen.glyphs.fail} {where}: {event.detail}"))
                return
            phase = f" (during {self.last_work_phase})" if event.phase == "Operation failed" else ""
            self.console.print(f"{self.line(event)}{phase}: {event.detail}")
            return
        if self.screen is not None:
            if self.live:
                self.live.refresh()
            return
        if not self.dynamic:
            if (event.kind in {"execution", "target_done"}
                    or (event.phase != self.last_phase and (not self.total or self.verbose))):
                self.console.print(self.line(event))
                self.last_phase = event.phase
        elif self.live:
            self.live.update(self.render())

    def line(self, event):
        target = " / ".join(v for v in (event.host, event.capability) if v)
        count = (f"{self.processed}/{self.total} targets | "
                 if event.kind == "target_done" else "")
        outcome = ("VERIFIED NO_OP (current)" if event.status == "CURRENT"
                   else " ".join(v for v in (event.status, event.action) if v))
        units = (f" | {event.completed} / {event.total}" if event.kind != "target_done"
                 and event.completed is not None and event.total is not None else "")
        phase = "" if event.kind == "target_done" else event.phase + " | "
        return f"{count}{phase}{target}".rstrip(" |") + (f" | {outcome}" if outcome else "") + units

    def render(self):
        if self.screen is not None:
            return self._render_screen()
        elapsed = self.elapsed()
        lines = [Text(self.line(self.event), overflow="ellipsis", no_wrap=True)]
        if self.total:
            pending = max(0, self.total - self.processed - int(self.running))
            lines.append(Text(f"{self.processed} / {self.total} targets processed | {int(self.running)} running | {pending} pending"))
            lines.append(Text(" | ".join(f"{n} {s.lower()}" for s, n in self.counts.copy().items())))
        self.spinner.update(text=Text(f"{self.event.phase} | {elapsed:.1f}s elapsed", overflow="ellipsis", no_wrap=True))
        return Group(*lines, self.spinner)

    def _name(self, host_id: str) -> str:
        return next((name for known, name, _ in self.hosts if known == host_id), host_id)

    def _render_screen(self):
        """One bar per agent while applying, then a spinner line with what happens now."""
        glyphs = self.screen.glyphs
        lines = []
        if self.hosts and self.executing:
            name_width = max(len(name) for _, name, _ in self.hosts)
            for host_id, name, total in self.hosts:
                done = min(self.host_done[host_id], total)
                row = Text(f"  {name.ljust(name_width)}  ", overflow="ellipsis", no_wrap=True)
                if self.console.width >= 60:
                    filled = round(BAR_CELLS * done / total) if total else BAR_CELLS
                    row.append(glyphs.full * filled)
                    row.append(glyphs.empty * (BAR_CELLS - filled), style="dim")
                    row.append("  ")
                row.append(f"{done}/{total}")
                if host_id in self.host_trouble:
                    row.append(f"  {glyphs.fail}", style="bold")
                elif done >= total:
                    row.append(f"  {glyphs.ok}", style="rgb({},{},{})".format(*KUNYIT))
                lines.append(row)
        # Between two targets keep naming the last one instead of the bare "Target finished" event.
        if self.active_host and (self.running or self.event.kind == "target_done"):
            doing = f"{VERB.get(self.active_action, 'Working on')} {self._name(self.active_host)}"
            doing += f"{glyphs.sep}{self.active_capability}" if self.active_capability else ""
        else:
            doing = self.event.phase
        frame = glyphs.spinner[int(monotonic() * 12) % len(glyphs.spinner)]
        status = Text(f"{frame} ", overflow="ellipsis", no_wrap=True)
        status.append(doing)
        status.append(f"{glyphs.sep}{self.elapsed():.1f}s", style="dim")
        lines.append(status)
        return Group(*lines)

    def __exit__(self, exc_type, exc, tb):
        if self._entered is not None:
            self._worked += monotonic() - self._entered
            self._entered = None
        if self.live:
            self.live.stop()
        if self.screen is not None:
            if exc_type:
                glyphs = self.screen.glyphs
                if issubclass(exc_type, KeyboardInterrupt):
                    text = f"{glyphs.fail} Cancelled after {self.elapsed():.1f}s{glyphs.sep}{self.processed} of {self.total} done"
                else:
                    text = f"{glyphs.fail} Failed after {self.elapsed():.1f}s: {self.line(self.event)}"
                self.console.print(Text(text))
            return False
        if exc_type:
            label = "Cancelled" if issubclass(exc_type, KeyboardInterrupt) else "Failed"
            self.console.print(f"{label}: {self.line(self.event)}")
        if self.executing or exc_type:
            self.summary()
        return False

    def summary(self):
        self.console.print(f"Setup summary ({self.elapsed():.1f}s elapsed)")
        self.console.print(f"{self.actions['INSTALL']} installed | {self.actions['UPDATE']} updated | {self.counts['CURRENT']} already current")
        self.console.print(f"{self.counts['FAILED']} failed | {self.counts['BLOCKED']} blocked | {self.counts['SKIPPED']} skipped | {self.counts['MANUAL_ACTION_REQUIRED']} manual")
        self.console.print(f"{max(0, self.total - self.processed)} unfinished")
        other = {a: n for a, n in self.actions.items() if a not in {"INSTALL", "UPDATE"}}
        if other:
            self.console.print("Other applied changes: " + ", ".join(f"{n} {a}" for a, n in other.items()))
