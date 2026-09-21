from __future__ import annotations

from dataclasses import dataclass, replace

from ai_rules.capabilities.base import CapabilityAdapter
from ai_rules.catalog.loader import Catalog
from ai_rules.domain.errors import ValidationError
from ai_rules.domain.models import (
    ActualState,
    InstallationPlan,
    Operation,
    PlanTarget,
)
from ai_rules.domain.statuses import (
    InstalledOwnership,
    ReconciliationAction,
    ReconciliationAssessment,
    Scope,
    TargetStatus,
)
from ai_rules.profiles.loader import ProfileSet


@dataclass(frozen=True)
class ResolveRequest:
    hosts: tuple[str, ...]
    scope: Scope = Scope.GLOBAL
    profile_id: str | None = None
    capabilities: tuple[str, ...] = ()
    explicit_pins: dict[str, str] | None = None
    allow_adopt: bool = False
    allow_replace: bool = False


class Resolver:
    def __init__(self, catalog: Catalog, profiles: ProfileSet, capability_adapter: CapabilityAdapter):
        self.catalog = catalog
        self.profiles = profiles
        self.capability_adapter = capability_adapter

    def resolve(self, request: ResolveRequest) -> InstallationPlan:
        selected = self._expand_selection(request)
        targets: list[PlanTarget] = []
        for host_id in request.hosts:
            host = self.catalog.require_host(host_id)
            if request.scope not in host.scopes:
                for capability_id in selected:
                    targets.append(self._unsupported_target(capability_id, host_id, request.scope, "scope unsupported by host"))
                continue
            for capability_id in selected:
                capability = self.catalog.require_capability(capability_id)
                strategies = [
                    strategy
                    for strategy in capability.delivery
                    if host_id in strategy.hosts and strategy.mechanism in host.mechanisms
                ]
                if not strategies:
                    targets.append(self._unsupported_target(capability_id, host_id, request.scope, "no compatible delivery strategy"))
                    continue
                strategy = sorted(strategies, key=lambda item: (item.preference, item.id))[0]
                actual = self.capability_adapter.detect_current_state(capability, host_id, request.scope)
                target_version = self._target_version(capability_id, request)
                if target_version is None:
                    target_version = self.capability_adapter.resolve_target(capability)
                action, assessment, status, reason = self._reconcile(actual, target_version, strategy.automated)
                operations = self._operations_for(action, capability_id, host_id, request.scope, strategy.id, reason, target_version)
                if action in {
                    ReconciliationAction.INSTALL,
                    ReconciliationAction.UPDATE,
                    ReconciliationAction.REPAIR,
                    ReconciliationAction.RECONFIGURE,
                }:
                    operations = tuple(
                        replace(operation, action=action, reason=reason)
                        for operation in self.capability_adapter.plan_operations(capability, host_id, request.scope)
                    )
                if action == ReconciliationAction.MANUAL_ACTION:
                    operations = (
                        Operation(
                            kind="manual_step",
                            capability_id=capability_id,
                            host_id=host_id,
                            scope=request.scope,
                            action=action,
                            source=capability.source.get("repository", capability_id),
                            target=strategy.target_hint or strategy.id,
                            reason=reason,
                            manual_step=strategy.finalization or "manual host finalization required",
                        ),
                    )
                targets.append(
                    PlanTarget(
                        capability_id=capability_id,
                        host_id=host_id,
                        scope=request.scope,
                        action=action,
                        assessment=assessment,
                        status=status,
                        strategy_id=strategy.id,
                        reason=reason,
                        operations=operations,
                        actual=actual,
                        target_version=target_version,
                    )
                )
        return InstallationPlan(schema_version=1, profile_id=request.profile_id, targets=tuple(targets))

    def _expand_selection(self, request: ResolveRequest) -> tuple[str, ...]:
        if request.profile_id:
            profile = self.profiles.require(request.profile_id)
            selected = list(profile.capabilities)
        else:
            selected = list(request.capabilities or self.profiles.default.capabilities)
        for capability_id in list(selected):
            capability = self.catalog.require_capability(capability_id)
            for required in capability.requires:
                if required not in selected:
                    selected.append(required)
        return tuple(dict.fromkeys(selected))

    def _target_version(self, capability_id: str, request: ResolveRequest) -> str | None:
        if request.explicit_pins and capability_id in request.explicit_pins:
            return request.explicit_pins[capability_id]
        return None

    def _reconcile(
        self, actual: ActualState, target_version: str | None, automated: bool
    ) -> tuple[ReconciliationAction, ReconciliationAssessment, TargetStatus, str]:
        if not automated:
            return (
                ReconciliationAction.MANUAL_ACTION,
                ReconciliationAssessment.VERSION_UNKNOWN,
                TargetStatus.MANUAL_ACTION_REQUIRED,
                "upstream or host path requires manual finalization",
            )
        if not actual.exists:
            return ReconciliationAction.INSTALL, ReconciliationAssessment.VERSION_UNKNOWN, TargetStatus.PLANNED, "target is absent"
        if actual.ownership in (InstalledOwnership.EXTERNAL_EXISTING, InstalledOwnership.UNKNOWN_ORIGIN, InstalledOwnership.CONFLICTING):
            return (
                ReconciliationAction.BLOCK,
                ReconciliationAssessment.UNMANAGED_EXISTING,
                TargetStatus.BLOCKED,
                "existing unmanaged or unknown-origin target is preserved",
            )
        if actual.config_drift and not actual.artifact_drift:
            return (
                ReconciliationAction.RECONFIGURE,
                ReconciliationAssessment.RECONFIGURE_REQUIRED,
                TargetStatus.PLANNED,
                "managed host configuration drift detected",
            )
        if actual.artifact_drift:
            return ReconciliationAction.REPAIR, ReconciliationAssessment.DRIFTED, TargetStatus.PLANNED, "managed artifact drift detected"
        if actual.installed_version and target_version and actual.installed_version != target_version:
            if _version_rank(actual.installed_version) > _version_rank(target_version):
                return (
                    ReconciliationAction.BLOCK,
                    ReconciliationAssessment.PINNED,
                    TargetStatus.BLOCKED,
                    "managed target is newer than stable target; no silent downgrade",
                )
            return (
                ReconciliationAction.UPDATE,
                ReconciliationAssessment.UPDATE_AVAILABLE,
                TargetStatus.PLANNED,
                "managed target is older than desired target",
            )
        if actual.healthy:
            return ReconciliationAction.NO_OP, ReconciliationAssessment.CURRENT, TargetStatus.VERIFIED, "managed target is current and healthy"
        return ReconciliationAction.REPAIR, ReconciliationAssessment.DRIFTED, TargetStatus.PLANNED, "managed target is present but unhealthy"

    def _operations_for(
        self,
        action: ReconciliationAction,
        capability_id: str,
        host_id: str,
        scope: Scope,
        strategy_id: str,
        reason: str,
        target_version: str | None,
    ) -> tuple[Operation, ...]:
        if action in (ReconciliationAction.NO_OP, ReconciliationAction.BLOCK):
            return ()
        return (
            Operation(
                kind=action.value.lower(),
                capability_id=capability_id,
                host_id=host_id,
                scope=scope,
                action=action,
                source=strategy_id,
                target=target_version or f"{host_id}:{capability_id}",
                reason=reason,
                backup=action in (ReconciliationAction.REPAIR, ReconciliationAction.RECONFIGURE, ReconciliationAction.UPDATE),
                reversible=action != ReconciliationAction.MANUAL_ACTION,
            ),
        )

    def _unsupported_target(self, capability_id: str, host_id: str, scope: Scope, reason: str) -> PlanTarget:
        return PlanTarget(
            capability_id=capability_id,
            host_id=host_id,
            scope=scope,
            action=ReconciliationAction.BLOCK,
            assessment=ReconciliationAssessment.VERSION_UNKNOWN,
            status=TargetStatus.UNSUPPORTED,
            strategy_id=None,
            reason=reason,
            operations=(),
            actual=ActualState(),
            target_version=None,
        )


def _version_rank(version: str) -> tuple[int, str]:
    if version.startswith("release-manifest:"):
        return (1, version)
    if version.startswith("future:"):
        return (2, version)
    return (0, version)


def build_resolver(catalog: Catalog, profiles: ProfileSet, capability_adapter: CapabilityAdapter) -> Resolver:
    if not catalog.capabilities:
        raise ValidationError("catalog has no capabilities")
    return Resolver(catalog, profiles, capability_adapter)
