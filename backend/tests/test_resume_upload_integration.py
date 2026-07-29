import asyncio
import sys
import os

sys.path.insert(0, os.getcwd())

import app.db.base  # ensure models are imported and registered
from app.db.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.organization import Organization
from app.models.candidate import Candidate, CandidateStatus
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.resume_repository import ResumeRepository
from app.repositories.job_repository import JobRepository
from app.services.resume_service import ResumeService


class ParsedResume:
    def __init__(self, parsed: dict, summary: str = "Parsed summary"):
        self._parsed = parsed
        self.summary = summary

    def model_dump(self):
        return self._parsed


class FakeGeminiClient:
    async def parse_resume(self, text: str) -> ParsedResume:
        # Return a minimal parsed structure compatible with ResumeService expectations
        return ParsedResume({"name": "Rounak Mishra", "skills": ["Python", "FastAPI"]}, summary="Test summary")


def _run_async_upload_test():
    async def _inner():
        async with AsyncSessionLocal() as session:
            cand_repo = CandidateRepository(session)
            res_repo = ResumeRepository(session)
            job_repo = JobRepository(session)

            result = await session.execute(select(Candidate))
            candidate = result.scalars().first()
            if not candidate:
                org = Organization(name="Test Org")
                session.add(org)
                await session.flush()
                org_id = org.id
                candidate = Candidate(
                    organization_id=org_id,
                    first_name="Rounak",
                    last_name="Mishra",
                    email="mishra.rounak15@gmail.com",
                    phone="+919852637240",
                    status=CandidateStatus.NEW,
                )
                session.add(candidate)
                await session.flush()
            else:
                org_id = candidate.organization_id

            fake_gemini = FakeGeminiClient()
            service = ResumeService(res_repo, cand_repo, job_repo, fake_gemini)

            file_name = "Rounak_Mishra.txt"
            file_content = b"Sample resume content for testing."

            resume = await service.upload_resume(candidate.id, file_name, file_content, org_id)

            assert resume is not None
            assert resume.id is not None
            assert resume.file_url is not None

            # verify repository retrieval
            fetched = await res_repo.get_by_id(resume.id)
            assert fetched is not None

    asyncio.run(_inner())


def test_resume_upload_integration():
    _run_async_upload_test()
