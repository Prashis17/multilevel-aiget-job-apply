from abc import ABC, abstractmethod

from app.schemas.workflow import JobLead


class JobSource(ABC):
    portal: str

    @abstractmethod
    async def search(self, keywords: list[str], locations: list[str]) -> list[JobLead]:
        raise NotImplementedError


class ConfiguredCareerPageSource(JobSource):
    portal = "career_page"

    async def search(self, keywords: list[str], locations: list[str]) -> list[JobLead]:
        return []


class JobSearchService:
    def __init__(self, sources: list[JobSource] | None = None) -> None:
        self.sources = sources or [ConfiguredCareerPageSource()]

    async def search(self, keywords: list[str], locations: list[str]) -> list[JobLead]:
        leads: list[JobLead] = []
        for source in self.sources:
            leads.extend(await source.search(keywords, locations))
        return leads

