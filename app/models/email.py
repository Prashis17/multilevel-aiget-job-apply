from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class EmailLog(TimestampMixin, Base):
    __tablename__ = "email_logs"
    __table_args__ = (UniqueConstraint("dedupe_hash", name="uq_email_logs_dedupe_hash"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    recipient: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(100), default="pending")
    dedupe_hash: Mapped[str] = mapped_column(String(64), index=True)

