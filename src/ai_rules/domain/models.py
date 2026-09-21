from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .errors import ValidationError
from .statuses import (
    CapabilityKind,
    DetectionStatus,
    Importance,
    InstalledOwnership,
    Mechanism,
    Ownership,
    ReconciliationAction,
    ReconciliationAssessment,
    Scope,
    TargetStatus,
    UpdateModel,
    VerificationOutcome,
    VersionObservability,
)


SECRET_MARKERS = ("secret", "token", "password", "api_key", "apikey", "credential")


def require_id(value: str, field_name: str = "id") -> str:
    if not value or not value.replace("-", "").replace("_", "").isalnum():
        raise ValidationError(f"{field_name} must be a non-empty slug: {value!r}")
    return value


def reject_secret_keys(mapping: dict[str, Any], context: str) -> None:
    for key, value in mapping.items():
        lowered = key.lower()
        policy_metadata = lowered in {"secret_policy", "credential_state"} or lowered.endswith("_policy")
        if any(marker in lowered for marker in SECRET_MARKERS) and not policy_metadata:
            if value not in (None, "", False, "env_reference", "oauth_managed_by_host"):
                raise ValidationError(f"{context} must not contain persisted secret field {key!r}")
        if isinstance(value, dict):
            reject_secret_keys(value, f"{context}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    reject_secret_keys(item, f"{context}.{key}[{index}]")


@dataclass(frozen=True)
class UpdatePolicy:
    model: UpdateModel
    default_channel: str = "stable"
    version_observability: VersionObservability = VersionObservability.NONE
    exact_pin_supported: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UpdatePolicy":
        return cls(
            model=UpdateModel(data["model"]),
            default_channel=data.get("default_channel", "stable"),
            version_observability=VersionObservability(data.get("version_observability", "none")),
            exact_pin_supported=bool(data.get("exact_pin_supported", False)),
        )


@dataclass(frozen=True)
class DeliveryStrategy:
    id: str
    mechanism: Mechanism
    hosts: tuple[str, ...]
    preference: int = 100
    automated: bool = True
    finalization: str | None = None
    argv: tuple[str, ...] = ()
    target_hint: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeliveryStrategy":
        return cls(
            id=require_id(data["id"], "delivery.id"),
            mechanism=Mechanism(data["mechanism"]),
            hosts=tuple(require_id(host, "delivery.host") for host in data.get("hosts", ())),
            preference=int(data.get("preference", 100)),
            automated=bool(data.get("automated", True)),
            finalization=data.get("finalization"),
            argv=tuple(str(part) for part in data.get("argv", ())),
            target_hint=data.get("target_hint"),
        )


@dataclass(frozen=True)
class Capability:
    schema_version: int
    id: str
    display_name: str
    ownership: Ownership
    kind: CapabilityKind
    importance: Importance
    source: dict[str, Any]
    provides: tuple[str, ...]
    requires: tuple[str, ...]
    recommends: tuple[str, ...]
    delivery: tuple[DeliveryStrategy, ...]
    verification: tuple[str, ...]
    update_policy: UpdatePolicy
    secret_policy: dict[str, Any] = field(default_factory=dict)
    specialized_consent_required: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Capability":
        reject_secret_keys(data, f"capability.{data.get('id', '<unknown>')}")
        if int(data.get("schema_version", 0)) < 1:
            raise ValidationError("capability schema_version is required")
        return cls(
            schema_version=int(data["schema_version"]),
            id=require_id(data["id"]),
            display_name=str(data["display_name"]),
            ownership=Ownership(data["ownership"]),
            kind=CapabilityKind(data["kind"]),
            importance=Importance(data["importance"]),
            source=dict(data.get("source", {})),
            provides=tuple(str(item) for item in data.get("provides", ())),
            requires=tuple(require_id(item, "requires") for item in data.get("requires", ())),
            recommends=tuple(require_id(item, "recommends") for item in data.get("recommends", ())),
            delivery=tuple(DeliveryStrategy.from_dict(item) for item in data.get("delivery", ())),
            verification=tuple(str(item) for item in data.get("verification", ())),
            update_policy=UpdatePolicy.from_dict(data["update_policy"]),
            secret_policy=dict(data.get("secret_policy", {})),
            specialized_consent_required=bool(data.get("specialized_consent_required", False)),
        )


@dataclass(frozen=True)
class Host:
    schema_version: int
    id: str
    display_name: str
    scopes: tuple[Scope, ...]
    mechanisms: tuple[Mechanism, ...]
    global_skill_path: str | None = None
    project_skill_path: str = ".agents/skills"
    mcp_config_hint: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Host":
        if int(data.get("schema_version", 0)) < 1:
            raise ValidationError("host schema_version is required")
        return cls(
            schema_version=int(data["schema_version"]),
            id=require_id(data["id"], "host.id"),
            display_name=str(data["display_name"]),
            scopes=tuple(Scope(item) for item in data.get("scopes", ())),
            mechanisms=tuple(Mechanism(item) for item in data.get("mechanisms", ())),
            global_skill_path=data.get("global_skill_path"),
            project_skill_path=data.get("project_skill_path", ".agents/skills"),
            mcp_config_hint=data.get("mcp_config_hint"),
        )


@dataclass(frozen=True)
class Profile:
    schema_version: int
    id: str
    display_name: str
    default: bool
    capabilities: tuple[str, ...]
    suggested: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Profile":
        reject_secret_keys(data, f"profile.{data.get('id', '<unknown>')}")
        if int(data.get("schema_version", 0)) < 1:
            raise ValidationError("profile schema_version is required")
        return cls(
            schema_version=int(data["schema_version"]),
            id=require_id(data["id"], "profile.id"),
            display_name=str(data["display_name"]),
            default=bool(data.get("default", False)),
            capabilities=tuple(require_id(item, "profile.capabilities") for item in data.get("capabilities", ())),
            suggested=tuple(require_id(item, "profile.suggested") for item in data.get("suggested", ())),
        )


@dataclass(frozen=True)
class ActualState:
    exists: bool = False
    ownership: InstalledOwnership = InstalledOwnership.UNKNOWN_ORIGIN
    installed_version: str | None = None
    target_version: str | None = None
    healthy: bool = False
    config_drift: bool = False
    artifact_drift: bool = False
    version_observability: VersionObservability = VersionObservability.NONE


@dataclass(frozen=True)
class HostDetection:
    host_id: str
    status: DetectionStatus
    version: str | None = None
    path: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class VerificationCheck:
    name: str
    outcome: VerificationOutcome
    message: str = ""


@dataclass(frozen=True)
class Operation:
    kind: str
    capability_id: str
    host_id: str
    scope: Scope
    action: ReconciliationAction
    source: str
    target: str
    reason: str
    argv: tuple[str, ...] = ()
    files: tuple[str, ...] = ()
    backup: bool = False
    reversible: bool = False
    network: bool = False
    manual_step: str | None = None


@dataclass(frozen=True)
class PlanTarget:
    capability_id: str
    host_id: str
    scope: Scope
    action: ReconciliationAction
    assessment: ReconciliationAssessment
    status: TargetStatus
    strategy_id: str | None
    reason: str
    operations: tuple[Operation, ...]
    actual: ActualState
    target_version: str | None = None


@dataclass(frozen=True)
class InstallationPlan:
    schema_version: int
    profile_id: str | None
    targets: tuple[PlanTarget, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def blocked(self) -> bool:
        return any(target.action == ReconciliationAction.BLOCK for target in self.targets)


def safe_child_path(root: Path, *parts: str) -> Path:
    resolved_root = root.resolve()
    candidate = resolved_root.joinpath(*parts).resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValidationError(f"path escapes approved root: {candidate}")
    return candidate
