from pathlib import Path
import re

from pypdf import PdfReader

from app.config.settings import get_settings


class ResumeLoadError(RuntimeError):
    pass


def get_configured_resume_path() -> Path:
    profile_config = get_settings().yaml_config.get("profile", {})
    resume_path = profile_config.get("resume_path")
    if not resume_path:
        raise ResumeLoadError("No profile.resume_path configured.")
    return Path(resume_path)


def load_resume_text(path: Path | None = None) -> str:
    resume_path = path or get_configured_resume_path()
    if not resume_path.exists():
        raise ResumeLoadError(f"Resume file does not exist: {resume_path}")
    if resume_path.suffix.lower() != ".pdf":
        raise ResumeLoadError("Only PDF resume extraction is currently supported.")

    reader = PdfReader(str(resume_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = normalize_pdf_text("\n".join(page.strip() for page in pages if page.strip()))
    if not text:
        raise ResumeLoadError(f"No extractable text found in resume: {resume_path}")
    return text


def normalize_pdf_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        parts = re.split(r"(\s{2,})", line)
        normalized_parts = []
        for part in parts:
            if re.fullmatch(r"\s{2,}", part):
                normalized_parts.append(" ")
            elif _looks_like_spaced_word(part):
                normalized_parts.append(part.replace(" ", ""))
            else:
                normalized_parts.append(part)
        lines.append("".join(normalized_parts).strip())
    return "\n".join(line for line in lines if line)


def _looks_like_spaced_word(value: str) -> bool:
    compact = value.replace(" ", "")
    if len(compact) < 2:
        return False
    single_char_tokens = re.findall(r"\b[A-Za-z0-9]\b", value)
    return len(single_char_tokens) >= 2 and len(single_char_tokens) >= len(compact) * 0.7

