from __future__ import annotations

from dataclasses import dataclass
import json
from importlib import resources

from ai_rules.domain.models import ActualState, Capability, Operation, VerificationCheck
from ai_rules.domain.statuses import InstalledOwnership, Ownership, ReconciliationAction, Scope, VerificationOutcome


@dataclass(frozen=True)
class StaticCapabilityAdapter:
    state: dict[tuple[str, str, str], ActualState] | None = None
    targets: dict[str, str] | None = None

    @property
    def id(self) -> str:
        return "static"

    def detect_current_state(self, capability: Capability, host_id: str, scope: Scope) -> ActualState:
        if self.state is None:
            return ActualState()
        return self.state.get((capability.id, host_id, scope.value), ActualState())

    def resolve_target(self, capability: Capability, channel: str = "stable") -> str | None:
        if self.targets and capability.id in self.targets:
            return self.targets[capability.id]
        if capability.ownership == Ownership.FIRST_PARTY:
            manifest = _load_release_manifest()
            target = manifest.get("first_party", {}).get(capability.id, {})
            commit = target.get("commit")
            if commit:
                sequence = int(target.get("release_sequence", manifest.get("release_sequence", 0)))
                return f"release-manifest:{capability.id}@{commit}#{sequence}"
            branch = capability.source.get("branch", capability.id)
            return f"release-manifest:{branch}@stable"
        if capability.id == "context7" and capability.update_policy.model.value == "remote_service":
            return "upstream-managed:remote-service"
        return f"{capability.update_policy.model.value}:{channel}"

    def plan_operations(self, capability: Capability, host_id: str, scope: Scope) -> tuple[Operation, ...]:
        if capability.id == "superpowers" and host_id == "antigravity-cli":
            return (
                Operation(
                    kind="run_command",
                    capability_id=capability.id,
                    host_id=host_id,
                    scope=scope,
                    action=ReconciliationAction.INSTALL,
                    source="https://github.com/obra/superpowers",
                    target="Antigravity plugin repository",
                    reason="official upstream install/update command",
                    argv=("agy", "plugin", "install", "https://github.com/obra/superpowers"),
                    network=True,
                ),
            )
        if capability.id == "context7":
            argv_by_host = {
                "codex": ("codex", "mcp", "add", "context7", "--url", "https://mcp.context7.com/mcp"),
                "claude-code": ("claude", "mcp", "add", "--scope", "user" if scope == Scope.GLOBAL else "project", "--transport", "http", "context7", "https://mcp.context7.com/mcp"),
                "opencode": ("opencode", "mcp", "add", "context7", "--url", "https://mcp.context7.com/mcp"),
                "antigravity-cli": ("agy", "mcp", "add", "context7", "https://mcp.context7.com/mcp"),
            }
            argv = argv_by_host.get(host_id)
            if argv:
                return (
                    Operation(
                        kind="run_command",
                        capability_id=capability.id,
                        host_id=host_id,
                        scope=scope,
                        action=ReconciliationAction.INSTALL,
                        source="https://mcp.context7.com/mcp",
                        target=f"{host_id} MCP configuration",
                        reason="register remote Context7 MCP without persisting credentials",
                        argv=argv,
                        network=True,
                        backup=True,
                        reversible=True,
                    ),
                )
        return (
            Operation(
                kind="capability_operation",
                capability_id=capability.id,
                host_id=host_id,
                scope=scope,
                action=ReconciliationAction.INSTALL,
                source=capability.source.get("repository", capability.source.get("upstream", capability.id)),
                target=f"{host_id}:{scope.value}:{capability.id}",
                reason="capability adapter operation",
                network=capability.ownership != Ownership.FIRST_PARTY,
                reversible=capability.ownership == Ownership.FIRST_PARTY,
            ),
        )

    def verify(self, capability: Capability, host_id: str, scope: Scope) -> tuple[VerificationCheck, ...]:
        if capability.ownership == Ownership.EXTERNAL:
            return (VerificationCheck("external runtime", VerificationOutcome.NOT_RUN, "live upstream check not run in static adapter"),)
        return (VerificationCheck("first-party metadata", VerificationOutcome.PASS, "first-party target resolved"),)


def managed_state(version: str, healthy: bool = True, artifact_drift: bool = False, config_drift: bool = False) -> ActualState:
    return ActualState(
        exists=True,
        ownership=InstalledOwnership.MANAGED_BY_AI_RULES,
        installed_version=version,
        healthy=healthy,
        artifact_drift=artifact_drift,
        config_drift=config_drift,
    )


def _load_release_manifest() -> dict:
    with resources.files("ai_rules.release.data").joinpath("release_manifest.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)
