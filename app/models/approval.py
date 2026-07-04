from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Approval(TimestampMixin, Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(100), default="pending", index=True)
    reason: Mapped[str] = mapped_column(String(512))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)

