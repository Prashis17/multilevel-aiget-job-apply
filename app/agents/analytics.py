from app.schemas.workflow import WorkflowState


class AnalyticsAgent:
    async def __call__(self, state: WorkflowState) -> WorkflowState:
        state["history"] = [
            *state.get("history", []),
            {
                "step": "analytics",
                "status": state.get("status", "unknown"),
                "errors": len(state.get("errors", [])),
            },
        ]
        return state

