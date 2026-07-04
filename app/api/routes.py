from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.graphs.supervisor import build_supervisor_graph
from app.repositories.applications import ApplicationRepository
from app.repositories.jobs import JobRepository
from app.schemas.workflow import CampaignRequest, JobLead, WorkflowState

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/campaigns/run")
async def run_campaign(request: CampaignRequest) -> WorkflowState:
    graph = build_supervisor_graph()
    initial_state: WorkflowState = {
        "campaign_id": "manual",
        "profile": request.profile.model_dump(mode="json"),
        "resume_text": request.resume_text,
        "keywords": request.keywords,
        "locations": request.locations,
        "retry_count": 0,
        "errors": [],
        "logs": [],
        "history": [],
    }
    return await graph.ainvoke(initial_state)


@router.post("/jobs")
async def create_job(lead: JobLead, session: AsyncSession = Depends(get_session)) -> dict[str, int]:
    job = await JobRepository(session).upsert_lead(lead)
    return {"id": job.id}


@router.get("/jobs")
async def list_jobs(session: AsyncSession = Depends(get_session)) -> list[dict]:
    jobs = await JobRepository(session).list_recent()
    return [
        {
            "id": job.id,
            "company": job.company,
            "title": job.title,
            "portal": job.portal,
            "status": job.status,
            "match_score": job.match_score,
        }
        for job in jobs
    ]


@router.get("/analytics")
async def analytics(session: AsyncSession = Depends(get_session)) -> dict[str, int]:
    return await ApplicationRepository(session).analytics()

