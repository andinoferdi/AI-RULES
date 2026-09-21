from __future__ import annotations

from ai_rules.domain.models import InstallationPlan


def render_plan(plan: InstallationPlan) -> str:
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
