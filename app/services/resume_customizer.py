from pathlib import Path

from app.schemas.workflow import JobAnalysis, JobLead, ResumeArtifacts
from app.utils.hashing import stable_hash


class ResumeCustomizer:
    def __init__(self, output_dir: Path = Path("generated/resumes")) -> None:
        self.output_dir = output_dir

    async def customize(self, resume_text: str, job: JobLead, analysis: JobAnalysis) -> ResumeArtifacts:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        version_hash = stable_hash(resume_text, job.company, job.title, ",".join(analysis.ats_keywords))
        cover_letter_path = self.output_dir / f"{version_hash}_cover_letter.txt"
        cover_letter_path.write_text(
            (
                f"Cover letter for {job.title} at {job.company}\n\n"
                f"Relevant keywords: {', '.join(analysis.ats_keywords)}\n"
                "This draft must be reviewed before sending."
            ),
            encoding="utf-8",
        )
        return ResumeArtifacts(cover_letter_path=str(cover_letter_path), version_hash=version_hash)

