from pathlib import Path

import pytest

from app.services.resume_loader import ResumeLoadError, load_resume_text


def test_resume_loader_rejects_missing_file() -> None:
    with pytest.raises(ResumeLoadError):
        load_resume_text(Path("missing.pdf"))

