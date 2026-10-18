from __future__ import annotations

from ai_rules.domain.models import InstallationPlan
from collections import Counter
from io import StringIO
import shutil

from rich.console import Console
from rich.table import Table
from rich.text import Text
from ai_rules.catalog import load_catalog


def render_plan(plan: InstallationPlan, *, verbose: bool = False, width: int | None = None) -> str:
    if not verbose:
        return _compact_plan(plan, width or shutil.get_terminal_size().columns)
    lines = [f"AI-RULES plan schema={plan.schema_version} profile={plan.profile_id or 'custom'}"]
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
    backups = sum(
        any(op.backup for op in t.operations) or (
            t.actual.exists and t.action.value not in {"NO_OP", "BLOCK", "MANUAL_ACTION", "ADOPT"}
            and t.capability_id in catalog.capabilities
            and catalog.require_capability(t.capability_id).ownership.value == "FIRST_PARTY"
            and any(op.kind != "register_skill_invocation" for op in t.operations)
        ) for t in plan.targets
    )
    console.print(f"Up to {backups} targets need backup if existing files are replaced.")
    console.print("Operation details: --verbose")
    for target in plan.targets:
        if target.action.value in {"BLOCK", "MANUAL_ACTION"}:
            console.print(f"{target.host_id} / {target.capability_id}: {target.action.value}: {target.reason}", markup=False)
            for op in target.operations:
                if op.manual_step:
                    console.print(op.manual_step, markup=False)
    return stream.getvalue().rstrip()
