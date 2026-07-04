from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.schemas.workflow import JobLead
from app.utils.hashing import stable_hash


class JobRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert_lead(self, lead: JobLead) -> Job:
        duplicate_hash = lead.duplicate_hash or stable_hash(lead.company, lead.title, str(lead.url))
        existing = await self.get_by_hash(duplicate_hash)
        if existing:
            return existing
        job = Job(
            company=lead.company,
            title=lead.title,
            portal=lead.portal,
            url=str(lead.url),
            location=lead.location,
            description=lead.description,
            duplicate_hash=duplicate_hash,
        )
        self.session.add(job)
        await self.session.commit()
        await self.session.refresh(job)
        return job

    async def get_by_hash(self, duplicate_hash: str) -> Job | None:
        result = await self.session.execute(select(Job).where(Job.duplicate_hash == duplicate_hash))
        return result.scalar_one_or_none()

    async def list_recent(self, limit: int = 100) -> list[Job]:
        result = await self.session.execute(select(Job).order_by(Job.created_at.desc()).limit(limit))
        return list(result.scalars().all())

