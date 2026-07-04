from pathlib import Path

import pytest

from app.services.resume_loader import ResumeLoadError, load_resume_text, normalize_pdf_text


def test_resume_loader_rejects_missing_file() -> None:
    with pytest.raises(ResumeLoadError):
        load_resume_text(Path("missing.pdf"))


def test_normalize_pdf_text_compacts_spaced_words() -> None:
    assert normalize_pdf_text("P r a s h i s  S h i r s a t") == "Prashis Shirsat"
