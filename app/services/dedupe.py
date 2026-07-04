from app.schemas.workflow import JobLead
from app.utils.hashing import stable_hash


def job_dedupe_hash(job: JobLead) -> str:
    return stable_hash(job.company, job.title, str(job.url))


def email_dedupe_hash(recipient: str, company: str, title: str) -> str:
    return stable_hash(recipient, company, title)


def semantic_similarity_bucket(company: str, title: str, description: str) -> str:
    return stable_hash(company, title, description[:500])

