from __future__ import annotations

from dataclasses import dataclass

from ai_rules.domain.models import InstallationPlan
from ai_rules.domain.statuses import ReconciliationAction, TargetStatus


@dataclass(frozen=True)
class DoctorTarget:
    capability_id: str
    host_id: str
    status: TargetStatus
    assessment: str
    message: str


@dataclass(frozen=True)
class DoctorReport:
    targets: tuple[DoctorTarget, ...]

    @property
    def healthy(self) -> bool:
        return all(target.status == TargetStatus.VERIFIED for target in self.targets)


def doctor_from_plan(plan: InstallationPlan) -> DoctorReport:
    targets = []
    for target in plan.targets:
        status = target.status
        if target.action == ReconciliationAction.NO_OP:
            status = TargetStatus.VERIFIED
        elif target.actual.exists and target.actual.artifact_drift:
            status = TargetStatus.FAILED
        elif target.actual.exists and target.actual.config_drift:
            status = TargetStatus.PARTIALLY_VERIFIED
        elif target.action == ReconciliationAction.MANUAL_ACTION:
            status = TargetStatus.MANUAL_ACTION_REQUIRED
        elif target.action == ReconciliationAction.BLOCK:
            status = TargetStatus.BLOCKED
        targets.append(
            DoctorTarget(
                capability_id=target.capability_id,
                host_id=target.host_id,
                status=status,
                assessment=target.assessment.value,
                message=target.reason,
            )
        )
    return DoctorReport(targets=tuple(targets))


def render_doctor(report: DoctorReport) -> str:
    lines = ["AI-RULES doctor"]
    for target in report.targets:
        lines.append(f"- {target.capability_id} -> {target.host_id}: {target.status.value} ({target.assessment}) - {target.message}")
    return "\n".join(lines)
