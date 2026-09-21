from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from ai_rules.domain.models import Host, HostDetection, Operation, VerificationCheck
from ai_rules.domain.statuses import DetectionStatus, Mechanism, ReconciliationAction, Scope, VerificationOutcome


@dataclass(frozen=True)
class StaticHostAdapter:
    host: Host
    home: Path

    @property
    def id(self) -> str:
        return self.host.id

    def detect(self) -> HostDetection:
        command = {
            "codex": "codex",
            "claude-code": "claude",
            "opencode": "opencode",
            "antigravity": "antigravity",
        }.get(self.host.id)
        path = shutil.which(command) if command else None
        status = DetectionStatus.PRESENT if path else DetectionStatus.UNKNOWN
        reason = None if path else "host command not found; file-based planning remains available"
        return HostDetection(host_id=self.host.id, status=status, path=path, reason=reason)

    def supported_scopes(self) -> tuple[Scope, ...]:
        return self.host.scopes

    def supported_mechanisms(self) -> tuple[Mechanism, ...]:
        return self.host.mechanisms

    def skill_target(self, scope: Scope, project_root: Path | None = None) -> Path | None:
        if scope == Scope.PROJECT:
            if project_root is None:
                return None
            return project_root / self.host.project_skill_path
        if self.host.global_skill_path is None:
            return None
        return Path(self.host.global_skill_path.replace("~", str(self.home), 1))

    def plan_mcp_registration(self, capability_id: str, scope: Scope) -> tuple[Operation, ...]:
        return (
            Operation(
                kind="patch_structured_config",
                capability_id=capability_id,
                host_id=self.host.id,
                scope=scope,
                action=ReconciliationAction.RECONFIGURE,
                source="catalog:mcp",
                target=self.host.mcp_config_hint or self.host.id,
                reason="register MCP server through host-supported configuration",
                backup=True,
                reversible=True,
            ),
        )

    def verify_skill(self, capability_id: str, scope: Scope, project_root: Path | None = None) -> tuple[VerificationCheck, ...]:
        target = self.skill_target(scope, project_root)
        if target is None:
            return (VerificationCheck("skill target", VerificationOutcome.FAIL, "scope has no target path"),)
        skill_file = target / capability_id / "SKILL.md"
        if skill_file.exists():
            return (VerificationCheck("skill artifact", VerificationOutcome.PASS, str(skill_file)),)
        return (VerificationCheck("skill artifact", VerificationOutcome.FAIL, f"missing {skill_file}"),)

    def verify_mcp(self, capability_id: str, scope: Scope) -> tuple[VerificationCheck, ...]:
        return (VerificationCheck("mcp runtime", VerificationOutcome.NOT_RUN, "live host MCP health is not available in fixture mode"),)

    def refresh_requirement(self) -> str | None:
        return "new-session"


def build_host_adapters(hosts: dict[str, Host], home: Path | None = None) -> dict[str, StaticHostAdapter]:
    root = home or Path.home()
    return {host_id: StaticHostAdapter(host=host, home=root) for host_id, host in hosts.items()}
