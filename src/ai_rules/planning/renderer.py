from __future__ import annotations

from ai_rules.domain.models import InstallationPlan
from collections import Counter
from io import StringIO
import shutil

from rich.console import Console
from rich.table import Table
from rich.text import Text
from ai_rules.catalog import load_catalog


# Screen mode's one-line plan: every action that occurs, in this order and wording.
ACTION_WORDS = (
    ("INSTALL", "to install"), ("UPDATE", "to update"), ("REPAIR", "to repair"),
    ("RECONFIGURE", "to reconfigure"), ("ADOPT", "to adopt"), ("REPLACE", "to replace"),
    ("DOWNGRADE", "to downgrade"), ("NO_OP", "current"), ("MANUAL_ACTION", "manual"), ("BLOCK", "blocked"),
)


def plan_summary(plan: InstallationPlan, *, sep: str = " · ") -> str:
    """`5 to update · 35 current`: non-zero counts only; `nothing to do` for an empty plan."""
    counts = Counter(target.action.value for target in plan.targets)
    words = dict(ACTION_WORDS)
    known = [f"{counts[action]} {word}" for action, word in ACTION_WORDS if counts[action]]
    other = [f"{count} {action.lower()}" for action, count in counts.items() if action not in words]
    return sep.join(known + other) or "nothing to do"


def plan_issues(plan: InstallationPlan, catalog) -> list[tuple[str, str, str]]:
    """Blocked and manual targets as (kind, "<Host> / <capability>", reason or manual step)."""
    issues = []
    for target in plan.targets:
        if target.action.value not in {"BLOCK", "MANUAL_ACTION"}:
            continue
        host = catalog.hosts[target.host_id].display_name if target.host_id in catalog.hosts else target.host_id
        where = f"{host} / {target.capability_id}"
        if target.action.value == "BLOCK":
            issues.append(("blocked", where, target.reason))
        else:
            step = next((op.manual_step for op in target.operations if op.manual_step), None)
            issues.append(("manual", where, step or target.reason))
    return issues


def count_backups(plan: InstallationPlan, catalog) -> int:
    """Targets that may replace existing files, each of which is backed up first."""
    return sum(
        any(op.backup for op in t.operations) or (
            t.actual.exists and t.action.value not in {"NO_OP", "BLOCK", "MANUAL_ACTION", "ADOPT"}
            and t.capability_id in catalog.capabilities
            and catalog.require_capability(t.capability_id).ownership.value == "FIRST_PARTY"
            and any(op.kind != "register_skill_invocation" for op in t.operations)
        ) for t in plan.targets
    )


def render_plan(plan: InstallationPlan, *, verbose: bool = False, width: int | None = None) -> str:
    if not verbose:
        return _compact_plan(plan, width or shutil.get_terminal_size().columns)
    lines = [f"Andino Skills plan schema={plan.schema_version} profile={plan.profile_id or 'custom'}"]
    for target in plan.targets:
        lines.append(
            f"- {target.capability_id} -> {target.host_id}/{target.scope.value}: "
            f"{target.action.value} ({target.assessment.value}) - {target.reason}"
        )
        for operation in target.operations:
            argv = f" argv={list(operation.argv)!r}" if operation.argv else ""
            manual = f" manual={operation.manual_step}" if operation.manual_step else ""
            files = f" files={list(operation.files)!r}" if operation.files else ""
            lines.append(
                f"  * {operation.kind}: source={operation.source} target={operation.target} "
                f"backup={operation.backup} reversible={operation.reversible}{argv}{files}{manual}"
            )
    return "\n".join(lines)


def _compact_plan(plan: InstallationPlan, width: int) -> str:
    catalog = load_catalog()
    actions = list(dict.fromkeys(["INSTALL", "UPDATE", "NO_OP", "BLOCK", "MANUAL_ACTION"] +
                                [t.action.value for t in plan.targets]))
    counts = Counter(t.action.value for t in plan.targets)
    visible = [a for a in actions if counts[a] or a in {"INSTALL", "UPDATE", "NO_OP", "BLOCK"}]
    labels = {"NO_OP": "Current", "BLOCK": "Blocked", "MANUAL_ACTION": "Manual"}
    table = Table(box=None, padding=(0, 1), collapse_padding=True)
    table.add_column("Host", overflow="ellipsis", no_wrap=True)
    # At narrow widths retain readable labels in a per-host action list.
    narrow = width < 72 or len(visible) > 5
    if narrow:
        table.add_column("Actions", overflow="fold")
    else:
        for action in visible:
            table.add_column(labels.get(action, action.title()), justify="right", no_wrap=True)
    for host in dict.fromkeys(t.host_id for t in plan.targets):
        host_counts = Counter(t.action.value for t in plan.targets if t.host_id == host)
        name = catalog.hosts[host].display_name if host in catalog.hosts else host
        cells = ([", ".join(f"{host_counts[a]} {labels.get(a, a.lower())}" for a in visible if host_counts[a])]
                 if narrow else [str(host_counts[a]) for a in visible])
        table.add_row(Text(name), *cells)
    stream = StringIO()
    console = Console(file=stream, width=width, color_system=None, force_terminal=False)
    console.print("INSTALLATION PLAN")
    console.print(table)
    totals = [
        f"{counts[a]} {'BLOCKED' if a == 'BLOCK' else a}" for a in actions
        if counts[a] or a in {"INSTALL", "UPDATE", "NO_OP", "BLOCK", "MANUAL_ACTION"}]
    console.print(f"{len(plan.targets)} targets")
    for start in range(0, len(totals), 3):
        console.print(" | ".join(totals[start:start + 3]), markup=False)
    console.print(f"Up to {count_backups(plan, catalog)} targets need backup if existing files are replaced.")
    console.print("Operation details: --verbose")
    for target in plan.targets:
        if target.action.value in {"BLOCK", "MANUAL_ACTION"}:
            console.print(f"{target.host_id} / {target.capability_id}: {target.action.value}: {target.reason}", markup=False)
            for op in target.operations:
                if op.manual_step:
                    console.print(op.manual_step, markup=False)
    return stream.getvalue().rstrip()
