import os
import uuid
from typing import Any, Dict, List, Optional
from app.ai.clients.gemini import GeminiClient
from app.ai.graph.graph import resume_screening_graph
from app.models.resume import Resume, InterviewQuestion
from app.models.match import MatchScore, EmailLog
from app.repositories.resume_repository import ResumeRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.job_repository import JobRepository
from app.exceptions.custom import EntityNotFoundError, FileStorageError
from app.utils.pagination import PaginationParams
from app.utils.text_extractor import extract_text


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

    async def _save_local(self, candidate_id: uuid.UUID, file_name: str, file_content: bytes) -> str:
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads")
        candidate_dir = os.path.join(uploads_dir, str(candidate_id))
        os.makedirs(candidate_dir, exist_ok=True)
        
        saved_filename = f"{uuid.uuid4()}-{file_name}"
        file_path = os.path.join(candidate_dir, saved_filename)
        try:
            with open(file_path, "wb") as f:
                f.write(file_content)
        except Exception as e:
            raise FileStorageError(f"Failed to save file locally: {e}")
        return f"/uploads/{candidate_id}/{saved_filename}"

    async def upload_resume(
        self,
        candidate_id: Optional[uuid.UUID],
        file_name: str,
        file_content: bytes,
        organization_id: uuid.UUID,
    ) -> Resume:
        # Extract raw text content from the uploaded resume file (PDF or DOCX)
        raw_text_extracted = extract_text(file_name, file_content)
        if not raw_text_extracted:
            raw_text_extracted = f"Resume document: {file_name}.\n"

        # Parse resume using Gemini LLM
        parsed_result = await self.gemini_client.parse_resume(raw_text_extracted)
        parsed_dict = parsed_result.model_dump() if hasattr(parsed_result, "model_dump") else dict(parsed_result)
        candidate_info = parsed_dict.get("candidate_info", {})

        candidate = None
        if candidate_id:
            candidate = await self.candidate_repo.get_by_id(candidate_id)
            if not candidate or candidate.organization_id != organization_id:
                raise EntityNotFoundError("Candidate not found in this organization.")
        else:
            # Auto-create candidate profile from extracted resume info
            from app.models.candidate import Candidate, CandidateStatus
            extracted_first = candidate_info.get("first_name") or "Applicant"
            extracted_last = candidate_info.get("last_name") or "Candidate"
            extracted_email = candidate_info.get("email") or f"applicant_{uuid.uuid4().hex[:8]}@extracted.com"
            extracted_phone = candidate_info.get("phone")

            new_cand = Candidate(
                organization_id=organization_id,
                first_name=extracted_first,
                last_name=extracted_last,
                email=extracted_email,
                phone=extracted_phone,
                status=CandidateStatus.NEW,
            )
            candidate = await self.candidate_repo.create(new_cand)
            candidate_id = candidate.id

        # Update candidate attributes if extracted details are richer or candidate has placeholders
        if candidate_info:
            ext_first = candidate_info.get("first_name")
            ext_last = candidate_info.get("last_name")
            ext_email = candidate_info.get("email")
            ext_phone = candidate_info.get("phone")

            updated = False
            if ext_first and ext_first.strip() and ext_first not in ["Applicant", "Candidate"]:
                candidate.first_name = ext_first.strip()
                updated = True
            if ext_last and ext_last.strip() and ext_last not in ["Applicant", "Candidate"]:
                candidate.last_name = ext_last.strip()
                updated = True
            if ext_email and ext_email.strip() and "example.com" not in ext_email:
                candidate.email = ext_email.strip()
                updated = True
            if ext_phone and ext_phone.strip():
                candidate.phone = ext_phone.strip()
                updated = True

            if updated:
                await self.candidate_repo.update(candidate)

        # Upload to AWS S3 if credentials are set, otherwise use local storage
        from app.core.config import settings
        import boto3
        
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            try:
                import io
                s3_key = f"resumes/{candidate_id}/{uuid.uuid4()}-{file_name}"
                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION
                )
                s3_client.upload_fileobj(io.BytesIO(file_content), settings.AWS_S3_BUCKET_NAME, s3_key)
                file_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            except Exception:
                file_url = await self._save_local(candidate_id, file_name, file_content)
        else:
            file_url = await self._save_local(candidate_id, file_name, file_content)

        # Populate CandidateSkill table with extracted skills
        skills_list = parsed_result.skills if hasattr(parsed_result, "skills") else []
        if not skills_list and hasattr(parsed_result, "model_dump"):
            skills_list = parsed_result.model_dump().get("skills", [])

        if skills_list:
            from app.models.candidate import CandidateSkill
            for skill_name in skills_list:
                if not skill_name or not isinstance(skill_name, str):
                    continue
                clean_name = skill_name.strip()
                if not clean_name:
                    continue
                skill = await self.candidate_repo.get_skill_by_name(clean_name)
                if not skill:
                    skill = await self.candidate_repo.create_skill(clean_name)

                cs = CandidateSkill(
                    candidate_id=candidate_id,
                    skill_id=skill.id,
                    proficiency="Proficient",
                )
                try:
                    await self.candidate_repo.add_candidate_skill(cs)
                except Exception:
                    pass

        # Create resume model instance
        resume = Resume(
            candidate_id=candidate_id,
            file_url=file_url,
            file_name=file_name,
            raw_text=raw_text_extracted,
            parsed_content=parsed_dict,
            summary=parsed_result.summary if hasattr(parsed_result, "summary") else parsed_dict.get("summary"),
        )

        created_resume = await self.resume_repo.create(resume)
        fetched_resume = await self.resume_repo.get_by_id(created_resume.id)
        return fetched_resume or created_resume

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
        score_val = graph_output.get("match_score", 75.0)
        explanation = graph_output.get("fit_explanation") or graph_output.get("hiring_recommendation") or "Automated AI candidate match evaluation completed."
        gaps = graph_output.get("skill_gap", {})

        matching_skills = graph_output.get("matching_skills", [])
        missing_skills = gaps.get("missing_skills") or graph_output.get("missing_skills", [])
        additional_skills = gaps.get("priority_skills") or gaps.get("strengths") or []

        skill_gap_analysis = {
            "matched_skills": matching_skills,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "recommended_learning": gaps.get("recommended_learning", []),
            "strengths": gaps.get("strengths", []),
            "weaknesses": gaps.get("weaknesses", []),
        }

        # Check if match already exists
        existing_match = await self.resume_repo.get_match_score(job_id, resume.candidate_id)
        if existing_match:
            existing_match.score = score_val
            existing_match.fit_explanation = explanation
            existing_match.skill_gap_analysis = skill_gap_analysis
            created_match = await self.resume_repo.create_match_score(existing_match)
        else:
            match_score = MatchScore(
                job_id=job_id,
                candidate_id=resume.candidate_id,
                resume_id=resume_id,
                score=score_val,
                fit_explanation=explanation,
                skill_gap_analysis=skill_gap_analysis,
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

        body_text = email_data.get("body") or email_data.get("email_body") or email_data.get("content") or ""

        email_log = EmailLog(
            sender_id=sender_id,
            recipient_email=candidate.email,
            subject=email_data.get("subject", f"Update on your application for {job.title}"),
            body=body_text,
            status="SENT",
        )
        return await self.resume_repo.create_email_log(email_log)

    async def chat_helper(self, query: str, organization_id: Optional[uuid.UUID]) -> str:
        # Load contextual candidates for this query
        context_str = "Available Candidates:\n"
        if organization_id:
            candidates, _ = await self.candidate_repo.list_candidates(
                organization_id, skip=0, limit=10
            )
            for c in candidates:
                skills = ", ".join([cs.skill.name for cs in (c.candidate_skills or [])])
                context_str += f"- {c.first_name} {c.last_name} (Email: {c.email}, Status: {c.status.value}, Skills: {skills})\n"
        else:
            context_str += "(No candidates found — user has no organization assigned.)\n"

        return await self.gemini_client.chat_interaction(query, context_str)

    async def get_dashboard_summary(self, organization_id: uuid.UUID) -> Dict[str, Any]:
        # Perform aggregate lookups using repositories
        _, total_jobs = await self.job_repo.list_jobs(organization_id, skip=0, limit=1)
        _, total_candidates = await self.candidate_repo.list_candidates(organization_id, skip=0, limit=1)
        
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

    async def _save_local(self, candidate_id: uuid.UUID, file_name: str, file_content: bytes) -> str:
        """Save uploaded resume file locally and return static file URL path."""
        import os
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        uploads_dir = os.path.join(backend_dir, "uploads", "resumes", str(candidate_id))
        os.makedirs(uploads_dir, exist_ok=True)

        safe_filename = f"{uuid.uuid4()}-{file_name}"
        file_path = os.path.join(uploads_dir, safe_filename)

        with open(file_path, "wb") as f:
            f.write(file_content)

        return f"/uploads/resumes/{candidate_id}/{safe_filename}"
