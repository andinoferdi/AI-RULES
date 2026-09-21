from __future__ import annotations

from pathlib import Path
from typing import Protocol

from ai_rules.domain.models import HostDetection, Operation, VerificationCheck
from ai_rules.domain.statuses import Mechanism, Scope


class HostAdapter(Protocol):
    id: str

    def detect(self) -> HostDetection: ...

    def supported_scopes(self) -> tuple[Scope, ...]: ...

    def supported_mechanisms(self) -> tuple[Mechanism, ...]: ...

    def skill_target(self, scope: Scope, project_root: Path | None = None) -> Path | None: ...

    def plan_mcp_registration(self, capability_id: str, scope: Scope) -> tuple[Operation, ...]: ...

    def verify_skill(self, capability_id: str, scope: Scope, project_root: Path | None = None) -> tuple[VerificationCheck, ...]: ...

    def verify_mcp(self, capability_id: str, scope: Scope) -> tuple[VerificationCheck, ...]: ...

    def refresh_requirement(self) -> str | None: ...
