import uuid
from typing import Any, Dict, List, Optional
from app.ai.gemini_client import GeminiClient
from app.ai.langgraph.graph import resume_screening_graph
from app.models.resume import Resume, InterviewQuestion
from app.models.match import MatchScore, EmailLog
from app.repositories.resume_repository import ResumeRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.job_repository import JobRepository
from app.exceptions.custom import EntityNotFoundError, FileStorageError
from app.utils.pagination import PaginationParams


class ResumeService:
    def __init__(
        self,
        resume_repo: ResumeRepository,
        candidate_repo: CandidateRepository,
        job_repo: JobRepository,
        gemini_client: GeminiClient,
    ):
        self.resume_repo = resume_repo
        self.candidate_repo = candidate_repo
        self.job_repo = job_repo
        self.gemini_client = gemini_client

    async def upload_resume(
        self, candidate_id: uuid.UUID, file_name: str, file_content: bytes, organization_id: uuid.UUID
    ) -> Resume:
        # Validate candidate belongs to organization
        candidate = await self.candidate_repo.get_by_id(candidate_id)
        if not candidate or candidate.organization_id != organization_id:
            raise EntityNotFoundError("Candidate not found in this organization.")

        # S3 Interface upload stub
        # In production, we would initialize boto3 client and upload file_content to S3 bucket.
        # s3_client.upload_fileobj(io.BytesIO(file_content), settings.AWS_S3_BUCKET_NAME, s3_key)
        s3_key = f"resumes/{candidate_id}/{uuid.uuid4()}-{file_name}"
        mock_s3_url = f"https://s3.amazonaws.com/hiremind-resumes/{s3_key}"

        # Mock text extraction (since we're only building interfaces here)
        # In a real environment, we'd use PyPDF2 or pdfplumber to convert file_content to text
        raw_text_extracted = f"Resume of {candidate.first_name} {candidate.last_name}.\nFile: {file_name}.\nSkill list: Python, FastAPI, PostgreSQL, Docker, AWS S3. Experience: Software Engineer with 3 years of building REST APIs."

        # Parse resume initially using Gemini
        parsed_result = await self.gemini_client.parse_resume(raw_text_extracted)

        # Create resume model instance
        resume = Resume(
            candidate_id=candidate_id,
            file_url=mock_s3_url,
            file_name=file_name,
            raw_text=raw_text_extracted,
            parsed_content=parsed_result.model_dump(),
            summary=parsed_result.summary,
        )

        return await self.resume_repo.create(resume)

    async def get_resume(self, resume_id: uuid.UUID, organization_id: uuid.UUID) -> Resume:
        resume = await self.resume_repo.get_by_id(resume_id)
        if not resume:
            raise EntityNotFoundError("Resume not found.")

        # Ensure applicant belongs to user's org
        candidate = await self.candidate_repo.get_by_id(resume.candidate_id)
        if not candidate or candidate.organization_id != organization_id:
            raise EntityNotFoundError("Resume does not belong to this organization.")

        return resume

    async def delete_resume(self, resume_id: uuid.UUID, organization_id: uuid.UUID) -> None:
        resume = await self.get_resume(resume_id, organization_id)
        await self.resume_repo.delete(resume)

    async def screen_and_match(
        self, resume_id: uuid.UUID, job_id: uuid.UUID, organization_id: uuid.UUID
    ) -> MatchScore:
        # Validate resume & job
        resume = await self.get_resume(resume_id, organization_id)
        job = await self.job_repo.get_by_id(job_id)
        if not job or job.organization_id != organization_id:
            raise EntityNotFoundError("Job not found under this organization.")

        # Check if match already exists
        existing_match = await self.resume_repo.get_match_score(job_id, resume.candidate_id)
        if existing_match:
            return existing_match

        # Execute the LangGraph screening pipeline!
        inputs = {
            "resume_raw_text": resume.raw_text or "",
            "job_title": job.title,
            "job_description": job.description,
            "job_requirements": job.requirements,
        }
        
        # Run graph workflow
        graph_output = await resume_screening_graph.ainvoke(inputs)

        # Save match score
        score_val = graph_output.get("match_score", 50.0)
        explanation = graph_output.get("fit_explanation", "Standard automated matching profile.")
        gaps = graph_output.get("skill_gap", {})

        match_score = MatchScore(
            job_id=job_id,
            candidate_id=resume.candidate_id,
            resume_id=resume_id,
            score=score_val,
            fit_explanation=explanation,
            skill_gap_analysis=gaps,
        )
        created_match = await self.resume_repo.create_match_score(match_score)

        # Save generated interview questions
        questions = graph_output.get("suggested_questions", [])
        for q in questions:
            iq = InterviewQuestion(
                resume_id=resume_id,
                question=q.get("question", ""),
                expected_answer=q.get("expected_answer", ""),
                category=q.get("category", "General"),
            )
            await self.resume_repo.create_interview_question(iq)

        # Update candidate status in screening
        candidate = await self.candidate_repo.get_by_id(resume.candidate_id)
        if candidate:
            from app.models.candidate import CandidateStatus
            candidate.status = CandidateStatus.SCREENING
            await self.candidate_repo.update(candidate)

        return created_match

    async def get_job_rankings(self, job_id: uuid.UUID, organization_id: uuid.UUID) -> List[MatchScore]:
        job = await self.job_repo.get_by_id(job_id)
        if not job or job.organization_id != organization_id:
            raise EntityNotFoundError("Job not found.")
        return await self.resume_repo.get_match_scores_by_job_id(job_id)

    async def generate_candidate_email(
        self,
        candidate_id: uuid.UUID,
        job_id: uuid.UUID,
        template_type: str,
        sender_id: uuid.UUID,
        organization_id: uuid.UUID,
    ) -> EmailLog:
        candidate = await self.candidate_repo.get_by_id(candidate_id)
        if not candidate or candidate.organization_id != organization_id:
            raise EntityNotFoundError("Candidate not found.")

        job = await self.job_repo.get_by_id(job_id)
        if not job or job.organization_id != organization_id:
            raise EntityNotFoundError("Job not found.")

        # Invoke Gemini Client
        email_data = await self.gemini_client.generate_email(
            template_type=template_type,
            candidate_name=f"{candidate.first_name} {candidate.last_name}",
            job_title=job.title,
            recruiter_name="HireMind Recruiting Team",
        )

        email_log = EmailLog(
            sender_id=sender_id,
            recipient_email=candidate.email,
            subject=email_data.get("subject", f"Update on your application for {job.title}"),
            body=email_data.get("body", ""),
            status="SENT",
        )
        return await self.resume_repo.create_email_log(email_log)

    async def chat_helper(self, query: str, organization_id: uuid.UUID) -> str:
        # Load contextual candidates for this query
        # Fetching candidate names to build context for LLM
        candidates, _ = await self.candidate_repo.list_candidates(organization_id, PaginationParams(size=5))
        context_str = "Available Candidates:\n"
        for c in candidates:
            skills = ", ".join([cs.skill.name for cs in c.candidate_skills])
            context_str += f"- {c.first_name} {c.last_name} (Email: {c.email}, Status: {c.status.value}, Skills: {skills})\n"

        return await self.gemini_client.chat_interaction(query, context_str)

    async def get_dashboard_summary(self, organization_id: uuid.UUID) -> Dict[str, Any]:
        # Perform aggregate lookups using repositories
        _, total_jobs = await self.job_repo.list_jobs(organization_id, PaginationParams(size=1))
        _, total_candidates = await self.candidate_repo.list_candidates(organization_id, PaginationParams(size=1))
        
        # Calculate screening ratios and return dict
        return {
            "total_jobs": total_jobs,
            "total_candidates": total_candidates,
            "active_screenings": total_candidates,  # Mocked dashboard metrics
            "recent_activity": [
                {"event": "Candidate screening complete", "timestamp": "Just now"},
                {"event": "New job post created", "timestamp": "2 hours ago"}
            ]
        }
