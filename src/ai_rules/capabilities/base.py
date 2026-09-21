from __future__ import annotations

from typing import Protocol

from ai_rules.domain.models import ActualState, Capability, Operation, VerificationCheck
from ai_rules.domain.statuses import Scope


class CapabilityAdapter(Protocol):
    id: str

    def detect_current_state(self, capability: Capability, host_id: str, scope: Scope) -> ActualState: ...

    def resolve_target(self, capability: Capability, channel: str = "stable") -> str | None: ...

    def plan_operations(self, capability: Capability, host_id: str, scope: Scope) -> tuple[Operation, ...]: ...

    def verify(self, capability: Capability, host_id: str, scope: Scope) -> tuple[VerificationCheck, ...]: ...
