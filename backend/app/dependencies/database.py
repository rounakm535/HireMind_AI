from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.job_repository import JobRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.resume_repository import ResumeRepository


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_job_repository(db: AsyncSession = Depends(get_db)) -> JobRepository:
    return JobRepository(db)


def get_candidate_repository(db: AsyncSession = Depends(get_db)) -> CandidateRepository:
    return CandidateRepository(db)


def get_resume_repository(db: AsyncSession = Depends(get_db)) -> ResumeRepository:
    return ResumeRepository(db)
