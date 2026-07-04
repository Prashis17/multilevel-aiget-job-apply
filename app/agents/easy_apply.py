from app.schemas.workflow import JobLead, WorkflowState
from app.services.easy_apply import EasyApplyService


class EasyApplyAgent:
    def __init__(self, service: EasyApplyService | None = None) -> None:
        self.service = service or EasyApplyService()

    async def __call__(self, state: WorkflowState) -> WorkflowState:
        job = JobLead.model_validate(state["current_job"])
        result = await self.service.apply(job, state.get("generated_answers", {}))
        state["history"] = [*state.get("history", []), {"step": "easy_apply", "result": result}]
        state["status"] = "applied" if result["status"] == "submitted" else result["status"]
        return state

