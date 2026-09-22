from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from ai_rules.catalog.loader import Catalog
from ai_rules.domain.errors import ValidationError
from ai_rules.domain.models import Profile


@dataclass(frozen=True)
class ProfileSet:
    profiles: dict[str, Profile]

    def require(self, profile_id: str) -> Profile:
        profile_id = {
            "recommended": "engineering", "web-development": "minimal", "design": "minimal",
            "media": "minimal", "reverse-engineering": "minimal",
        }.get(profile_id, profile_id)
        try:
            return self.profiles[profile_id]
        except KeyError as exc:
            raise ValidationError(f"unknown profile: {profile_id}") from exc

    @property
    def default(self) -> Profile:
        defaults = [profile for profile in self.profiles.values() if profile.default]
        if len(defaults) != 1:
            raise ValidationError("exactly one default profile is required")
        if defaults[0].id == "everything":
            raise ValidationError("Everything profile must not be default")
        return defaults[0]


def load_profiles(catalog: Catalog, base_path: Path | None = None) -> ProfileSet:
    if base_path is None:
        with resources.files("ai_rules.profiles.data").joinpath("profiles.json").open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    else:
        with base_path.joinpath("profiles.json").open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    profiles = _index([Profile.from_dict(item) for item in data.get("profiles", ())])
    profile_set = ProfileSet(profiles=profiles)
    _ = profile_set.default
    _validate_profile_references(profile_set, catalog)
    return profile_set


def _index(values: list[Profile]) -> dict[str, Profile]:
    indexed: dict[str, Profile] = {}
    for value in values:
        if value.id in indexed:
            raise ValidationError(f"duplicate profile id: {value.id}")
        indexed[value.id] = value
    return indexed


def _validate_profile_references(profile_set: ProfileSet, catalog: Catalog) -> None:
    for profile in profile_set.profiles.values():
        for capability_id in (*profile.capabilities, *profile.suggested):
            catalog.require_capability(capability_id)
