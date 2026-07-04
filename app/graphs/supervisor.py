from langgraph.graph import END, StateGraph

from app.agents.analytics import AnalyticsAgent
from app.agents.easy_apply import EasyApplyAgent
from app.agents.email_generator import EmailGeneratorAgent
from app.agents.email_sender import EmailSenderAgent
from app.agents.human_approval import HumanApprovalAgent
from app.agents.job_analyzer import JobAnalyzerAgent
from app.agents.job_search import JobSearchAgent
from app.agents.recruiter_finder import RecruiterFinderAgent
from app.agents.resume_customizer import ResumeCustomizationAgent
from app.config.settings import get_settings
from app.schemas.workflow import JobAnalysis, WorkflowState


def should_continue_after_analysis(state: WorkflowState) -> str:
    threshold = get_settings().yaml_config.get("workflow", {}).get("match_threshold", 0.72)
    analysis = JobAnalysis.model_validate(state.get("analysis", {}))
    return "recruiter_finder" if analysis.match_score >= threshold else "analytics"


def approval_route(state: WorkflowState) -> str:
    mode = get_settings().yaml_config.get("workflow", {}).get("mode", "manual_approval")
    if mode in {"manual_approval", "before_email"}:
        return "approval_before_email"
    return "email_sender"


def build_supervisor_graph():
    graph = StateGraph(WorkflowState)
    graph.add_node("job_search", JobSearchAgent())
    graph.add_node("job_analyzer", JobAnalyzerAgent())
    graph.add_node("recruiter_finder", RecruiterFinderAgent())
    graph.add_node("email_generator", EmailGeneratorAgent())
    graph.add_node("approval_before_email", HumanApprovalAgent("Review generated email", "email"))
    graph.add_node("email_sender", EmailSenderAgent())
    graph.add_node("resume_customizer", ResumeCustomizationAgent())
    graph.add_node("approval_before_apply", HumanApprovalAgent("Review application before apply", "apply"))
    graph.add_node("easy_apply", EasyApplyAgent())
    graph.add_node("analytics", AnalyticsAgent())

    graph.set_entry_point("job_search")
    graph.add_edge("job_search", "job_analyzer")
    graph.add_conditional_edges(
        "job_analyzer",
        should_continue_after_analysis,
        {"recruiter_finder": "recruiter_finder", "analytics": "analytics"},
    )
    graph.add_edge("recruiter_finder", "email_generator")
    graph.add_conditional_edges(
        "email_generator",
        approval_route,
        {"approval_before_email": "approval_before_email", "email_sender": "email_sender"},
    )
    graph.add_edge("approval_before_email", "analytics")
    graph.add_edge("email_sender", "resume_customizer")
    graph.add_edge("resume_customizer", "approval_before_apply")
    graph.add_edge("approval_before_apply", "analytics")
    graph.add_edge("easy_apply", "analytics")
    graph.add_edge("analytics", END)
    return graph.compile()

