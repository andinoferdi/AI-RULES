"""Agent defaults (Layer 1): a managed working-defaults block in host instruction files."""
from .core import (
    END,
    LANGUAGES,
    START,
    STATE_FILE,
    DefaultsResult,
    DefaultsTarget,
    check,
    detect_mcp_servers,
    detect_skills,
    expand,
    format_result,
    plan_targets,
    read_state,
    reconcile,
    remove,
    render_block,
)
from .text import DOMAIN_HINTS, MCP_NOTES

__all__ = [
    "DOMAIN_HINTS", "END", "LANGUAGES", "MCP_NOTES", "START", "STATE_FILE", "DefaultsResult", "DefaultsTarget", "check",
    "detect_mcp_servers", "detect_skills", "expand", "format_result", "plan_targets", "read_state",
    "reconcile", "remove", "render_block",
]
