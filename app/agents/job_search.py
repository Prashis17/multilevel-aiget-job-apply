from app.schemas.workflow import JobLead, WorkflowState
from app.services.job_sources import JobSearchService
from app.services.dedupe import job_dedupe_hash


class JobSearchAgent:
    def __init__(self, service: JobSearchService | None = None) -> None:
        self.service = service or JobSearchService()

    async def __call__(self, state: WorkflowState) -> WorkflowState:
        profile = state.get("profile", {})
        keywords = state.get("keywords", []) or profile.get("skills", [])[:3]
        locations = state.get("locations", []) or profile.get("preferred_locations", ["Remote"])
        leads = await self.service.search(keywords, locations)
        for lead in leads:
            lead.duplicate_hash = job_dedupe_hash(lead)
        state["history"] = [*state.get("history", []), {"step": "job_search", "count": len(leads)}]
        if leads:
            state["current_job"] = leads[0].model_dump(mode="json")
        return state

