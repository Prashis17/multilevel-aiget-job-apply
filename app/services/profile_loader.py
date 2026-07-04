from pathlib import Path
from typing import Any

import yaml

from app.schemas.profile import CandidateProfile


class ProfileLoadError(RuntimeError):
    pass


def load_local_profile(path: Path = Path("data/profile.yaml")) -> CandidateProfile:
    if not path.exists():
        raise ProfileLoadError(f"Local profile file does not exist: {path}")
    with path.open("r", encoding="utf-8") as profile_file:
        payload: dict[str, Any] = yaml.safe_load(profile_file) or {}
    return CandidateProfile.model_validate(payload)


def load_target_role(path: Path = Path("data/profile.yaml")) -> str:
    if not path.exists():
        return "Product Manager"
    with path.open("r", encoding="utf-8") as profile_file:
        payload: dict[str, Any] = yaml.safe_load(profile_file) or {}
    return str(payload.get("target_role") or "Product Manager")

