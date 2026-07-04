from app.llm.providers import get_llm_client
from app.schemas.workflow import GeneratedEmail, JobLead, RecruiterContact, WorkflowState


class EmailGeneratorAgent:
    async def __call__(self, state: WorkflowState) -> WorkflowState:
        job = JobLead.model_validate(state["current_job"])
        recruiter = RecruiterContact.model_validate(state.get("recruiter", {}))
        profile = state.get("profile", {})
        llm = get_llm_client()
        system = "Write concise, truthful recruiting outreach. Never invent experience."
        user = (
            f"Candidate: {profile}\nRecruiter: {recruiter.model_dump()}\n"
            f"Job: {job.model_dump()}\nResume: {state.get('resume_text', '')[:5000]}"
        )
        draft = await llm.generate(system, user)
        email = GeneratedEmail(
            subject=f"Application for {job.title} at {job.company}",
            body=draft,
            signature=profile.get("full_name", "Candidate"),
            follow_up_1=f"Following up on my interest in the {job.title} role.",
            follow_up_2=f"Checking once more regarding the {job.title} opening.",
        )
        state["email"] = email.model_dump()
        return state

