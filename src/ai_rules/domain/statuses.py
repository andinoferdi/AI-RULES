from __future__ import annotations

from enum import StrEnum


class Ownership(StrEnum):
    FIRST_PARTY = "FIRST_PARTY"
    EXTERNAL = "EXTERNAL"


class CapabilityKind(StrEnum):
    SKILL = "skill"
    SKILL_FAMILY = "skill_family"
    PLUGIN = "plugin"
    MCP = "mcp"
    CLI = "cli"
    SERVICE = "service"
    INTEGRATION = "integration"
    PROJECT_TEMPLATE = "project_template"
    RUNTIME = "runtime"


class Importance(StrEnum):
    REQUIRED = "REQUIRED"
    RECOMMENDED = "RECOMMENDED"
    OPTIONAL = "OPTIONAL"
    SPECIALIZED = "SPECIALIZED"


class Mechanism(StrEnum):
    SKILL_DIRECTORY = "SKILL_DIRECTORY"
    PLUGIN_MARKETPLACE = "PLUGIN_MARKETPLACE"
    PLUGIN_REPOSITORY = "PLUGIN_REPOSITORY"
    MCP_STDIO = "MCP_STDIO"
    MCP_HTTP = "MCP_HTTP"
    MCP_OAUTH = "MCP_OAUTH"
    PROJECT_SKILL_SCOPE = "PROJECT_SKILL_SCOPE"
    GLOBAL_SKILL_SCOPE = "GLOBAL_SKILL_SCOPE"
    HOST_PLUGIN_CONFIG = "HOST_PLUGIN_CONFIG"
    MANUAL = "MANUAL"


class Scope(StrEnum):
    GLOBAL = "global"
    PROJECT = "project"


class DetectionStatus(StrEnum):
    PRESENT = "PRESENT"
    MISSING = "MISSING"
    UNKNOWN = "UNKNOWN"
    UNSUPPORTED = "UNSUPPORTED"


class TargetStatus(StrEnum):
    NOT_SELECTED = "NOT_SELECTED"
    PLANNED = "PLANNED"
    BLOCKED = "BLOCKED"
    UNSUPPORTED = "UNSUPPORTED"
    INSTALLED = "INSTALLED"
    CONFIGURED = "CONFIGURED"
    MANUAL_ACTION_REQUIRED = "MANUAL_ACTION_REQUIRED"
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class ReconciliationAssessment(StrEnum):
    CURRENT = "CURRENT"
    UPDATE_AVAILABLE = "UPDATE_AVAILABLE"
    DRIFTED = "DRIFTED"
    RECONFIGURE_REQUIRED = "RECONFIGURE_REQUIRED"
    UNMANAGED_EXISTING = "UNMANAGED_EXISTING"
    PINNED = "PINNED"
    UPSTREAM_MANAGED = "UPSTREAM_MANAGED"
    VERSION_UNKNOWN = "VERSION_UNKNOWN"


class ReconciliationAction(StrEnum):
    INSTALL = "INSTALL"
    NO_OP = "NO_OP"
    UPDATE = "UPDATE"
    REPAIR = "REPAIR"
    RECONFIGURE = "RECONFIGURE"
    ADOPT = "ADOPT"
    REPLACE = "REPLACE"
    DOWNGRADE = "DOWNGRADE"
    MANUAL_ACTION = "MANUAL_ACTION"
    BLOCK = "BLOCK"


class VerificationOutcome(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT_RUN"
    MANUAL = "MANUAL"


class UpdateModel(StrEnum):
    RELEASE_MANIFEST = "release_manifest"
    REMOTE_SERVICE = "remote_service"
    PACKAGE_REGISTRY = "package_registry"
    GIT = "git"
    MARKETPLACE = "marketplace"
    MANUAL = "manual"


class VersionObservability(StrEnum):
    FULL = "full"
    PARTIAL = "partial"
    NONE = "none"


class InstalledOwnership(StrEnum):
    MANAGED_BY_AI_RULES = "MANAGED_BY_AI_RULES"
    EXTERNAL_EXISTING = "EXTERNAL_EXISTING"
    CONFLICTING = "CONFLICTING"
    UNKNOWN_ORIGIN = "UNKNOWN_ORIGIN"
