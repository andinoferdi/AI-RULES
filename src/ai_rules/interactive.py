from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence


HOST_IDS = ("codex", "claude-code", "opencode", "antigravity-cli", "antigravity-ide")
PROFILE_IDS = ("minimal", "recommended", "engineering", "web-development", "research-skripsi", "design", "media", "reverse-engineering", "everything")
CAPABILITY_IDS = ("andino-workflow", "ai-codebase-rescue", "skripsi-skill", "superpowers", "context7")


@dataclass(frozen=True)
class InteractiveSelection:
    hosts: tuple[str, ...]
    profile_id: str | None
    capabilities: tuple[str, ...]


def collect_selection(
    choose: Callable[[str, Sequence[str]], str | None],
    checkbox: Callable[[str, Sequence[str]], Sequence[str] | None],
    host_ids: Sequence[str] = HOST_IDS,
    profile_ids: Sequence[str] = PROFILE_IDS,
    capability_ids: Sequence[str] = CAPABILITY_IDS,
) -> InteractiveSelection | None:
    hosts = checkbox("Select host(s)", host_ids)
    if not hosts:
        return None
    profile = choose("Select profile", (*profile_ids, "custom"))
    if profile is None:
        return None
    if profile != "custom":
        return InteractiveSelection(tuple(hosts), profile, ())
    capabilities = checkbox("Select capabilities", capability_ids)
    if not capabilities:
        return None
    return InteractiveSelection(tuple(hosts), None, tuple(capabilities))


def prompt_selection(
    host_ids: Sequence[str] = HOST_IDS,
    profile_ids: Sequence[str] = PROFILE_IDS,
    capability_ids: Sequence[str] = CAPABILITY_IDS,
) -> InteractiveSelection | None:
    import questionary

    return collect_selection(
        choose=lambda message, choices: questionary.select(message, choices=choices).ask(),
        checkbox=lambda message, choices: questionary.checkbox(message, choices=choices).ask(),
        host_ids=host_ids,
        profile_ids=profile_ids,
        capability_ids=capability_ids,
    )


def confirm_execution(confirm: Callable[[str], bool | None]) -> bool:
    return confirm("Apply this installation plan?") is True


def prompt_confirmation() -> bool:
    import questionary

    return confirm_execution(lambda message: questionary.confirm(message, default=False).ask())
