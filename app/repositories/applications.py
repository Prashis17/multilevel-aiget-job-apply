from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import Application


class ApplicationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def exists(self, dedupe_hash: str) -> bool:
        result = await self.session.execute(
            select(Application.id).where(Application.dedupe_hash == dedupe_hash)
        )
        return result.scalar_one_or_none() is not None

    async def save(self, application: Application) -> Application:
        self.session.add(application)
        await self.session.commit()
        await self.session.refresh(application)
        return application

    async def analytics(self) -> dict[str, int]:
        result = await self.session.execute(
            select(Application.status, func.count(Application.id)).group_by(Application.status)
        )
        return {status: count for status, count in result.all()}

