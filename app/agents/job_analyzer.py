import json

from app.llm.providers import get_llm_client
from app.schemas.workflow import JobAnalysis, JobLead, WorkflowState


class JobAnalyzerAgent:
    async def __call__(self, state: WorkflowState) -> WorkflowState:
        job = JobLead.model_validate(state["current_job"])
        resume_text = state.get("resume_text", "")
        profile_text = json.dumps(state.get("profile", {}))
        candidate_text = f"{resume_text}\n{profile_text}"
        llm = get_llm_client()
        prompt = (
            "Return strict JSON with skills, mandatory_requirements, preferred_requirements, "
            "ats_keywords, priority_score, match_score, category, salary_range, "
            "company_reputation_score, response_prediction."
        )
        response = await llm.generate(prompt, f"Resume:\n{candidate_text}\n\nJob:\n{job.description}")
        analysis = self._parse_analysis(response, job, candidate_text)
        state["analysis"] = analysis.model_dump()
        state["status"] = "analyzed"
        return state

    def _parse_analysis(self, response: str, job: JobLead, resume_text: str) -> JobAnalysis:
        try:
            payload = json.loads(response)
            analysis = JobAnalysis.model_validate(payload)
            if analysis.match_score > 0:
                return analysis
            return self._heuristic_analysis(job, resume_text)
        except Exception:
            return self._heuristic_analysis(job, resume_text)

    def _heuristic_analysis(self, job: JobLead, resume_text: str) -> JobAnalysis:
        resume_lower = resume_text.lower()
        skill_hits = [
            skill
            for skill in job.skills_required
            if all(token in resume_lower for token in skill.lower().replace("/", " ").split())
        ]
        jd_keywords = {
            word.strip(".,:;()[]{}")
            for word in job.description.lower().split()
            if len(word.strip(".,:;()[]{}")) >= 5
        }
        resume_words = set(resume_lower.split())
        keyword_hits = sorted(jd_keywords & resume_words)
        skill_score = len(skill_hits) / max(len(job.skills_required), 1)
        keyword_score = min(len(keyword_hits) / 20, 1.0)
        score = round((skill_score * 0.7) + (keyword_score * 0.3), 2)
        return JobAnalysis(
            skills=skill_hits or job.skills_required,
            mandatory_requirements=job.skills_required,
            preferred_requirements=[],
            ats_keywords=list(dict.fromkeys([*skill_hits, *keyword_hits]))[:30],
            priority_score=score,
            match_score=score,
            category="High Match" if score >= 0.72 else "Medium Match" if score >= 0.5 else "Low Match",
            salary_range=job.salary,
        )
