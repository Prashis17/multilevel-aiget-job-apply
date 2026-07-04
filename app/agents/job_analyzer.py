import json

from app.llm.providers import get_llm_client
from app.schemas.workflow import JobAnalysis, JobLead, WorkflowState


class JobAnalyzerAgent:
    async def __call__(self, state: WorkflowState) -> WorkflowState:
        job = JobLead.model_validate(state["current_job"])
        resume_text = state.get("resume_text", "")
        llm = get_llm_client()
        prompt = (
            "Return strict JSON with skills, mandatory_requirements, preferred_requirements, "
            "ats_keywords, priority_score, match_score, category, salary_range, "
            "company_reputation_score, response_prediction."
        )
        response = await llm.generate(prompt, f"Resume:\n{resume_text}\n\nJob:\n{job.description}")
        analysis = self._parse_analysis(response, job, resume_text)
        state["analysis"] = analysis.model_dump()
        state["status"] = "analyzed"
        return state

    def _parse_analysis(self, response: str, job: JobLead, resume_text: str) -> JobAnalysis:
        try:
            payload = json.loads(response)
            return JobAnalysis.model_validate(payload)
        except Exception:
            resume_words = set(resume_text.lower().split())
            jd_words = set(job.description.lower().split())
            overlap = len(resume_words & jd_words)
            score = min(overlap / max(len(jd_words), 1), 1.0)
            return JobAnalysis(
                skills=job.skills_required,
                ats_keywords=list((resume_words & jd_words))[:20],
                priority_score=score,
                match_score=score,
                category="High Match" if score >= 0.72 else "Medium Match" if score >= 0.5 else "Low Match",
            )

