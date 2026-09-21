from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from ai_rules.domain.errors import ValidationError
from ai_rules.domain.models import Capability, Host


@dataclass(frozen=True)
class Catalog:
    hosts: dict[str, Host]
    capabilities: dict[str, Capability]

    def require_host(self, host_id: str) -> Host:
        try:
            return self.hosts[host_id]
        except KeyError as exc:
            raise ValidationError(f"unknown host: {host_id}") from exc

    def require_capability(self, capability_id: str) -> Capability:
        try:
            return self.capabilities[capability_id]
        except KeyError as exc:
            raise ValidationError(f"unknown capability: {capability_id}") from exc


def _load_json_resource(name: str) -> dict:
    with resources.files("ai_rules.catalog.data").joinpath(name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_catalog(base_path: Path | None = None) -> Catalog:
    if base_path is None:
        hosts_data = _load_json_resource("hosts.json")
        capabilities_data = _load_json_resource("capabilities.json")
    else:
        with base_path.joinpath("hosts.json").open("r", encoding="utf-8") as handle:
            hosts_data = json.load(handle)
        with base_path.joinpath("capabilities.json").open("r", encoding="utf-8") as handle:
            capabilities_data = json.load(handle)

    hosts = _index("host", [Host.from_dict(item) for item in hosts_data.get("hosts", ())])
    capabilities = _index(
        "capability",
        [Capability.from_dict(item) for item in capabilities_data.get("capabilities", ())],
    )
    _validate_references(capabilities)
    return Catalog(hosts=hosts, capabilities=capabilities)


def _index(kind: str, values):
    indexed = {}
    for value in values:
        if value.id in indexed:
            raise ValidationError(f"duplicate {kind} id: {value.id}")
        indexed[value.id] = value
    return indexed


def _validate_references(capabilities: dict[str, Capability]) -> None:
    for capability in capabilities.values():
        for dependency in (*capability.requires, *capability.recommends):
            if dependency not in capabilities:
                raise ValidationError(f"{capability.id} references missing capability {dependency}")
