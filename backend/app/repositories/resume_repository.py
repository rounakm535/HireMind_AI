import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.resume import Resume, InterviewQuestion
from app.models.match import MatchScore, EmailLog


class ResumeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, resume_id: uuid.UUID) -> Optional[Resume]:
        result = await self.db.execute(
            select(Resume)
            .options(
                selectinload(Resume.interview_questions),
                selectinload(Resume.match_scores),
            )
            .where(Resume.id == resume_id)
        )
        return result.scalars().first()

    async def create(self, resume: Resume) -> Resume:
        self.db.add(resume)
        await self.db.flush()
        return resume

    async def delete(self, resume: Resume) -> None:
        await self.db.delete(resume)
        await self.db.flush()

    async def get_by_candidate_id(self, candidate_id: uuid.UUID) -> List[Resume]:
        result = await self.db.execute(
            select(Resume).where(Resume.candidate_id == candidate_id).order_by(Resume.created_at.desc())
        )
        return list(result.scalars().all())

    # Match Scores
    async def create_match_score(self, match_score: MatchScore) -> MatchScore:
        self.db.add(match_score)
        await self.db.flush()
        return match_score

    async def get_match_scores_by_job_id(self, job_id: uuid.UUID) -> List[MatchScore]:
        result = await self.db.execute(
            select(MatchScore)
            .options(selectinload(MatchScore.candidate))
            .where(MatchScore.job_id == job_id)
            .order_by(MatchScore.score.desc())
        )
        return list(result.scalars().all())

    async def get_match_score(self, job_id: uuid.UUID, candidate_id: uuid.UUID) -> Optional[MatchScore]:
        result = await self.db.execute(
            select(MatchScore)
            .where(MatchScore.job_id == job_id, MatchScore.candidate_id == candidate_id)
        )
        return result.scalars().first()

    # Interview Questions
    async def create_interview_question(self, question: InterviewQuestion) -> InterviewQuestion:
        self.db.add(question)
        await self.db.flush()
        return question

    async def get_interview_questions_by_resume_id(self, resume_id: uuid.UUID) -> List[InterviewQuestion]:
        result = await self.db.execute(
            select(InterviewQuestion).where(InterviewQuestion.resume_id == resume_id)
        )
        return list(result.scalars().all())

    # Email Logs
    async def create_email_log(self, email_log: EmailLog) -> EmailLog:
        self.db.add(email_log)
        await self.db.flush()
        return email_log

    async def get_email_logs_by_sender(self, sender_id: uuid.UUID, limit: int = 50) -> List[EmailLog]:
        result = await self.db.execute(
            select(EmailLog)
            .where(EmailLog.sender_id == sender_id)
            .order_by(EmailLog.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_email_logs(self, limit: int = 100) -> List[EmailLog]:
        result = await self.db.execute(
            select(EmailLog)
            .order_by(EmailLog.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
