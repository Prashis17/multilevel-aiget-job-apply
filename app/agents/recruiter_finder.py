from app.schemas.workflow import RecruiterContact, WorkflowState


class RecruiterFinderAgent:
    async def __call__(self, state: WorkflowState) -> WorkflowState:
        job = state["current_job"]
        contact = RecruiterContact(
            name=None,
            designation="Recruiting Team",
            email=None,
            confidence_score=0.25,
            source="placeholder_public_search_adapter",
        )
        state["recruiter"] = contact.model_dump()
        return state
