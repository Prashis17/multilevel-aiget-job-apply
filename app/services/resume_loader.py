from pathlib import Path

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
    text = "\n".join(page.strip() for page in pages if page.strip())
    if not text:
        raise ResumeLoadError(f"No extractable text found in resume: {resume_path}")
    return text

