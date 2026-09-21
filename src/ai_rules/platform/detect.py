from __future__ import annotations

import platform
import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentInfo:
    os: str
    architecture: str
    python: str
    commands: dict[str, bool]


def detect_environment(commands: tuple[str, ...] = ("git", "npx", "node", "codex", "claude", "opencode", "antigravity")) -> EnvironmentInfo:
    return EnvironmentInfo(
        os=platform.system().lower(),
        architecture=platform.machine().lower(),
        python=platform.python_version(),
        commands={command: shutil.which(command) is not None for command in commands},
    )
