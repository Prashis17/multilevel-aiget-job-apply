from app.schemas.workflow import JobAnalysis, JobLead, WorkflowState
from app.services.resume_customizer import ResumeCustomizer


class ResumeCustomizationAgent:
    def __init__(self, customizer: ResumeCustomizer | None = None) -> None:
        self.customizer = customizer or ResumeCustomizer()

    async def __call__(self, state: WorkflowState) -> WorkflowState:
        job = JobLead.model_validate(state["current_job"])
        analysis = JobAnalysis.model_validate(state["analysis"])
        artifacts = await self.customizer.customize(state.get("resume_text", ""), job, analysis)
        state["resume_artifacts"] = artifacts.model_dump()
        return state

