from datetime import datetime
from enum import StrEnum
from typing import Any, TypedDict

from pydantic import BaseModel, Field, HttpUrl

from app.schemas.profile import CandidateProfile


class ApprovalMode(StrEnum):
    automatic = "automatic"
    manual_approval = "manual_approval"
    before_email = "before_email"
    before_apply = "before_apply"
    before_resume_customization = "before_resume_customization"


class ApplicationStatus(StrEnum):
    discovered = "discovered"
    analyzed = "analyzed"
    pending_approval = "pending_approval"
    email_sent = "email_sent"
    applied = "applied"
    failed = "failed"
    rejected = "rejected"
    interview = "interview"
    offer = "offer"


class JobLead(BaseModel):
    company: str
    title: str
    location: str | None = None
    experience: str | None = None
    salary: str | None = None
    url: HttpUrl
    portal: str
    posting_time: str | None = None
    description: str
    employment_type: str | None = None
    skills_required: list[str] = []
    duplicate_hash: str | None = None


class JobAnalysis(BaseModel):
    skills: list[str] = []
    mandatory_requirements: list[str] = []
    preferred_requirements: list[str] = []
    ats_keywords: list[str] = []
    priority_score: float = Field(ge=0, le=1, default=0)
    match_score: float = Field(ge=0, le=1, default=0)
    category: str = "Low Match"
    salary_range: str | None = None
    company_reputation_score: float | None = Field(default=None, ge=0, le=1)
    response_prediction: float | None = Field(default=None, ge=0, le=1)


class RecruiterContact(BaseModel):
    name: str | None = None
    designation: str | None = None
    email: str | None = None
    linkedin_url: str | None = None
    confidence_score: float = Field(default=0, ge=0, le=1)
    source: str | None = None


class GeneratedEmail(BaseModel):
    subject: str
    body: str
    signature: str
    follow_up_1: str
    follow_up_2: str


class ResumeArtifacts(BaseModel):
    resume_pdf_path: str | None = None
    resume_docx_path: str | None = None
    cover_letter_path: str | None = None
    version_hash: str | None = None


class ApprovalTask(BaseModel):
    kind: str
    reason: str
    payload: dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WorkflowState(TypedDict, total=False):
    campaign_id: str
    current_job: dict[str, Any]
    profile: dict[str, Any]
    resume_text: str
    analysis: dict[str, Any]
    recruiter: dict[str, Any]
    email: dict[str, Any]
    resume_artifacts: dict[str, Any]
    status: str
    current_step: str
    retry_count: int
    errors: list[str]
    logs: list[str]
    history: list[dict[str, Any]]
    approval_tasks: list[dict[str, Any]]


class CampaignRequest(BaseModel):
    profile: CandidateProfile
    resume_text: str = ""
    keywords: list[str] = []
    locations: list[str] = []
    approval_mode: ApprovalMode = ApprovalMode.manual_approval
