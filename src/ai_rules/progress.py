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


class SetupProgress:
    def __init__(self, *, console: Console | None = None, enabled: bool = True, verbose: bool = False):
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

    def __enter__(self):
        if self.dynamic:
            self.live = Live(console=self.console, get_renderable=self.render,
                             refresh_per_second=8, transient=True)
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
            if event.status == "APPLIED":
                self.actions[event.action] += 1
        elif event.kind == "verification_failed":
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
            phase = f" (during {self.last_work_phase})" if event.phase == "Operation failed" else ""
            self.console.print(f"{self.line(event)}{phase}: {event.detail}")
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
        elapsed = monotonic() - self.started
        lines = [Text(self.line(self.event), overflow="ellipsis", no_wrap=True)]
        if self.total:
            pending = max(0, self.total - self.processed - int(self.running))
            lines.append(Text(f"{self.processed} / {self.total} targets processed | {int(self.running)} running | {pending} pending"))
            lines.append(Text(" | ".join(f"{n} {s.lower()}" for s, n in self.counts.copy().items())))
        self.spinner.update(text=Text(f"{self.event.phase} | {elapsed:.1f}s elapsed", overflow="ellipsis", no_wrap=True))
        return Group(*lines, self.spinner)

    def __exit__(self, exc_type, exc, tb):
        if self.live:
            self.live.stop()
        if exc_type:
            label = "Cancelled" if issubclass(exc_type, KeyboardInterrupt) else "Failed"
            self.console.print(f"{label}: {self.line(self.event)}")
        if self.executing or exc_type:
            self.summary()
        return False

    def summary(self):
        self.console.print(f"Setup summary ({monotonic() - self.started:.1f}s elapsed)")
        self.console.print(f"{self.actions['INSTALL']} installed | {self.actions['UPDATE']} updated | {self.counts['CURRENT']} already current")
        self.console.print(f"{self.counts['FAILED']} failed | {self.counts['BLOCKED']} blocked | {self.counts['SKIPPED']} skipped | {self.counts['MANUAL_ACTION_REQUIRED']} manual")
        self.console.print(f"{max(0, self.total - self.processed)} unfinished")
        other = {a: n for a, n in self.actions.items() if a not in {"INSTALL", "UPDATE"}}
        if other:
            self.console.print("Other applied changes: " + ", ".join(f"{n} {a}" for a, n in other.items()))
