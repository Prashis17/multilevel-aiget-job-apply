from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ResumeVersion(TimestampMixin, Base):
    __tablename__ = "resume_versions"
    __table_args__ = (UniqueConstraint("version_hash", name="uq_resume_versions_hash"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    profile_name: Mapped[str] = mapped_column(String(255), default="default")
    resume_pdf_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_docx_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_letter_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    version_hash: Mapped[str] = mapped_column(String(64), index=True)

