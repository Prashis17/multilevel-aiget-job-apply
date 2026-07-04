import hashlib
import re


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def stable_hash(*parts: str) -> str:
    payload = "|".join(normalize_text(part) for part in parts if part)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

