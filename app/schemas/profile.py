from pydantic import BaseModel, EmailStr, HttpUrl


class Education(BaseModel):
    institution: str
    degree: str
    start_year: int | None = None
    end_year: int | None = None


class Project(BaseModel):
    name: str
    summary: str
    skills: list[str] = []
    url: HttpUrl | None = None


class CandidateProfile(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    location: str
    skills: list[str]
    experience_years: float
    current_company: str | None = None
    current_ctc: str | None = None
    expected_ctc: str | None = None
    notice_period: str | None = None
    linkedin_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    portfolio_url: HttpUrl | None = None
    work_authorization: str | None = None
    visa_status: str | None = None
    education: list[Education] = []
    projects: list[Project] = []
    preferred_locations: list[str] = []
    preferred_answers: dict[str, str] = {}

