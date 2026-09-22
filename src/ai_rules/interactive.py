from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Sequence

from ai_rules.catalog.loader import Catalog
from ai_rules.domain.models import Capability, Host, Profile


@dataclass(frozen=True)
class InteractiveSelection:
    hosts: tuple[str, ...]
    profile_id: str | None
    capabilities: tuple[str, ...]


@dataclass(frozen=True)
class InteractiveChoice:
    """A portable display/value pair for a Questionary option."""

    title: str
    value: str
    description: str


def build_host_choices(hosts: Mapping[str, Host]) -> tuple[InteractiveChoice, ...]:
    return tuple(
        InteractiveChoice(
            title=host.display_name,
            value=host.id,
            description=f"Skills: {host.global_skill_path}" if host.global_skill_path else "Skills: host-managed location",
        )
        for host in hosts.values()
    )


def build_profile_choices(
    profiles: Mapping[str, Profile], capabilities: Mapping[str, Capability]
) -> tuple[InteractiveChoice, ...]:
    return tuple(
        InteractiveChoice(
            title=profile.display_name,
            value=profile.id,
            description=_profile_description(profile, capabilities),
        )
        for profile in profiles.values()
    )


def build_capability_choices(capabilities: Mapping[str, Capability]) -> tuple[InteractiveChoice, ...]:
    return tuple(
        InteractiveChoice(title=capability.display_name, value=capability.id, description=capability.description)
        for capability in capabilities.values()
    )


def render_setup_summary(
    host_ids: Sequence[str],
    profile_id: str | None,
    capabilities: Sequence[str],
    scope: str,
    catalog: Catalog,
    profiles: Mapping[str, Profile] | None = None,
) -> str:
    profile_name = "Custom" if profile_id is None else (profiles or {}).get(profile_id, None)
    profile_label = profile_name.display_name if isinstance(profile_name, Profile) else (profile_id or "Custom").replace("-", " ").title()
    lines = ["AI-RULES Setup", "", "Hosts"]
    lines.extend(f"  {catalog.require_host(host_id).display_name}" for host_id in host_ids)
    lines.extend(["", "Profile", f"  {profile_label}", "", "Will install/configure"])
    lines.extend(f"  {catalog.require_capability(capability_id).display_name} - {_capability_kind_label(catalog.require_capability(capability_id))}" for capability_id in capabilities)
    lines.extend(["", "Scope", f"  {scope.title()}"])
    return "\n".join(lines)


def _profile_description(profile: Profile, capabilities: Mapping[str, Capability]) -> str:
    lines = [profile.description, "Includes: " + ", ".join(capabilities[capability_id].display_name for capability_id in profile.capabilities)]
    if profile.suggested:
        lines.append("Suggested: " + ", ".join(capabilities[capability_id].display_name for capability_id in profile.suggested))
    return "\n".join(line for line in lines if line)


def _capability_kind_label(capability: Capability) -> str:
    if capability.kind.value == "mcp":
        return "MCP integration"
    if capability.kind.value == "plugin":
        return "external plugin"
    if capability.ownership.value == "FIRST_PARTY":
        return "first-party skill"
    return capability.kind.value.replace("_", " ")


def collect_selection(
    choose: Callable[[str, Sequence[object]], str | None],
    checkbox: Callable[[str, Sequence[object]], Sequence[str] | None],
    host_choices: Sequence[object],
    profile_choices: Sequence[object],
    capability_choices: Sequence[object],
) -> InteractiveSelection | None:
    hosts = checkbox("Select AI agent(s)", host_choices)
    if not hosts:
        return None
    profile = choose("Select profile", profile_choices)
    if profile is None:
        return None
    if profile != "custom":
        return InteractiveSelection(tuple(hosts), profile, ())
    capabilities = checkbox("Select capabilities", capability_choices)
    if not capabilities:
        return None
    return InteractiveSelection(tuple(hosts), None, tuple(capabilities))


def prompt_selection(
    hosts: Mapping[str, Host],
    profiles: Mapping[str, Profile],
    capabilities: Mapping[str, Capability],
) -> InteractiveSelection | None:
    import questionary

    host_choices = _questionary_choices(build_host_choices(hosts))
    profile_choices = _questionary_choices(build_profile_choices(profiles, capabilities))
    profile_choices.append(questionary.Choice(title="Custom", value="custom", description="Choose skills and integrations manually"))
    capability_choices = _questionary_choices(build_capability_choices(capabilities))
    return collect_selection(
        choose=lambda message, choices: questionary.select(message, choices=choices).ask(),
        checkbox=lambda message, choices: questionary.checkbox(message, choices=choices).ask(),
        host_choices=host_choices,
        profile_choices=profile_choices,
        capability_choices=capability_choices,
    )


def _questionary_choices(choices: Sequence[InteractiveChoice]):
    import questionary

    return [questionary.Choice(title=choice.title, value=choice.value, description=choice.description) for choice in choices]


def confirm_execution(confirm: Callable[[str], bool | None]) -> bool:
    return confirm("Apply this installation plan?") is True


def prompt_confirmation() -> bool:
    import questionary

    return confirm_execution(lambda message: questionary.confirm(message, default=False).ask())

