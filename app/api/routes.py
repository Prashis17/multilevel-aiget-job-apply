from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.graphs.supervisor import build_supervisor_graph
from app.repositories.applications import ApplicationRepository
from app.repositories.jobs import JobRepository
from app.schemas.workflow import CampaignRequest, JobLead, WorkflowState
from app.agents.email_generator import EmailGeneratorAgent
from app.agents.human_approval import HumanApprovalAgent
from app.agents.job_analyzer import JobAnalyzerAgent
from app.agents.recruiter_finder import RecruiterFinderAgent
from app.services.profile_loader import load_local_profile, load_target_role
from app.services.resume_loader import load_resume_text

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
        "resume_text": request.resume_text or load_resume_text(),
        "keywords": request.keywords,
        "locations": request.locations,
        "retry_count": 0,
        "errors": [],
        "logs": [],
        "history": [],
    }
    return await graph.ainvoke(initial_state)


@router.get("/profile/local")
async def local_profile() -> dict:
    profile = load_local_profile()
    return {
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "location": profile.location,
        "target_role": load_target_role(),
        "skills": profile.skills,
        "experience_years": profile.experience_years,
        "preferred_locations": profile.preferred_locations,
    }


@router.post("/campaigns/run-local")
async def run_local_campaign() -> WorkflowState:
    profile = load_local_profile()
    request = CampaignRequest(
        profile=profile,
        keywords=[load_target_role(), "Product Manager", "Associate Product Manager"],
        locations=profile.preferred_locations or ["Remote", "Bengaluru", "Mumbai", "Pune"],
    )
    return await run_campaign(request)


@router.post("/campaigns/product-manager-dry-run")
async def product_manager_dry_run() -> WorkflowState:
    profile = load_local_profile()
    job = JobLead(
        company="Demo Product Company",
        title="Product Manager",
        location="Remote / India",
        experience="2+ years",
        salary="Not disclosed",
        url="https://example.com/product-manager-demo",
        portal="manual_demo",
        posting_time="dry run",
        description=(
            "We are hiring a Product Manager to own user research, roadmap planning, "
            "analytics, experimentation, stakeholder alignment, product discovery, "
            "PRDs, feature launches, funnel analysis, customer feedback loops, and "
            "cross-functional delivery with design, engineering, sales, and operations."
        ),
        employment_type="Full-time",
        skills_required=[
            "Product Management",
            "User Research",
            "Analytics",
            "SQL",
            "A/B Testing",
            "Roadmapping",
            "PRDs",
            "Stakeholder Management",
        ],
    )
    state: WorkflowState = {
        "campaign_id": "product-manager-dry-run",
        "profile": profile.model_dump(mode="json"),
        "resume_text": load_resume_text(),
        "current_job": job.model_dump(mode="json"),
        "retry_count": 0,
        "errors": [],
        "logs": [],
        "history": [],
    }
    for agent in [
        JobAnalyzerAgent(),
        RecruiterFinderAgent(),
        EmailGeneratorAgent(),
        HumanApprovalAgent("Review Product Manager dry-run email draft", "email"),
    ]:
        state = await agent(state)
    return state


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
