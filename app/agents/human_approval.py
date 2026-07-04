from app.schemas.workflow import ApprovalTask, WorkflowState


class HumanApprovalAgent:
    def __init__(self, reason: str, kind: str) -> None:
        self.reason = reason
        self.kind = kind

    async def __call__(self, state: WorkflowState) -> WorkflowState:
        task = ApprovalTask(kind=self.kind, reason=self.reason, payload=dict(state))
        state["approval_tasks"] = [*state.get("approval_tasks", []), task.model_dump(mode="json")]
        state["status"] = "pending_approval"
        return state

