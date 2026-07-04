from app.schemas.workflow import GeneratedEmail, RecruiterContact, WorkflowState
from app.services.email_sender import EmailSender


class EmailSenderAgent:
    def __init__(self, sender: EmailSender | None = None) -> None:
        self.sender = sender or EmailSender()

    async def __call__(self, state: WorkflowState) -> WorkflowState:
        recruiter = RecruiterContact.model_validate(state.get("recruiter", {}))
        email = GeneratedEmail.model_validate(state["email"])
        result = await self.sender.send(recruiter, email)
        state["history"] = [*state.get("history", []), {"step": "email_sender", "result": result}]
        if result.startswith("sent") or result.startswith("dry_run"):
            state["status"] = "email_sent"
        return state

